**Verdict** — changes needed. Three correctness gaps in the injection path (displaced cards, wildcard deps, files outside the project). The rest is minor.

I didn't run any of this. Each finding below comes from reading the code, and I haven't confirmed the reproducers by execution.

**Findings**

1. MEDIUM — `plugin/lib/fmlib.py:202-205` with `plugin/lib/fmhooks.py:1181-1183` — `cards_for` cuts the list to two before the hook drops the cards already injected. A file importing `fastapi`, `pydantic` and `sqlalchemy` gets fastapi and pydantic on edit 1. Every later edit returns the same two, which are already marked, so the language card `python` and `sqlalchemy` never fire. Before this change, the first `.py` edit always injected `python`. The new test pins this ("they come before the language card"), and its check `assertNotIn("stack card python,")` is a weak substring match. Fix: pass the already-injected names into `cards_for` (or filter first), then take two. Confidence high.
   - file: `plugin/lib/fmlib.py`; line: 202; short: "Cap of two applied before the already-injected filter"; category: logic-error; verdict: CONFIRMED.

2. MEDIUM — `plugin/lib/fmlib.py:175-185` — `_dep_hit` compares dependency names with `==`, but 26 cards use `*` wildcards. Examples: `dep:@tauri-apps/plugin-*`, `@sveltejs/adapter-*`, `@vitejs/plugin-*`, `@codemirror/*`, `opentelemetry-*`. Detection supports globs at `fmlib.py:348`, so those cards are detected but never import-matched. Fix: use `fnmatch.fnmatchcase` when `*` is in the dep, and apply `_norm` as detection does. Confidence high.
   - file: `plugin/lib/fmlib.py`; line: 185; short: "Wildcard dep signals never match imports"; category: logic-error; verdict: CONFIRMED.

3. MEDIUM — `plugin/lib/fmlib.py:188-206` — `cards_for` has no inside-the-project check. `card_for` returns None when the path is under `../`; `_card_note` has no such guard. A scratch `/tmp/x.py` containing `import fastapi` now injects, marks and logs the card with file `../..`, which uses up that card's once-per-task slot. Fix: return `[]` when `os.path.relpath(path, p.root)` starts with `../`. Confidence high.
   - file: `plugin/lib/fmlib.py`; line: 191; short: "Out-of-project files now trigger import cards"; category: scope-leak; verdict: CONFIRMED.

4. LOW — `plugin/lib/fmmap.py:148` — `VERSION = 7` is not bumped even though the comment says to bump it "when build() changes". Existing `map.json` files have no `dep:` signals until HEAD changes, so the feature does nothing in the meantime. `test_edit_cards.py:126` (`assertFalse` on `dep:` signals) now passes only because its test repo has no dependencies. Fix: bump `VERSION`.

5. LOW — `plugin/lib/fmcli.py:3715` — `ledger_tail(p, 5000)` silently misses cards from a long task, or a task audited late. `fm lib stats` has the same limit at 20000. Fix: read `cards.json[b.id]`, which is the per-task marker, and skip names starting with `:`.

6. LOW — `plugin/lib/fmlib.py:135-137` — the alias `"google": "protobuf"` fires on any `google.*` import (cloud, auth) when the project depends on protobuf. Go import paths are not lowercased while deps are.

7. LOW — `plugin/lib/fmhooks.py:1179` — MultiEdit's `edits[].new_string` is never read. The CLI help text for `fm lib` (`fmcli.py:4276`) omits `stats`.

**Acceptance criteria**
- Import-matched card injected beside the language card, once per task: met for the tested cases. Findings 1-3 are where it breaks.
- `fm audit prep` carries the checklists and `fm lib stats` lists injections per card: met. The `ledger_tail` window (finding 5) can silently truncate the data.

**Implicit decisions**
- At most 2 cards per edit, with import-matched cards ahead of the language card.
- First 64 KB of the file is read.
- Up to 40 dependency cards kept in the map.
- Up to 4 checklists, 1,200 characters each, in the audit brief.
- Python distribution-name alias table of 15 entries.
- Ledger windows of 5000 events (audit prep) and 20000 (stats).

**Not checked**
- Whether the tests pass.
- Measured per-edit cost: `map.json` is parsed twice and 64 KB of the file is read on every edit, with no before/after numbers.
- Card content quality.

**Intent gaps**
- The request also asks for each card's Verify at evidence time, usage stats in the pane, and bulk-grown cards for uncovered deps. None are in the diff or the acceptance criteria.
- `MASTER.md`, `fmcli.py`, `fmhooks.py` and the test file serve no named step, so the plan's steps need updating.

**Noticed:** `plugin/tests/test_edit_cards.py:126` asserts there are no `dep:` signals in the map, which contradicts this feature; reword it. Also: the Python distribution-to-import-name alias table is too small to cover common cases like `psycopg2-binary`.
