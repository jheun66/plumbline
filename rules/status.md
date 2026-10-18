# status

`status` is a mechanical part ([conformance.md](conformance.md)) that reports the current state of a project in one run: the current milestone, the changes in progress, the gap items not yet answered, the design documents whose intent basis is behind, the rules version of the setup, the settings changed since the reproduction, and whether newer rules exist.

Who runs it and when is stated in [carriers.md](carriers.md).

## Running it

- The part's name is `status`.
- **Arguments**: none.
- **Standard input**: empty, or the output of `git ls-remote --tags` run on the rules repository the setup record names. Each line of that output is a commit hash, a tab, and a ref name.
- **Verdict**: `pass` whenever it ran. Anything it cannot read is reported in its output, not as an error.
- It never blocks and never uses the network.
- It checks the form only of the files it reads, and only as far as [What `invalid` covers](#what-invalid-covers) states.

## What it reads

| What | Where |
|---|---|
| the layers and `not_in_git` | the settings file ([settings.md](settings.md)) |
| the rules repository, commit and tag, and the settings used | the setup record ([setup-record.md](setup-record.md)) |
| the current milestone | the `milestone` line of the design README's front matter ([design-docs.md](design-docs.md)) |
| changes and gap items | `.plumbline/changes/*/` and `.plumbline/current-change` ([changes.md](changes.md)) |
| intent versions | the `version` line of each intent document ([layers.md](layers.md#intent-versions)) |
| design bases | the `basis` lines of each design document ([design-docs.md](design-docs.md#basis-lines)) |

status needs the intent layer and the design layer. When one of them is not present, it does as [settings.md](settings.md#a-check-and-a-missing-layer) states, with the `skip` and `missing-layer` lines below.

## Output lines

Each line is a code and its fields, separated by tabs ([conformance.md](conformance.md#output)).

| Code | Fields | When |
|---|---|---|
| `invalid` | path | a file status reads does not have the form these rules define for it ([What `invalid` covers](#what-invalid-covers)): the settings file, the setup record, the design README's front matter, a design document's front matter or `basis` lines, as stated below, a `change.md`, a gap item, or `.plumbline/current-change` when it names no open change |
| `milestone` | name | the design README's front matter has exactly one `milestone` line |
| `milestone-unknown` | — | the design README is missing, or it gives an `invalid` line, or its front matter has no `milestone` line, or more than one |
| `rules` | repository, commit, tag or `-` | from a valid setup record |
| `rules-unknown` | — | there is no valid setup record |
| `newer-rules` | tag, commit | standard input was given, and a newer tag than the setup's rules exists ([Newer rules](#newer-rules)) |
| `rules-up-to-date` | — | standard input was given, and no newer tag exists |
| `newer-rules-not-checked` | — | standard input was empty |
| `settings-changed` | key, `added` or `removed`, value | the settings file differs from the setup record's copy of the settings ([setup-record.md](setup-record.md#the-same-settings)): one line per layer path added to or removed from a layer, with the layer's name as the key; one line per layer added to or removed from `not_in_git`, with `not_in_git` as the key |
| `change` | name, state, diagnosis, `current` or `-` | one line per change whose state is `open` or `closed`; `current` when `.plumbline/current-change` names it |
| `gap` | change, number, layer | one line per gap item whose state is `proposed`, in a change listed by a `change` line |
| `skip` | layer | a layer that status needs is in `not_in_git` and not present; the part that needs it was skipped |
| `missing-layer` | layer | a layer that status needs is not in `not_in_git` and not present |
| `stale` | design document, intent document, basis version, intent version | a `basis` line names an intent document whose `version` is newer than the version in the line |

- Paths are relative to the project root, with `/`.
- When the settings file is missing or not valid, the lines that need it, `settings-changed`, `stale`, `skip`, `missing-layer` and the `invalid` lines for design documents, are left out, and `milestone-unknown` takes the place of `milestone`.
- When the setup record is not valid or absent, `rules-unknown` takes the place of `rules`, and `newer-rules`, `rules-up-to-date`, `newer-rules-not-checked` and `settings-changed` are left out.
- When the intent layer is present, a design document, the design README included, gives `invalid` with its own path when it has no front matter, or its front matter does not have the form [layers.md](layers.md#documents-and-front-matter) defines, or when one of its `basis` lines is not the path of an intent document, a space and a version ([layers.md](layers.md#intent-versions)), or names an intent document that does not exist or has no valid version. An intent document is a Markdown file at the intent location. A path elsewhere is not one.
- When the intent layer is not present, `basis` lines are not checked.

## What `invalid` covers

status checks the form only of the parts it reads:

| File | What is checked | When the file is missing |
|---|---|---|
| the settings file | all of it ([settings.md](settings.md#the-format)) | `invalid` with its path |
| the setup record | that it is a JSON object, and its `rules` and `settings` ([setup-record.md](setup-record.md#the-format)) | no `invalid` line; `rules-unknown` says it |
| the design README | its front matter ([layers.md](layers.md#documents-and-front-matter)); a README without front matter does not have the form. When the intent layer is present, also its `basis` lines, as for every design document ([Output lines](#output-lines)) | no `invalid` line; `milestone-unknown` says it |
| `change.md`, in every folder directly under `.plumbline/changes/` | all of its front matter ([changes.md](changes.md#changemd)) | `invalid` with the path the `change.md` should have |
| gap items | all of their front matter ([changes.md](changes.md#gap-items)), only in changes whose `change.md` has the form and whose state is `open` or `closed` | — |
| `.plumbline/current-change` | that it names an existing change whose `change.md` has the form and whose state is `open`, when it is not empty ([changes.md](changes.md#the-current-change)) | — |

- A file gives at most one `invalid` line, whatever problems it has.
- Nothing else is read from a file that gives an `invalid` line. A README that gives an `invalid` line, for its front matter or for its `basis` lines, gives `milestone-unknown`. A gap item that does not have the form gives no `gap` line. A `.plumbline/current-change` that names no open change marks no change `current`.
- Where these rules for status say a file is valid, they mean that what this table checks holds.
- A change whose `change.md` is missing or does not have the form is not listed, and its gap items are not read.

Examples, with fields separated by spaces here for reading:

- A setup record with an unknown key at its top level, and valid `rules` and `settings`, gives `rules` and no `invalid` line.
- A folder `.plumbline/changes/2026-11-05-d/` without `change.md` gives `invalid .plumbline/changes/2026-11-05-d/change.md`, and no `change` line for it.
- With no settings file, status gives `invalid .plumbline/settings.json` and `milestone-unknown`.
- With the intent layer present, a design document with a blank line inside its front matter gives `invalid` with its path, and no `stale` line.
- With `docs/intent.md` holding `version: 2` and a line `bad line` inside its front matter, every design document whose `basis` line names `docs/intent.md` gives `invalid` with its path. When the design README is one of them, status gives `invalid docs/design/README.md` and `milestone-unknown`.
- A `change.md` with `state: done` and `diagnosis: code` gives one `invalid` line with its path. When `.plumbline/current-change` names that change, it gives `invalid .plumbline/current-change` too. Neither the change nor its gap items are listed.
- A `.plumbline/current-change` that names a closed change gives `invalid .plumbline/current-change`, and every `change` line ends with `-`.

## Order of the lines

1. `invalid`, by path.
2. `milestone` or `milestone-unknown`.
3. `rules` or `rules-unknown`.
4. `newer-rules`, `rules-up-to-date` or `newer-rules-not-checked`.
5. `settings-changed`, by key, then `added` before `removed`, then by value.
6. `change`, by name.
7. `gap`, by change, then by number, compared as integers.
8. `skip` and `missing-layer`, by layer, in the order intent, design, impl.
9. `stale`, by design document, then by intent document.

All other sorting is by the bytes of the text. For example, gap item 2 comes before gap item 10.

## Newer rules

- Each line of standard input is a hash, a tab, and a ref name. A line of any other form is ignored. Only ref names `refs/tags/<tag>` count.
- When a tag also appears as `refs/tags/<tag>^{}`, the hash on that line is the tag's commit. Otherwise the hash on the plain line is.
- A tag names a version when it is `v` followed by a version, or a version alone, in the form of intent versions ([layers.md](layers.md#intent-versions)). Other tags are ignored.
- The newest tag is the one with the greatest version, compared as intent versions are compared. When several tags name that version, such as `v1.2`, `1.2` and `v1.2.0`, the one whose name comes first by bytes is the newest.
- `newer-rules` is given with the newest tag and its commit when that commit differs from the setup record's commit, unless the record's tag names a version that is the same as or greater than the newest tag's. Otherwise `rules-up-to-date` is given.
- When no tag names a version, `rules-up-to-date` is given.

Examples, with a setup record at commit `c1` and tag `v1.0`. `c1` to `c9` and `t1` stand for distinct hashes, and fields are separated by spaces here for reading:

- Tags `v1.0` at `c1`, `v1.9` at `c2` and `v1.10` at `c3` give `newer-rules v1.10 c3`.
- Tags `v1.0` at `c1` and `nightly` at `c9` give `rules-up-to-date`.
- A line `t1 refs/tags/v1.1` and a line `c4 refs/tags/v1.1^{}` give `newer-rules v1.1 c4`.
- Tags `v1.0` at `c1`, `v1.2` at `c5` and `1.2` at `c6` give `newer-rules 1.2 c6`.

## What always holds

- The same files and the same standard input always give the same lines, in the same order.
- Every change whose state is `open` or `closed` and whose `change.md` is valid is listed. No `archived` change is.
- Every `proposed` gap item in a listed change is listed.
- A design document is listed as `stale` only when its basis names an intent document that is present.
- With empty standard input, status says it did not check for newer rules. It never says then that the rules are up to date.

## Conformance cases

The cases of `status` are in [cases/status.json](cases/status.json) ([conformance.md](conformance.md#which-parts-have-cases)).
