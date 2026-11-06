---
id: T-2276
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-31T05:49:25Z
updated: 2026-10-31T06:29:37Z
base: 7ced78e6286117f2f4d214be161c2ce28a166460
base_tree: 9876e5765606f45573ccce07f57b1baf1bc4a45f
plan0_at: 2026-10-31T05:50:06Z
plan0_scope: []
verified: strong
---
# Trigger routing learns from outcomes (Mission 8/#11): fm triggers lists each trigger kind (fired, done, dropped, open, precision), and a trigger whose captures are mostly dropped files at low priority
## Raw request
> Trigger routing learns from outcomes (Mission 8/#11): fm triggers lists each trigger kind (fired, done, dropped, open, precision), and a trigger whose captures are mostly dropped files at low priority
## Interpretation
Gap map #11 (trigger→task routing table, tier 4) and #7 (signal→fix): Foreman files tasks from many triggers (baseline red, CI, spec, scout probes, friction, capability misses, recurring failures, discovered work), each at a fixed priority. Nobody sees which triggers earn their keep: a noisy trigger keeps filing tasks that get dropped, and the inbox fills with them.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm triggers [--days N] [--json] groups capture events by trigger kind (capture_once's new trigger= name, defaulting to its source) with fired/done/dropped/open counts and precision done/(done+dropped); capture_once files a capture at priority low with a note when its trigger has 5+ closed captures and precision under 0.3; a trigger with too few closed captures is unchanged — verify with `python3 plugin/tests/run.py test_triggers test_eco`
## Non-goals
## Approach (options → choice → why)
1) one learned table from data already kept: capture_once gains trigger= (default: its source) and logs it on the capture event; fm triggers reads capture events and each captured brief's final status (done, dropped, open) per trigger; capture_once demotes to priority low (with a note naming the record) when the trigger's precision over its last 20 closed captures is under 0.3 and it has 5+. 2) a hand-written routing table per trigger — rejected: lists go stale (learn gaps from data). 3) stop filing from low-precision triggers — rejected: demote, never silence; a rare true capture still lands. Choice 1.
## Risks and rollback
Urgent triggers (baseline red, security) must never be demoted: they keep their priority whatever the precision. Old capture events have no trigger field: grouped by source.
## Execution prompt
## Steps
1. [x] red tests: counts per trigger from seeded captures and closes; low precision demotes; few closes don't
2. [x] trigger= on capture_once and its callers (baseline, ci, spec, capability-miss, recurring-failure, scout, friction); the precision read; fm triggers verb with --json
3. [x] docs: MASTER, CHANGELOG; fm status names the noisiest trigger
## Resume here
<!-- auto -->
- 2026-10-31T06:26:47Z steps 3/3 done
- git: foreman/build; 0 uncommitted
- touched since last checkpoint: .claude/worktrees/agent-a39f92fdb0efec0c2/plugin/tests/test_triggers.py, .claude/worktrees/agent-a39f92fdb0efec0c2/plugin/lib/fmtriggers.py, .claude/worktrees/agent-a39f92fdb0efec0c2/plugin/lib/fmeco.py, .claude/worktrees/agent-a39f92fdb0efec0c2/.gitignore, .claude/worktrees/agent-a39f92fdb0efec0c2/CHANGELOG.md, .claude/worktrees/agent-a39f92fdb0efec0c2/README.md, .claude/worktrees/agent-a39f92fdb0efec0c2/plugin/agents/fm-builder.md, .claude/worktrees/agent-a39f92fdb0efec0c2/plugin/lib/fmcli.py, .claude/worktrees/agent-a39f92fdb0efec0c2/plugin/lib/fmcore.py, .claude/worktrees/agent-a39f92fdb0efec0c2/plugin/lib/fmcost.py, .claude/worktrees/agent-a39f92fdb0efec0c2/plugin/lib/fmexam.py, .claude/worktrees/agent-a39f92fdb0efec0c2/plugin/lib/fmgenesis.py, .claude/worktrees/agent-a39f92fdb0efec0c2/plugin/lib/fmlong.py, .claude/worktrees/agent-a39f92fdb0efec0c2/plugin/tests/genesis_page.js, .claude/worktrees/agent-a39f92fdb0efec0c2/plugin/tests/test_docs.py
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_triggers test_eco` → exit 0 · Ran 30 tests in 3.9s (11 classes, 16 at a time; slowest: HarnessCanary 4s, Sweep 2s, AdoptHistory 1s) / OK [ran] [tree a819b70ab62b] (2026-10-31T05:52:31Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_away test_board_verbs test_cli test_docs test_drive_side test_ecosystem test_foresight test_goal test_guard_cases test_guard_evasions test_hooks test_mcp test_memory test_onwrite test_paused test_recall test_repeats test_tool_taint test_triggers test_trust test_ui_signals && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 671 tests in 78.2s (146 classes, 16 at a time; slowest: Stop 78s, NoTaskGate 58s, PreToolUse 56s) / FAILED (1 classes) [ran] [tree a819b70ab62b] (2026-10-31T05:53:49Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_away test_board_verbs test_cli test_core test_docs test_drive_side test_ecosystem test_foresight test_goal test_guard_cases test_guard_evasions test_hooks test_mcp test_memory test_onwrite test_paused test_reasoning test_recall test_repeats test_tool_taint test_triggers test_trust test_ui_signals && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [21.07s] [ran] [tree 93f8c2b0e633] (2026-10-31T05:59:48Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_away test_board_verbs test_cli test_core test_docs test_drive_side test_ecosystem test_foresight test_goal test_guard_cases test_guard_evasions test_hooks test_mcp test_memory test_onwrite test_paused test_reasoning test_recall test_repeats test_tool_taint test_triggers test_trust test_ui_signals && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [14.07s] [ran] [tree edea23c496c5] (2026-10-31T06:15:01Z)
- `python3 plugin/tests/run.py test_triggers test_eco test_mcp` → ✗ exit 1 · Ran 58 tests in 4.9s (21 classes, 16 at a time; slowest: HarnessCanary 4s, McpNew 2s, McpTools 2s) / FAILED (2 classes) (start tree + this task's tests) [ran] [tree 3d0c935f970f] (2026-10-31T06:26:35Z)
- `python3 plugin/tests/run.py test_triggers test_eco test_mcp` → exit 0 · Ran 58 tests in 3.9s (21 classes, 16 at a time; slowest: HarnessCanary 4s, McpNew 2s, Triggers 2s) / OK [ran] [tree 3d0c935f970f] (2026-10-31T06:26:35Z)
- (step 1) `python3 plugin/tests/run.py test_triggers test_eco test_mcp` → exit 0 · Ran 58 tests in 4.0s (21 classes, 16 at a time; slowest: HarnessCanary 4s, McpNew 2s, Triggers 2s) / OK [ran] [tree 3d0c935f970f] (2026-10-31T06:26:39Z)
- (step 2) `python3 plugin/tests/run.py test_triggers test_eco test_mcp` → exit 0 · Ran 58 tests in 4.0s (21 classes, 16 at a time; slowest: HarnessCanary 4s, McpNew 2s, Triggers 2s) / OK [ran] [tree 3d0c935f970f] (2026-10-31T06:26:43Z)
- (step 3) `python3 plugin/tests/run.py test_triggers test_eco test_mcp` → exit 0 · Ran 58 tests in 3.9s (21 classes, 16 at a time; slowest: HarnessCanary 4s, McpNew 2s, Sweep 2s) / OK [ran] [tree 3d0c935f970f] (2026-10-31T06:26:47Z)
- (ac 1) `python3 plugin/tests/run.py test_triggers test_eco` → exit 0 · Ran 35 tests in 5.6s (11 classes, 16 at a time; slowest: HarnessCanary 5s, Triggers 2s, Sweep 2s) / OK [ran] [tree 3d0c935f970f] (2026-10-31T06:28:05Z)
- (audit intent) `self + one fm-reviewer pass (1 medium: the noisiest line and the demotion used different windows; 4 low; all fixed with tests); fm state's line measured and cached` → Foreman sees which of its own triggers earn their keep, and a noisy one files at low priority instead of crowding the inbox (test_triggers red-to-green) [tree 3d0c935f970f] (2026-10-31T06:28:05Z)
- (audit adversary) `self + one fm-reviewer pass (1 medium: the noisiest line and the demotion used different windows; 4 low; all fixed with tests); fm state's line measured and cached` → baseline, CI and security captures are never demoted; a failure computing precision never loses a capture; the MCP tool is read-only [tree 3d0c935f970f] (2026-10-31T06:28:05Z)
- (audit edge) `self + one fm-reviewer pass (1 medium: the noisiest line and the demotion used different windows; 4 low; all fixed with tests); fm state's line measured and cached` → fewer than 5 closed captures changes nothing; --days clamped; archived briefs counted [tree 3d0c935f970f] (2026-10-31T06:28:05Z)
- (audit operator) `self + one fm-reviewer pass (1 medium: the noisiest line and the demotion used different windows; 4 low; all fixed with tests); fm state's line measured and cached` → demotion is computed before the lock; fm triggers loads once [tree 3d0c935f970f] (2026-10-31T06:28:05Z)
## Log
- 2026-10-31T05:49:25Z created
- 2026-10-31T05:49:33Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2276.builder.md
- 2026-10-31T05:50:05Z focused
- 2026-10-31T06:17:43Z merged worktree-agent-a39f92fdb0efec0c2 (11 file(s))
- 2026-10-31T06:17:43Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a39f92fdb0efec0c2
- 2026-10-31T06:26:25Z focused
- 2026-10-31T06:26:47Z paused: focus moved to T-2239
- 2026-10-31T06:27:57Z focused
- 2026-10-31T06:27:59Z scope: plugin/lib/fmtriggers.py (new), plugin/lib/fmeco.py (capture_once trigger=, demotion), callers' trigger= (fmrecall, fmforesight, fmhooks, forge), plugin/lib/fmcli.py (triggers parser, fm state line), plugin/lib/fmmcp.py (triggers tool), plugin/tests/test_triggers.py, test_mcp.py, MASTER.md, CHANGELOG.md
- 2026-10-31T06:29:37Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2124 [FEATURE M, done, 2 steps] Scout project probes: fm find + prove on the user's own project, at most 3 a day, proven only, refutation ledger, doctor faults to the …
- research draft-mission-genesis-gen1: Task: T-2093 (brief 1, fm genesis check), T-2095 (brief 2, fm genesis step), T-2099 (brief 3, fm genesis draft/spec), T-2102 (brief …
- T-2125 [FEATURE M, done, 3 steps] Value ranking: severity x proof x reach / effort, per-finder precision from outcomes, a mute floor, abstain below a threshold (Mission …
- decision 2026-10-30: [cites: the user's steer 2026-10-30 (sixth): the frame may grow, never shrink] [check: pending T-2188] Standing rule from gen 2 on: the Genesis fram…
## Lessons
- A summary line and the rule it summarizes must call the same function, or the surface reports a rule that isn't the one acting
## Files touched
- plugin/tests/test_triggers.py
- plugin/lib/fmtriggers.py
- plugin/lib/fmeco.py
- plugin/lib/fmcli.py
- plugin/lib/fmrecall.py
- plugin/lib/fmforesight.py
- plugin/lib/fmhooks.py
- plugin/lib/fmrepeats.py
- plugin/lib/fmmcp.py
- MASTER.md
- plugin/tests/test_mcp.py
- .gitignore
- CHANGELOG.md
- README.md
- plugin/agents/fm-builder.md
- plugin/lib/fmcore.py
- plugin/lib/fmcost.py
- plugin/lib/fmexam.py
- plugin/lib/fmgenesis.py
- plugin/lib/fmlong.py
- plugin/tests/genesis_page.js
- plugin/tests/test_docs.py
- plugin/tests/test_genesis.py
- plugin/tests/test_long.py
- plugin/tests/test_proof.py
- plugin/tests/test_site_build.py
- site/genesis/genesis.js
- site/genesis/index.html
- plugin/lib/fmfind.py
- plugin/tests/test_find.py
