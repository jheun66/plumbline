"""Connects gap-guard to the hook before an agent's file-writing tools."""

import connector_lib as lib

event = lib.hook_input()
paths = lib.tool_paths(event, lib.WRITE_TOOLS)
if paths:
    verdict, lines, err = lib.run_part("gap-guard", paths)
    lib.pre_tool_use_reply("gap-guard", "gap guard", verdict, lines, err)
