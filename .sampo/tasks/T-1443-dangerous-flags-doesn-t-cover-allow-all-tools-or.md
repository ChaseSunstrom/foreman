---
id: T-1443
type: SECURITY
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcode.py, plugin/tests/test_code_hardening.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-21T22:44:08Z
updated: 2026-10-22T14:00:00Z
group: guard evasion and dangerous-flag coverage
base: df577908ccde82cfb0368329524d4f1480d876ee
base_tree: 1cae68b25448c41bfe71c74a174a6b2bc96eb07d
plan0_at: 2026-10-22T13:57:47Z
plan0_scope: [plugin/lib/fmcode.py, plugin/tests/test_code_hardening.py, CHANGELOG.md]
verified: strong
---
# Runner lint knows Copilot, Droid and Claude's allow-all flags
## Raw request
> - `dangerous_flags` doesn't cover `--allow-all-tools` or `--skip-permissions-unsafe
> (noticed by an agent; research T-1434-1417-review)
## Interpretation
dangerous_flags misses --allow-all-tools / --allow-all (GitHub Copilot CLI), --skip-permissions-unsafe (Factory droid exec) and Claude's --allow-dangerously-skip-permissions (the --dangerously- prefix check needs the flag to start with it).
## Assumptions (confidence)
## Acceptance criteria
- [x] the four flags are caught, a scoped --allow-tool isn't — verify with `cd plugin/tests && python3 -m unittest test_code_hardening.ReviewNits.test_allow_all_flags`
## Non-goals
## Approach (options → choice → why)
Add the exact flags; match 'dangerously' anywhere in a flag name. Copilot's scoped --allow-tool stays allowed.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] extend dangerous_flags
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_code_hardening.ReviewNits.test_allow_all_flags` → ✗ exit 1 · Ran 1 test in 0.007s / FAILED (failures=4) [ran] [tree f660c38e45a5] (2026-10-22T13:57:48Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_code_hardening.ReviewNits.test_allow_all_flags` → exit 0 · Ran 1 test in 0.007s / OK [ran] [tree 0f0f65368f91] (2026-10-22T13:57:54Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_code_hardening.ReviewNits.test_allow_all_flags` → exit 0 · Ran 1 test in 0.008s / OK [ran] [tree 0adb50752ae6] (2026-10-22T13:58:06Z)
- (audit adversary) `self: three exact flags plus any --flag containing 'dangerously'; test covers the four forms and a scoped --allow-tool; test_code_hardening + test_runner_lint green.` → a --flag=value form is split before the compare, so --allow-all=true is caught too; a wrapper script stays out of reach (documented ponytail ceiling) [tree 0adb50752ae6] (2026-10-22T13:58:06Z)
- (audit edge) `self: three exact flags plus any --flag containing 'dangerously'; test covers the four forms and a scoped --allow-tool; test_code_hardening + test_runner_lint green.` → built-in WORKERS aren't linted (registry is trusted); only code.toml runners and inline --worker templates [tree 0adb50752ae6] (2026-10-22T13:58:06Z)
- (audit self) `self: three exact flags plus any --flag containing 'dangerously'; test covers the four forms and a scoped --allow-tool; test_code_hardening + test_runner_lint green.` → no findings [tree 0adb50752ae6] (2026-10-22T13:58:06Z)
## Log
- 2026-10-21T22:44:08Z created
- 2026-10-22T13:57:46Z planned from capture
- 2026-10-22T13:57:46Z focused
- 2026-10-22T13:59:59Z done
- 2026-10-22T14:00:00Z committed 6d0ee3bb (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1395 [SECURITY M, done, 2 steps] Runner flag lint and grade: a dangerous runner template waits for an acknowledgement of its exact hash; runners show a guard grade; li…
- research brainstorm-fm-anthropic-half-a: Grounded against `plugin/lib` at HEAD (branch foreman/build; fmcli.py and test_cli.py have uncommitted edits).
- research T-1328-review: Verdict: changes needed.** One crash, one silent fallback that sends code to a cloud CLI, one unguarded command-bearing config file, and a gap ag…
- decision 2026-10-21: fm code brainstorm round 1: 39 build clusters and 5 planned ones are queued (29 new tasks T-1333..T-1361 plus steers on T-1305, T-1308, T-1327..T-13…
- similar past tasks were M: consider --tier M
- likely tests for the scope: plugin/tests/test_code.py
## Preflight
Changed in scope since this was planned (2026-10-21): CHANGELOG.md, plugin/lib/fmcode.py, plugin/tests/test_code_hardening.py; re-ground the plan against them before editing
## Plan gaps
- failed first: step 1 failing test
## Files touched
- plugin/tests/test_code_hardening.py
- plugin/lib/fmcode.py
- CHANGELOG.md
