Verdict: changes needed (2 MEDIUM, 3 LOW) on the lane branch; all addressed or skipped with reason. Reviewer: foreman:fm-reviewer, read-only, lenses intent/adversary/edge.

## lens: intent
- MEDIUM — any red counted as tf-first, including a red caused by the putback removing a name the arm's test imports (an edge region runs to the file's end and wipes code appended after it). FIXED: grade credits only `_caught` (red and not a LOAD error); test_a_red_from_a_name_the_putback_removed_is_not_the_arms_test_catching_the_defect. Refusing edge regions outright was tried and dropped: goal/none/child scenarios put their defect at the file's end, so the oracle lost credit (tf_first != tf_keyed). Residual (a wiped side effect reading red) marked ponytail in putback.
- LOW — a timeout counts as red. SKIPPED: by design, a slow defect shows itself by a timeout (SLOW_T, "a timeout is a failure").

## lens: adversary
- LOW — putback wrote through an arm's symlink. FIXED: the copy's file is unlinked before writing.
- Confirmed: putback executes nothing; arm code runs only via _run with credentials stripped.

## lens: edge
- MEDIUM — a read-only arm file raised PermissionError outside the cleanup path, leaking the temp dir and crashing grade(). FIXED: unlink before write, and except (LookupError, OSError) cleans up; the synthetic test chmods the arm's file 0444.
- LOW — a planted file clean lacks, or a binary file, credits nothing. Accepted (never over-credits).

## tests
- Added a synthetic case: two reworded replace regions in one file, an anchor widened past a repeated line, an end-of-file region, a read-only file. Mutation check: removing the after-anchor widening fails it.

Noticed: grade() has no per-scenario guard, so one scenario's exception aborts the run's grade (out of scope).
