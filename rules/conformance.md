# Conformance cases

## Mechanical parts

The mechanical parts are the role guard, `role-guard` ([roles.md](roles.md#the-role-guard)), and validate, `validate` ([validate.md](validate.md)). Every one keeps the contract below. Each part's arguments, output lines and cases are stated by the file that states the part.

### Running a part

A part is run as its runner, then its entry file, then the part's arguments. The setup record gives the runner and the entry file ([setup-record.md](setup-record.md#parts)).

### Input

- The working directory is the project root. A part finds the project only through it, never through where its own files are.
- Its arguments and its standard input are those its file states. Either may be empty.
- Its result depends only on the files in the working directory, a git repository there included, its arguments and its standard input. It does not use the network.

### Verdict

The exit status gives the verdict:

| Exit status | Verdict |
|---|---|
| 0 | `pass` |
| 3 | `block` |
| anything else, or no exit within the time limit | `error` |

- `error` is an environment error: the part could not give `pass` or `block`. A part that finds such a problem exits with a status other than 0 and 3, and says what in standard error.
- `error` is never treated as `block`.

### Output

- Standard output holds the result lines. Each line is a code and its fields, separated by single tabs. A field holds no tab and no line break. The codes, the fields and the order of the lines are stated by the part's file.
- Standard error is free text for people. Nothing compares it.

## Connectors

A connector connects a part to an AI tool's hooks. It differs from one AI tool to another; the reproducing AI writes it ([reproduction.md](reproduction.md#connectors)).

- A connector only translates: what the AI tool gives, into the part's arguments and standard input; and the part's verdict and lines, into the form the AI tool understands. It makes no judgment of its own.
- It blocks only on `block`. On `error`, it reports an environment error and lets the AI go on.
- Cases run the part directly, never through a connector. A connector is checked at reproduction by acting through it ([reproduction.md](reproduction.md#checking-connectors)).

## The form of a case

A case is one JSON object. In this example, the part, its argument and its output code are made up: a part that blocks when the file its argument names does not exist.

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

| Key | Holds |
|---|---|
| `id` | the case's name, unique among all cases. A failing case is reported by it |
| `part` | the name of the part the case is for |
| `input.files` | the files of the working directory: an object from path to content. A path is relative, with its names separated by `/` |
| `input.git` | optional. When present, the working directory is a git repository in which git tracks exactly these paths. Each is in `input.files`. When absent, the working directory is inside no git repository |
| `input.args` | optional. The arguments, as a list of texts. Empty when absent |
| `input.stdin` | optional. The standard input, as a text. Empty when absent |
| `expect.verdict` | `pass`, `block` or `error` |
| `expect.output` | optional. The result lines the part must write, in order. When absent, the output is not compared. An empty list means the part must write no result line |

Any other key, in the case, in its `input` or in its `expect`, makes the case wrong.

- A case expecting `block` is a must-block case; a case expecting `pass` is a must-pass case.
- A case holds every file it needs, the settings file included. It uses no file of the project it runs in, other than the part's own.

## Running a case

1. Make a new, empty directory that is inside no git repository.
2. When the case has `input.git`, make the directory a git repository.
3. Write every file in `input.files`, making folders as needed. A path under `.git/` is written into the repository made in step 2.
4. When the case has `input.git`, make git track exactly those paths.
5. Run the part: the runner and the entry file the reproduction chose, then `input.args`. The working directory is the case's directory, the standard input is `input.stdin`, and there is no network. Stop the part when it has not ended after 60 seconds.
6. Take the verdict from the exit status. Turn every CR LF into LF in standard output, and split it into lines. A final LF does not start an empty line.
7. The case passes when the verdict equals `expect.verdict` and, when the case has `expect.output`, the lines equal it, in order.
8. Remove the directory.

- The entry file is the one in the project being reproduced, found from that project's root.
- When the runner cannot be started at all, that is reported as an environment error that names the runner.

Examples:

- A case expecting `block` passes when the part exits with 3, and fails when it exits with 0 or 1.
- A case expecting `error` passes when the part exits with 1, 2 or 127, and when it has not ended after 60 seconds.
- A case with `expect.output` of `a` TAB `x` and `b` TAB `y` fails when the part writes the same two lines in the other order, and passes when it writes them with CR LF line ends, whatever it writes to standard error.

## Which parts have cases

- Every mechanical part has cases. A part that can block has at least one must-block case and one must-pass case.
- The cases of a part are in the file `cases/<name>.json` of these rules, where `<name>` is the part's name: a JSON array of all of that part's cases. They are [cases/role-guard.json](cases/role-guard.json) and [cases/validate.json](cases/validate.json).
- Work that needs judgment, such as diagnosis, the verifier's check and status, has no cases.

## When cases run

1. The reproduction writes the parts.
2. It reads the cases from these rules, at the commit it reproduces, and runs every one in the project.
3. When a case fails, it fixes the part and runs every case again.
4. When all pass, the reproduction goes on.

## What always holds

- A reproduction ends only when every case of every part passes.
- Cases are not copied into the project, and nothing used to run them is left there.
- The same case expects the same verdict and the same output in any project.
