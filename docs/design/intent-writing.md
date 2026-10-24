# Writing intent

## 1. Responsibilities

- Says how the lead writes and confirms intent with the user.
- Does not fix the form of intent. Each project decides it.

Changing a confirmed intent follows A change.

## 2. Public interface

### Marks

Every item of a draft carries one of three marks.

| Mark | Means |
|---|---|
| decided | the user said or chose it |
| proposed | the lead's thought, which the user has not decided yet |
| open | still open |

- Near the top of the draft, the three marks are named in the project's own words.
- The decided mark may be left out, when the draft says that an item with no mark is decided.

### The confirmed mark

When intent is confirmed, its top says, in the project's own words, that the user confirmed it, and on which date.

## 3. Flow

1. The lead talks with the user. The user may answer first in their own words, or the lead may listen and draft; the order is not fixed.
2. The draft is written at the intent location. The location is decided first (Layers and settings).
3. Of what intent must say (goals and scope, milestones, decisions and their reasons), what the user has not said is left open and asked.
4. Open items are resolved one at a time. When the user answers, the item is decided.
5. What follows directly from earlier decisions is written as decided without asking, and the user is told. When the user objects, it becomes open again.
6. When the user asks for the lead's thought, the lead gives it with its reasons and with what it is less sure of, and the draft holds it as proposed. When the user accepts or changes it, it is decided.
7. When nothing proposed or open is left, the user reads the whole. When the user understands it and says it is right, it is confirmed.

## 4. Invariants and contracts

- The lead never fills what the user has not said with a default of its own.
- What the lead asks the user is in plain words, with no name left unexplained. When the user wants, it shows a concrete example.
- What each project decides, such as its language or code comment policy, is not asked about separately. When the user states it, it goes into intent.
- Intent is confirmed only when nothing proposed or open is left and the user has read and understood the whole.
- Marks are used only in drafts. They are not carried into documents of other layers.

## 5. Decisions and reasons

- The order of the conversation is not fixed. It only has to go both ways.
- Defaults are not filled in; the user is asked. Filling them in piles up decisions the user confirmed without understanding.
- What follows directly is not asked. The same thing is not asked twice, and since the user is told, the user can correct it.
- The decided mark may be left out. When almost every item is decided, the marks get in the way of reading.

## 6. Verification criteria

This needs judgment, so there are no conformance cases. The verifier checks that the rules state the flow and conditions above without omission.

## 7. Out of scope

None.
