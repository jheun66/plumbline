---
state: archived
diagnosis: design
---

# M3: plumbline applied to itself, and published

## Asked

The work of milestone M3 (intent 1.5, §11): plumbline set up by its own rules, validate run on plumbline's own design on the user's machine and in a clone without intent, the README, publishing on GitHub, and the first tag.

## Diagnosis

`design`: a milestone's work. The design does not yet describe the README that intent 1.5 §10 puts in impl.

## Opened at

353646a861c8160f11ffbe9f3500ce74fe85da57

## Tasks

1. Design README: `milestone` line to M3.
2. Design: the README and the license in plumbline's impl, what the README holds, and the rules folder as what a reproducing agent reads (design README, overview, reproduction). Design-level decisions are confirmed by the user.
3. Wording fixes reported by the first reproduction (below).
4. carriers §5: a known limit of the CI connector check at a first reproduction.
5. Settings: `LICENSE` added to the impl locations, so that a role may write it (gap-1); the setup is reproduced again (task 7).
6. An implementer aligns the rules and writes the README and the license.
7. Reproduce again at the new rules commit, in a new session, so the role table's connector check can run.
8. `validate gate` on the user's machine, in CI, and in a fresh clone without intent.
9. After archive: publish the repository and tag the first release, once the user confirms.

## Wording fixes

- design-docs §2, §4, §5, authoring §2 and settings §5: "the top-level README" and "the design's top-level README" became "the design README", as settings, status and changes already say; the term is added to the terms of the design README.
- carriers §2, validate at the end of a turn: the lead is given validate's lines only when there is a problem line, aligned to the lead's M2 row of the same section, which has the lead tell the user the problems validate reports. Reported by the first reproduction.
- reproduction §2: the reproducing agent reads only the rules and their conformance cases, aligned to overview §3.
- overview §4, §5 and the figure in §3, reproduction §3, §5 and §6: the folder `rules` is named as the part of impl that holds the rules and their cases, and the reproducing agent reads only the rules, aligned to overview §2, where impl also holds the README and the license. Reported by the implementer.
- overview §2: a release is a tag whose name is a version, aligned to status §2, where only tags that name a version count as releases. Reported by the implementer.
- design-docs §3: the figure's class for the design README is named after the term.

Also recorded: carriers §5, a known limit of the CI connector check, reported by the first reproduction.

## How the result was confirmed

- Implementers built the README, the license and the rule changes from the design; the role guard blocked none of their reads or writes.
- The setup was reproduced again at the rules commit 913743b, in a new session: all 216 conformance cases passed, and the role table, the gap guard, validate at the end of a turn and validate in CI are enforced mechanically; the role guard's connector was checked as the lead, the implementer and the verifier.
- `validate gate` passed on the user's machine with intent present, figures rendered.
- `validate gate` passed in a fresh clone of the GitHub repository, without intent (`skip layer intent`), and in CI on GitHub for 913743b and 9601a9b (`skip layer intent`, `skip figures mermaid`).

## Commits

Before the change was opened: 06eb6c8 (design) and d3a6a54 (rules), wording that validate took for impl paths; 353646a, plumbline's own setup from rules d3a6a54.

- 35c96b4: design, settings and this change record
- 913743b: impl: the README, the license and the rules
- 9601a9b: the setup reproduced from rules 913743b

## Verify result

`verify.md`: clean, no findings to take up. The diagnosis held.
