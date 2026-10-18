"""The CI step: runs validate in gate mode and fails the run on block and on
error, saying which."""

import sys

import connector_lib as lib

verdict, lines, err = lib.run_part("validate", ["gate"], timeout=None)
for line in lines:
    print(line)
if verdict == "pass":
    print("validate (gate): pass")
    sys.exit(0)
if verdict == "block":
    print("validate (gate): block")
else:
    print("validate (gate): error: %s" % err)
sys.exit(1)
