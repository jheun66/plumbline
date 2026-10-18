# verify

verify is the judgment check a fresh verifier makes on a closed change ([roles.md](roles.md)). It is not a mechanical part and has no conformance cases ([conformance.md](conformance.md)).

The verify result's file and front matter, and how its findings are taken up, are stated in [changes.md](changes.md#the-verify-result). Formats, basis lines, paths under impl locations and checksums are checked by `validate` ([validate.md](validate.md)), not by verify.

## Input

The lead's hand-off ([roles.md](roles.md#hand-off)) names:

- the change, by its name;
- its diagnosis: `impl`, `design` or `intent`;
- the layers the change touched;
- the commit the change's work started from: the start commit;
- the design sections the change touched: design documents and the sections in them.

## What the verifier reads

- The design sections it is handed, and whatever else of the design it needs to understand them.
- Impl.
- The history git keeps of the design and impl locations since the start commit.

For the check, it reads nothing else. It never reads intent or change records.

## What it looks for

In the design sections it is handed:

| What | A finding when |
|---|---|
| verification criteria | a criterion has no test in impl that shows it |
| invariants and contracts | impl does not keep one |
| public interface | something the design defines is not in impl, or impl has a public name, field or contract the design does not define |
| impl locations | the design names an impl location that is not a path, such as a test name or a function name |
| the diagnosis | the change's work does not fit its diagnosis (below) |

- The public interface is compared both ways.
- Only the design sections it is handed are checked.

## Whether the diagnosis held

The verifier compares the design and impl at the start commit with what they are now.

| Diagnosis | It held when |
|---|---|
| `impl` | at the start commit, impl did not follow the design sections, and now it does |
| `design` | the design sections changed, and impl now follows them |
| `intent` | the design documents that changed carry a newer intent basis, and impl now follows them |

In every case, no layer outside the layers the change touched was changed. When the work does not fit its diagnosis, that is a finding.

## Output

1. The verifier writes `verify.md` into the change's folder, `.plumbline/changes/<name>/`, in the form [changes.md](changes.md#the-verify-result) states: `result: clean` when there is no finding, `result: findings` otherwise.
2. Its body numbers the findings 1, 2, 3 and so on. Each finding names the design document and the section, and says what impl does not show or does otherwise, in terms of the design. It may name impl locations. It never quotes impl content.
3. Its body says whether the diagnosis held.
4. The verifier tells the lead it is done. It writes nothing else.

## What always holds

- The verifier never reads intent or change records.
- The verifier writes nothing but the `verify.md` of the change it was given.
- Every finding is named in terms of the design, and no impl content is quoted.
- A change whose work does not fit its diagnosis has a finding that says so.
