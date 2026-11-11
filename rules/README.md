# plumbline rules

These rules set up a project to be developed in three layers: intent, design and impl. An AI reads them and reproduces the setup in the project: the rules each role follows, brought to it by rule carriers; the role guard; validate; the template; and the setup record.

The rules are the folder `rules` of the plumbline repository, at one commit: the files below and their conformance cases. An AI that uses the rules starts at this file, and reads nothing else of the repository.

## Where to start

| Task | Done by | Start at |
|---|---|---|
| Starting plumbline in a project that has no setup yet | the project's lead | [Starting a project](#starting-a-project) |
| Reproducing the setup again | the project's lead | [reproduction.md](reproduction.md) |

A project whose setup has been reproduced runs without these rules. Its AIs receive their rules through the setup's rule carriers ([reproduction.md](reproduction.md#what-each-role-receives)).

## Starting a project

When the user asks an AI to reproduce the setup in a project that has none yet, that AI is the project's lead. With the user, it goes through these steps, in order:

1. Write and confirm intent ([intent-writing.md](intent-writing.md)).
2. Decide the template's project part with the user and write it, then write the module map; the user confirms it ([design-docs.md](design-docs.md#writing-and-confirming-the-design)).
3. Complete the settings with the user: layer locations, layers kept out of git, zones, every role's name, read zones, write zones, duty and model, and guard choices ([layers.md](layers.md#the-settings-file)). Agree on the workflow, including assignments, shared work, reports, findings and all five checks ([change.md](change.md#the-projects-workflow)).
4. Reproduce the setup ([reproduction.md](reproduction.md)).
5. For each milestone, write its module documents; the user reads and confirms all of them ([design-docs.md](design-docs.md#writing-and-confirming-the-design)).
6. The configured roles build impl and complete the five checks through the project's workflow ([roles.md](roles.md), [change.md](change.md)). Whether building and checking use different roles is a project choice.

Each layer's location and git exclusion are decided before that layer's first file is saved ([layers.md](layers.md#steps)). Roles, models, guards and workflow have no defaults. Reproduce again when the settings or rules commit change, or when a workflow change needs different carriers or role startup.

## Files

| File | States |
|---|---|
| [layers.md](layers.md) | the three layers, settings, named zones, role entries and guard choices |
| [roles.md](roles.md) | the lead, project-defined roles, their limits, file-part recognition and shell inspection |
| [design-docs.md](design-docs.md) | design documents and module documents; the module map; the seven sections; how to write; figures; the template; how a Markdown document is read |
| [intent-writing.md](intent-writing.md) | how intent is written and confirmed with the user |
| [change.md](change.md) | a change, from diagnosis to commit; the project workflow, hand-offs, work note and five checks |
| [status.md](status.md) | how the lead answers when the user asks where things stand; things to fix; newer rules |
| [validate.md](validate.md) | `validate`: the checks run on request, and their output |
| [setup-record.md](setup-record.md) | the settings snapshot, role carriers, commands, tested enforcement and instruction limits, and checksums |
| [conformance.md](conformance.md) | the contract of a mechanical part; connectors; the form of conformance cases and how they run |
| [reproduction.md](reproduction.md) | how the lead builds the setup, what each role receives, and reproducing again |
| [cases/](cases/) | the conformance cases, one file per mechanical part |

## For every AI

- What reaches the user, such as questions, notices and check results, is said in plain words, with no name left unexplained.
- Each project decides its own language and its own code comment policy.
- The content of a layer kept out of git is never copied into a file of a layer in git ([layers.md](layers.md#what-always-holds)).
- Reproduced files and reproduced parts are never edited by hand ([reproduction.md](reproduction.md#what-always-holds)).

## Terms

| Term | Meaning |
|---|---|
| layer | one of intent, design and impl ([layers.md](layers.md)) |
| read direction | which layers are read when writing a layer |
| location | a path from the project root that a layer is at ([layers.md](layers.md#the-settings-file)) |
| project settings, settings file | the settings that differ from project to project, in `.plumbline/settings.json` |
| role | the built-in lead or one of the project's configured members ([roles.md](roles.md)) |
| lead | the AI that talks with the user, writes intent and design, and reproduces |
| zone | a named selection of design or impl, using paths and optionally file-name patterns and file parts ([layers.md](layers.md#zones)) |
| workflow | the project's assignments, coordination, communication and checking arrangements ([change.md](change.md#the-projects-workflow)) |
| the five checks | the required checks of criteria, invariants, public names, design boundaries and diagnosis ([change.md](change.md#the-five-checks)) |
| hand-off / report | a role's assigned work and context / its progress, results, gaps and findings ([change.md](change.md#hand-offs-and-reports)) |
| gap | something missing or wrong in a higher layer, found while working on a lower one |
| design README | the file `README.md` directly in the design location ([design-docs.md](design-docs.md)) |
| module map | the part of the design README that names the modules, what relies on what, the flows, the promises for every module and the milestones |
| module document | a design document with the seven sections |
| the seven sections | the sections every module document has, in order ([design-docs.md](design-docs.md#the-seven-sections)) |
| template | `.plumbline/template.md`: the section titles, the figure kinds, and what each section holds ([design-docs.md](design-docs.md#the-template)) |
| figure | a fenced code block in a design document whose kind the template names ([design-docs.md](design-docs.md#figures)) |
| milestone | a stage of development, set by intent |
| change | one piece of work, from diagnosis to commit ([change.md](change.md)) |
| diagnosis | which layer a change finds wrong: impl, design or intent |
| work note | the note of the change in progress ([change.md](change.md#the-work-note)) |
| status | where things stand ([status.md](status.md)) |
| reproduction (reproduce) | the lead building a project's setup from these rules and the project settings ([reproduction.md](reproduction.md)) |
| setup | what a reproduction writes in a project: rule carriers, the template's reproduced part, the mechanical parts, their connectors, and the setup record |
| setup record | what a reproduction used and wrote ([setup-record.md](setup-record.md)) |
| instruction file | the file an AI tool has an AI read at the start of every session |
| rule carrier | what brings a role its rules: an instruction file, part of one, a file it points to, a script a hook runs, a skill, and so on |
| reproduced part / project part | in a file that both a reproduction and the project write: the lines between the begin line and the end line, which the reproduction writes / the rest |
| mechanical part | a part that runs without an AI and keeps the contract in [conformance.md](conformance.md): the role guard and validate |
| role guard | the mechanical part that checks mandatory intent-read and design-write limits, requested zone guards and chosen shell inspection ([roles.md](roles.md#the-role-guard)); coverage is recorded only after cases and connector checks pass |
| validate | the mechanical part that checks the whole project when the user asks ([validate.md](validate.md)) |
| environment error | a mechanical part could not give `pass` or `block` |
| conformance case | an input and the result a mechanical part must give for it |
| must-block case / must-pass case | a conformance case that expects `block` / `pass` |
| connector | what connects a mechanical part to an AI tool's hooks; it only translates |
| runner | the program that runs a mechanical part's entry file |
| renderer | a command that tells whether a figure of one kind renders |
