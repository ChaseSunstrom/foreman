---
id: T-1236
type: SECURITY
tier: S
status: done
priority: normal
scope: [plugin/lib/fmhooks.py, plugin/tests/test_hooks.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-16T17:46:27Z
updated: 2026-10-16T17:47:06Z
base: 777311a539f3cc36c7ad04fabe54fdfa53bb2310
base_tree: ac84eb1bcd36245d92449964284d222b69df7090
plan0_at: 2026-10-16T17:46:27Z
plan0_scope: [plugin/lib/fmhooks.py, plugin/tests/test_hooks.py, CHANGELOG.md]
verified: strong
---
# Hook's Claude Code process found by a fixed shape (one python layer, one system shell), never by skipping look-alikes at any depth
## Raw request
> Hook's Claude Code process found by a fixed shape (one python layer, one system shell), never by skipping look-alikes at any depth
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] Shape tests: only the hook's own python and one system shell launching it are skipped; a nested or disguised claude is identified; approvals still pass — verify with `python3 plugin/tests/run.py -k HookClaudeShape -k Approvals -k PromptApprovals`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Shape tests red, then the fixed-shape lookup
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k HookClaudeShape -k Approvals -k PromptApprovals` → exit 0 · Ran 27 tests in 15.1s (3 classes, 16 at a time; slowest: Approvals 15s, PromptApprovals 11s, HookClaudeShape 0s) / OK [ran] [tree ac84eb1bcd36] (2026-10-16T17:46:43Z)
- (ac 1) `python3 plugin/tests/run.py -k HookClaudeShape -k Approvals -k PromptApprovals` → exit 0 · Ran 27 tests in 14.9s (3 classes, 16 at a time; slowest: Approvals 15s, PromptApprovals 11s, HookClaudeShape 0s) / OK [ran] [tree ac84eb1bcd36] (2026-10-16T17:47:06Z)
- (audit adversary) `automated security review (HIGH) of 777311a5: the skip rules trusted argv substrings and skipped look-alike layers at any depth; reproduced as a failing shape test (two shell layers were both skipped), fixed with a fixed shape and absolute-path identity` → a copy of claude named python3 with a relative 'yes' link to the hook, a bash -c that merely mentions /hooks/hook, two stacked shells: none is skipped; the only skipped layers are this file's own dispatcher by absolute path and one /bin or /usr/bin shell whose -c starts with it. An unexpected shape fails closed (no chat approval; the permission dialog still grants). Residual: typing into the user's own terminal [tree ac84eb1bcd36] (2026-10-16T17:47:06Z)
- (audit edge) `automated security review (HIGH) of 777311a5: the skip rules trusted argv substrings and skipped look-alike layers at any depth; reproduced as a failing shape test (two shell layers were both skipped), fixed with a fixed shape and absolute-path identity` → no procfs (macOS): no exe, so the shell layer is never skipped and chat approvals fail closed; a quoted hook path is read with shlex [tree ac84eb1bcd36] (2026-10-16T17:47:06Z)
- (audit self) `automated security review (HIGH) of 777311a5: the skip rules trusted argv substrings and skipped look-alike layers at any depth; reproduced as a failing shape test (two shell layers were both skipped), fixed with a fixed shape and absolute-path identity` → no findings [tree ac84eb1bcd36] (2026-10-16T17:47:06Z)
## Log
- 2026-10-16T17:46:27Z created
- 2026-10-16T17:46:27Z focused
- 2026-10-16T17:47:06Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0781 [FEATURE S, done, 2 steps] Sessions are named after their task: SessionStart and UserPromptSubmit set sessionTitle when the active task changes — lesson: a rename…
- T-0785 [FEATURE S, done, 2 steps] fm doctor names the Foreman features the installed Claude Code is too old for — lesson: a probe for a setting must look where Foreman w…
- T-1109 [FIX S, done, 2 steps] Two signal bugs found in reviews: fmhooks._cc_version caches the Claude Code version for 2 — lesson: A cache of another program's version s…
- decision 2026-10-16: Recommendation: build the 9 grounded items T-1180..T-1188 with builders; the worktree-fm re-exec idea is skipped (unreviewed lane code would write r…
- likely tests for the scope: plugin/tests/test_hooks.py
## Files touched
- CHANGELOG.md
