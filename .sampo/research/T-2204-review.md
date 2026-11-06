Verdict: approve with nits (4 MEDIUM, 7 LOW); fixed or skipped with reason. Reviewer: one foreman:fm-reviewer, six lenses (incl. design), read-only.

## lens: intent
- MEDIUM — a capability with "Exam: bug, docs" passed on its bug child results alone. FIXED: state "partial" (never pass) when some kinds have no outside author; `why` names them. Test: test_a_capability_partly_without_an_outside_author_never_passes.
- MEDIUM — #13 is hard-wired to no outside author, so the scorecard can't go green with a Genesis capability. FIXED (said): the row's `why` reads "fm genesis spec renders template projects only"; the path is captured.
- MEDIUM (plausible) — the AUTHOR prompt told a dep child the existing tests must pass, which dep can't do. FIXED: per-kind KEEP line for dep.

## lens: edge
- MEDIUM — ids are author-independent; a later template run erased earlier child results. FIXED: a template result never overwrites a child one. Test added.
- LOW — _check_one passes dep on any build failure; non-python slow/dep untested. SKIPPED: fm exam check gates each generated scenario; a python stub covers the path, other languages drop cleanly when their check fails.
- LOW — slow check under load may drop borderline child inputs (fail-closed). Accepted.

## lens: adversary
- LOW — a forged child id of a non-child kind would count (exam.jsonl is state-direct guarded already). FIXED: ids of kinds CHILD_KINDS lacks are ignored. Test added.
- LOW — none-kind scenarios count child though two of three defects are template-written. Accepted: the lead plant is the child's (documented in the implicit decisions).

## lens: maintainer
- LOW — stale scorecard docstring; `self` vs `selfmade` naming. FIXED (docstring rewritten; row key renamed selfmade).
- LOW — stale --author/--kind help. FIXED.

## lens: design
- LOW — the site marker hit draft rows and pre-T-2204 lines with no author. FIXED: shown only when e.author is set and not child.

## lens: operator
- LOW — child calls up ~33% per full gen. Accepted (gen is off the hot path).

Noticed: T-2211 is a hard dependency for the scorecard ever going green (planned and approved).
