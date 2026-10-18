---
state: archived
diagnosis: design
---

# Conformance cases for setup-record's criteria

## Asked

Take up findings 1 to 4 of [2026-10-18-no-absolute-paths](../2026-10-18-no-absolute-paths/): criteria in setup-record §6 that no conformance case shows. A checksum of a whole file with CR LF line ends; a changed line inside a reproduced part; a reproduced part without its end line; the same settings in another order, and a layer added to `not_in_git`.

## Diagnosis

`design`: the checking modules' §6 do not list cases for these criteria, so a part can be wrong on them and still pass every case.

## Opened at

bc577a1aba2ba3f83188ac8a95e5302c3e389cfb

## Tasks

1. validate §6: cases for findings 1 to 3.
2. status §6: cases for finding 4.
3. setup-record §6: name where these criteria are shown.
4. An implementer adds the cases to the rules.
5. This repository's setup is reproduced at the new rules commit, so its parts run the new cases.
6. Tag v1.1, once this change is archived.

## Wording fixes

## How the result was confirmed

- The setup was reproduced at rules 29f20a5: all 226 conformance cases passed, the five new ones among them, with no part to correct; every connector check gave the expected result, and all four rules are enforced mechanically.
- `validate gate` passed on the user's machine with every figure rendered, and in CI for 2afa2b4.

## Commits

- 79d2e9c: design, validate, status and setup-record §6
- 29f20a5: the cases in the rules
- 2afa2b4: the setup reproduced from rules 29f20a5

## Verify result

`verify.md`: one finding, older than this change; the diagnosis held.

- Finding 1, no case shows the checksum of an empty whole file: the user decided not to act on it, on 2026-10-18. The SHA-256 of empty input is the same in every library, and a reproduced file is rarely empty.
