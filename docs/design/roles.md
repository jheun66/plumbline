# Roles

## 1. Responsibilities

- Says what the three roles (lead, implementer, verifier) do, and where each reads and writes.
- Defines the hand-offs to a role and the reports back.
- Says what the two mechanical blocks (the role guard) promise.

The order of work is in A change. How the role guard is built, and what each role is given, is in Reproduction.

## 2. Public interface

### The three roles

| Role | Does | Reads | Writes |
|---|---|---|---|
| lead | talks with the user; writes intent and design; diagnoses; starts the implementer and the verifier; reproduces | intent, design, settings, work note. When reproducing, plumbline's rules | intent, design, settings, work note, `.git/info/exclude`, the project parts of the template and of carrier files. When reproducing, the setup files and the setup record |
| implementer | builds the design sections it is given into impl; answers questions about the code | design, impl, settings | impl |
| verifier | checks what changed once a change is done | design, impl, settings | nothing |

- A project file that belongs to no layer may be read by anyone. When such a file must be written (for example, a git ignore list that impl needs), the lead asks the user which layer to add its path to, adds it to the settings, and then the role that writes that layer writes it.
- The verifier is started on a lighter model than the lead.

### Hand-offs

| To | Holds |
|---|---|
| implementer (when started) | the role name "implementer"; the design documents and sections to build. For a question about the code, the question |
| implementer (after a design fix) | the design documents and sections that changed |
| verifier | the role name "verifier"; the diagnosis; the layers touched; the commit checked out when the change started; the design documents and sections changed |
| implementer (to fix a finding) | the verifier's finding: its number, the design document and section, and how impl falls short |
| verifier (after a finding is fixed) | the numbers of the findings to check again |

A hand-off holds only what is listed above, and what Reproduction adds (where the role's rules are, the role guard check). It never holds content of intent.

### Reports

| From | Holds |
|---|---|
| implementer | what it built. For each gap, the design document and section, and what is missing or wrong. For a question, the answer |
| verifier | "no findings", or numbered findings: for each, the design document and section, and how impl falls short of it. And whether the diagnosis held |

- A report never copies impl content, since the lead does not read impl. It may name impl locations.

### The role guard

Just before an AI reads or writes a file, it is checked, and these two are blocked:

1. The implementer or the verifier reads a path that belongs to intent. Searching a folder that contains a path belonging to intent counts as reading.
2. The implementer writes a path that belongs to design (editing, creating or removing).

- When it blocks, it tells that AI in plain words what it blocked and why.
- When the part cannot run (no runner, the settings file missing or broken), it reports an environment error and does not block.
- When the implementer or the verifier reports being blocked, the lead looks at what that work needed. When it was something missing from the design, it is handled as a gap (A change).
- On an environment error, the lead tells the user in plain words what is broken and how to fix it (install the runner, fix the settings, reproduce again).

The part (it keeps the contract in Conformance cases):

- Its name is `role-guard`.
- Arguments: the role (`lead`, `implementer`, `verifier`), the action (`read`, `write`), then the paths the action touches. A search is given as a `read` of the folders it searches. Standard input is empty.
- A path is either relative to the project root or an absolute path inside the project. A path outside the project, and a path inside `.git/`, is never blocked.
- When at least one path is blocked, the verdict is `block`; otherwise `pass`. For each blocked path it writes one line, in the order of the arguments: `block`, the path, the role and the action, separated by tabs. The path is written relative to the project root.
- Fewer than three arguments (a role, an action, at least one path), or a role or action not among the names above, give `error`. So does a settings file that is missing or does not have its form.
- The project root is written `.`. Whether a path exists, or is a file or a folder, does not matter.

## 3. Flow

The implementer:

1. Receives the hand-off and reads the design documents and sections it names.
2. Builds impl.
3. When it finds something missing or wrong in the design, it leaves that point unbuilt and goes on with the rest.
4. When done, it reports what it built and the gaps.
5. When the lead fixes the design and hands over the changed sections, it builds what it left.

What the verifier checks is in A change.

## 4. Invariants and contracts

- Every AI plays exactly one role. An AI started as the implementer is the implementer, an AI started as the verifier is the verifier, and every other AI is the lead.
- The implementer and the verifier never read intent. The role guard enforces it.
- The implementer never writes design. The role guard enforces it.
- The lead never reads impl. The verifier writes nothing. These, and the rest of the table above, are kept by instruction.
- The implementer never fills a gap in the design by itself.

## 5. Decisions and reasons

- The implementer is a new AI that does not know the earlier conversation. An AI cannot act as if it does not know what it knows, so an instruction alone cannot make it build from the design only.
- After a design fix, the same implementer is handed the changed sections. All it knows is still the design, so the test holds, and starting a new one is saved.
- Only two things are blocked mechanically. Both keep "what the user read in the design is what gets built". The rest is kept by instruction.
- A search counts as reading. Its results can bring in intent content.
- When the part cannot run, it does not block. Blocking without end in a state that cannot be fixed stops all work.
- The verifier checks only what changed, so a lighter model is enough.

## 6. Verification criteria

Shown by the role guard's conformance cases (Conformance cases). Take the settings intent `docs/intent.md`, design `docs/design`, impl `src`.

Must-block cases:

- The implementer reads `docs/intent.md`.
- The verifier reads `docs/intent.md`.
- The implementer searches the project root.
- The implementer searches `docs`.
- The implementer edits `docs/design/a.md`.
- The implementer creates `docs/design/new.md`.
- The implementer reads `src/a.rs` and `docs/intent.md` together → only the line for `docs/intent.md`.

Must-pass cases:

- The implementer reads `docs/design/a.md`.
- The implementer writes `src/main.rs`.
- The implementer searches `src`.
- The verifier reads `src/main.rs`.
- The lead reads and writes `docs/intent.md`.
- The lead writes `docs/design/a.md`.
- The implementer reads a file outside the project.
- The implementer reads `.git/HEAD`.

Error cases:

- With no settings file, the implementer reads `docs/intent.md` → `error`. The connector reports an environment error and does not block.
- The role is `builder` → `error`.
- A role and an action but no path → `error`.

## 7. Out of scope

- Blocking files opened through shell commands.
