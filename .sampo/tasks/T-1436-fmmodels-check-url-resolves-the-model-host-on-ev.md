---
id: T-1436
type: PERFORMANCE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-21T21:09:23Z
updated: 2026-10-21T22:51:18Z
base: 9d4f228248add837660426366251f580df7c1b77
base_tree: fdc6e3feec54a8b078c30fdcdccebfe83d0fbc78
plan0_at: 2026-10-21T22:45:23Z
plan0_scope: []
verified: strong
---
# fm code looks up a model host's addresses once a minute, not on every model call
## Raw request
> fmmodels._check_url resolves the model host on every complete() call (T-1432's metadata check); cache the result per host for the run, and note DNS rebinding stays a time-of-check gap
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] two _link_local checks of one hostname within a minute make one getaddrinfo call; a lookup that timed out or failed isn't cached — verify with `python3 plugin/tests/run.py test_code_hardening`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test in test_code_hardening counting patched getaddrinfo calls, then a per-host cache of a successful lookup's addresses for 60 s in fmmodels._link_local
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_code_hardening.MetadataEndpoints` → ✗ exit 1 · Ran 4 tests in 0.7s (1 classes, 16 at a time; slowest: MetadataEndpoints 0s) / FAILED (1 classes) [ran] [tree af3af24eb23e] (2026-10-21T22:45:36Z)
- (step 1) `python3 plugin/tests/run.py test_code_hardening test_runner_lint test_models` → exit 0 · Ran 78 tests in 8.2s (14 classes, 16 at a time; slowest: Bench 8s, RunnerLint 2s, ReviewNits 1s) / OK [ran] [tree 2d972838f964] (2026-10-21T22:45:55Z)
- (ac 1) `python3 plugin/tests/run.py test_code_hardening` → exit 0 · Ran 14 tests in 1.4s (6 classes, 16 at a time; slowest: InlineWorker 1s, ReviewNits 1s, WorkerReadCreatesNothing 1s) / OK [ran] [tree 2fbc14f1d979] (2026-10-21T22:46:09Z)
- (audit intent) `self: only a lookup that answered is kept, keyed by the normalised host, for 60 s; IP literals never reach the cache; a timed-out or failed lookup isn't kept, so the next call tries again; the cached addresses are checked by the same rule every call` → two checks of one host within a minute make one getaddrinfo call (test_code_hardening) [tree 2fbc14f1d979] (2026-10-21T22:46:09Z)
- (audit edge) `self: only a lookup that answered is kept, keyed by the normalised host, for 60 s; IP literals never reach the cache; a timed-out or failed lookup isn't kept, so the next call tries again; the cached addresses are checked by the same rule every call` → a DNS change takes up to a minute to be seen by the check (rebinding was already a time-of-check gap, named in _link_local's docstring) [tree 2fbc14f1d979] (2026-10-21T22:46:09Z)
- (audit self) `self: only a lookup that answered is kept, keyed by the normalised host, for 60 s; IP literals never reach the cache; a timed-out or failed lookup isn't kept, so the next call tries again; the cached addresses are checked by the same rule every call` → no findings [tree 2fbc14f1d979] (2026-10-21T22:46:09Z)
- (audit intent) `self: only a lookup that answered is kept, keyed by the normalised host, for 60 s; IP literals never reach the cache; a timed-out or failed lookup isn't kept; the cached addresses are checked by the same rule every call` → two checks of one host within a minute make one getaddrinfo call (test_code_hardening) [tree 2fbc14f1d979] (2026-10-21T22:48:44Z)
- (audit edge) `self: only a lookup that answered is kept, keyed by the normalised host, for 60 s; IP literals never reach the cache; a timed-out or failed lookup isn't kept; the cached addresses are checked by the same rule every call` → a DNS change takes up to a minute to be seen by the check (rebinding was already a time-of-check gap, named in _link_local's docstring) [tree 2fbc14f1d979] (2026-10-21T22:48:44Z)
- (audit self) `self: only a lookup that answered is kept, keyed by the normalised host, for 60 s; IP literals never reach the cache; a timed-out or failed lookup isn't kept; the cached addresses are checked by the same rule every call` → no findings [tree 2fbc14f1d979] (2026-10-21T22:48:44Z)
## Log
- 2026-10-21T21:09:23Z created
- 2026-10-21T22:45:21Z planned from capture
- 2026-10-21T22:45:22Z focused
- 2026-10-21T22:51:15Z done
- 2026-10-21T22:51:18Z committed e66d9039 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0959 [FEATURE M, done, 3 steps] Brainstorm and cost: keep a child's partial answer, a run manifest, cache-bust causes, friction minutes, unused verbs — lesson: A repor…
- T-1432 [SECURITY M, done, 7 steps] fm code hardening: inline --worker templates linted, more metadata endpoints refused, odd usage counts survived, the pl… — lesson: A l…
- T-1421 [SECURITY S, done, 0 steps] Fm code's model endpoint check: also refuse other cloud metadata addresses (Alibaba 100.10
- decision 2026-10-09: Added JARVIS (<host>) as a fm conductor remote so the Foreman pane shows its sessions as tiles: the user's own host over their own …
- similar finished tasks took 0–7 steps
## Why not caught
none: performance follow-up
## Measurements
host lookups per run: one per model call → one per minute per host (test_code_hardening counts getaddrinfo: 2 checks → 1 call); with a slow resolver at the 2 s cap, a 30-call run spent up to 60 s on lookups → up to 2 s per minute of run
## Lessons
- Cache only answers, never failures, when a lookup guards a security check
## Plan gaps
- failed first: step 1 failing test in test_code_hardening counting patched getaddrinfo calls, then a per-host cache of a …
## Files touched
- plugin/tests/test_code_hardening.py
- plugin/lib/fmmodels.py
- CHANGELOG.md
