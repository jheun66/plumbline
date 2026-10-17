# Roles

## The role table

This table is the rule named `role table`.

| Role | Does | Reads | Writes |
|---|---|---|---|
| `lead` | talks with the user; writes intent and design with the user; opens, closes and archives changes; diagnoses; records gap items and the user's answers; edits the settings and reproduces the setup | intent, design, change records, setup files | intent, design, change records, the current change, settings, setup files, the lines these rules call for in `.git/info/exclude` |
| `implementer` | builds the design sections it is given into impl; answers questions about impl | design, impl, the rule carriers it receives | impl |

- Setup files are what a reproduction writes and keeps: rule carriers, document templates, guards, checks, the setup record. They are not a layer.
- No role reads or writes outside its row.
- The lead never reads impl. The implementer never reads intent, and never writes intent or design.
- Only the lead writes change records and the current change ([changes.md](changes.md)).
- The role table may be enforced mechanically. The setup record says whether it is ([setup-record.md](setup-record.md)). When it is not, the rule carriers state it as an instruction ([carriers.md](carriers.md)).

### Files in no layer

A project file is a file kept in the project's repository. Files that tools create while they run, such as build outputs and caches, are not project files.

A project file that lies in no layer location ([settings.md](settings.md#the-format)) is written by no role, unless it is one of these:

- a file a reproduction writes, whether it keeps it or removes it again ([reproduction.md](reproduction.md));
- the settings file ([settings.md](settings.md#the-file));
- a change record, or the current change ([changes.md](changes.md));
- the lines these rules call for in `.git/info/exclude` ([settings.md](settings.md#a-layer-kept-out-of-git), [changes.md](changes.md#the-current-change)).

When the work needs any other project file in no layer:

1. The lead proposes to the user to add its path to the paths of a layer in the settings, usually impl. This is not a gap item. The `change.md` of the change the work belongs to lists it among its tasks ([changes.md](changes.md#changemd)).
2. Once the user agrees, the lead edits the settings and reproduces the setup ([reproduction.md](reproduction.md)).
3. The role that writes that layer writes the file.

An implementer whose work needs such a file stops that work and reports it to the lead. After the reproduction, a new implementer continues with the same design sections ([Hand-off](#hand-off)).

Examples:

- A version control ignore file at the project root, such as `.gitignore`, lies in no layer. No role writes it until its path is added to impl's paths and the setup is reproduced. Then an implementer writes it.
- Build outputs and caches that a build or a test run creates are not project files. This rule does not cover them.
- A file that a reproduction writes to check a connector and then removes ([carriers.md](carriers.md#checking-the-gap-guards-connector)) is one of the files above.

## Which role an agent plays

Every agent plays exactly one role:

- An agent started by a hand-off that names it an implementer is an implementer.
- Every other agent is the lead.

## Fresh agents

- The implementer starts without the lead's conversation.
- One implementer serves one hand-off. Work after a design change always goes to a new implementer.

## Hand-off

- The lead hands work to an implementer by naming its role, `implementer`, and design sections: a design document and the sections in it.
- The hand-off names nothing else, except a question it carries (below) and the carrier that holds the implementer's rules when [carriers.md](carriers.md) requires it.
- The lead starts the implementer with the hand-off. When the lead cannot start an agent itself, or cannot start it in the way the implementer's carrier needs ([carriers.md](carriers.md)), it gives the hand-off to the user, who starts the implementer with it, and tells the user how to start it. That instruction is for the user and is not part of the hand-off.
- A hand-off never carries intent content.
- A question about impl from the user goes from the lead to an implementer in the same way: the hand-off names the design sections the question is about, and the question. The answer comes back to the lead.

## Changes

- The lead opens, closes and archives changes, and keeps the current change ([changes.md](changes.md)).
- The lead diagnoses which layer is wrong from what the user said and from intent and design ([changes.md](changes.md#diagnosis)). When telling requires impl, the lead asks an implementer, as for a question about impl ([Hand-off](#hand-off)). The lead never reads impl itself.
- The lead records each gap as a gap item, and records the user's answer with its date ([changes.md](changes.md#gap-items)).

## A gap found by the implementer

1. The implementer stops work on that point and reports the gap to the lead, in terms of the design: which section, and what it does not say or says wrongly. It leaves that point unbuilt and does not choose a way to build it. Work on other points goes on.
2. The lead records it as a proposed gap item in the current change ([changes.md](changes.md#gap-items)) and proposes the change to the user. When it is a wording fix ([changes.md](changes.md#wording-fixes)), the lead instead makes the fix at once, records it in the change and tells the user.
3. The lead records the user's answer. After the user confirms, the lead changes the design, or intent first when the gap is at intent's level ([layers.md](layers.md)).
4. A new implementer continues the work.

- A gap goes from the implementer to the lead, and from the lead to the user. The implementer never settles it, and leaves its point unbuilt.
- Every gap is recorded as a gap item before it is proposed to the user.
