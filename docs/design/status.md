# Status

## 1. Responsibilities

- Says how the lead answers when the user asks where things stand.
- Says when things to fix (reproducing again, a file edited by hand, and so on) are reported.
- Says how to check for newer rules.

## 2. Public interface

### The answer

- A few lines in plain words. They say: what is finished, what is being done now, how many pieces the current work has and which one it is on, what comes next.
- No name left unexplained (milestone numbers, commit hashes, file names, and so on). A milestone is named by what it does, not by a number.

Example:

> The word-count program has finished its first milestone (reading and counting documents). Now the design of the second milestone, "showing the results", is being written. Two of its three module documents are confirmed. Once the third is confirmed, the implementer builds it, and then the third milestone starts.

### Where it reads

- intent: milestones and scope
- the design README: the module map and the current milestone
- the work note: the change in progress and how far it is

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
3. It answers in the form above.

## 4. Invariants and contracts

- Where things stand is said only when the user asks.
- The answer is given without reading impl.

## 5. Decisions and reasons

- There is no script; the lead reads and says it. The answer must be in plain words, and there are only three places to read.
- The design README holds the current milestone, so there is an answer even when no change is in progress.
- Things to fix are reported when the lead learns of them. There is no separate part that checks every time.

## 6. Verification criteria

This needs judgment, so there are no conformance cases. The verifier checks that the rules state the answer's form, where it reads, and when things are reported, without omission.

## 7. Out of scope

None.
