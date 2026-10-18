"""validate: checks design documents, change records and the setup against
their formats.

Arguments: exactly one, the mode: report or gate. Standard input: empty.
"""

import os
import re
import subprocess
import sys

import plumbline_lib as lib

RENDER_SECONDS = 60
LAYER_ORDER = {"intent": 0, "design": 1, "impl": 2}
TOKEN_SPLIT = re.compile(r"[\s`\"'()\[\]<>{}|]+")
LINK = re.compile(r"\]\(([^)]*)\)")

# Codes in the order of their groups, and which fields are line numbers.
DESIGN_CODES = ["basis", "basis-target", "stale", "sections", "marker",
                "impl-path", "figure", "decision-link"]
NUMBER_FIELDS = {"marker": {1}, "impl-path": {1}, "figure": {1}, "decision-link": {1}}


# ---------------------------------------------------------------- Markdown


def fences(lines):
    """For each line: 'open', 'inside', 'close' or None; and for each opening
    line, its info string's first word or None."""
    kinds = [None] * len(lines)
    first_words = {}
    index = 0
    while index < len(lines):
        line = lines[index]
        match = re.match(r"(`{3,}|~{3,})(.*)\Z", line, re.S)
        if not match:
            index += 1
            continue
        fence = match.group(1)
        word = None
        stripped = match.group(2).lstrip(" \t")
        if stripped:
            word = re.match(r"[^ \t]+", stripped).group(0)
        kinds[index] = "open"
        first_words[index] = word
        char, size = fence[0], len(fence)
        close = None
        for later in range(index + 1, len(lines)):
            run = re.match(re.escape(char) + "+", lines[later])
            if run and len(run.group(0)) >= size:
                close = later
                break
        end = close if close is not None else len(lines)
        for inner in range(index + 1, end):
            kinds[inner] = "inside"
        if close is not None:
            kinds[close] = "close"
            index = close + 1
        else:
            index = len(lines)
    return kinds, first_words


def headings(lines, kinds):
    """(line index, text) of every level-2 heading."""
    found = []
    for index, line in enumerate(lines):
        if kinds[index] is None and line.startswith("## "):
            found.append((index, line[3:].rstrip(" ")))
    return found


def figures_of(lines, kinds, first_words, names):
    """(opening line index, name, text) of every figure."""
    found = []
    for index, word in first_words.items():
        if word in names:
            end = index + 1
            while end < len(lines) and kinds[end] == "inside":
                end += 1
            text = "".join(line + "\n" for line in lines[index + 1:end])
            found.append((index, word, text))
    return sorted(found)


# ---------------------------------------------------------------- template


def read_template():
    """(titles, confirmed, pending, figure names) or None when not valid."""
    text = lib.read_text(lib.TEMPLATE_PATH)
    if text is None:
        return None
    pairs = lib.front_matter(text)
    if pairs is None:
        return None
    names = [name for name, _ in pairs]
    if names.count("confirmed") != 1 or names.count("pending") != 1:
        return None
    if any(name not in ("confirmed", "pending", "figure") for name in names):
        return None
    confirmed = lib.values_of(pairs, "confirmed")[0]
    pending = lib.values_of(pairs, "pending")[0]
    if confirmed.count("YYYY-MM-DD") != 1:
        return None
    lines = lib.lines_of(text)
    kinds, _ = fences(lines)
    titles = [title for _, title in headings(lines, kinds)]
    if len(titles) != 7:
        return None
    return titles, confirmed, pending, lib.values_of(pairs, "figure")


# ---------------------------------------------------------------- markers


def common_beginning(a, b):
    size = 0
    while size < len(a) and size < len(b) and a[size] == b[size]:
        size += 1
    return a[:size]


def is_marker(rest, confirmed, pending):
    if rest.startswith(pending):
        return True
    before, after = confirmed.split("YYYY-MM-DD", 1)
    if not rest.startswith(before):
        return False
    date = rest[len(before):len(before) + 10]
    if not lib.is_date(date):
        return False
    return rest[len(before) + 10:].startswith(after)


def bad_marker(line, prefix, confirmed, pending):
    start = line.find(prefix)
    while start != -1:
        if not is_marker(line[start:], confirmed, pending):
            return True
        start = line.find(prefix, start + 1)
    return False


# ---------------------------------------------------------------- impl paths


