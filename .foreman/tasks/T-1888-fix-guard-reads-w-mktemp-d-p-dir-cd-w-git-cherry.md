---
id: T-1888
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-29T00:55:38Z
updated: 2026-10-29T01:40:46Z
base: 81deaa25f4c5be8a111d4aec220225f9273426bb
base_tree: 56dd1e2ddcb04e8601ed379ab6b722e87112c59c
plan0_at: 2026-10-29T01:33:00Z
plan0_scope: []
verified: strong
---
# Guard reads mktemp -d -p DIR and -d DIR/nameXXX as a literal folder
## Raw request
> FIX: guard reads W=$(mktemp -d -p DIR) && cd $W && git cherry-pick as a tree write over the repo (fmguard.py:3017-3034 all-empty guess); treat mktemp -d -p DIR / DIR/x.XXXX as literal (friction 2x, low confidence)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] W=$(mktemp -d -p /tmp/x) && cd $W && git cherry-pick passes; ~, $NAME, -p with a template stay unknown — verify with `python3 plugin/tests/run.py test_guard`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing table rows for -p DIR, -p DIR -d, DIR/nameXXX and the unknown forms
2. [x] _MKTEMP_ARGS: read the literal forms in _mktemp_literal
3. [x] CHANGELOG
## Resume here
<!-- auto -->
- 2026-10-29T01:35:28Z steps 3/3 done
- git: foreman/build; 3 uncommitted: CHANGELOG.md, plugin/lib/fmguard.py, plugin/tests/test_guard.py
- touched since last checkpoint: plugin/tests/test_guard.py, CHANGELOG.md, plugin/lib/fmguard.py
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_guard.KnownVars.test_a_substitution_keeps_literal_variables_known` → red as expected (exit 1) · Ran 1 tests in 0.8s (1 classes, 16 at a time; slowest: KnownVars 0s) / FAILED (1 classes) [ran] [tree 027247151733] (2026-10-29T01:33:02Z)
- (step 2) `python3 plugin/tests/run.py test_guard test_guard_diff test_pass4` → exit 0 · Ran 300 tests in 18.6s (94 classes, 16 at a time; slowest: Mutation 17s, GuardAgainstBash 17s, Trust 10s) / OK [ran] [tree 163f25f1cf37] (2026-10-29T01:33:31Z)
- (step 3) `grep -c T-1888 CHANGELOG.md` → exit 0 · 1 [ran] [tree 163f25f1cf37] (2026-10-29T01:33:31Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmguard.py — commit it through a task, or git checkout it back / fm doctor: OK (49 pass, 5 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                42.0    45.4     150  [0] / SessionEnd                  36.3    38.3     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman- [ran] [tree 163f25f1cf37] (2026-10-29T01:39:40Z)
- (ac 1) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 290 tests in 8.1s (88 classes, 16 at a time; slowest: Mutation 8s, GuardAgainstBash 7s, Trust 5s) / OK [ran] [tree 163f25f1cf37] (2026-10-29T01:39:59Z)
- (audit intent) `self-review of the diff plus the lenses below; gates exit 0` → W=$(mktemp -d -p /tmp/x) && cd $W and -d /tmp/x/wXXXX now read as a known folder, so the cherry-pick after it isn't taken as one over the main tree [tree 163f25f1cf37] (2026-10-29T01:39:59Z)
- (audit adversary) `self-review of the diff plus the lenses below; gates exit 0` → ~, $NAME, --tmpdir=, -t, -p with a template, quotes and $ stay unknown (unchanged forms); a core DIR stays core [tree 163f25f1cf37] (2026-10-29T01:39:59Z)
- (audit edge) `self-review of the diff plus the lenses below; gates exit 0` → a relative DIR resolves against the cwd, as mktemp does; no DIR falls back to TMPDIR then /tmp [tree 163f25f1cf37] (2026-10-29T01:39:59Z)
- (audit self) `self-review of the diff plus the lenses below; gates exit 0` → no findings [tree 163f25f1cf37] (2026-10-29T01:39:59Z)
- `python3 plugin/tests/run.py test_guard` → ✗ exit 1 · Ran 290 tests in 8.9s (88 classes, 16 at a time; slowest: Mutation 8s, GuardAgainstBash 6s, Trust 5s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 163f25f1cf37] (2026-10-29T01:40:29Z)
- `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 290 tests in 8.2s (88 classes, 16 at a time; slowest: Mutation 8s, GuardAgainstBash 7s, Trust 5s) / OK [ran] [tree 163f25f1cf37] (2026-10-29T01:40:29Z)
- (audit intent) `self-review of the diff plus the lenses below; gates exit 0` → W=$(mktemp -d -p /tmp/x) && cd $W and -d /tmp/x/wXXXX now read as a known folder, so the cherry-pick after it isn't taken as one over the main tree [tree 163f25f1cf37] (2026-10-29T01:40:34Z)
- (audit adversary) `self-review of the diff plus the lenses below; gates exit 0` → ~, $NAME, --tmpdir=, -t, -p with a template, quotes and $ stay unknown (unchanged forms); a core DIR stays core [tree 163f25f1cf37] (2026-10-29T01:40:34Z)
- (audit edge) `self-review of the diff plus the lenses below; gates exit 0` → a relative DIR resolves against the cwd, as mktemp does; no DIR falls back to TMPDIR then /tmp [tree 163f25f1cf37] (2026-10-29T01:40:34Z)
- (audit self) `self-review of the diff plus the lenses below; gates exit 0` → no findings [tree 163f25f1cf37] (2026-10-29T01:40:34Z)
## Log
- 2026-10-29T00:55:38Z created
- 2026-10-29T01:09:37Z planned from capture
- 2026-10-29T01:32:59Z focused
- 2026-10-29T01:40:44Z done
- 2026-10-29T01:40:46Z committed 91cf61d5 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1487 [FIX S, done, 2 steps] Guard false block: D=/literal; mkdir -p $D && git init -q $D && printf … > $D/p.sh is refu
- T-0859 [FIX S, done, 1 steps] Guard: a bare git init in a folder that's already a repo isn't a tree write over core (3 f
- T-1727 [SECURITY M, done, 4 steps] Guard: touch into protected folders, $D resolved across ; and &&, obfuscated snapshot commands — lesson: When the guard reads a comman…
- decision 2026-10-16: T-0275: a script over the guard's parse budget stays allowed after the literal scan, not refused
- similar finished tasks took 1–4 steps
- start here (files T-0859 touched): plugin/tests/test_guard_git.py, plugin/lib/fmguard.py
## Lessons
- Read the exact arg grammar of a tool before mirroring it in the guard: only plain forms are literal, the rest stay unknown
## Files touched
- plugin/tests/test_guard.py
- CHANGELOG.md
- plugin/lib/fmguard.py
