# plumbline rules

These rules set up a project to be developed in three layers: intent, design and impl. The rules are this folder, at one commit of the plumbline repository.

## Where to start

| Task | Done by | Start at |
|---|---|---|
| Writing a project's intent, then its design's module map and module documents, with the user | the project's lead | [authoring.md](authoring.md) |
| Reproducing a project's setup, the first time or again | the project's lead | [reproduction.md](reproduction.md) |

A project whose setup has been reproduced runs without these rules. Its agents receive their rules through the setup's rule carriers ([carriers.md](carriers.md)).

## Files

| File | States |
|---|---|
| [layers.md](layers.md) | the three layers; read direction; change direction; gaps; front matter; intent versions |
| [design-docs.md](design-docs.md) | design documents and module documents; the template; basis lines; design-level decisions; figures |
| [settings.md](settings.md) | the project settings: where the layers are, and which are kept out of git |
| [roles.md](roles.md) | lead and implementer: what each does, reads and writes; files in no layer; which role an agent plays; fresh agents; hand-off; the lead's part in changes; gaps between roles |
| [setup-record.md](setup-record.md) | the setup record; checksums of reproduced files |
| [conformance.md](conformance.md) | mechanical parts; connectors; conformance cases; the parts of a setup |
| [authoring.md](authoring.md) | how the lead and the user write intent, the template's project part, the module map and the module documents |
| [changes.md](changes.md) | changes: change records, diagnosis, gap items, wording fixes, the current change; opening, closing and archiving; a milestone's work as a change; decisions that came from a gap |
| [status.md](status.md) | `status`: the mechanical part that reports the current state of a project |
| [guards.md](guards.md) | guards; the gap guard |
| [cases/](cases/) | the conformance cases of each mechanical part, one file per part |
| [carriers.md](carriers.md) | what the rule carriers tell each role, how they reach agents, and what carried text may hold |
| [reproduction.md](reproduction.md) | how a setup is built from these rules and the project settings, and built again |

## Terms

| Term | Meaning |
|---|---|
| layer | one of intent, design, impl ([layers.md](layers.md)) |
| read direction | which layers may be read when writing a layer |
| gap | a missing piece or an error in an upper layer, found while working on a lower one |
| design-level decision | a decision the design makes because intent does not |
| module document | a design document with the seven sections ([design-docs.md](design-docs.md)) |
| module map | the module document that names a design's modules, their dependencies and milestones, the flows, and the contracts every module keeps |
| milestone | a development stage set by a project's intent. The design's README names the current one |
| template | a project's document template, `.plumbline/template.md` ([design-docs.md](design-docs.md)) |
| project settings | the values a reproduction needs that differ from project to project ([settings.md](settings.md)) |
| role | lead or implementer ([roles.md](roles.md)) |
| hand-off | the lead giving work to a fresh implementer by naming its role and design sections |
| reproduction (reproduce) | an agent building a project's setup from these rules and the project settings |
| setup | everything a reproduction writes and keeps in a project: rule carriers, document templates, guards, checks, the setup record |
| setup record | what a reproduction used and produced ([setup-record.md](setup-record.md)) |
| project file | a file kept in the project's repository; files that tools create while they run, such as build outputs and caches, are not project files ([roles.md](roles.md#files-in-no-layer)) |
| instruction file | the file an agent reads at the start of every session |
| rule carrier | where reproduced rules reach agents: an instruction file, a file it refers to, a script a hook runs, a skill, and so on |
| reproduced part / project part | in a file that both a reproduction and the project write: the lines the reproduction writes / everything else |
| mechanical part | a guard or a deterministic check in a setup |
| deterministic check / judgment check | a check that gives the same answer for the same input / a check that needs an agent's judgment |
| conformance case | an input and its expected result that a mechanical part must meet |
| must-block / must-pass | a conformance case the part must block / must let through |
| connector | what connects a mechanical part to an agent's hooks or to CI; it only translates |
| guard | a mechanical part that an agent's hook runs before an action that writes files, to let it through or block it ([guards.md](guards.md)) |
| change | one unit of work, from opening to archive ([changes.md](changes.md)) |
| change record | the folder of a change, with its `change.md` and its gap items |
| diagnosis | which layer a change finds wrong: `impl`, `design` or `intent` |
| gap item | a gap recorded in a change, with its layer and its state |
| wording fix | a fix that changes no meaning: it makes a document say what a confirmed decision, or another part of the same layer, already says ([changes.md](changes.md#wording-fixes)) |
| proposed / confirmed / rejected | the states of a gap item |
| current change | the open change a working tree is working on; an edit belongs to it |
| archive | marking a finished change as `archived`; it stays where it is |
