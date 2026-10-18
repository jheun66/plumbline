# Reproduction

A reproduction builds a project's setup from these rules at one commit and the project settings. Reproducing again builds it the same way.

## Who and when

- The lead reproduces, in its conversation with the user ([roles.md](roles.md)).
- The first reproduction comes after the module map is confirmed ([authoring.md](authoring.md)).
- A project reproduces again when it moves to another rules commit, when its settings change, or when the user asks.

## Input

- The plumbline repository and a commit: the ones the user names, or else the ones in the setup record. A tag is resolved to its commit. On a first reproduction with no commit named, the agent asks the user, and may propose the newest tag.
- The settings file ([settings.md](settings.md)).
- The project as it is: the previous setup record, the project parts of carrier files, and the template's project part ([design-docs.md](design-docs.md)).

## Before writing anything

The agent stops and tells the user why when:

- the project is not a git repository;
- the settings file is not valid ([settings.md](settings.md));
- a layer location is `.plumbline/`, contains it, or lies inside it;
- the template's project part does not exist yet ([authoring.md](authoring.md));
- the previous setup record exists, and what the reproduction reads from it does not have the form [setup-record.md](setup-record.md#the-format) states: the record must be a JSON object, and its `rules`, `settings`, `files`, `carriers`, `parts`, `renderers` and `enforcement` must have their form, as far as the reproduction reads them. A record written under older rules, which lacks a key these rules have added since, is read as it is. A runner or a renderer command that these rules do not allow ([setup-record.md](setup-record.md#commands)) is read as it is too, whoever wrote it: that runner or renderer is not kept, and step 5 chooses it again;
- there is no setup record ([setup-record.md](setup-record.md#the-file)), but the git history of the commit checked out in the project holds one: it was removed by hand. The agent asks the user to restore it from git;
- a file that the previous setup record lists with `begin` and `end` exists, and its reproduced part cannot be found in it ([setup-record.md](setup-record.md#checksums)). The agent names the file, and the `begin` or `end` line that is missing, occurs more than once, or comes in the wrong order. A file that no longer exists is not this case: step 1 names it;
- the agent has no means that reaches the lead at the start of every session by itself: neither one that reaches only the lead, nor one that every agent reads by itself ([carriers.md](carriers.md)). This is an environment error;
- the rules at that commit cannot be read.

The git history of the commit checked out in the project is that commit and every commit before it. In a git repository with no commit yet, that history holds no setup record, and every file that exists counts as differing from the commit checked out in the project.

## Reading the rules

- The agent reads the rules from a copy of the plumbline repository at that commit, kept outside the project.
- In that copy, it reads only this folder, which holds the rules and their conformance cases, whatever else the copy holds.
- No file of the rules is copied into the project. What agents must do reaches them through the carriers ([carriers.md](carriers.md)).
- When the rules do not say what to produce, the agent does not fill the gap. It stops, says what the rules do not say, and proposes a change to the rules.

## Steps

1. Name every file in the previous setup record that no longer exists, or whose checksum ([setup-record.md](setup-record.md#checksums)) no longer matches: it was deleted or edited by hand. Write such files again, or remove them in step 8, only after the user agrees. If the user does not agree, stop before writing anything.
2. Choose the carriers and write them ([carriers.md](carriers.md)): whole files, and reproduced parts with the project parts kept.
3. Write the template's reproduced part ([carriers.md](carriers.md)), keeping its project part.
4. Add to `.git/info/exclude` every path of each layer in `not_in_git` that is not there yet. Remove the paths of a layer that the previous record kept out of git and the settings no longer do.
5. Write the mechanical parts and their connectors ([carriers.md](carriers.md#connectors)), and choose a runner for each. A runner must be present wherever its part runs: the developer's machine, and CI for a part that runs there. A runner is present only when it can be recorded as [setup-record.md](setup-record.md#commands) allows: by a name found on the PATH. When there is none, report an environment error that names what is missing, and stop.
   - For CI, use the CI the project already uses. When the agent finds none, it asks the user which one. When the project uses none, there is no CI step.
   - For each figure name in the template ([design-docs.md](design-docs.md#the-template)), choose a renderer present on the developer's machine and record it ([setup-record.md](setup-record.md#renderers)). A renderer is present only when it can be recorded as [setup-record.md](setup-record.md#commands) allows. When none is present, record none for that name. When one is installed but can be reached only by an absolute path, record none for that name, and tell the user in step 10 what to put on the PATH. A renderer need not be present in CI. Where it is not, `validate` skips that kind of figure.
6. Run every conformance case ([conformance.md](conformance.md)). When one fails, correct the part and run every case again.
7. Check each connector as [carriers.md](carriers.md#connectors) states: a connector to an agent by acting through it, once with an action that must be blocked and once with an action that must pass; the connector at the end of a turn by running it as the hook would run it; the CI connector by running its command locally on a copy of the project. When a connector does not give the expected results and cannot be corrected, or cannot be checked in this session ([carriers.md](carriers.md#a-connector-that-cannot-be-checked-in-this-session)), its rule is enforced by instruction only.
8. Remove the files, and the reproduced parts, that the previous record listed and this reproduction no longer writes.
9. Write the setup record ([setup-record.md](setup-record.md)), replacing the old one.
10. Tell the user which rules are enforced mechanically and which by instruction only, and which files were written, changed or removed. Tell the user to commit the setup record and every file that the previous or the new setup record lists and that differs from the commit checked out in the project, and name each of them. When a connector could not be checked in this session, tell the user to reproduce again in a new session. For each renderer step 5 did not record because only an absolute path reaches it, tell the user what to put on the PATH. The reproduction commits nothing.

A setup has the four mechanical parts these rules define: `status`, `gap-guard`, `role-guard` and `validate` ([conformance.md](conformance.md#the-parts-of-a-setup)). `status`, and `validate` before a change closes, have no connector ([carriers.md](carriers.md#connectors)).

## Mechanical or instruction

The rules that may be enforced mechanically:

| Rule | Stated in | Part that enforces it | Connector |
|---|---|---|---|
| `gap guard` | [changes.md](changes.md#gap-items) | `gap-guard` ([guards.md](guards.md#the-gap-guard)) | before an agent writes files |
| `role table` | [roles.md](roles.md#the-role-table) | `role-guard` ([guards.md](guards.md#the-role-guard)) | before an agent reads or writes files |
| `validate at the end of a turn` | [carriers.md](carriers.md#connectors) | `validate`, in `report` mode ([validate.md](validate.md)) | when the lead ends a turn |
| `validate in CI` | [carriers.md](carriers.md#connectors) | `validate`, in `gate` mode ([validate.md](validate.md)) | a step of the project's CI |

Such a rule is `mechanical` when all of these hold:

- the agent has a means to run the rule's part at the moment the rule needs it: before an action, at the end of a turn, in CI;
- the part passed every case;
- the check of its connector gave the expected results ([carriers.md](carriers.md#connectors)).

Otherwise it is `instruction`, and the carriers state it as an instruction. When the project uses no CI, `validate in CI` is `instruction`.

Every rule in the table above has one entry in the setup record's `enforcement` ([setup-record.md](setup-record.md)). Every other rule reaches agents as an instruction and has none.

## Reproducing again

- The steps are the same. Reproduced files and reproduced parts are replaced; project parts are kept.
- The agent keeps the previous record's choices (carriers, begin and end lines, runners, renderers, the CI) unless the rules, the settings or the means it has require otherwise. A runner or a renderer command that these rules do not allow ([setup-record.md](setup-record.md#commands)) is never kept.

## What always holds

- What a reproduction writes comes only from these rules at one commit and the settings. It keeps every project part, and keeps its earlier choices where the rules and the settings allow.
- The reproducing agent reads nothing of the plumbline repository but this folder, and copies no file of the rules into the project.
- A gap in the rules is never filled by the reproducing agent.
- Every file a reproduction writes lies outside every layer location.
- No file a reproduction writes, the setup record included, holds a path particular to the developer's machine, such as one under the developer's home folder.
- A reproduced file or reproduced part is never edited by hand. The setup changes only by changing the rules or the settings and reproducing again.
- The setup record is written last, and only after every case has passed.
- A reproduced file deleted or edited by hand is never written again or removed without the user knowing.
- A reproduced part whose `begin` or `end` line cannot be found is never written over.
- A project whose checked-out commit has a setup record in its git history is never reproduced as if for the first time.
- A reproduction commits nothing. The user commits the setup record and every file that the previous or the new setup record lists and that differs from the checked-out commit.
