# Reproduction

## 1. Responsibilities

- Says the order in which the lead reads plumbline's rules and builds the setup in a project.
- Says what each role must receive, and through which carriers.
- Says how to tell whether a rule is enforced mechanically or left as an instruction.
- Says how to reproduce again.

The form of the setup record is in Setup record; how cases run is in Conformance cases.

## 2. Public interface

### Who and when

- The lead reproduces, in its conversation with the user.
- The first reproduction comes after the module map is confirmed and the settings are complete.
- A project reproduces again when it moves to another rules commit, when its settings change, or when the user asks.

### Input

- The plumbline repository and a commit: the ones the user names, or else the ones in the setup record. A tag is resolved to its commit. On a first reproduction with no commit given, the lead asks the user; it may propose the newest tag.
- The repository address must be reachable from other machines (Setup record). When given a copy on the machine, the lead reads the rules from it and asks the user for the address of the original repository. Without an address, it stops before writing anything.
- The settings file, the previous setup record, the project parts of carrier files, and the template's project part.

### When it stops before writing anything

When any of these holds, it writes nothing, stops, and tells the user why in plain words.

- The project is not a git repository.
- The settings file is missing or does not have its form (Layers and settings).
- A layer location is `.plumbline`, contains it, or lies inside it.
- The template's project part does not exist yet (Design documents).
- The previous setup record exists, and what the reproduction reads from it does not have its form. But a record written under older rules that lacks a key newer rules added, a repository that is not an address, and a command the current rules do not allow, are read as they are. Such a command is not kept; a new one is chosen.
- There is no setup record, but the git history has one: it was removed by hand. The lead asks the user to restore it from git.
- A file the previous setup record lists with a reproduced part exists, but the part cannot be found in it. The lead names the file, and the boundary line that is missing, appears twice, or is out of order.
- There is no carrier that reaches the lead by itself at the start of every session (below, "How carriers reach roles"). This is an environment error.
- The rules at that commit cannot be read.

### Reading the rules

- The lead reads only plumbline's rules and conformance cases at that commit, from a copy kept outside the project. It never reads plumbline's design, even when the copy holds it.
- No rule file is copied into the project. What AIs must do reaches them through carriers.
- When the rules do not say what to produce, the lead does not fill the gap. It stops, says what the rules do not say, and proposes a change to the rules.

### Steps

1. Tell the user which files in the previous setup record are missing or have a different checksum: they were removed or edited by hand. Only with the user's agreement are they written again, or removed in step 8. Without agreement, stop before writing anything.
2. Choose the rule carriers and write them. Keep project parts as they are.
3. Write the template's reproduced part. Keep its project part as it is.
4. Add to `.git/info/exclude`, when missing, the locations of the layers kept out of git and the work note's place (`/.plumbline/work-note.md`). Remove the lines of a layer that was kept out of git before and no longer is.
5. Write the parts (the role guard, validate) and their connectors, and choose a runner for each part. A runner counts as present only when it can be recorded by a name found on the PATH. When none is present, report an environment error that names what is missing, and stop. For each figure kind in the template, choose a renderer present on this machine; when none is, record none. A renderer reachable only through an absolute path is recorded as none too, and the final report tells the user what to put on the PATH.
6. Run every conformance case (Conformance cases). When one fails, fix the part and run every case again.
7. Act through the connectors (below, "Checking connectors").
8. Remove the files and reproduced parts the previous setup record listed and this reproduction no longer writes.
9. Write the setup record anew, whole (Setup record).
10. Tell the user in plain words: which rules are enforced mechanically and which are left as instructions; which files were written, changed and removed; what to commit (the setup record, and the files listed in the previous or the new setup record that changed). The reproduction commits nothing. When a carrier was written or changed and it is read only when a session starts, tell the user it reaches that role only from a new session on.

### What each role receives

| Role | Receives |
|---|---|
| lead | the three layers, their locations, and the layers kept out of git (Layers and settings); the read direction, fixing from the top down, and asking about gaps; the whole role table, which role an AI plays, how to start the implementer and the verifier, and the hand-offs (Roles); how to write design documents (Design documents); Writing intent; A change; Status; how to run validate and report its result; what to do when the role guard blocks or reports an environment error; how to reproduce; that the content of a layer kept out of git is never copied into a layer in git; that reproduced files are never edited by hand, and that the setup changes only by changing the rules or the settings and reproducing again |
| implementer | its row of the role table; the layer locations, and the intent location as a place it never reads; how to read a design document (what the seven sections mean; the design never names locations of impl); that it builds only the design sections it is handed; that on a gap it leaves that point unbuilt and reports it in terms of the design; that when a file in no layer must be written, it stops that work and reports; that when blocked, it stops that work and reports, and never does it another way; its report |
| verifier | its row of the role table; the layer locations, and the intent location as a place it never reads; how to read a design document; its hand-off; the five checks and how to judge the diagnosis (A change); its report; that when blocked, it never does it another way |

