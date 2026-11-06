---
id: T-1233
type: SECURITY
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-16T17:25:38Z
updated: 2026-10-16T17:27:52Z
base: 03444605f297fd97f67960ec2d78a7c941d3fb25
base_tree: 8af491a5057ce4313a87360e2a3c8d3c1ed0ec61
plan0_at: 2026-10-16T17:25:38Z
plan0_scope: []
verified: strong
---
# Chat approvals answer only in the Claude Code process that asked: exact process identity instead of name-based wrapper skipping
## Raw request
> Chat approvals answer only in the Claude Code process that asked: exact process identity instead of name-based wrapper skipping
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] A yes from any other Claude Code process (renamed, under a pty, positional prompt, -p) grants nothing; the asking process's own yes grants — verify with `python3 plugin/tests/run.py -k Approvals -k PromptApprovals`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Same-process test red, then _hook_claude + pid binding in _record_asks, fm ask and _resolve_approvals
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k Approvals -k PromptApprovals` → exit 0 · Ran 25 tests in 15.6s (2 classes, 16 at a time; slowest: Approvals 15s, PromptApprovals 11s) / OK [ran] [tree a94cc246c598] (2026-10-16T17:26:51Z)
- (ac 1) `python3 plugin/tests/run.py -k Approvals -k PromptApprovals` → exit 0 · Ran 25 tests in 15.6s (2 classes, 16 at a time; slowest: Approvals 15s, PromptApprovals 11s) / OK [ran] [tree a94cc246c598] (2026-10-16T17:27:07Z)
- (audit adversary) `automated security review finding on T-1226 confirmed by reasoning (a copy of claude named bash, run under a python pty with a positional yes, was skipped as a wrapper and reached the asking process); fixed test-first (red: a yes from another process granted) with exact process identity and pid:start binding recorded at ask time` → renamed copies, pty wrappers, positional prompts, -p/stream-json and resumed sessions are all other processes; the hook layers skipped are only python running this very hook file and a /bin or /usr/bin shell whose -c launches hooks/hook. Residual: typing into the user's own terminal (tmux send-keys) is still a person-shaped prompt [tree a94cc246c598] (2026-10-16T17:27:07Z)
- (audit edge) `automated security review finding on T-1226 confirmed by reasoning (a copy of claude named bash, run under a python pty with a positional yes, was skipped as a wrapper and reached the asking process); fixed test-first (red: a yes from another process granted) with exact process identity and pid:start binding recorded at ask time` → no procfs (macOS) falls back to ps and comm; a misidentified process only makes chat approvals fail closed; asks recorded before this change carry no process and can't be chat-approved (the dialog still grants) [tree a94cc246c598] (2026-10-16T17:27:07Z)
- (audit self) `automated security review finding on T-1226 confirmed by reasoning (a copy of claude named bash, run under a python pty with a positional yes, was skipped as a wrapper and reached the asking process); fixed test-first (red: a yes from another process granted) with exact process identity and pid:start binding recorded at ask time` → no findings [tree a94cc246c598] (2026-10-16T17:27:07Z)
## Log
- 2026-10-16T17:25:38Z created
- 2026-10-16T17:25:38Z focused
- 2026-10-16T17:27:51Z done
- 2026-10-16T17:27:52Z committed 1daa4218 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0084 [FEATURE L, done, 7 steps] Foreman UI mod: docked pane, prompt band, toasts, /fm, one-press approve/next/drive/inbox — lesson: Mods: functions that take $ must be…
- T-0946 [FEATURE M, done, 3 steps] MCP: a great Foreman MCP server (state, stack library, zero-token instruments) and fm mcp new to wrap any process or CLI as a tested MC…
- T-0961 [FEATURE M, done, 3 steps] Lanes and internals: the merge base saved before the merge, one _git helper — lesson: When a helper turns exceptions into return codes,…
- decision 2026-10-16: T-1032 plan: automatic failure→fix pairing in the hooks, recall across projects, pre-run warning, feedback counts, fm fix CLI, git transport via fm …
## Files touched
- CHANGELOG.md
