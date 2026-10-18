"""Helpers shared by the plumbline mechanical parts.

Every part runs with the project root as its working directory and finds the
project only through it.
"""

import datetime
import hashlib
import json
import os
import re
import subprocess
import sys

LAYERS = ("intent", "design", "impl")
ROLES = ("lead", "implementer", "verifier")
PART_NAMES = ("status", "gap-guard", "role-guard", "validate")
RULE_NAMES = (
    "role table",
    "gap guard",
    "validate at the end of a turn",
    "validate in CI",
)

SETTINGS_PATH = ".plumbline/settings.json"
RECORD_PATH = ".plumbline/setup-record.json"
TEMPLATE_PATH = ".plumbline/template.md"
CHANGES_DIR = ".plumbline/changes"
CURRENT_CHANGE_PATH = ".plumbline/current-change"
EXCLUDE_PATH = ".git/info/exclude"

PASS = 0
BLOCK = 3
ERROR = 2


class EnvError(Exception):
    """A problem with the environment: the part gives `error`."""


# ---------------------------------------------------------------- output


def emit(lines, verdict):
    out = sys.stdout.buffer
    for fields in lines:
        out.write("\t".join(fields).encode("utf-8", "surrogateescape") + b"\n")
    out.flush()
    sys.exit(verdict)


def fail(message):
    sys.stderr.write(message.rstrip("\n") + "\n")
    sys.stderr.flush()
    sys.exit(ERROR)


# ---------------------------------------------------------------- files


def read_bytes(path):
    try:
        with open(path, "rb") as handle:
            return handle.read()
    except OSError:
        return None


def read_text(path):
    data = read_bytes(path)
    if data is None:
        return None
    return data.replace(b"\r\n", b"\n").decode("utf-8", "surrogateescape")


def lines_of(text):
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    return lines


def markdown_files(location):
    """The Markdown files at a location, as relative paths, sorted."""
    if os.path.isfile(location):
        return [location] if location.endswith(".md") else []
    found = []
    if os.path.isdir(location):
        for root, dirs, files in os.walk(location):
            dirs.sort()
            for name in files:
                path = os.path.join(root, name)
                if name.endswith(".md") and os.path.isfile(path):
                    found.append(path.replace(os.sep, "/"))
    return sorted(found)


# ---------------------------------------------------------------- front matter

FM_LINE = re.compile(r"([a-z0-9_-]+): (.*)\Z", re.S)


def front_matter(text):
    """The front matter as a list of (key, value), or None when the document
    has no valid front matter."""
    lines = text.split("\n")
    if not lines or lines[0] != "---":
        return None
    close = None
    for index in range(1, len(lines)):
        if lines[index] == "---":
            close = index
            break
    if close is None:
        return None
    pairs = []
    for line in lines[1:close]:
        match = FM_LINE.match(line)
        if not match:
            return None
        value = match.group(2).rstrip(" \t")
        if value == "":
            return None
        pairs.append((match.group(1), value))
    return pairs


def values_of(pairs, key):
    return [value for name, value in pairs if name == key]


# ---------------------------------------------------------------- versions

VERSION = re.compile(r"[0-9]+(\.[0-9]+)*\Z")


def is_version(text):
    return bool(VERSION.match(text))


def version_key(text):
    return [int(part) for part in text.split(".")]


def compare_versions(a, b):
    left, right = version_key(a), version_key(b)
    size = max(len(left), len(right))
    left += [0] * (size - len(left))
    right += [0] * (size - len(right))
    return (left > right) - (left < right)


DATE = re.compile(r"([0-9]{4})-([0-9]{2})-([0-9]{2})\Z")


def is_date(text):
    match = DATE.match(text)
    if not match:
        return False
    try:
        datetime.date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
    except ValueError:
        return False
    return True


# ---------------------------------------------------------------- JSON


