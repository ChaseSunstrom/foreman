---
id: T-1891
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-29T01:26:55Z
updated: 2026-10-29T02:06:38Z
base: fbe7d26ae3fe12ae6cee89eafcf6834b8bbadcd0
base_tree: eaf966adab97dc46b7468cf666a37a13b0bd46b5
plan0_at: 2026-10-29T01:58:35Z
plan0_scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, CHANGELOG.md]
verified: strong
---
# Guard keeps a cd certain for && commands after it when the line has ||
## Raw request
> Guard reads git checkout -- . after cd into a scratch worktree as a tree write over core
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] cd DIR && git checkout -- . && a || b reads the checkout in DIR; true || cd X && y still maybe-here — verify with python3 plugin/tests/run.py test_guard
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing table: || later in the line, cd after ||, failing cd before ||
2. [x] _top: || splits segments; a cd after || is never certain
3. [x] CHANGELOG
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_guard.KnownVars` → ✗ exit 1 · Ran 8 tests in 0.9s (1 classes, 16 at a time; slowest: KnownVars 0s) / FAILED (1 classes) [ran] [tree 822a18210e45] (2026-10-29T01:58:37Z)
- (step 2) `python3 plugin/tests/run.py test_guard.KnownVars` → exit 0 · Ran 8 tests in 1.0s (1 classes, 16 at a time; slowest: KnownVars 0s) / OK [ran] [tree e77eb5e20c86] (2026-10-29T01:58:44Z)
- (step 3) `grep -c T-1891 CHANGELOG.md` → exit 0 · 1 [ran] [tree e77eb5e20c86] (2026-10-29T01:59:09Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmguard.py — commit it through a task, or git checkout it back / fm doctor: OK (49 pass, 5 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                40.1    41.8     150  [0] / SessionEnd                  35.4    37.9     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman- [ran] [tree e77eb5e20c86] (2026-10-29T02:05:35Z)
- (ac 1) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 291 tests in 7.8s (88 classes, 16 at a time; slowest: Mutation 8s, GuardAgainstBash 6s, Trust 4s) / OK [ran] [tree e77eb5e20c86] (2026-10-29T02:06:00Z)
- (ac 1) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 291 tests in 7.9s (88 classes, 16 at a time; slowest: Mutation 8s, GuardAgainstBash 6s, Trust 4s) / OK [ran] [tree e77eb5e20c86] (2026-10-29T02:06:27Z)
- (audit intent) `self-review of the diff plus the lenses below; gates exit 0` → cd S/try && git checkout -- . && ... || echo reads the checkout as one in S/try, not the main tree, so the guard no longer blocks it [tree e77eb5e20c86] (2026-10-29T02:06:27Z)
- (audit adversary) `self-review of the diff plus the lenses below; gates exit 0` → true || cd X && y and true || cd X; y stay maybe-here (a cd after || may be skipped); a failing cd before || leaves the cwd unchanged [tree e77eb5e20c86] (2026-10-29T02:06:27Z)
- (audit edge) `self-review of the diff plus the lenses below; gates exit 0` → cd X || exit; y with an existing X stays certain; false || true && cd X && y is certain since y needs the cd [tree e77eb5e20c86] (2026-10-29T02:06:27Z)
- (audit self) `self-review of the diff plus the lenses below; gates exit 0` → no findings [tree e77eb5e20c86] (2026-10-29T02:06:27Z)
## Log
- 2026-10-29T01:26:55Z created
- 2026-10-29T01:33:38Z planned from capture
- 2026-10-29T01:58:33Z focused
- 2026-10-29T02:06:36Z done
- 2026-10-29T02:06:38Z committed 0979983c (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1727 [SECURITY M, done, 4 steps] Guard: touch into protected folders, $D resolved across ; and &&, obfuscated snapshot commands — lesson: When the guard reads a comman…
- T-1487 [FIX S, done, 2 steps] Guard false block: D=/literal; mkdir -p $D && git init -q $D && printf … > $D/p.sh is refu
- research rsi-pass-20261008: 1. **Answer.** I could ground one improvement fully (the pipe-shell false block) and one partly (state-direct from guessed variable targets).…
- decision 2026-10-06: The desktop app lives in its own repo (~/projects/foreman-desktop), not apps/desktop in the Foreman checkout
- similar finished tasks took 2–4 steps
- likely tests for the scope: plugin/tests/test_guard.py
## Lessons
- A cd's certainty depends on the operator before it, not on whether the line holds an || anywhere
## Plan gaps
- failed first: step 1 Failing table: || later in the line, cd after ||, failing cd before ||
## Files touched
- plugin/tests/test_guard.py
- CHANGELOG.md
- plugin/lib/fmguard.py
