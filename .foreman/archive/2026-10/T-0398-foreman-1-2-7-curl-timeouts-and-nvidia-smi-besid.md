---
id: T-0398
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T02:51:33Z
updated: 2026-10-09T02:52:54Z
base: 05151e4268aeb4a555d75b095f1fe0231f3c15a9
base_tree: 0166dde3c3b05103e542338b8fa1d57e2ea4f3fa
verified: strong
---
# Foreman 1.2.7: curl timeouts and nvidia-smi beside a data-reading python -c (T-0397) to GitHub main and JARVIS
## Raw request
> Foreman 1.2.7: curl timeouts and nvidia-smi beside a data-reading python -c (T-0397) to GitHub main and JARVIS
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
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (28 pass, 3 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · skipped: nothing under plugin/lib/**, plugin/hooks/**, plugin/bin/**, plugin/tests/bench_hooks.py, plugin/tests/fixtures/** changed since its pass at 02:50 UTC; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 00:30 UTC; pytho [ran] [tree 58fee916be18] (2026-10-09T02:52:38Z)
- (step 2) `git -C ~/.claude/foreman merge-base --is-ancestor HEAD origin/main` → exit 0 · (no output) [ran] [tree 58fee916be18] (2026-10-09T02:52:54Z)
- (ac 1) `git -C ~/.claude/foreman merge-base --is-ancestor HEAD origin/main` → exit 0 · (no output) [ran] [tree 58fee916be18] (2026-10-09T02:52:54Z)
- (audit intent) `self: gate green; pushed to main; JARVIS fast-forwarded from a clean tree, install updated` → main and JARVIS carry 1.2.7 [tree 58fee916be18] (2026-10-09T02:52:54Z)
- (audit self) `self: gate green; pushed to main; JARVIS fast-forwarded from a clean tree, install updated` → no findings [tree 58fee916be18] (2026-10-09T02:52:54Z)
## Log
- 2026-10-09T02:51:33Z created
- 2026-10-09T02:51:34Z focused
- 2026-10-09T02:52:54Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0397 [FIX S, done, 1 steps] Guard: curl -m/--max-time and nvidia-smi beside a data-reading python -c count as writing files (JARVIS: curl -s -m 5 127.0.0.1:9000/runnin…
- research mission-20261008-195201.pack: super improve foreman
- T-0395 [CLEAN S, done, 1 steps] Guard: the pipe-shell refusal of curl | python3 -c should say how it passes (JARVIS lost a turn: hf download > log on the same line)
- decision 2026-10-09: [outward] Updating Foreman on JARVIS (merge to main, pull, plugin update, reload) as fixes land during the monitoring
- similar finished tasks took 1–1 steps
- start here (files T-0397 touched): plugin/tests/test_guard.py, plugin/lib/fmguard.py, CHANGELOG.md
## Regression test
none: a release; the gate ran the full suite on the released tree
## Files touched
- .claude-plugin/marketplace.json
- CHANGELOG.md
- plugin/.claude-plugin/plugin.json
