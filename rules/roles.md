# Roles

## The role table

This section is the rule named `role table`.

| Role | Does |
|---|---|
| `lead` | talks with the user; writes intent and design with the user; opens, closes and archives changes; diagnoses; records gap items and the user's answers; edits the settings and reproduces the setup |
| `implementer` | builds the design sections it is given into impl; answers questions about impl |
| `verifier` | checks impl against the design sections it is given, for one change, and writes the result into that change ([verify.md](verify.md)) |

What each role may read (R) and write (W):

| Path | `lead` | `implementer` | `verifier` |
|---|---|---|---|
| intent | R W | — | — |
| design | R W | R | R |
| impl | — | R W | R |
| the verify result of a change ([changes.md](changes.md#the-verify-result)) | R | — | R W: only that of the change it was given |
| other change records | R W | — | — |
| the current change | R W | — | — |
| the settings file | R W | R | R |
| rule carriers meant for that role or for every agent | R W | R | R |
| other setup files | R W | — | — |
| `.git/info/exclude` | R W: the lines these rules call for | — | — |
| other project files in no layer | R | R | R |
| files that are not project files | R W | R W | R W |

- No role reads or writes outside its row. Every path an action touches falls in exactly one row of this table.
- A layer's paths are the ones the settings give ([settings.md](settings.md)). A path lies in a layer when it equals one of them or lies under one.
- Setup files are what a reproduction writes and keeps: rule carriers, document templates, guards, checks, their connectors, and the setup record. They are not a layer. The setup record says which roles each rule carrier is meant for ([setup-record.md](setup-record.md#carriers)).
- The lead also writes the files a reproduction writes for its checks and removes again ([carriers.md](carriers.md#connectors)). They are setup work, not project files.
- A project file is a file under the project root, outside `.git/`, that the project's own ignore rules do not ignore: its ignore files and `.git/info/exclude`. A path outside the project root, a path git ignores, and a path under `.git/` other than `.git/info/exclude` are not project files. A user's global ignore file, or any other ignore rule that is not the project's own, does not count.
- Files that tools create while they run, such as build outputs, are the tools' and not a role's writes. A role never writes them by an action of its own.
- The lead never reads impl. The implementer never reads intent, and never writes intent or design. The verifier never reads intent or change records, and writes nothing but its result.
- Only the lead writes change records and the current change, except the verify result, which only the verifier writes ([changes.md](changes.md)).
- The role table may be enforced mechanically, by the role guard ([guards.md](guards.md#the-role-guard)). The setup record says whether it is ([setup-record.md](setup-record.md)). When it is not, the rule carriers state each role's row as an instruction ([carriers.md](carriers.md)).

### Files in no layer

A project file that lies in no layer is written by no role, unless the table above lets that role write it.

When the work needs any other project file in no layer:

1. The lead proposes to the user to add its path to the paths of a layer in the settings, usually impl. This is not a gap item. The `change.md` of the change the work belongs to lists it among its tasks ([changes.md](changes.md#changemd)).
2. Once the user agrees, the lead edits the settings and reproduces the setup ([reproduction.md](reproduction.md)).
3. The role that writes that layer writes the file.

An implementer whose work needs such a file stops that work and reports it to the lead. After the reproduction, a new implementer continues with the same design sections ([Hand-off](#hand-off)).

Examples:

- A version control ignore file at the project root, such as `.gitignore`, lies in no layer. No role writes it until its path is added to impl's paths and the setup is reproduced. Then an implementer writes it.
- Build outputs that a build or a test run creates, in a folder git ignores, are not project files. The build writes them, not a role.
- A temporary file that a reproduction writes to check a connector and then removes ([carriers.md](carriers.md#connectors)) is written by the lead.

## Which role an agent plays

Every agent plays exactly one role:

- An agent started by a hand-off that names it an implementer is an implementer.
- An agent started by a hand-off that names it a verifier is a verifier.
- Every other agent is the lead.

## Fresh agents

- The implementer and the verifier start without the lead's conversation.
- One implementer serves one hand-off. Work after a design change always goes to a new implementer.
- One verifier serves one check of one change.

## Hand-off

To an implementer:

- The lead hands work to an implementer by naming its role, `implementer`, and design sections: a design document and the sections in it.
- The hand-off names nothing else, except a question it carries (below) and the carrier that holds the implementer's rules when [carriers.md](carriers.md) requires it.
- The lead starts the implementer with the hand-off. When the lead cannot start an agent itself, or cannot start it in the way the implementer's carrier needs ([carriers.md](carriers.md)), it gives the hand-off to the user, who starts the implementer with it, and tells the user how to start it. That instruction is for the user and is not part of the hand-off.
- A hand-off never carries intent content.
- A question about impl from the user goes from the lead to an implementer in the same way: the hand-off names the design sections the question is about, and the question. The answer comes back to the lead.

To a verifier:

- The lead hands the check of a closed change to a verifier by naming:
  - its role, `verifier`;
  - the change, by its name;
  - the change's diagnosis;
  - the layers the change touched ([changes.md](changes.md#diagnosis));
  - the commit the change's work started from: the commit that `change.md` records as checked out when the change was opened ([changes.md](changes.md#changemd));
  - the design sections the change touched: design documents and the sections in them.
- The hand-off names nothing else, except the carrier that holds the verifier's rules when [carriers.md](carriers.md) requires it.
- The lead starts the verifier with the hand-off, or gives it to the user to start, as for an implementer.
- A hand-off to a verifier never carries intent content.
- The verifier writes its result into that change and tells the lead it is done.

For a check of the role guard:

- During a reproduction, a hand-off may ask an implementer or a verifier for a check of the role guard instead of design sections ([carriers.md](carriers.md#checking-the-role-guards-connector)).
- Such a hand-off names the role, says that it is a check of the role guard, and asks only for the reads that check lists. It names nothing else, except the carrier that holds the role's rules when [carriers.md](carriers.md) requires it.
- The agent is started with it as for any other hand-off to its role. It never carries intent content.

## Changes

- The lead opens, closes and archives changes, and keeps the current change ([changes.md](changes.md)).
- The lead diagnoses which layer is wrong from what the user said and from intent and design ([changes.md](changes.md#diagnosis)). When telling requires impl, the lead asks an implementer, as for a question about impl ([Hand-off](#hand-off)). The lead never reads impl itself.
- The lead records each gap as a gap item, and records the user's answer with its date ([changes.md](changes.md#gap-items)).
- Once a change is closed, the lead hands its check to a fresh verifier ([Hand-off](#hand-off)), reads the verify result, tells the user its findings, and takes up each finding before archiving the change ([changes.md](changes.md#taking-up-findings)).

## A gap found by the implementer

1. The implementer stops work on that point and reports the gap to the lead, in terms of the design: which section, and what it does not say or says wrongly. It leaves that point unbuilt and does not choose a way to build it. Work on other points goes on.
2. The lead records it as a proposed gap item in the current change ([changes.md](changes.md#gap-items)) and proposes the change to the user. When it is a wording fix ([changes.md](changes.md#wording-fixes)), the lead instead makes the fix at once, records it in the change and tells the user.
3. The lead records the user's answer. After the user confirms, the lead changes the design, or intent first when the gap is at intent's level ([layers.md](layers.md)).
4. A new implementer continues the work.

- A gap goes from the implementer to the lead, and from the lead to the user. The implementer never settles it, and leaves its point unbuilt.
- Every gap is recorded as a gap item before it is proposed to the user.

## A closed change checked by a verifier

1. The lead hands the check to a fresh verifier ([Hand-off](#hand-off)).
2. The verifier checks the change as [verify.md](verify.md) states, writes `verify.md` into the change's folder, and tells the lead it is done.
3. The lead reads the verify result and tells the user its findings.
4. For each finding, the user decides to take it up or to decline it. The lead records the follow-up change that takes it up, or the user's dated decision not to act on it ([changes.md](changes.md#taking-up-findings)).
5. The lead archives the change.
