# Layers and settings

What each role reads and writes is in [roles.md](roles.md). The form of design documents is in [design-docs.md](design-docs.md).

## The three layers

| Layer | Says | Read when writing it |
|---|---|---|
| intent | what to build and why: scope, milestones, decisions and their reasons, open questions | — |
| design | how it is divided and what it promises: what each module does, public interfaces, invariants, decisions, verification criteria | intent, design |
| impl | code and tests, and anything else built from the design, such as documents an AI reads | design, impl |

- The last column is the read direction. Writing design reads intent and design, never impl. Writing impl reads design and impl, never intent.
- A point belongs to the layer whose "Says" column names its kind.

## The settings file

The settings file is `.plumbline/settings.json`. Its form:

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

- It is one JSON object with the key `layers`, and optionally the key `not_in_git`. It has no other key.
- `layers` is an object with exactly the keys `intent`, `design` and `impl`. The value of each is the list of that layer's locations. Every layer has at least one.
- A location is a path from the project root: one or more names separated by single `/` characters, with no `/` at its start or end. No name is empty, `.` or `..`. A location may be a file or a folder.
- The design location is one folder: `design` has exactly one location.
- `not_in_git` is a list of the names of the layers kept out of git, each named at most once. When it is absent or empty, all three layers are in git.
- No location of one layer equals, contains or lies inside a location of another layer ([Which layer a path belongs to](#which-layer-a-path-belongs-to)).

A settings file that breaks any of these does not have its form.

Examples:

- The object above has the form. So does the same object without `not_in_git`.
- A missing layer, an empty list of locations, two design locations, a key other than those above at any level, an unknown layer name in `not_in_git`, and a layer named twice in `not_in_git` each break the form.
- With the design location `docs/design`, an impl location `docs/design/x` breaks the form.
- The locations `/src`, `src/`, `./src`, `src//main` and `docs/../src` break the form.

## Which layer a path belongs to

- A path lies inside a location when it begins with the location followed at once by `/`. This holds for a file location too. The project root contains every path.
- A path belongs to a layer when it equals one of the layer's locations, or lies inside one of them.
- Sharing only the start of a name is not lying inside.
- A path may belong to no layer.
- Whether a path exists, and whether it is a file or a folder, does not matter.

Examples:

- With the location `docs/design`: `docs/design`, `docs/design/a.md` and `docs/design/sub/b.md` belong to design; `docs/designer.md` and `docs` do not.
- With the file location `docs/intent.md`: that file belongs to intent, and so does a path that continues it with `/`, such as `docs/intent.md/x`. `docs/intent.md.bak` and `docs/intent` do not.

## What each project decides

The language of documents and code, the code comment policy, the form of intent, the layout and file names of the design, the kinds of figures, the names of milestones, and checks between layers that only that project needs.

## When settings are decided

1. A layer's locations are decided with the user before that layer's first file is saved: intent's before the first intent draft is saved, design's before the module map is saved, impl's before the first reproduction.
2. Whether a layer is kept out of git is decided before that layer's first file is saved.
3. The lead writes each decision into the settings file at once. Until the first reproduction, the file holds only what has been decided. For a layer kept out of git, the lead adds each of its locations to `.git/info/exclude` at once, as a line that is `/` followed by the location.
4. When the settings change, the setup is reproduced again ([reproduction.md](reproduction.md)).

## What always holds

- A path belongs to at most one layer.
- Every location of a layer kept out of git is in `.git/info/exclude`.
- The content of a layer kept out of git is never copied into a file of a layer in git. Where it must be referred to, only the document's path and the section's title are named.
- A check that needs a layer is skipped where that layer is absent, such as in a clone of a repository that keeps it out of git. A layer is absent when none of its locations exists.
- When the settings file is missing or does not have its form, the role guard and reproduction report an environment error ([roles.md](roles.md#the-role-guard), [reproduction.md](reproduction.md#when-it-stops-before-writing-anything)), and validate gives a `settings` problem line ([validate.md](validate.md#problem-lines)).
