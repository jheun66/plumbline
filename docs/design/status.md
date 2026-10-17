---
basis: docs/intent.md 1.2
---

# status

> Basis: intent 1.2 — §5.2 (the rules version, settings changed since the reproduction, newer rules only with a network), §5.5, §7 (where status reads the milestone; a layer not present), §8.1 (what status shows), §11 (M1).

## 1. Responsibilities

**Does**: defines `status`, the mechanical part that reports the current state of a project in one run: the current milestone, the changes in progress, the gap items not yet answered, the design documents whose intent basis is behind, the rules version of the setup, the settings changed since the reproduction, and whether newer rules exist. Defines its input, its output lines and their order, and its conformance cases.

**Does not**:

- Block anything. Its verdict is always `pass` when it ran.
- Use the network. Whoever runs it fetches the rules repository's tags and gives them as input.
- Check formats or checksums. `validate` does (M2).
- Decide who runs it and when. `carriers` says (the lead's procedures).

## 2. Public interface

### The part

- Its name is `status`. It runs under the contract in `conformance`.
- Arguments: none.
- Standard input: empty, or the output of `git ls-remote --tags` run on the rules repository the setup record names. Each line is a commit hash, a tab, and a ref name.
- Verdict: `pass` whenever it ran. Anything it cannot read is reported in its output, not as an error.

### What it reads

| What | Where |
|---|---|
| the layers and `not_in_git` | the settings file (`settings`) |
| the rules repository, commit and tag, and the settings used | the setup record (`setup-record`) |
| the current milestone | the `milestone` line of the design README's front matter (`design-docs`) |
| changes and gap items | `.plumbline/changes/*/` and `.plumbline/current-change` (`changes`) |
| intent versions | the `version` line of each intent document (`layers`) |
| design bases | the `basis` lines of each design document (`design-docs`) |

### Output lines

Each line is a code and its fields, separated by tabs (`conformance`).

| Code | Fields | When |
|---|---|---|
| `invalid` | path | a file status reads does not have the form its module defines: the settings file, the setup record, the design README's front matter, a `change.md`, a gap item, or `.plumbline/current-change` when it names no existing change |
| `milestone` | name | the design README's front matter has exactly one `milestone` line |
| `milestone-unknown` | — | the design README is missing, or has no `milestone` line, or more than one |
| `rules` | repository, commit, tag or `-` | from a valid setup record |
| `rules-unknown` | — | there is no valid setup record |
| `newer-rules` | tag, commit | standard input was given, and a newer tag than the setup's rules exists (below) |
| `rules-up-to-date` | — | standard input was given, and no newer tag exists |
| `newer-rules-not-checked` | — | standard input was empty |
| `settings-changed` | key, `added` or `removed`, value | the settings differ from the record's copy (`setup-record`, the same settings): one line per layer path added to or removed from a layer, with the layer name as the key; one line per layer added to or removed from `not_in_git`, with `not_in_git` as the key |
| `change` | name, state, diagnosis, `current` or `-` | one line per change whose state is `open` or `closed` |
| `gap` | change, number, layer | one line per gap item whose state is `proposed`, in a change listed above |
| `stale` | design document, intent document, basis version, intent version | a `basis` line names an intent document whose `version` is newer than the version in the line |
| `skip` | layer | a layer that status needs is in `not_in_git` and not present (`settings`); the part that needs it was skipped |
| `missing-layer` | layer | a layer that status needs is not in `not_in_git` and not present |

- Paths are relative to the project root, with `/`.
- When the settings file is not valid, the lines that need it (`settings-changed`, `stale`, `skip`, `missing-layer`) are left out. When the setup record is not valid or absent, `rules-unknown` takes the place of `rules`, and `newer-rules`, `rules-up-to-date`, `newer-rules-not-checked` and `settings-changed` are left out.
- When the intent layer is present, a `basis` line whose intent document does not exist or has no valid version gives `invalid` with the design document's path. When it is not present, basis lines are not checked.

### Order of the lines

1. `invalid`, by path.
2. `milestone` or `milestone-unknown`.
3. `rules` or `rules-unknown`.
4. `newer-rules`, `rules-up-to-date` or `newer-rules-not-checked`.
5. `settings-changed`, by key, then `added` before `removed`, then value.
6. `change`, by name.
7. `gap`, by change, then number.
8. `skip` and `missing-layer`, by layer, in the order intent, design, impl.
9. `stale`, by design document, then intent document.

All sorting is by the bytes of the text.

### Newer rules

- Each line of standard input is a hash, a tab, and a ref name. Only ref names `refs/tags/<tag>` count. When a tag also appears as `refs/tags/<tag>^{}`, the hash on that line is the tag's commit; otherwise the hash on the plain line is.
- A tag names a version when it is `v` followed by a version, or a version alone, in the form `layers` defines for intent versions. Other tags are ignored.
- The newest tag is the one with the greatest version, compared as `layers` compares versions.
- `newer-rules` is given with the newest tag when its commit differs from the setup record's commit, unless the record's tag names a version that is the same as or greater than the newest one. Otherwise `rules-up-to-date` is given. When no tag names a version, `rules-up-to-date` is given.

## 3. Flow

```mermaid
sequenceDiagram
  actor U as User
  participant L as lead
  participant R as Rules repository
  participant S as status
  U->>L: what is the state?
  opt the network is available
    L->>R: git ls-remote --tags<br/>(the repository in the setup record)
    R-->>L: tags and their commits
  end
  L->>S: run, with the tags on standard input, or with none
  S-->>L: result lines
  L-->>U: the state, in the project's words
```

What status reports, and what each part needs:

```mermaid
flowchart LR
  ST["settings file"] --> SC["settings-changed"]
  REC["setup record"] --> SC
  REC --> RU["rules"]
  REC --> NR["newer rules"]
  IN["standard input:<br/>tags"] --> NR
  RM["design README"] --> MI["milestone"]
  CH["change records,<br/>current change"] --> CG["change, gap"]
  ST --> SL["stale, skip,<br/>missing-layer"]
  ID["intent versions"] --> SL
  DD["design bases"] --> SL
```

## 4. Invariants and contracts

- status never blocks and never uses the network.
- The same files and the same standard input always give the same lines, in the same order.
- Every change whose state is `open` or `closed` is listed, and no `archived` one is.
- Every `proposed` gap item in a listed change is listed.
- A design document is listed as `stale` only when its basis names an intent document that is present.
- With empty standard input, status says it did not check for newer rules; it never says the rules are up to date.

## 5. Decisions and reasons

- **status reports the current milestone, changes in progress, gap items not answered, design documents whose intent basis is behind, the setup's rules version, settings changed since the reproduction, and newer rules.** intent §8.1, §5.2.
- **Newer rules are reported only when the network was available; validate never looks at them.** intent §5.2.
- **A part that needs a layer not present skips it and says so.** intent §7.
- **The current milestone is the `milestone` line of the design README's front matter.** The milestone is a fact about what the design now covers, and the README already holds the design's scope and reading order. Rejected: a file of its own under `.plumbline/`, which can drift from the README's scope; working it out from the module map, which cannot tell a milestone whose documents are done and whose impl is being built from the next one. (Design-level — confirmed 2026-10-17)
- **The caller fetches the rules repository's tags and gives them on standard input; status compares them.** Mechanical parts never use the network (`conformance`), and the comparison then has conformance cases. Rejected: leaving newer rules to the lead's own judgment, which no case can pin down; letting status use the network, which gives different results for the same files. (Design-level — confirmed 2026-10-17)
- **status lists changes that are `open` or `closed`, but not `archived`.** A closed change still waits for its checks; an archived one is finished. (Design-level — confirmed 2026-10-17)
- **What status cannot read becomes an `invalid` line, and its verdict stays `pass`.** status is how the user learns what is wrong; stopping at the first bad file would hide the rest. (Design-level — confirmed 2026-10-17)
- **Lines are codes and fields in a fixed order; the lead tells the user the state in the project's words.** Codes keep what cases compare free of any natural language (`conformance`). (Design-level — confirmed 2026-10-17)
- **The newest rules are the tag with the greatest version, compared like intent versions; tags that name no version are ignored.** Tag names are how people name releases of the rules (intent §5.2), and comparing them as versions puts `v1.10` after `v1.9`. A record without a tag cannot be ordered against tags, so a newest tag at another commit is reported. (Design-level — confirmed 2026-10-17)

## 6. Verification criteria

Conformance cases. Each case gives the files listed and the standard input, and expects `pass` and the lines given, in order. Unless a case says otherwise, it uses these files:

- `.plumbline/settings.json`: `intent` `["docs/intent.md"]`, `design` `["docs/design"]`, `impl` `["src"]`, `not_in_git` `[]`;
- `.plumbline/setup-record.json`: a valid record whose `rules` are repository `R`, commit `c1` (40 hex digits) and tag `v1.0`, and whose settings are the same as the settings file;
- `docs/intent.md` with `version: 2`;
- `docs/design/README.md` with `basis: docs/intent.md 2` and `milestone: M1`;
- `docs/design/cli.md` with `basis: docs/intent.md 2`;
- `.plumbline/changes/2026-11-02-a/change.md` with `state: open`, `diagnosis: design`, and `gap-1.md` with `layer: design`, `state: proposed`;
- `.plumbline/current-change` holding `2026-11-02-a`;
- empty standard input.

| # | Difference from the files above | Expected lines |
|---|---|---|
| 1 | none | `milestone M1`; `rules R c1 v1.0`; `newer-rules-not-checked`; `change 2026-11-02-a open design current`; `gap 2026-11-02-a 1 design` |
| 2 | `cli.md` has `basis: docs/intent.md 1` | as 1, then `stale docs/design/cli.md docs/intent.md 1 2` |
| 3 | `intent` in `not_in_git` in the settings file and in the record's copy, and no `docs/intent.md` | as 1, then `skip intent` |
| 4 | no `docs/intent.md`, `not_in_git` empty | as 1, then `missing-layer intent` |
| 5 | the settings file has `impl` `["src", "tests"]` | `settings-changed impl added tests` after `newer-rules-not-checked` |
| 6 | the README has no `milestone` line | `milestone-unknown` in place of `milestone M1` |
| 7 | standard input: `c1 refs/tags/v1.0`, `c2 refs/tags/v1.9`, `c3 refs/tags/v1.10` | `newer-rules v1.10 c3` in place of `newer-rules-not-checked` |
| 8 | standard input: `c1 refs/tags/v1.0`, `c9 refs/tags/nightly` | `rules-up-to-date` in place of `newer-rules-not-checked` |
| 9 | standard input: `t1 refs/tags/v1.1`, `c4 refs/tags/v1.1^{}` | `newer-rules v1.1 c4` |
| 10 | a second change `2026-11-03-b` with `state: archived`, and a third `2026-11-04-c` with `state: closed`, `diagnosis: impl` | as 1, then `change 2026-11-04-c closed impl -` after the first `change` line |
| 11 | no setup record | `rules-unknown` in place of `rules R c1 v1.0`, and no `newer-rules-not-checked` |
| 12 | `change.md` has `state: done` | `invalid .plumbline/changes/2026-11-02-a/change.md` first; the change and its gap item are not listed |
| 13 | `gap-1.md` has `state: confirmed`, `date: 2026-11-03` | as 1 without the `gap` line |
| 14 | `.plumbline/current-change` is absent | `change 2026-11-02-a open design -` |

In the table, fields are separated by spaces for reading; in the cases they are tabs. `c1` to `c9` and `t1` stand for distinct 40-digit hashes.

## 7. Out of scope

- None. status is complete in M1.