def impl_tokens(line, impl_paths):
    found = []
    for token in TOKEN_SPLIT.split(line):
        token = token.rstrip(".,;:!?")
        if token.startswith("./"):
            token = token[2:]
        if not token:
            continue
        for path in impl_paths:
            if token.startswith(path + "/") or (token == path and ("/" in path or "." in path)):
                found.append(token)
                break
    return found


# ---------------------------------------------------------------- decision links


def decision_target(doc, target):
    """The change name a link target leads to, or None."""
    if target == "" or target.startswith("/"):
        return None
    head = target.split("/", 1)[0]
    if ":" in head:
        return None
    segments = doc.split("/")[:-1]
    for segment in target.split("/"):
        if segment in ("", "."):
            continue
        if segment == "..":
            if not segments:
                return None
            segments.pop()
            continue
        segments.append(segment)
    if len(segments) == 3 and segments[:2] == [".plumbline", "changes"]:
        return segments[2]
    return None


def has_confirmed_design_gap(change):
    if not os.path.isdir(lib.CHANGES_DIR + "/" + change):
        return False
    for _, path in lib.gap_items(change):
        item = lib.parse_gap_item(path)
        if item is not None and item["layer"] == "design" and item["state"] == "confirmed":
            return True
    return False


# ---------------------------------------------------------------- renderers


