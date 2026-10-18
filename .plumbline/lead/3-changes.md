# plumbline: rules for the lead (3 of 4): changes

A change is one unit of work, from opening to archive. Writing intent, the module map and the module documents for the first time is authoring. From the first reproduction on, each milestone's work is also a change. An intent or design document that was confirmed is changed through a change.

## Change records

- Each change has one folder, `.plumbline/changes/<name>/`, in git. Every folder directly under `.plumbline/changes/` is a change.
- `<name>` is `YYYY-MM-DD-<slug>`: the date the change was opened, then a slug of lowercase ASCII letters, digits and hyphens. No two changes have the same name.
- The folder holds `change.md`, and one file per gap item, `gap-<n>.md`, numbered 1, 2, 3 and so on in the order the gap items were recorded, with no leading zeros. Once the change is closed, it also holds `verify.md`, which only the verifier writes. It may hold other files the work needs.
- A change folder is never removed and never moved. A finished change stays where it is, with the state `archived`.
- A change record never holds content of intent. It names only its location: a document path, a version, a section.

`change.md` has front matter with exactly `state` (`open`, `closed` or `archived`) and `diagnosis` (`impl`, `design` or `intent`), each once. Its body, in the project's own words with no template, holds: what was asked, briefly; the diagnosis and what it rests on; for a bug, the current behaviour, the expected behaviour, and the behaviour that must not change; the tasks; how the result was confirmed; the commit that was checked out when the change was opened; the commits that belong to the change; once the change is verified, how each finding of its verify result was taken up.

## Diagnosis

When a change is opened, decide which layer is wrong:

| diagnosis | When | Layers changed | Intent version |
|---|---|---|---|
| `impl` | the design states the point rightly, and impl does not follow it | impl | unchanged |
| `design` | the design has a gap or an error, and intent does not state the point | design, then impl | unchanged |
| `intent` | intent states the point, and it must change | intent, then design, then impl | raised |

- A change is at the design level when it changes what the design states: public interfaces, invariants, decisions, verification criteria. It is at the intent level when it changes what intent states: goals and scope, decisions and their reasons, milestones.
- Diagnose from what the user said and from intent and design; never read impl. (1) When the request changes what intent states, the diagnosis is `intent`. (2) Otherwise, when it changes what the design states, `design`. (3) Otherwise, when you can tell this without impl, `impl`. (4) Otherwise, ask an implementer, with a hand-off that names the design sections and the question, then go back to (2).
- The diagnosis is written when the change is opened and never changed afterwards. A gap found later in the change is recorded as a gap item.
- The layers a change touches are the layer of its diagnosis and every layer below it, together with the layer of each confirmed gap item and every layer below that.

## Gap items

`gap-<n>.md` has front matter with exactly: `layer`, `intent` or `design`, the layer that has the gap; `state`, `proposed`, `confirmed` or `rejected`; and `date`, the date of the user's answer as `YYYY-MM-DD`, present exactly when the state is not `proposed`.

- The body says, in terms of the gap's layer, which section does not say something or says it wrongly, and what is proposed. For a gap in intent, the body names only the location in intent and what the layer below needs to know; the proposed wording is given to the user and is not written in the gap item.
- Record a gap item as `proposed` as soon as the gap is found, before proposing it to the user. Record the user's answer, `confirmed` or `rejected`, with the date of the answer. The state moves only from `proposed` to `confirmed` or `rejected`.
- When it is confirmed, the gap's layer is changed first, then the layers below. When it is rejected, the gap's layer stays as it is, and the layers below follow it.
- Within the current change, while one of its gap items is `proposed`, no layer below the gap's layer is edited. Other changes are not held back by it.

Wording fixes: a wording fix changes no meaning; it makes a document say what a confirmed decision, or another part of the same layer, already says. It is not a gap item. Make it at once, write in the change record which words were aligned to what (for intent, only the locations), and tell the user in the same report. When the user objects, record the point as a proposed gap item and handle it like any other. A fix that adds or changes what a layer states, or that has to choose between two readings neither of which a confirmed decision settles, is not a wording fix.

## The current change

- `.plumbline/current-change` holds one line: the name of an open change. When it is absent or empty, there is no current change.
- It belongs to one working tree and is never in git. Before writing it, make sure `.git/info/exclude` lists `/.plumbline/current-change`.
- Write it when you open a change or turn to another open change. Empty it when the current change is closed. An edit made while a change is current belongs to that change. Two changes worked on at the same time use two working trees.

## Opening, closing, verifying, archiving

1. Open: choose the name, write `change.md` with `state: open`, the diagnosis and the commit checked out now, and make the change current.
2. Work: record gap items and the user's answers; change the layers top-down; implementers build impl.
3. Close: when no gap item of the change is `proposed`, the body says how the result was confirmed, and `validate` in `gate` mode does not block, set `state: closed`. Empty `.plumbline/current-change` if it names this change. Never close a change while `validate` in `gate` mode blocks.
4. Verify: hand the closed change's check to a fresh verifier (part 1). The verifier writes `verify.md`.
5. Archive: when `verify.md` is there, the body of `change.md` names for every finding a follow-up change or the user's dated decision not to act on it, and the change's work is committed with its commits listed in `change.md`, set `state: archived`. The change's work is what it changed in the layers kept in git; intent is not committed. Edits to the change record itself may go into a later commit. When the change's work is not committed yet, ask the user to commit it first.

A change's state moves only from `open` to `closed` to `archived`.

The verify result, `verify.md`, has front matter with exactly one key, `result`: `clean` when there is no finding, `findings` otherwise. Its body numbers each finding, names the design document and section of each, and says whether the diagnosis held.

Taking up findings:

- Read `verify.md` and tell the user its findings. For each finding, the user decides to take it up or to decline it.
- For each finding, write in the body of `change.md` either the follow-up change that takes it up, as a link to that change's folder, or the user's decision not to act on it, with the date of that decision.
- A follow-up change is opened like any change, with its own diagnosis. Its body names the change and the findings it takes up, with a link to that change's folder. One follow-up change may take up several findings. For example, `.plumbline/changes/2026-11-02-a/change.md` links to `../2026-11-09-b/` for the finding, and `.plumbline/changes/2026-11-09-b/change.md` links to `../2026-11-02-a/` and names the finding by its number.
- A finding is never taken up by opening the closed change again.

## A milestone's work

- From the first reproduction on, the work of each milestone is one change with diagnosis `design`: its module documents and its impl, and, for every milestone after the first, the change of the design README's `milestone` line to it.
- Open it before that work starts: for the first milestone, after the first reproduction; for each later one, once the previous milestone's change is archived.
- A gap found while its module documents are written or its impl is built is a gap item of this change.
- Close it when the milestone's impl is done, like any change. Then it is verified and archived like any change.

## A decision that came from a gap

- When a gap item at the design layer is confirmed, the decision that settles it is written in section 5 of the module document it belongs to. Its confirmed marker carries the gap item's date.
- The same line holds a Markdown link to the change folder, as a path relative to the module document; the link text is in the project's own words. A module document directly in `docs/design` links to `../../.plumbline/changes/<name>/`.
- The change keeps the gap item after it is archived.
- A section 5 line that links to a change belongs only to a decision that settled a confirmed gap item of that change at the design layer.
