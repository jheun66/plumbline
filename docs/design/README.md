---
basis: docs/intent.md 1.4
milestone: M2
---

# plumbline design

> Basis: intent 1.4 — §1, §4 (principles 5–7), §6, §10, §11, §13. intent is not published.
> Stage 1 — module map: confirmed by the user on 2026-10-16.
> M0 module documents: bundles A (layers, design-docs, settings, roles), B (setup-record, conformance) and C (authoring, carriers, reproduction) confirmed by the user on 2026-10-17. The M0 design is complete.
> Revised after gaps reported while building M0 impl: roles, carriers, reproduction, setup-record and overview. Confirmed by the user on 2026-10-17, except decisions still marked pending.
> M1 module documents: bundles A (changes, roles), B (status, guards, and the `milestone` line in design-docs and authoring) and C (carriers, with M1 wording in reproduction, setup-record, conformance, settings, layers and design-docs) confirmed by the user on 2026-10-17. The M1 design is complete.
> Revised after gaps reported while building M1 impl: changes (a milestone's work is a change), status, guards, carriers, layers, design-docs, settings, setup-record, authoring and overview; every basis raised to intent 1.3 (archive keeps a change in place). Confirmed by the user on 2026-10-17, except decisions still marked pending.
> Revised after the M1 Done check on 2026-10-18: roles (a file in no layer is added to a layer before it is written; an implementer leaves a gap's point unbuilt), changes (wording fixes, intent 1.4), carriers and design-docs. Every basis raised to intent 1.4.
> M2 module documents: bundles A (roles, changes), B (design-docs, setup-record, validate, guards, verify) and C (carriers, reproduction, conformance) written on 2026-10-18.

## Where this document sits

```
intent  ──►  design (here)  ──►  impl
what, why    how it is divided,    the rules agents read,
             what it promises      conformance cases
```

- The design is derived only from intent. It is never written by looking at impl.
- Impl is built only from the design. The design must be enough on its own: if building impl needs a fact that only intent has, that is a gap in the design.
- When building impl reveals a gap or an error here, the implementer stops and reports it. The design is changed first, after the user confirms.
- The design defines public interfaces (names, fields, contracts). It never names impl locations (file paths, case names).
- intent is not published. The design cites intent versions and sections, but never copies intent content.

## What plumbline's impl is

plumbline's impl has two parts:

| Part | Read by | What it is |
|---|---|---|
| Rules | an agent reproducing a setup in a target project | what the setup must do, stated as rules only |
| Conformance cases | the same agent, after reproducing | inputs and expected results that the reproduced mechanical parts must meet |

The modules in this design divide the rules. Each module that defines a mechanical part also lists its conformance cases.

## Scope

The module map covers the first version: milestones M0 to M3. Module documents are written milestone by milestone, starting with M0. A module that grows over several milestones names the later parts under "Out of scope".

| Milestone | Modules written in that milestone |
|---|---|
| M0 | layers, design-docs, settings, roles, setup-record, conformance, authoring, carriers, reproduction |
| M1 | changes, status, guards (gap guard), carriers (change procedures), roles (the lead's work on changes), design-docs and authoring (the `milestone` line) |
| M2 | validate, verify, guards (role guard), carriers (verify procedure, connectors), roles (verifier, the full role table), changes (verify results, follow-up changes), setup-record (carrier roles, renderers), design-docs (figure kinds), reproduction and conformance (CI) |
| M3 | none. validate runs on plumbline's own design documents |

M0 documents are written in three bundles. Each bundle is confirmed by the user before the next is written.

| Bundle | Modules |
|---|---|
| A | layers, design-docs, settings, roles |
| B | setup-record, conformance |
| C | authoring, carriers, reproduction |

## Reading order

1. [overview.md](overview.md): module map, dependencies, flows, global contracts
2. Module documents, bottom tier first (the tiers are in the overview)

## Module document template

Every document in this folder except this README is a module document. Every module document has these seven sections, in this order. A section that does not apply says "None".

| # | Section | Says |
|---|---|---|
| 1 | Responsibilities | what the module does, and what it does not |
| 2 | Public interface | names, fields and contracts other modules or agents rely on |
| 3 | Flow | the main sequences |
| 4 | Invariants and contracts | conditions that always hold |
| 5 | Decisions and reasons | why it is this way, what was rejected. A design-level decision (one intent does not make) says so and carries the date the user confirmed it |
| 6 | Verification criteria | what must be shown for the module to be right. For a mechanical part, its conformance cases |
| 7 | Out of scope | what a later milestone adds |

In this design, a design-level decision ends with `(Design-level — confirmed YYYY-MM-DD)` or `(Design-level — pending)`. A decision that only restates intent carries no marker.

## Figures

When text is easier to follow as a picture, the document has the picture too.

| Content | Figure | Format |
|---|---|---|
| Dependencies between modules | flowchart | Mermaid |
| Formats and their relations (setup record, change record) | class diagram | Mermaid |
| Who does what in which order (reproduction, a change) | sequence diagram | Mermaid |
| Branching processing (diagnosis, guard verdicts) | flowchart | Mermaid |
| Things with states (gap items, changes) | state diagram | Mermaid |

- The figure and the text say the same thing. No fact appears only in a figure. Changing one changes the other.
- Every figure is rendered and checked for overlapping or cut-off text.
- A figure shows only the current milestone's scope.

## Terms

| Term | Meaning |
|---|---|
| layer | one of intent, design, impl |
| intent | what to build and why |
| design | how it is divided and what it promises |
| impl | the implementation, and any other product built from the design |
| read direction | which layers may be read when writing a layer |
| rules | the part of plumbline's impl that agents read |
| reproduction (reproduce) | an agent building a project's setup from the rules and the project settings |
| setup | everything reproduced: rule carriers, document templates, guards, checks |
| setup record | what a reproduction used and produced: rules commit, settings used, reproduced files |
| project settings | values a reproduction needs that differ per project |
| instruction file | the file an agent reads at the start of every session |
| rule carrier | where reproduced rules reach agents: an instruction file, a file it refers to, a script a hook runs, a skill, and so on |
| conformance case | an input and its expected result that a reproduced mechanical part must meet |
| connector | what connects a mechanical part to an agent's hooks or to CI. It only translates |
| must-block / must-pass | a conformance case the part must block / must let through |
| deterministic check / judgment check | a check that gives the same answer for the same input / a check that needs an agent's judgment |
| gap | a missing piece or an error in an upper layer, found from a lower one |
| proposed / confirmed / rejected | the states of a gap item |
| change | one unit of work, from opening to archive |
| current change | the open change a working tree is working on; an edit belongs to it |
| diagnosis | which layer is wrong |
| lead | the agent talking with the user; works on intent and design |
| implementer | a fresh agent that builds impl from the design |
| verifier | a fresh agent that checks impl against the design |
| archive | marking a finished change as archived; it stays where it is |
| verify result | what a verifier writes into a closed change: clean, or numbered findings |
| follow-up change | a change opened to take up findings of another change's verify result |
| role guard | the guard that blocks reads and writes outside a role's row of the role table |
| design-level decision | a decision the design makes because intent does not |
| milestone | a development stage set by intent |
| module map | a design's modules, their dependencies, flows and global contracts |

## Files

- One document per module, named after the module: `layers.md`, `changes.md`, and so on.
- When a module needs a second document, it becomes a folder with the first document as its `README.md`.
- Links between documents are relative. Moving a document updates its links.
