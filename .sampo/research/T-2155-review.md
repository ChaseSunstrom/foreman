## Verdict
**Changes needed.** The `exam.jsonl` refusal is correct and tested, but the request's second half, the forged-Verdict case, isn't fixed.

## lens: intent
- HIGH — plugin/lib/fmgenesis.py:16-17 — The request said "fix the forged-Verdict case alongside". Nothing in the diff touches it. `put` still accepts `gen-N/drift.md` and `gen-N/sweep.md`. `step()` passes either file as long as it has a line `Verdict: clean` (CLEAN regex at :1235, check at :332). The drift stage also needs `_stale` to pass, and that only compares mtimes. — Fix, either of these:
  - Stop `put` writing `drift.md` and `sweep.md`, so only `drift()` and `sweep()` write them. Take them out of SHAPE the same way `exam.jsonl` was.
  - Have `put` refuse any text containing a line `^Verdict:` for those two names, or have `drift()` and `sweep()` write a seal such as a sha of the body. — confidence high (the code path is read; I didn't run a reproducer).
  - Proof: `echo 'Verdict: clean' | fm genesis put gen-1/drift.md --file -` and the same for `sweep.md`. `fm genesis step` then moves past both stages without running either check. The existing line-478 reader (`^Verdict: (\w+)`) shows the same forged text on the site.
  - Add a test that the put is refused.
- MEDIUM — plugin/lib/fmgenesis.py:318 — `lineage.md` is still writable through `put`. A `## gen-N` heading satisfies the select stage without running `fm genesis select`. This is the same class as the forged Verdict. It may be out of scope, but capture it if you don't fix it here. — Fix: refuse it, or let only `select()` write it. — confidence medium.

## lens: adversary
- Same as the HIGH above. The only way that stops a forged pass is to remove the put route for the two verdict files.
- `exam.jsonl` refusal: SHAPE is matched with `fullmatch`, so `./exam.jsonl`, `gen-1/../exam.jsonl` and `EXAM.JSONL` don't match any alternative. They are refused, not routed around. I found no way around the refusal inside `put`.

## lens: edge
- No findings. Fixtures now write the file directly with `exam_file`, `os.makedirs` handles a missing tower folder, and the helper doesn't use the lock. That is fine in a test.

## lens: operator
- CHANGELOG entry is present and accurate. It claims nothing about the Verdict fix, which fits the diff. I only reviewed the one-line diff: MASTER.md was left out of the diff as generated.
- No cost or startup changes.

## lens: maintainer
- LOW — plugin/tests/test_genesis.py:12 — `exam_file` sits above `GEN0` and the other module constants. It has no blank-line handling that matters. — Fix: none needed. Drop this one; it's style only.
- The new refusal test (:57-60) asserts the return code, the stderr text and that no file was written. It would fail without the change. Good.
- `exam_line` appending is covered by `test_exam`, which still reads the file at lines 86, 104, 265, 382 and 394. I didn't run it.

## Acceptance criteria
- "`fm genesis put exam.jsonl` is refused and `exam_line` still appends": **met by the code**. The refusal and the test are there, and `exam_line` is unchanged. The criterion doesn't cover the Verdict half of the request, so passing it won't show that half is done.

## Implicit decisions
- Dropping `exam.jsonl` from SHAPE, rather than adding a special-case branch.
- The refusal message names `fm exam grade` and `fm genesis exam` as the writers.
- Test fixtures write the file directly instead of going through `exam_line`.

## Not checked
- I didn't run the test suite.
- Direct filesystem edits of `exam.jsonl`, which would be a guard question.
- MASTER.md's one-line change.

Noticed: `lineage.md` can be forged through `put`, which skips the select stage (fmgenesis.py:318). That is worth its own task if it isn't fixed here.
