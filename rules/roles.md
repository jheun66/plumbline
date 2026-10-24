# Roles

The order of work is in [change.md](change.md). How the role guard is connected, and how each role receives its rules, are in [reproduction.md](reproduction.md).

## The three roles

| Role | Does | Reads | Writes |
|---|---|---|---|
| lead | talks with the user; writes intent and design; diagnoses; starts the implementer and the verifier; reproduces | intent, design, the settings file, the work note; when reproducing, plumbline's rules | intent, design, the settings file, the work note, `.git/info/exclude`, the project parts of the template and of carrier files; when reproducing, the setup files and the setup record |
| implementer | builds the design sections it is handed into impl; answers questions about the code | design, impl, the settings file | impl |
| verifier | checks what changed once a change is done ([change.md](change.md#what-the-verifier-checks)) | design, impl, the settings file | nothing |

- No role reads or writes beyond its row. The lead never reads impl. The implementer and the verifier never read intent. The implementer never writes design. The verifier writes nothing.
- A project file that belongs to no layer may be read by every role.
- When a project file that belongs to no layer must be written, such as a git ignore list that impl needs, the lead asks the user which layer to add its path to, and adds the path to that layer's locations in the settings file. The setup is then reproduced again ([layers.md](layers.md#when-settings-are-decided)), and the role that writes that layer writes the file.
- The setup files are the files a reproduction writes ([reproduction.md](reproduction.md)). The work note is in [change.md](change.md#the-work-note).

## Which role an AI plays

- Every AI plays exactly one role.
- An AI started as the implementer, with a hand-off that names the role `implementer`, is the implementer. An AI started as the verifier, with a hand-off that names the role `verifier`, is the verifier.
- Every other AI is the lead.

## Starting the implementer and the verifier

- The lead starts the implementer and the verifier as new AIs, without its own conversation, each with a hand-off ([Hand-offs](#hand-offs)).
- After a design fix, the lead hands the changed sections to the same implementer. It does not start a new one.
- The lead starts the verifier on a lighter model than its own.

## The implementer's work

1. It receives the hand-off, and reads the design documents and sections it names.
2. It builds them into impl. It builds only the design sections it is handed.
3. When it finds a gap, something missing or wrong in the design, it leaves that point unbuilt, chooses no way to build it, and goes on with the rest.
4. When done, it reports what it built and the gaps ([Reports](#reports)).
5. When the lead fixes the design and hands over the changed sections, it builds what it left.

- A point of a kind the design says ([layers.md](layers.md#the-three-layers)) that the design does not state, or states wrongly, is a gap. A point of another kind that the design does not state is decided in impl.
- The implementer never fills a gap in the design by itself.
- When its work needs a write to a project file that belongs to no layer, it stops that work and reports it to the lead.
- When the role guard blocks a read or a write, it stops that work and reports it to the lead. It never does the blocked read or write another way.

## Hand-offs

| To | Holds |
|---|---|
| the implementer, when started | the role name `implementer`; the design documents, and the sections in them, to build. For a question about the code, the question |
| the implementer, after a design fix | the design documents and sections that changed |
| the verifier | the role name `verifier`; the diagnosis; the layers touched; the commit checked out when the change started; the design documents and sections changed |
| the implementer, to fix a finding | the verifier's finding: its number, the design document and section, and how impl falls short |
| the verifier, after a finding is fixed | the numbers of the findings to check again |

- A hand-off holds only what is listed above, and what [reproduction.md](reproduction.md#how-carriers-reach-roles) adds: where the role's rules are, when no carrier brings them to it, and the check of the role guard ([reproduction.md](reproduction.md#checking-connectors)).
- A hand-off never holds content of intent.

## Reports

| From | Holds |
|---|---|
| the implementer | what it built. For each gap, the design document and section, and what is missing or wrong. For a question, the answer |
| the verifier | that there are no findings, or numbered findings: for each, the design document and section, and how impl falls short of it. And whether the diagnosis held |

- A report never copies impl content. It may name impl locations.

## The role guard

Just before an AI reads or writes a file, the role guard checks the action. It blocks these two, and nothing else:

1. The implementer or the verifier reads a path that belongs to intent. Searching a folder that contains a path that belongs to intent counts as reading it.
2. The implementer writes a path that belongs to design: editing, creating or removing it.

- When it blocks, the AI is told in plain words what was blocked and why.
- When the role guard cannot run, because there is no runner, or the settings file is missing or does not have its form, the AI is told of an environment error, and nothing is blocked.
- Everything else in the table above is kept by instruction.

What the lead does:

- When the implementer or the verifier reports being blocked, the lead looks at what that work needed. When it was something missing from the design, it is handled as a gap ([change.md](change.md#steps)).
- On an environment error, the lead tells the user in plain words what is broken and how to fix it: install the runner, fix the settings, or reproduce again.

### The part

The role guard is a mechanical part ([conformance.md](conformance.md)).

- Its name is `role-guard`.
- **Arguments**: the role, `lead`, `implementer` or `verifier`; then the action, `read` or `write`; then the paths the action touches, one or more. A search is given as a `read` of the folders it searches.
- **Standard input**: empty.
- It reads the settings file ([layers.md](layers.md#the-settings-file)), and nothing else.

How a path is taken:

- A path is relative to the project root, or absolute. Its names are separated by `/`.
- Empty names and `.` names are dropped. A `..` name removes the name before it.
- An absolute path is compared, name by name as text, with the working directory as the system reports it. Symbolic links are not followed.
- A path that, so taken, lies outside the project root, and a path that is `.git` or lies inside it, is never blocked.
- The project root itself is written `.`.

When a path is blocked:

- The role is `implementer` or `verifier`, the action is `read`, and the path belongs to intent, or a location of intent lies inside the path, or the path is the project root ([layers.md](layers.md#which-layer-a-path-belongs-to)).
- The role is `implementer`, the action is `write`, and the path belongs to design.

Whether a path exists, and whether it is a file or a folder, does not matter.

**Verdict**:

- `error` when there are fewer than three arguments, when the role or the action is not one of the names above, or when the settings file is missing or does not have its form.
- Otherwise, `block` when at least one path is blocked, and `pass` when none is.

**Output**: for each blocked path, in the order of the arguments, one line: `block`, the path, the role and the action, separated by tabs. The path is written relative to the project root, as taken above. Nothing else is written to standard output.

Examples, with intent at `docs/intent.md`, design at `docs/design` and impl at `src`, and fields separated by spaces here for reading:

- `implementer read docs/intent.md` gives `block docs/intent.md implementer read`. So does `implementer read ./docs//intent.md`.
- `implementer read .` gives `block . implementer read`. `implementer read docs` gives `block docs implementer read`. `implementer read src` gives `pass`.
- `implementer read src/a.rs docs/intent.md` gives only `block docs/intent.md implementer read`.
- `implementer write docs/design/new.md` gives `block docs/design/new.md implementer write`, whether or not the file exists.
- `lead read docs/intent.md`, `lead write docs/design/a.md`, `verifier read src/main.rs`, `implementer read ../elsewhere/a.md` and `implementer read .git/HEAD` give `pass`.
- `builder read docs/intent.md` and `implementer read` give `error`.

The cases of `role-guard` are in [cases/role-guard.json](cases/role-guard.json) ([conformance.md](conformance.md#which-parts-have-cases)).

## What always holds

- Every AI plays exactly one role.
- The implementer and the verifier never read intent. The role guard enforces it where the setup record gives `intent-read` as `mechanical` ([setup-record.md](setup-record.md#enforcement)).
- The implementer never writes design. The role guard enforces it where the setup record gives `design-write` as `mechanical`.
- The lead never reads impl. The verifier writes nothing. These, and the rest of the table above, are kept by instruction.
- The implementer never fills a gap in the design by itself.
- The role guard never blocks when it cannot run.
