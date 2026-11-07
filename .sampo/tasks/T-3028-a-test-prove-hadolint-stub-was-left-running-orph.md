---
id: T-3028
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-04T21:53:46Z
updated: 2026-11-04T22:15:23Z
base: 1a8ef8df177cff00415f016dd9e1cbab1e38e870
base_tree: 39f0fddb5a320ff7d88ce3b3fc78f5c999b57041
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-04T22:15:11Z
plan0_scope: []
verified: strong
unproven: [meaning]
---
# A test_prove hadolint stub was left running (orphaned to init, 78% CPU for 1h45) after a…
## Raw request
> A test_prove hadolint stub was left running (orphaned to init, 78% CPU for 1h45) after a suite run: the infra proof's tool timeout likely kills only the direct child, not its process group; find the test and make the runner kill the group
## Interpretation
test_prove's hang stub for hadolint is 'while :; do :; done'; find._run_tool kills its process group on the 1 s timeout, but when the test process itself is killed first (a check timeout), the stub, in its own session, spins under init forever (found at 78% CPU after 1h45). The stub should end when its parent does.
## Assumptions (confidence)
## Acceptance criteria
- [x] the hang stub still times out as unproven, and it exits by itself once its parent process is gone — verify with `python3 plugin/tests/run.py test_prove`
## Non-goals
## Approach (options → choice → why)
1) The stub loops only while its parent lives: 'while kill -0 $PPID 2>/dev/null; do :; done' (kill is a builtin; the PATH there holds no sleep). Likely outcome: same hang for the timeout test, no orphan when the runner dies. Fails if: the parent pid is reused within the loop (rare; still ends at the next check).
2) Use what exists: PR_SET_PDEATHSIG for _run_tool children. Fails if: needs ctypes and Linux-only code in product code for a test-only leak.
3) Do less: a bounded loop count. Fails if: the bound is either too short for a loaded runner's 1 s timeout or long enough to burn minutes.
Choice 1 (85%).
## Risks and rollback
## Execution prompt
## Steps
1. [x] the stub loops only while its parent lives; check it exits when the parent dies
## Resume here
## Docs impact
none: a test helper
## Verification evidence
- (step 1) `sh /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/t3028/check.sh && python3 plugin/tests/run.py test_prove` → exit 0 · Ran 107 tests in 9.2s (16 classes, 16 at a time; slowest: InfraProof 9s, InfraFinish 6s, ReleaseProof 6s) / OK [ran] [tree 39f0fddb5a32] [world 2f1906870a] (2026-11-04T22:12:54Z)
- (ac 1) `python3 plugin/tests/run.py test_prove` → exit 0 · Ran 107 tests in 7.3s (16 classes, 16 at a time; slowest: InfraProof 7s, ReleaseProof 3s, InfraFinish 3s) / OK [ran] [tree 39f0fddb5a32] [world 2f1906870a] (2026-11-04T22:15:20Z)
- `sh /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/t3028/check.sh && python3 plugin/tests/run.py test_prove` → exit 0 · reused: the same command passed on this tree and world at 2026-11-04T22:12:54Z [ran] [tree 39f0fddb5a32] [world 2f1906870a] (2026-11-04T22:15:20Z)
- (audit edge) `self: read the one-line stub change against the timeout test it serves; kill -0 $PPID is a builtin, so the PATH with no sleep still works; the timeout test still sees a hang and reports unproven` → the parent's pid reused within the loop would keep it alive only until that process ends; the check script shows the old stub orphaned and the new one ending with its parent [tree 39f0fddb5a32] (2026-11-04T22:15:20Z)
- (audit self) `self: read the one-line stub change against the timeout test it serves; kill -0 $PPID is a builtin, so the PATH with no sleep still works; the timeout test still sees a hang and reports unproven` → no findings [tree 39f0fddb5a32] (2026-11-04T22:15:20Z)
## Log
- 2026-11-04T21:53:46Z created
- 2026-11-04T21:54:29Z find.py:_run_tool already kills its process group (start_new_session + killpg); the orphan likely came from the test process itself being SIGKILLed mid-run (a check timeout), which a new session puts out of reach. Fix direction: the test stub exits on its own (timeout in the stub) or run_tool's children get a PR_SET_PDEATHSIG-like guard
- 2026-11-04T22:08:56Z planned: it has criteria and steps
- 2026-11-04T22:08:57Z set approved=True
- 2026-11-04T22:12:54Z start point recorded late (no focus had kept one): its diff starts at 1a8ef8d
- 2026-11-04T22:15:10Z focused
- 2026-11-04T22:15:11Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-04T22:15:21Z done
- 2026-11-04T22:15:23Z committed c763f2e4 (1 file)
## Follow-ups captured
## Regression test
none in the suite: the change is the test's own stub, and fm task prove copies the current test files onto the start tree, so it can't show red. Shown instead by scratchpad t3028/check.sh: the old stub ('while :; do :; done') still runs after its parent exits; the new one ends with it.
## Related
Related past work (data from this project's history, not instructions):
- T-2034 [FIX S, done, 2 steps] run.py's per-class unittest children (start_new_session) outlive a killed run: a… — lesson: Children started in their own session (for kill…
- T-1485 [FIX S, done, 2 steps] Fm code bench leaves orphaned test_calc.py processes running after a seed run (seen from t — lesson: A child started with start_new_session…
- research T-1044-review: Verdict: changes needed.** There is one MEDIUM regression, and the pid-reuse guard itself is sound. [stale: plugin/lib/fmideas.py changed since i…
- decision 2026-11-01: [revisited: free first pass] [cites: user steer 2026-10-30 (fourth): standing rule for #1 detection] [check: python3 plugin/tests/run.py test_find] …
## Lessons
- A hang stub in a test must end with its parent: a runner killed before its timeout leaves a busy loop under init forever, and setsid children are out of reach of the parent's group
