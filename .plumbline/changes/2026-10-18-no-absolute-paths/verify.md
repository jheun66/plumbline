---
result: findings
---

# Verify: 2026-10-18-no-absolute-paths

## Findings

All four findings are in setup-record section 6, in criteria this change did not touch. They were already there at the start commit. The change's own work has no finding (see below).

1. setup-record, section 6 (Verification criteria), checksums: no conformance case shows that a whole file holding `a` CR LF `b` CR LF has the same checksum as one holding `a` LF `b` LF. No case of any part lists a file with CR LF line ends in the setup record. A validate that takes the checksum without turning CR LF into LF first passes every case. Impl gives the value only as an example in `rules/setup-record.md`.
2. setup-record, section 6, checksums: no case shows that a reproduced part has another checksum when a line inside it changes (`rule two` in place of `rule one`). In `rules/cases/validate.json` the only checksum mismatches are for a whole file, edited or missing. For a reproduced part, the cases show only a checksum that matches, a line added outside the part, and a begin line that occurs twice. A validate that never compares a reproduced part's checksum passes every case.
3. setup-record, section 6, checksums: no case shows that a reproduced part whose end line is missing is an error. Only a begin line that occurs twice is shown.
4. setup-record, section 6, the same settings: no case shows that `["src", "tests"]` and `["tests", "src"]` for `impl` are the same settings. No case shows that adding a layer to `not_in_git` makes them differ. Only adding a path to a layer is shown, in `rules/cases/status.json`.

## The change's own work

- setup-record section 2 (parts, renderers, Commands): impl defines the same form for a part's runner and a renderer's command as the design does: no absolute path, and the program is a name found on the PATH. A record that breaks the form is not valid, and whether the program can be started on a machine has no bearing on that. Compared both ways, impl adds no public name, field or contract of its own. Sections 4 and 5 are kept, and the record-format criterion in section 6 that a command with an absolute path is an error is shown by validate cases 55 to 57.
- reproduction sections 2, 4 and 5: impl handles each case the same way the design does. A runner or renderer command the rules do not allow is read as it is, is not kept, and is chosen again in step 5. A runner counts as present only when it can be recorded by a name found on the PATH. A renderer that can be reached only by an absolute path is recorded as none, and the final report tells the user what to put on the PATH. When reproducing again, such a command is never kept. No file a reproduction writes holds a path particular to the developer's machine. Section 6 says its criteria are checked in a Done check on an example project, so I did not look for them as tests in impl. Validate cases 55, 56 and 59 show that a renderer recorded by an absolute path, or by a program that holds `/`, is rejected.
- validate section 6, cases 55 to 59: each has a case in `rules/cases/validate.json` with the files, argument, verdict and lines the design gives, in the same order. Each listed checksum matches its file.
- The design names no impl location in the sections it was handed.

## Diagnosis

The diagnosis `design` held. The design sections changed: setup-record sections 2, 4, 5 and 6, reproduction sections 2, 4, 5 and 6, and validate section 6 (cases 55 to 59). Impl now follows them. Since the start commit, only the design and impl locations changed among the layers, and both were layers this change touched. The findings above came before the change and do not bear on its diagnosis.
