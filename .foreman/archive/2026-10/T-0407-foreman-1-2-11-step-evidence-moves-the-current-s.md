---
id: T-0407
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T04:27:49Z
updated: 2026-10-09T04:29:03Z
base: 6eca3f8691fbb2d307815083f5e1ef09293fc577
base_tree: bbe286371051ae63fd81aaf27349be598bee45c3
verified: strong
---
# Foreman 1.2.11: step evidence moves the current step (T-0406) to GitHub main and JARVIS
## Raw request
> Foreman 1.2.11: step evidence moves the current step (T-0406) to GitHub main and JARVIS
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
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (28 pass, 3 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · skipped: nothing under plugin/lib/**, plugin/hooks/**, plugin/bin/**, plugin/tests/bench_hooks.py, plugin/tests/fixtures/** changed since its pass at 04:27 UTC; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 00:30 UTC; pytho [ran] [tree a30908832128] (2026-10-09T04:28:44Z)
- (step 2) `git -C ~/.claude/foreman merge-base --is-ancestor HEAD origin/main` → exit 0 · (no output) [ran] [tree a30908832128] (2026-10-09T04:29:03Z)
- (ac 1) `git -C ~/.claude/foreman merge-base --is-ancestor HEAD origin/main` → exit 0 · (no output) [ran] [tree a30908832128] (2026-10-09T04:29:03Z)
- (audit intent) `self: gate green; pushed to main; JARVIS fast-forwarded from a clean tree, install updated; T-0278's stale steps ticked from their own passing evidence` → main and JARVIS carry 1.2.11; JARVIS's band now shows T-0278's real progress [tree a30908832128] (2026-10-09T04:29:03Z)
- (audit self) `self: gate green; pushed to main; JARVIS fast-forwarded from a clean tree, install updated; T-0278's stale steps ticked from their own passing evidence` → no findings [tree a30908832128] (2026-10-09T04:29:03Z)
## Log
- 2026-10-09T04:27:49Z created
- 2026-10-09T04:27:49Z focused
- 2026-10-09T04:29:03Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0406 [FIX M, done, 3 steps] Evidence for a step should move the UI's current step there (JARVIS: steps 3-5 proven, band stuck on step 1/5 — only finish ticks steps) — …
- T-0396 [FIX S, done, 2 steps] Foreman 1.2.6: the merge and pipe-shell refusal hints (T-0394, T-0395) to GitHub main and JARVIS
- T-0402 [FIX S, done, 2 steps] Foreman 1.2.9: the drive offers queued work during background jobs (T-0401) to GitHub main and JARVIS
- decision 2026-10-09: [outward] Updating Foreman on JARVIS (merge to main, pull, plugin update, reload) as fixes land during the monitoring
- similar finished tasks took 2–3 steps
## Regression test
none: a release; the gate ran the full suite on the released tree
## Files touched
- .claude-plugin/marketplace.json
- CHANGELOG.md
- plugin/.claude-plugin/plugin.json
