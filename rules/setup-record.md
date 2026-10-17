# Setup record

The setup record is the one file in which a reproduction writes what it used and what it produced.

## The file

- `.plumbline/setup-record.json` at the project root.
- Only a reproduction writes it. Each reproduction replaces it whole. Nobody edits it by hand.
- The record is in git, and so is every file it lists.
- The record and every file it lists lie outside every layer location ([settings.md](settings.md)).

## The format

A JSON object with exactly these keys:

```json
{
  "rules": {
    "repository": "https://github.com/OWNER/plumbline",
    "commit": "0123456789abcdef0123456789abcdef01234567",
    "tag": "v0.1"
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
      "path": ".plumbline/lead.md",
      "checksum": "sha256:bb5e6a13ff86dc4f333bbef04ca0657bfebcbc2b173a2a42aedd4d1e849e3d3e"
    },
    {
      "path": ".plumbline/implementer.md",
      "checksum": "sha256:d7643b3243eb56482b2b34a8dde980201d3787e34475476743fd182667eec2bd"
    },
    {
      "path": ".plumbline/template.md",
      "checksum": "sha256:ea86728e0c9f2933951b83eea2a0b9a9e30b4aa03de63621d1e8c59f8618e15d",
      "begin": "<!-- plumbline:begin -->",
      "end": "<!-- plumbline:end -->"
    },
    {
      "path": ".plumbline/parts/status",
      "checksum": "sha256:4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a"
    },
    {
      "path": ".plumbline/parts/gap-guard",
      "checksum": "sha256:ef2d127de37b942baad06145e54b0c619a1f22327b2ebbcfbec78f5564afe39d"
    },
    {
      "path": ".plumbline/hooks/gap-guard-connector",
      "checksum": "sha256:e7f6c011776e8db7cd330b54174fd76f7d0216b612387a5ffcfb81e6f0919683"
    }
  ],
  "carriers": [
    { "kind": "instruction file, reproduced part: the roles and where each role's rules are", "files": ["INSTRUCTIONS.md"] },
    { "kind": "file the instruction file names for the lead", "files": [".plumbline/lead.md"] },
    { "kind": "file the instruction file names for the implementer", "files": [".plumbline/implementer.md"] }
  ],
  "parts": [
    { "name": "status", "runner": ["RUNNER"], "entry": ".plumbline/parts/status" },
    { "name": "gap-guard", "runner": ["RUNNER"], "entry": ".plumbline/parts/gap-guard" }
  ],
  "enforcement": [
    { "rule": "role table", "by": "instruction" },
    { "rule": "gap guard", "by": "mechanical", "part": "gap-guard" }
  ]
}
```

The paths, runners and checksums in this example are illustrations. A reproduction chooses its own.

| Key | Value |
|---|---|
| `rules` | where the rules came from |
| `settings` | a copy of the settings the reproduction used, in the format of [settings.md](settings.md) |
| `files` | every file the reproduction wrote, except the record itself and `.git/info/exclude` |
| `carriers` | the rule carriers the reproduction chose |
| `parts` | the mechanical parts of the setup, and how each is run |
| `enforcement` | for each rule that may be enforced mechanically, whether it is |

Any other key, anywhere in the object, is an error. The record holds no time.

### `rules`

| Key | Value |
|---|---|
| `repository` | the plumbline repository the rules were read from, as the user gave it |
| `commit` | the full hash of the commit the rules were read at: 40 or 64 lowercase hexadecimal digits |
| `tag` | optional. A tag that named that commit when the reproduction ran |

The commit identifies the rules. A tag does not.

### `files`

A list with one object per file. No path appears twice.

| Key | Value |
|---|---|
| `path` | relative to the project root, with `/` |
| `checksum` | `sha256:` followed by 64 lowercase hexadecimal digits |
| `begin`, `end` | only for a file the project also writes: the exact text of the line that opens the reproduced part and of the line that closes it |

An entry without `begin` and `end` is a whole file: the reproduction wrote all of it. An entry with both is a reproduced part: the reproduction wrote the lines from `begin` to `end`, and the rest of the file is the project's.

### `carriers`

A list with one object per rule carrier.

