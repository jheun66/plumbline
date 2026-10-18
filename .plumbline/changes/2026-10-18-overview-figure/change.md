---
state: closed
diagnosis: design
---

# The order of steps in the overview's reproduction figure

## Asked

The verifier of [the M3 change](../2026-10-18-m3/) noted, outside its findings, that the figure "Reproducing a setup" in overview §3 writes the guards and checks before it adds the layers kept out of git to `.git/info/exclude`, while reproduction §2 does the reverse.

## Diagnosis

`design`: the overview's figure says otherwise than reproduction §2. Impl does not hold the figure; the rules already follow reproduction §2.

## Opened at

9601a9ba647c7dbd03c24da5e9fb5c550168027d

## Tasks

1. overview §3: the figure's steps in the order of reproduction §2.

## Wording fixes

- overview §3, the figure "Reproducing a setup": document templates, then the exclusions, then guards and checks, aligned to reproduction §2, steps 3 to 5.

## How the result was confirmed

The figure was rendered and checked: no overlapping or cut-off text, and its steps follow reproduction §2. `validate gate` passed.

## Commits
