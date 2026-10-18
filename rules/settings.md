# Project settings

The project settings are where the three layers are, and which of them are kept out of git. Everything else a project decides belongs in its own intent and design, not in the settings.

## The file

- `.plumbline/settings.json` at the project root. People edit it. It is in git.
- `.plumbline/` is the one folder for everything plumbline keeps in a project: the settings, the template ([design-docs.md](design-docs.md)), the setup record ([setup-record.md](setup-record.md)), and the change records and the current change ([changes.md](changes.md)).

## The format

A JSON object with exactly two keys:

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

| Key | Value |
|---|---|
| `layers` | an object with exactly the keys `intent`, `design`, `impl`. Each value is a non-empty list of paths |
| `not_in_git` | a list of the layers kept out of git, each `intent`, `design` or `impl`. Empty when every layer is in git. That is the default |

Paths:

- A path is relative to the project root and uses `/`. It is one or more segments joined by single `/`, with no `/` at its start or end, and no segment that is empty, `.` or `..`.
- A path names a file or a folder. A folder means everything under it.
- `design` has exactly one path, and it is a folder. `<design location>/README.md` is the design README ([design-docs.md](design-docs.md)).
- No path of one layer lies inside, or contains, a path of another layer.

Any other key, anywhere in the object, is an error.

Examples:

- The object above is valid.
- A missing `layers` key, a missing layer, an empty path list, a second `design` path, or a `design` path that is a file is an error.
- A path of `impl` inside the `design` folder is an error.
- The paths `/src`, `src/`, `./src`, `src//main` and `docs/../src` are errors.
- An unknown key at any level is an error.

## A layer kept out of git

- Every path of a layer in `not_in_git` is listed in the project's `.git/info/exclude`. The lead lists them as soon as the layer is set to stay out of git ([authoring.md](authoring.md)), and every reproduction adds any that are missing ([reproduction.md](reproduction.md)).
- The content of a layer kept out of git is never copied into a file that is in git: a design document, a change record, a rule carrier, the setup record, or any other. Only its location may be cited: a document path, a version, a section.
- A layer kept out of git has no git history. How its history is kept is the project's choice.
- `validate` reports a file that git tracks at a location of a layer kept out of git ([validate.md](validate.md#files-kept-out-of-git)).

## A check and a missing layer

A layer is present when at least one of its paths exists.

When a check needs a layer:

| The layer | The check |
|---|---|
| is present | runs that part |
| is not present, and is in `not_in_git` | skips that part and says it skipped it |
| is not present, and is not in `not_in_git` | reports an error: a layer in git is missing |

Examples:

- With `intent` in `not_in_git` and no intent file present, a check that needs intent skips that part and says so.
- With `intent` not in `not_in_git` and no intent file present, a check that needs intent reports an error.