| Key | Value |
|---|---|
| `kind` | what the carrier is, in the reproducing agent's own words: an instruction file, a file it refers to, a script a hook runs, a skill, and so on |
| `files` | the paths that make up the carrier. Each is listed in `files` |

### `parts`

A list with one object per mechanical part: a guard or a deterministic check.

| Key | Value |
|---|---|
| `name` | the part's name, as these rules name it ([conformance.md](conformance.md#the-parts-of-a-setup)) |
| `runner` | the command that runs the part, as a list: the program and any arguments it needs before the entry file |
| `entry` | the path of the file the runner runs. It is listed in `files` |

A part is run as its `runner`, then its `entry`, then the part's own arguments ([conformance.md](conformance.md)).

### `enforcement`

A list with one object per rule that may be enforced mechanically. These rules are listed in [reproduction.md](reproduction.md).

| Key | Value |
|---|---|
| `rule` | the rule's name, as these rules give it |
| `by` | `mechanical` or `instruction`. A rule is `mechanical` only when its part passed every case and acting through its connector gave the expected results ([reproduction.md](reproduction.md)). Otherwise it is `instruction` |
| `part` | only when `by` is `mechanical`: the `name` of the part in `parts` that enforces it |

Every other rule reaches agents as an instruction and is not listed.

### Valid records

A record is valid when its keys and values follow everything stated under [The format](#the-format). Whether the files it lists still match their checksums does not bear on whether the record is valid.

Its copy of the settings is checked against the format in [settings.md](settings.md#the-format) without looking at the file system. Whether a path exists, or is a file or a folder, does not bear on whether the record is valid either.

Among the errors: an unknown key; a commit of 39 digits; a checksum without `sha256:`; a path listed twice in `files`; a carrier file that is not listed in `files`; a `mechanical` entry without a part.

## Checksums

To compute the checksum of a listed file:

1. Read the file's bytes and replace every CR LF pair with LF.
2. For a whole file, take all the bytes.
3. For a reproduced part, split the bytes into lines at LF. The line equal to `begin` and the line equal to `end` each occur exactly once in the file, `begin` first. Take the bytes from the start of the `begin` line to the end of the `end` line, with the `end` line's LF when it has one.
4. The checksum is `sha256:` followed by the SHA-256 digest of the bytes taken, in lowercase hexadecimal.

If the `begin` line or the `end` line is missing, occurs more than once, or the `end` line comes first, the reproduced part cannot be found. That is an error, not a mismatch.

A file has at most one entry, so at most one reproduced part. A file the project also writes can hold a reproduced part only if it can hold those two lines. Otherwise a reproduction writes it whole or does not write it.

Examples:

- An empty whole file has `sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- A whole file holding `a` CR LF `b` CR LF and one holding `a` LF `b` LF both have `sha256:911169ddaaf146aff539f58c26c489af3b892dff0fe283c1c264c65ae5aa59a2`.
- A reproduced part made of the lines `<!-- plumbline:begin -->`, `rule one`, `<!-- plumbline:end -->`, each ending in LF, has `sha256:0feea6f5b44d05e5c486ab443fce6ba01ec0951d9ee6c24d79a907c3758e9f67`, whatever project lines come before and after it. With `rule two` in place of `rule one` it has `sha256:372194c54600515e210c907b2e0b3ffc3381da531960057b83ac9ae667b1f878`.
- A reproduced part whose `begin` line occurs twice, or whose `end` line is missing, is an error.

## The same settings

The settings in the record and the settings file are the same when every layer has the same set of paths and `not_in_git` names the same set of layers. Order and formatting do not count.

Examples: `["src", "tests"]` and `["tests", "src"]` for `impl` are the same. Adding a path, or adding a layer to `not_in_git`, is not.

## What always holds

- Only a reproduction writes the record, and it replaces it whole.
- Right after a reproduction, every listed file exists and its checksum matches.
- No path is listed twice in `files`. Every path in `carriers`, and every `entry` in `parts`, is listed in `files`.
- Every `mechanical` entry in `enforcement` names a part in `parts`.
- The record holds nothing from a layer kept out of git. Its copy of the settings holds only paths and layer names.
- The record holds no copy of the rules.
