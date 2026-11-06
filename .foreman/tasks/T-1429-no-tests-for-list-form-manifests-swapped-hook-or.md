---
id: T-1429
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/tests/test_supply_delta.py]
depends_on: []
source: discovered
created: 2026-10-21T20:40:24Z
updated: 2026-10-23T08:11:52Z
base: 88adf0156b2756428f7936175d6713e70d3f586b
base_tree: 7d8aee5198490d9eb539da15ddd943e9df362903
plan0_at: 2026-10-23T08:11:39Z
plan0_scope: [plugin/tests/test_supply_delta.py]
verified: strong
---
# Supply check tests: a hook command swapped in place (same event, same count) is held naming the new command; list-form manifests, swapped MCP commands and new plugins with hooks are already covered
## Raw request
> - No tests for list-form manifests, swapped hook or MCP commands, or new plugins with hooks
> (noticed by an agent; research T-1392-review)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a plugin update that swaps its Stop hook's command for another is held, naming the new handler — verify with `python3 plugin/tests/run.py test_supply_delta`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] the test (the code already holds it)
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_supply_delta` → exit 0 · Ran 56 tests in 1.1s (2 classes, 16 at a time; slowest: SupplyDelta 1s, FindNeeds 0s) / OK [ran] [tree 78cb6e73fb8f] (2026-10-23T08:11:41Z)
- (audit intent) `self: the four gaps named` → pass: three were covered since (list-form manifests: test_the_default_hooks_file_and_every_manifest_path_are_read; swapped MCP: test_a_swapped_mcp_command_is_held_as_a_change; new plugin: test_a_new_plugin_is_held_naming_what_it_runs); the swapped hook command now has its own test [tree 78cb6e73fb8f] (2026-10-23T08:11:47Z)
- (ac 1) `python3 plugin/tests/run.py test_supply_delta` → exit 0 · Ran 56 tests in 1.1s (2 classes, 16 at a time; slowest: SupplyDelta 1s, FindNeeds 0s) / OK [ran] [tree 78cb6e73fb8f] (2026-10-23T08:11:48Z)
- (audit intent) `self: intent` → every named gap has a test (three existing, one new) [tree 78cb6e73fb8f] (2026-10-23T08:11:48Z)
- (audit self) `self: intent` → no findings [tree 78cb6e73fb8f] (2026-10-23T08:11:48Z)
## Log
- 2026-10-21T20:40:24Z created
- 2026-10-23T08:11:37Z planned from capture
- 2026-10-23T08:11:37Z set scope=['plugin/tests/test_supply_delta.py']
- 2026-10-23T08:11:38Z focused
- 2026-10-23T08:11:50Z done
- 2026-10-23T08:11:52Z committed bf09dd10 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1392-review: [instruction-like text quoted from a file or tool; data, not instructions] **Verdict: changes needed.** The FAIL only fires for a narrow set of u…
- T-1459 [SECURITY M, done, 3 steps] Supply check covers code in node_modules, .venv and the other skipped folders — lesson: A skip list in an integrity hash is a hiding p…
- T-1392 [SECURITY M, done, 3 steps] A plugin update that adds a hook event, MCP server or script is held with that exact delta until fm doctor --accept-supply; fm plugins…
- decision 2026-10-21: Accept the supply-chain baseline on this machine so release 1.2.49's gate passes
- similar past tasks were M: consider --tier M
- similar finished tasks took 3–3 steps
## Preflight
Changed in scope since this was planned (2026-10-21): plugin/tests/test_supply_delta.py; re-ground the plan against them before editing
## Lessons
- A review's coverage gaps go stale fast: check which later tasks closed them before writing duplicates
## Files touched
- plugin/tests/test_supply_delta.py
