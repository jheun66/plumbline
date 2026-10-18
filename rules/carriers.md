# Rule carriers

A setup's rule carriers bring these rules to the agents that play each role in a project ([roles.md](roles.md)). The reproducing agent chooses them and writes them ([reproduction.md](reproduction.md)). Only what carried text must say is fixed here, not its wording.

## What each role must receive

The lead:

- the three layers, their locations, and which are kept out of git ([settings.md](settings.md));
- the read direction, the change direction, and gaps as proposals ([layers.md](layers.md));
- the whole role table, which role an agent plays, fresh agents, hand-off, and the gap flow ([roles.md](roles.md));
- when a hand-off must name the implementer's or the verifier's carrier (see "Choosing a role's carrier"), which file that is;
- when the means that reaches only the implementer, or only the verifier, needs that agent to be started in a particular way, how to start it;
- how design documents are written: the template, basis lines, design-level markers, figures, and never naming impl locations ([design-docs.md](design-docs.md));
- the authoring procedure ([authoring.md](authoring.md));
- that the content of a layer kept out of git is never copied into a file in git ([settings.md](settings.md));
- that reproduced files and reproduced parts are never edited by hand, and that the setup changes only by changing the rules or the settings and reproducing again;
- changes ([changes.md](changes.md)):
  - opening one: its name, `change.md` with its state and diagnosis and the commit checked out when it was opened ([changes.md](changes.md#changemd)), making it current, and listing `/.plumbline/current-change` in `.git/info/exclude` before writing it;
  - each milestone's work, from the first reproduction on, as one change with diagnosis `design`, opened before that work starts and closed when the milestone's impl is done ([changes.md](changes.md#a-milestones-work));
  - the three diagnoses, what each changes, when the intent version is raised, how to tell the design level from the intent level, and asking an implementer when a diagnosis needs impl;
  - for a bug, the current, the expected and the unchanged behaviour;
  - recording a gap item before proposing it, and the user's answer with its date; what a gap item may hold for a layer kept out of git;
  - making a wording fix at once without a gap item, recording what was aligned to what, telling the user, and turning it into a gap item when the user objects ([changes.md](changes.md#wording-fixes));
  - closing: no gap item proposed, how the result was confirmed, `validate` in `gate` mode not blocking, emptying the current change; and archiving, once the verify result is there and each of its findings is taken up;
  - the section 5 line of a decision from a gap, with its link to the change;
  - that a change record holds no content of a layer kept out of git;
- status ([status.md](status.md)):
  - how to run it, as the setup record gives its runner and entry ([setup-record.md](setup-record.md#parts));
  - to run it at the start of every session, before anything else, with empty standard input, and to tell the user the state in a few lines, in the project's own words, before acting on the user's request;
  - to use the rules only to reproduce, and the rules repository only to fetch its tags as below;
  - when the user asks for the state or about the rules, to fetch the tags of the rules repository the setup record names when the network is available, and to run it with them on standard input;
- the gap guard ([guards.md](guards.md#the-gap-guard)):
  - when it blocks a write, to tell the user which gap item must be answered;
  - when it reports an environment error, to tell the user;
  - never to write a blocked file another way;
- a project file in no layer that the role table lets no role write ([roles.md](roles.md#files-in-no-layer)): that no role writes it; when the work needs one, to propose to the user adding its path to a layer, and after the user agrees, to edit the settings and reproduce;
- validate ([validate.md](validate.md)):
  - how to run it, as the setup record gives its runner and entry ([setup-record.md](setup-record.md#parts));
  - to tell the user the problems it reports at the end of a turn, in the project's own words, without stopping on them;
  - before closing a change, to run it in `gate` mode, and never to close a change while it blocks;
  - when the project has no CI that runs it, to tell the user so;
- verify ([verify.md](verify.md), [changes.md](changes.md#the-verify-result)):
  - once a change is closed, to hand its check to a fresh verifier with the hand-off [roles.md](roles.md#hand-off) states, and how to start the verifier when its means needs that;
  - to read `verify.md` and tell the user the findings;
  - for each finding, to open a follow-up change or to record the user's decision not to act on it with its date, linking the changes both ways ([changes.md](changes.md#taking-up-findings));
  - to archive the change only then;
- the role guard ([guards.md](guards.md#the-role-guard)):
  - when it blocks a read or a write, never to do it another way;
  - when the work needed that read or write, to tell the user.

The implementer:

- its row of the role table: it reads design and impl, writes impl only, and never reads intent ([roles.md](roles.md));
- the design and impl locations, and the intent location as a place it never reads;
- how to read a design document: what each of the seven sections holds, what the design-level markers mean, and that a design never names impl locations ([design-docs.md](design-docs.md));
- that it builds only the design sections it is handed;
- that on a gap it stops and reports to the lead in terms of the design, leaves that point unbuilt and chooses no way to build it ([roles.md](roles.md#a-gap-found-by-the-implementer));
- that when a hand-off asks for a check of the role guard ([roles.md](roles.md#hand-off)), it tries the reads the hand-off lists, and a blocked read is the expected result;
- when a read or a write is blocked, to stop that work and report to the lead; never to read or write a blocked file another way;
- when the work needs a file in no layer, to stop that work and report it to the lead ([roles.md](roles.md#files-in-no-layer)).

The verifier:

- its row of the role table: it reads design and impl and their git history, never reads intent or change records, and writes only the `verify.md` of the change it is given ([roles.md](roles.md));
- the design and impl locations, and the intent location as a place it never reads;
- how to read a design document, as the implementer receives it;
- what the hand-off names ([roles.md](roles.md#hand-off));
- what it looks for, and how it judges whether the diagnosis held ([verify.md](verify.md));
- the place and the form of `verify.md`: findings numbered and named in terms of the design, impl locations allowed, impl content never quoted ([changes.md](changes.md#the-verify-result));
- to tell the lead when it is done;
- when a read or a write is blocked, never to do it another way;
- that when a hand-off asks for a check of the role guard ([roles.md](roles.md#hand-off)), it tries the reads the hand-off lists, and a blocked read is the expected result.

For every role:

- Every location is stated as the settings give it.
- A rule enforced by instruction only (`enforcement` in [setup-record.md](setup-record.md)) is stated as an instruction.
- When the setup record gives the `role table` as `instruction`, each role receives its row of the role table as an instruction ([roles.md](roles.md#the-role-table)).
- When the setup record gives the `gap guard` as `instruction`, the lead receives the rule itself: within the current change, while a gap item is proposed, no layer below it is edited ([changes.md](changes.md#gap-items)).
- When the setup record gives `validate at the end of a turn` as `instruction`, the lead receives the instruction to run `validate` in `report` mode at the end of every turn that edited files, and to tell the user what it reports.

## How carriers reach agents

- The reproducing agent chooses the carriers from the means it has: an instruction file, part of one, a file it refers to, a script a hook runs, a skill, and so on.
- A means reaches a role by itself when, once an agent of that role has started, its rules reach the agent without anyone pointing the agent to them. Such a means may need the agent to be started in a particular way, for example as a given agent type. The implementer or the verifier is then started that way ([roles.md](roles.md#hand-off)). For the lead, and for a means that every agent reads by itself, only a means that needs no particular way of starting counts.
- Each role's rules go in a carrier that only that role receives. Each role's rules reach only that role.
- What a reproduction writes in a carrier that every agent reads by itself holds no role's rules. It holds nothing but the names of the roles, which role an agent plays ([roles.md](roles.md)), and, for each role whose rules no means can bring to that role alone, the carrier that holds them (see "Choosing a role's carrier"). A reproduction writes such a carrier only when it must name at least one role's carrier.
- The lead's carrier reaches the lead at the start of every session, without the user doing anything: through a means that reaches only the lead, or because the carrier every agent reads names it. When the reproducing agent has neither a means that reaches only the lead nor a means that every agent reads by itself, the reproduction stops with an environment error ([reproduction.md](reproduction.md)).
- An implementer or a verifier receives its rules when it starts: through a means that reaches only that role, or because the carrier every agent reads names its carrier. When neither is possible, the lead's hand-off also names the carrier that holds them. Beyond that, the hand-off names only what [roles.md](roles.md#hand-off) states.
- An implementer's carrier tells it nothing about intent but its location, and nothing about changes.
- A verifier's carrier tells it nothing about intent but its location, and nothing about changes but the place and the form of `verify.md`.
- Every carrier file is in git, lies outside every layer location, and is listed in the setup record ([setup-record.md](setup-record.md)).
- Every rule the lead, the implementer and the verifier must follow reaches them through a carrier. A project with its setup runs without these rules.

### Choosing a role's carrier

For the lead, the implementer and the verifier alike:

1. When a means reaches only that role when it starts, by itself, the role's rules are carried there.
2. Otherwise they are carried in a file that only that role receives, and:
   - when there is a means that every agent reads by itself, a carrier there names the file for that role;
   - when there is no such means and the role is the implementer or the verifier, the lead's hand-off names the file;
   - when there is no such means and the role is the lead, the reproduction stops with an environment error ([reproduction.md](reproduction.md)). A hand-off never gives the lead its file.
3. Every carrier file, the carrier every agent reads included, is written whole when the project does not also write it. When the project also writes it, it is written as a reproduced part (below). When it cannot hold the begin line and the end line, another file is chosen, and this step is applied to that file.

The carrier every agent reads by itself is written only when step 2 has it name at least one role's file. What a reproduction writes in it holds nothing but the names of the roles, which role an agent plays, and the files step 2 has it name.

### An implementer or a verifier starting work

1. The agent is started with the lead's hand-off, by the lead or by the user ([roles.md](roles.md#hand-off)). The hand-off names the role and what [roles.md](roles.md#hand-off) lists for it, and also the role's carrier when the hand-off must name it (see "Choosing a role's carrier"). When the means that reaches only that role needs the agent to be started in a particular way, it is started that way.
2. When there is a carrier that every agent reads by itself, the agent learns there which role it plays. When no means reaches only its role, it also learns there which carrier holds its rules. When a means reaches only its role, that carrier does not name the role's carrier. When there is no carrier that every agent reads, this step does not happen.
3. The agent reads its rules from its carrier.
4. An implementer builds the design sections. A verifier checks the change ([verify.md](verify.md)). When the hand-off asks for a check of the role guard instead, the agent tries the reads the hand-off lists.

## What carried text may hold

- Rules only: no reasons, no history, no open questions ([layers.md](layers.md)).
- No pointer to plumbline's intent or design.
- No content of a layer kept out of git. Only its location.
- Nothing these rules do not say. What a project adds goes in a project part.

## Reproduced parts and project parts

- When a carrier is a file the project also writes, a reproduction writes only its reproduced part, between a begin line and an end line. The reproducing agent chooses the two lines to suit the file type, and the setup record names them ([setup-record.md](setup-record.md)).
- Everything outside those two lines is the project's part. Reproducing again leaves it as it is.
- A project part holds the project's own working rules, such as what its intent decided about natural language or code comments. A reproduced part never holds such rules.
- A file the project also writes that cannot hold the two lines is not used. The reproducing agent chooses another file.

## The template's reproduced part

- The template ([design-docs.md](design-docs.md)) is a file with both parts. Its project part is the lead's ([authoring.md](authoring.md)).
- Its reproduced part says what each of the seven sections is for, how basis lines are written, and how the two markers are used.
- It holds no level-2 heading, and it comes after the template's front matter.

## Connectors

For each mechanical part connected to an agent or to CI, a connector is written under the contract in [conformance.md](conformance.md#connectors). Connectors are setup files: each file of one is listed in the setup record ([setup-record.md](setup-record.md)). A connector written into a file the project also writes is a reproduced part of it.

- **The gap guard** ([guards.md](guards.md#the-gap-guard)) is connected to the hook that an agent's file-writing actions pass through before they happen, for the lead and the implementer alike. The connector gives the guard the paths the action will create, change or remove.
- **The role guard** ([guards.md](guards.md#the-role-guard)) is connected to the hook that an agent's file-reading and file-writing actions pass through before they happen, for every role. The connector gives the guard the role the agent plays, the action, `read` or `write`, and the paths: for a search, the files and folders it searches. When the connector cannot tell which role an agent plays, the `role table` is enforced by instruction only.
- **validate at the end of a turn** ([validate.md](validate.md)) is connected to the hook that runs when the lead ends a turn. It runs `validate` in `report` mode and gives its lines to the lead. It may let the lead go on once, so that the lead can tell the user what `validate` reports. It never holds the lead back more than once in a turn, and never blocks.
- **validate before closing** has no connector. The lead runs `validate` in `gate` mode before it closes a change, and never closes the change while it blocks.
- **validate in CI** is a step of the CI the project uses ([reproduction.md](reproduction.md#steps)). The step runs `validate` in `gate` mode with its runner and entry, and fails when the verdict is `block` or `error`, saying which. When the project uses no CI, there is no such step, and `validate in CI` is enforced by instruction only.
- **status** ([status.md](status.md)) has no connector. The lead runs it with its runner and entry ([setup-record.md](setup-record.md#parts)).

No agent reads or writes a file the role guard blocked by another way. No agent writes a file the gap guard blocked by another way.

The files a reproduction writes for the checks below are written by the lead ([roles.md](roles.md#the-role-table)), and every check leaves nothing behind.

### Checking the gap guard's connector

In step 7 of a reproduction ([reproduction.md](reproduction.md#steps)), the reproducing agent acts through the gap guard's connector:

1. It writes a temporary change with a proposed gap item at the intent layer, and makes it current, as [changes.md](changes.md#the-current-change) states for writing `.plumbline/current-change`.
2. An action that creates a new file in the design location must be blocked.
3. An action that creates a new file outside the project root must pass.
4. It removes the temporary change and every file the check created, and puts `.plumbline/current-change` back as it was.

Each new file in steps 2 and 3 is at a path that does not exist yet.

Nothing of the check reaches git, and the check leaves no change, file or marker behind.

### Checking the role guard's connector

1. Acting as the lead, the reproducing agent reads a path that lies under an impl location and does not exist. The read must be blocked. Then it reads a design document. The read must pass.
2. For the implementer and for the verifier, the reproducing agent starts an agent of that role as the setup starts it, with a hand-off that says it is a check of the role guard and asks only for two reads: a path that lies under the intent location and does not exist, which must be blocked; and a design document, which must pass.

A path under a location that is a file lies in that location's layer: with intent at `docs/intent.md`, `docs/intent.md/x` is such a path ([guards.md](guards.md#the-role-guard)).

Reads change nothing, so the check leaves nothing behind.

### A connector that cannot be checked in this session

When the reproducing agent cannot start an agent of a role until a new session, for example because the means that starts it was written by this reproduction, the rule whose connector check needs that agent is enforced by instruction only. The final report of the reproduction tells the user to reproduce again in a new session ([reproduction.md](reproduction.md#steps)).

Such a connector stays in place, and its files are listed in the setup record ([setup-record.md](setup-record.md)). So does a connector whose check did not give the expected results and could not be corrected.

### Checking validate's connector at the end of a turn

1. The reproducing agent writes a temporary module document with no level-2 heading in the design location.
2. It runs the connector as the hook would run it at the end of a turn. The lead must be given a `sections` line for that document, and nothing must be blocked.
3. It removes the document.

### Checking the CI connector

1. The reproducing agent copies the project to a temporary folder outside the project.
2. It runs the CI step's command there, as CI would run it: once with the copy as it is, and once after writing a temporary module document with no level-2 heading into the copy's design location.
3. Each time, the step must fail exactly when `validate` in `gate` mode blocks on the copy, or gives `error`.
4. It removes the copy.

## What always holds

- Every rule that the lead, the implementer and the verifier must follow reaches them through a carrier.
- Carried text holds rules only, with no reasons, no history, no pointer to plumbline's intent or design, and no content of a layer kept out of git.
- An implementer's or a verifier's carrier tells it nothing about intent but its location.
- Each role's rules reach only that role.
- Reproducing again never changes a project part.
- Every carrier file is listed in the setup record.
- No agent writes a file the gap guard blocked by another way.
- No agent reads or writes a file the role guard blocked by another way.
- The lead never closes a change while `validate` in `gate` mode blocks.
- The connector checks leave nothing behind.
