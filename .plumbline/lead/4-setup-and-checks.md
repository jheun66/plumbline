# plumbline: rules for the lead (4 of 4): the setup and its checks

## The setup

- The setup was reproduced from the plumbline rules at the commit the setup record `.plumbline/setup-record.json` names. Use the rules only to reproduce, and the rules repository only to fetch its tags (below). To reproduce, read the rules from a copy of the rules repository at that commit, kept outside the project.
- Reproduce again when the project moves to another rules commit, when its settings change, or when the user asks.
- Reproduced files and reproduced parts are never edited by hand: every file the setup record lists, and in a file it lists with `begin` and `end` lines, the lines from `begin` to `end`. The setup changes only by changing the rules or the settings and reproducing again.
- Run every command below from the project root.

## status

- Run it with `python3 -B .plumbline/parts/status.py < /dev/null`.
- At the start of every session, before anything else, run it with empty standard input, and tell the user the state in a few lines, in the project's own words, before acting on the user's request.
- When the user asks for the state or about the rules, fetch the tags of the rules repository the setup record names when the network is available, and run status with them on standard input: `git ls-remote --tags https://github.com/jheun66/plumbline | python3 -B .plumbline/parts/status.py`.
- Its lines: `invalid` (a file without its form), `milestone` or `milestone-unknown`, `rules` or `rules-unknown`, `newer-rules`, `rules-up-to-date` or `newer-rules-not-checked`, `settings-changed` (the settings differ from those of the reproduction), `change` (each open or closed change; `current` marks the current one), `gap` (each proposed gap item), `skip` or `missing-layer`, `stale` (a design document whose intent basis is behind).

## validate

- Run it with `python3 -B .plumbline/parts/validate.py report` or `python3 -B .plumbline/parts/validate.py gate`. In `report` mode it only reports. In `gate` mode it blocks, with exit status 3, when it gives a problem line; `skip` lines never block. Exit status 0 is a pass; any other status is an environment error.
- When you end a turn, a hook runs `validate` in `report` mode. When it gives a problem line, the hook gives you its lines and lets you go on once. Tell the user the problems it reports, in the project's own words, without stopping on them.
- Before closing a change, run it in `gate` mode. Never close a change while it blocks.
- The project's CI, the GitHub Actions workflow `.github/workflows/plumbline-validate.yml`, runs it in `gate` mode on every push and pull request, and fails when it blocks or gives an error.

## verify

- Once a change is closed, hand its check to a fresh verifier with the hand-off of part 1, started with the Agent tool as `subagent_type` `verifier`.
- Read `verify.md` and tell the user the findings. For each finding, open a follow-up change or record the user's decision not to act on it with its date, linking the changes both ways (part 3).
- Archive the change only then, and only once the change's work is committed and its commits are listed in `change.md`. When the work is not committed yet, ask the user to commit it first.

## Guards

Hooks run two guards before your file tools act: before Write, Edit and NotebookEdit, and, for the role guard, before Read and Grep too.

- The gap guard enforces: within the current change, while a gap item is `proposed`, no layer below its layer is edited. When it blocks a write, tell the user which gap item must be answered. Never write a blocked file another way.
- The role table is enforced by instruction only: keep to your row of the role table yourself, and each implementer and verifier keeps to its own. The role guard still runs: it blocks a read or a write outside your row, and a read or search of a folder that contains a path you may not read, such as the project root, which contains impl. Search with a path that contains no impl location. When it blocks a read or a write, never do it another way. When the work needed that read or write, tell the user.
- When a guard reports an environment error, tell the user. The action went ahead.
- Changes a hook cannot see, such as files a shell command reads or writes, are not guarded. The rules hold for them all the same.
