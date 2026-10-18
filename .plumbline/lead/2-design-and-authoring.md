# plumbline: rules for the lead (2 of 4): design documents and authoring

## Design documents

- Every Markdown file under `docs/design` is a design document. `docs/design/README.md` is the design's README: what applies to the whole design, such as scope, reading order and terms. Its front matter has exactly one `milestone: <name>` line, naming the milestone the design is in now, as intent names it. Every other design document, a `README.md` in a folder below included, is a module document. The module map is a module document.
- Front matter is the block at a document's very top: the first line is exactly `---`, the block ends at the next line that is exactly `---`, and every line between is `key: value`: a key of lowercase ASCII letters, digits, `_` and `-`, a colon and one space, and a value that is not empty. Any other line, a blank line included, makes it invalid.
- A module document has seven sections, as level-2 headings (`## `), equal to the template's level-2 headings, exactly and in order, and no other level-2 heading. Level-3 headings and below are free. A section that does not apply still appears and says so. What each holds: (1) responsibilities: what the module does and what it does not; (2) public interface: names, fields and contracts other modules or agents rely on; (3) flow: the main sequences; (4) invariants and contracts: conditions that always hold; (5) decisions and reasons: why it is this way, what was rejected; (6) verification criteria: what must be shown for the module to be right, for a mechanical part its conformance cases; (7) out of scope: what a later milestone adds.
- How design documents are laid out and named is the project's own.

The template, `.plumbline/template.md`, lies outside the design location and is not a design document. Its project part is its front matter, with `confirmed: <text>` once, `pending: <text>` once, one `figure: <name>` per kind of figure the project uses and no other key, and its seven level-2 headings, which are the project's section titles. You write the project part with the user before the module map is written. The `confirmed` text holds `YYYY-MM-DD` exactly once. Its reproduced part, between `<!-- plumbline:begin -->` and `<!-- plumbline:end -->`, is never edited by hand. When the project changes its section titles or marker texts, every module document is changed to match.

Basis lines: every design document, the README included, has front matter with one or more lines `basis: <intent document> <version>`: the path of an intent document from the project root, such as `docs/intent.md`, and that document's version when the design document was written or last checked against it. Every design document also names, in its text, the intent sections it is based on; that line has no fixed form.

Intent versions: every intent document has exactly one `version: V` line in its front matter. V is one or more non-negative integers joined by dots, such as `1` or `1.2`. Versions compare part by part as integers, and a missing part counts as 0: `1.10` is newer than `1.9`, and `1.2` equals `1.2.0`.

Design-level decisions:

- A decision the design makes because intent does not is a design-level decision. It is written in section 5 of the module document it belongs to. There is no other list or table of decisions.
- It carries a design-level marker: the template's `confirmed` text with the date the user confirmed it in place of `YYYY-MM-DD`, or the template's `pending` text.
- A decision that only restates intent carries no marker.
- A point intent states is never a design-level decision. A design that would change or narrow it reveals a gap in intent.
- A decision that settled a gap item also links to its change (part 3).

Figures: a figure is a fenced code block in a design document whose info string's first word is one of the template's `figure` names. A figure says the same as the text; no fact appears only in a figure, and changing one changes the other. A figure shows only the current milestone's scope. Every figure is rendered and checked for overlapping or cut-off text: `validate` checks that it renders where the setup has a renderer for its kind; whoever writes it checks that its text does not overlap and is not cut off.

A design document never names a location of impl: a path under an impl location (such as `rules/...`, or `README.md` at the project root), a test name, a case name. Nor how impl currently looks.

## Authoring

You and the user write intent, then the design's module map, then its module documents, milestone by milestone. You read intent and design only, never impl.

1. Intent: draft it, resolve it, confirm it.
2. The template's project part, then the module map and the design's README, whose `milestone` line names the first milestone. The user confirms the map.
3. The settings are complete, and the setup is reproduced.
4. The module documents of the first milestone. The user confirms them. Then implementers build that milestone's impl.
5. Each later milestone: once the previous milestone is finished, change the `milestone` line of the design's README to it; then its module documents are written, then its impl is built. A milestone is finished when its change is archived.

A milestone's module documents are all confirmed before its impl starts. Each milestone's work is one change, opened before that work starts (part 3). A gap found during it is a gap item of that change.

Writing intent:

1. Listen to the user and write a draft at the intent location. Every item in it carries one of three marks: decided (the user said or chose it), proposed (your default), open (a question).
2. Near its top, the draft names its three marks, in the project's own words. A new session can continue from the draft alone.
3. Resolve the open questions, then the proposals, one item at a time. A point that follows directly from earlier decisions is applied without asking, and the user is told. Only real choices are asked.
4. When no proposal and no open question is left, the intent is confirmed. Raise its version and state in it, in the project's own words, that the user confirmed it and on which date.

- An open item becomes proposed when you propose an answer, and decided when the user answers. A proposed item becomes decided when the user accepts or changes it. A decided item stays decided.
- The version stays the same while the draft is worked on. It is raised when the intent is confirmed.
- The form of intent is the project's, beyond Markdown files at the intent location, each with one version line.
- Do not ask about the natural language of the project's documents, a policy for code comments, or similar working conventions. When the user states them, they go into intent.

Settings: `.plumbline/settings.json` gives the layer locations and which layers are kept out of git. Propose each setting and have the user confirm it, and write it as soon as it is decided: the intent location before the first draft is saved, the design location before the module map is saved, the impl locations before the reproduction, and whether a layer stays out of git before anything of that layer is saved. As soon as a layer is set to stay out of git, list its paths in `.git/info/exclude`.

The module map:

1. After intent is confirmed, settle the template's project part with the user: the seven section titles, the two marker texts, and the kinds of figures the project uses, if any. Write them into the template.
2. Write the module map from intent only: the modules, their dependencies, the flows, and the contracts that hold for every module. With it comes the design's README: scope, reading order, terms, and the `milestone` line.
3. The map gives every module the milestone in which its document is written.
4. The user confirms the map. Every design-level decision in it then carries the confirmed marker with the date.

Module documents:

- They are written milestone by milestone, in the order the map gives. Each is derived from intent and the design documents above it, never from impl.
- Design-level decisions are written with the pending marker. When the user confirms them, each marker becomes the confirmed one with the date.
- You may present a milestone's documents in groups. Each group is confirmed before the next is written.
- A point the user must choose is asked one at a time. A point that follows directly from earlier decisions is applied, reported, and confirmed with the rest.
- When writing design reveals a gap in intent, stop and propose the change to intent. After the user confirms, intent is changed first and its version raised.
