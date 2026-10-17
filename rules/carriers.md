# Rule carriers

A setup's rule carriers bring these rules to the agents that play each role in a project ([roles.md](roles.md)). The reproducing agent chooses them and writes them ([reproduction.md](reproduction.md)). Only what carried text must say is fixed here, not its wording.

## What each role must receive

The lead:

- the three layers, their locations, and which are kept out of git ([settings.md](settings.md));
- the read direction, the change direction, and gaps as proposals ([layers.md](layers.md));
- the whole role table, which role an agent plays, fresh agents, hand-off, and the gap flow ([roles.md](roles.md));
- when a hand-off must name the implementer's carrier (see "Choosing a role's carrier"), which file that is;
- how design documents are written: the template, basis lines, design-level markers, figures, and never naming impl locations ([design-docs.md](design-docs.md));
- the authoring procedure ([authoring.md](authoring.md));
- that the content of a layer kept out of git is never copied into a file in git ([settings.md](settings.md));
- that reproduced files and reproduced parts are never edited by hand, and that the setup changes only by changing the rules or the settings and reproducing again.

The implementer:

- its row of the role table: it reads design and impl, writes impl only, and never reads intent ([roles.md](roles.md));
- the design and impl locations, and the intent location as a place it never reads;
- how to read a design document: what each of the seven sections holds, what the design-level markers mean, and that a design never names impl locations ([design-docs.md](design-docs.md));
- that it builds only the design sections it is handed;
- that on a gap it stops and reports to the lead in terms of the design ([roles.md](roles.md)).

For both roles:

- Every location is stated as the settings give it.
- A rule enforced by instruction only (`enforcement` in [setup-record.md](setup-record.md)) is stated as an instruction. The `role table` is such a rule ([reproduction.md](reproduction.md)).

## How carriers reach agents

- The reproducing agent chooses the carriers from the means it has: an instruction file, part of one, a file it refers to, a script a hook runs, a skill, and so on.
- Each role's rules go in a carrier that only that role receives. Each role's rules reach only that role.
- A carrier that every agent reads by itself holds no role's rules. It holds nothing but the names of the roles, which role an agent plays ([roles.md](roles.md)), and, for each role whose rules no means can bring to that role alone, the carrier that holds them (see "Choosing a role's carrier"). A reproduction writes such a carrier only when it must name at least one role's carrier.
- The lead's carrier reaches the lead at the start of every session, without the user doing anything: through a means that reaches only the lead, or because the carrier every agent reads names it. When the reproducing agent has neither a means that reaches only the lead nor a means that every agent reads by itself, the reproduction stops with an environment error ([reproduction.md](reproduction.md)).
- An implementer receives its rules when it starts: through a means that reaches only the implementer, or because the carrier every agent reads names its carrier. When neither is possible, the lead's hand-off also names the carrier that holds them. The hand-off names nothing else but the role and design sections ([roles.md](roles.md)).
- An implementer's carrier tells it nothing about intent but its location.
- Every carrier file is in git, lies outside every layer location, and is listed in the setup record ([setup-record.md](setup-record.md)).
- Every rule the lead and the implementer must follow reaches them through a carrier. A project with its setup runs without these rules.

### Choosing a role's carrier

For the lead and the implementer alike:

1. When a means reaches only that role when it starts, by itself, the role's rules are carried there.
2. Otherwise they are carried in a file that only that role receives, and:
   - when there is a means that every agent reads by itself, a carrier there names the file for that role;
   - when there is no such means and the role is the implementer, the lead's hand-off names the file;
   - when there is no such means and the role is the lead, the reproduction stops with an environment error ([reproduction.md](reproduction.md)). A hand-off never gives the lead its file.
3. Every carrier file, the carrier every agent reads included, is written whole when the project does not also write it. When the project also writes it, it is written as a reproduced part (below). When it cannot hold the begin line and the end line, another file is chosen, and this step is applied to that file.

The carrier every agent reads by itself is written only when step 2 has it name at least one role's file. It holds nothing but the names of the roles, which role an agent plays, and the files step 2 has it name.

### An implementer starting work

1. The lead's hand-off names the role `implementer` and design sections, and also the implementer's carrier when the hand-off must name it (see "Choosing a role's carrier").
2. When there is a carrier that every agent reads by itself, the implementer learns there which role it plays. When no means reaches only the implementer, it also learns there which carrier holds its rules. When a means reaches only the implementer, that carrier does not name the implementer's carrier. When there is no carrier that every agent reads, this step does not happen.
3. The implementer reads its rules from its carrier.
4. It builds the design sections.

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

For each mechanical part connected to an agent or to CI, a connector is written under the contract in [conformance.md](conformance.md). A setup has no mechanical part ([conformance.md](conformance.md)), so it has no connector.
