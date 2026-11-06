---
id: T-2371
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmwhich.py, plugin/lib/fmhooks.py, plugin/lib/fmcli.py, plugin/tests/test_which.py, plugin/tests/test_hooks.py, plugin/tests/helpers.py, MASTER.md, README.md, CHANGELOG.md]
depends_on: []
source: self
created: 2026-10-31T14:01:59Z
updated: 2026-10-31T16:21:05Z
builder_model: sonnet
base: 6c18fc5197c4e10635fc1fb9b2e7255cd664e2f2
base_tree: 1ea4e134dc55b6dfd32e007a8cd6f152f1b30325
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-10-31T15:37:22Z
plan0_scope: [plugin/lib/fmwhich.py, plugin/lib/fmhooks.py, plugin/tests/test_which.py, plugin/tests/test_hooks.py, MASTER.md, README.md, CHANGELOG.md]
lane_stop: merged 2026-10-31T16:12:01Z
verified: strong
---
# One find across every shelf (Mission 6, #5): fm which NEED searches Foreman's verbs and skills, installed skills, project tools, MCP servers, binaries on this machine, stack cards, marketplace plugins and past fixes, local first, and leaves a search receipt
## Raw request
> One find across every shelf (Mission 6, #5): fm which NEED searches Foreman's verbs and skills, installed skills, project tools, MCP servers, binaries on this machine, stack cards, marketplace plugins and past fixes, local first, and leaves a search receipt
## Interpretation
Reading 1: one search across every shelf before building: grow the existing finder so a session finds what this machine, this project and past fixes already hold, and the search leaves a receipt a build can show. Reading 2: only make the capability-miss note smarter (point at the best local hit) without a unified search; ruled out because a build still couldn't show it searched first, and gen-0 #5 asks to find an existing plugin, skill or MCP server before building. Today the finders are split: fm which (Foreman's own skills, playbooks and verbs), fm lib search (stack cards), fm plugins find (marketplace plugins); nothing looks at other plugins' installed skills, project tools from fm new tool, configured MCP servers, binaries on this machine, or what fixed the same miss before (fmfixes, T-1032); the miss note names only fm plugins find; nothing records that a search happened.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm which NEED lists hits from every source, each with where it came from and whether it needs a grant, past fixes and on-machine hits first; a binary on PATH, a project tool, an installed skill and an MCP server entry in fixtures are each found; each run logs tool_search; the capability-miss note names fm which NAME; no network call is made — verify with `python3 plugin/tests/run.py test_which test_hooks`
## Non-goals
## Approach (options → choice → why)
1) use what exists: grow fm which with new sources beside its skills, playbooks and commands: installed skills (fmplugins._skill_index), project tools (the '# fm new tool' header), MCP servers named in .mcp.json and ~/.claude.json, binaries (shutil.which plus ~/.local/bin, ~/.cargo/bin, node_modules/.bin), fmlib.search, fmplugins.find, and fmfixes' known fix for the miss; ranked solved before, then on this machine, then installable (needs a grant); each run logs tool_search {need, sources, hits}; the miss note (a hook, a real session path) carries the best local hit from the cheap sources only and names fm which NAME for the rest; no network. Likely outcome: one finder, a receipt per search; fails if: a source read is slow enough to show in the hook (the hook reads only the cheap sources). 2) A new fm tools find verb; fails if: it adds a fourth finder beside three, against the lean rule that a new verb removes an old path (rejected). 3) do less: only the miss note names the best local hit, no unified search or receipt; fails if: a build still can't show it searched first (rejected: gen-0 #5). Choice 1 (80%): it reuses the three finders and the hook path; option 3's note is its first part.
## Risks and rollback
Blast radius (fm graph blast): co-changes plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmguard.py, plugin/tests/test_guard.py, plugin/lib/fmgenesis.py; past FIXes T-0877, T-0907, T-0908, T-0928, T-0980.
## Execution prompt
## Steps
1. [x] red tests first in test_which: one per source, the ranking, the receipt event, the note text (test_hooks)
2. [x] fmwhich: the new sources, the ranking and the tool_search event; fmhooks note names fm which
3. [x] docs: MASTER.md, README.md where fm which is listed, CHANGELOG.md
## Resume here
<!-- auto -->
- 2026-10-31T15:43:55Z step 1/3: red tests first in test_which: one per source, the ranking, the receipt event, the note text (test_hooks)
- git: worktree-agent-acacbf6c4b424bb18; 3 uncommitted: plugin/lib/fmwhich.py, plugin/tests/test_hooks.py, plugin/tests/test_which.py
- touched since last checkpoint: plugin/tests/test_which.py, plugin/tests/test_hooks.py, plugin/lib/fmwhich.py
## Docs impact
MASTER.md, README.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_which test_hooks` → ✗ exit 1 · Ran 264 tests in 199.0s (34 classes, 16 at a time; slowest: Stop 195s, NoTaskGate 107s, PreToolUse 107s) / FAILED (2 classes: test_which.Shelves, test_hooks.CapabilityMiss) [ran] [tree 10836cabe55c] (2026-10-31T15:43:38Z)
- (step 1) `python3 plugin/tests/run.py test_which` → exit 0 · Ran 28 tests in 13.1s (4 classes, 16 at a time; slowest: Which 13s, Shelves 11s, Snapshots 0s) / OK [ran] [tree 56017dccb760] (2026-10-31T15:47:54Z)
- (step 2) `python3 plugin/tests/run.py test_which test_hooks` → exit 0 · Ran 264 tests in 40.7s (34 classes, 16 at a time; slowest: Stop 40s, NoTaskGate 28s, PreToolUse 23s) / OK [ran] [tree 56017dccb760] (2026-10-31T15:48:37Z)
- (step 3) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 102 tests in 8.3s (23 classes, 16 at a time; slowest: Fences 8s, DocsProof 2s, TaskLifecycle 1s) / OK [ran] [tree 56017dccb760] (2026-10-31T15:48:47Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_away test_compact test_core test_docs test_drive_side test_guard_evasions test_hooks test_memory test_onwrite test_statusline_ui test_tool_loop test_tool_taint test_which && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.60s] [ran] [tree 56017dccb760] (2026-10-31T15:49:55Z)
- (step 2) `python3 plugin/tests/run.py test_which test_hooks test_bookkeeping` → exit 0 · Ran 284 tests in 106.7s (42 classes, 16 at a time; slowest: Stop 106s, NoTaskGate 55s, PreToolUse 46s) / OK [ran] [tree bbddefedb887] (2026-10-31T16:02:40Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_audit test_away test_board_surfaces test_board_verbs test_builder test_cli test_compact test_core test_cost test_design_surfaces test_design_tokens test_docs test_doctor test_drive_side test_edit_cards test_exam test_extras test_find test_followups test_guard test_guard_cases test_guard_evasions test_hooks test_ideation test_judgment test_lane_stall test_lanes test_lib_hostile test_lib_source_kill test_library test_memory test_nudges test_onwrite test_paused test_playbook_use test_plugin_parity test_plugins test_prove test_replan test_robustness test_scaffold test_scene test_scout test_second test_shade test_showpieces test_site_gallery test_skillroute test_smoke_profiles test_speed test_statusline_ui test_steering test_supply_delta test_taste_ledger test_tidy test_tool_loop test_tool_taint test_ui test_verify_strength test_verifying test_which && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [31.71s] [ran] [tree 134e3b4080c8] (2026-10-31T16:08:51Z)
- (step 1) `python3 plugin/tests/run.py test_which test_hooks test_bookkeeping` → exit 0 · Ran 284 tests in 39.1s (42 classes, 16 at a time; slowest: Stop 39s, NoTaskGate 27s, PreToolUse 21s) / OK [ran] [tree 8c24abb5b0fc] (2026-10-31T16:17:54Z)
- (ac 1) `python3 plugin/tests/run.py test_which test_hooks` → exit 0 · Ran 266 tests in 70.0s (34 classes, 16 at a time; slowest: Stop 70s, NoTaskGate 54s, PreToolUse 51s) / OK [ran] [tree 504a23ee207f] (2026-10-31T16:19:31Z)
- (audit intent) `fm-reviewer pass (intent, adversary, edge, maintainer) on the lane diff; findings fixed in f3116dd4 before merge` → every shelf searched, each row with source and grant, local first [tree 504a23ee207f] (2026-10-31T16:19:31Z)
- (audit adversary) `fm-reviewer pass (intent, adversary, edge, maintainer) on the lane diff; findings fixed in f3116dd4 before merge` → repo-carried rows (a repo's .mcp.json, tools/) labelled unreviewed; the hook note never names a repo tool; ~/.claude.json read only for server names [tree 504a23ee207f] (2026-10-31T16:19:31Z)
- (audit edge) `fm-reviewer pass (intent, adversary, edge, maintainer) on the lane diff; findings fixed in f3116dd4 before merge` → missing or unreadable config and absent shelves are named as skipped, no crash [tree 504a23ee207f] (2026-10-31T16:19:31Z)
- (audit maintainer) `fm-reviewer pass (intent, adversary, edge, maintainer) on the lane diff; findings fixed in f3116dd4 before merge` → one shelf function per source in fmwhich, each with its own test [tree 504a23ee207f] (2026-10-31T16:19:31Z)
## Log
- 2026-10-31T14:01:59Z created
- 2026-10-31T15:35:58Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2371.builder.md
- 2026-10-31T15:37:19Z focused
- 2026-10-31T15:37:22Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-10-31T15:57:02Z set scope=['plugin/lib/fmwhich.py', 'plugin/lib/fmhooks.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_which.py', 'plugin/tests/test_hooks.py', 'plugin/tests/helpers.py', 'MASTER.md', 'README.md', 'CHANGELOG.md']
- 2026-10-31T15:57:03Z scope widened: coordinator review nits need fmcli which help and tests/helpers.py HOME isolation
- 2026-10-31T16:12:01Z merged worktree-agent-acacbf6c4b424bb18 (8 file(s))
- 2026-10-31T16:12:01Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-acacbf6c4b424bb18
- 2026-10-31T16:17:13Z focused
- 2026-10-31T16:21:02Z done
- 2026-10-31T16:21:05Z committed 29838df1 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1397 [FEATURE M, done, 1 steps] Intake offer: fm code prints one line when an indexed skill matches the request (name, lic — lesson: Stack cards name tools (cargo) mor…
- research mission-20261031-083834: Request: Mission 6, Genesis gen 1: 5. Getting the tools it lacks. When it hits something it can't do, it finds an existing plugin, skil…
- T-2192 [FIX M, done, 4 steps] The foreman arm still trails the free finders on s31-006 with session-start leads: 10/18… — lesson: A grade that reads one reply object sco…
- decision 2026-10-30: [cites: the user's steer 2026-10-30 (seventh): STANDING INTENT] [check: pending T-2191] The user's standing intent (on top of every earlier steer, u…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_hooks.py, plugin/tests/test_which.py
## Preflight
Changed in scope since this was planned (2026-10-31): CHANGELOG.md, MASTER.md, README.md, plugin/lib/fmcli.py, plugin/lib/fmhooks.py, plugin/lib/fmwhich.py, plugin/tests/helpers.py, plugin/tests/test_hooks.py, plugin/tests/test_which.py; re-ground the plan against them before editing
## Lessons
- A search that mixes trusted and repo-carried sources must label provenance on every row, or a cloned repo can pose as an installed tool
## Plan gaps
- failed first: step 1 red tests first in test_which: one per source, the ranking, the receipt event, the note text (test_…
## Files touched
- plugin/tests/test_which.py
- plugin/tests/test_hooks.py
- plugin/lib/fmwhich.py
- plugin/lib/fmhooks.py
- MASTER.md
- README.md
- plugin/tests/helpers.py
- plugin/lib/fmcli.py
- CHANGELOG.md
