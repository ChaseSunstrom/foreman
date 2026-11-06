---
id: T-0353
type: SECURITY
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-06T04:49:44Z
updated: 2026-10-06T04:51:19Z
base: 73caa057ac5da3e72d05b8db7ca574bf6fb90b8b
base_tree: 081fd00c56605b058aa79a753354c1b58e2b1a42
verified: strong
---
# UI review fixes: no approval without a plan, visible done-blockers, show every step
## Raw request
> Address the security review of the UI cleanup (T-0351): no approval without a plan to read; done-blockers visible, not behind a count; a one-click 'show every step' so folded tool runs stay auditable
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] approval is offered only for an item with a plan to read; the reasons a task can't close are listed; one click shows every folded step — verify with `bash -c 'cd ~/projects/foreman-desktop && bun run check'`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] three fixes, verified on screen
## Resume here
## Docs impact
none: UI behaviour only, covered by the app README's conversation description
## Verification evidence
- (step 1) `bash -c 'cd ~/projects/foreman-desktop && bun run check && ls /tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/c2-both.png'` → exit 0 · 1791262277141 COMPLETED 200 FILES 0 ERRORS 0 WARNINGS 0 FILES_WITH_PROBLEMS / /tmp/claude-1000/-home-<user>--claude-foreman/e18ac773-469c-4b5e-8209-e5612aaa52a2/scratchpad/c2-both.png [ran] [tree 081fd00c5660] (2026-10-06T04:51:17Z)
- (ac 1) `bash -c 'cd ~/projects/foreman-desktop && bun run check'` → exit 0 · 1791262279352 START "~/projects/foreman-desktop" / 1791262279353 COMPLETED 200 FILES 0 ERRORS 0 WARNINGS 0 FILES_WITH_PROBLEMS [ran] [tree 081fd00c5660] (2026-10-06T04:51:19Z)
- (audit adversary) `the automated security reviews of the cleanup commit: approval now needs a plan with an approach to read (unplanned inbox items no longer offer a yes); the done-blockers are listed (four, then 'and N more' with the rest on hover); 'Show every step' opens every folded run, here and in subagents; a run's key no longer equals its first call's, which made opening that call collapse the run` → no click approves an item the user can't read a plan for; nothing an agent did is hidden past one click [tree 081fd00c5660] (2026-10-06T04:51:19Z)
- (audit self) `the automated security reviews of the cleanup commit: approval now needs a plan with an approach to read (unplanned inbox items no longer offer a yes); the done-blockers are listed (four, then 'and N more' with the rest on hover); 'Show every step' opens every folded run, here and in subagents; a run's key no longer equals its first call's, which made opening that call collapse the run` → no findings [tree 081fd00c5660] (2026-10-06T04:51:19Z)
## Log
- 2026-10-06T04:49:44Z created
- 2026-10-06T04:49:56Z planned from capture
- 2026-10-06T04:49:56Z focused
- 2026-10-06T04:51:17Z scope: app repo ~/projects/foreman-desktop
- 2026-10-06T04:51:19Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0088-review: Verdict:** approve with nits. I read the diff and the `fmcore.py`/`fmcli.py` code it calls into. I ran no tests, so the three verify commands in …
- T-0276 [FEATURE L, done, 4 steps] fm second: one primitive for independent second reads — rival-model plan review, debate rebuttal, daily session review,… — lesson: Anyt…
- research brainstorm-pass-5: Source: research/brainstorm-20261004-033458 (simplicity: what to cut, merge or make automatic; bold bets: what would make Foreman indispensab…
- decision 2026-09-26: T-0018 plan self-approved under full autonomy after self-critique: umbrella with rounds (one core ask), per-round reviewer audits, green gates each …
