# Setup record

## 1. Responsibilities

- Defines where the setup record is and its form.
- Defines how checksums are computed.

When the setup record is written is in Reproduction; when checksums are compared is in Validate.

## 2. Public interface

### The file

- It is `.plumbline/setup-record.json`.
- Only a reproduction writes it. Each reproduction writes it anew, whole. Nobody edits it by hand.
- It is in git, and so is every file it lists.

### The form

One JSON object with exactly these keys. The paths, commands and checksums in the example are made up for illustration.

```json
{
  "rules": {
    "repository": "https://github.com/OWNER/plumbline",
    "commit": "0123456789abcdef0123456789abcdef01234567",
    "tag": "v2.0"
  },
  "settings": {
    "layers": {
      "intent": ["docs/intent.md"],
      "design": ["docs/design"],
      "impl": ["src", "tests"]
    },
    "not_in_git": ["intent"]
  },
  "files": [
    {
      "path": "INSTRUCTIONS.md",
      "checksum": "sha256:0f8ffbd6cd643eb1b595ee683fc34eef9d208436d1ecbf35585077d17151e2d7",
      "begin": "<!-- plumbline:begin -->",
      "end": "<!-- plumbline:end -->"
    },
    {
      "path": ".plumbline/parts/validate",
      "checksum": "sha256:4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a"
    }
  ],
  "carriers": [
    { "kind": "instruction file, reproduced part", "files": ["INSTRUCTIONS.md"], "roles": ["lead", "implementer", "verifier"] }
  ],
  "parts": [
    { "name": "validate", "runner": ["RUNNER"], "entry": ".plumbline/parts/validate" }
  ],
  "renderers": [
    { "figure": "mermaid", "command": ["RENDERER", "--check"] }
  ],
  "enforcement": [
    { "rule": "intent-read", "by": "mechanical", "part": "role-guard" },
    { "rule": "design-write", "by": "instruction" }
  ]
}
```

| Key | Holds |
|---|---|
| `rules` | where the rules were read from |
| `settings` | a copy of the settings the reproduction used, in the form of the settings file (Layers and settings) |
| `files` | every file the reproduction wrote, except the setup record itself and `.git/info/exclude` |
| `carriers` | the rule carriers the reproduction chose |
| `parts` | the mechanical parts and how to run each |
| `renderers` | for each figure kind that has a renderer, how to render |
| `enforcement` | for each rule that may be enforced mechanically, whether it is, or is left as an instruction |

Any other key makes the form wrong.

#### `rules`

| Key | Holds |
|---|---|
| `repository` | the address of the plumbline repository the rules were read from. It must be reachable from other machines too: an address that starts with `<scheme>://` (the scheme is not `file`), or of the form `<user>@<host>:<path>`. A path on the machine is not allowed |
| `commit` | the full hash of the commit the rules were read at: 40 or 64 lowercase hexadecimal digits |
| `tag` | optional. A tag that named that commit when the reproduction ran. It is for people; the commit is what counts |

#### `files`

One object per file. No path appears twice.

| Key | Holds |
|---|---|
| `path` | relative to the project root, separated by `/` |
| `checksum` | `sha256:` followed by 64 lowercase hexadecimal digits |
| `begin`, `end` | only for a file the project also writes: the exact text of the line that opens the reproduced part and of the line that closes it |

Without `begin` and `end`, the reproduction wrote the whole file. With both, the reproduction wrote only the lines from `begin` to `end`, and the rest is the project's.

#### `carriers`

One object per rule carrier.

| Key | Holds |
|---|---|
| `kind` | what it is, in the reproducing AI's words: an instruction file, a file it points to, a script a hook runs, a skill, and so on |
| `files` | the paths that make up the carrier. Each is in `files` |
| `roles` | the roles the carrier reaches: one or more of `lead`, `implementer`, `verifier`, each once |

#### `parts`

One object per mechanical part.

