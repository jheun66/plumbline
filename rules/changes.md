# Changes

A change is one unit of work, from opening to archive. The lead opens, closes and archives changes, diagnoses them, and records their gap items ([roles.md](roles.md)).

Writing intent, the module map and the module documents for the first time is authoring ([authoring.md](authoring.md)). From the first reproduction on, each milestone's work is also a change ([A milestone's work](#a-milestones-work)). An intent or design document that was confirmed is changed through a change.

## Change records

- Each change has one folder, `.plumbline/changes/<name>/`. It is in git.
- Every folder directly under `.plumbline/changes/` is a change.
- `<name>` is `YYYY-MM-DD-<slug>`: the date the change was opened, then a slug of lowercase ASCII letters, digits and hyphens. No two changes have the same name.
- The folder holds `change.md`, and one file per gap item, `gap-<n>.md`, numbered 1, 2, 3 and so on in the order the gap items were recorded. `<n>` is a positive integer written without leading zeros. A file whose name has any other form is not a gap item.
- The folder may hold other files the work needs.
- A change folder is never removed and never moved. A finished change stays where it is, with the state `archived`.
- A change record never holds content of a layer kept out of git ([settings.md](settings.md)). It names only its location: a document path, a version, a section.

## `change.md`

Its front matter ([layers.md](layers.md#documents-and-front-matter)) has exactly these keys, each once:

| Key | Value |
|---|---|
| `state` | `open`, `closed` or `archived` |
| `diagnosis` | `impl`, `design` or `intent` |

The body is written in the project's own words, with no template. It holds:

- what was asked, briefly;
- the diagnosis and what it rests on;
- for a bug: the current behaviour, the expected behaviour, and the behaviour that must not change;
- the tasks;
- how the result was confirmed;
- the commits that belong to the change.

Examples:

- Front matter with `state: open` and `diagnosis: design` is valid.
- Front matter with `state: done`, with `diagnosis: code`, with a third key, or with `state` twice is not.

## Diagnosis

When a change is opened, the lead decides which layer is wrong.

| `diagnosis` | When | Layers changed | Intent version |
|---|---|---|---|
| `impl` | the design states the point rightly, and impl does not follow it | impl | unchanged |
| `design` | the design has a gap or an error, and intent does not state the point | design, then impl | unchanged |
| `intent` | intent states the point, and it must change | intent, then design, then impl | raised ([layers.md](layers.md#intent-versions)) |

- A change is at the design level when it changes what the design states: public interfaces, invariants, decisions, verification criteria.
- A change is at the intent level when it changes what intent states: goals and scope, decisions and their reasons, milestones.
- The lead diagnoses from what the user said and from intent and design. It never reads impl ([roles.md](roles.md)).

How the lead diagnoses:

1. When the request changes what intent states, the diagnosis is `intent`.
2. Otherwise, when it changes what the design states, the diagnosis is `design`.
3. Otherwise, when the lead can tell this without impl, the diagnosis is `impl`.
4. Otherwise, the lead asks an implementer ([roles.md](roles.md#changes)), then goes back to step 2.

- The diagnosis is written when the change is opened and is never changed afterwards. A gap found later in the change is recorded as a gap item.
- The layers a change touches are the layer of its diagnosis and every layer below it, together with the layer of each confirmed gap item and every layer below that. They are not written down separately.

## Gap items

The front matter of `gap-<n>.md` ([layers.md](layers.md#documents-and-front-matter)) has exactly these keys, each once:

| Key | Value |
|---|---|
| `layer` | `intent` or `design`: the layer that has the gap |
| `state` | `proposed`, `confirmed` or `rejected` |
| `date` | only when `state` is `confirmed` or `rejected`: the date of the user's answer, `YYYY-MM-DD` |

- The body says, in terms of the gap's layer, which section does not say something or says it wrongly, and what is proposed.
- For a layer kept out of git, the body names only the location in that layer and what the layer below needs to know. The proposed wording is given to the user and is not written in the gap item.
- The lead records a gap item as `proposed` as soon as the gap is found, before proposing it to the user. It records the user's answer, `confirmed` or `rejected`, with the date of the answer.
- A gap item's state moves only from `proposed` to `confirmed` or `rejected`. It has a `date` exactly when it is not `proposed`.
- When a gap item is confirmed, the gap's layer is changed first, then the layers below ([layers.md](layers.md#change-direction)). When it is rejected, the gap's layer stays as it is, and the layers below follow it.
- While a gap item is `proposed`, no layer below its layer is edited within its change. Other changes are not held back by it. Where the setup enforces this mechanically, the gap guard does ([guards.md](guards.md#the-gap-guard)).

Examples:

- A gap item with `state: proposed` and no `date` is valid.
- A gap item with `state: proposed` and a `date`, or with `state: confirmed` and no `date`, is not.
- `gap-1.md`, `gap-2.md` and `gap-10.md` are gap items. `gap-01.md`, `gap-0.md` and `gap-a.md` are not.

## The current change

- `.plumbline/current-change` holds one line: the name of an open change.
- Its content, with every CR LF read as LF and one final LF removed, is the name. When the file is absent or that content is empty, there is no current change.
- The file belongs to one working tree and is never in git. Before writing it, the lead makes sure `.git/info/exclude` lists `/.plumbline/current-change`.
- The lead writes it when it opens a change or turns to another open change. It empties it when the current change is closed.
- An edit made while a change is current belongs to that change.
- Two changes worked on at the same time use two working trees.

Examples:

- `.plumbline/current-change` names change X, which has a proposed gap item at the design layer. An edit to an impl file belongs to X and is held back.
- `.plumbline/current-change` names change Y, which has no proposed gap item. The same edit belongs to Y and is not held back.
- An absent or empty `.plumbline/current-change` means there is no current change.
- `.plumbline/current-change` holding `2026-11-02-a` followed by CR LF names `2026-11-02-a`. One holding only LF names no change, so there is no current change.

## Opening, closing, archiving

1. **Open**: the lead chooses the name, writes `change.md` with `state: open` and the diagnosis, and makes the change current.
2. **Work**: the lead records gap items and the user's answers; the layers are changed top-down; implementers build impl ([roles.md](roles.md)).
3. **Close**: when no gap item of the change is `proposed`, and the body says how the result was confirmed, the lead sets `state: closed`. It empties `.plumbline/current-change` if that names this change.
4. **Archive**: when the checks that run at closing are done, the lead sets `state: archived`. These rules define no check that runs at closing, so a closed change may be archived at once.

A change's state moves only from `open` to `closed` to `archived`.

## A milestone's work

- From the first reproduction on, the work of each milestone is one change: its module documents and its impl ([authoring.md](authoring.md)), and, for every milestone after the first, the change of the design README's `milestone` line to it ([design-docs.md](design-docs.md#design-documents-and-module-documents)).
- Its diagnosis is `design`: the design does not yet hold that milestone's module documents.
- The lead opens it before that work starts: for the first milestone, after the first reproduction; for each later one, once the previous milestone's change is closed.
- A gap found while its module documents are written or its impl is built is a gap item of this change.
- It is closed when the milestone's impl is done, like any change: no gap item is `proposed`, and the body says how the result was confirmed.

## A decision that came from a gap

- When a gap item at the design layer is confirmed, the decision that settles it is written in section 5 of the module document it belongs to ([design-docs.md](design-docs.md#design-level-decisions)). Its confirmed marker carries the gap item's date.
- The same line holds a Markdown link to the change folder, as a path relative to the module document. The link text is in the project's own words.
- The change keeps the gap item after it is archived.
- A section 5 line that links to a change belongs only to a decision that settled a confirmed gap item of that change at the design layer.

Example: with the design at `docs/design`, a decision in `docs/design/cli.md` that settled a gap item of change `2026-11-02-a` links to `../../.plumbline/changes/2026-11-02-a/`.

## What always holds

- Every change folder has a `change.md` whose front matter has exactly `state` and `diagnosis`, with the values above.
- A change is closed only when none of its gap items is `proposed`.
- The diagnosis of a change never changes after it is opened.
- `.plumbline/current-change`, when it names a change, names an open one. It is never in git.
- Within a change, while one of its gap items is `proposed`, no layer below the gap's layer is edited.
- A change record holds no content of a layer kept out of git.
- Change folders are never removed or moved.
- From the first reproduction on, a milestone's work happens within that milestone's change.
