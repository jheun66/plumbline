# Roles

## The role table

This table is the rule named `role table`.

| Role | Does | Reads | Writes |
|---|---|---|---|
| `lead` | talks with the user; writes intent and design with the user; opens, closes and archives changes; diagnoses; records gap items and the user's answers; edits the settings and reproduces the setup | intent, design, change records, setup files | intent, design, change records, the current change, settings, setup files |
| `implementer` | builds the design sections it is given into impl; answers questions about impl | design, impl, the rule carriers it receives | impl |

- Setup files are what a reproduction writes and keeps: rule carriers, document templates, guards, checks, the setup record. They are not a layer.
- No role reads or writes outside its row.
- The lead never reads impl. The implementer never reads intent, and never writes intent or design.
- Only the lead writes change records and the current change ([changes.md](changes.md)).
- The role table may be enforced mechanically. The setup record says whether it is ([setup-record.md](setup-record.md)). When it is not, the rule carriers state it as an instruction ([carriers.md](carriers.md)).

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

1. The implementer stops work on that point and reports the gap to the lead, in terms of the design: which section, and what it does not say or says wrongly.
2. The lead records it as a proposed gap item in the current change ([changes.md](changes.md#gap-items)) and proposes the change to the user.
3. The lead records the user's answer. After the user confirms, the lead changes the design, or intent first when the gap is at intent's level ([layers.md](layers.md)).
4. A new implementer continues the work.

- A gap goes from the implementer to the lead, and from the lead to the user. The implementer never settles it.
- Every gap is recorded as a gap item before it is proposed to the user.
