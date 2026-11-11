# Validate

## 1. Responsibilities

- Checks the whole project by machine when the user asks.
- Gives the same answer for the same input.

Checks that need judgment follow the project's assigned roles and workflow (A change). The lead checks whether newer rules exist (Status).

## 2. Public interface

### The part

- Its name is `validate`. It keeps the contract in Conformance cases.
- Its arguments and standard input are empty. Any argument gives `error`.
- At least one problem line gives `block`; none gives `pass`. A `skip` line is not a problem.
- A command it needs that fails for a reason of the environment gives `error`. A file it cannot read, or that does not have its form, is a problem line, not an error.

### What it reads

| What | Where |
|---|---|
| the complete settings, including layer locations, git exclusions, named zones, role members and guard choices | the settings file (Layers and settings) |
| the setup record, the files it lists, the renderers | the setup record (Setup record) |
| the section titles and figure kinds | the template's project part (Design documents) |
| design documents | every Markdown file inside the design location |
| which files git tracks | the git repository at the project root |

### Settings and record validation

Settings must satisfy the complete form in Layers and settings. Validate checks role and zone references, allowed layer assignments, required fields and recognition declarations. Missing roles are a `settings` problem, not an invitation to supply a default roster. An empty member list is valid; whether that roster can perform the planned work is a judgment made during reproduction.

The record must satisfy Setup record, including its own complete settings snapshot, carrier coverage, file and part references, and the enforcement combinations. Those references use the snapshot, even when live settings have changed. Invalid live settings do not prevent validation of an otherwise readable record against its own snapshot.

Validate checks structure, not the truth of an enforcement claim. It does not invoke a recognizer, execute a shell command being inspected, rerun guard cases or operate through connectors. Evidence, scope and limits must have their documented form; their adequacy is checked during reproduction. A `pass` from validate alone is not proof of guard coverage or completion of the five checks.

### Problem lines

Each line is a code and its fields, separated by tabs. Line numbers count from 1.

| Code | Fields | When |
|---|---|---|
| `settings` | path | the settings file is missing or does not have its form |
| `missing-layer` | layer | a layer in git has none of its locations present |
| `record` | path | the setup record is missing or fails its form, including internal references or enforcement coverage entries |
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
- Role settings and enforcement records are checked without inventing roles or promoting untested coverage to mechanical enforcement.

## 5. Decisions and reasons

- There is one mode. It runs only on request, so there is nothing to block. That there are problems is shown as `block`.
- Figures are always rendered when a renderer exists. It runs only on request, so it may take time.
- Locations of impl are found by the token rule, so the same input gives the same answer. A single word such as `src` is also an ordinary word, so it does not count.

## 6. Verification criteria

Shown by conformance cases (Conformance cases). Unless stated otherwise, use the complete settings in the Setup record example: intent `docs/intent.md`, design `docs/design`, impl `src`, with its named zones, `builder` member and guard choices. The template and setup record are valid, and all listed files have matching checksums. Only the difference is given.

Must-pass cases (`pass`):

- One module document that keeps the template → no lines.
- The design README has no seven sections → no lines.
- The project added lines outside a reproduced part → no lines.
- A reproduced file whose line ends turned into CR LF → no lines.
- A design document holds the word `src` alone → no lines.
- A figure with no renderer → only a `skip figures` line.
- The project root is not a git repository → only a `skip tracked not-git` line.
- With design kept out of git, design is absent → only a `skip layer design` line.
- Empty members, empty write zones or shared write zones, with a correspondingly valid record → no lines.
- A part zone without recognition when neither requested zone guard needs it → no lines.
- A valid current roster differs from the valid record snapshot → no `record` line just because the role names differ.
- A selected guard remains instruction-only with a stated reason and complete coverage entries → no lines.
- A structurally valid custom recognition command cannot be found → no line from settings validation; the command is not invoked.

Must-block cases (`block`):

- No settings file → `settings`.
- Missing `roles`, duplicate role or zone names, a `lead` member, unknown zone references, an intent zone, a design write zone, an empty duty or model, an unknown field, invalid guard types or shell choice → `settings` each.
- A requested zone guard uses a file-part zone without recognition, or a recognition declaration has an invalid form → `settings`.
- A layer in git has no location present → `missing-layer`.
- No setup record → `record`.
- A snapshot missing role settings; an unknown carrier role; a role with no carrier; a reference to an unlisted file or part → `record` each.
- An unknown enforcement rule, role or channel; a missing or repeated rule–role–channel combination; empty scope; mechanical coverage without evidence or its part; an instruction entry with no reason or with mechanical-only fields → `record` each.
- Mechanical zone enforcement while that guard is off, or mechanical shell enforcement with shell choice `none` → `record`.
- A record in an older form that lacks the required fields → `record`; no migration is performed.
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

Also verify output ordering and deduplication when several settings or record defects coexist. A record-format defect suppresses its dependent checksum and figure checks as specified above; a valid snapshot remains independently checkable when live settings are invalid.

## 7. Out of scope

None.
