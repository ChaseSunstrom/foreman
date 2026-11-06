---
id: T-0378
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-09T00:32:48Z
updated: 2026-10-09T00:33:37Z
base: 8734dbf478da009577bc2c9c00929bcda5af9f9e
base_tree: 6c809bfbd73e5248bbc46178326dadf071e4b9c5
verified: strong
---
# Guard: design-token files (design/tokens.json, design-tokens.json) aren't credentials
## Raw request
> Guard: design-token files (design/tokens.json, design-tokens.json) aren't credentials
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a tokens file in a design/theme/styles/ui folder or with a design-/theme- name is writable; token.json, ~/.config/x/tokens.json and design/secrets.yaml stay credentials — verify with `python3 plugin/tests/run.py -k test_design_tokens_are_not_credentials`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first: design tokens vs credential tokens
## Resume here
## Docs impact
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py -k test_design_tokens_are_not_credentials` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: ScratchNames 0s) / OK [ran] [tree 6b7463fa51a9] (2026-10-09T00:33:29Z)
- (step 1) `python3 plugin/tests/run.py -k test_design_tokens_are_not_credentials` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: ScratchNames 0s) / OK [ran] [tree 6b7463fa51a9] (2026-10-09T00:33:29Z)
- (audit self) `self + adversary: the exemption covers only 'token(s)' names in a design/theme/style/ui folder or with a design-/theme-/style- prefix, never secret/credential names, never token.json; replay 0 newly allowed` → no findings [tree 6b7463fa51a9] (2026-10-09T00:33:29Z)
- `python3 plugin/tests/run.py -k test_design_tokens_are_not_credentials` → ✗ exit 1 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: ScratchNames 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 6b7463fa51a9] (2026-10-09T00:33:36Z)
- `python3 plugin/tests/run.py -k test_design_tokens_are_not_credentials` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: ScratchNames 0s) / OK [ran] [tree 6b7463fa51a9] (2026-10-09T00:33:36Z)
- (audit adversary) `self + adversary in the main thread; replay 0 newly allowed` → the exemption covers only 'token(s)' names in a design/theme/style/ui folder or with a design-/theme-/style- prefix, never secret/credential names and never token.json; credential dirs, .env, keys and home credential files are checked before it [tree 6b7463fa51a9] (2026-10-09T00:33:36Z)
- (audit self) `self + adversary in the main thread; replay 0 newly allowed` → no findings [tree 6b7463fa51a9] (2026-10-09T00:33:36Z)
## Log
- 2026-10-09T00:32:48Z created
- 2026-10-09T00:32:48Z focused
- 2026-10-09T00:33:36Z done
- 2026-10-09T00:33:37Z committed 673ef9e (3 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0169 [FIX S, done, 3 steps] Guard: a secret-sounding file name under the scratchpad or /tmp isn't a credential; its real path still is checked — lesson: A name-based h…
- research t0018-r5-adversary: HIGH — `~/.claude/foreman/plugin/lib/fmguard.py:188-198` (`_protected_roots`) and `:146-147` (`_CRED_DIRS`/`_CRED_FILES`) — tree-w…
- research t0016-adversary: ":"standard","inference_geo":"not_available"},"input_transformations":[],"diagnostics":null,"context_management":null},"apiBlockIndex":0,"reque…
- decision 2026-09-26: T-0014: claude config/mcp commands that change ~/.claude.json stay ungated for now and are documented as a guard limitation; consent for plugin/MCP/…
- likely tests for the scope: plugin/tests/test_guard.py
## Lessons
- A name heuristic for secrets needs the vocabulary of the domains it runs in: design systems call their palette 'tokens'
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- CHANGELOG.md
