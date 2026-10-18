---
result: findings
---

# Findings

1. `docs/design/setup-record.md`, section 6 (Verification criteria), Checksums: the criterion that an empty whole file has the checksum `sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` has no conformance case that shows it. No case in `rules/cases/validate.json` lists an empty whole file in the record and checks it against that checksum. The value appears in `rules/setup-record.md` only as an example, and no case runs it. The design's new list of the validate cases that show the checksum criteria (a whole file with CR LF line ends, a changed line inside a reproduced part, a `begin` line twice, a missing `end` line) leaves this criterion out as well. The gap was already there at the start commit and is not in the text this change added.

# Diagnosis

The `design` diagnosis held. At the start commit, validate section 6 ended at case 59, status section 6 ended at case 25, and setup-record section 6 did not say which cases show the checksum and same-settings criteria. The design added validate cases 60 to 62, status cases 26 and 27, and the two statements in setup-record section 6. Impl then added matching cases to `rules/cases/validate.json` and `rules/cases/status.json`:

- Each new case differs from its part's base files only in the way the design table says.
- Its expected verdict and lines are the ones the table gives.
- Its recorded checksums match the checksum algorithm, or fail to match it, as the case needs.

The other setup-record section 6 criteria also have cases:

- a `begin` line twice: validate 24;
- adding a path: status 5;
- every listed record-format error: validate 26 to 31, 50, 51 and 55 to 57, and also 59.

Design and impl were changed in separate commits. No layer outside design and impl was changed: the intent basis of every design document is still 1.6, and the only other file changed is the setup record, which lies in no layer.
