---
id: T-0351
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-06T04:38:41Z
updated: 2026-10-08T23:50:48Z
base: d1fdbc0758b37e1833248944fc24a0f31ec75b36
base_tree: 4848aa4d9c280b32f9da5f7eb5099cbf279f3b71
verified: strong
---
# Desktop UI cleanup: conversations without tool-call spam, and a tidier UI
## Raw request
> Desktop UI cleanup: conversations without tool-call spam, and a tidier UI
## Interpretation
The user: 'clean it up, there's a lot of chat spam from your messages', then 'clean up the UI a little more'. A Claude session's conversation in the app is mostly tool calls and results (this one: 775 tool rows against 97 messages), burying what was said. Fold tool runs, and tidy the views.
## Assumptions (confidence)
## Acceptance criteria
- [x] a conversation shows the messages first: runs of tool calls fold into one quiet expandable row each, results open on demand — verify with `bash -c 'cd ~/projects/foreman-desktop && bun run check'`
- [x] the cleaned views are checked on screen — verify with `bash -c 'ls /tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/c1-*.png'`
## Non-goals
## Approach (options → choice → why)
(A) In Transcript, group each run of consecutive tool calls and results into one quiet row ('Ran 12 tools · Bash 8, Edit 3, Read 1') that expands to the calls, each result collapsed until opened; then a polish pass from screenshots. (B) A toggle that hides tools entirely — loses what was done. Choice A.
## Risks and rollback
## Execution prompt
## Steps
1. [x] look at the current views and list what's noisy
2. [x] fold tool runs in Transcript; polish pass
3. [x] verify on screen
## Resume here
## Docs impact
CHANGELOG
## Verification evidence
- (step 1) `bash -c 'cd ~/projects/foreman-desktop && bun run check && ls /tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/c1-conversation.png /tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/c1-project2.png'` → exit 0 · /tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/c1-conversation.png / /tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scr [ran] [tree 4848aa4d9c28] (2026-10-06T04:47:00Z)
- (step 2) `bash -c 'cd ~/projects/foreman-desktop && bun run check && ls /tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/c1-conversation.png /tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/c1-project2.png'` → exit 0 · /tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/c1-conversation.png / /tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scr [ran] [tree 4848aa4d9c28] (2026-10-06T04:47:02Z)
- (step 3) `bash -c 'cd ~/projects/foreman-desktop && bun run check && ls /tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/c1-conversation.png /tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/c1-project2.png'` → exit 0 · /tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/c1-conversation.png / /tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scr [ran] [tree 4848aa4d9c28] (2026-10-06T04:47:04Z)
- (ac 1) `bash -c 'cd ~/projects/foreman-desktop && bun run check'` → exit 0 · 1791262034224 START "~/projects/foreman-desktop" / 1791262034224 COMPLETED 200 FILES 0 ERRORS 0 WARNINGS 0 FILES_WITH_PROBLEMS [ran] [tree 37a7233ab0bf] (2026-10-06T04:47:14Z)
- (ac 2) `bash -c 'ls /tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/c1-*.png'` → exit 0 · /tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/c1-project2.png / /tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratch [ran] [tree 37a7233ab0bf] (2026-10-06T04:47:14Z)
- (audit intent) `self-review against before/after captures of the same session (off-screen on Xvfb :99, never the user's screen): tool runs fold into one row with counts and failures, results and images open on demand; overview declutter verified; type-check clean` → the 'chat spam' the user saw is this session in the app: 388 tool calls and their screenshots between 97 messages; now one quiet row per run [tree 37a7233ab0bf] (2026-10-06T04:47:14Z)
- (audit maintainer) `self-review against before/after captures of the same session (off-screen on Xvfb :99, never the user's screen): tool runs fold into one row with counts and failures, results and images open on demand; overview declutter verified; type-check clean` → one blocks pass in Transcript (no new component); unused styles removed; the Images tab still collects every picture [tree 37a7233ab0bf] (2026-10-06T04:47:14Z)
## Log
- 2026-10-06T04:38:41Z created
- 2026-10-06T04:40:20Z focused
- 2026-10-06T04:47:12Z scope: app repo ~/projects/foreman-desktop (d6d888c)
- 2026-10-06T04:47:14Z done
- 2026-10-06T04:47:14Z committed 564d213 (1 path(s))
- 2026-10-08T23:50:48Z includes T-0362: "also clean it up, there's a lot of chat spam from your messages and stuff"
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0328 [FEATURE L, done, 9 steps] FEATURE: Foreman Desktop v2 — clean up the UI so it looks less AI-made and better organize — lesson: Read another tool's internal store…
- T-0137 [FEATURE M, done, 3 steps] Everything in the chat: shell rows with their output formatted inline, folded command groups unfolded, the pane's Output card gone — le…
- T-0179 [FEATURE M, done, 3 steps] Each reply is a panel: a round-bordered box per message, the closing report accented — lesson: Check a layout change in the live render…
- decision 2026-10-06: The desktop app lives in its own repo (~/projects/foreman-desktop), not apps/desktop in the Foreman checkout
- similar finished tasks took 3–9 steps
## Lessons
- Capture the app off-screen (Xvfb + PIL) when the user is at the keyboard: spectacle -a grabs whatever has focus, which was their browser.
## Files touched
- CHANGELOG.md
