# Layers and settings

## 1. Responsibilities

- Says what each of the three layers (intent, design, impl) says, and what is read when writing each.
- Defines the project settings file.
- Defines how to tell which layer a path belongs to.
- Names what each project decides for itself.

What each role reads and writes is in Roles; the form of design documents is in Design documents.

## 2. Public interface

### The three layers

| Layer | Says | Read when writing it |
|---|---|---|
| intent | what to build and why: scope, milestones, decisions and their reasons, open questions | — |
| design | how it is divided and what it promises: what each module does, public interfaces, invariants, decisions, verification criteria | intent, design |
| impl | code and tests, and anything else built from the design (such as documents an AI reads) | design, impl |

### The settings file

It is `.plumbline/settings.json`. Its form:

```json
{
  "layers": {
    "intent": ["docs/intent.md"],
    "design": ["docs/design"],
    "impl": ["src", "tests"]
  },
  "not_in_git": ["intent"]
}
```

- `layers`: for each of the three layers `intent`, `design` and `impl`, a list of its locations. Every layer has at least one.
- A location is a path from the project root, separated by `/`, with no `/` at its start or end. It may be a file or a folder.
- `not_in_git`: the names of the layers kept out of git. When it is absent or empty, all three layers are in git.
- The design location is one folder.
- These break the form: a key other than `layers` and `not_in_git`; a location with an empty name, `.` or `..`; a layer named twice in `not_in_git`; locations of two layers that overlap.

### Which layer a path belongs to

- A path belongs to a layer when it equals one of the layer's locations or lies inside one of its location folders.
- Sharing only the start of a name is not lying inside. With the location `docs/design`, `docs/design/a.md` belongs to design and `docs/designer.md` does not.
- A path may belong to no layer.
- Even when a location is a file, a path that continues it with `/` is taken to belong to that layer (for example, `docs/intent.md/x`). Whether a path exists, or is a file or a folder, does not matter.

### What each project decides

The language of documents and code, the code comment policy, the form of intent, the layout and file names of the design, the kinds of figures, the names of milestones, and checks between layers that only that project needs.

## 3. Flow

1. A layer's locations are decided with the user before that layer's first file is saved: intent's before the first intent draft is saved, design's before the module map is saved, impl's before the reproduction.
2. Whether a layer is kept out of git is decided before that layer's first file is saved.
3. Each decision is written in the settings file at once. For a layer kept out of git, its locations are added to `.git/info/exclude` at once.
4. When the settings change, the setup is reproduced again (Reproduction).

## 4. Invariants and contracts

- The locations of two layers never overlap. A path belongs to at most one layer.
- Every location of a layer kept out of git is in `.git/info/exclude`.
- The content of a layer kept out of git is never copied into a file of a layer in git. When needed, only the document's path and section title are named.
- A check that needs a layer is skipped where that layer is absent (for example, in a clone of a repository that keeps it out of git).

## 5. Decisions and reasons

- There are only two settings. Only what reproduction and the checks must know is taken; everything else is the project's.
- By default all three layers are in git. That is for when other people use it.
- A layer is kept out of git with `.git/info/exclude`. It lives on that machine only and leaves no trace in the repository.
- Each layer takes a list of locations. A layer such as impl can be spread over several places.
- Only design is one folder. With one design README, the module map is in one place.

## 6. Verification criteria

- With the location `docs/design`: `docs/design`, `docs/design/a.md` and `docs/design/sub/b.md` belong to design.
- With the location `docs/design`: `docs/designer.md` and `docs` do not belong to design.
- With the file location `docs/intent.md`: that file, and a path that continues it with `/` (`docs/intent.md/x`), belong to intent.
- Settings with two design locations, or with overlapping locations of two layers, break the form.
- When the settings file is missing or does not have its form, the role guard and reproduction report an environment error, and validate gives a `settings` problem line.

These criteria are shown by the conformance cases of the role guard and validate (Conformance cases).

## 7. Out of scope

- Keeping only part of a layer out of git. The settings work by whole layers only.
