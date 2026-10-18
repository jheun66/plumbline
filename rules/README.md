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
| [design-docs.md](design-docs.md) | design documents and module documents; the template; basis lines; design-level decisions; figures; how a check reads a Markdown document |
| [settings.md](settings.md) | the project settings: where the layers are, and which are kept out of git |
| [roles.md](roles.md) | lead, implementer and verifier: what each does, reads and writes; files in no layer; which role an agent plays; fresh agents; hand-off; the lead's part in changes; gaps between roles; a closed change checked by a verifier |
| [setup-record.md](setup-record.md) | the setup record; the roles of each carrier; renderers; checksums of reproduced files |
| [conformance.md](conformance.md) | mechanical parts; connectors; conformance cases; the parts of a setup |
| [authoring.md](authoring.md) | how the lead and the user write intent, the template's project part, the module map and the module documents |
| [changes.md](changes.md) | changes: change records, diagnosis, gap items, wording fixes, the verify result, taking up findings, the current change; opening, closing, verifying and archiving; a milestone's work as a change; decisions that came from a gap |
| [status.md](status.md) | `status`: the mechanical part that reports the current state of a project |
| [guards.md](guards.md) | guards; the gap guard; the role guard |
| [validate.md](validate.md) | `validate`: the mechanical part that checks design documents, change records and the setup against their formats |
| [verify.md](verify.md) | verify: the judgment check a fresh verifier makes on a closed change |
| [cases/](cases/) | the conformance cases of each mechanical part, one file per part |
| [carriers.md](carriers.md) | what the rule carriers tell each role, how they reach agents, and what carried text may hold; connectors and how each is checked |
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
| role | lead, implementer or verifier ([roles.md](roles.md)) |
| lead | the agent talking with the user; it works on intent and design |
| implementer | a fresh agent that builds impl from the design |
| verifier | a fresh agent that checks impl against the design for one closed change |
| hand-off | the lead giving work to a fresh implementer, a check to a fresh verifier, or, during a reproduction, a check of the role guard to either, by naming its role and what [roles.md](roles.md#hand-off) lists |
| reproduction (reproduce) | an agent building a project's setup from these rules and the project settings |
| setup | everything a reproduction writes and keeps in a project: rule carriers, document templates, guards, checks, their connectors, the setup record |
| setup record | what a reproduction used and produced ([setup-record.md](setup-record.md)) |
| project file | a file under the project root, outside `.git/`, that the project's own ignore rules do not ignore ([roles.md](roles.md#the-role-table)) |
| instruction file | the file an agent reads at the start of every session |
| rule carrier | where reproduced rules reach agents: an instruction file, a file it refers to, a script a hook runs, a skill, and so on |
| reproduced part / project part | in a file that both a reproduction and the project write: the lines the reproduction writes / everything else |
| mechanical part | a guard or a deterministic check in a setup |
| deterministic check / judgment check | a check that gives the same answer for the same input / a check that needs an agent's judgment |
| conformance case | an input and its expected result that a mechanical part must meet |
| must-block / must-pass | a conformance case the part must block / must let through |
| connector | what connects a mechanical part to an agent's hooks or to CI; it only translates |
| guard | a mechanical part that an agent's hook runs before an action that reads or writes files, to let it through or block it ([guards.md](guards.md)) |
| gap guard | the guard that blocks edits below a proposed gap item in the current change ([guards.md](guards.md#the-gap-guard)) |
| role guard | the guard that blocks reads and writes outside a role's row of the role table ([guards.md](guards.md#the-role-guard)) |
| figure | a fenced code block in a design document whose info string's first word is one of the template's figure names ([design-docs.md](design-docs.md#figures)) |
| renderer | a command recorded in the setup record that tells whether a figure of one kind renders ([setup-record.md](setup-record.md#renderers)) |
| change | one unit of work, from opening to archive ([changes.md](changes.md)) |
| change record | the folder of a change, with its `change.md`, its gap items and, once it is verified, its verify result |
| diagnosis | which layer a change finds wrong: `impl`, `design` or `intent` |
| gap item | a gap recorded in a change, with its layer and its state |
| wording fix | a fix that changes no meaning: it makes a document say what a confirmed decision, or another part of the same layer, already says ([changes.md](changes.md#wording-fixes)) |
| proposed / confirmed / rejected | the states of a gap item |
| current change | the open change a working tree is working on; an edit belongs to it |
| archive | marking a finished change as `archived`; it stays where it is |
| verify result | what a verifier writes into a closed change, `verify.md`: clean, or numbered findings ([changes.md](changes.md#the-verify-result)) |
| follow-up change | a change opened to take up findings of another change's verify result ([changes.md](changes.md#taking-up-findings)) |
