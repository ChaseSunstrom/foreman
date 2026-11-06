---
id: T-0291
type: SECURITY
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-04T08:55:01Z
updated: 2026-10-04T09:08:37Z
batch: [T-0288, T-0289, T-0290]
base: 747532e11d5de5f071328324ea6dceca6065e6a8
base_tree: 45f63a3b928bd543ad64b921baecb80cb5bf69a9
verified: strong
---
# Session review security fixes: export --out confined to the project, second-session captures always ask, judge staging …
## Raw request
> T-0288: SECURITY: fm export agents --out (T-0263) writes any path, outside the project too, with no guard category; --force overwrites any file
> T-0289: SECURITY: fm second session (T-0276) captures are documented confirm-first, but full autonomy self-approves explore items, so a child's reading of a past transcript can be worked unattended
> T-0290: SECURITY: the bench judge's git add -A (T-0280) still runs clean/process filter drivers a bypass-mode replay could set up via .gitattributes
## Interpretation
Do T-0288, T-0289, T-0290 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-0291.
## Assumptions (confidence)
## Acceptance criteria
- [x] T-0288: fm export agents --out writes only inside the project (real path, symlinks resolved); a path outside it is refused before anything is written — verify with `python3 plugin/tests/run.py -p test_session_fixes.py -k Export`
- [x] T-0289: an item fm second session captures waits for the user's yes even in full autonomy (fm next skips it, fm state says it waits) — verify with `python3 plugin/tests/run.py -p test_session_fixes.py -k Confirm`
- [x] T-0290: bench git (worktree add, checkout of hidden tests, the judge's add and diff) runs no filter driver, whatever filter config a replay session left — verify with `python3 plugin/tests/run.py -p test_session_fixes.py -k Filters`
## Non-goals
## Approach (options → choice → why)
Export: refuse --out whose real parent isn't under the project's real root (one check in cmd_export; the guard needn't learn fm's flags). Confirm: a confirm meta flag that needs_approval honours whatever the autonomy, set by fm second session's captures. Filters: _git reads the filter drivers configured in effect (git config --get-regexp ^filter\.) and overrides each with empty clean/smudge/process and required=false — exact names, so any driver a session configured is neutral, without parsing attribute files.
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-0288: SECURITY: fm export agents --out (T-0263) writes any path, outside the project too, with n
2. [x] T-0289: SECURITY: fm second session (T-0276) captures are documented confirm-first, but full auton
3. [x] T-0290: SECURITY: the bench judge's git add -A (T-0280) still runs clean/process filter drivers a
## Resume here
<!-- auto -->
- 2026-10-04T08:59:53Z step 1/3: T-0288: SECURITY: fm export agents --out (T-0263) writes any path, outside the project too, with n
- git: foreman/build; 14 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmbench.py, plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmcost.py, plugin/lib/fmdoctor.py, plugin/lib/fmlanes.py, plugin/lib/fmsecond.py, plugin/skills/intake/references/delegate.md
- touched since last checkpoint: plugin/tests/test_session_fixes.py, plugin/lib/fmcost.py, plugin/lib/fmcore.py, plugin/lib/fmsecond.py, plugin/lib/fmbench.py, CHANGELOG.md, MASTER.md
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_session_fixes.py` → ✗ exit 1 · Ran 3 tests in 0.2s (3 classes, 16 at a time; slowest: Confirm 0s, Export 0s, Filters 0s) / FAILED (3 classes) [ran] [tree c5299bfb15bc] (2026-10-04T08:56:02Z)
- (step 1) `python3 plugin/tests/run.py -p test_session_fixes.py -k Export` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Export 0s) / OK [ran] [tree 33789c1226b9] (2026-10-04T08:56:56Z)
- (step 2) `python3 plugin/tests/run.py -p test_session_fixes.py -k Confirm` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Confirm 0s) / OK [ran] [tree 33789c1226b9] (2026-10-04T08:56:56Z)
- (step 3) `python3 plugin/tests/run.py -p test_session_fixes.py -k Filters` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Filters 0s) / OK [ran] [tree 33789c1226b9] (2026-10-04T08:56:56Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 2 of 6 failed: fm doctor → ✗ exit 1 · PASS  integrity            6 repo(s) and state intact / fm doctor: FAILED (23 pass, 4 warn, 1 fail); python3 plugin/tests/run.py → ✗ exit 1 · Ran 786 tests in 31.2s (185 classes, 16 at a time; slowest: Stop 22s, TaskLifecycle 19s, Parallel 18s) / FAILED (2 classes) [ran] [tree b76f29e83907] (2026-10-04T08:58:26Z)
- (step 1) `python3 plugin/tests/run.py -p test_session_fixes.py -k Export` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Export 0s) / OK [ran] [tree 9b90cbb2126b] (2026-10-04T09:05:46Z)
- (step 2) `python3 plugin/tests/run.py -p test_session_fixes.py -k Confirm` → exit 0 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: Confirm 1s) / OK [ran] [tree 9b90cbb2126b] (2026-10-04T09:05:47Z)
- (step 3) `python3 plugin/tests/run.py -p test_session_fixes.py -k Filters` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Filters 0s) / OK [ran] [tree 9b90cbb2126b] (2026-10-04T09:05:47Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  integrity            6 repo(s) and state intact / fm doctor: OK (24 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                30.9    32.4     150  [0] / SessionEnd                  28.3    31.7     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 08:06 UTC; python3 plugin/tests/run.py → exit 0 · Ran 786 te [ran] [tree 9b90cbb2126b] (2026-10-04T09:06:47Z)
- `fm task prove --hunks: python3 plugin/tests/run.py -p test_session_fixes.py` → 9/11 hunks proven; unproven: plugin/lib/fmcore.py @@ -512,6 +512,18 @@ def write_atomic(path, text):; plugin/lib/fmcore.py @@ -1541 +1558,2 @@ def plan_gaps(b, autonomy="standard"): [inconclusive] [ran] [tree 9b90cbb2126b] (2026-10-04T09:06:56Z)
- `fm task prove --hunks: python3 plugin/tests/run.py -p test_session_fixes.py` → exit 0 · 11/11 hunks proven [ran] [tree 775bc32a7030] (2026-10-04T09:07:14Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  integrity            6 repo(s) and state intact / fm doctor: OK (24 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · skipped: nothing under plugin/lib/**, plugin/hooks/**, plugin/bin/**, plugin/tests/bench_hooks.py, plugin/tests/fixtures/** changed since its pass at 09:06 UTC; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 08:06 UTC; [ran] [tree b9e25e658cf6] (2026-10-04T09:08:26Z)
- (ac 1) `python3 plugin/tests/run.py -p test_session_fixes.py -k Export` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Export 0s) / OK [ran] [tree b9e25e658cf6] (2026-10-04T09:08:37Z)
- (ac 2) `python3 plugin/tests/run.py -p test_session_fixes.py -k Confirm` → exit 0 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: Confirm 1s) / OK [ran] [tree b9e25e658cf6] (2026-10-04T09:08:37Z)
- (ac 3) `python3 plugin/tests/run.py -p test_session_fixes.py -k Filters` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Filters 0s) / OK [ran] [tree b9e25e658cf6] (2026-10-04T09:08:37Z)
- (audit adversary) `one fm-reviewer pass (T-0291-review-1): 1 HIGH (approved=true from fm task set bypassed confirm), 2 MEDIUM (batch and explore=false bypassed it, fm next still picked it; global-scope filter drivers still ran), 2 LOW (old git without --show-scope failed open; guessable temp name and .git/.claude targets for export) — each reproduced as a failing assertion, then fixed: confirm became a user-only guard category granted only by fm ask + the user's yes, honoured by needs_approval, batch and fm next; filters emptied in every scope but git-lfs's own driver, without --show-scope; export refuses .git/.claude; write_atomic uses mkstemp and keeps modes. Hunks 11/11 proven; guard replay 0 newly allowed` → every path the review named (approved=, explore=, --allow, batch, next, global config, planted temp symlink) is a test [tree b9e25e658cf6] (2026-10-04T09:08:37Z)
- (audit edge) `one fm-reviewer pass (T-0291-review-1): 1 HIGH (approved=true from fm task set bypassed confirm), 2 MEDIUM (batch and explore=false bypassed it, fm next still picked it; global-scope filter drivers still ran), 2 LOW (old git without --show-scope failed open; guessable temp name and .git/.claude targets for export) — each reproduced as a failing assertion, then fixed: confirm became a user-only guard category granted only by fm ask + the user's yes, honoured by needs_approval, batch and fm next; filters emptied in every scope but git-lfs's own driver, without --show-scope; export refuses .git/.claude; write_atomic uses mkstemp and keeps modes. Hunks 11/11 proven; guard replay 0 newly allowed` → LFS repos keep content; existing file modes kept; old git no longer fails open [tree b9e25e658cf6] (2026-10-04T09:08:37Z)
- (audit intent) `one fm-reviewer pass (T-0291-review-1): 1 HIGH (approved=true from fm task set bypassed confirm), 2 MEDIUM (batch and explore=false bypassed it, fm next still picked it; global-scope filter drivers still ran), 2 LOW (old git without --show-scope failed open; guessable temp name and .git/.claude targets for export) — each reproduced as a failing assertion, then fixed: confirm became a user-only guard category granted only by fm ask + the user's yes, honoured by needs_approval, batch and fm next; filters emptied in every scope but git-lfs's own driver, without --show-scope; export refuses .git/.claude; write_atomic uses mkstemp and keeps modes. Hunks 11/11 proven; guard replay 0 newly allowed` → the three member criteria met; confirm now means the user's own yes [tree b9e25e658cf6] (2026-10-04T09:08:37Z)
## Log
- 2026-10-04T08:55:01Z created
- 2026-10-04T08:55:37Z focused
- 2026-10-04T08:59:53Z paused: focus moved to T-0234
- 2026-10-04T09:04:09Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-10-04T09:04:09Z focused
- 2026-10-04T09:08:37Z done
- 2026-10-04T09:08:37Z committed 91c65ce (10 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0258-review-1: Verdict:** changes needed. I found one HIGH cross-feature issue, two MEDIUM, and the rest are LOW doc or maintainer drift. I read the whole dif…
- T-0260 [FEATURE M, dropped, 3 steps] Evidence quality: inconclusive runs, assumed vs verified facts, surprise log
- T-0276 [FEATURE L, done, 4 steps] fm second: one primitive for independent second reads — rival-model plan review, debate rebuttal, daily session review,… — lesson: Anyt…
- research T-0263-review-1: Findings come from reading the diff plus `fmcore.py`, `fmmap.py` and `fmrecall.py`. I did not run any tests. Line numbers for new code are diff…
- similar past tasks were L: consider --tier L
- the similar finished task took 4 steps
## Regression test
plugin/tests/test_session_fixes.py
## Lessons
- A flag that guards against self-authorization must clear only through the user's own grant, not through any field the session can set
## Files touched
- plugin/tests/test_session_fixes.py
- plugin/lib/fmcost.py
- plugin/lib/fmcore.py
- plugin/lib/fmsecond.py
- plugin/lib/fmbench.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmguard.py
- plugin/lib/fmcli.py
- plugin/agents/fm-builder.md
