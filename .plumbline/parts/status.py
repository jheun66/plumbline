"""status: reports the current state of the project.

Arguments: none. Standard input: empty, or the output of `git ls-remote --tags`
run on the rules repository the setup record names.
"""

import sys

import plumbline_lib as lib

TAG_REF = "refs/tags/"
LAYER_ORDER = {"intent": 0, "design": 1, "impl": 2}


def read_record():
    """(record or None, invalid) with the checks status makes."""
    text = lib.read_text(lib.RECORD_PATH)
    if text is None:
        return None, False
    ok, obj = lib.load_json(text)
    if not ok or not isinstance(obj, dict):
        return None, True
    if "rules" not in obj or not lib.check_rules_key(obj["rules"]):
        return None, True
    if "settings" not in obj:
        return None, True
    settings = lib.check_settings(obj["settings"], look_at_files=False)
    if settings is None:
        return None, True
    return {"rules": obj["rules"], "settings": settings}, False


def tag_version(tag):
    name = tag[1:] if tag.startswith("v") else tag
    return name if lib.is_version(name) else None


def newer_rules(stdin_text, record):
    plain = {}
    peeled = {}
    for line in stdin_text.replace("\r\n", "\n").split("\n"):
        fields = line.split("\t")
        if len(fields) != 2 or not fields[0] or not fields[1]:
            continue
        commit, ref = fields
        if not ref.startswith(TAG_REF):
            continue
        tag = ref[len(TAG_REF):]
        if tag.endswith("^{}"):
            peeled[tag[:-3]] = commit
        elif tag:
            plain[tag] = commit
    best = None
    for tag in plain:
        version = tag_version(tag)
        if version is None:
            continue
        if best is None:
            best = (tag, version)
            continue
        order = lib.compare_versions(version, best[1])
        if order > 0 or (order == 0 and tag.encode() < best[0].encode()):
            best = (tag, version)
    if best is None:
        return ["rules-up-to-date"]
    tag, version = best
    commit = peeled.get(tag, plain[tag])
    rules = record["rules"]
    if commit == rules["commit"]:
        return ["rules-up-to-date"]
    own = tag_version(rules["tag"]) if "tag" in rules else None
    if own is not None and lib.compare_versions(own, version) >= 0:
        return ["rules-up-to-date"]
    return ["newer-rules", tag, commit]


def main():
    stdin_text = sys.stdin.buffer.read().decode("utf-8", "surrogateescape")
    invalid = set()
    lines = []

    settings_state, settings = lib.load_settings()
    if settings_state != "ok":
        invalid.add(lib.SETTINGS_PATH)

    record, record_invalid = read_record()
    if record_invalid:
        invalid.add(lib.RECORD_PATH)

    # Changes and the current change.
    changes = []
    change_values = {}
    for name in lib.change_folders():
        path = lib.CHANGES_DIR + "/" + name + "/change.md"
        values = lib.parse_change_md(path)
        if values is None:
            invalid.add(path)
            continue
        change_values[name] = values
    current = lib.current_change_name()
    if current is not None:
        values = change_values.get(current) if lib.change_folder_exists(current) else None
        if values is None or values["state"] != "open":
            invalid.add(lib.CURRENT_CHANGE_PATH)
            current = None
    gaps = []
    for name in sorted(change_values):
        values = change_values[name]
        if values["state"] not in ("open", "closed"):
            continue
        changes.append(["change", name, values["state"], values["diagnosis"],
                        "current" if name == current else "-"])
        for number, path in lib.gap_items(name):
            item = lib.parse_gap_item(path)
            if item is None:
                invalid.add(path)
                continue
            if item["state"] == "proposed":
                gaps.append((name, number, item["layer"]))

    # Layers, the design's README, bases.
    milestone = None
    layer_lines = []
    stale = []
    settings_changed = []
    if settings is not None:
        intent_present = lib.layer_present(settings, "intent")
        design_present = lib.layer_present(settings, "design")
        for name, present in (("intent", intent_present), ("design", design_present)):
            if not present:
                code = "skip" if name in settings["not_in_git"] else "missing-layer"
                layer_lines.append([code, name])
        intents = lib.intent_documents(settings) if intent_present else set()
        versions = {}

        def version_of(path):
            if path not in versions:
                versions[path] = lib.intent_version(path) if path in intents else None
            return versions[path]

        readme = lib.design_readme(settings)
        if design_present:
            for doc in lib.markdown_files(lib.design_location(settings)):
                is_readme = doc == readme
                if not intent_present and not is_readme:
                    continue
                text = lib.read_text(doc)
                pairs = lib.front_matter(text) if text is not None else None
                if pairs is None:
                    invalid.add(doc)
                    continue
                doc_stale = []
                bad = False
                if intent_present:
                    for value in lib.values_of(pairs, "basis"):
                        basis = lib.parse_basis(value)
                        if basis is None or version_of(basis[0]) is None:
                            bad = True
                            break
                        target, version = basis
                        if lib.compare_versions(version_of(target), version) > 0:
                            doc_stale.append(["stale", doc, target, version, version_of(target)])
                if bad:
                    invalid.add(doc)
                    continue
                stale.extend(doc_stale)
                if is_readme:
                    names = lib.values_of(pairs, "milestone")
                    if len(names) == 1:
                        milestone = names[0]

        if record is not None:
            old = record["settings"]
            for name in lib.LAYERS:
                now_paths = set(settings["layers"][name])
                then_paths = set(old["layers"][name])
                for path in now_paths - then_paths:
                    settings_changed.append([name, "added", path])
                for path in then_paths - now_paths:
                    settings_changed.append([name, "removed", path])
            now_out = set(settings["not_in_git"])
            then_out = set(old["not_in_git"])
            for name in now_out - then_out:
                settings_changed.append(["not_in_git", "added", name])
            for name in then_out - now_out:
                settings_changed.append(["not_in_git", "removed", name])

    for path in sorted(invalid, key=lambda p: p.encode("utf-8", "surrogateescape")):
        lines.append(["invalid", path])
    lines.append(["milestone", milestone] if milestone is not None else ["milestone-unknown"])
    if record is not None:
        rules = record["rules"]
        lines.append(["rules", rules["repository"], rules["commit"], rules.get("tag", "-")])
        if stdin_text == "":
            lines.append(["newer-rules-not-checked"])
        else:
            lines.append(newer_rules(stdin_text, record))
        settings_changed.sort(key=lambda f: (f[0].encode(), f[1] != "added", f[2].encode()))
        lines.extend(["settings-changed"] + fields for fields in settings_changed)
    else:
        lines.append(["rules-unknown"])
    lines.extend(changes)
    gaps.sort(key=lambda g: (g[0].encode(), g[1]))
    lines.extend(["gap", name, str(number), layer] for name, number, layer in gaps)
    layer_lines.sort(key=lambda f: LAYER_ORDER[f[1]])
    lines.extend(layer_lines)
    stale.sort(key=lambda f: (f[1].encode(), f[2].encode()))
    lines.extend(stale)
    lib.emit(lines, lib.PASS)


if __name__ == "__main__":
    try:
        main()
    except lib.EnvError as exc:
        lib.fail("status: %s" % exc)
