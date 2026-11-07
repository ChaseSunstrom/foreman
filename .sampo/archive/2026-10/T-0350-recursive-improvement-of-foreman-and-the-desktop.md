---
id: T-0350
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-06T03:48:50Z
updated: 2026-10-06T03:49:16Z
base: d1fdbc0758b37e1833248944fc24a0f31ec75b36
base_tree: 4848aa4d9c280b32f9da5f7eb5099cbf279f3b71
verified: strong
---
# Recursive improvement of Foreman and the desktop app after v2 (T-0329): four app rounds and the self-improvement fixes
## Raw request
> Recursive improvement of Foreman and the desktop app after v2 (T-0329): four app rounds and the self-improvement fixes
## Interpretation
The user's open-ended 'recursively improve yourself and the desktop app' (T-0329), bounded for this run: one friction pass (recon → T-0330..T-0334) plus what this session's friction showed (T-0315, T-0340, T-0342..T-0345, T-0349), and four app rounds from a brainstorm (decisions/blocked, usage meter, health + capture, review). Later rounds come from fm friction --every 3 and /foreman:brainstorm.
## Assumptions (confidence)
## Acceptance criteria
- [x] the self-improvement fixes and the four app rounds pass their tests — verify with `python3 plugin/tests/run.py -k test_guard -k test_agents -k test_projects -k test_cli -k test_recall -k test_unattended`
- [x] the app type-checks and its transport tests pass — verify with `bash -c 'cd ~/projects/foreman-desktop && bun run check && cd src-tauri && cargo test --target-dir /tmp/claude-1000/-home-~--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/cargo-target 2>&1 | grep -q "test result: ok. 9 passed"'`
## Non-goals
## Approach (options → choice → why)
(A) Bound the umbrella to the rounds done and let the friction loop carry the rest. (B) Keep it open — it would sit at the head of the queue and drive could never finish. Choice A.
## Risks and rollback
## Execution prompt
## Steps
1. [x] rounds shipped as T-0341, T-0346, T-0347, T-0348; fixes T-0330..T-0345, T-0349
## Resume here
## Docs impact
CHANGELOG; app README
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py -k test_guard -k test_agents -k test_projects -k test_cli -k test_recall -k test_unattended` → exit 0 · Ran 187 tests in 15.3s (57 classes, 16 at a time; slowest: TaskLifecycle 15s, Recall 11s, StateViews 6s) / OK [ran] [tree 4848aa4d9c28] (2026-10-06T03:49:16Z)
- (ac 2) `bash -c 'cd ~/projects/foreman-desktop && bun run check && cd src-tauri && cargo test --target-dir /tmp/claude-1000/-home-~--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/cargo-target 2>&1 | grep -q "test result: ok. 9 passed"'` → exit 0 · 1791258556197 START "~/projects/foreman-desktop" / 1791258556198 COMPLETED 200 FILES 0 ERRORS 0 WARNINGS 0 FILES_WITH_PROBLEMS [ran] [tree 4848aa4d9c28] (2026-10-06T03:49:16Z)
- (step 1) `python3 plugin/tests/run.py -k test_guard -k test_agents -k test_projects -k test_cli -k test_recall -k test_unattended` → exit 0 · Ran 187 tests in 15.3s (57 classes, 16 at a time; slowest: TaskLifecycle 15s, Recall 11s, StateViews 6s) / OK [ran] [tree 4848aa4d9c28] (2026-10-06T03:49:16Z)
- (audit intent) `each round and fix closed with its own evidence, audits and commits (T-0330..T-0349); their tests and the app's checks re-run together here` → the user's 'recursively improve yourself and the desktop app' got a friction pass, the Foreman fixes it and this run's own friction found (four guard bypasses caught by adversary reviews before they shipped), and four app rounds grounded in a brainstorm; later rounds come from the friction loop [tree 4848aa4d9c28] (2026-10-06T03:49:16Z)
- (audit adversary) `each round and fix closed with its own evidence, audits and commits (T-0330..T-0349); their tests and the app's checks re-run together here` → the guard changes in this run were reviewed adversarially (T-0338, T-0339, T-0344) and each review's bypasses fixed test-first; the replay corpus shows no unintended verdicts [tree 4848aa4d9c28] (2026-10-06T03:49:16Z)
## Log
- 2026-10-06T03:48:50Z created
- 2026-10-06T03:48:58Z focused
- 2026-10-06T03:49:16Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0329 [FEATURE M, dropped, 1 steps] Recursive improvement of Foreman and the desktop app after v2: four app rounds and the self-improvement fixes
- T-0258 [RESEARCH L, done, 4 steps] After all of that, recursively brainstorm and improve yourself — lesson: Recursive brainstorming converges fast once each pass is grou…
- T-0125 [FEATURE M, done, 4 steps] Recursive self-improvement loop: fm friction digests Foreman's own friction since the last pass, fm next calls for a pass every N close…
- decision 2026-09-27: Recursion bound for T-0063: after R5, one more round (R6: auto-evidence from Bash results matching a criterion's verify command) from the existing R…
- similar finished tasks took 4–4 steps
## Lessons
- An open-ended 'keep improving' request needs a bound per run (rounds shipped + a loop for the rest), or it sits at the head of the queue forever.
