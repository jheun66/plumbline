---
state: archived
diagnosis: design
---

# The rules repository as an address every machine can reach

## Asked

The example project's setup record named the rules repository by a local path, `~/Projects/plumbline-rules`, as the user had given it. That path holds on one machine only, against the rule that no file a reproduction writes holds a path particular to the developer's machine, and status cannot look for newer rules from it elsewhere. The user asked that the record name an address every machine can reach.

## Diagnosis

`design`: setup-record says the repository is recorded as the user gave it; intent does not state the point.

## Opened at

ca68efb8356a0b3610feb585ec77f8d9271062eb

## Tasks

1. setup-record: `rules.repository` is an address other machines can reach, never a local path; a record with a local path is not valid.
2. reproduction: a local copy the user names is only where the rules are read; the agent asks for the repository's address. A previous record whose repository is a local path is read as it is.
3. validate: cases for a local repository path.
4. reproduction §2 step 10: when a carrier read only at the start of a session was written or changed, the final report says that work for its role waits for a new session. The user asked for it on 2026-10-18, after the example project's implementer received its carrier as it was before a reproduction. setup-record: the rest of a `<scheme>://` address is not empty; validate case 67.
5. An implementer aligns the rules and the cases.
6. This repository's setup is reproduced at the new rules commit.
7. Tag v1.2, once this change is archived.

## Wording fixes

- setup-record §2 and §6: an address is defined by its form, `<scheme>://…` other than `file`, or `<user>@<host>:<path>`, instead of by a list of local-path beginnings, which let a relative name, `FILE:` and an empty string through; aligned to the decision that the repository is an address other machines can reach. validate §6 gains cases 65 and 66.
- reproduction §2, Input and Before writing anything: a local copy at hand, from the user or from the previous record, is read and the address asked for, unless the user has named it; the previous record's address may be proposed; with no address the reproduction stops before writing anything, since it could not write a valid record.
Reported by the implementer.

## How the result was confirmed

- The setup was reproduced at rules 315019a: four of the new validate cases failed at first, the record check in this repository's parts was corrected, and then all 231 conformance cases passed. No carrier changed, so the final report rightly asked for no new session. Every connector check gave the expected result; all four rules are enforced mechanically.
- The example project's record already names the rules repository by its address, since its reproduction at v1.1.
- `validate gate` passed on the user's machine with every figure rendered, and in CI for dd40fa4.

## Commits

- e9fd0bb: design, setup-record, reproduction and validate
- 315019a: rules and cases
- dd40fa4: the setup reproduced from rules 315019a

## Verify result

`verify.md`: clean, no findings to take up. The diagnosis held.
