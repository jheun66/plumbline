# Layers

## The three layers

| Layer | Says | Derived from |
|---|---|---|
| intent | what to build and why: goals and scope, milestones, decisions and their reasons, open questions | nothing |
| design | how it is divided and what it promises: module responsibilities, public interfaces, invariants, decisions, verification criteria | intent only |
| impl | the implementation, and any other product built from the design, such as documents agents read | design only |

- Each layer is the truth at its own level of detail.
- Which layer a statement belongs to is decided by the "Says" column.
- Every design statement traces to intent. Every impl part traces to design.
- No lower layer contradicts an upper one.

## Read direction

| When writing | May read | Never reads |
|---|---|---|
| design | intent, design | impl |
| impl | design, impl | intent |

Writing intent is not restricted by this table.

## Change direction

- A change is made first in the highest layer it touches, then in each layer below.
- A lower layer changes alone only when the upper layer does not state the point being changed. What a layer states is given by the "Says" column.

## Gaps

A gap is a missing piece or an error in an upper layer, revealed while working on a lower one.

When a point comes up while working on a lower layer:

| The upper layer | Then |
|---|---|
| states it | follow it |
| states it wrongly | it is a gap |
| says nothing, and the point is one the upper layer would state by the "Says" column | it is a gap |
| says nothing, and the point is not one the upper layer would state | decide it in the lower layer |

On a gap:

1. Work on that point in the lower layer stops.
2. The change to the upper layer is proposed to the user.
3. When the user confirms it, the upper layer is changed first. Then work below continues.
4. When the user does not, the upper layer stays as it is, and the lower layer follows it.

The lower layer never settles a gap by itself.

A point the design decides because intent does not is a design-level decision. It needs the user's confirmation ([design-docs.md](design-docs.md)).

## Impl products that agents read

An impl product that agents read, such as prompts or rules, states rules only. Reasons, history and open questions stay in intent and design.

## Documents and front matter

- Intent and design documents are Markdown files (`.md`).
- Every Markdown file at the intent location ([settings.md](settings.md)) is an intent document.
- A document's front matter is the block at its very top: the file's first line is exactly `---`, and the block ends at the next line that is exactly `---`.
- Every line between those two is a `key: value` line. A key may appear more than once.
- Keys these rules do not define are ignored. The keys these rules define are `version` (below), and `basis`, `confirmed` and `pending` ([design-docs.md](design-docs.md)).

## Intent versions

- Every intent document has exactly one `version` line in its front matter: `version: V`.
- V is one or more non-negative integers joined by dots, such as `1`, `1.2`, `1.46`.
- Versions compare part by part, as integers, from the first part. A missing part counts as 0.

Examples:

- A file whose first line is `---`, followed by `version: 1.2` and a closing `---`, has version `1.2`.
- A file without front matter, or whose front matter has no `version` line or two of them, is an intent document without a valid version.
- `basis` and other keys in front matter are read without error.
- `1.10` is newer than `1.9`. `1.2` equals `1.2.0`. `2` is newer than `1.46`.
