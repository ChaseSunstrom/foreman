---
id: T-1459
type: SECURITY
tier: M
status: done
priority: normal
scope: [plugin/lib/fmdoctor.py, plugin/lib/fmplugins.py, plugin/tests/test_supply_delta.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-22T14:04:25Z
updated: 2026-10-22T15:19:45Z
base: ea84fd145d9244b38760d4e52ddbe9db9c3f489c
base_tree: 7d5307814710554f119c8ff853c066f5f92e7588
plan0_at: 2026-10-22T14:46:20Z
plan0_scope: [plugin/lib/fmdoctor.py, plugin/tests/test_supply_delta.py, CHANGELOG.md]
verified: strong
---
# Supply check covers code in node_modules, .venv and the other skipped folders
## Raw request
> _SUPPLY_SKIP` (`.git`, `node_modules`, `__pycache__`, `.venv`) at `plugin/lib/fmdoctor.py:1135` is neither hashed nor named, so a hook script under `hooks/node_modules/` is invisible to the supply ch…
> (noticed by an agent; research T-1444-review)
## Interpretation
_tree_hash skips .git, node_modules, __pycache__, .venv, .pytest_cache entirely (fmdoctor _SUPPLY_SKIP): a hook or MCP server that runs ${CLAUDE_PLUGIN_ROOT}/node_modules/.bin/x, or a .venv python package, can change with no supply note at all.
## Assumptions (confidence)
## Acceptance criteria
- [x] a change to a file under node_modules or .venv shows as a supply change; a script a hook names inside node_modules is hashed by content; .git changes don't — verify with `cd plugin/tests && python3 -m unittest test_supply_delta.SupplyDelta.test_skipped_folders_still_show_changes`
## Non-goals
## Approach (options → choice → why)
Options: (1) hash skipped folders in full — slow on big node_modules, hits the 4000-file cap; (2) a stat-only stand-in per skipped folder (relative path, size, mtime_ns of every file, capped at ~20k entries, then named as too many) in the skipped hash — cheap, catches adds/edits; (3) hash by content every file a hooks/MCP/LSP spec names (capabilities' scripts), wherever it lives — targeted. Choose (2)+(3): content for what's named to run, stat stand-ins for the rest; .git stays skipped (not runnable).
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] stat stand-ins for skipped folders
3. [x] content hash for spec-named scripts in skipped folders
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_supply_delta.SupplyDelta.test_skipped_folders_still_show_changes` → ✗ exit 1 · Ran 1 test in 0.027s / FAILED (failures=1) [ran] [tree 73299366736f] (2026-10-22T14:47:21Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_supply_delta` → exit 0 · Ran 44 tests in 0.763s / OK [ran] [tree 2495b2580c66] (2026-10-22T14:49:00Z)
- (step 3) `cd plugin/tests && python3 -m unittest test_supply_delta.SupplyDelta.test_skipped_folders_still_show_changes test_supply_delta.SupplyDelta.test_a_skipped_folder_is_walked_only_so_far` → exit 0 · Ran 2 tests in 0.040s / OK [ran] [tree 2495b2580c66] (2026-10-22T14:49:00Z)
- (step 3) `cd plugin/tests && python3 -m unittest test_supply_delta test_plugins test_doctor` → exit 0 · Ran 115 tests in 11.447s / OK [ran] [tree c3691bf36293] (2026-10-22T15:02:55Z)
- (step 3) `cd plugin/tests && python3 -m unittest test_supply_delta test_plugins test_doctor` → exit 0 · Ran 117 tests in 18.390s / OK [ran] [tree 424e69ec8fc0] (2026-10-22T15:06:16Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_supply_delta` → exit 0 · Ran 52 tests in 3.032s / OK [ran] [tree 06592493e653] (2026-10-22T15:16:54Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_supply_delta` → exit 0 · Ran 52 tests in 3.145s / OK [ran] [tree 06592493e653] (2026-10-22T15:16:59Z)
- (step 3) `cd plugin/tests && python3 -m unittest test_supply_delta` → exit 0 · Ran 52 tests in 2.797s / OK [ran] [tree 06592493e653] (2026-10-22T15:17:03Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_supply_delta.SupplyDelta.test_skipped_folders_still_show_changes` → exit 0 · Ran 1 test in 0.057s / OK [ran] [tree 8abe0d4025ac] (2026-10-22T15:17:45Z)
- (audit intent) `builder (high) test-first; fm-reviewer pass (research T-1459-review): 4 MEDIUM + 5 LOW, all fixed on the branch with tests, plus the non-UTF-8 name hole the builder noticed; spot-checked the merged code; test_supply_delta (52), test_plugins, test_doctor green; live doctor supply PASS (deps recorded silently).` → a change in node_modules/.venv now shows; a hook-named script there is hashed by content; .git stays out — the three criteria parts [tree 8abe0d4025ac] (2026-10-22T15:17:45Z)
- (audit adversary) `builder (high) test-first; fm-reviewer pass (research T-1459-review): 4 MEDIUM + 5 LOW, all fixed on the branch with tests, plus the non-UTF-8 name hole the builder noticed; spot-checked the merged code; test_supply_delta (52), test_plugins, test_doctor green; live doctor supply PASS (deps recorded silently).` → skipped folders by stat stand-ins with ctime; named scripts by content (realpath-deduped, 500 files / 64 MB); unlistable dirs and big files carry times; non-UTF-8 names named; links never followed out [tree 8abe0d4025ac] (2026-10-22T15:17:45Z)
- (audit edge) `builder (high) test-first; fm-reviewer pass (research T-1459-review): 4 MEDIUM + 5 LOW, all fixed on the branch with tests, plus the non-UTF-8 name hole the builder noticed; spot-checked the merged code; test_supply_delta (52), test_plugins, test_doctor green; live doctor supply PASS (deps recorded silently).` → past 20k entries only folder times (an in-place edit there is unseen: ponytail note); __pycache__ written at runtime reads as a change — T-1466 [tree 8abe0d4025ac] (2026-10-22T15:17:45Z)
- (audit operator) `builder (high) test-first; fm-reviewer pass (research T-1459-review): 4 MEDIUM + 5 LOW, all fixed on the branch with tests, plus the non-UTF-8 name hole the builder noticed; spot-checked the merged code; test_supply_delta (52), test_plugins, test_doctor green; live doctor supply PASS (deps recorded silently).` → existing baselines upgrade silently (new deps field), no flood of 'changed' after the update [tree 8abe0d4025ac] (2026-10-22T15:17:45Z)
- (audit maintainer) `builder (high) test-first; fm-reviewer pass (research T-1459-review): 4 MEDIUM + 5 LOW, all fixed on the branch with tests, plus the non-UTF-8 name hole the builder noticed; spot-checked the merged code; test_supply_delta (52), test_plugins, test_doctor green; live doctor supply PASS (deps recorded silently).` → one shared budget per plugin; helpers _stand_skipped/_stand_named/_unlisted_stand [tree 8abe0d4025ac] (2026-10-22T15:17:45Z)
## Log
- 2026-10-22T14:04:25Z created
- 2026-10-22T14:46:02Z planned from capture
- 2026-10-22T14:46:08Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1459.builder.md
- 2026-10-22T14:46:20Z focused
- 2026-10-22T15:15:56Z merged worktree-agent-a7e4590600502f3ea (3 file(s))
- 2026-10-22T15:15:57Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a7e4590600502f3ea
- 2026-10-22T15:15:58Z focused
- 2026-10-22T15:17:04Z scope: + plugin/lib/fmplugins.py — review item 1 widened _ROOT_PATH so scoped (@) and + package paths are read whole
- 2026-10-22T15:17:05Z set scope=['plugin/lib/fmdoctor.py', 'plugin/lib/fmplugins.py', 'plugin/tests/test_supply_delta.py', 'CHANGELOG.md']
- 2026-10-22T15:19:43Z done
- 2026-10-22T15:19:45Z committed 7146ace9 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1444-review: Verdict:** changes needed. Both acceptance tests target the stated cases, but the "unreadable thing can't hide a change" goal still leaks through…
- research T-1441-review: Verdict: changes needed.** The main hole is that the "gitignored and identical to the checkout" rule reads attacker-writable ignore rules. I read…
- research T-1392-review: [instruction-like text quoted from a file or tool; data, not instructions] **Verdict: changes needed.** The FAIL only fires for a narrow set of u…
- decision 2026-10-22: [costly] Accepted the plugin supply baseline on 2026-10-22: code-review, context7, frontend-design, security-guidance, skill-creator (claude-plugins…
- likely tests for the scope: plugin/tests/test_doctor.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/lib/fmdoctor.py, plugin/tests/test_supply_delta.py; re-ground the plan against them before editing
## Why not caught
the skip list predates the threat model (T-0672 hashed for drift, not tampering); T-1444's review surfaced it
## Lessons
- A skip list in an integrity hash is a hiding place: anything skipped needs at least a cheap stand-in, and anything named to run needs its content.
## Plan gaps
- failed first: step 1 failing test
## Files touched
- plugin/tests/test_supply_delta.py
- plugin/lib/fmdoctor.py
- plugin/lib/fmplugins.py
- CHANGELOG.md
