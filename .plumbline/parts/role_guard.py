"""role-guard: blocks reads and writes outside a role's row of the role table.

Arguments: the role (lead, implementer, verifier), the action (read, write),
then the paths the action touches. Standard input: empty.
"""

import os
import sys

import plumbline_lib as lib

# The cells of the role table: r = read, w = write.
ALLOW = {
    "intent": {"lead": "rw", "implementer": "", "verifier": ""},
    "design": {"lead": "rw", "implementer": "r", "verifier": "r"},
    "impl": {"lead": "", "implementer": "rw", "verifier": "r"},
    "verify-result": {"lead": "r", "implementer": "", "verifier": "rw"},
    "change-record": {"lead": "rw", "implementer": "", "verifier": ""},
    "current-change": {"lead": "rw", "implementer": "", "verifier": ""},
    "settings": {"lead": "rw", "implementer": "r", "verifier": "r"},
    "carrier-own": {"lead": "rw", "implementer": "r", "verifier": "r"},
    "carrier-other": {"lead": "rw", "implementer": "", "verifier": ""},
    "setup-file": {"lead": "rw", "implementer": "", "verifier": ""},
    "exclude": {"lead": "rw", "implementer": "", "verifier": ""},
    "project-file": {"lead": "r", "implementer": "r", "verifier": "r"},
    "not-project": {"lead": "rw", "implementer": "rw", "verifier": "rw"},
}


class Guard:
    def __init__(self, role, action, settings):
        self.role = role
        self.action = action
        self.settings = settings
        self.record = None
        self.git_root = lib.is_git_root()

    # The row of a path: (number, name), numbered as in the rules' table.
    # Rows 1 to 8 need no setup record.
    def early_row(self, path):
        if path is None:
            return 1, "not-project"
        if path == lib.EXCLUDE_PATH:
            return 2, "exclude"
        if lib.lies_in(path, ".git"):
            return 3, "not-project"
        layer = lib.layer_of(path, self.settings)
        if layer is not None:
            return 4, layer
        if path == lib.CURRENT_CHANGE_PATH:
            return 5, "current-change"
        parts = path.split("/")
        if len(parts) == 4 and parts[:2] == [".plumbline", "changes"] and parts[3] == "verify.md":
            return 6, "verify-result"
        if lib.lies_in(path, lib.CHANGES_DIR):
            return 7, "change-record"
        if path == lib.SETTINGS_PATH:
            return 8, "settings"
        return None

    def row(self, path):
        early = self.early_row(path)
        if early is not None:
            return early
        if path in self.carrier_roles:
            return 9, "carrier"
        if path == lib.RECORD_PATH or path in self.record_files:
            return 10, "setup-file"
        if path != "" and self.git_root and lib.git_ignores(path):
            return 11, "not-project"
        return 12, "project-file"

    def load_record(self):
        state, record = lib.load_record()
        if state != "ok":
            lib.fail("role-guard: the setup record %s is %s" % (lib.RECORD_PATH, state))
        self.record = record
        self.record_files = {entry["path"] for entry in record["files"]}
        self.carrier_roles = {}
        for carrier in record["carriers"]:
            for path in carrier["files"]:
                self.carrier_roles.setdefault(path, set()).update(carrier["roles"])

    def cell(self, path, row_name):
        if row_name == "carrier":
            own = self.role in self.carrier_roles.get(path, ())
            return ALLOW["carrier-own" if own else "carrier-other"][self.role]
        return ALLOW[row_name][self.role]

    def allowed(self, path, row_name, action):
        letter = "r" if action == "read" else "w"
        if letter not in self.cell(path, row_name):
            return False
        if row_name == "verify-result" and self.role == "verifier":
            change = path.split("/")[2]
            values = lib.parse_change_md(lib.CHANGES_DIR + "/" + change + "/change.md")
            if values is None or values["state"] != "closed":
                return False
        return True

    def contained(self, folder, with_record):
        """Paths a folder contains that the folder rule looks for."""
        found = []
        for name in lib.LAYERS:
            found.extend(self.settings["layers"][name])
        found.append(lib.CURRENT_CHANGE_PATH)
        found.append(lib.EXCLUDE_PATH)
        found.extend(lib.CHANGES_DIR + "/" + name for name in lib.change_folders())
        if with_record:
            found.extend(self.carrier_roles)
            found.append(lib.RECORD_PATH)
            found.extend(self.record_files)
        if folder == "":
            return found
        return [path for path in found if path.startswith(folder + "/")]

    def decide(self, arg, path):
        """The block line for the path, or None when it passes."""
        number, row_name = self.row(path)
        shown = "." if path == "" else (arg if path is None else path)
        if not self.allowed(path, row_name, self.action):
            return ["block", shown, self.role, self.action, row_name]
        if self.action == "read" and path is not None and os.path.isdir(path or "."):
            with_record = self.early_row(path) is None
            worst = None
            for inner in self.contained(path, with_record):
                inner_number, inner_row = self.row(inner)
                if not self.allowed(inner, inner_row, "read"):
                    if worst is None or inner_number < worst[0]:
                        worst = (inner_number, inner_row)
            if worst is not None:
                return ["block", shown, self.role, self.action, worst[1]]
        return None


def main(args):
    if len(args) <= 2:
        lib.emit([], lib.PASS)
    role, action, raw = args[0], args[1], args[2:]
    if role not in lib.ROLES or action not in ("read", "write"):
        lib.fail("role-guard: the leading arguments must be a role and read or write, "
                 "not %r %r" % (role, action))

    state, settings = lib.load_settings()
    if state != "ok":
        lib.fail("role-guard: the settings file %s is %s" % (lib.SETTINGS_PATH, state))

    guard = Guard(role, action, settings)
    root = lib.cwd_segments()
    paths = [(arg, lib.project_path(arg, root)) for arg in raw]
    if any(guard.early_row(path) is None for _, path in paths):
        guard.load_record()
    else:
        guard.record_files = set()
        guard.carrier_roles = {}

    lines = []
    for arg, path in paths:
        line = guard.decide(arg, path)
        if line is not None:
            lines.append(line)
    lib.emit(lines, lib.BLOCK if lines else lib.PASS)


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except lib.EnvError as exc:
        lib.fail("role-guard: %s" % exc)
