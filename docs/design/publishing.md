# Public documents

## 1. Responsibilities

- Says what the plumbline repository's README and license hold.

## 2. Public interface

### The README

It is written in English. It holds:

- What plumbline is: a way of developing in three layers, intent, design and impl, written as rules; an AI reads the rules and reproduces a setup in a project.
- How to use it in a project: pick a version of the rules (a tag or a commit); keep a copy of that version outside the project; in the project, tell the AI to reproduce from this repository at that version. The first time, the AI writes intent and the module map with the user, then reproduces.
- What a reproduction makes: the three roles (lead, implementer, verifier), the role guard's two blocks, validate run on request, the template, the setup record.
- How this repository is laid out: where the rules, the conformance cases, the design and the license are.
- The license's name.

### The license

- MIT-0.
- Copyright notice: Jonghyeok Eun, 2026.

## 3. Flow

None.

## 4. Invariants and contracts

- The README says only what is actually in the current commit.
- The README never points to intent or copies its content.

## 5. Decisions and reasons

- The README is in English, for people who visit the public repository.
- The license is MIT-0. A reproduction carries sentences of the rules into each project's files, so the license must not ask for a copyright notice on those copies.

## 6. Verification criteria

- Every file and folder the README mentions is in the current commit.
- The README holds the five items above.
- The license holds the MIT-0 text and the copyright notice above.

## 7. Out of scope

None.
