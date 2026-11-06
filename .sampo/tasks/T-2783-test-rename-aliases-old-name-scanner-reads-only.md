---
id: T-2783
type: CLEAN
tier: S
status: done
priority: normal
scope: [plugin/tests/test_rename_aliases.py]
depends_on: []
source: discovered
created: 2026-11-03T05:05:28Z
updated: 2026-11-03T17:27:59Z
builder_model: sonnet
base: eec735fb4809de6ab161f39d29366a810f2ab04e
base_tree: bd83673e21820d5e55c048f4b0836610f7d0467f
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-03T05:32:11Z
plan0_scope: [plugin/tests/test_rename_aliases.py]
lane_stop: merged 2026-11-03T06:09:00Z
verified: strong
---
# The rename ratchet sees every old module name a test or library passes as a string: test_rename_aliases' scanner walks every argument (keywords too) of lazy, import_module, __import__, find_spec and patch, and the constant parts of f-strings, not only the first string argument
## Raw request
> CLEAN: test_rename_aliases' old-name scanner reads only the first string argument of lazy/import_module/__import__/find_spec/patch; walk f-string parts and every argument so the ratchet sees f'fm{x}' and keyword targets (T-2748 review)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the scanner flags patch('x', new=…) with target='fmcore.y' as a keyword, import_module(f'fm{name}') and a second-argument old name, and the live tree still has none outside the shims — verify with `python3 plugin/tests/run.py test_rename_aliases`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red: a fixture string of source with each missed form is flagged; then widen the AST walk; run test_rename_aliases
## Resume here
## Docs impact
none
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_rename_aliases` → exit 0 · Ran 9 tests in 8.7s (1 classes, 16 at a time; slowest: RenameAliases 6s) / OK [ran] [tree 01dc5e4f7e34] [world 2f1906870a] (2026-11-03T05:34:36Z)
- (step 1) `python3 plugin/tests/run.py test_rename_aliases` → exit 0 · Ran 9 tests in 8.7s (1 classes, 16 at a time; slowest: RenameAliases 6s) / OK [ran] [tree 01dc5e4f7e34] [world 2f1906870a] (2026-11-03T05:34:36Z)
- (step 1) `python3 plugin/tests/run.py test_rename_aliases` → exit 0 · Ran 9 tests in 7.1s (1 classes, 16 at a time; slowest: RenameAliases 6s) / OK [ran] [tree 01dc5e4f7e34] [world 2f1906870a] (2026-11-03T05:34:46Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 1 of 6 failed: python3 plugin/tests/run.py → ✗ exit 124 (timed out after 600s) · timed out after 600s [ran] [tree 01dc5e4f7e34] [world 2f1906870a] (2026-11-03T05:48:06Z)
- (ac 1) `python3 plugin/tests/run.py test_rename_aliases` → exit 0 · Ran 9 tests in 3.3s (1 classes, 16 at a time; slowest: RenameAliases 3s) / OK [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T17:27:26Z)
- (step 1) `python3 plugin/tests/run.py test_rename_aliases` → exit 0 · Ran 9 tests in 3.3s (1 classes, 16 at a time; slowest: RenameAliases 3s) / OK [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T17:27:26Z)
- (audit intent) `self: read the diff; the scanner walks every argument and f-string constants` → the rename ratchet sees old module names passed as keywords, later arguments or f-strings [tree 07445d19b39c] (2026-11-03T17:27:26Z)
- (audit edge) `self: read the diff; the scanner walks every argument and f-string constants` → print(f'fm{x}'), lazy(f'{p}.x') and 'fmxy' are not flagged; 'fm' + x stays invisible [tree 07445d19b39c] (2026-11-03T17:27:26Z)
- (audit adversary) `self: read the diff; the scanner walks every argument and f-string constants` → a test-only scanner; no runtime effect [tree 07445d19b39c] (2026-11-03T17:27:26Z)
- (audit self) `self: read the diff; the scanner walks every argument and f-string constants` → no findings [tree 07445d19b39c] (2026-11-03T17:27:26Z)
- `python3 plugin/tests/run.py test_rename_aliases` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T17:27:26Z [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T17:27:43Z)
- (audit intent) `self: read the diff; the scanner walks every argument and f-string constants` → the rename ratchet sees old module names passed as keywords, later arguments or f-strings [tree 07445d19b39c] (2026-11-03T17:27:43Z)
- (audit edge) `self: read the diff; the scanner walks every argument and f-string constants` → print(f'fm{x}'), lazy(f'{p}.x') and 'fmxy' are not flagged; 'fm' + x stays invisible [tree 07445d19b39c] (2026-11-03T17:27:43Z)
- (audit adversary) `self: read the diff; the scanner walks every argument and f-string constants` → a test-only scanner; no runtime effect [tree 07445d19b39c] (2026-11-03T17:27:43Z)
- (audit self) `self: read the diff; the scanner walks every argument and f-string constants` → no findings [tree 07445d19b39c] (2026-11-03T17:27:43Z)
## Log
- 2026-11-03T05:05:28Z created
- 2026-11-03T05:31:49Z planned from capture
- 2026-11-03T05:31:50Z set approved=True
- 2026-11-03T05:31:52Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2783.builder.md
- 2026-11-03T05:32:10Z focused
- 2026-11-03T05:32:11Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-03T06:09:00Z merged worktree-agent-a4c455d44380461f4 (1 file(s))
- 2026-11-03T14:21:31Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a4c455d44380461f4
- 2026-11-03T15:07:44Z focused
- 2026-11-03T15:07:45Z paused: focus moved to T-2786
- 2026-11-03T17:05:15Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-03T17:05:15Z focused
- 2026-11-03T17:05:16Z paused: focus moved to T-2786
- 2026-11-03T17:27:21Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-03T17:27:21Z focused
- 2026-11-03T17:27:59Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2748 [CLEAN M, planned, 4 steps] Internals become Sampo (T-2742 step 4): plugin/lib/fmX.py moves to the package plugin/lib/sampo/ under the decided map, each old fmX.p…
- research T-2748-review: Verdict:** changes needed. This is a narrow MEDIUM fix in the hook's fallback. The shim and rename work looks sound. I read the code but did not …
- T-2742 [FEATURE L, planned, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias;…
- decision 2026-11-03: [cites: user steer: read SAMPO.md (RENAME, NOW)] [check: python3 plugin/tests/run.py test_rename_scan] Rename Foreman to Sampo per SAMPO.md: aliases…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx
## Preflight
Changed in scope since this was planned (2026-11-03): plugin/tests/test_rename_aliases.py; re-ground the plan against them before editing
## Behaviour lock
none: the builder lane's pre-edit fm check timed out or failed on bench_hooks timing under machine load on 2026-11-03 (T-2797), so no lock was recorded before the first edit; the change is covered by its targeted tests and the post-merge full suite
## Lessons
- A ratchet must read the forms the code really uses
## Files touched
- plugin/tests/test_rename_aliases.py
