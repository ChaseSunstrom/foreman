---
id: T-0347
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-06T03:43:01Z
updated: 2026-10-06T03:45:24Z
base: 5f0e8122076222ddb1baf012e6b8a7702faf0ffe
base_tree: a7c4b0d0325c905b0182f272d0918ddd7a77154d
verified: strong
---
# Desktop round 3: device health from fm doctor, a global quick capture (Ctrl Shift C)
## Raw request
> Desktop round 3: device health from fm doctor, a global quick capture (Ctrl Shift C)
## Interpretation
Round 3 of T-0329 from brainstorm-20261005-224118 (user value, unspoken needs): see each device's Foreman health at a glance, and capture an idea into any project's inbox without navigating there.
## Assumptions (confidence)
## Acceptance criteria
- [x] the app runs only a read-only fm doctor (--json alone) and capture from anywhere; Rust allow-list tests pass — verify with `bash -c 'cd ~/projects/foreman-desktop/src-tauri && cargo test --target-dir /tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/cargo-target 2>&1 | grep -q "test result: ok. 9 passed"'`
- [x] the app type-checks — verify with `bash -c 'cd ~/projects/foreman-desktop && bun run check'`
## Non-goals
## Approach (options → choice → why)
(A) fm doctor --json once per device on connect and on demand (it takes ~7 s; no polling), its FAIL count as a sidebar mark and the non-PASS checks on the Devices page; a capture sheet sharing New session's sheet styles (moved to app.css under .sheet). (B) Poll doctor on the projects stream — 7 s per tick per device is too costly. Choice A.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Rust: doctor in the allow-list, JSON answers kept on a non-zero exit
2. [x] UI: health dot + Devices health panel; capture sheet + shortcut + palette
3. [x] verify on screen
## Resume here
## Docs impact
CHANGELOG; app README
## Verification evidence
- (step 1) `bash -c 'cd ~/projects/foreman-desktop/src-tauri && cargo test --target-dir /tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/cargo-target 2>&1 | grep -q "test result: ok. 9 passed"'` → ✗ exit 1 · (no output) [ran] [tree a7c4b0d0325c] (2026-10-06T03:43:10Z)
- (step 1) `bash -c 'cd ~/projects/foreman-desktop && bun run check && ls /tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/r3-devices.png'` → exit 0 · 1791258316782 COMPLETED 200 FILES 0 ERRORS 0 WARNINGS 0 FILES_WITH_PROBLEMS / /tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/r3-devices.png [ran] [tree 30501586cacd] (2026-10-06T03:45:16Z)
- (step 2) `bash -c 'cd ~/projects/foreman-desktop && bun run check && ls /tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/r3-devices.png'` → exit 0 · 1791258318788 COMPLETED 200 FILES 0 ERRORS 0 WARNINGS 0 FILES_WITH_PROBLEMS / /tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/r3-devices.png [ran] [tree 30501586cacd] (2026-10-06T03:45:18Z)
- (step 3) `bash -c 'cd ~/projects/foreman-desktop && bun run check && ls /tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/r3-devices.png'` → exit 0 · 1791258320792 COMPLETED 200 FILES 0 ERRORS 0 WARNINGS 0 FILES_WITH_PROBLEMS / /tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/r3-devices.png [ran] [tree 30501586cacd] (2026-10-06T03:45:20Z)
- (ac 1) `bash -c 'cd ~/projects/foreman-desktop/src-tauri && cargo test --target-dir /tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/cargo-target 2>&1 | grep -q "test result: ok. 9 passed"'` → exit 0 · (no output) [ran] [tree 30501586cacd] (2026-10-06T03:45:24Z)
- (ac 2) `bash -c 'cd ~/projects/foreman-desktop && bun run check'` → exit 0 · 1791258324683 START "~/projects/foreman-desktop" / 1791258324684 COMPLETED 200 FILES 0 ERRORS 0 WARNINGS 0 FILES_WITH_PROBLEMS [ran] [tree 30501586cacd] (2026-10-06T03:45:24Z)
- (audit intent) `self-review of the app diff; cargo tests 9/9 incl. allow-list (doctor only with --json; --repair/--restore-state refused); type-check clean; Devices health panel and the capture sheet verified in screenshots` → health at a glance (28/30, two real warnings shown) and capture from anywhere, both from the brainstorm's top user-value ideas [tree 30501586cacd] (2026-10-06T03:45:24Z)
- (audit adversary) `self-review of the app diff; cargo tests 9/9 incl. allow-list (doctor only with --json; --repair/--restore-state refused); type-check clean; Devices health panel and the capture sheet verified in screenshots` → doctor can't repair or move state from the app; capture only adds an inbox item (Foreman's own capture rules apply); a non-zero exit is kept as an answer only when stdout is a JSON object, so refusals (stderr, empty stdout) still fail [tree 30501586cacd] (2026-10-06T03:45:24Z)
## Log
- 2026-10-06T03:43:01Z created
- 2026-10-06T03:43:01Z focused
- 2026-10-06T03:45:20Z scope: app repo ~/projects/foreman-desktop
- 2026-10-06T03:45:24Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-20261002-round2: Source: research/brainstorm-20261002-145137 (3 lenses, 21 ideas) merged with own list; user steer: queue/inbox/activity must match t…
- decision 2026-10-04: The recursive brainstorm loop is dry: pass 5 kept 2 small ideas (built as T-0287) and pass 6 (fresh lenses: performance, unspoken needs; 43 titles) …
- research brainstorm-pass-5: Source: research/brainstorm-20261004-033458 (simplicity: what to cut, merge or make automatic; bold bets: what would make Foreman indispensab…
- research brainstorm-20261003-round4: 127 new ideas (6 lenses x 2 rounds, past the 152 of rounds 1-3). Grounded against the code and this session.
## Lessons
- A health check that takes seconds belongs on connect and on request, never on a follow tick; the answer is still worth having when the check fails, so keep JSON on a non-zero exit.
## Files touched
- CHANGELOG.md
