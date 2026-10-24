# Status

The lead says where things stand when the user asks. It reports things to fix when it learns of them, and checks for newer rules when the user asks about the rules. There is no mechanical part for any of this.

## The answer

- A few lines in plain words. They say what is finished, what is being done now, how many pieces the current work has and which one it is on, and what comes next.
- No name is left unexplained: milestone numbers, commit hashes, file names, and so on. A milestone is named by what it does, not by a number.

Example:

> The word-count program has finished its first milestone (reading and counting documents). Now the design of the second milestone, "showing the results", is being written. Two of its three module documents are confirmed. Once the third is confirmed, the implementer builds it, and then the third milestone starts.

## Where it reads

- intent: the milestones and the scope;
- the design README: the module map and the current milestone ([design-docs.md](design-docs.md#the-module-map));
- the work note: the change in progress, and how far it is ([change.md](change.md#the-work-note)). When there is no work note, no change is in progress.

## Steps

1. The user asks where things stand.
2. The lead reads intent's milestones, the design README's module map and current milestone, and the work note.
3. It answers in the form above.

## Things to fix

When the lead learns of one of these, it tells the user in plain words what to do:

| When it learns | It tells |
|---|---|
| the lead changed the settings | the setup must be reproduced again |
| validate says a reproduced file's checksum differs | that file was edited by hand; the rules or the settings are fixed, and the setup is reproduced again |
| validate says the setup record is missing or broken | the setup must be reproduced again |

## Newer rules

When the user asks about the rules:

- When the network is available, the lead fetches the tags of the plumbline repository the setup record names.
- A version is whole numbers joined by dots, with or without a leading `v`, such as `v1.2` or `1.2`. Versions compare number by number from the left; a missing number counts as 0. A tag not of this form is ignored.
- When a tag names a higher version than the tag on the setup record's commit, the lead says: the setup was made from rules version X, and version Y is out. Y is the highest version among the tags.
- When no tag is on the setup record's commit, it names the tag with the highest version.
- Otherwise, it says that no newer version is out.
- When the network is not available, it says that it could not check.

## What always holds

- Where things stand is said only when the user asks.
- The answer is given without reading impl.
