# Design documents

## Design documents and module documents

- The design location is one folder ([layers.md](layers.md#the-settings-file)). Every Markdown file inside it is a design document. A Markdown file is a file whose name ends in `.md`.
- The design README is the file `README.md` directly in the design location. It holds what applies to the whole design: scope, reading order, terms, and the module map. It is not a module document, and has no seven sections.
- Every other design document is a module document. A `README.md` in a folder below the design location is a module document too.

## The module map

The module map is written in the design README. It holds:

- the modules, each module's document, and one line on what each does;
- what relies on what;
- the main flows;
- the promises that hold for every module;
- for each module, the milestone in which its document is written;
- the current milestone. When a milestone's work is done, the current milestone is moved to the next one.

## The seven sections

A module document has these seven sections, in this order. Each is one level-2 heading.

| Section | Holds |
|---|---|
| 1 | responsibilities: what the module does and does not |
| 2 | public interface: names, fields and promises other modules or AIs rely on |
| 3 | flow: the main sequences |
| 4 | invariants and contracts: what always holds |
| 5 | decisions and reasons: why it is this way, what was rejected |
| 6 | verification criteria: what must be shown for the module to be right. For a mechanical part, its conformance cases |
| 7 | out of scope: what a later milestone adds |

- The table gives what each section holds, not its title. Each project titles the sections in its own words, in the template. A module document's section titles equal the template's, character for character.
- The number, order and meaning of the sections are the same in every project.
- A section that does not apply still appears, and says that there is none.
- A module document has no other level-2 heading. Level-3 headings and below are free.

## How to write

- In plain words, with no name left unexplained.
- Boundaries with other modules, and verification criteria, are written in the text too, in plain words.
- Decisions go in the decisions and reasons section.
- Another design document is named by its document name and section title.
- No design document names a location of impl, such as a file path or a test name, or says how impl looks now.
- The whole design is an amount the user can read in full.

## Figures

- A figure is a fenced code block in a design document whose info string's first word is a figure kind the template names ([Reading a Markdown document](#reading-a-markdown-document)).
- A figure and the text say the same. No fact appears only in a figure. When one changes, the other changes with it.
- A figure shows only the current milestone's scope.
- The AI that draws a figure renders it, and checks that no text in it overlaps or is cut off. validate checks only that it renders ([validate.md](validate.md#figures)).

Example: with the figure kind `mermaid`, a block opened by a line ```` ```mermaid ```` or ```` ```mermaid title ```` is a figure. A block opened by ```` ```text ```` or ```` ```mermaids ```` is not.

## The template

The template is `.plumbline/template.md`. Its form:

```
---
figure: mermaid
---

## Responsibilities
## Public interface
## Flow
## Invariants and contracts
## Decisions and reasons
## Verification criteria
## Out of scope

<!-- plumbline:begin -->
(the reproduced part: what each section holds)
<!-- plumbline:end -->
```

- The project part is the figure kind lines at the top and the seven section titles. A project that uses no figures has no figure line, and no `---` lines around it. The lead writes it ([roles.md](roles.md#the-three-roles)).
- The reproduced part runs from the begin line to the end line that the setup record gives for the template ([setup-record.md](setup-record.md#files)). A reproduction writes it. It says what each of the seven sections holds, and has no level-2 heading.

The project part has its form when both of these hold:

- When the file's first line is `---`, the lines up to the next line that is `---` are its figure kind lines. There is at least one. Each is `figure: ` followed by a figure kind: one or more characters, none of them a space or a tab. When the first line is `---` and no later line is `---`, the project part does not have its form.
- The file has exactly seven level-2 headings. Their texts, in order, are the project's section titles.

Spaces and tabs at the end of a line are not part of it. The figure kinds are the kinds those lines name.

## Reading a Markdown document

What a check reads in a design document, and in the template, is found this way:

- Every CR LF is read as LF. Every line of the file is read.
- A fenced code block is opened by a line that begins with three or more `` ` `` characters, or three or more `~` characters. That run of characters is its fence. Its info string is the rest of the opening line, after the fence. The info string's first word is its first run of characters that are neither spaces nor tabs; an info string with no such run has no first word.
- A fenced code block is closed by the next line that begins with the fence's character at least as many times as the fence has it. When there is no such line, it runs to the end of the file. Its text is the lines between its opening line and its closing line.
- A level-2 heading is a line that begins with `## `, two `#` characters and a space, and that is neither inside a fenced code block nor its opening or closing line. Its text is the rest of the line, with the spaces and tabs at its end removed.

Examples:

- `## Responsibilities` is a level-2 heading whose text is `Responsibilities`. `### Inputs` and `##Responsibilities` are not level-2 headings.
- A line `## Notes` between a line ```` ``` ```` and the next line that begins with ```` ``` ```` is inside a fenced code block, and is not a heading.
- A block opened by ````` ````mermaid ````` is closed by a line ````` ```` ````` or `````` ````` ``````, not by a line ```` ``` ````. Its info string is `mermaid`.

## Writing and confirming the design

1. Once intent is confirmed, the lead and the user decide the template's project part, the section titles and the figure kinds, and the lead writes it into the template.
2. The lead writes the module map from intent only. The user reads and confirms it.
3. For each milestone, its module documents are written in the module map's order. They are shown a few at a time; once the user reads and confirms a group, the next is written.
4. Once all of a milestone's module documents are confirmed, that milestone's impl is built.
5. When writing reveals a gap in intent, the lead stops and asks the user. After the answer, intent is fixed first.
6. When intent changes, the lead finds the design documents to look at again, and tells the user.
7. When the section titles or the figure kinds change, the lead changes the template's project part, and every module document is changed to match.

## What always holds

- Every module document has the template's seven section titles, character for character, in order, and no other level-2 heading.
- A figure and the text say the same.
- No design document names a location of impl.
- A milestone's impl is not built until all of its module documents are confirmed.
