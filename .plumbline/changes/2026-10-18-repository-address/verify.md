---
result: clean
---

# Verification: 2026-10-18-repository-address

Sections checked:

- setup-record §2 (`repository` under `rules`), §4, §5, §6
- reproduction §2 (Input, Before writing anything, step 10 of Steps), §5, §6
- validate §6 (cases 63 to 67)

## Findings

None.

- setup-record §2: impl defines `repository` as an address that other machines can reach. It gives both forms with the same conditions as the design: a scheme of ASCII letters, digits, `+`, `-` and `.` that begins with a letter and is not `file` in any case, followed by `://` and a rest that is not empty; or `<user>@<host>:<path>`, where user and host hold no `/`, `:` or `@` and none of the three is empty. A record whose repository has neither form is not valid. Impl defines nothing about the repository that the design leaves out. Its extra examples follow the same two forms.
- setup-record §4: impl's list of what always holds says the rules repository is named by an address, never by a local path.
- setup-record §5: impl follows the new decision. The record names an address and never records a local copy as the user gave it. The rule that status fetches tags from the repository the record names is unchanged and still holds.
- setup-record §6: validate's cases include each non-address the criterion names (cases 63, 64, 65). Case 66 passes the `<user>@<host>:<path>` address, and every case built on the base files passes a `https://` address. No earlier case in any part's cases uses a repository that is not an address, so none was broken by the new validity condition.
- reproduction §2 Input: impl reads the rules from a local copy. It asks for the address that copy was made from unless the user has named it, and may propose the previous record's repository when that is an address. It stops before writing anything when no address is given.
- reproduction §2 Before writing anything: a previous record whose repository is not an address is read as it is.
- reproduction §2 step 10: when a carrier that its means reads only at session start was written or changed, impl's final report says the change reaches its roles only in a new session and that their work waits for one. Work is handed to those roles only in such a session.
- reproduction §5: impl's rules follow both new decisions.
- reproduction §6: the two new criteria are checked by a reproduction on the example project in the M2 Done, as the design says for this module. Impl states the behavior they check.
- validate §6: cases 63 to 67 are in impl in the design's order, with the verdicts and lines the design gives. Each differs from the base files only in the record's repository.

## Diagnosis

The `design` diagnosis held.

- At the start commit, the design recorded the repository as the user gave it, and impl did the same.
- The design sections listed above changed first, in one commit, and impl was changed in a separate commit to follow them. Impl now follows every section checked.
- Only the design and impl layers changed in the design and impl locations. No design document's intent basis changed.
