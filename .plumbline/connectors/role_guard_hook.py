"""Connects role-guard to the hook before an agent's file-reading and
file-writing tools."""

import connector_lib as lib

event = lib.hook_input()
for tools, action in ((lib.READ_TOOLS, "read"), (lib.WRITE_TOOLS, "write")):
    paths = lib.tool_paths(event, tools)
    if paths:
        verdict, lines, err = lib.run_part("role-guard", [lib.role_of(event), action] + paths)
        lib.pre_tool_use_reply("role-guard", "role table", verdict, lines, err)
