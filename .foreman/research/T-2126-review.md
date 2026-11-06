## Verdict
Changes needed. The new exam code works as tested. But adding two kinds to `fmexam.KINDS` changes an existing Genesis exam in fmgenesis.py, which this diff doesn't touch. I could not run anything, so every finding comes from reading the code.

## lens: intent, adversary, edge, operator, maintainer

- MEDIUM — plugin/lib/fmgenesis.py:863 (caused by fmexam.py:21) — Growing `KINDS` from 11 to 13 changes the exam's meaning. `_ask` picks each G-scenario's planted defect as `fmexam.KINDS[h % len(fmexam.KINDS)]`. The modulus goes from 11 to 13, so most existing G-scenario ids now get a different defect. Earlier `draft-*` scores in exam.jsonl, such as `draft-genesis`, `draft-plain` and `draft-oracle`, are no longer comparable with new runs. About 2 in 13 G-scenarios now draw `clean` or `rank`. `_misses` (fmgenesis.py:883) requires a §2 capability whose kinds include that defect. `KIND_WORDS` (fmgenesis.py:674-677) has no pattern for either, and its `none` pattern matches "clean repo", not `clean`. A draft that falls back to word-mapping therefore cannot close those scenarios, and a `clean` G-scenario has no planted defect to name at all. The CHILD prompt (fmgenesis.py:682) also still says `"none" is a clean repo`, which now collides with the `clean` kind. Fix: keep `_ask` on a frozen 11-kind tuple, such as `GEN_DEFECTS = KINDS[:11]`, or exclude `clean` and `rank`. Then add `KIND_WORDS` entries and reword the CHILD prompt if you want the new kinds in the genesis exam. Reproducer: `fmgenesis._ask(s)[2]` for any fixed id before and after the change. Confidence: high on the reshuffle, medium on the unmappable-kinds effect.

- LOW — plugin/lib/fmexam.py:911-923 — `summary()` ignores `rank_keyed` and `rank_hit`. An arm that finds all three rank defects but names the vuln last scores "3/3 found" and is silently not closed. The score row never says rank order was the reason. Fix: add `if r.get("rank_keyed"): parts.append(f"{r['rank_hit']}/{r['rank_keyed']} ranked")`.

- LOW — plugin/lib/fmexam.py:781-782 — `_in_order` finds each defect's index with `next(...)` over every finding. One finding that matches both the vuln and a lower tier gives equal indexes, and `max(a) < min(b)` then fails. This can happen with a combined symbol such as `query, clamp`. It is a false negative, so it is only worth a comment or a test.

## Acceptance criteria
- `fm exam gen --author child` makes none, clean and rank scenarios with a held-out third, and the oracle closes each: met. `test_initiative_kinds_none_rank_clean` (test_exam.py:209-232) covers gen, check, oracle, empty and the order logic. The held-out third comes from `draw`'s `(n+1)//3` rule at fmexam.py:341. The test uses `--per-kind 3`, which draws one held-out scenario per kind. Not run here.

## Implicit decisions
- `gap` is `label` when the child plants `clamp`, else `clamp`. It compares against the template key, which is correct because `_author` returns `function=fn`.
- The child's `request` is discarded for `none` and `rank`, because `REQUESTS[kind]` is empty.
- `clean` is never child-authored.
- Rank ordering is strict: every tier-1 index must be below every tier-2 index.
- Keys without a `rank` field grade as before.
- `_author`'s dedent heuristic assumes Python openers end in `:`. A trailing comment such as `if x:  # c` gets dedented and is dropped as an IndentationError. That is safe, because `_authored` drops the scenario.

## Not checked
- I ran no tests and no real child author. I did not check the finders 16/18 figure or the s31-006 run. I did not read the site or genesis.js.

Noticed: plugin/tests/test_genesis.py:1325 slices `fmexam.KINDS[i::3]`, so the genesis test's capability sets shift with every kind added. Pin it to an explicit list.
