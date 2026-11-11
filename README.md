# plumbline

plumbline is a way of developing a project in three layers, written as rules: intent, which says what to build and why; design, which says how it is divided and what each part promises; and impl, which is built from the design. An AI reads the rules and reproduces, in a project, a setup for developing that way.

## Using it in a project

1. Pick a version of the rules: a tag of this repository, or a commit.
2. Keep a copy of this repository, at that version, outside the project.
3. In the project, tell the AI to reproduce the setup from this repository at that version.

The first time, you and the AI confirm the project's intent and the design's module map. Then you complete the layer locations, git exclusions and role settings, and agree on the workflow before reproduction. Changes to the settings or the rules commit require reproduction again.

## What a reproduction makes

- Instructions for each role. Only the lead is built in: it talks with you and writes intent and design. Your project defines the other roles, their duties, models, and read and write zones. Zones can select paths, file-name patterns and parts of files, and roles may share them.
- Your project's workflow, including how work and the five required checks are assigned. The project decides whether building and checking use different roles.
- The role guard. Every non-lead role is forbidden to read intent or its copies and to change design. Your project chooses whether to enforce read and write zones mechanically and whether shell commands receive no inspection, inspection of identifiable file actions, or cautious inspection that also blocks unresolved effects.
- validate, which checks the whole project when you ask.
- The template that the project's design documents follow.
- The setup record, which names the rules version, settings, generated files, and tested enforcement for each role and tool channel. It distinguishes mechanical coverage from rules that remain instructions. Requesting a guard does not prove that a tool enforces it.

The AI chooses runners, tool connectors and figure renderers for the available environment during reproduction. These are outputs of the [rules](rules/README.md); this repository does not distribute an executable or plugin.

## How this repository is laid out

| Where | What |
|---|---|
| `rules/` | the rules. An AI starts at `rules/README.md` |
| `rules/cases/` | the conformance cases of the rules |
| `docs/design/` | plumbline's design |
| `LICENSE` | the license |

## License

MIT-0. The text is in [LICENSE](LICENSE).
