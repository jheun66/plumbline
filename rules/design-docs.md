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
  - front matter ([layers.md](layers.md#documents-and-front-matter)) whose keys are `confirmed` and `pending`, each exactly once, and `figure`, any number of times. It has no other key;
  - `confirmed: <text>` and `pending: <text>` are the project's two design-level markers. The `confirmed` text holds `YYYY-MM-DD` exactly once, where the date goes;
  - each `figure: <name>` names a kind of figure the project uses, by the first word of the info string of its fenced code blocks ([Figures](#figures)). A project that uses no figure has no `figure` line;
  - the seven level-2 headings, in order. Their exact text is the project's section titles. The template has no other level-2 heading.
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

- A figure is a fenced code block in a design document whose info string's first word ([Reading a Markdown document](#reading-a-markdown-document)) is one of the template's `figure` names. Which kinds of figures a project uses is its own choice.
- A figure says the same as the text. No fact appears only in a figure. Changing one changes the other.
- A figure shows only the current milestone's scope.
- Every figure is rendered and checked for overlapping or cut-off text. Whether it renders is checked by `validate` where the setup has a renderer for its kind ([validate.md](validate.md#figures)). Whether its text overlaps or is cut off is checked by whoever writes it.

Example: with `figure: mermaid` in the template, a code block opened by a line `` ```mermaid `` or `` ```mermaid title `` is a figure. One opened by `` ```text `` or `` ```mermaids `` is not.

## What a design document never names

- A location of impl: a path under any impl location ([settings.md](settings.md)), a test name, a case name.
- How impl currently looks.

`validate` finds the paths under impl locations ([validate.md](validate.md#impl-paths)). The verifier judges the impl locations that are not paths, such as test names ([verify.md](verify.md)).

## Reading a Markdown document

What a check reads in a design document, and in the template, is found this way:

- Every CR LF is read as LF. Every line of the file is read, front matter included.
- A fenced code block is opened by a line that begins with three or more `` ` `` characters, or three or more `~` characters. That run of characters is its fence. Its info string is the rest of the opening line, after the fence. The info string's first word is its first run of characters that are neither spaces nor tabs; an info string with no such run has no first word.
- A fenced code block is closed by the next line that begins with the fence's character at least as many times as the fence has it. When there is no such line, it runs to the end of the file. Its text is the lines between its opening line and its closing line.
- A level-2 heading is a line that begins with `## `, two `#` characters and a space, and that is neither inside a fenced code block nor its opening or closing line. Its text is the rest of the line, with the spaces at its end removed.
- Section 5 of a module document is the lines between its fifth level-2 heading and its sixth, or the end of the file when it has no sixth.
- A link is the text `](`, then its target, then `)`, within one line. Its target is the characters between the parentheses: from just after `](` up to the next `)`. A `#` in the target, and everything after it, is removed.

Examples:

- `## Responsibilities` is a level-2 heading with the text `Responsibilities`. `### Inputs` and `##Responsibilities` are not level-2 headings.
- A line `## Notes` between a line `` ``` `` and the next line that begins with `` ``` `` is inside a fenced code block, and is not a heading.
- A block opened by `` ````mermaid `` is closed by a line `` ```` `` or `` ````` ``, not by a line `` ``` ``. Its info string is `mermaid`.
- `[the change](../../.plumbline/changes/2026-11-02-a/#gap-1)` is a link whose target is `../../.plumbline/changes/2026-11-02-a/`.
