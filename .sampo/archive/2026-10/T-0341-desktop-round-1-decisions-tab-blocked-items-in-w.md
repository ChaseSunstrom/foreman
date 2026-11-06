---
id: T-0341
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-06T03:19:31Z
updated: 2026-10-06T03:22:42Z
base: 167b4bec7045a1dc7703a3d7db77ac740fa93780
base_tree: e765e0f5aa135a59d53ce5b2e9a8deea1a349db8
verified: strong
---
# Desktop round 1: decisions tab, blocked items in Waiting on you, agent unwire; fm decide --list --json rows
## Raw request
> Desktop round 1: decisions tab, blocked items in Waiting on you, agent unwire; fm decide --list --json rows
## Interpretation
First grounded round of T-0329: what only the user can unblock (blocked reasons, autonomous costly/outward decisions) becomes visible in the app; the Agents page can undo wiring by the user's click.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm decide --list --json gives rows with date, kind, text, why, reversed — verify with `python3 plugin/tests/run.py -k test_cli.DecideRows`
- [x] the app type-checks and builds — verify with `bash -c 'cd ~/projects/foreman-desktop && bun run check'`
## Non-goals
## Approach (options → choice → why)
(A) Additive rows field on fm decide --list --json, parsed in Foreman from decisions.md, rendered by a Decisions tab fetched on open; Home lists projects with blocked tasks next to waits. (B) Parse the markdown strings in the app — duplicates the format knowledge in TypeScript. Choice A.
## Risks and rollback
## Execution prompt
## Steps
1. [x] fm: structured decision rows (red→green)
2. [x] app: Decisions tab, blocked in Waiting on you, agents Remove
3. [x] verify in the running app (screenshots)
## Resume here
## Docs impact
CHANGELOG; app README
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_cli.DecideRows` → ✗ exit 1 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: DecideRows 0s) / FAILED (1 classes) [ran] [tree 64d246a08513] (2026-10-06T03:19:38Z)
- (step 1) `python3 plugin/tests/run.py -k test_cli.DecideRows` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: DecideRows 0s) / OK [ran] [tree ab2a16632e48] (2026-10-06T03:22:25Z)
- (step 2) `bash -c 'cd ~/projects/foreman-desktop && bun run check && cd src-tauri && cargo test --target-dir /tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/cargo-target 2>&1 | grep -E "test result: ok. 9"'` → exit 0 · 1791256947560 COMPLETED 199 FILES 0 ERRORS 0 WARNINGS 0 FILES_WITH_PROBLEMS / test result: ok. 9 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.39s [ran] [tree ab2a16632e48] (2026-10-06T03:22:29Z)
- (step 3) `ls /tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/r1-decisions2.png /tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/r1-home.png` → exit 0 · /tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/r1-decisions2.png / /tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scrat [ran] [tree ab2a16632e48] (2026-10-06T03:22:29Z)
- (ac 1) `python3 plugin/tests/run.py -k test_cli.DecideRows` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: DecideRows 0s) / OK [ran] [tree ab2a16632e48] (2026-10-06T03:22:42Z)
- (ac 2) `bash -c 'cd ~/projects/foreman-desktop && bun run check'` → exit 0 · 1791256962288 START "~/projects/foreman-desktop" / 1791256962289 COMPLETED 199 FILES 0 ERRORS 0 WARNINGS 0 FILES_WITH_PROBLEMS [ran] [tree ab2a16632e48] (2026-10-06T03:22:42Z)
- (audit intent) `self-review of both diffs; app type-check clean, 9 Rust tests incl. allow-list (decide only with --list/--review), screenshots of Decisions tab, Home and Agents in the running app` → blocked tasks and autonomous costly/outward decisions are now visible where the user looks first; Remove undoes wiring by click [tree ab2a16632e48] (2026-10-06T03:22:42Z)
- (audit adversary) `self-review of both diffs; app type-check clean, 9 Rust tests incl. allow-list (decide only with --list/--review), screenshots of Decisions tab, Home and Agents in the running app` → the app's allow-list admits fm decide only with --list or --review (recording a decision stays the agent's); Remove runs fm agents uninstall from the user's click, outside any agent hook, which is the intended path [tree ab2a16632e48] (2026-10-06T03:22:42Z)
## Log
- 2026-10-06T03:19:31Z created
- 2026-10-06T03:19:31Z focused
- 2026-10-06T03:22:39Z scope: app repo ~/projects/foreman-desktop (committed there as 6a81399)
- 2026-10-06T03:22:42Z done
- 2026-10-06T03:22:42Z committed 62505d7 (3 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- playbook Release and changelog (skills/playbooks/references/release/release-and-changelog.md)
- T-0057 [FEATURE M, done, 0 steps] Decisions record reversibility (reversible, costly, outward); later reversals listed by fm
- research brainstorm-20261002-round2: Source: research/brainstorm-20261002-145137 (3 lenses, 21 ideas) merged with own list; user steer: queue/inbox/activity must match t…
- research brainstorm-20261002-super: 171 titles (6 lenses × 2 rounds + 3 deepen rounds: speed, gates, autonomy). Grounded against the code:
- the similar finished task took 0 steps
## Lessons
- A UI that shows what only the user can unblock is worth more than another control: blocked reasons and costly decisions were already in Foreman's state, just never in front of the user.
## Files touched
- plugin/tests/test_cli.py
- plugin/lib/fmcli.py
- CHANGELOG.md
