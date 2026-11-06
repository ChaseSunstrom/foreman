---
id: T-0400
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T02:58:43Z
updated: 2026-10-09T02:59:52Z
base: b860a14e1185492db7700718fe69205d2371d97e
base_tree: 121f1989765fd0f305919cef691940be142e0c68
verified: strong
---
# Foreman 1.2.8: builder briefs say edit with Edit/Write (T-0399) to GitHub main and JARVIS
## Raw request
> Foreman 1.2.8: builder briefs say edit with Edit/Write (T-0399) to GitHub main and JARVIS
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
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (28 pass, 3 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · skipped: nothing under plugin/lib/**, plugin/hooks/**, plugin/bin/**, plugin/tests/bench_hooks.py, plugin/tests/fixtures/** changed since its pass at 02:58 UTC; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 00:30 UTC; pytho [ran] [tree e07045952de8] (2026-10-09T02:59:33Z)
- (step 2) `git -C ~/.claude/foreman merge-base --is-ancestor HEAD origin/main` → exit 0 · (no output) [ran] [tree e07045952de8] (2026-10-09T02:59:52Z)
- (ac 1) `git -C ~/.claude/foreman merge-base --is-ancestor HEAD origin/main` → exit 0 · (no output) [ran] [tree e07045952de8] (2026-10-09T02:59:52Z)
- (audit intent) `self: gate green; pushed to main; JARVIS fast-forwarded from a clean tree, install updated` → main and JARVIS carry 1.2.8 [tree e07045952de8] (2026-10-09T02:59:52Z)
- (audit self) `self: gate green; pushed to main; JARVIS fast-forwarded from a clean tree, install updated` → no findings [tree e07045952de8] (2026-10-09T02:59:52Z)
## Log
- 2026-10-09T02:58:43Z created
- 2026-10-09T02:58:43Z focused
- 2026-10-09T02:59:52Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0399 [FIX S, done, 1 steps] Builder brief: edit files with the Edit/Write tools, never shell heredocs (JARVIS builders: 5 'too complex' isolation refusals in 10 min on…
- T-0396 [FIX S, done, 2 steps] Foreman 1.2.6: the merge and pipe-shell refusal hints (T-0394, T-0395) to GitHub main and JARVIS
- T-0398 [FIX S, done, 2 steps] Foreman 1.2.7: curl timeouts and nvidia-smi beside a data-reading python -c (T-0397) to GitHub main and JARVIS
- decision 2026-10-09: [outward] Updating Foreman on JARVIS (merge to main, pull, plugin update, reload) as fixes land during the monitoring
- similar finished tasks took 1–2 steps
- start here (files T-0399 touched): plugin/tests/test_builder.py, plugin/lib/fmlanes.py, CHANGELOG.md
## Regression test
none: a release; the gate ran the full suite on the released tree
## Files touched
- .claude-plugin/marketplace.json
- CHANGELOG.md
- plugin/.claude-plugin/plugin.json