def load_json(text):
    """(True, value) or (False, None). Duplicate keys make it not valid."""

    def pairs_hook(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate key")
            result[key] = value
        return result

    try:
        return True, json.loads(text, object_pairs_hook=pairs_hook)
    except (ValueError, RecursionError):
        return False, None


def is_str_list(value, non_empty=False):
    if not isinstance(value, list):
        return False
    if non_empty and not value:
        return False
    return all(isinstance(item, str) for item in value)


# ---------------------------------------------------------------- settings


def valid_path_form(path):
    if not isinstance(path, str) or path == "":
        return False
    return all(segment not in ("", ".", "..") for segment in path.split("/"))


def lies_in(path, location):
    return path == location or path.startswith(location + "/")


def check_settings(obj, look_at_files):
    """The settings when obj has the form of the settings file, else None."""
    if not isinstance(obj, dict) or set(obj) != {"layers", "not_in_git"}:
        return None
    layers = obj["layers"]
    kept_out = obj["not_in_git"]
    if not isinstance(layers, dict) or set(layers) != set(LAYERS):
        return None
    for name in LAYERS:
        paths = layers[name]
        if not is_str_list(paths, non_empty=True):
            return None
        if not all(valid_path_form(path) for path in paths):
            return None
    if len(layers["design"]) != 1:
        return None
    if not is_str_list(kept_out) or not all(name in LAYERS for name in kept_out):
        return None
    for first in LAYERS:
        for second in LAYERS:
            if first == second:
                continue
            for a in layers[first]:
                for b in layers[second]:
                    if lies_in(a, b) or lies_in(b, a):
                        return None
    if look_at_files and os.path.isfile(layers["design"][0]):
        return None
    return {
        "layers": {name: list(layers[name]) for name in LAYERS},
        "not_in_git": list(kept_out),
    }


def load_settings():
    """('missing' | 'invalid' | 'ok', settings or None)."""
    text = read_text(SETTINGS_PATH)
    if text is None:
        return "missing", None
    ok, obj = load_json(text)
    if not ok:
        return "invalid", None
    settings = check_settings(obj, look_at_files=True)
    if settings is None:
        return "invalid", None
    return "ok", settings


def layer_of(path, settings):
    for name in LAYERS:
        for location in settings["layers"][name]:
            if lies_in(path, location):
                return name
    return None


def layer_present(settings, name):
    return any(os.path.exists(path) for path in settings["layers"][name])


def design_location(settings):
    return settings["layers"]["design"][0]


def design_readme(settings):
    return design_location(settings) + "/README.md"


# ---------------------------------------------------------------- intent


def intent_documents(settings):
    found = set()
    for location in settings["layers"]["intent"]:
        found.update(markdown_files(location))
    return found


def intent_version(path):
    """The intent document's valid version, or None."""
    text = read_text(path)
    if text is None:
        return None
    pairs = front_matter(text)
    if pairs is None:
        return None
    versions = values_of(pairs, "version")
    if len(versions) != 1 or not is_version(versions[0]):
        return None
    return versions[0]


def parse_basis(value):
    """(path, version) when value is a path, one space and a version."""
    if " " not in value:
        return None
    path, version = value.rsplit(" ", 1)
    if not valid_path_form(path) or not is_version(version):
        return None
    return path, version


# ---------------------------------------------------------------- changes

STATES = ("open", "closed", "archived")
DIAGNOSES = ("impl", "design", "intent")
GAP_NAME = re.compile(r"gap-([1-9][0-9]*)\.md\Z")


def exactly_keys(pairs, keys):
    names = [name for name, _ in pairs]
    return sorted(names) == sorted(keys)


def parse_change_md(path):
    """{'state', 'diagnosis'} when change.md has its form, else None."""
    text = read_text(path)
    if text is None:
        return None
    pairs = front_matter(text)
    if pairs is None or not exactly_keys(pairs, ["state", "diagnosis"]):
        return None
    values = dict(pairs)
    if values["state"] not in STATES or values["diagnosis"] not in DIAGNOSES:
        return None
    return values


def parse_gap_item(path):
    """{'layer', 'state', 'date'?} when the gap item has its form, else None."""
    text = read_text(path)
    if text is None:
        return None
    pairs = front_matter(text)
    if pairs is None:
        return None
    values = dict(pairs)
    state = values.get("state")
    if state == "proposed":
        keys = ["layer", "state"]
    elif state in ("confirmed", "rejected"):
        keys = ["layer", "state", "date"]
    else:
        return None
    if not exactly_keys(pairs, keys):
        return None
    if values["layer"] not in ("intent", "design"):
        return None
    if "date" in values and not is_date(values["date"]):
        return None
    return values


def parse_verify_result(path):
    text = read_text(path)
    if text is None:
        return None
    pairs = front_matter(text)
    if pairs is None or not exactly_keys(pairs, ["result"]):
        return None
    if pairs[0][1] not in ("clean", "findings"):
        return None
    return pairs[0][1]


def change_folders():
    """Names of the folders directly under .plumbline/changes/, sorted."""
    if not os.path.isdir(CHANGES_DIR):
        return []
    try:
        names = os.listdir(CHANGES_DIR)
    except OSError:
        return []
    return sorted(name for name in names if os.path.isdir(CHANGES_DIR + "/" + name))


def gap_items(change):
    """(number, path) of every gap item file in a change folder, by number."""
    folder = CHANGES_DIR + "/" + change
    try:
        names = os.listdir(folder)
    except OSError:
        return []
    items = []
    for name in names:
        match = GAP_NAME.match(name)
        path = folder + "/" + name
        if match and os.path.isfile(path):
            items.append((int(match.group(1)), path))
    return sorted(items)


def current_change_name():
    """The name in .plumbline/current-change, or None when there is none."""
    data = read_bytes(CURRENT_CHANGE_PATH)
    if data is None:
        return None
    text = data.replace(b"\r\n", b"\n").decode("utf-8", "surrogateescape")
    if text.endswith("\n"):
        text = text[:-1]
    return text or None


def change_folder_exists(name):
    if "/" in name or name in (".", "..") or "\n" in name:
        return False
    return os.path.isdir(CHANGES_DIR + "/" + name)


def open_change(name):
    """True when name is a change folder whose change.md has the form and
    state open."""
    if not change_folder_exists(name):
        return False
    values = parse_change_md(CHANGES_DIR + "/" + name + "/change.md")
    return values is not None and values["state"] == "open"


# ---------------------------------------------------------------- setup record

SHA = re.compile(r"sha256:[0-9a-f]{64}\Z")
COMMIT = re.compile(r"([0-9a-f]{40}|[0-9a-f]{64})\Z")


def check_rules_key(rules):
    if not isinstance(rules, dict):
        return False
    keys = set(rules)
    if not {"repository", "commit"} <= keys <= {"repository", "commit", "tag"}:
        return False
    if not isinstance(rules["repository"], str) or rules["repository"] == "":
        return False
    if not isinstance(rules["commit"], str) or not COMMIT.match(rules["commit"]):
        return False
    if "tag" in rules and (not isinstance(rules["tag"], str) or rules["tag"] == ""):
        return False
    return True


def is_line_text(value):
    return isinstance(value, str) and value != "" and "\n" not in value and "\r" not in value


def check_record(obj):
    """True when obj is a valid setup record."""
    keys = {"rules", "settings", "files", "carriers", "parts", "renderers", "enforcement"}
    if not isinstance(obj, dict) or set(obj) != keys:
        return False
    if not check_rules_key(obj["rules"]):
        return False
    if check_settings(obj["settings"], look_at_files=False) is None:
        return False

    files = obj["files"]
    if not isinstance(files, list):
        return False
    listed = set()
    for entry in files:
        if not isinstance(entry, dict):
            return False
        if set(entry) not in ({"path", "checksum"}, {"path", "checksum", "begin", "end"}):
            return False
        if not valid_path_form(entry["path"]) or entry["path"] in listed:
            return False
        listed.add(entry["path"])
        if not isinstance(entry["checksum"], str) or not SHA.match(entry["checksum"]):
            return False
        if "begin" in entry and not (is_line_text(entry["begin"]) and is_line_text(entry["end"])):
            return False

    carriers = obj["carriers"]
    if not isinstance(carriers, list):
        return False
    for carrier in carriers:
        if not isinstance(carrier, dict) or set(carrier) != {"kind", "files", "roles"}:
            return False
        if not isinstance(carrier["kind"], str) or carrier["kind"] == "":
            return False
        if not is_str_list(carrier["files"]) or not all(path in listed for path in carrier["files"]):
            return False
        roles = carrier["roles"]
        if not is_str_list(roles, non_empty=True):
            return False
        if not all(role in ROLES for role in roles) or len(set(roles)) != len(roles):
            return False

    parts = obj["parts"]
    if not isinstance(parts, list):
        return False
    part_names = set()
    for part in parts:
        if not isinstance(part, dict) or set(part) != {"name", "runner", "entry"}:
            return False
        if part["name"] not in PART_NAMES:
            return False
        if not is_str_list(part["runner"]):
            return False
        if not isinstance(part["entry"], str) or part["entry"] not in listed:
            return False
        part_names.add(part["name"])

    renderers = obj["renderers"]
    if not isinstance(renderers, list):
        return False
    figures = set()
    for renderer in renderers:
        if not isinstance(renderer, dict) or set(renderer) != {"figure", "command"}:
            return False
        figure = renderer["figure"]
        if not isinstance(figure, str) or figure == "" or figure in figures:
            return False
        figures.add(figure)
        if not is_str_list(renderer["command"], non_empty=True):
            return False

    enforcement = obj["enforcement"]
    if not isinstance(enforcement, list):
        return False
    for entry in enforcement:
        if not isinstance(entry, dict):
            return False
        if entry.get("by") == "mechanical":
            if set(entry) != {"rule", "by", "part"}:
                return False
            if not isinstance(entry["part"], str) or entry["part"] not in part_names:
                return False
        elif entry.get("by") == "instruction":
            if set(entry) != {"rule", "by"}:
                return False
        else:
            return False
        if entry["rule"] not in RULE_NAMES:
            return False
    return True


def load_record():
    """('missing' | 'invalid' | 'ok', record or None), with the full check."""
    text = read_text(RECORD_PATH)
    if text is None:
        return "missing", None
    ok, obj = load_json(text)
    if not ok or not check_record(obj):
        return "invalid", None
    return "ok", obj


def checksum_of(path, begin=None, end=None):
    """('ok', checksum), ('missing', None) or ('no-part', None)."""
    if not os.path.isfile(path):
        return "missing", None
    data = read_bytes(path)
    if data is None:
        return "missing", None
    data = data.replace(b"\r\n", b"\n")
    if begin is not None:
        begin_b = begin.encode("utf-8", "surrogateescape")
        end_b = end.encode("utf-8", "surrogateescape")
        starts = []
        offset = 0
        pieces = data.split(b"\n")
        if pieces and pieces[-1] == b"":
            pieces.pop()
        for piece in pieces:
            starts.append(offset)
            offset += len(piece) + 1
        begins = [i for i, piece in enumerate(pieces) if piece == begin_b]
        ends = [i for i, piece in enumerate(pieces) if piece == end_b]
        if len(begins) != 1 or len(ends) != 1 or begins[0] >= ends[0]:
            return "no-part", None
        first, last = begins[0], ends[0]
        stop = min(starts[last] + len(pieces[last]) + 1, len(data))
        data = data[starts[first]:stop]
    return "ok", "sha256:" + hashlib.sha256(data).hexdigest()


# ---------------------------------------------------------------- git


def git_env():
    env = dict(os.environ)
    for name in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_COMMON_DIR"):
        env.pop(name, None)
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    env["GIT_CONFIG_GLOBAL"] = os.devnull
    env["XDG_CONFIG_HOME"] = os.path.join(os.getcwd(), ".git", "plumbline-no-config")
    return env


def run_git(args):
    command = ["git", "-c", "core.excludesFile=" + os.devnull, "-c", "core.quotePath=false"] + args
    try:
        return subprocess.run(command, capture_output=True, env=git_env(), stdin=subprocess.DEVNULL)
    except OSError as exc:
        raise EnvError("git cannot be started: %s" % exc)


def is_git_root():
    return os.path.lexists(".git")


def tracked_files():
    result = run_git(["ls-files", "-z"])
    if result.returncode != 0:
        raise EnvError("git ls-files failed: %s" % result.stderr.decode("utf-8", "replace"))
    names = result.stdout.decode("utf-8", "surrogateescape").split("\0")
    return [name for name in names if name]


def git_ignores(path):
    result = run_git(["check-ignore", "-q", "--", path])
    if result.returncode == 0:
        return True
    if result.returncode == 1:
        return False
    raise EnvError("git check-ignore failed: %s" % result.stderr.decode("utf-8", "replace"))


# ---------------------------------------------------------------- guard paths


def cwd_segments():
    return [segment for segment in os.getcwd().split("/") if segment]


def project_path(arg, root_segments):
    """The path relative to the project root ('' for the root itself), or
    None when it lies outside the project root."""
    if arg.startswith("/"):
        segments = []
    else:
        segments = list(root_segments)
    for segment in arg.split("/"):
        if segment in ("", "."):
            continue
        if segment == "..":
            if segments:
                segments.pop()
            continue
        segments.append(segment)
    if segments[: len(root_segments)] != root_segments:
        return None
    return "/".join(segments[len(root_segments):])
