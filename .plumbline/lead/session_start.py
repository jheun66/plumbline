"""Gives the lead its rules at the start of every session: prints the part of
the lead's rules named by its argument. An agent started as the implementer or
the verifier gets nothing."""

import json
import os
import sys

PARTS = {
    "1": "1-layers-and-roles.md",
    "2": "2-design-and-authoring.md",
    "3": "3-changes.md",
    "4": "4-setup-and-checks.md",
}

data = sys.stdin.read()
try:
    event = json.loads(data) if data.strip() else {}
except ValueError:
    event = {}
if isinstance(event, dict) and event.get("agent_type") in ("implementer", "verifier"):
    sys.exit(0)
root = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
with open(os.path.join(root, ".plumbline", "lead", PARTS[sys.argv[1]]), encoding="utf-8") as handle:
    sys.stdout.write(handle.read())
