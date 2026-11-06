---
id: T-0287
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-04T08:45:52Z
updated: 2026-10-04T08:48:07Z
base: e5cf898be2cf47afae5a2cc83c329f9411d170e9
base_tree: c74785bb61c16b5758a661c7d8537bc9413b0a6e
verified: strong
---
# Pass 5: fm replay --cmd asks the guard about one command without running it; the pre-audit's code patterns scan code files only
## Raw request
> Pass 5: fm replay --cmd asks the guard about one command without running it; the pre-audit's code patterns scan code files only
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm replay --cmd TEXT [--cwd DIR] prints the guard's default verdict (category and detail, or allow) for that one command and never runs it — verify with `python3 plugin/tests/run.py -p test_pass5.py -k Probe`
- [x] the pre-audit's security code patterns read added lines of code files only, so docs naming the patterns don't flag the change — verify with `python3 plugin/tests/run.py -p test_pass5.py -k Patterns`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests first: test_pass5.py
2. [x] fm replay --cmd; sensitive() reads code files' added lines
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_pass5.py` → ✗ exit 1 · Ran 2 tests in 0.1s (2 classes, 16 at a time; slowest: Probe 0s, Patterns 0s) / FAILED (2 classes) [ran] [tree 999d58b45621] (2026-10-04T08:46:02Z)
- (step 2) `python3 plugin/tests/run.py -p test_pass5.py` → exit 0 · Ran 2 tests in 0.1s (2 classes, 16 at a time; slowest: Probe 0s, Patterns 0s) / OK [ran] [tree ff4f46b05746] (2026-10-04T08:46:59Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  integrity            6 repo(s) and state intact / fm doctor: OK (24 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                31.2    33.7     150  [0] / SessionEnd                  28.1    29.6     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 08:06 UTC; python3 plugin/tests/run.py → exit 0 · Ran 779 te [ran] [tree 8c8b617ee92f] (2026-10-04T08:47:50Z)
- `fm task prove --hunks: python3 plugin/tests/run.py -p test_pass5.py` → 5/6 hunks proven; unproven: plugin/lib/fmreplay.py @@ -63,2 +72 @@ def verdicts(cmds): [inconclusive] [ran] [tree 8c8b617ee92f] (2026-10-04T08:48:01Z)
- (ac 1) `python3 plugin/tests/run.py -p test_pass5.py -k Probe` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Probe 0s) / OK [ran] [tree 8c8b617ee92f] (2026-10-04T08:48:07Z)
- (ac 2) `python3 plugin/tests/run.py -p test_pass5.py -k Patterns` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Patterns 0s) / OK [ran] [tree 8c8b617ee92f] (2026-10-04T08:48:07Z)
- (audit adversary) `self: both criteria red→green; the narrowed pattern scan replayed over 60 real commits changed only the pass-4 commit's doc-only hits; fm replay --cmd never runs the command (asserted on a path it would create); hunks 5/6 (the rest: an equivalent refactor of verdicts() onto _ctx)` → the filter fails closed — only doc extensions are skipped, every other file (html, vue, scripts) is still scanned; --cmd only reads [tree 8c8b617ee92f] (2026-10-04T08:48:07Z)
- (audit self) `self: both criteria red→green; the narrowed pattern scan replayed over 60 real commits changed only the pass-4 commit's doc-only hits; fm replay --cmd never runs the command (asserted on a path it would create); hunks 5/6 (the rest: an equivalent refactor of verdicts() onto _ctx)` → no findings [tree 8c8b617ee92f] (2026-10-04T08:48:07Z)
## Log
- 2026-10-04T08:45:52Z created
- 2026-10-04T08:45:52Z focused
- 2026-10-04T08:48:07Z done
- 2026-10-04T08:48:07Z committed 747532e (6 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-pass-3: Source: research/brainstorm-20261004-021539 (bold bets, simplicity, user-love, security and safety × 2 rounds, past passes 1–2 and two earlie…
- research T-0270-review-1: Verdict: changes needed.** The new code has one regression and several ways around it. I read the code only. I could not run commands, so every…
- research t0018-r1-adversary: ck add \"true\"` (a trivially-passing later gate), then `fm check --evidence T-1 --step N`. `fm check`'s own exit code is 1 (line 640, corre…
- research brainstorm-pass-2: Source: research/brainstorm-20261004-020314 (4 lenses × 2 rounds, past pass 1 and three earlier lists; 82 new titles). Pack: pass 1's results…
## Regression test
plugin/tests/test_pass5.py (Probe, Patterns)
## Lessons
- When a scan flags its own docs, skip by what can't run (doc extensions), not by an allowlist of code types, so the filter fails closed
## Files touched
- plugin/tests/test_pass5.py
- plugin/lib/fmcore.py
- plugin/lib/fmreplay.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
