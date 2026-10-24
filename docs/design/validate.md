# Validate

## 1. Responsibilities

- Checks the whole project by machine when the user asks.
- Gives the same answer for the same input.

Checks that need judgment are the verifier's (A change); whether there are newer rules is the lead's (Status).

## 2. Public interface

### The part

- Its name is `validate`. It keeps the contract in Conformance cases.
- Its arguments and standard input are empty. Any argument gives `error`.
- At least one problem line gives `block`; none gives `pass`. A `skip` line is not a problem.
- A command it needs that fails for a reason of the environment gives `error`. A file it cannot read, or that does not have its form, is a problem line, not an error.

### What it reads

| What | Where |
|---|---|
| the layer locations and the layers kept out of git | the settings file (Layers and settings) |
| the setup record, the files it lists, the renderers | the setup record (Setup record) |
| the section titles and figure kinds | the template's project part (Design documents) |
| design documents | every Markdown file inside the design location |
| which files git tracks | the git repository at the project root |

### Problem lines

Each line is a code and its fields, separated by tabs. Line numbers count from 1.

| Code | Fields | When |
|---|---|---|
| `settings` | path | the settings file is missing or does not have its form |
| `missing-layer` | layer | a layer in git has none of its locations present |
| `record` | path | the setup record is missing or does not have its form |
| `checksum` | path | a file the setup record lists is missing, or its checksum differs |
| `part-not-found` | path | in a file with a reproduced part, the part's begin or end line cannot be found |
| `template` | path | the template is missing, or its project part does not have its form |
| `sections` | document | a module document's level-2 headings are not the template's seven section titles, in order |
| `impl-path` | document, line, token | a design document names a location of impl (below) |
| `figure` | document, line, figure kind | a figure does not render. The line is the one that opens the figure |
| `tracked` | path | git tracks a file of a layer kept out of git |

### Skip lines

| Code | Fields | When |
|---|---|---|
| `skip` | `layer`, layer | a layer kept out of git is absent here. When design is absent, `sections`, `impl-path` and `figure` are left out |
| `skip` | `figures`, figure kind | a figure kind a design document uses has no renderer, or its renderer cannot be started |
| `skip` | `tracked`, `not-git` | the project root is not a git repository |

### Checks left out

- When the settings file is missing or broken, every check that needs the layers is left out: `missing-layer`, `sections`, `impl-path`, `figure`, `tracked`, and `skip layer`. When the project root is not a git repository, `skip tracked not-git` is still given.
- When the setup record is missing or broken, `checksum`, `part-not-found` and `figure` are left out, and each figure kind a design document uses gives a `skip figures` line.
- When the template is missing or broken, `sections` and `figure` are left out.

### Finding locations of impl

- Every line of a design document (code blocks and figures included) is cut into tokens. A token is a longest run of characters other than white space and `` ` `` `"` `'` `(` `)` `[` `]` `<` `>` `{` `}` `|`.
- From the end of a token, `.` `,` `;` `:` `!` `?` are removed. A leading `./` is removed.
- A token names a location of impl when it starts with an impl location followed at once by `/`, or equals an impl location that holds `/` or `.`.
- Example: with the impl locations `src` and `Cargo.toml`, `src/main.rs`, `src/` and `Cargo.toml` are named; the word `src` alone is not.

### Figures

- Each figure is rendered with the renderer the setup record gives for its kind (Setup record).
- A renderer that ends with a status other than 0, or does not end within 60 seconds, gives `figure`.

### The order of the lines

1. `settings`, `missing-layer`. Layers in the order intent, design, impl.
2. `record`, `checksum`, `part-not-found`. Each by path.
3. `template`.
4. `sections`, `impl-path`, `figure`. In this order, each by document, then by line.
5. `tracked`. By path.
6. `skip`. In the order of the table above, then by the second field. For `skip layer`, layers in the order intent, design, impl.

Within a code, lines are ordered by their fields in turn: line numbers as numbers, every other field by the bytes of its text. A line that would be given twice is given once.

## 3. Flow

1. When the user asks, the lead runs it.
2. The lead tells the user the result in plain words: for each line, what is wrong and what to do.
   - `record`, `checksum`, `part-not-found`: the setup must be reproduced again (things to fix, in Status).
   - `settings`: the settings file is fixed with the user, then the setup is reproduced again.
   - `template`: when the template's project part is wrong, the lead fixes it with the user; then the setup is reproduced again.
   - `sections`, `impl-path`, `figure`: the design is fixed.
   - `tracked`: the user is asked whether to take that file out of git.
   - `missing-layer`: the settings' locations are checked with the user.

## 4. Invariants and contracts

- The same input gives the same answer. It does not use the network.
- It writes no file.
- It runs only when the user asks.

## 5. Decisions and reasons

- There is one mode. It runs only on request, so there is nothing to block. That there are problems is shown as `block`.
- Figures are always rendered when a renderer exists. It runs only on request, so it may take time.
- Locations of impl are found by the token rule, so the same input gives the same answer. A single word such as `src` is also an ordinary word, so it does not count.

## 6. Verification criteria

Shown by conformance cases (Conformance cases). In each case the settings are intent `docs/intent.md`, design `docs/design`, impl `src`, and the template and the setup record are valid. Only what differs is given.

Must-pass cases (`pass`):

- One module document that keeps the template → no lines.
- The design README has no seven sections → no lines.
- The project added lines outside a reproduced part → no lines.
- A reproduced file whose line ends turned into CR LF → no lines.
- A design document holds the word `src` alone → no lines.
- A figure with no renderer → only a `skip figures` line.
- The project root is not a git repository → only a `skip tracked not-git` line.
- With design kept out of git, design is absent → only a `skip layer design` line.

Must-block cases (`block`):

- No settings file → `settings`.
- A layer in git has no location present → `missing-layer`.
- No setup record → `record`.
- The content of a file the setup record lists changed → `checksum`.
- A line inside a reproduced part changed → `checksum`.
- A reproduced part's end line is missing → `part-not-found`.
- No template → `template`.
- A module document missing a section, with sections out of order, with a title that differs from the template's, or with another level-2 heading → `sections` each.
- A README file in a folder below has no seven sections → `sections`.
- A design document names `src/main.rs` → `impl-path`.
- A figure the renderer fails on → `figure`.
- git tracks intent, which is kept out of git → `tracked`.

Error cases (`error`):

- One argument is given.

## 7. Out of scope

None.
