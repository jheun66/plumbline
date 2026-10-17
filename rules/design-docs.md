# Design documents

## Design documents and module documents

- Every Markdown file at the design location ([settings.md](settings.md)) is a design document.
- The design location's top-level `README.md` is the design's README. It is the only design document that is not a module document. It holds what applies to the whole design: scope, reading order, terms.
- The design's README has exactly one `milestone` line in its front matter ([layers.md](layers.md#documents-and-front-matter)): `milestone: <name>`. It names the milestone the design is in now, as the project's intent names it.
- Every other design document is a module document.
- A project's section titles, its kinds of figures, and how its design documents are laid out and named are its own.

## The seven sections

Every module document has seven sections, as level-2 headings, in this order:

| # | Holds |
|---|---|
| 1 | Responsibilities: what the module does and what it does not |
| 2 | Public interface: names, fields and contracts other modules or agents rely on |
| 3 | Flow: the main sequences |
| 4 | Invariants and contracts: conditions that always hold |
| 5 | Decisions and reasons: why it is this way, what was rejected |
| 6 | Verification criteria: what must be shown for the module to be right; for a mechanical part, its conformance cases |
| 7 | Out of scope: what a later milestone adds |

- The table gives what each section holds, not its title. The titles are the template's level-2 headings.
- A module document's level-2 headings equal the template's, exactly and in order.
- A module document has no other level-2 headings. Level-3 headings and below are free.
- A section that does not apply still appears and says so.

## The template

- Each project has one document template: `.plumbline/template.md`. It lies outside the design location and is not a design document.
- It has a project part and a reproduced part.
- The project part is:
  - front matter ([layers.md](layers.md#documents-and-front-matter)) with exactly two keys, each once: `confirmed: <text>` and `pending: <text>`. These texts are the project's two design-level markers. The `confirmed` text holds `YYYY-MM-DD` where the date goes;
  - the seven level-2 headings, in order. Their exact text is the project's section titles.
- The lead writes the project part with the user before the module map is written ([authoring.md](authoring.md)). A reproduction never changes it.
- When the project changes its section titles or marker texts, every module document is changed to match.
- The reproduced part says what each section is for, how basis lines are written, and how the two markers are used. It holds no level-2 heading. A reproduction writes it ([carriers.md](carriers.md)).

## Basis lines

- Every design document, the design's README included, has front matter with one or more lines `basis: <intent document> <version>`.
- `<intent document>` is the path of an intent document from the project root. `<version>` is that document's version when the design document was written or last checked against it.
- Every design document also names, in its text, the intent sections it is based on. That line has no fixed form.

## Design-level decisions

- A decision the design makes because intent does not is a design-level decision.
- It is written in section 5 of the module document it belongs to. There is no other list or table of decisions.
- It carries a design-level marker: the template's `confirmed` text with the date the user confirmed it in place of `YYYY-MM-DD`, or the template's `pending` text.
- A decision that only restates intent carries no marker.
- A point intent states is never a design-level decision. A design that would change or narrow it reveals a gap in intent ([layers.md](layers.md#gaps)).
- A decision that settled a gap item also links to its change ([changes.md](changes.md#a-decision-that-came-from-a-gap)).

Example: with `confirmed: (DL ok YYYY-MM-DD)` in the template, `(DL ok 2026-10-17)` is a confirmed marker and `(DL ok)` is a malformed one.

## Figures

- A figure says the same as the text. No fact appears only in a figure. Changing one changes the other.
- A figure shows only the current milestone's scope.
- Every figure is rendered and checked for overlapping or cut-off text.

## What a design document never names

- A location of impl: a path under any impl location ([settings.md](settings.md)), a test name, a case name.
- How impl currently looks.
