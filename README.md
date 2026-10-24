# plumbline

plumbline is a way of developing a project in three layers, written as rules: intent, which says what to build and why; design, which says how it is divided and what each part promises; and impl, which is built from the design. An AI reads the rules and reproduces, in a project, a setup for developing that way.

## Using it in a project

1. Pick a version of the rules: a tag of this repository, or a commit.
2. Keep a copy of this repository, at that version, outside the project.
3. In the project, tell the AI to reproduce the setup from this repository at that version.

The first time, the AI writes the project's intent and the design's module map with you, and then reproduces.

## What a reproduction makes

- Three roles. The lead talks with you and writes intent and design. The implementer builds impl from the design. The verifier checks what changed once a change is done.
- The role guard, which blocks two things: the implementer or the verifier reading intent, and the implementer writing design.
- validate, which checks the whole project when you ask.
- The template that the project's design documents follow.
- The setup record, which names the rules the setup was made from and the files the reproduction wrote.

## How this repository is laid out

| Where | What |
|---|---|
| `rules/` | the rules. An AI starts at `rules/README.md` |
| `rules/cases/` | the conformance cases of the rules |
| `docs/design/` | plumbline's design |
| `LICENSE` | the license |

## License

MIT-0. The text is in [LICENSE](LICENSE).