class Renderer:
    def __init__(self, command):
        self.command = command
        self.missing = False

    def renders(self, text):
        """True, False, or None when the program cannot be started."""
        try:
            process = subprocess.Popen(self.command, stdin=subprocess.PIPE,
                                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except OSError:
            self.missing = True
            return None
        try:
            process.communicate(text.encode("utf-8", "surrogateescape"), timeout=RENDER_SECONDS)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
            return False
        except BrokenPipeError:
            process.wait()
        return process.returncode == 0


# ---------------------------------------------------------------- main


def main(args):
    if len(args) != 1 or args[0] not in ("report", "gate"):
        lib.fail("validate: give exactly one argument, report or gate")
    mode = args[0]
    problems = set()
    skips = set()

    def problem(*fields):
        problems.add(tuple(fields))

    # Settings and layers.
    settings_state, settings = lib.load_settings()
    if settings_state != "ok":
        problem("settings", lib.SETTINGS_PATH)
    present = {}
    if settings is not None:
        for name in lib.LAYERS:
            present[name] = lib.layer_present(settings, name)
            if not present[name]:
                if name in settings["not_in_git"]:
                    skips.add(("skip", "layer", name))
                else:
                    problem("missing-layer", name)

    # The setup record and the files it lists.
    record_state, record = lib.load_record()
    if record_state != "ok":
        problem("record", lib.RECORD_PATH)
    else:
        for entry in record["files"]:
            state, checksum = lib.checksum_of(entry["path"], entry.get("begin"), entry.get("end"))
            if state == "missing":
                problem("checksum", entry["path"])
            elif state == "no-part":
                problem("part-not-found", entry["path"])
            elif checksum != entry["checksum"]:
                problem("checksum", entry["path"])

    # The template.
    template = read_template()
    if template is None:
        problem("template", lib.TEMPLATE_PATH)

    # Design documents.
    if settings is not None and present["design"]:
        check_design(mode, settings, present, template, record, problem, skips)

    # Change records.
    for name in lib.change_folders():
        folder = lib.CHANGES_DIR + "/" + name
        if lib.parse_change_md(folder + "/change.md") is None:
            problem("change", folder + "/change.md")
        for _, path in lib.gap_items(name):
            if lib.parse_gap_item(path) is None:
                problem("change", path)
        verify = folder + "/verify.md"
        if os.path.lexists(verify) and lib.parse_verify_result(verify) is None:
            problem("change", verify)
    current = lib.current_change_name()
    if current is not None and not lib.open_change(current):
        problem("change", lib.CURRENT_CHANGE_PATH)

    # Files kept out of git.
    if settings is not None:
        if lib.is_git_root():
            kept_out = [path for name in settings["not_in_git"]
                        for path in settings["layers"][name]]
            for tracked in lib.tracked_files():
                if any(lib.lies_in(tracked, path) for path in kept_out):
                    problem("tracked", tracked)
        else:
            skips.add(("skip", "tracked", "not-git"))

    lines = order(problems, skips)
    blocked = mode == "gate" and bool(problems)
    lib.emit(lines, lib.BLOCK if blocked else lib.PASS)


def check_design(mode, settings, present, template, record, problem, skips):
    readme = lib.design_readme(settings)
    text = lib.read_text(readme) if os.path.isfile(readme) else None
    pairs = lib.front_matter(text) if text is not None else None
    if pairs is None or len(lib.values_of(pairs, "milestone")) != 1:
        problem("milestone", readme)

    intents = lib.intent_documents(settings) if present["intent"] else set()
    versions = {}

    def version_of(path):
        if path not in versions:
            versions[path] = lib.intent_version(path) if path in intents else None
        return versions[path]

    impl_paths = settings["layers"]["impl"]
    figure_names = set(template[3]) if template is not None else set()
    renderers = {}
    if record is not None:
        for entry in record["renderers"]:
            renderers[entry["figure"]] = Renderer(entry["command"])
    used_names = set()

    for doc in lib.markdown_files(lib.design_location(settings)):
        text = lib.read_text(doc)
        if text is None:
            problem("basis", doc)
            continue
        lines = lib.lines_of(text)
        kinds, first_words = fences(lines)
        is_module = doc != readme

        # Basis lines.
        pairs = lib.front_matter(text)
        bases = []
        if pairs is not None:
            for value in lib.values_of(pairs, "basis"):
                basis = lib.parse_basis(value)
                if basis is None:
                    bases = None
                    break
                bases.append(basis)
        if pairs is None or not bases:
            problem("basis", doc)
        elif present["intent"]:
            for path, version in bases:
                target_version = version_of(path)
                if target_version is None:
                    problem("basis-target", doc, path)
                elif lib.compare_versions(target_version, version) > 0:
                    problem("stale", doc, path, version, target_version)

        found = headings(lines, kinds)

        # Sections and markers.
        if is_module and template is not None:
            titles, confirmed, pending, _ = template
            if [title for _, title in found] != titles:
                problem("sections", doc)
            prefix = common_beginning(confirmed, pending)
            if prefix:
                for index, line in enumerate(lines):
                    if bad_marker(line, prefix, confirmed, pending):
                        problem("marker", doc, str(index + 1))

        # Impl paths.
        for index, line in enumerate(lines):
            for token in impl_tokens(line, impl_paths):
                problem("impl-path", doc, str(index + 1), token)

        # Figures.
        if template is not None:
            for index, name, figure_text in figures_of(lines, kinds, first_words, figure_names):
                used_names.add(name)
                if mode != "gate":
                    continue
                renderer = renderers.get(name)
                if renderer is None or renderer.missing:
                    continue
                result = renderer.renders(figure_text)
                if result is False:
                    problem("figure", doc, str(index + 1), name)

        # Decision links.
        if is_module and len(found) >= 5:
            start = found[4][0] + 1
            stop = found[5][0] if len(found) >= 6 else len(lines)
            for index in range(start, stop):
                for target in LINK.findall(lines[index]):
                    target = target.split("#", 1)[0]
                    change = decision_target(doc, target)
                    if change is not None and not has_confirmed_design_gap(change):
                        problem("decision-link", doc, str(index + 1), change)

    if template is not None and used_names:
        if mode == "report":
            skips.add(("skip", "figures", "report"))
        else:
            for name in used_names:
                renderer = renderers.get(name)
                if renderer is None or renderer.missing:
                    skips.add(("skip", "figures", name))


def sort_key(fields):
    numbers = NUMBER_FIELDS.get(fields[0], set())
    key = []
    for position, field in enumerate(fields[1:]):
        if position in numbers:
            key.append((0, int(field), b""))
        else:
            key.append((1, 0, field.encode("utf-8", "surrogateescape")))
    return key


def order(problems, skips):
    def group(code):
        return sorted((f for f in problems if f[0] == code), key=sort_key)

    lines = group("settings")
    lines += sorted((f for f in problems if f[0] == "missing-layer"), key=lambda f: LAYER_ORDER[f[1]])
    for code in ["record", "checksum", "part-not-found", "template", "milestone"]:
        lines += group(code)
    for code in DESIGN_CODES:
        lines += group(code)
    lines += group("change")
    lines += group("tracked")
    skip_lines = sorted(
        skips,
        key=lambda f: ({"layer": 0, "figures": 1, "tracked": 2}[f[1]],
                       LAYER_ORDER.get(f[2], 0) if f[1] == "layer" else 0,
                       f[2].encode("utf-8", "surrogateescape")),
    )
    return [list(f) for f in lines + skip_lines]


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except lib.EnvError as exc:
        lib.fail("validate: %s" % exc)
