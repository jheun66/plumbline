# Authoring

The lead and the user write a project's intent, then its design's module map, then its module documents, milestone by milestone. The lead does all of it. It reads intent and design only, never impl ([roles.md](roles.md)).

## Order

1. Intent: draft it, resolve it, confirm it.
2. The template's project part ([design-docs.md](design-docs.md)), then the module map and the design's README, whose `milestone` line names the first milestone. The user confirms the map.
3. The settings are complete, and the setup is reproduced ([reproduction.md](reproduction.md)).
4. The module documents of the first milestone. The user confirms them. Then implementers build that milestone's impl ([roles.md](roles.md)).
5. Each later milestone: once the previous milestone's impl is done, the lead changes the `milestone` line of the design's README to it. Then its module documents are written, then its impl is built.

A milestone's module documents are all confirmed before its impl starts.

From the first reproduction on, each milestone's work is one change, opened before that work starts ([changes.md](changes.md#a-milestones-work)). A gap found during it is a gap item of that change.

## Writing intent

1. The lead listens to the user and writes a draft at the intent location. Every item in the draft carries one of three marks: decided (the user said or chose it), proposed (the lead's default), open (a question).
2. Near its top, the draft names its three marks, in the project's own words. A new session can continue from the draft alone.
3. The lead resolves the open questions, then the proposals, one item at a time. A point that follows directly from earlier decisions is applied without asking, and the user is told. Only real choices are asked.
4. When no proposal and no open question is left, the intent is confirmed. The lead raises its version ([layers.md](layers.md)) and states in it, in the project's own words, that the user confirmed it and on which date.

An item's mark:

| Mark | Set when | Becomes |
|---|---|---|
| open | the lead cannot propose a default | proposed, when the lead proposes an answer; decided, when the user answers |
| proposed | the lead proposes a default | decided, when the user accepts or changes it |
| decided | the user said or chose it | stays decided |

- The version stays the same while the draft is worked on. It is raised when the intent is confirmed.
- The form of intent is the project's, beyond what [layers.md](layers.md) requires: Markdown files at the intent location, each with one version line.
- The lead does not ask about the natural language of the project's documents, a policy for code comments, or similar working conventions. When the user states them, they go into intent.
- No mechanical part checks the marks or the confirmation.

## Settings decided on the way

| Setting ([settings.md](settings.md)) | Decided |
|---|---|
| the intent location | before the first draft is saved |
| the design location | before the module map is saved |
| the impl locations | before the reproduction |
| whether a layer stays out of git | before anything of that layer is saved |

- The lead proposes each setting, and the user confirms it.
- The lead writes each setting into the settings file as soon as it is decided. Until the reproduction starts, the file may be incomplete. When it starts, the file is complete and valid.
- As soon as a layer is set to stay out of git, the lead lists its paths in `.git/info/exclude`. When the project is not yet a git repository, the lead tells the user that nothing is excluded until it is one.

## The module map

1. After intent is confirmed, the lead settles the template's project part with the user: the seven section titles and the two marker texts ([design-docs.md](design-docs.md)). The lead writes them into the template.
2. The lead writes the module map from intent only: the modules, their dependencies, the flows, and the contracts that hold for every module. With it comes the design's README: scope, reading order, terms, and the `milestone` line ([design-docs.md](design-docs.md#design-documents-and-module-documents)).
3. The map gives every module the milestone in which its document is written.
4. The user confirms the map. Every design-level decision in it then carries the confirmed marker with the date.

The module map is a module document. Its level-2 headings equal the template's. Its name and place in the design are the project's choice.

## Module documents

- They are written milestone by milestone, in the order the map gives.
- Each is derived from intent and the design documents above it, never from impl ([layers.md](layers.md)).
- Design-level decisions are written with the pending marker. When the user confirms them, each marker becomes the confirmed one with the date.
- The lead may present a milestone's documents in groups. Each group is confirmed before the next is written.
- A point the user must choose is asked one at a time. A point that follows directly from earlier decisions is applied, reported, and confirmed with the rest.
- When writing design reveals a gap in intent, the lead stops and proposes the change to intent. After the user confirms, intent is changed first and its version raised.
