---
id: T-0269
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/, plugin/tests/, MASTER.md, CHANGELOG.md]
depends_on: []
source: self
created: 2026-10-04T06:41:42Z
updated: 2026-10-04T06:51:30Z
batch: [T-0265, T-0266, T-0267]
base: e6c4293fdbd213b7d3580ac03fb397d2b45e21fe
base_tree: 42d15f01e07cbdc4f287a76340661a151ffe7657
verified: strong
---
# Pass 1 quick wins: read-only git stash, S-tier outgrowth tripwire, shared-prefix child prompts
## Raw request
> T-0265: Guard: git stash list and git stash show are read-only
> T-0266: S tasks that outgrow S: fm next says to re-tier when an S task touches more than two non-test files
> T-0267: Shared-prefix child prompts: the context pack goes before the lens so sibling and later-round children share a cacheable prefix
## Interpretation
Pass 1's small grounded fixes: a guard false positive from today's friction, a quality gap when small tasks grow, and free prompt-cache hits for brainstorm children.
## Assumptions (confidence)
## Acceptance criteria
- [x] T-0265: git stash list / git stash show over a protected tree pass the guard; git stash, stash pop/apply/drop still block — verify with `python3 plugin/tests/run.py -p "test_pass1*" -k Stash`
- [x] T-0266: fm next on an S task whose edits reach three or more non-test files says it has outgrown S and how to re-tier — verify with `python3 plugin/tests/run.py -p "test_pass1*" -k Outgrown`
- [x] T-0267: two lenses' child prompts (and a later round's) share the context pack as their prefix — verify with `python3 plugin/tests/run.py -p "test_pass1*" -k Prefix`
## Non-goals
## Approach (options → choice → why)
Stash: in _write_targets, git stash list|show is not a worktree write (every other stash form still is). Outgrown: next_action's executing branch counts task_touches (non-test files) for S tasks — the same ledger read fm done already uses; ≥3 adds the re-tier hint (rules say S = 1–2 files). Rejected: diff line counts (a git call on every prompt). Prefix: child_prompt puts 'Context pack' first and the lens last; later_round_pack/deepen_pack already append to the pack.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Tests first: plugin/tests/test_pass1.py (Stash, Outgrown, Prefix) fail
2. [x] Implement the three fixes
3. [x] Docs: MASTER.md, CHANGELOG.md
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p "test_pass1*"` → ✗ exit 1 · Ran 0 tests in 0.0s (1 classes, 16 at a time; slowest: _FailedTest 0s) / FAILED (1 classes) [ran] [tree 35f3c78c5bb8] (2026-10-04T06:42:13Z)
- (step 1) `python3 plugin/tests/run.py -p "test_pass1*"` → ✗ exit 1 · Ran 3 tests in 0.2s (3 classes, 16 at a time; slowest: Outgrown 0s, Stash 0s, Prefix 0s) / FAILED (3 classes) [ran] [tree e410666e5655] (2026-10-04T06:42:21Z)
- (step 2) `python3 plugin/tests/run.py -p "test_pass1*"` → exit 0 · Ran 3 tests in 0.4s (3 classes, 16 at a time; slowest: Outgrown 0s, Stash 0s, Prefix 0s) / OK [ran] [tree 286e696ad4fa] (2026-10-04T06:42:46Z)
- (step 3) `grep -c 'T-0269' MASTER.md CHANGELOG.md` → exit 0 · MASTER.md:1 / CHANGELOG.md:1 [ran] [tree 286e696ad4fa] (2026-10-04T06:42:46Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (23 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                29.7    31.5     150  [0] / SessionEnd                  27.9    30.7     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 06:33 UTC; python3 plugin/tests/run.py → e [ran] [tree 286e696ad4fa] (2026-10-04T06:43:41Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (23 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                30.6    32.8     150  [0] / SessionEnd                  27.8    29.1     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 06:33 UTC; python3 plugin/tests/run.py → e [ran] [tree ce17247accc1] (2026-10-04T06:48:05Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (23 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                29.9    31.3     150  [0] / SessionEnd                  27.6    29.0     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 06:33 UTC; python3 plugin/tests/run.py → e [ran] [tree aecc8a89b468] (2026-10-04T06:51:22Z)
- (ac 1) `python3 plugin/tests/run.py -p "test_pass1*" -k Stash` → exit 0 · Ran 2 tests in 0.1s (1 classes, 16 at a time; slowest: Stash 0s) / OK [ran] [tree aecc8a89b468] (2026-10-04T06:51:29Z)
- (ac 2) `python3 plugin/tests/run.py -p "test_pass1*" -k Outgrown` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Outgrown 0s) / OK [ran] [tree aecc8a89b468] (2026-10-04T06:51:29Z)
- (ac 3) `python3 plugin/tests/run.py -p "test_pass1*" -k Prefix` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Prefix 0s) / OK [ran] [tree aecc8a89b468] (2026-10-04T06:51:29Z)
- (audit intent) `fm-reviewer pass (research T-0269-review-1) then a focused adversary pass on the guard fix (T-0269-review-2); every finding in this diff fixed with tests, older git gaps captured as T-0270` → criteria met; stash list/show read-only without opening a hole [tree aecc8a89b468] (2026-10-04T06:51:29Z)
- (audit adversary) `fm-reviewer pass (research T-0269-review-1) then a focused adversary pass on the guard fix (T-0269-review-2); every finding in this diff fixed with tests, older git gaps captured as T-0270` → fixed — git --output targets, exec env vars, -c command keys (widened), aliases with their global options, --exec-path/--config-env/env config refused, value-taking globals skipped; pre-existing git channels → T-0270 [tree aecc8a89b468] (2026-10-04T06:51:29Z)
- (audit edge) `fm-reviewer pass (research T-0269-review-1) then a focused adversary pass on the guard fix (T-0269-review-2); every finding in this diff fixed with tests, older git gaps captured as T-0270` → fixed — outgrowth hint counts code files only, short ledger window, errors isolated; self-alias hits the depth cap (fail-closed) [tree aecc8a89b468] (2026-10-04T06:51:29Z)
- (audit operator) `fm-reviewer pass (research T-0269-review-1) then a focused adversary pass on the guard fix (T-0269-review-2); every finding in this diff fixed with tests, older git gaps captured as T-0270` → ok — docs; fm replay 0 newly allowed [tree aecc8a89b468] (2026-10-04T06:51:29Z)
- (audit maintainer) `fm-reviewer pass (research T-0269-review-1) then a focused adversary pass on the guard fix (T-0269-review-2); every finding in this diff fixed with tests, older git gaps captured as T-0270` → ok — CODE/TESTISH shared from fmcore instead of copies [tree aecc8a89b468] (2026-10-04T06:51:29Z)
## Log
- 2026-10-04T06:41:42Z created
- 2026-10-04T06:42:02Z set scope=['plugin/lib/', 'plugin/tests/', 'MASTER.md', 'CHANGELOG.md']
- 2026-10-04T06:42:03Z focused
- 2026-10-04T06:51:29Z done
- 2026-10-04T06:51:30Z committed 447785a (7 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-pass-1: Source: research/brainstorm-20261004-013651 (4 lenses × 3 rounds, past the four earlier idea lists; 132 new titles). Pack: the user's words, …
- research brainstorm-20261003-round6: Runs: brainstorm-20261003-230652 (5 lenses + deepen 3: 78 new titles) and brainstorm-20261003-230844 (4 lenses + deepen 2: 61 new ti…
- research brainstorm-20260926-super2-slate: Build: F1 files changed through the shell/outside Claude (git since base) join Files touched and scope drift (R1 "detect edits…
- research brainstorm-20261003-round5: Quota brake (bold bets) → T-0198 economy mode: the mod reads session.usage rate limits; past 80% weekly / 90% 5-hour a prompt.compos…
- likely tests for the scope: plugin/tests/test_bench.py, plugin/tests/test_budget.py, plugin/tests/test_core.py, plugin/tests/test_docs.py, plugin/tests/test_doctor.py, plugin/tests/test_evolve.py, plugin/tests/test_friction.py,…
## Lessons
- Loosening a guard rule needs an adversary pass over everything the old over-broad rule was silently catching (here: git --output and -c exec keys), not just the case being allowed
## Files touched
- plugin/tests/test_pass1.py
- plugin/lib/fmcore.py
- plugin/lib/fmguard.py
- plugin/lib/fmideas.py
- plugin/lib/fmmap.py
- CHANGELOG.md
- MASTER.md
