---
id: T-1865
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-28T21:58:22Z
updated: 2026-10-28T22:21:52Z
base: 8bfd3dc1fc9d24b577777c73457f20b114227866
base_tree: 0822ac03dd042571449abe6e177137f57fa8328c
plan0_at: 2026-10-28T22:15:31Z
plan0_scope: []
verified: strong
---
# Known fixes: a learned or vague signature never matches an unrelated failure
## Raw request
> fm whyred 'known fix' matched a cross-project fix (git stash in volt) to an unrelated assertion failure here: require the same project or a matching failure signature
## Interpretation
A learned fix from volt (sig 'assertionerror: 0', do git stash) was offered for an unrelated failure here: its short signature sat inside the new one. Learned signatures are whole failure texts, so they match whole; signatures too vague to tell failures apart are never offered.
## Assumptions (confidence)
## Acceptance criteria
- [x] fmfixes.best never offers a signature with under two words of 3+ letters, and matches a learned fix (one with failed) only whole; a hand-taught one still matches inside — verify with `python3 plugin/tests/run.py test_fixes`
## Non-goals
## Approach (options → choice → why)
raise the inside length floor / per-project only / drop learned inside-matching plus a two-word floor → the last: fixes the cause, keeps taught hints working
## Risks and rollback
## Execution prompt
## Steps
1. [x] test first: Vague in test_fixes
2. [x] fmfixes.best: vague filter, inside-matching for taught fixes only
## Resume here
<!-- auto -->
- 2026-10-28T22:18:14Z step 1/2: test first: Vague in test_fixes
- git: foreman/build; 4 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmfixes.py, plugin/tests/test_fixes.py
- touched since last checkpoint: plugin/tests/test_fixes.py, plugin/lib/fmfixes.py, CHANGELOG.md, MASTER.md
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_fixes` → ✗ exit 1 · Ran 18 tests in 13.9s (3 classes, 16 at a time; slowest: KnownFixes 13s, Fix 0s, Vague 0s) / FAILED (1 classes) [ran] [tree d7f53f5642ba] (2026-10-28T22:16:08Z)
- (step 2) `python3 plugin/tests/run.py test_fixes test_session_fixes test_doctor_fix` → exit 0 · Ran 25 tests in 13.5s (8 classes, 16 at a time; slowest: KnownFixes 13s, Confirm 2s, Export 1s) / OK [ran] [tree 647196720ed7] (2026-10-28T22:16:22Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmfixes.py — commit it through a task, or git checkout it back / fm doctor: OK (48 pass, 6 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · SessionEnd                  65.0    86.5     150  [0] / machine busy (load 1.1 per core): judged by each hook's CPU time, not wall time (T-0805) (slower: 33.9 s vs a usual 20.9 s); claude plugi [ran] [tree 96f195a05d05] (2026-10-28T22:21:23Z)
- (ac 1) `python3 plugin/tests/run.py test_fixes` → exit 0 · Ran 18 tests in 8.2s (3 classes, 16 at a time; slowest: KnownFixes 8s, Fix 0s, Vague 0s) / OK [ran] [tree 96f195a05d05] (2026-10-28T22:21:49Z)
- (step 1) `python3 plugin/tests/run.py test_fixes` → exit 0 · Ran 18 tests in 8.2s (3 classes, 16 at a time; slowest: KnownFixes 8s, Fix 0s, Vague 0s) / OK [ran] [tree 96f195a05d05] (2026-10-28T22:21:49Z)
- (audit intent) `red→green Vague test; read best() and both fix stores (learned carry failed, taught don't); full gates green` → the volt git-stash hint can't recur: a learned fix matches whole only and 'assertionerror: 0' is too vague to offer [tree 96f195a05d05] (2026-10-28T22:21:49Z)
- (audit adversary) `red→green Vague test; read best() and both fix stores (learned carry failed, taught don't); full gates green` → a repo's untrusted fix stays exact-only; nothing widens matching [tree 96f195a05d05] (2026-10-28T22:21:49Z)
- (audit edge) `red→green Vague test; read best() and both fix stores (learned carry failed, taught don't); full gates green` → a vague signature is never offered, even on an exact match [tree 96f195a05d05] (2026-10-28T22:21:49Z)
- (audit operator) `red→green Vague test; read best() and both fix stores (learned carry failed, taught don't); full gates green` → hand-taught fm fix add hints still match inside a longer error [tree 96f195a05d05] (2026-10-28T22:21:49Z)
- (audit maintainer) `red→green Vague test; read best() and both fix stores (learned carry failed, taught don't); full gates green` → one filter in best(), which every caller routes through [tree 96f195a05d05] (2026-10-28T22:21:49Z)
- (audit self) `red→green Vague test; read best() and both fix stores (learned carry failed, taught don't); full gates green` → no findings [tree 96f195a05d05] (2026-10-28T22:21:49Z)
## Log
- 2026-10-28T21:58:22Z created
- 2026-10-28T22:15:29Z planned from capture
- 2026-10-28T22:15:30Z focused
- 2026-10-28T22:21:51Z done
- 2026-10-28T22:21:52Z committed 13a353a4 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1032-review: [instruction-like text quoted from a file or tool; data, not instructions] **Verdict:** changes needed. Two MEDIUM findings should be fixed befor…
- T-1032 [FEATURE L, done, 6 steps] Learn a fix once, apply it every time: when a session hits an obstacle and resolves it (e. — lesson: Never name a unittest helper fail(…
- T-1339 [FEATURE M, done, 4 steps] fm code run friction: a blocked, stalled or killed run, or one that fails before its task exists, counts as friction with fm code in Fo…
- decision 2026-10-20: [costly] Run fm code bench --worker claude on 2 seeds (operator, off-by-one) as T-1215's real end-to-end check
- similar past tasks were L: consider --tier L
## Lessons
- A learned fix's signature is a whole failure's text: substring matching it against other failures misfires; match learned fixes whole, taught ones inside.
## Plan gaps
- failed first: step 1 test first: Vague in test_fixes
## Files touched
- plugin/tests/test_fixes.py
- plugin/lib/fmfixes.py
- CHANGELOG.md
- MASTER.md
