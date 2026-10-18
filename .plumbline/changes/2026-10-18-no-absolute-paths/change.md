---
state: open
diagnosis: design
---

# No absolute paths in the setup record's commands

## Asked

The setup record of this repository records the Mermaid renderer by an absolute path under the developer's home folder. The record is in git, so the path holds that machine's user name, and on any other machine the renderer is not found. The user asked that the rules prevent this in every project.

## Diagnosis

`design`: setup-record and reproduction say a renderer is chosen and recorded on the developer's machine, and do not say how its program may be named. Intent does not state the point.

## Opened at

8451c497dbb30db4fa7c80ed20b3dd7d74fc6fe7

## Tasks

1. setup-record: a runner or a renderer command holds no absolute path; its program is a name found on the PATH or a file the reproduction wrote. A record with such an element is not valid.
2. reproduction: a runner or a renderer counts as present only when it can be recorded that way; a renderer reachable only by an absolute path is not recorded, and the user is told what to put on the PATH. No file the reproduction writes holds a path particular to the developer's machine.
3. validate: conformance cases for the new form of the record.
4. An implementer aligns the rules and the cases.
5. The Mermaid renderer is put on the PATH of this machine, and this repository's setup is reproduced at the new rules commit.
6. Tag v1.1.

## Wording fixes

- setup-record §2 (Commands) and §5, reproduction §2 step 5: a command's program is only a name found on the PATH, with no `/` or `\`; the alternative of a relative path to a file the reproduction wrote is removed, aligned to the decision the user confirmed. Whether the program is found on a machine does not decide validity. validate §6 gains case 59 for a program given as a relative path. Reported by the implementer: a case runs in its own folder, where a relative program cannot be found.

## How the result was confirmed

## Commits
