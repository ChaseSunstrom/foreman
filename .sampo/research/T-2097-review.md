**Verdict** — approve with nits. The scorecard logic is correct on the cases I traced. The real `fm genesis exam` path that feeds #13 has no test.

## lens: intent
- MEDIUM — plugin/lib/fmgenesis.py:1123-1124 — The scorecard has no coverage floor. A scenario that was never answered doesn't count against the agent, only against the 3-graded minimum. `fm exam run --limit 3` picks 3 held-out scenarios, so those 3 can pass a capability that has 18. — Optional: compare `graded` to the held-out count in the run's meta and show "graded/held", or document that the rate is over answered scenarios. — medium
- LOW — plugin/lib/fmgenesis.py:1123 — #13 is chosen by `re.search("genesis", name)`, not by number 13. A capability in another project's gen-0 whose name contains "genesis" would score on Foreman's `draft-genesis` lines. In the real gen-0, only #13 matches. — Match `n == 13 and "genesis" in name`, or say it's by name. — low
- LOW — plugin/lib/fmgenesis.py:111-119 — The scorecard ignores `gen`. A scenario last graded under an earlier generation still counts for the current one, because "newest wins" is per scenario. That matches the AC wording. — Show the oldest `gen` in the output if it should be visible. — low
- LOW — plugin/lib/fmcli.py:6949 — `--agent <typo>` finds no lines, so every row reads "too few" and exit 1 with no hint that the agent name is wrong. `--bar` is unchecked: a value over 1 can never pass, and nan fails every row. — Reject a bar outside 0..1 and print "no graded lines for AGENT" when the pool is empty. — high

## lens: adversary
- LOW — plugin/lib/fmgenesis.py:72,1058 — `fm genesis put exam.jsonl` is allowed by `SHAPE` and overwrites the whole file. A forged line with `agent`, `answered` and `closed` makes any capability pass. The trust model was already this loose (`_train` reads the same file), but the scorecard is now a DONE-WHEN gate. — Same class as the earlier "forged Verdict" finding; fix both together, for example by refusing `put` on `exam.jsonl`. — medium

## lens: edge
- ok. Old lines with no `answered`, non-list or non-dict fields, and non-string ids are all skipped by the `isinstance` guards (fmgenesis.py:114-118). `missing-tool` ids split correctly with `rsplit("-", 2)`. A missing gen-0 raises `ValueError`, which `cmd_exam` turns into a usage error.

## lens: operator
- LOW — plugin/lib/fmexam.py:1013 — `answered["train"]` is written to every line but never read; only `holdout` is. A full default run has 15 kinds × 6 languages × 9 scenarios = 810 ids, about 24 KB per line. Every reader scans `exam.jsonl` whole (fmgenesis.py:93, 488, 1058). The cost is small, but the bytes buy nothing. — Keep only `holdout`, or keep `train` if a later task will read it. — low

## lens: maintainer
- MEDIUM — plugin/tests/test_genesis.py:1419-1434 — Nothing tests that `fm genesis exam` writes `answered`. The scorecard test builds its lines by hand with `exam_line`. Deleting `answered=answered` at fmgenesis.py:1005-1006 would pass every test, and #13 would then read "too few" for good. — In `test_the_oracle_closes_every_scenario_and_empty_none`, assert `rows[0]["answered"]["holdout"]` equals the held-out ids, or run `scorecard` after an oracle exam. — high

Hunk-to-step mapping: the CLI wiring in fmcli.py and the two test files have no step naming them. They serve the AC. The plan lacks a wiring and tests step.

## Acceptance criteria
- Scorecard rows, newest result wins, train never counts, #13 from `draft-genesis`, exit 1 unless all pass: met in `test_scorecard_grades_each_capability_on_its_newest_held_out_results`. I did not run it. The "#13 from draft-genesis" check there rests on hand-written lines, not a real `fm genesis exam` run (see the MEDIUM above).
- `fm exam grade` with the oracle writes `answered` ids and its capability passes: met in the new `test_exam.py` test (fmexam.py:1013; test at lines 147-158). I did not run it.

## Implicit decisions
- The default agent is `foreman` and the default bar is 0.8.
- The minimum sample is 3 graded scenarios.
- #13 is matched by capability name.
- The scorecard looks at all generations.
- Scenarios across runs are pooled by id.
- Errored or fallback drafts count as graded misses.

## Not checked
- The MASTER.md hunk, which the diff left out as generated.
- I ran no tests.
- Site or export consumers of `exam.jsonl` and whether they tolerate the new `answered` key.

**Noticed:** `fm genesis put exam.jsonl` can rewrite the exam record that the selection and scorecard gates read (fmgenesis.py:72). That deserves its own task.
