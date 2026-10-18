---
result: clean
---

# Verify: 2026-10-18-overview-figure

Checked: `docs/design/overview.md`, section 3, "Reproducing a setup", its figure. Compared with impl and with the history of the design and impl locations since the start commit, 9601a9b.

## Findings

None.

The figure now lists the reproducing agent's steps in this order: write the rule carriers, write the document templates, add layers not in git to `.git/info/exclude`, write the guards and checks, run every conformance case, check each connector, write the setup record, report to the user. Impl gives the reproduction steps in that order. The figure still agrees with the text under it in section 3, and with the flow in `docs/design/reproduction.md` section 3. The changed figure names no impl location.

## Diagnosis

The diagnosis `design` held.

- At the start commit, the figure put writing the guards and checks before adding layers not in git to `.git/info/exclude`. Impl put the exclusion first. Impl was right and the figure was wrong.
- The only change since the start commit is in this figure, in the design location. Impl (`rules`, `README.md`, `LICENSE`) did not change, and it follows the figure as it is now.
- Nothing changed outside the layers the change touched. The change also lists impl as touched, though nothing in impl changed. That is allowed: impl already followed the corrected figure.
