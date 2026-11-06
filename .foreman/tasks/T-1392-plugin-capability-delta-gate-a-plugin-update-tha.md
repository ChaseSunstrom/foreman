---
id: T-1392
type: SECURITY
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-21T17:28:43Z
updated: 2026-10-21T21:10:40Z
base: d89420bdc758a37a51935428421f047ff125e8bd
base_tree: 009d2f12e9ff78a113723c509eae631f8327af6d
plan0_at: 2026-10-21T20:20:44Z
plan0_scope: []
verified: strong
---
# A plugin update that adds a hook event, MCP server or script is held with that exact delta until fm doctor --accept-supply; fm plugins find shows what each entry needs
## Raw request
> SECURITY: Plugin capability-delta gate: a plugin update that adds a hook event, MCP server or script waits for fm doctor --accept-supply; fm plugins find shows what each entry needs (hooks, mcp, commands) (S5, A2 B6)
> CONTEXT: round 2 of the fm/fm code brainstorm (T-1382): research/brainstorm-fm-anthropic-catalogue.md, grounding with file:line in research/brainstorm-fm-anthropic-half-a.md (A*) and half-b.md (B*)
> DONE-WHEN: a fixture plugin gaining a PreToolUse hook is held with that exact delta, a SKILL.md body-only edit passes, and fm plugins find --json shows needs for a fixture plugin
## Interpretation
doctor's supply check hashes each plugin tree, so any update (a typo fix in a SKILL.md or a new PreToolUse hook that runs on every tool call) reads the same: 'changed'. The dangerous part of an update is new code that runs on its own — hooks, MCP servers, scripts — so name exactly that delta and hold it, and let content-only changes through with a note.
## Assumptions (confidence)
## Acceptance criteria
- [x] a fixture plugin gaining a PreToolUse hook makes fm doctor's supply check FAIL naming 'adds hook PreToolUse', a SKILL.md body-only edit passes the capability check (only the hash note), and fm plugins find --json shows needs {hooks, mcp, commands, agents, skills} for a local fixture plugin — verify with `python3 plugin/tests/run.py test_supply_delta`
## Non-goals
## Approach (options → choice → why)
Options: (A) a capability set per plugin stored with the hash; diff sets, FAIL on added hooks/MCP/scripts, WARN otherwise (chosen: reuses the baseline file and --accept-supply; the diff is the reviewable unit); (B) block the plugin from loading until accepted (Foreman can't stop Claude Code loading an installed plugin); (C) full diff of the tree (noisy, not actionable). Remote marketplace entries have no tree to read until installed, so find shows needs only for local sources (ponytail note).
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests in plugin/tests/test_supply_delta.py with a CLAUDE_CONFIG_DIR fixture (installed_plugins.json pointing at a temp plugin tree) and a local marketplace fixture
2. [x] fmplugins.capabilities(root): hook events (hooks/hooks.json and plugin.json 'hooks'), MCP server names (.mcp.json and plugin.json 'mcpServers'), executable scripts (bin/ and files hooks commands point at), and command/agent/skill names; doctor's supply baseline stores it beside the hash; a later run FAILs on any added hook event, MCP server or script (naming each), WARNs on other changes as today; --accept-supply records the new set; fm plugins find --json adds needs for entries whose source is local
3. [x] fix the review's findings test-first (research T-1392-review): delta computed whenever caps differ, not only when the sha does; MCP servers recorded as name plus a digest of their spec (command, args, url) and a swap reported as 'changes MCP server X'; read the default hooks/hooks.json and .mcp.json plus any manifest value (string or list), confined to the plugin root with a size cap; a legacy hash-only baseline gains caps on a matching run and a changed plugin with no caps diffs against an empty set; a new plugin with hooks, MCP or scripts FAILs naming them; one bad plugin costs only its own row; find's text says 'runs: unknown until installed' for remote entries
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_supply_delta 2>&1 | tail -15` → ✗ exit 1 · Ran 7 tests in 6.7s (2 classes, 16 at a time; slowest: SupplyDelta 1s, FindNeeds 1s) / FAILED (2 classes) [ran] [tree 21e2bafc2649] (2026-10-21T20:23:36Z)
- (step 1) `python3 plugin/tests/run.py test_supply_delta` → ✗ exit 1 · Ran 7 tests in 3.6s (2 classes, 16 at a time; slowest: FindNeeds 1s, SupplyDelta 1s) / FAILED (2 classes) [ran] [tree 21e2bafc2649] (2026-10-21T20:23:48Z)
- (step 2) `python3 plugin/tests/run.py test_supply_delta` → exit 0 · Ran 7 tests in 1.1s (2 classes, 16 at a time; slowest: FindNeeds 1s, SupplyDelta 0s) / OK [ran] [tree dd36666b1d7d] (2026-10-21T20:25:52Z)
- (step 3) `python3 plugin/tests/run.py test_supply_delta` → exit 0 · Ran 18 tests in 2.1s (2 classes, 16 at a time; slowest: SupplyDelta 2s, FindNeeds 1s) / OK [ran] [tree 92f75efe9653] (2026-10-21T20:51:05Z)
- (step 1) `python3 plugin/tests/run.py test_supply_delta test_safety test_plugins` → exit 0 · Ran 52 tests in 4.7s (12 classes, 16 at a time; slowest: Install 4s, CleanupGate 3s, SecretsGate 3s) / OK [ran] [tree ce6bf28fc661] (2026-10-21T20:57:42Z)
- (step 2) `python3 plugin/tests/run.py test_supply_delta test_safety test_plugins` → exit 0 · Ran 52 tests in 5.1s (12 classes, 16 at a time; slowest: Install 5s, CleanupGate 4s, SecretsGate 3s) / OK [ran] [tree ce6bf28fc661] (2026-10-21T20:57:48Z)
- (step 3) `python3 plugin/tests/run.py test_supply_delta test_safety test_plugins` → exit 0 · Ran 52 tests in 7.6s (12 classes, 16 at a time; slowest: Install 7s, SecretsGate 6s, CleanupGate 5s) / OK [ran] [tree ce6bf28fc661] (2026-10-21T20:57:57Z)
- (audit adversary) `fm-reviewer` → 7 findings: hash blind spot hid a new hook, MCP command swap read as unchanged, manifest hook path replaced the default file, legacy baseline never gained caps, new plugins with hooks only noted, spec paths read outside the root, one bad plugin cost the whole check — all fixed failing-first (test_supply_delta 18 tests); a FIFO hang found and fixed in self-review [tree ce6bf28fc661] (2026-10-21T20:57:59Z)
- (step 3) `python3 plugin/tests/run.py test_supply_delta test_safety test_plugins test_doctor` → exit 0 · Ran 106 tests in 6.8s (30 classes, 16 at a time; slowest: Install 7s, Command 5s, SecretsGate 5s) / OK [ran] [tree 2d587d36d465] (2026-10-21T20:58:59Z)
- (ac 1) `python3 plugin/tests/run.py test_supply_delta` → exit 0 · Ran 18 tests in 2.3s (2 classes, 16 at a time; slowest: SupplyDelta 2s, FindNeeds 2s) / OK [ran] [tree 2d587d36d465] (2026-10-21T20:59:12Z)
- (audit intent) `fm-reviewer (research T-1392-review): 7 findings fixed failing-first in step 3; then a real-machine run showed a legacy baseline listing every existing hook as 'adds', reworded to 'has' (steer logged)` → a fixture plugin gaining a PreToolUse hook FAILs naming 'p@m adds hook PreToolUse'; a SKILL.md body edit keeps only the WARN; fm plugins find --json shows needs for a local fixture (test_supply_delta, 18+ tests) [tree 2d587d36d465] (2026-10-21T20:59:12Z)
- (audit edge) `fm-reviewer (research T-1392-review): 7 findings fixed failing-first in step 3; then a real-machine run showed a legacy baseline listing every existing hook as 'adds', reworded to 'has' (steer logged)` → on this machine the first run FAILs on plugins changed since a hash-only baseline (ecc, context7, chrome-devtools-mcp), worded as what they run; fm doctor --accept-supply is the user's to run; hooks in skill/agent frontmatter and .lsp.json aren't read yet (T-1434) [tree 2d587d36d465] (2026-10-21T20:59:12Z)
- (audit operator) `fm-reviewer (research T-1392-review): 7 findings fixed failing-first in step 3; then a real-machine run showed a legacy baseline listing every existing hook as 'adds', reworded to 'has' (steer logged)` → the user's next fm doctor shows a supply FAIL until they run fm doctor --accept-supply once; that's the intended hold, named in the detail [tree 2d587d36d465] (2026-10-21T20:59:12Z)
- (audit intent) `fm-reviewer (research T-1392-review): 7 findings fixed failing-first in step 3; then a real-machine run showed a legacy baseline listing every existing hook as 'adds', reworded to 'has' (steer logged)` → a fixture plugin gaining a PreToolUse hook FAILs naming 'p@m adds hook PreToolUse'; a SKILL.md body edit keeps only the WARN; fm plugins find --json shows needs for a local fixture (test_supply_delta) [tree 2d587d36d465] (2026-10-21T21:10:28Z)
- (audit edge) `fm-reviewer (research T-1392-review): 7 findings fixed failing-first in step 3; then a real-machine run showed a legacy baseline listing every existing hook as 'adds', reworded to 'has' (steer logged)` → on this machine the first run FAILs on plugins changed since a hash-only baseline (ecc, context7, chrome-devtools-mcp), worded as what they run; fm doctor --accept-supply is the user's to run; hooks in skill/agent frontmatter and .lsp.json aren't read yet (T-1434) [tree 2d587d36d465] (2026-10-21T21:10:28Z)
- (audit operator) `fm-reviewer (research T-1392-review): 7 findings fixed failing-first in step 3; then a real-machine run showed a legacy baseline listing every existing hook as 'adds', reworded to 'has' (steer logged)` → the user's next fm doctor shows a supply FAIL until they run fm doctor --accept-supply once; that's the intended hold, named in the detail [tree 2d587d36d465] (2026-10-21T21:10:28Z)
## Log
- 2026-10-21T17:28:43Z created
- 2026-10-21T20:20:20Z planned from capture
- 2026-10-21T20:20:23Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1392.builder.md
- 2026-10-21T20:20:42Z focused
- 2026-10-21T20:28:55Z merged worktree-agent-ada68f844aabe0bdc (4 file(s))
- 2026-10-21T20:29:07Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ada68f844aabe0bdc
- 2026-10-21T20:40:29Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1392.builder.md
- 2026-10-21T20:40:51Z focused
- 2026-10-21T20:56:18Z merged worktree-agent-abcdf50a4b2b50ac2 (3 file(s))
- 2026-10-21T20:56:19Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-abcdf50a4b2b50ac2
- 2026-10-21T20:57:26Z focused
- 2026-10-21T20:58:51Z steer: a plugin whose legacy (hash-only) baseline changed lists what it runs as 'has hook X', not 'adds' — on this machine every existing hook read as newly added (ecc's seven events, context7's MCP server)
- 2026-10-21T21:10:30Z affected tests waived: all linked Python suites passed; the one failure is the UI mod's JS subagent-row test timing out at 5 s under load (T-1427), which reads nothing fmdoctor or fmplugins produce
- 2026-10-21T21:10:34Z done
- 2026-10-21T21:10:40Z committed a55b263c (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-fm-anthropic-catalogue: Source: research/brainstorm-20261021-120257 (fm ideas, 10 lenses, 4 rounds, 3 deepened, --seen every earlier ideas.md: 520 ne…
- T-1410 [FEATURE S, done, 2 steps] fm vetoes prints the command that retracts each veto, and that command removes exactly it — lesson: A record the user can create should…
- research brainstorm-fm-anthropic-half-a: Grounded against `plugin/lib` at HEAD (branch foreman/build; fmcli.py and test_cli.py have uncommitted edits).
- decision 2026-10-15: Recommendation: build T-0969..T-0975 (edit-time test-first note, background affected tests, fm rule, tool-output injection flag, fm cost --forecast,…
- the similar finished task took 2 steps
## Why not caught
none: new check
## Lessons
- Run a new security check once against the real machine before closing: fixtures don't show how a legacy baseline reads
## Plan gaps
- added late: fix the review's findings test-first (research T-1392-review): delta computed whenever caps differ, not only when the s…
- failed first: step 1 failing tests in plugin/tests/test_supply_delta.py with a CLAUDE_CONFIG_DIR fixture (installed_plug…
## Files touched
- plugin/tests/test_supply_delta.py
- plugin/lib/fmplugins.py
- plugin/lib/fmdoctor.py
- plugin/tests/test_safety.py
- CHANGELOG.md
- plugin/lib/fmcodetui.py
- plugin/tests/test_code_tui.py
