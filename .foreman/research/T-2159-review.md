## Verdict
Approve with nits. I read the diff, `coverage.md` and the callers, but ran no commands, so the two verify commands are unrun.

## lens: intent
- LOW — plugin/lib/fmgenesis.py:203-204 — A short templated cell isn't caught. `I: a shim for plan (real.py)` and the same cell with "ship" share only 3 words, below the 4-word floor. A cell that is only the area name, such as `N/A: Initiative`, reduces to no words and is skipped (`not (a and b)`). Both are easy ways to dodge "only concrete cells count". — Require a distinctive word beyond the area and stage names (or add a minimum cell length) instead of a flat 4. — medium
- LOW — plugin/lib/fmgenesis.py:253-260 — Both twins are marked templated, including the first, concrete-looking one. A copy pasted from a real cell also un-fills the original. An identical N/A reason that is legitimate across several areas is flagged in all of them. This follows the request, but it is a surprise. The CHANGELOG line doesn't say it. — Add one line to the docstring or CHANGELOG saying "all twins, not just the later ones". — high

## lens: edge
- LOW — plugin/lib/fmgenesis.py:259 with :103 and :549 — Templated problems are appended after all the empty ones. On a mostly empty grid (the reset state) `fm genesis check` shows only 6 lines, and the export keeps the first 50 problems. A templated cell is then never visible in the text output or the site data. The count is still in the header. — Put templated and bad-cell problems before the empty ones, or list them first. — medium

## lens: operator
- LOW — plugin/lib/fmgenesis.py:196 — "~0.6 s on a 1,200-cell grid" is a claim with no recorded measurement. Cost is O(pairs per column) per `check()`. `health()` caches it (fmgenesis.py:398). `fm genesis check`, `put` and `export` pay it uncached. The real grid is nearly empty now, so there is no cost today. — Record the timing in the task, or check how long it takes on a full grid. — low

## lens: maintainer
- LOW — plugin/lib/fmgenesis.py:1244-1245 — The seed Mission table now counts a templated cell as "ungrounded" (it adds to `bad`). For an I cell, `ideas` falls by 1 and `bad` rises by 1, so the open count is unchanged, but the label is wrong. The text calls it "ungrounded" when the cell is templated. — Track templated separately in `rows[r]`, or relabel the column "ungrounded or templated". — high
- LOW — plugin/lib/fmgenesis.py:192 — `import difflib` sits inside `_twins`. Earlier reviews flagged an import moved into a function body for no stated reason. — Move it to the module header, or comment why (health stays light). — medium
- Tests: the new test covers the template, area swap, N/A twin, concrete cells, F cells and the check-line count. Nothing covers `seed`'s Mission counts after a twin is removed (the `ideas` and `bad` adjustment at :257-258). — Add one assertion on `cov["rows"]`. — medium

## Acceptance criteria
- AC1 (templated I or N/A cell is a problem naming its twin; concrete and F cells still count): met by the code, and `test_a_templated_cell_is_a_problem_naming_its_twin` asserts it (6 templated, 122 filled). Unrun.
- AC2 (`coverage.md` reset, check reports no templated cell): met on a read. `state/projects/foreman-4a056f/research/genesis/coverage.md` has 17 I cells and no N/A cells. I estimated the ratio for same-column pairs (fm code, Desktop) at about 0.3 to 0.4, below 0.6. Unrun.

## Implicit decisions
- Twins are compared only within one surface column. A frame reused across surfaces isn't caught.
- Both twins are flagged, and an F cell is exempt.
- Word-level difflib with a 0.6 ratio and a 4-matched-word floor.
- Only words of 4+ letters from the area heading are dropped. Stage words are not dropped; the ratio absorbs them.
- The unmatched `coverage.md` edit is state, not repo, so the diff doesn't show it.

## Not checked
The MASTER.md hunk (elided from the diff), a real-grid timing, and the pane and site renderers of `templated`.

**Noticed:** none
