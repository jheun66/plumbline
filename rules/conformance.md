# Conformance

## Mechanical parts

A mechanical part is a guard or a deterministic check in a setup. Every mechanical part runs without an agent and keeps the contract below.

### Running a part

A part is run as its runner, then its entry file, then its arguments. The setup record gives the runner and the entry file ([setup-record.md](setup-record.md)).

### Input

- The working directory is the project root. The part finds the project only through it, never through where its own files are.
- Its arguments and its standard input, as the rules for the part define them. Either may be empty.
- Its result depends only on the files under the working directory (a git repository there included), its arguments and its standard input. It does not use the network.

### Verdict

The exit status gives the verdict:

| Exit status | Verdict |
|---|---|
| 0 | `pass` |
| 3 | `block` |
| anything else, or no exit within the time limit | `error` |

- `error` is an environment error: the part could not give `pass` or `block`. It crashed, its runner is missing, or it found a problem with its environment. A part that finds such a problem exits with a status other than 0 and 3 and says what in standard error.
- `error` is never treated as `block`.
- A part that never blocks gives `pass` whenever it ran.

### Output

- Standard output holds the part's result lines. Each line is a code followed by fields, all separated by single tab characters. A field never holds a tab or a line break. The rules for the part define the codes, the fields and the order of the lines.
- Standard error is free text for people. Nothing compares it.

## Connectors

- A connector connects a mechanical part to an agent's hooks or to CI. The reproducing agent writes it ([carriers.md](carriers.md)).
- A connector only translates: what the agent or CI gives, into the part's arguments and standard input; and the part's verdict, into the form the agent or CI understands. It makes no judgment of its own.
- A connector to an agent blocks only on `block`. On `error` it reports an environment error and lets the agent go on.
- Cases do not run through a connector. A connector to an agent is checked at reproduction by acting through it ([reproduction.md](reproduction.md)).

## Conformance cases

### The format

A case is a JSON object. In this one, the part, its argument and its output code are made up for illustration: a part that blocks when the file named by its argument does not exist.

```json
{
  "id": "example-missing-file-blocks",
  "part": "example",
  "input": {
    "files": {
      "notes/a.md": "hello\n"
    },
    "git": ["notes/a.md"],
    "args": ["notes/b.md"],
    "stdin": ""
  },
  "expect": {
    "verdict": "block",
    "output": ["missing\tnotes/b.md"]
  }
}
```

| Key | Value |
|---|---|
| `id` | the case's name, unique among all cases. A failing case is reported by it |
| `part` | the name of the part the case is for, as these rules name the part |
| `input.files` | the files of the working directory: an object from path to content. A path is relative, with `/` |
| `input.git` | optional. When present, the working directory is a git repository in which git tracks exactly these paths. Each is in `input.files`. When absent, the working directory is not inside any git repository |
| `input.args` | optional. The arguments, a list of strings. Empty when absent |
| `input.stdin` | optional. The standard input, a string. Empty when absent |
| `expect.verdict` | `pass`, `block` or `error` |
| `expect.output` | optional. The result lines the part must write, in order. When absent, the output is not compared. An empty list means the part writes no result line |

Any other key in a case, in its `input` or in its `expect` is an error.

- A case expecting `block` is a must-block case. A case expecting `pass` is a must-pass case.
- A case with `expect.output` also expects that output.
- A case carries every file it needs, project settings included. It uses no file of the project it runs in, other than the part's own.

### Running a case

1. Make a new, empty directory that is not inside any git repository.
2. If the case has `input.git`, make the directory a git repository.
3. Write every file in `input.files`, making folders as needed. A path under `.git/` is written into the repository made in step 2.
4. If the case has `input.git`, have git track exactly those paths.
5. Run the part: its runner and its entry file, as the setup gives them, then `input.args`. The working directory is the case's directory, the standard input is `input.stdin`, and there is no network. If the part has not exited after 10 seconds, stop it.
6. Take the verdict from the exit status. In standard output, turn CR LF into LF and split it into lines. A final LF does not start an empty line.
7. The case passes when the verdict equals `expect.verdict` and, if the case has `expect.output`, the lines equal it, in order.
8. Remove the directory.

- The entry file is the one in the project being reproduced, found from that project's root, not from the case's directory.
- When a part's runner cannot be started at all, the run is reported as an environment error that names the runner.

Examples:

- A case expecting `block` passes when the part exits with 3, and fails when it exits with 0 or with 1.
- A case expecting `error` passes when the part exits with 1, 2 or 127, and when it has not exited after 10 seconds.
- A case expecting `pass` with `expect.output` of `a` TAB `x` and `b` TAB `y`: fails when the part writes the same two lines in the other order; passes when it writes them with CR LF line ends; passes whatever it writes to standard error.
- A case without `expect.output` passes whatever the part writes to standard output. A case with an empty `expect.output` fails when the part writes a line.
- A case whose `input.git` names a path that is not in `input.files`, a case with an unknown key, and two cases with the same `id` are invalid.

### Which parts have cases

- Every mechanical part of a setup has cases. A part that can block has at least one must-block case and one must-pass case.
- The cases of a part are in the folder `cases/` of these rules, in one file named after the part with `.json` added. The file holds a JSON array whose items are the part's cases, all of them.
- Judgment checks have no cases.
- Cases run a part through the contract above, not through its connector.

### When cases run

- During a reproduction, in the project being reproduced, after the parts are written. The cases are read from the rules at the commit the reproduction uses.
- The reproduction is finished only when every case of every part passes. When a case fails, the reproducing agent corrects the part and runs every case again.
- Cases are not copied into the project, and nothing used to run them is kept there.

## The parts of a setup

A setup has exactly the mechanical parts these rules define:

| Part | Defined in | Cases |
|---|---|---|
| `status` | [status.md](status.md) | [cases/status.json](cases/status.json) |
| `gap-guard` | [guards.md](guards.md) | [cases/gap-guard.json](cases/gap-guard.json) |

Its setup record's `parts` has one entry for each ([setup-record.md](setup-record.md#parts)).
