---
id: T-0397
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T02:48:52Z
updated: 2026-10-09T02:51:27Z
base: 6dc533cb6a6ab55fa41cae478aa327719a16d606
base_tree: 1e9d9dcfb4c82dd6dfb335f929e2e5b649b663fa
verified: strong
---
# Guard: curl -m/--max-time and nvidia-smi beside a data-reading python -c count as writing files (JARVIS: curl -s -m 5 127.0.0.1:9000/running | python3 -c …; nvidia-smi)
## Raw request
> Guard: curl -m/--max-time and nvidia-smi beside a data-reading python -c count as writing files (JARVIS: curl -s -m 5 127.0.0.1:9000/running | python3 -c …; nvidia-smi)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] timing and stdout-only curl flags and nvidia-smi without -f pass; -o, -K, a non-numeric -m and nvidia-smi -f still block — verify with `python3 plugin/tests/run.py -k test_timing_flags_and_nvidia_smi_write_nothing`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first, then widen _writes_nothing
## Resume here
## Docs impact
CHANGELOG Unreleased
## Verification evidence
- `python3 plugin/tests/run.py -k test_timing_flags_and_nvidia_smi_write_nothing` → ✗ exit 1 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: DataTools 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree db4b6d675b91] (2026-10-09T02:49:16Z)
- `python3 plugin/tests/run.py -k test_timing_flags_and_nvidia_smi_write_nothing` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: DataTools 0s) / OK [ran] [tree db4b6d675b91] (2026-10-09T02:49:16Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (27 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                32.4    35.4     150  [0] / SessionEnd                  29.1    30.7     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 00:30 UTC; python3 plugin/tests/run.py → exit 0 · Ran 935 tests in [ran] [tree 0166dde3c3b0] (2026-10-09T02:50:54Z)
- (ac 1) `python3 plugin/tests/run.py -k test_timing_flags_and_nvidia_smi_write_nothing` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: DataTools 0s) / OK [ran] [tree 0166dde3c3b0] (2026-10-09T02:51:26Z)
- (audit adversary) `self adversary pass + the row table (5 refusals kept, 5 forms allowed) + replay (0 newly allowed) + real-bash differential suite` → only numeric timeout values are skipped; a fused write flag (-sm5o), -o, -K, a stderr redirect, and nvidia-smi -f/--filename/dmon -f all still refuse; a ./tool named like a data tool was already trusted by name (pre-existing, the agent's own file, not a download) [tree 0166dde3c3b0] (2026-10-09T02:51:26Z)
- (audit intent) `self adversary pass + the row table (5 refusals kept, 5 forms allowed) + replay (0 newly allowed) + real-bash differential suite` → JARVIS's curl -s -m 5 127.0.0.1:9000/running | python3 -c …; nvidia-smi line passes (test) [tree 0166dde3c3b0] (2026-10-09T02:51:26Z)
- (audit edge) `self adversary pass + the row table (5 refusals kept, 5 forms allowed) + replay (0 newly allowed) + real-bash differential suite` → --max-time=5 and --max-time 5 both pass; --format=csv on nvidia-smi isn't mistaken for -f [tree 0166dde3c3b0] (2026-10-09T02:51:26Z)
- (audit self) `self adversary pass + the row table (5 refusals kept, 5 forms allowed) + replay (0 newly allowed) + real-bash differential suite` → no findings [tree 0166dde3c3b0] (2026-10-09T02:51:26Z)
## Log
- 2026-10-09T02:48:52Z created
- 2026-10-09T02:48:52Z focused
- 2026-10-09T02:51:27Z done
- 2026-10-09T02:51:27Z committed 05151e4 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0354 [SECURITY S, done, 1 steps] Guard: the curl-into-python data exemption also refuses a folder that shadows any standard-library module — lesson: An existence check…
- research mission-20261008-195201.pack: super improve foreman
- T-0395 [CLEAN S, done, 1 steps] Guard: the pipe-shell refusal of curl | python3 -c should say how it passes (JARVIS lost a turn: hf download > log on the same line)
- decision 2026-10-08: T-0368: entry points re-exec under a saved supported Python
- similar finished tasks took 1–1 steps
- start here (files T-0354 touched): plugin/tests/test_guard.py, plugin/lib/fmguard.py, CHANGELOG.md
## Lessons
- A data-tool allowlist grows from real refusals: add the exact flags seen, numeric values only, with the write flags beside them as refusal rows
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- CHANGELOG.md
