# Reproduction

A reproduction builds a project's setup from these rules and the project settings. The form of the setup record is in [setup-record.md](setup-record.md). How cases run is in [conformance.md](conformance.md).

## Who and when

- The lead reproduces, in its conversation with the user.
- The first reproduction comes after the module map is confirmed and the settings are complete ([README.md](README.md#starting-a-project)).
- A project reproduces again when it moves to another rules commit, when its settings change, or when the user asks.

## Input

- The plumbline repository and a commit: those the user names, or else those in the setup record. A tag is resolved to its commit. On a first reproduction with no commit given, the lead asks the user; it may propose the newest tag.
- The repository's address must be reachable from other machines ([setup-record.md](setup-record.md#rules)). When given a copy on the machine, the lead reads the rules from that copy, and asks the user for the address of the original repository. Without an address, it stops before writing anything.
- The settings file, the previous setup record, the project parts of carrier files, and the template's project part.

## When it stops before writing anything

When any of these holds, the lead writes nothing, stops, and tells the user why in plain words:

- The project is not a git repository.
- The settings file is missing or does not have its form ([layers.md](layers.md#the-settings-file)).
- A layer location is `.plumbline`, contains it, or lies inside it.
- The template's project part does not exist yet ([design-docs.md](design-docs.md#the-template)).
- The previous setup record exists, and what the reproduction reads from it, its `rules`, `settings`, `files`, `carriers`, `parts` and `renderers`, does not have its form ([setup-record.md](setup-record.md#the-form)). These are read as they are, though: a record written under older rules that lacks a key newer rules added; a repository that is not an address; and a command the current rules do not allow. Such a command is not kept; a new one is chosen.
- There is no setup record, but the git history of the commit checked out has one: it was removed by hand. The lead asks the user to restore it from git.
- A file the previous setup record lists with a reproduced part exists, but the part cannot be found in it ([setup-record.md](setup-record.md#checksums)). The lead names the file, and the boundary line that is missing, appears twice, or comes out of order.
- No carrier can reach the lead by itself at the start of every session ([How carriers reach roles](#how-carriers-reach-roles)). This is an environment error.
- The rules at that commit cannot be read.

## Reading the rules

- The lead reads only these rules and their conformance cases, the folder `rules` at that commit, from a copy kept outside the project. It reads nothing else of the copy, and never plumbline's design, even when the copy holds it.
- No rule file and no conformance case is copied into the project. What AIs must do reaches them through carriers.
- When the rules do not say what to produce, the lead does not fill the gap. It stops, says what the rules do not say, and proposes a change to the rules.

## Steps

1. Tell the user which files in the previous setup record are missing or have a different checksum: they were removed or edited by hand. Only with the user's agreement are they written again, or removed in step 8. Without agreement, stop before writing anything.
2. Choose the rule carriers and write them ([What each role receives](#what-each-role-receives), [How carriers reach roles](#how-carriers-reach-roles)). Keep project parts as they are.
3. Write the template's reproduced part ([design-docs.md](design-docs.md#the-template)). Keep its project part as it is.
4. Add to `.git/info/exclude`, when missing, a line for each location of a layer kept out of git, `/` followed by the location, and the work note's place, `/.plumbline/work-note.md`. Remove the lines of a layer that was kept out of git before and no longer is.
5. Write the parts, the role guard and validate, and their connectors ([Connectors](#connectors)), and choose a runner for each part. A runner counts as present only when it can be recorded by a name found on the PATH ([setup-record.md](setup-record.md#commands)). When none is present, report an environment error that names what is missing, and stop. For each figure kind in the template, choose a renderer present on this machine; when none is, record none. A renderer that can be reached only through an absolute path is recorded as none too.
6. Run every conformance case ([conformance.md](conformance.md#running-a-case)). When one fails, fix the part and run every case again.
7. Act through the connectors ([Checking connectors](#checking-connectors)).
8. Remove the files and reproduced parts the previous setup record listed and this reproduction no longer writes.
9. Write the setup record anew, whole ([setup-record.md](setup-record.md)).
10. Tell the user in plain words:
    - which rules are enforced mechanically and which are left as instructions;
    - which files were written, changed and removed;
    - what to commit: the setup record, and the files listed in the previous or the new setup record that changed. The reproduction commits nothing;
    - for each renderer recorded as none because only an absolute path reaches it, what to put on the PATH;
    - when a connector check needed a role that can be started only in a new session, that the setup is to be reproduced again in a new session;
    - when a carrier was written or changed and it is read only when a session starts, that it reaches its role only from a new session on.

## What each role receives

The carriers bring each role these rules, from the files named:

The lead:

- the three layers, their locations, and the layers kept out of git ([layers.md](layers.md));
- the read direction, fixing from the top down, and asking about gaps ([layers.md](layers.md#the-three-layers), [change.md](change.md));
- the whole role table, which role an AI plays, how to start the implementer and the verifier, and the hand-offs ([roles.md](roles.md));
- how to write design documents ([design-docs.md](design-docs.md));
- writing intent ([intent-writing.md](intent-writing.md));
- a change ([change.md](change.md));
- status ([status.md](status.md));
- how to run validate and report its result ([validate.md](validate.md#telling-the-user));
- what to do when the role guard blocks or reports an environment error ([roles.md](roles.md#the-role-guard));
- how to reproduce: from the repository and commit the setup record names, by reading these rules from a copy kept outside the project ([Reading the rules](#reading-the-rules));
- that the content of a layer kept out of git is never copied into a file of a layer in git;
- that reproduced files and reproduced parts are never edited by hand, and that the setup changes only by changing the rules or the settings and reproducing again.

The implementer:

- its row of the role table ([roles.md](roles.md#the-three-roles));
- the layer locations, and the intent location as a place it never reads;
- how to read a design document: what the seven sections hold, and that the design never names locations of impl ([design-docs.md](design-docs.md));
- that it builds only the design sections it is handed;
- that on a gap it leaves that point unbuilt, and reports it in terms of the design ([roles.md](roles.md#the-implementers-work));
- that when a file that belongs to no layer must be written, it stops that work and reports it;
- that when the role guard blocks it, it stops that work and reports it, and never does it another way;
- its report ([roles.md](roles.md#reports)).

The verifier:

- its row of the role table ([roles.md](roles.md#the-three-roles));
- the layer locations, and the intent location as a place it never reads;
- how to read a design document, as the implementer receives it;
- its hand-off ([roles.md](roles.md#hand-offs));
- the five checks, and how to judge whether the diagnosis held ([change.md](change.md#what-the-verifier-checks));
- its report ([roles.md](roles.md#reports));
- that when the role guard blocks it, it never does it another way.

For every role:

- Every location is written as the settings give it.
- A rule that could not be enforced mechanically is written as an instruction. When `intent-read` is left as an instruction, the implementer and the verifier receive "never read intent" as an instruction. When `design-write` is, the implementer receives "never write design" as an instruction.

## How carriers reach roles

- The reproducing lead chooses carriers from the means it has: an instruction file, part of one, a file it points to, a script a hook runs, a skill, and so on.
- Each role's rules go in a carrier that only that role receives.
- A carrier every AI reads by itself holds no role's rules. It holds only the role names, which AI plays which role ([roles.md](roles.md#which-role-an-ai-plays)), and, for a role no carrier can reach alone, where that role's rules are. When it would have nothing to point to, no such carrier is written.
- The lead's rules reach it at the start of every session, without the user doing anything: through a carrier only the lead receives, or because the carrier every AI reads points to them.
- The implementer and the verifier receive their rules when started: through a carrier only that role receives, or because the carrier every AI reads points to them. When that carrier reaches the role only if it is started in a certain way, such as a given kind of agent, the lead starts it that way. When neither works, the hand-off names where its rules are.
- Carrier files are in git, belong to no layer, and are listed in the setup record.
- A carrier holds rules only: no reasons, no history, no open questions. It holds nothing that points to plumbline's intent or design, no content of a layer kept out of git, and nothing these rules do not say. What a project adds goes in a project part.

## Reproduced parts and project parts

- When a carrier is a file the project also writes, the reproduction writes only what lies between a begin line and an end line. The two lines are chosen to suit the file type, and recorded in the setup record ([setup-record.md](setup-record.md#files)). The rest is the project part; reproducing again leaves it as it is.
- A project part holds the project's own working rules, such as its language and its code comment policy. A reproduced part never holds them.
- A file that cannot hold the two lines is not used; another file is chosen.
- The template has both parts too. Its reproduced part says what each of the seven sections holds, and has no level-2 heading.

## Connectors

- The role guard is connected, for every role, to the hook an AI passes through just before it reads or writes files. The connector gives the part the AI's role, the action, and the paths: for a search, the folders searched ([roles.md](roles.md#the-part)). On `block`, it stops the action and tells the AI in plain words what was blocked and why. On `error`, it tells the AI of an environment error and lets it go on ([conformance.md](conformance.md#connectors)).
- When the connector cannot tell an AI's role, `intent-read` and `design-write` are both left as instructions.
- Validate has no connector. The lead runs it with its runner and entry, as the setup record gives them.

## Checking connectors

- The lead starts the implementer and the verifier as the setup starts them, each with a hand-off that says this is a check of the role guard, and asks only for these:
  - The implementer and the verifier each: read a path under the intent location that does not exist, which must be blocked; and read a design document, which must pass.
  - The implementer: write a new file at a path under the design location that does not exist, which must be blocked. When it is not blocked and the file is created, the lead removes it, and `design-write` is left as an instruction.
- With intent at a file location, such as `docs/intent.md`, a path under it is such as `docs/intent.md/x` ([layers.md](layers.md#which-layer-a-path-belongs-to)).
- When a role cannot be started before a new session because of a carrier this reproduction wrote, the rule whose check needs that role is left as an instruction, and the final report tells the user to reproduce again in a new session. The connector stays in place and is listed in the setup record.

## Mechanical or instruction

`intent-read` and `design-write` are each enforced mechanically only when all of these hold; otherwise each is left as an instruction:

- There is a means to run the part just before the action.
- The part passed every conformance case.
- The connector check gave the expected results: for `intent-read`, the reads of both the implementer and the verifier; for `design-write`, the implementer's write.

The setup record's `enforcement` holds one entry for each of the two rules ([setup-record.md](setup-record.md#enforcement)).

## Reproducing again

- The steps are the same. Reproduced files and reproduced parts are written anew; project parts are kept.
- The previous setup record's choices, its carriers, boundary lines, runners and renderers, are kept unless the rules, the settings or the means at hand changed. A command the current rules do not allow is never kept.

## What always holds

- A reproduction commits nothing.
- A reproduction never changes project parts.
- A reproduction ends only when every conformance case passes.
- Every file a reproduction wrote, except the setup record and `.git/info/exclude`, is in the setup record, and every file in the setup record was written by a reproduction.
- Rule files and conformance cases are never copied into the project.
- Reproduced files and reproduced parts are never edited by hand. The setup changes only by changing the rules or the settings and reproducing again.
