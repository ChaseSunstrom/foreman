---
id: T-0405
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T04:18:42Z
updated: 2026-10-09T04:19:47Z
base: db6e495ec7b114f5d74fdc56372d609604ddf713
base_tree: fd40930828063c19fbf9e85d2b03a82df397db09
verified: strong
---
# Foreman 1.2.10: lane merge beside uncommitted work, focus-in-the-line hint (T-0403, T-0404) to GitHub main and JARVIS
## Raw request
> Foreman 1.2.10: lane merge beside uncommitted work, focus-in-the-line hint (T-0403, T-0404) to GitHub main and JARVIS
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
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (28 pass, 3 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · skipped: nothing under plugin/lib/**, plugin/hooks/**, plugin/bin/**, plugin/tests/bench_hooks.py, plugin/tests/fixtures/** changed since its pass at 04:18 UTC; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 00:30 UTC; pytho [ran] [tree 06ac4f982211] (2026-10-09T04:19:32Z)
- (step 2) `git -C ~/.claude/foreman merge-base --is-ancestor HEAD origin/main` → exit 0 · (no output) [ran] [tree 06ac4f982211] (2026-10-09T04:19:46Z)
- (ac 1) `git -C ~/.claude/foreman merge-base --is-ancestor HEAD origin/main` → exit 0 · (no output) [ran] [tree 06ac4f982211] (2026-10-09T04:19:46Z)
- (audit intent) `self: gate green; pushed to main; JARVIS fast-forwarded from a clean tree, install updated` → main and JARVIS carry 1.2.10 [tree 06ac4f982211] (2026-10-09T04:19:46Z)
- (audit self) `self: gate green; pushed to main; JARVIS fast-forwarded from a clean tree, install updated` → no findings [tree 06ac4f982211] (2026-10-09T04:19:46Z)
## Log
- 2026-10-09T04:18:42Z created
- 2026-10-09T04:18:42Z focused
- 2026-10-09T04:19:47Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0396 [FIX S, done, 2 steps] Foreman 1.2.6: the merge and pipe-shell refusal hints (T-0394, T-0395) to GitHub main and JARVIS
- T-0398 [FIX S, done, 2 steps] Foreman 1.2.7: curl timeouts and nvidia-smi beside a data-reading python -c (T-0397) to GitHub main and JARVIS
- T-0403 [FIX S, done, 1 steps] fm lane merge refuses any dirty main checkout; the main thread is mid-task while lanes finish (JARVIS: T-0280 couldn't land during T-0278) …
- decision 2026-10-04: T-0234 builder lanes: use Claude Code's Agent isolation worktree plus fm focus inside it, not fm lane's sibling folders
- similar finished tasks took 1–2 steps
## Regression test
none: a release; the gate ran the full suite on the released tree
## Files touched
- .claude-plugin/marketplace.json
- CHANGELOG.md
- plugin/.claude-plugin/plugin.json
