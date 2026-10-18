---
state: archived
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
5. reproduction: a runner or a renderer command an older record holds and these rules do not allow is read and chosen again (gap-1).
6. The Mermaid renderer is put on the PATH of this machine, and this repository's setup is reproduced at the new rules commit.
7. Tag v1.1.

## Wording fixes

- setup-record §2 (Commands) and §5, reproduction §2 step 5: a command's program is only a name found on the PATH, with no `/` or `\`; the alternative of a relative path to a file the reproduction wrote is removed, aligned to the decision the user confirmed. Whether the program is found on a machine does not decide validity. validate §6 gains case 59 for a program given as a relative path. Reported by the implementer: a case runs in its own folder, where a relative program cannot be found.
- reproduction §2 and §5: the exception for a runner or a renderer command that these rules do not allow holds whoever wrote the record, aligned to "Reproducing again" and §6 of the same document, which state it without the condition. Reported by the implementer: a reproducing agent cannot tell which rules wrote a record. reproduction §5 gains a known limit for the older exception on missing keys.

## How the result was confirmed

- A reproduction at rules 6c363f8 stopped before writing anything, on the previous record's absolute renderer path; that became gap-1.
- The setup was reproduced at rules fc69d21: the previous renderer was not kept, the renderer is recorded as `mmdc` by its name on the PATH, and all 221 conformance cases passed, the new validate cases 55 to 59 among them. Every connector check gave the expected result, and all four rules are enforced mechanically.
- No file git tracks or would track holds the developer's home path. `validate gate` passed on the user's machine with every figure rendered, and in CI for bc577a1.

## Commits

- ffc950e: design, setup-record, reproduction and validate
- 6c363f8: rules and cases
- 7e5bdcc: design, reproduction (gap-1)
- fc69d21: rules, reproduction (gap-1)
- bc577a1: the setup reproduced from rules fc69d21

## Verify result

`verify.md`: four findings, all in setup-record §6 and older than this change; the diagnosis held.

- Findings 1 to 4: taken up by the follow-up change [2026-10-18-setup-record-cases](../2026-10-18-setup-record-cases/), as the user decided on 2026-10-18.
