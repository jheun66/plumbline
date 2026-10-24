# Validate

validate checks the whole project by machine, when the user asks. The same input gives the same answer. Checks that need judgment are the verifier's ([change.md](change.md#what-the-verifier-checks)). Whether there are newer rules is the lead's ([status.md](status.md#newer-rules)).

## The part

validate is a mechanical part ([conformance.md](conformance.md)).

- Its name is `validate`.
- **Arguments** and **standard input**: empty. Any argument gives `error`.
- **Verdict**: `block` when it gives at least one problem line; `pass` when it gives none. A `skip` line is not a problem line.
- A command it needs that fails for a reason of the environment, such as `git` that cannot be started, gives `error`. A file it cannot read, or that does not have its form, gives a problem line, never `error`.
- It does not use the network, and writes no file.

## What it reads

| What | Where |
|---|---|
| the layer locations and the layers kept out of git | the settings file ([layers.md](layers.md#the-settings-file)) |
| the setup record, the files it lists, the renderers | `.plumbline/setup-record.json` ([setup-record.md](setup-record.md)) |
| the section titles and the figure kinds | the template's project part ([design-docs.md](design-docs.md#the-template)) |
| design documents | every Markdown file inside the design location ([design-docs.md](design-docs.md#design-documents-and-module-documents)) |
| which files git tracks | the git repository at the project root |

- Every CR LF in a file is read as LF. Lines are numbered from 1, counting every line of the file.
- Level-2 headings, fenced code blocks and their info strings are found as [design-docs.md](design-docs.md#reading-a-markdown-document) states.
- A path in an output line is relative to the project root, with `/`.

## Problem lines

Each line is a code and its fields, separated by tabs ([conformance.md](conformance.md#output)).

| Code | Fields | When |
|---|---|---|
| `settings` | path | the settings file is missing or does not have its form |
| `missing-layer` | layer | a layer in git has none of its locations present |
| `record` | path | the setup record is missing or does not have its form |
| `checksum` | path | a file the setup record lists is missing, or its checksum differs |
| `part-not-found` | path | in a file the setup record lists with a reproduced part, the part's begin or end line cannot be found |
| `template` | path | the template is missing, or its project part does not have its form |
| `sections` | document | a module document's level-2 headings are not the template's seven section titles, in order |
| `impl-path` | document, line, token | a line of a design document names a location of impl ([Locations of impl](#locations-of-impl)) |
| `figure` | document, line, figure kind | a figure does not render. The line is the one that opens the figure |
| `tracked` | path | git tracks a file of a layer kept out of git |

## Skip lines

| Code | Fields | When |
|---|---|---|
| `skip` | `layer`, layer | a layer kept out of git is absent here |
| `skip` | `figures`, figure kind | a figure kind a design document uses has no renderer, or its renderer cannot be started |
| `skip` | `tracked`, `not-git` | the project root is not a git repository |

## The settings and the layers

- `settings` is given with `.plumbline/settings.json` when it is missing, or does not have its form ([layers.md](layers.md#the-settings-file)).
- When the settings file is missing or does not have its form, every check that needs the layers is left out: `missing-layer`, `sections`, `impl-path`, `figure`, `tracked`, and `skip layer`. There is then no design document, so no figure kind is used either.
- A layer is present when at least one of its locations exists.
- `missing-layer` is given for each layer in git that is not present.
- `skip layer` is given for each layer kept out of git that is not present.
- When design is not present, there is no design document, and `sections`, `impl-path` and `figure` give no line.

## The setup record

- `record` is given with `.plumbline/setup-record.json` when it is missing, or does not have its form ([setup-record.md](setup-record.md#the-form)).
- When the setup record has its form, each entry of its `files` is checked, its checksum computed as [setup-record.md](setup-record.md#checksums) states:
  - `checksum` is given when the file does not exist, or its checksum differs from the entry's;
  - `part-not-found` is given when the entry has `begin` and `end`, the file exists, and its reproduced part cannot be found.
- Lines a project adds outside a reproduced part change no checksum.
- When the setup record is missing or does not have its form, `checksum`, `part-not-found` and `figure` are left out, and each figure kind a design document uses gives a `skip figures` line.

## The template

- `template` is given with `.plumbline/template.md` when it is missing, or its project part does not have its form ([design-docs.md](design-docs.md#the-template)).
- When the template is missing or its project part does not have its form, `sections` and `figure` are left out. It then names no figure kind, so no `skip figures` line is given either.

## Sections

- `sections` is given for each module document whose level-2 headings, in order, are not exactly the template's seven section titles, in order. A missing section, two sections out of order, a title that differs from the template's, and another level-2 heading each give it.
- The design README is not checked. A `README.md` in a folder below the design location is a module document, and is checked.

## Locations of impl

- Every line of every design document, code blocks and figures included, is cut into tokens. A token is a longest run of characters that are neither white space nor one of `` ` `` `"` `'` `(` `)` `[` `]` `<` `>` `{` `}` `|`.
- From the end of a token, every `.` `,` `;` `:` `!` and `?` is removed. Then a leading `./` is removed, once. A token left empty is dropped.
- A token names a location of impl when it begins with an impl location followed at once by `/`, or when it equals an impl location that holds a `/` or a `.`.
- `impl-path` is given with the document, the line's number and the token, as it is after the removals.

Examples, with the impl locations `src` and `Cargo.toml`:

- `src/main.rs`, `src/`, `./src/main.rs` and `Cargo.toml` name locations of impl.
- The word `src` alone does not, nor does `tests`.
- A line `See [x](./src/main.rs).` gives `impl-path` with the token `src/main.rs`.

## Figures

- A figure is found as [design-docs.md](design-docs.md#figures) states, with the template's figure kinds. A design document uses a figure kind when it holds a figure of that kind.
- Each figure is rendered with the renderer the setup record gives for its kind, run as [setup-record.md](setup-record.md#renderers) states.
- A renderer that ends with a status other than 0, or that has not ended 60 seconds after it was started, gives `figure` with the document, the number of the line that opens the figure, and the figure kind. A renderer that has not ended in time is stopped.
- For each figure kind a design document uses that has no renderer in the setup record, `skip figures` is given with that kind, and no figure of it is rendered.
- When a renderer cannot be started, no figure of its kind is rendered, and `skip figures` is given with that kind.
- A renderer is started only for a figure kind a design document uses.

## Files kept out of git

- The project root is a git repository when it holds `.git`. The files git tracks are those that `git ls-files`, run in the project root, lists.
- `tracked` is given for each tracked path that belongs to a layer kept out of git ([layers.md](layers.md#which-layer-a-path-belongs-to)).
- When the project root is not a git repository, `skip tracked not-git` is given, and `tracked` is not checked.

## The order of the lines

1. `settings`, then `missing-layer` by layer, in the order intent, design, impl.
2. `record`, then `checksum`, then `part-not-found`, each by path.
3. `template`.
4. `sections`, then `impl-path`, then `figure`, each by document, then by line.
5. `tracked`, by path.
6. `skip`: the lines whose first field is `layer`, then `figures`, then `tracked`; within each, by the second field. For `skip layer`, the layers go in the order intent, design, impl.

- Within a code, lines are ordered by their fields in turn: line numbers as numbers, every other field by the bytes of its text.
- A line found more than once is given once.

## Telling the user

When the user asks, the lead runs validate with the runner and entry the setup record gives ([setup-record.md](setup-record.md#parts)), and tells the user the result in plain words: for each line, what is wrong and what to do.

| Lines | What to do |
|---|---|
| `record`, `checksum`, `part-not-found` | the setup is reproduced again ([status.md](status.md#things-to-fix)) |
| `settings` | the settings file is fixed with the user, then the setup is reproduced again |
| `template` | when the template's project part is missing or wrong, the lead fixes it with the user; then the setup is reproduced again |
| `sections`, `impl-path`, `figure` | the design is fixed |
| `tracked` | the user is asked whether to take that file out of git |
| `missing-layer` | the settings' locations are checked with the user |
| `skip` | what was not checked, and why |

## What always holds

- The same input gives the same answer. validate does not use the network.
- It writes no file.
- It runs only when the user asks.

The cases of `validate` are in [cases/validate.json](cases/validate.json) ([conformance.md](conformance.md#which-parts-have-cases)).
