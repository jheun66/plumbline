# Roles

## The role table

This table is the rule named `role table`.

| Role | Does | Reads | Writes |
|---|---|---|---|
| `lead` | talks with the user; writes intent and design with the user; edits the settings and reproduces the setup | intent, design, setup files | intent, design, settings, setup files |
| `implementer` | builds the design sections it is given into impl; answers questions about impl | design, impl, the rule carriers it receives | impl |

- Setup files are what a reproduction writes and keeps: rule carriers, document templates, guards, checks, the setup record. They are not a layer.
- No role reads or writes outside its row.
- The lead never reads impl. The implementer never reads intent, and never writes intent or design.
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
- The hand-off names nothing else, except the carrier that holds the implementer's rules when [carriers.md](carriers.md) requires it.
- The lead starts the implementer with the hand-off. When the lead cannot start an agent itself, or cannot start it in the way the implementer's carrier needs ([carriers.md](carriers.md)), it gives the hand-off to the user, who starts the implementer with it, and tells the user how to start it. That instruction is for the user and is not part of the hand-off.
- A hand-off never carries intent content.
- A question about impl from the user goes from the lead to an implementer in the same way. The answer comes back to the lead.

## A gap found by the implementer

1. The implementer stops work on that point and reports the gap to the lead, in terms of the design: which section, and what it does not say or says wrongly.
2. The lead proposes the change to the user.
3. After the user confirms, the lead changes the design, or intent first when the gap is at intent's level ([layers.md](layers.md)).
4. A new implementer continues the work.

A gap goes from the implementer to the lead, and from the lead to the user. The implementer never settles it.
