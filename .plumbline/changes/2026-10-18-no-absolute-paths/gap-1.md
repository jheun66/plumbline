---
layer: design
state: confirmed
date: 2026-10-18
---

reproduction §2, "Before writing anything", stops when what the reproduction reads from the previous setup record does not have the form setup-record defines, and excepts only a record that lacks a key later rules added. A record written before the rules on commands, whose runner or renderer command holds an absolute path, is then not valid, and the reproduction stops. The record cannot be edited by hand, and removing it stops the next reproduction too, so such a project can never be reproduced again.

Proposed: such a runner or renderer command is read as it is and is not kept: the reproduction chooses the runner or the renderer again in step 5, as "Reproducing again" already lets the rules require. Reported by the reproducer, which stopped before writing anything.
