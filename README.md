# plumbline

plumbline is a set of rules for developing a project in three layers: intent, design and impl. With these rules, an agent helps the user write the project's intent and its design's module map, and then reproduces the project's setup: rule carriers that give each role its rules, a document template, guards, checks, and a setup record.

## Using plumbline in a project

1. Give an agent the rules at one commit of this repository, in a copy of the repository kept outside the project.
2. The agent starts at [rules/README.md](rules/README.md), the top-level README of the folder `rules`, and works with the user from there.

Nothing is installed. The setup is written into the project, and the project runs without the rules. Its setup record, `.plumbline/setup-record.json`, names the rules repository and the commit the setup was reproduced from.

## What this repository holds

| Where | What |
|---|---|
| `rules/` | the rules, and their conformance cases in `rules/cases/` |
| `docs/design/` | plumbline's design |
| `.plumbline/setup-record.json`, the files it lists, and `.plumbline/settings.json` | the setup this repository itself uses, reproduced from the rules and those settings |
| `LICENSE` | the license |

## Releases

A release is a git tag whose name is a version, such as `v1.0`. It names one commit of this repository. A project records the commit in its setup record.

## License

MIT-0. The text is in [LICENSE](LICENSE).
