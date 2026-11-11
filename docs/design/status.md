# Status

## 1. Responsibilities

- Says how the lead answers when the user asks where things stand.
- Says when things to fix (reproducing again, a file edited by hand, and so on) are reported.
- Says how to check for newer rules.

## 2. Public interface

### The answer

- A few lines in plain words. They say: what is finished, what is being done now, how many pieces the current work has and which one it is on, what comes next.
- No name left unexplained (milestone numbers, commit hashes, file names, and so on). A milestone is named by what it does, not by a number.
- When a change is in progress, distinguish completed tasks from completion of the change. Include remaining checks, findings or questions when they determine what happens next.

Example:

> The word-count program can read and count documents. It is now being extended to show the results. The screen changes are complete, but two of the five checks and one reported issue remain. The assigned roles will fix the issue and finish the checks before this milestone is complete.

### Where it reads

- intent: milestones and scope
- the design README: the module map and the current milestone
- the work note: assigned tasks and progress, check results, unresolved findings and questions

The lead maintains the note from reports received through the project's workflow (A change, The work note). Direct exchanges between roles must still supply enough progress and result information for the lead to update it. A report that a task is built does not establish that the five checks are complete. Missing reports remain unconfirmed; the lead requests the needed update through the workflow, without reading impl.

### Reporting things to fix

When the lead learns of one of these, it tells the user in plain words what to do.

| When it learns | It tells |
|---|---|
| the lead changed the settings | the setup must be reproduced again |
| validate says a reproduced file's checksum differs | that file was edited by hand; fix the rules or the settings and reproduce again |
| validate says the setup record is missing or broken | the setup must be reproduced again |

### Newer rules

When the user asks about the rules, and the network is available, the lead fetches the tags of the plumbline repository the setup record names.

- When there is a tag with a higher version than the tag on the setup record's commit, it says: "the setup was made from rules version X, and version Y is out".
- When the setup record's commit has no tag, it names the tag with the highest version.
- When the network is not available, it says it could not check.
- A version is whole numbers joined by dots, with or without a leading `v`. Versions compare number by number from the left; a missing number counts as 0 (`1.2` equals `1.2.0`). A tag not of this form is ignored.

## 3. Flow

1. The user asks where things stand.
2. The lead reads intent's milestones, the design README's module map and current milestone, and the work note.
3. If needed reports are missing, the lead requests them through the workflow and updates the note when they arrive. Until then, it identifies what is still unconfirmed.
4. It answers in the form above.

## 4. Invariants and contracts

- Where things stand is said only when the user asks.
- The answer is given without reading impl.
- A role's completed task or a missing report is not presented as a completed change. Completion follows A change, The five checks.

## 5. Decisions and reasons

- There is no script; the lead reads and says it. The answer must be in plain words, and there are only three places to read.
- The design README holds the current milestone, so there is an answer even when no change is in progress.
- Things to fix are reported when the lead learns of them. There is no separate part that checks every time.
- Reports converge in the work note so the lead can describe progress even when work and checks are split among roles.

## 6. Verification criteria

This needs judgment, so there are no executable conformance cases. The project's assigned roles review the rules for the answer's form, sources and reporting times, including these situations:

- A role has finished building, but checks or findings remain: the answer distinguishes the finished task from the unfinished change.
- Roles exchange results directly: their reports still update the lead's work note, and the lead answers without reading impl.
- A required report is missing: the answer names the unconfirmed work rather than treating it as passed.

## 7. Out of scope

None.
