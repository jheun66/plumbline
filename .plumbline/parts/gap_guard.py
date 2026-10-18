"""gap-guard: blocks edits below a proposed gap item in the current change.

Arguments: the paths of the files a writing action will create, change or
remove. Standard input: empty.
"""

import sys

import plumbline_lib as lib

RANK = {"intent": 0, "design": 1, "impl": 2}


def main(paths):
    if not paths:
        lib.emit([], lib.PASS)

    change = lib.current_change_name()
    if change is None:
        lib.emit([], lib.PASS)

    if not lib.open_change(change):
        lib.fail("gap-guard: the current change %r does not exist, its change.md "
                 "does not have its form, or it is not open" % change)

    proposed = []
    for number, path in lib.gap_items(change):
        item = lib.parse_gap_item(path)
        if item is None:
            lib.fail("gap-guard: gap item %s does not have its form" % path)
        if item["state"] == "proposed":
            proposed.append((RANK[item["layer"]], number, item["layer"]))
    if not proposed:
        lib.emit([], lib.PASS)

    state, settings = lib.load_settings()
    if state != "ok":
        lib.fail("gap-guard: the settings file %s is %s" % (lib.SETTINGS_PATH, state))

    gap_rank, gap_number, gap_layer = min(proposed)
    root = lib.cwd_segments()
    lines = []
    for arg in paths:
        path = lib.project_path(arg, root)
        if path is None:
            continue
        layer = lib.layer_of(path, settings)
        if layer is None or RANK[layer] <= gap_rank:
            continue
        lines.append(["block", path, layer, change, str(gap_number), gap_layer])
    lib.emit(lines, lib.BLOCK if lines else lib.PASS)


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except lib.EnvError as exc:
        lib.fail("gap-guard: %s" % exc)
