# Setup record

The setup record is where a reproduction writes what it used and what it wrote. When it is written is in [reproduction.md](reproduction.md). When its checksums are compared is in [validate.md](validate.md).

## The file

- It is `.plumbline/setup-record.json`.
- Only a reproduction writes it. Each reproduction writes it anew, whole. Nobody edits it by hand.
- It is in git, and so is every file it lists.

## The form

One JSON object with exactly these keys. The paths, commands and checksums in the example are made up.

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
| `settings` | a copy of the settings the reproduction used, in the form of the settings file ([layers.md](layers.md#the-settings-file)) |
| `files` | every file the reproduction wrote, except the setup record itself and `.git/info/exclude` |
| `carriers` | the rule carriers the reproduction chose |
| `parts` | the mechanical parts, and how to run each |
| `renderers` | for each figure kind that has a renderer, how to render it |
| `enforcement` | for each rule that may be enforced mechanically, whether it is, or is left as an instruction |

Any other key, at any level, breaks the form.

### `rules`

| Key | Holds |
|---|---|
| `repository` | the address of the plumbline repository the rules were read from. It is reachable from other machines too: it has one of the two forms below. A path on the machine is never one |
| `commit` | the full hash of the commit the rules were read at: 40 or 64 lowercase hexadecimal digits |
| `tag` | optional. A tag that named that commit when the reproduction ran. The commit is what names the rules; the tag is for people |

An address has one of these two forms:

- `<scheme>://` followed by a rest that is not empty. The scheme begins with an ASCII letter, and holds only ASCII letters, digits, `+`, `-` and `.`. It is not `file`, in any case of its letters.
- `<user>@<host>:<path>`. None of the three is empty. The user and the host hold no `/`, `:` or `@`.

Examples: `https://github.com/OWNER/plumbline` and `git@github.com:OWNER/plumbline.git` are addresses. `~/Projects/plumbline`, `plumbline`, `/srv/plumbline`, `../plumbline`, `C:\src\plumbline`, `file:///srv/plumbline` and `https://` are not.

### `files`

One object per file. No path appears twice.

| Key | Holds |
|---|---|
| `path` | relative to the project root, in the form of a location ([layers.md](layers.md#the-settings-file)) |
| `checksum` | `sha256:` followed by 64 lowercase hexadecimal digits |
| `begin`, `end` | only for a file the project also writes: the exact text of the line that opens the reproduced part, and of the line that closes it. Both are present, or neither. Each is not empty, holds no line break, and they differ |

Without `begin` and `end`, the reproduction wrote the whole file. With both, the reproduction wrote only the lines from `begin` to `end`, and the rest is the project's.

### `carriers`

One object per rule carrier.

| Key | Holds |
|---|---|
| `kind` | what the carrier is, in the reproducing AI's own words: an instruction file, a file it points to, a script a hook runs, a skill, and so on. It is not empty |
| `files` | the paths that make up the carrier, one or more, none twice. Each is the `path` of an entry in `files` |
| `roles` | the roles the carrier reaches: one or more of `lead`, `implementer` and `verifier`, each at most once |

### `parts`

One object per mechanical part.

| Key | Holds |
|---|---|
| `name` | the part's name: not empty, and not twice. A reproduction writes the names the files that state the parts give: `role-guard` ([roles.md](roles.md#the-role-guard)) and `validate` ([validate.md](validate.md)) |
| `runner` | the command that runs the part, as a list: the runner, and any arguments it needs before the entry file. It has the form [Commands](#commands) states |
| `entry` | the path of the file the runner runs. It is the `path` of an entry in `files` |

A part is run as its `runner`, then its `entry`, then the part's own arguments ([conformance.md](conformance.md#running-a-part)).

### `renderers`

One object per figure kind for which a renderer was found. The list may be empty.

| Key | Holds |
|---|---|
| `figure` | a figure kind named in the template: one or more characters, none of them white space. No kind appears twice |
| `command` | the command that renders one figure, as a list. It has the form [Commands](#commands) states. A file it runs that the reproduction wrote is in `files` |

A renderer runs in the project root, with the figure's text on standard input: the lines between the figure's opening line and its closing line, each followed by LF ([design-docs.md](design-docs.md#reading-a-markdown-document)). Ending with status 0 means the figure rendered; any other status means it did not. A renderer that cannot be started counts as absent.

### Commands

A part's `runner` and a renderer's `command` are lists of one or more texts, and hold no absolute path:

- The first element is a name found on the PATH. It is not empty, and holds no `/` and no `\`.
- No element begins with `/` or `\`, or with an ASCII letter, a `:`, and then `/` or `\`.

Examples, as JSON: `["python3"]`, `["python3", ".plumbline/render"]` and `["git", "--version"]` have this form. `["/usr/bin/python3"]`, `["/usr/local/bin/mmdc"]` and `["C:\\tools\\mmdc.exe"]` do not: each is an absolute path. `["tools/mmdc"]` does not either: its first element holds `/`.

### `enforcement`

One object per rule that may be enforced mechanically.

| Key | Holds |
|---|---|
| `rule` | the rule's name: not empty, and not twice. A reproduction writes `intent-read`, the implementer and the verifier cannot read intent, and `design-write`, the implementer cannot write design. Other names come from records written under older rules |
| `by` | `mechanical` or `instruction`. It is `mechanical` only when the part that enforces it passed every conformance case, and acting through its connector blocked and passed as expected ([reproduction.md](reproduction.md#mechanical-or-instruction)) |
| `part` | present exactly when `by` is `mechanical`: the `name` of the entry in `parts` that enforces the rule |

### What does not bear on the form

- Whether a listed file exists, or matches its checksum.
- Whether a runner or a renderer can be started on the machine where the record is read.
- Whether the template still names each figure kind in `renderers`.
- Whether a path in the copy of the settings exists. That copy is checked against the settings file's form without looking at files.

Among the ways to break the form: an unknown key; a missing key; a `commit` that is not 40 or 64 digits; a `repository` that is a path on the machine; a checksum without `sha256:`; a path listed twice in `files`; a carrier file or a part's `entry` that is not in `files`; a carrier without `roles`, or with a role other than the three; a `mechanical` entry without `part`, or an `instruction` entry with one; two renderers for one figure kind; a runner whose first element is `/usr/bin/python3`.

## Checksums

1. Read the file's bytes, and turn every CR LF into LF.
2. For a whole file, take all the bytes.
3. For a reproduced part, split the bytes into lines at LF. The line equal to `begin` and the line equal to `end` each occur exactly once in the file, `begin` first. Take the bytes from the start of the `begin` line to the end of the `end` line, with the `end` line's LF when it has one.
4. The checksum is `sha256:` followed by the SHA-256 of the bytes taken, in lowercase hexadecimal.

When the `begin` line or the `end` line is missing, occurs more than once, or the `end` line comes first, the reproduced part cannot be found. That is not a checksum that differs.

Examples:

- An empty whole file has `sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- A whole file holding `a` CR LF `b` CR LF, and one holding `a` LF `b` LF, both have `sha256:911169ddaaf146aff539f58c26c489af3b892dff0fe283c1c264c65ae5aa59a2`.
- A reproduced part made of the lines `<!-- plumbline:begin -->`, `rule one` and `<!-- plumbline:end -->`, each ending in LF, has `sha256:0feea6f5b44d05e5c486ab443fce6ba01ec0951d9ee6c24d79a907c3758e9f67`, whatever project lines come before and after it. With `rule two` in place of `rule one`, it has `sha256:372194c54600515e210c907b2e0b3ffc3381da531960057b83ac9ae667b1f878`.

## Steps

1. When a reproduction has written the setup and every conformance case passes, it writes the setup record, whole.
2. When reproducing again, the reproduction reads the previous setup record to know the files it wrote before.
3. validate compares the checksums of the files the setup record lists.

## What always holds

- Only a reproduction writes the setup record.
- Every file in `files` was written by a reproduction, and every file the reproduction wrote, except the setup record and `.git/info/exclude`, is in `files`.
- Every file named in `carriers`, `parts` and `renderers` is in `files`.
- A file has at most one reproduced part.
- No runner and no renderer command holds an absolute path.
