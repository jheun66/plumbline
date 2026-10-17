# Guards

A guard is a mechanical part ([conformance.md](conformance.md)). An agent's hook runs it, through a connector, before an action that writes files, and the guard lets the action through or blocks it.

## Every guard

| Item | What it is |
|---|---|
| Arguments | the paths of the files the action will create, change or remove (below) |
| Standard input | empty |
| Verdict | `block` when at least one path is blocked; `pass` when none is, and when there are no arguments; `error` when the guard cannot read what it needs |
| Output | one line per blocked path, in the order of the arguments; nothing when the verdict is `pass` |

- A guard blocks only with exit status 3, and only on its own rule.
- A guard blocks only while the state its rule names lasts. That state can always be ended by edits the guard does not block.
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
