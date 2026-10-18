# validate

`validate` is a mechanical part ([conformance.md](conformance.md)) that checks a project's design documents, change records and setup against the formats these rules define. It has two modes: in `report` mode it only reports, in `gate` mode it blocks on any problem it finds.

When it runs, and what a block stops, is stated in [carriers.md](carriers.md#connectors): at the end of the lead's turn in `report` mode, and before a change closes and in CI in `gate` mode.

validate does not judge what needs reading to tell, such as whether impl follows the design, or whether a design names an impl location that is not a path. The verifier does ([verify.md](verify.md)).

## Running it

- The part's name is `validate`.
- **Arguments**: exactly one, the mode: `report` or `gate`.
- **Standard input**: empty.
- **Verdict**: in `report` mode, `pass` whenever it ran. In `gate` mode, `block` when it gives at least one problem line, and `pass` otherwise. `skip` lines never block.
- It gives `error` when its argument is missing, when there is more than one, or when it is not one of the two modes, and when a command it needs, such as `git`, cannot be started or fails for a reason of the environment.
- A file it cannot read, or that does not have its form, gives a problem line. It is never an `error`.
- It checks the whole project, not one change.
- It never uses the network.

## What it reads

| What | Where |
|---|---|
| the layers and `not_in_git` | the settings file ([settings.md](settings.md)) |
| the setup record, the files it lists, its renderers | `.plumbline/setup-record.json` ([setup-record.md](setup-record.md)) |
| the section titles, the marker texts and the figure names | the template's project part ([design-docs.md](design-docs.md#the-template)) |
| design documents | every Markdown file at the design location ([design-docs.md](design-docs.md)) |
| intent versions | the `version` line of each intent document ([layers.md](layers.md#intent-versions)) |
| change records and the current change | `.plumbline/changes/*/` and `.plumbline/current-change` ([changes.md](changes.md)) |
| which files git tracks | the git repository at the project root, when there is one |

- The Markdown files at a location are: when the location is a file, that file, if its name ends in `.md`; when it is a folder, every file under it whose name ends in `.md`.
- Every CR LF in a file is read as LF. Lines are numbered from 1, counting every line of the file, front matter included.
- Level-2 headings, fenced code blocks and their info strings, section 5 of a module document, and links are found as [design-docs.md](design-docs.md#reading-a-markdown-document) states.

## Output lines

Each line is a code and its fields, separated by tabs ([conformance.md](conformance.md#output)). Paths are relative to the project root, with `/`.

### Problem lines

| Code | Fields | When |
|---|---|---|
| `settings` | path | the settings file is missing or not valid |
| `missing-layer` | layer | a layer is not in `not_in_git` and none of its paths exists |
| `record` | path | the setup record is missing or not valid |
| `checksum` | path | a file the record lists is missing, or its checksum differs |
| `part-not-found` | path | a file the record lists with `begin` and `end` exists, but its reproduced part cannot be found |
| `template` | path | the template is missing, or its project part does not have its form |
| `milestone` | path | the design README is missing, or its front matter does not have exactly one `milestone` line |
| `basis` | document | a design document's front matter or `basis` lines do not have their form |
| `basis-target` | document, intent document | a `basis` line names a path that is not an intent document, or an intent document without a valid version |
| `stale` | document, intent document, basis version, intent version | a `basis` line names an intent document whose version is newer |
| `sections` | document | a module document's level-2 headings are not the template's, in order |
| `marker` | document, line | a line of a module document holds a design-level marker that is not one of the template's two forms |
| `impl-path` | document, line, token | a design document names a path under an impl location |
| `figure` | document, line, figure name | in `gate` mode, a figure does not render, or its renderer has not exited after 60 seconds; the line is that of its opening fence |
| `decision-link` | document, line, change | a line in section 5 of a module document links to a change that does not exist, or that has no confirmed gap item at the design layer |
| `change` | path | a change record does not have its form, or `.plumbline/current-change` names no open change |
| `tracked` | path | git tracks a file that lies at a location of a layer in `not_in_git` |

### Skip lines

| Code | Fields | When |
|---|---|---|
| `skip` | `layer`, layer | a layer in `not_in_git` is not present: the checks that need it are not made. For intent: `basis-target` and `stale`. For design: `milestone`, `basis`, `sections`, `marker`, `impl-path`, `figure` and `decision-link`. For impl: none |
| `skip` | `figures`, `report` | in `report` mode, when a design document uses a figure name of the template: figures are not rendered |
| `skip` | `figures`, figure name | in `gate` mode, for a figure name of the template that a design document uses, when it has no renderer, or its renderer's program cannot be started |
| `skip` | `tracked`, `not-git` | the project root is not a git repository |

The sections below say exactly when each line is given.

## The settings and the layers

- `settings` is given when `.plumbline/settings.json` is missing or is not valid by everything [settings.md](settings.md#the-format) states, a `design` path that is a file included.
- A layer is present when at least one of its paths exists.
- `missing-layer` is given for each layer that is not in `not_in_git` and is not present.
- `skip layer` is given with the layer for each layer that is in `not_in_git` and is not present.
- When the intent layer is not present, `basis-target` and `stale` are not checked.
- When the design layer is not present, `milestone`, `basis`, `sections`, `marker`, `impl-path`, `figure` and `decision-link` are not checked. There is no design document, so no design document is checked for `basis-target` or `stale` either.
- No check needs the impl layer to be present. When it is in `not_in_git` and not present, `skip layer impl` is given, and no check is left out for it.
- When a layer that is not present is in `not_in_git`, its `skip layer` line says that these checks are not made. Otherwise its `missing-layer` line stands for them.

## The setup record and the files it lists

- `record` is given when `.plumbline/setup-record.json` is missing or is not a valid record ([setup-record.md](setup-record.md#valid-records)).
- For each entry in a valid record's `files`, its checksum is computed as [setup-record.md](setup-record.md#checksums) states:
  - `checksum` is given when the file does not exist, or when the checksum differs from the entry's;
  - `part-not-found` is given when the entry has `begin` and `end`, the file exists, and its reproduced part cannot be found.
- A line added to a file outside its reproduced part changes no checksum.

## The template

`template` is given with `.plumbline/template.md` when the file is missing, or when it does not have all of these:

- front matter ([layers.md](layers.md#documents-and-front-matter)) whose keys are `confirmed`, exactly once, `pending`, exactly once, and `figure`, any number of times, and no other key;
- a `confirmed` text that holds `YYYY-MM-DD` exactly once;
- exactly seven level-2 headings.

The template's figure names are the values of its `figure` lines. A template that gives `template` has no section titles, marker texts or figure names.

## The design README

The design README is the file `README.md` directly in the design location. When the design layer is present, `milestone` is given with its path when the README is missing, or when its front matter is missing, does not have the form [layers.md](layers.md#documents-and-front-matter) defines, or does not have exactly one `milestone` line.

## Basis lines

Every design document is checked. A design document gives `basis` when:

- it has no front matter, or its front matter does not have the form [layers.md](layers.md#documents-and-front-matter) defines;
- its front matter has no `basis` line;
- a `basis` line's value is not a path, one space, and a version. The path has the form of a path in the settings ([settings.md](settings.md#the-format)). The version has the form of an intent version ([layers.md](layers.md#intent-versions)).

When a design document does not give `basis`, and the intent layer is present, each of its `basis` lines is checked:

- `basis-target` is given with the document and the line's path when that path is not an intent document, or when the intent document has no valid version. An intent document is a Markdown file at the intent location.
- Otherwise, `stale` is given with the document, the path, the line's version and the intent document's version, when the intent document's version is newer than the line's.

Examples, with fields separated by spaces here for reading:

- `basis: docs/intent.md 1`, with `docs/intent.md` at `version: 2`, gives `stale docs/design/cli.md docs/intent.md 1 2`.
- `basis: docs/notes.md 2`, with `docs/notes.md` outside the intent location, gives `basis-target docs/design/cli.md docs/notes.md`.
- A design document without front matter gives `basis`.

## Sections

`sections` is given for a module document whose level-2 headings, in order, are not exactly the template's level-2 headings, in order. A missing heading, two headings swapped, and an extra level-2 heading each give it.

## Markers

- The template's two marker texts are its `confirmed` text and its `pending` text.
- Their common beginning is the longest text that both begin with. When it is empty, no marker is checked.
- A candidate is each place in a line of a module document where the common beginning starts. Every line counts, front matter and code blocks included.
- A candidate is a marker when, from there, the line goes on with the `pending` text, or with the `confirmed` text in which `YYYY-MM-DD` is replaced by a date: four digits, `-`, two digits, `-`, two digits, naming a day of the Gregorian calendar.
- `marker` is given with the document and the line's number for each line that holds a candidate that is not a marker.
- Whether a decision should carry a marker at all is not checked.

Examples, with `confirmed: (DL ok YYYY-MM-DD)` and `pending: (DL pending)` in the template, whose common beginning is `(DL ` with its space:

- `(DL ok 2026-10-17)` and `(DL pending)` are markers.
- `(DL ok)` and `(DL ok 2026-13-40)` are not, and each gives `marker`.

## Impl paths

- Every line of every design document is cut into tokens, code blocks and figures included. A token is each longest run of characters that are neither white space nor one of `` ` `` `"` `'` `(` `)` `[` `]` `<` `>` `{` `}` `|`.
- From the end of a token, every `.` `,` `;` `:` `!` and `?` is removed. Then a leading `./` is removed once. A token left empty is dropped.
- A token names an impl location when, for one of the impl paths in the settings, it begins with that path followed by `/`, or it equals that path and that path holds a `/` or a `.`.
- `impl-path` is given with the document, the line's number and the token, as it is after the removals, for each token that names an impl location.

Examples, with the impl paths `src` and `Cargo.toml`:

- `src/main.rs`, `src/`, `./src/main.rs` and `Cargo.toml` name impl locations.
- `src` alone and the word `tests` do not.
- A line `See [x](./src/main.rs).` gives `impl-path` with the token `src/main.rs`.

## Figures

- A figure is a fenced code block in a design document whose info string's first word is one of the template's figure names ([design-docs.md](design-docs.md#figures)). A design document uses a figure name when it holds a figure of that name.
- In `gate` mode, with a valid setup record and a valid template, each figure is handed to the renderer the record's `renderers` gives for its figure name, as [setup-record.md](setup-record.md#renderers) states. An exit status other than 0 gives `figure` with the document, the line's number of the figure's opening fence, and the figure name. A renderer that has not exited 60 seconds after it was started is stopped, and gives `figure` in the same way.
- In `gate` mode, for each figure name of a valid template that a design document uses and that has no renderer in the record, `skip figures` with that name is given, and no figure of that name is rendered. When the setup record is missing or not valid, no figure name has a renderer.
- When a renderer's program cannot be started, no figure of that name is rendered, and `skip figures` with that name is given. This is found when validate first starts it. A renderer is not started when no figure has its name, so a figure name that no design document uses gives no `skip figures` line.
- In `report` mode, no figure is rendered. When a design document uses a figure name of a valid template, `skip figures report` is given, once. When no design document uses one, it is not given.

## Decision links

- Links, their targets, and section 5 of a module document are found as [design-docs.md](design-docs.md#reading-a-markdown-document) states. A target has no `#` part.
- A link in a line of section 5 of a module document is a decision link when its target is a relative path that leads to `.plumbline/changes/<name>`, with or without a final `/`:
  - the target is not empty, does not begin with `/`, and has no `:` before its first `/`;
  - it is taken relative to the folder of the module document. Empty segments and `.` segments are ignored, and a `..` segment removes the segment before it. A target that leaves the project root leads nowhere.
- `decision-link` is given with the document, the line's number and `<name>` when `.plumbline/changes/<name>/` is not a folder, or when no gap item in it has the form [changes.md](changes.md#gap-items) defines with `layer: design` and `state: confirmed`.

Example: in `docs/design/cli.md`, a line in section 5 holding `[the change](../../.plumbline/changes/2026-11-02-a/)` is a decision link to `2026-11-02-a`. It gives no line when that change has a gap item with `layer: design`, `state: confirmed` and a `date`.

## Change records

`change` is given with the path:

- of `change.md`, for a folder directly under `.plumbline/changes/` that has no `change.md`, or whose `change.md` does not have the form [changes.md](changes.md#changemd) defines;
- of a gap item, a file `gap-<n>.md` in such a folder, that does not have the form [changes.md](changes.md#gap-items) defines;
- of `verify.md`, in such a folder, when it does not have the form [changes.md](changes.md#the-verify-result) defines;
- `.plumbline/current-change`, when it names a change ([changes.md](changes.md#the-current-change)) and that name is not a folder directly under `.plumbline/changes/` whose `change.md` has the form and `state: open`.

Every change is checked, whatever its state.

## Files kept out of git

- The project root is a git repository when it holds `.git`. The files git tracks are the paths in its index, as `git ls-files` lists them.
- `tracked` is given for each tracked path that equals or lies under a path of a layer in `not_in_git`.
- When the project root is not a git repository, `skip tracked not-git` is given.

## What depends on what

- When the settings file is missing or not valid, these are left out: `missing-layer`, `milestone`, `basis`, `basis-target`, `stale`, `sections`, `marker`, `impl-path`, `figure`, `decision-link`, `tracked`, and every `skip` line.
- When a layer is not present, the checks that need it are left out, whether it gives `skip layer` or `missing-layer` ([The settings and the layers](#the-settings-and-the-layers)).
- When the setup record is missing or not valid, `checksum`, `part-not-found` and `figure` are left out, and in `gate` mode every figure name of a valid template that a design document uses gives its `skip figures` line.
- When the template is missing or not valid, `sections`, `marker` and `figure` are left out, and no `skip figures` line is given.
- A design document that gives `basis` is not checked for `basis-target` or `stale`.

## Order of the lines

1. `settings`, then `missing-layer` by layer, in the order intent, design, impl.
2. `record`, then `checksum`, then `part-not-found`, each by path.
3. `template`, then `milestone`.
4. `basis`, `basis-target`, `stale`, `sections`, `marker`, `impl-path`, `figure`, `decision-link`: every line of one code before the lines of the next, in this order.
5. `change`, by path.
6. `tracked`, by path.
7. `skip`: `layer`, then `figures`, then `tracked`, as the first field; then by the second field. `skip layer` lines go by layer, in the order intent, design, impl.

- Within a code, lines sort by their fields in turn: line numbers as integers, every other field by the bytes of its text.
- A line is given once, even when it is found more than once.

## What always holds

- validate never uses the network.
- The same files, the same mode and the same renderers always give the same lines, in the same order.
- In `report` mode it never blocks. In `gate` mode it blocks exactly when it gives a problem line.
- A check that needs a layer that is not present and is kept out of git is skipped, and says so. A missing layer that is in git is a problem.
- A file it cannot read is a problem line, never an error.

## Conformance cases

The cases of `validate` are in [cases/validate.json](cases/validate.json) ([conformance.md](conformance.md#which-parts-have-cases)).
