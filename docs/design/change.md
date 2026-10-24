# A change

## 1. Responsibilities

- Says the order in which one change goes from diagnosis to commit.
- Says what the verifier checks.
- Defines where the work note is and what it holds.

Who reads and writes what, and the hand-offs and reports, are in Roles.

## 2. Public interface

### Diagnosis

| Diagnosis | Means | Layers fixed |
|---|---|---|
| impl | the design is right, and impl does not follow it | impl |
| design | something is missing or wrong in the design, and intent does not state the point | design, impl |
| intent | what intent states must change | intent, design, impl |

- A change is at the design level when it changes what the design states (public interfaces, invariants, decisions, verification criteria). It is at the intent level when it changes what intent states (goals and scope, decisions and their reasons, milestones).
- The lead diagnoses from what the user said and from intent and design. When telling needs impl, it asks the implementer.
- The layers touched are the diagnosis's layer and the layers below it. When a gap in an upper layer shows up during the work and that layer is fixed, it and the layers below it are touched too.

### The work note

- It is `.plumbline/work-note.md`. It is not in git.
- There is at most one per working tree. Two changes at the same time use two working trees.
- It holds: what was asked; the diagnosis; the commit checked out when the change started; the layers touched; the tasks and how far they are done; the questions waiting for the user's answer.
- It is written in plain words the user can read.

### What the verifier checks

"What changed" is the parts of the design changed since the commit the change started from (the documents and sections handed over), and the parts of impl that changed. The verifier reads git history only for the design and impl locations.

1. For every verification criterion in the changed design parts, impl has a test or a conformance case that shows it
2. impl keeps the invariants in the changed design parts
3. The public names in the changed design parts are in impl, and the changed parts of impl add no public name the design does not define
4. The changed design parts name no location of impl (file path, test name)
5. The diagnosis held
   - impl: the design is as it was at the start, and impl changed to follow it
   - design or intent: the design changed, and impl follows the changed design
   - every diagnosis: nothing outside the layers touched changed

## 3. Flow

1. **Start**: the lead decides the diagnosis, tells the user in plain words, and writes the work note.
2. **Fix from the top down**: at the intent level, intent is fixed first. When the design is fixed, the user reads and confirms the changed parts. Then, when impl must change, the implementer changes it.
3. **Gaps**: when the implementer reports a gap in the design, the lead asks the user, fixes the design by the answer, and hands the changed sections to the same implementer.
4. **Check**: when impl is done, the lead starts the verifier. The verifier checks only what changed and reports.
5. **Findings**: a finding that impl does not follow the design is fixed by the same implementer. A finding that something is missing or wrong in the design is asked about, as in 3. After a fix, the same verifier checks that finding's part again.
6. **Report and commit**: the lead tells the user in plain words what changed and what the check found. When the user wants, it is committed. Why it changed goes in the commit message.
7. **End**: the work note is removed.

- A milestone's work (writing its module documents and building its impl) is one change too. When it is done, the design README's current milestone is moved to the next milestone.
- A wording fix that changes no meaning (aligning a text with what is already decided, or with what another part of the same layer says) is made at once, and the user is told. When the user objects, it is handled as a gap.

## 4. Invariants and contracts

- A lower layer is fixed only after the upper layer is fixed and confirmed.
- While an answer from the user is awaited, the parts of lower layers that depend on that gap are not changed. Other parts go on.
- The verifier checks only what changed.
- There is at most one work note per working tree, and none once the change ends.

## 5. Decisions and reasons

- The diagnosis is not kept as a record; it is only in the work note. It is needed only while the change is worked on.
- The work note has one fixed place, so work can go on in a new session, and status draws on it.
- The verifier is handed the layers touched, since a gap can add layers during the work.
- Even when the diagnosis is intent, the verifier cannot read intent, so it checks only that design and impl changed together correctly.
- Findings are handled within the change. Only what changed is checked, so the findings belong to this change.
- After a fix, only that part is checked again. On a lighter model, checking again costs little.

## 6. Verification criteria

This needs judgment, so there are no conformance cases. The verifier checks that the rules state the flow and conditions above without omission.

## 7. Out of scope

None.
