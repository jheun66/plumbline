"""Helpers shared by the plumbline connectors. A connector only translates:
what the agent or CI gives into a part's arguments, and the part's verdict
into what the agent or CI understands."""

import json
import os
import subprocess
import sys

PARTS = {
    "status": ["python3", "-B", ".plumbline/parts/status.py"],
    "gap-guard": ["python3", "-B", ".plumbline/parts/gap_guard.py"],
    "role-guard": ["python3", "-B", ".plumbline/parts/role_guard.py"],
    "validate": ["python3", "-B", ".plumbline/parts/validate.py"],
}
PART_SECONDS = 120

WRITE_TOOLS = {"Write": "file_path", "Edit": "file_path", "MultiEdit": "file_path",
               "NotebookEdit": "notebook_path"}
READ_TOOLS = {"Read": "file_path", "Grep": "path"}


def project_root():
    return os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()


def hook_input():
    data = sys.stdin.read()
    try:
        value = json.loads(data) if data.strip() else {}
    except ValueError:
        value = {}
    return value if isinstance(value, dict) else {}


def role_of(event):
    """The role the agent plays: the agent type it was started as, when that
    is implementer or verifier; otherwise the lead."""
    agent_type = event.get("agent_type")
    if agent_type in ("implementer", "verifier"):
        return agent_type
    return "lead"


def tool_paths(event, tools):
    """The absolute paths a tool call touches, or None when it is not one of
    the tools."""
    name = event.get("tool_name")
    if name not in tools:
        return None
    tool_input = event.get("tool_input") or {}
    base = event.get("cwd") or project_root()
    value = tool_input.get(tools[name])
    if not isinstance(value, str) or value == "":
        if name == "Grep":
            value = base
        else:
            return []
    return [value if value.startswith("/") else os.path.join(base, value)]


def run_part(name, args, timeout=PART_SECONDS):
    """(verdict, stdout lines, stderr text)."""
    command = PARTS[name] + list(args)
    try:
        result = subprocess.run(command, cwd=project_root(), capture_output=True,
                                stdin=subprocess.DEVNULL, timeout=timeout)
    except subprocess.TimeoutExpired:
        return "error", [], "%s did not exit within %d seconds" % (name, timeout)
    except OSError as exc:
        return "error", [], "%s cannot be started: %s" % (name, exc)
    verdict = {0: "pass", 3: "block"}.get(result.returncode, "error")
    out = result.stdout.decode("utf-8", "replace").replace("\r\n", "\n")
    lines = [line for line in out.split("\n") if line != ""]
    err = result.stderr.decode("utf-8", "replace").strip()
    if verdict == "error":
        err = "exit status %d: %s" % (result.returncode, err)
    return verdict, lines, err


def pre_tool_use_reply(part, rule, verdict, lines, err):
    """Print the PreToolUse reply for a guard's verdict and exit."""
    if verdict == "block":
        reason = "Blocked by %s (rule: %s):\n%s" % (part, rule, "\n".join(lines))
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }}))
    elif verdict == "error":
        message = "Environment error: %s could not decide (%s). The action was let through." % (part, err)
        print(json.dumps({
            "systemMessage": message,
            "hookSpecificOutput": {"hookEventName": "PreToolUse", "additionalContext": message},
        }))
    sys.exit(0)
