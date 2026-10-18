"""Connects validate, in report mode, to the hook that runs when the lead ends
a turn. When validate gives a problem line, it gives the lead all its lines and
lets the lead go on once. It never holds the lead back more than once in a
turn, and never blocks."""

import json
import sys

import connector_lib as lib

event = lib.hook_input()
if lib.role_of(event) != "lead" or event.get("stop_hook_active"):
    sys.exit(0)
verdict, lines, err = lib.run_part("validate", ["report"])
if verdict == "error":
    reason = "Environment error: validate in report mode could not run (%s)." % err
elif any(not line.startswith("skip\t") for line in lines):
    reason = "validate in report mode, at the end of this turn:\n" + "\n".join(lines)
else:
    sys.exit(0)
print(json.dumps({"decision": "block", "reason": reason}))
