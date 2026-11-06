---
id: T-0396
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T02:43:30Z
updated: 2026-10-09T02:44:39Z
base: e0f4cb742ef10bbae2926b82f4d039ab642d835d
base_tree: 62006891c3e42bff0f8c71ea62d5ea3331b8db63
verified: strong
---
# Foreman 1.2.6: the merge and pipe-shell refusal hints (T-0394, T-0395) to GitHub main and JARVIS
## Raw request
> Foreman 1.2.6: the merge and pipe-shell refusal hints (T-0394, T-0395) to GitHub main and JARVIS
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] origin/main contains HEAD — verify with `git -C ~/.claude/foreman merge-base --is-ancestor HEAD origin/main`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] bump, gate, commit
2. [x] merge in a scratch clone, push; fast-forward JARVIS
## Resume here
## Docs impact
## Verification evidence
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (28 pass, 3 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · skipped: nothing under plugin/lib/**, plugin/hooks/**, plugin/bin/**, plugin/tests/bench_hooks.py, plugin/tests/fixtures/** changed since its pass at 02:43 UTC; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 00:30 UTC; pytho [ran] [tree 1e9d9dcfb4c8] (2026-10-09T02:44:19Z)
- (step 2) `git -C ~/.claude/foreman merge-base --is-ancestor HEAD origin/main` → exit 0 · (no output) [ran] [tree 1e9d9dcfb4c8] (2026-10-09T02:44:39Z)
- (ac 1) `git -C ~/.claude/foreman merge-base --is-ancestor HEAD origin/main` → exit 0 · (no output) [ran] [tree 1e9d9dcfb4c8] (2026-10-09T02:44:39Z)
- (audit intent) `self: gate green; pushed 2da2fd6 to main (owner's yes for main pushes); JARVIS fast-forwarded from a clean tree and its install updated` → main and JARVIS carry 1.2.6 [tree 1e9d9dcfb4c8] (2026-10-09T02:44:39Z)
- (audit self) `self: gate green; pushed 2da2fd6 to main (owner's yes for main pushes); JARVIS fast-forwarded from a clean tree and its install updated` → no findings [tree 1e9d9dcfb4c8] (2026-10-09T02:44:39Z)
## Log
- 2026-10-09T02:43:30Z created
- 2026-10-09T02:43:30Z focused
- 2026-10-09T02:44:39Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0395 [CLEAN S, done, 1 steps] Guard: the pipe-shell refusal of curl | python3 -c should say how it passes (JARVIS lost a turn: hf download > log on the same line)
- T-0366 [FIX M, done, 3 steps] Ship T-0364 to JARVIS: merge its 2 local commits into main, bump plugin to 1.2.0, refresh its plugin cache — lesson: A directory-marketplac…
- T-0379 [FIX S, done, 1 steps] Builder brief: start from the main checkout's commit; isolation refusals are reported for the main thread, not retried — lesson: Watch the …
- decision 2026-10-09: [outward] Updating Foreman on JARVIS (merge to main, pull, plugin update, reload) as fixes land during the monitoring
- similar finished tasks took 1–3 steps
## Regression test
none: a release; the gate ran the full suite on the released tree
## Files touched
- .claude-plugin/marketplace.json
- CHANGELOG.md
- plugin/.claude-plugin/plugin.json
