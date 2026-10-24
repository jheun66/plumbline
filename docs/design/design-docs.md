# Design documents

## 1. Responsibilities

- Says which files are design documents, and which of those are module documents.
- Defines the module map and module documents: the seven sections, figures, how to write.
- Defines the template.
- Defines the order in which design is written and confirmed.

## 2. Public interface

### Design documents and module documents

- The design location is one folder (Layers and settings). Every Markdown file inside it is a design document.
- The README file at the top of the design location holds what applies to the whole design: scope, reading order, the module map.
- Every other design document is a module document. A README file in a folder below is a module document too.

### The module map

It is written in the design README. It holds:

- the modules, each module's document, and one line on what it does
- what relies on what
- the main flows
- the promises that hold for every module
- for each module, the milestone in which its document is written
- the current milestone. When a milestone's work is done, it is moved to the next milestone

### The seven sections

A module document has these seven sections, in this order. Each is one level-2 heading (`## `).

| Section | Holds |
|---|---|
| 1 | responsibilities: what the module does and does not |
| 2 | public interface: names, fields and promises other modules or AIs rely on |
| 3 | flow: the main sequences |
| 4 | invariants and contracts: what always holds |
| 5 | decisions and reasons: why it is this way, what was rejected |
| 6 | verification criteria: what must be shown for the module to be right. For a mechanical part, its conformance cases |
| 7 | out of scope: what a later milestone adds |

- Each project titles the sections in its own words. The titles must match the template's, character for character.
- A section that does not apply still appears and says "none".
- There is no other level-2 heading. Level-3 headings and below are free.

### How to write

- In plain words, with no name left unexplained.
- Boundaries with other modules and verification criteria are written in the text too, in plain words.
- Decisions go in the decisions and reasons section.
- Another design document is named by its document name and section title.
- No location of impl (file path, test name) and nothing about how impl looks now.
- The whole design is an amount the user can read in full.

### Figures

- A figure is a fenced code block in a design document whose info string's first word is a figure kind named in the template. For example, with the figure kind `mermaid`, a block opened with ` ```mermaid `.
- A figure and the text say the same. No fact appears only in a figure. Changing one changes the other.
- A figure shows only the current milestone's scope.
- The AI that draws a figure renders it and checks that no text overlaps or is cut off.

### The template

It is `.plumbline/template.md`. Reproduction makes it. Its form:

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

- The project part: the figure kind lines at the top and the seven section titles. A project that uses no figures has no figure line and no `---` lines around it.
- The reproduced part: from `<!-- plumbline:begin -->` to `<!-- plumbline:end -->`.

## 3. Flow

1. Once intent is confirmed, the lead and the user decide the template's project part (section titles, figure kinds).
2. The lead writes the module map from intent only. The user reads and confirms it.
3. For each milestone, its module documents are written in the module map's order. They are shown a few at a time; once the user reads and confirms a group, the next is written.
4. Once all of a milestone's module documents are confirmed, that milestone's impl is built.
5. When writing reveals a gap in intent, the lead stops and asks the user. After the answer, intent is fixed first.
6. When intent changes, the lead finds the design documents to look at again and tells the user.
7. When the section titles or figure kinds change, every module document is changed to match.

## 4. Invariants and contracts

- Every module document has the template's seven section titles, character for character, in order, and no other level-2 heading.
- A figure and the text say the same.
- No design document names a location of impl.
- A milestone's impl is not built until all its module documents are confirmed.

## 5. Decisions and reasons

- The module map is in the design README, so what applies to the whole design is read in one place. The README is not a module document, so it has no seven sections.
- Section titles are in the project's own words, since the user reads them. The number, order and meaning of the sections are the same in every project.
- A section that does not apply still appears, so something left out can be told from something absent.
- Overlapping or cut-off text in a figure is hard to check by machine, so the AI that draws it checks. Validate checks only that it renders.

## 6. Verification criteria

Shown by validate's conformance cases (Validate, Conformance cases).

- A module document whose seven section titles match the template, in order → pass.
- A document missing a section, with sections out of order, with a title that differs from the template's, or with another level-2 heading → a problem.
- The README at the top of the design location is not checked for sections.
- A README file in a folder below is a module document and is checked.
- Only a code block whose info string's first word is a figure kind is a figure.

## 7. Out of scope

None.
