# A change

A change is one piece of work, from diagnosis to commit. Who reads and writes what, and the hand-offs and reports, are in [roles.md](roles.md).

## Diagnosis

| Diagnosis | Means | Layers fixed |
|---|---|---|
| impl | the design is right, and impl does not follow it | impl |
| design | something is missing or wrong in the design, and intent does not state the point | design, impl |
| intent | what intent states must change | intent, design, impl |

- A change is at the design level when it changes what the design states: public interfaces, invariants, decisions, verification criteria. It is at the intent level when it changes what intent states: goals and scope, decisions and their reasons, milestones.
- The lead diagnoses from what the user said, and from intent and design. When telling needs impl, it asks the implementer, with the question in the hand-off ([roles.md](roles.md#hand-offs)). It never reads impl.
- The layers touched are the diagnosis's layer and the layers below it. When a gap in a higher layer shows up during the work and that layer is fixed, it and the layers below it are touched too.

## The work note

- It is `.plumbline/work-note.md`. It is not in git: its place is in `.git/info/exclude` ([reproduction.md](reproduction.md#steps)).
- There is at most one per working tree. Two changes at the same time use two working trees.
- It holds: what was asked; the diagnosis; the commit checked out when the change started; the layers touched; the tasks, and how far each is done; the questions waiting for the user's answer.
- It is written in plain words the user can read.
- The diagnosis is written only in the work note.

## Steps

1. **Start**: the lead decides the diagnosis, tells the user in plain words, and writes the work note.
2. **Fix from the top down**: at the intent level, intent is fixed first. When the design is fixed, the user reads and confirms the changed parts. Then, when impl must change, the implementer changes it.
3. **Gaps**: when the implementer reports a gap in the design, the lead asks the user, fixes the design by the answer, and hands the changed sections to the same implementer.
4. **Check**: when impl is done, the lead starts the verifier ([roles.md](roles.md#starting-the-implementer-and-the-verifier)). The verifier checks only what changed, and reports.
5. **Findings**: a finding that impl does not follow the design is fixed by the same implementer; the lead hands it the finding ([roles.md](roles.md#hand-offs)). A finding that something is missing or wrong in the design is asked about, as in step 3. After a fix, the same verifier checks that finding's part again; the lead hands it the numbers of the findings to check again. Findings are handled within the change.
6. **Report and commit**: the lead tells the user in plain words what changed and what the check found. When the user wants, it is committed. Why it changed goes in the commit message.
7. **End**: the work note is removed.

- A milestone's work, writing its module documents and building its impl, is one change too. When it is done, the design README's current milestone is moved to the next milestone ([design-docs.md](design-docs.md#the-module-map)).
- A wording fix that changes no meaning, aligning a text with what is already decided or with what another part of the same layer says, is made at once, and the user is told. When the user objects, it is handled as a gap.

## What the verifier checks

What changed is the parts of the design changed since the commit the change started from, which are the documents and sections handed over, and the parts of impl that changed.

1. For every verification criterion in the changed design parts, impl has a test or a conformance case that shows it.
2. impl keeps the invariants in the changed design parts.
3. The public names in the changed design parts are in impl, and the changed parts of impl add no public name the design does not define.
4. The changed design parts name no location of impl, such as a file path or a test name.
5. The diagnosis held:
   - impl: the design is as it was at the start, and impl changed to follow it;
   - design or intent: the design changed, and impl follows the changed design;
   - every diagnosis: nothing outside the layers touched changed.

- The verifier compares design and impl with the commit the change started from. Of git's history, it reads only that of the design and impl locations.
- It never reads intent, whatever the diagnosis.
- Each finding names the design document and section, and how impl falls short of it ([roles.md](roles.md#reports)).

## What always holds

- A lower layer is fixed only after the upper layer is fixed and confirmed.
- While an answer from the user is awaited, the parts of lower layers that depend on that gap are not changed. Other parts go on.
- The verifier checks only what changed.
- There is at most one work note per working tree, and none once the change ends.