| Key | Holds |
|---|---|
| `name` | the part's name: not empty, and not twice. A reproduction writes the names the modules that define the parts give (`validate`, `role-guard`) |
| `runner` | the command that runs the part, as a list: the runner and any arguments it needs before the entry file |
| `entry` | the path of the file the runner runs. It is in `files` |

A part is run as its `runner`, then its `entry`, then the part's own arguments (Conformance cases).

#### `renderers`

One object per figure kind for which a renderer was found. It may be empty.

| Key | Holds |
|---|---|
| `figure` | a figure kind named in the template. No name appears twice |
| `command` | the command that renders one figure, as a list. A file it runs that the reproduction wrote is in `files` |

A renderer runs in the project root, with the figure's text (the lines between its opening and closing fences) on standard input. Ending with 0 means it rendered; anything else means it did not. A renderer that cannot be started counts as absent.

#### Commands

`runner` and `command` hold no absolute path. The first element (the runner) is a name found on the PATH, so it holds no `/` or `\`. No element starts with `/` or `\`, or with a letter, `:` and then `/` or `\`.

#### `enforcement`

One object per rule that may be enforced mechanically.

| Key | Holds |
|---|---|
| `rule` | the rule's name: not empty, and not twice. A reproduction writes `intent-read` (the implementer and the verifier cannot read intent) and `design-write` (the implementer cannot write design). Other names come from records written under older rules |
| `by` | `mechanical` or `instruction`. It is `mechanical` only when the part that enforces it passed every conformance case and acting through its connector blocked and passed as expected |
| `part` | only when `by` is `mechanical`: the `name` of the part that enforces it |

### Checksums

1. Read the file's bytes and turn every CR LF into LF.
2. For a whole file, take all the bytes.
3. For a reproduced part, split the bytes into lines at LF. The line equal to `begin` and the line equal to `end` each occur exactly once in the file, `begin` first. Take the bytes from the start of the `begin` line to the end of the `end` line (with the `end` line's LF, when it has one).
4. The checksum is `sha256:` followed by the SHA-256 of the bytes taken, in lowercase hexadecimal.

When the `begin` line or the `end` line is missing, occurs more than once, or `end` comes first, the reproduced part cannot be found. That is not the same as a checksum that differs.

## 3. Flow

1. When the reproduction has written the setup and every conformance case passes, it writes the setup record, whole.
2. When reproducing again, the reproduction reads the previous setup record to know the files it wrote before.
3. Validate compares the checksums of the files the setup record lists.

## 4. Invariants and contracts

- Only a reproduction writes the setup record.
- Every file in `files` was written by the reproduction, and every file the reproduction wrote (except the setup record and `.git/info/exclude`) is in `files`.
- Every file named in `carriers`, `parts` and `renderers` is in `files`.
- A file has at most one reproduced part.

## 5. Decisions and reasons

- The commit is what counts; the tag is added for people. A commit never changes.
- The repository address must be reachable from other machines, so that a clone or another machine can reproduce again.
- Commands hold no absolute path. Paths differ between machines, and the record would fit only one machine.
- Checksums are computed with line ends turned into LF. A change only in line ends, from the operating system or git settings, is not an edit by hand.
- A reproduced part's checksum covers only that part. The rest is where the project edits.

## 6. Verification criteria

Shown by validate's conformance cases (Validate).

- A setup record with the right form → no problem.
- An unknown key; a `commit` that is not 40 or 64 digits; a `repository` that is a path on the machine; a `runner` whose first element is `/usr/bin/python3`; a part's `entry` that is not in `files` → `record` each.
- The content of a whole-file entry changed → `checksum`.
- The same content with CR LF line ends → no problem.
- A change inside a reproduced part → `checksum`. A change only outside it → no problem.
- A reproduced part with no `end` line, or with the `begin` line twice → `part-not-found`.

## 7. Out of scope

None.
