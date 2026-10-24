# Conformance cases

## 1. Responsibilities

- Defines the contract every mechanical part keeps (input, verdict, output).
- Defines the form of conformance cases and how to run them.
- Says what a connector, which connects a part to an AI's hooks, does.

Each part's arguments, output lines and list of cases are defined by the module that defines the part (the role guard in Roles, and Validate).

## 2. Public interface

### The contract of a part

The mechanical parts are the role guard (`role-guard`) and validate (`validate`). Every one keeps this contract.

**Running it**: the runner, then the entry file, then the part's arguments.

**Input**

- The working directory is the project root. A part finds the project only through it, never through where its own files are.
- The arguments and standard input are defined by the part's module. Either may be empty.
- The result depends only on the files in the working directory (a git repository there included), the arguments and standard input. It does not use the network.

**Verdict**: given by the exit status.

| Exit status | Verdict |
|---|---|
| 0 | `pass` |
| 3 | `block` |
| anything else, or no exit within the time limit | `error` |

- `error` is an environment error: the part could not give `pass` or `block`. A part that finds such a problem exits with a status other than 0 and 3 and says what in standard error.
- `error` is never treated as `block`.

**Output**

- Standard output holds the result lines. Each line is a code and its fields, separated by single tabs. A field holds no tab or line break. The codes, fields and order of lines are defined by the part's module.
- Standard error is free text for people. Nothing compares it.

### Connectors

A connector connects a part to an AI tool's hooks. It differs from one AI tool to another, so the rules do not fix it; the reproducing AI writes it.

- A connector only translates: what the AI tool gives, into the part's arguments and standard input; and the part's verdict, into the form the AI tool understands. It makes no judgment of its own.
- It blocks only on `block`. On `error` it reports an environment error and lets the AI go on.
- Cases run the part directly, not through a connector. A connector is checked at reproduction by acting through it (Reproduction).

### The form of a case

A case is one JSON object. In this example, the part, its argument and its output code are made up for illustration: a part that blocks when the file named by its argument does not exist.

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
| `input.files` | the files of the working directory: an object from path to content. A path is relative, separated by `/` |
| `input.git` | optional. When present, the working directory is a git repository in which git tracks exactly these paths. Each is in `input.files`. When absent, the working directory is inside no git repository |
| `input.args` | optional. The arguments, as a list. Empty when absent |
| `input.stdin` | optional. The standard input. Empty when absent |
| `expect.verdict` | `pass`, `block` or `error` |
| `expect.output` | optional. The result lines the part must write, in order. When absent, the output is not compared. An empty list means there must be no result line |

Any other key makes the case wrong.

- A case expecting `block` is a must-block case; a case expecting `pass` is a must-pass case.
- A case holds every file it needs, the settings file included. It uses no file of the project it runs in, other than the part's own.

### Running a case

1. Make a new, empty directory that is inside no git repository.
2. When the case has `input.git`, make the directory a git repository.
3. Write every file in `input.files`, making folders as needed. A path under `.git/` is written into the repository made in step 2.
4. When the case has `input.git`, make git track exactly those paths.
5. Run the part: the runner and entry file the reproduction chose, then `input.args`. The working directory is the case's directory, the standard input is `input.stdin`, and there is no network. Stop it when it has not ended after 60 seconds.
6. Take the verdict from the exit status. Turn CR LF into LF in standard output and split it into lines. A final LF does not start an empty line.
7. The case passes when the verdict equals `expect.verdict` and, when the case has `expect.output`, the lines equal it, in order.
8. Remove the directory.

- The entry file is the one in the project being reproduced, found from that project's root.
- When the runner cannot be started at all, it is reported as an environment error that names the runner.

### Which parts have cases

- Every mechanical part has cases. A part that can block has at least one must-block case and one must-pass case.
- The module that defines a part lists all its cases in its verification criteria, as inputs and expected results.
- Work that needs judgment (diagnosis, the verifier's check, status) has no cases.

## 3. Flow

1. The reproduction writes the parts.
2. It reads the cases from the rules at the commit it reproduces, and runs every one in the project.
3. When a case fails, it fixes the part and runs every case again.
4. When all pass, the reproduction goes on.

## 4. Invariants and contracts

- A reproduction ends only when every case of every part passes.
- Cases are not copied into the project, and nothing used to run them is left there.
- The same case expects the same verdict and output in any project.

## 5. Decisions and reasons

- A case is a promise of input and expected result, so a part written in any programming language is judged by the same cases.
- The verdict is the exit status. Any language can give it, and a connector translates it easily.
- `error` is never treated as `block`, so that an environment problem that cannot be fixed does not block work without end.
- Cases do not go through connectors. Connectors differ between AI tools, so the same case cannot run through them.
- Cases are not left in the project. A part edited after reproduction is found by its checksum.

## 6. Verification criteria

This module has no cases of its own. Reproducing in another project shows that the cases of the role guard and validate run in this form and by these steps, and that a reproduction passes every case.

## 7. Out of scope

None.
