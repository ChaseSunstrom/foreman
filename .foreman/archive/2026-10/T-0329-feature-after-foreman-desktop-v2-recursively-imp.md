---
id: T-0329
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-06T02:02:33Z
updated: 2026-10-06T03:48:50Z
base: d1fdbc0758b37e1833248944fc24a0f31ec75b36
base_tree: 4848aa4d9c280b32f9da5f7eb5099cbf279f3b71
---
# Recursive improvement of Foreman and the desktop app after v2: four app rounds and the self-improvement fixes
## Raw request
> FEATURE: after Foreman Desktop v2 (#T-0328): recursively improve Foreman itself and the desktop app — super improvements: self-improvement passes (fm friction / /foreman:improve) and brainstorm-driven improvement rounds on the app, each grounded, built and verified
## Interpretation
Open-ended 'keep improving' request, bounded here: one friction pass (recon → T-0330..T-0334, built as T-0333/T-0338/T-0339) plus what this session's own friction showed (T-0315, T-0340, T-0342..T-0345, T-0349), and four app rounds from a brainstorm (decisions/blocked, usage meter, health + capture, review). Later rounds come from fm friction --every 3 and /foreman:brainstorm.
## Assumptions (confidence)
## Acceptance criteria
- [ ] the self-improvement fixes and the four app rounds pass their tests — verify with `python3 plugin/tests/run.py -k 'test_guard or test_agents or test_projects or test_cli or test_recall or test_unattended'`
- [x] the app type-checks and its transport tests pass — verify with `bash -c 'cd ~/projects/foreman-desktop && bun run check && cd src-tauri && cargo test --target-dir /tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/cargo-target 2>&1 | grep -q "test result: ok. 9 passed"'`
## Non-goals
## Approach (options → choice → why)
(A) Bound the umbrella to the rounds done and let the friction loop carry the rest. (B) Keep it open forever — it would sit at the head of the queue and block drive from ever finishing. Choice A.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] rounds shipped as T-0341, T-0346, T-0347, T-0348; fixes T-0330..T-0345, T-0349  <- CURRENT
## Resume here
## Docs impact
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py -k 'test_guard or test_agents or test_projects or test_cli or test_recall or test_unattended'` → ✗ exit 1 · Ran 0 tests in 0.1s (0 classes, 16 at a time; slowest: ) / NO TESTS RAN [ran] [tree 4848aa4d9c28] (2026-10-06T03:48:35Z)
- (ac 2) `bash -c 'cd ~/projects/foreman-desktop && bun run check && cd src-tauri && cargo test --target-dir /tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/cargo-target 2>&1 | grep -q "test result: ok. 9 passed"'` → exit 0 · 1791258515447 START "~/projects/foreman-desktop" / 1791258515448 COMPLETED 200 FILES 0 ERRORS 0 WARNINGS 0 FILES_WITH_PROBLEMS [ran] [tree 4848aa4d9c28] (2026-10-06T03:48:35Z)
- (step 1) `python3 plugin/tests/run.py -k 'test_guard or test_agents or test_projects or test_cli or test_recall or test_unattended'` → ✗ exit 1 · Ran 0 tests in 0.1s (0 classes, 16 at a time; slowest: ) / NO TESTS RAN [ran] [tree 4848aa4d9c28] (2026-10-06T03:48:35Z)
## Log
- 2026-10-06T02:02:33Z created
- 2026-10-06T03:48:27Z planned from capture
- 2026-10-06T03:48:27Z focused
- 2026-10-06T03:48:50Z dropped: criterion 1's verify used '-k a or b', which run.py doesn't read (it ran no tests); a checked criterion can't be edited (T-0342), so it's recreated with repeated -k
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0125 [FEATURE M, done, 4 steps] Recursive self-improvement loop: fm friction digests Foreman's own friction since the last pass, fm next calls for a pass every N close…
- T-0071 [FEATURE L, done, 5 steps] Super-brainstorm (recursive multi-round fm ideas) + implement every grounded idea and the inbox, recursing until dry; candidate improve…
- research brainstorm-20261003-round5: Quota brake (bold bets) → T-0198 economy mode: the mod reads session.usage rate limits; past 80% weekly / 90% 5-hour a prompt.compos…
- decision 2026-10-03: Brainstorm recursion stops at round 5: the 2×2 probe grounded 1 idea of real value (built as T-0198); further improvement comes from friction passes…
