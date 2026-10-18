# Guards

A guard is a mechanical part ([conformance.md](conformance.md)). An agent's hook runs it, through a connector, before an action that reads or writes files, and the guard lets the action through or blocks it.

A setup has two guards: the gap guard and the role guard.

## Every guard

| Item | What it is |
|---|---|
| Arguments | first the guard's own leading arguments, when its section names any; then the paths of the files the action touches (below) |
| Standard input | empty |
| Verdict | `block` when at least one path is blocked; `pass` when none is, and when there are no paths; `error` when the guard cannot read what it needs, or when its leading arguments are not what its section names |
| Output | one line per blocked path, in the order of the arguments; nothing when the verdict is `pass` |

- A guard blocks only with exit status 3, and only the actions its own rule forbids.
- A block never keeps an agent from stopping, or from the actions its rule allows.
- A guard that cannot read what it needs gives `error`, never `block`. Its connector reports it as an environment error and lets the agent go on ([conformance.md](conformance.md#connectors)).
- The same files and the same arguments always give the same verdict and the same lines.
- Changes a hook cannot see, such as files written by a shell command, are not guarded.

A guard's connector is written as [carriers.md](carriers.md#connectors) states.

### Paths given as arguments

- A path is relative to the project root, with `/`, or absolute.
- Empty segments and `.` segments are ignored. A `..` segment removes the segment before it.
- An absolute path is compared, segment by segment as text, with the working directory as the system reports it. Symbolic links are not followed.
- A path that lies outside the project root is in no layer. A path that reaches the project through a symbolic link lies outside the project root.

Examples, with the working directory at `/work/p`:

- `./src/main.rs`, `src//main.rs`, `docs/../src/main.rs` and `/work/p/src/main.rs` are all `src/main.rs`.
- `../elsewhere/main.rs` and `/work/other/main.rs` lie outside the project root.

## The gap guard

- The part's name is `gap-guard`. The rule it enforces is named `gap guard` ([reproduction.md](reproduction.md#mechanical-or-instruction)).
- It has no leading arguments. Its paths are those of the files a writing action will create, change or remove.
- It blocks only while a gap item is proposed, and that state can always be ended by edits it does not block.
- It reads the settings ([settings.md](settings.md)), `.plumbline/current-change`, and the gap items of the current change ([changes.md](changes.md)).

How it decides, in this order. It reads only what the step at hand needs:

1. When there are no arguments, it gives `pass`.
2. When there is no current change ([changes.md](changes.md#the-current-change)), every path passes.
3. When the current change does not exist, its `change.md` does not have the form [changes.md](changes.md#changemd) defines, or its state is not `open`, it gives `error`.
4. When a gap item of the current change does not have the form [changes.md](changes.md#gap-items) defines, it gives `error`.
5. When no gap item of the current change is `proposed`, every path passes.
6. When the settings file is missing or not valid ([settings.md](settings.md#the-format)), it gives `error`.
7. Otherwise, it takes the highest layer among the current change's `proposed` gap items. `intent` is above `design`. A path in a layer below that layer is blocked. A path in that layer or above, or in no layer, passes.

A path is in a layer when it equals one of that layer's paths in the settings, or lies under one.

The output line for a blocked path:

| Code | Fields |
|---|---|
| `block` | the path, relative to the project root; the path's layer; the current change; the number of the gap item; the gap item's layer |

The gap item named is the lowest-numbered `proposed` one at the highest layer.

The gap guard gives `error` only in steps 3, 4 and 6. A file it does not need for its verdict is not read, so a problem in that file gives no `error`.

Examples:

- With no arguments, it gives `pass` whatever the other files hold.
- With no current change, it gives `pass` even when the settings file is not valid.
- With an open current change whose `change.md` and gap items have the form, and none of whose gap items is `proposed`, it gives `pass` even when the settings file is not valid.

### What always holds

- The gap guard never blocks a path in no layer, nor a path in the gap item's layer or above.
- The gap guard never blocks because of a change other than the current one.
- The edits that end a block, answering the gap item or changing the current change, touch no layer, so the gap guard never blocks them.

### Conformance cases

The cases of `gap-guard` are in [cases/gap-guard.json](cases/gap-guard.json) ([conformance.md](conformance.md#which-parts-have-cases)).

## The role guard

- The part's name is `role-guard`. The rule it enforces is named `role table` ([roles.md](roles.md#the-role-table), [reproduction.md](reproduction.md#mechanical-or-instruction)).
- **Leading arguments**: the role of the agent that acts, `lead`, `implementer` or `verifier`; then the action, `read` or `write`.
- A read is an action that opens the content of a file or searches the content of files. Its paths are the files it opens, or the files and folders it searches. An action that only lists the names of files is not guarded.
- A write is an action that creates, changes or removes a file. Its paths are those files.
- It reads the settings ([settings.md](settings.md)), the setup record ([setup-record.md](setup-record.md)), the state of changes ([changes.md](changes.md)), and which paths git ignores, when the project root is a git repository. The project root is a git repository when it holds `.git`.

### The row of a path

Each path falls in the row of the role table given by the first line of this table that applies:

| # | The path | Row |
|---|---|---|
| 1 | lies outside the project root | `not-project` |
| 2 | is `.git/info/exclude` | `exclude` |
| 3 | is `.git`, or lies under it | `not-project` |
| 4 | lies in the intent, design or impl layer ([roles.md](roles.md#the-role-table)) | `intent`, `design` or `impl` |
| 5 | is `.plumbline/current-change` | `current-change` |
| 6 | is `verify.md` directly in a change folder, `.plumbline/changes/<name>/verify.md` | `verify-result` |
| 7 | is `.plumbline/changes`, or lies under it | `change-record` |
| 8 | is `.plumbline/settings.json` | `settings` |
| 9 | is a file of a carrier in the setup record's `carriers` | `carrier` |
| 10 | is `.plumbline/setup-record.json`, or another path in the setup record's `files` | `setup-file` |
| 11 | is ignored by git | `not-project` |
| 12 | anything else | `project-file` |

- A path is ignored by git when the project's own ignore rules ignore it: the ignore files in the repository and `.git/info/exclude`, read as git reads them. No other ignore rule counts, such as a user's global ignore file. A path git tracks is not ignored. When the project root is not a git repository, no path is ignored.
- The project root itself is a folder in no layer. It falls in row 12.

The cell of a role in each row, from [roles.md](roles.md#the-role-table):

| Row | `lead` | `implementer` | `verifier` |
|---|---|---|---|
| `intent` | read, write | — | — |
| `design` | read, write | read | read |
| `impl` | — | read, write | read |
| `verify-result` | read | — | read, write |
| `change-record` | read, write | — | — |
| `current-change` | read, write | — | — |
| `settings` | read, write | read | read |
| `carrier`, when the setup record lists the role among the carrier's `roles` | read, write | read | read |
| `carrier`, otherwise, and `setup-file` | read, write | — | — |
| `exclude` | read, write | — | — |
| `project-file` | read | read | read |
| `not-project` | read, write | read, write | read, write |

### How it decides

1. When its leading arguments are not a role and an action as above, it gives `error`.
2. When there are no paths, it gives `pass`, without reading anything.
3. When the settings file is missing or not valid ([settings.md](settings.md#the-format)), or the setup record is missing or not valid ([setup-record.md](setup-record.md#valid-records)), it gives `error`.
4. Then, for each path in turn:
   1. Take the path's row, and the role's cell in it.
   2. When the cell does not allow the action, the path is blocked.
   3. For the verifier, `verify-result` allows a read or a write only when the change, `.plumbline/changes/<name>/`, has a `change.md` with the form [changes.md](changes.md#changemd) defines and `state: closed`. Otherwise the path is blocked.
   4. For a read of a folder, a path that exists and is a folder, the path is also blocked when it contains one of these that the role's cell does not allow it to read: a path of a layer, a file of a carrier, `.plumbline/setup-record.json` or a path in its `files`, `.plumbline/current-change`, `.git/info/exclude`, or a change folder. A folder contains a path when the path lies under it, whether or not that path exists. The change folders are the folders that listing `.plumbline/changes/` finds directly under it. The project root is a folder like any other.

Paths are taken as [Paths given as arguments](#paths-given-as-arguments) states.

The output line for a blocked path:

| Code | Fields |
|---|---|
| `block` | the path, relative to the project root, or as given when it lies outside; the role; the action; the row |

- The project root is written `.`.
- For a folder blocked by step 4.4, the row is that of the first path it contains that the role may not read, in the order of the rows in [The row of a path](#the-row-of-a-path).

Examples, with fields separated by spaces here for reading, and impl at `src`:

- `lead read .` gives `block . lead read impl`: the project root contains `src`.
- `implementer read .plumbline` gives `block .plumbline implementer read current-change`.
- `implementer read .` gives `block . implementer read exclude`: the project root contains `.git/info/exclude`, whether or not that file exists.
- `verifier read .git` gives `block .git verifier read exclude`, though `.git` itself is in the row `not-project`.
- `implementer write src/a.rs README.md` gives `block README.md implementer write project-file` when `README.md` lies in no layer.
- With intent in `not_in_git` and listed in `.git/info/exclude`, `implementer read docs/intent.md` still gives the row `intent`.

### What always holds

- The role guard blocks a path exactly when the role table does not let that role do that action there, or when a folder it reads contains such a path.
- The role guard never blocks a path that is not a project file, except a read of a folder that contains one the role may not read.
- When two changes are closed and not yet archived, the verifier may write the verify result of either.

### Conformance cases

The cases of `role-guard` are in [cases/role-guard.json](cases/role-guard.json) ([conformance.md](conformance.md#which-parts-have-cases)).