- Every location is written as the settings give it.
- A rule that could not be enforced mechanically is written as an instruction. When `intent-read` is an instruction, the implementer and the verifier receive "never read intent" as an instruction. When `design-write` is an instruction, the implementer receives "never write design" as an instruction.

### How carriers reach roles

- The reproducing lead chooses carriers from the means it has: an instruction file, part of one, a file it points to, a script a hook runs, a skill, and so on.
- Each role's rules go in a carrier only that role receives.
- A carrier every AI reads by itself holds no role's rules. It holds only the role names, which AI plays which role, and, for a role no carrier can reach alone, where that role's rules are. When it has nothing to point to, no such carrier is written.
- The lead's rules reach it at the start of every session, without the user doing anything: through a carrier only the lead receives, or because the carrier every AI reads points to them.
- The implementer and the verifier receive their rules when started: through a carrier only that role receives, or because the carrier every AI reads points to them. When that carrier reaches the role only if it is started in a certain way (for example, as a given kind of agent), the lead starts it that way. When neither works, the hand-off names where its rules are.
- Carrier files are in git, belong to no layer, and are listed in the setup record.
- What a carrier holds: rules only. No reasons, history or open questions. Nothing that points to plumbline's intent or design. No content of a layer kept out of git. Nothing the rules do not say. What a project adds goes in a project part.

### Reproduced parts and project parts

- When a carrier is a file the project also writes, the reproduction writes only what lies between a begin line and an end line. The two lines are chosen to suit the file type and recorded in the setup record. The rest is the project part, and reproducing again leaves it as it is.
- A project part holds the project's own working rules (language, code comment policy, and so on). A reproduced part never holds them.
- A file that cannot hold the two lines is not used; another file is chosen.
- The template has both parts too. Its reproduced part says what each of the seven sections holds, and has no level-2 heading.

### Connectors

- The role guard is connected, for every role, to the hook an AI passes through just before it reads or writes files. The connector gives the part the AI's role, the action, and the paths (for a search, the folders searched). When the connector cannot tell an AI's role, both rules are left as instructions.
- Validate has no connector. The lead runs it with its runner and entry.

### Checking connectors

- The lead starts the implementer and the verifier as the setup starts them, with a hand-off that says this is a check of the role guard, and asks only for these:
  - The implementer and the verifier each: read a path that does not exist under the intent location → must be blocked. Read a design document → must pass.
  - The implementer: write a new file at a path that does not exist under the design location → must be blocked. When it is not blocked and the file is created, the lead removes it, and that rule is left as an instruction.
- A path that does not exist reveals nothing, so no role has a reason to refuse.
- When a role cannot be started before a new session because of a carrier this reproduction wrote, the rule whose check needs it is left as an instruction, and the final report tells the user to reproduce again in a new session. The connector stays in place and is listed in the setup record.

### Mechanical or instruction

`intent-read` and `design-write` are enforced mechanically only when all of these hold; otherwise they are left as instructions.

- There is a means to run the part just before the action.
- The part passed every conformance case.
- The connector check gave the expected results.

### Reproducing again

- The steps are the same. Reproduced files and reproduced parts are written anew; project parts are kept.
- The previous setup record's choices (carriers, boundary lines, runners, renderers) are kept unless the rules, the settings or the means at hand changed. A command the current rules do not allow is never kept.

## 3. Flow

1. The user asks for a reproduction (with a commit or a tag, if any).
2. The lead reads the settings, the previous setup record and the project parts.
3. When a stop condition holds, it stops and tells the user.
4. It reads the rules at that commit from the copy outside the project. When the rules have a gap, it stops and proposes a change to the rules.
5. It goes through steps 1 to 10 above.

## 4. Invariants and contracts

- A reproduction commits nothing.
- A reproduction never changes project parts.
- A reproduction ends only when every conformance case passes.
- Every file a reproduction wrote is in the setup record (except the setup record and `.git/info/exclude`), and every file in the setup record was written by a reproduction.
- Rule files and conformance cases are never copied into the project.

## 5. Decisions and reasons

- The lead reproduces. There are things to ask the user, such as what to do with files edited by hand. To another project's lead, plumbline's rules are not that project's impl, so it may read them.
- The copy of the rules is kept outside the project, so rules never mix with project files.
- Files edited by hand are written again only with the user's agreement. The user may have edited them on purpose.
- Connectors are checked by acting through them. Cases test only the parts, and connectors differ between AI tools, so cases cannot test them.
- The checks use paths that do not exist. Even when not blocked, nothing is revealed.
- A check that needs a role reachable only from a new session waits for the next reproduction, so that no rule is recorded as mechanical without being checked.

## 6. Verification criteria

This needs judgment, so there are no cases. Reproducing in another project shows:

- In a project after reproduction, validate gives no `record`, `checksum`, `part-not-found` or `template` line.
- Reproducing again in a new session with the same rules and settings gives the same list of files in the setup record.
- Reproducing again leaves project parts as they are.
- The locations of the layers kept out of git and the work note's place are in `.git/info/exclude`.
- The final report names the rules enforced mechanically, those left as instructions, and the files to commit.

## 7. Out of scope

None.
