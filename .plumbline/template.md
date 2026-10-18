---
confirmed: (Design-level — confirmed YYYY-MM-DD)
pending: (Design-level — pending)
figure: mermaid
---

<!-- plumbline:begin -->
A module document has the seven level-2 headings below, exactly and in this order, and no other level-2 heading. Level-3 headings and below are free. A section that does not apply still appears and says so.

1. The first section holds the responsibilities: what the module does and what it does not.
2. The second, the public interface: names, fields and contracts other modules or agents rely on.
3. The third, the flow: the main sequences.
4. The fourth, the invariants and contracts: conditions that always hold.
5. The fifth, the decisions and reasons: why it is this way, what was rejected. Every design-level decision of the module is written here, and nowhere else.
6. The sixth, the verification criteria: what must be shown for the module to be right; for a mechanical part, its conformance cases.
7. The seventh, what is out of scope: what a later milestone adds.

Basis lines: every design document, the design's README included, has front matter with one or more lines `basis: <intent document> <version>`: the path of an intent document from the project root, and that document's version when the design document was written or last checked against it. Its text also names the intent sections it is based on.

Markers: a design-level decision, one the design makes because intent does not, carries one of the two markers of this template's front matter. Until the user confirms it, it carries the `pending` text. Once the user confirms it, it carries the `confirmed` text with the date of the confirmation in place of `YYYY-MM-DD`. A decision that only restates intent carries no marker. A decision that settled a confirmed gap item at the design layer carries that gap item's date, and its line links to the change folder.
<!-- plumbline:end -->

## 1. Responsibilities

## 2. Public interface

## 3. Flow

## 4. Invariants and contracts

## 5. Decisions and reasons

## 6. Verification criteria

## 7. Out of scope
