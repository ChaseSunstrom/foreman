---
id: T-2197
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T17:57:56Z
updated: 2026-10-31T03:40:47Z
base: 42fedb8d2d0873cf45629af3f6cdb555baaa8e42
base_tree: d23b4b587cf210e1e144c7ec2addb6b1aa622a3f
plan0_at: 2026-10-31T03:10:53Z
plan0_scope: []
verified: strong
---
# fm genesis confirm N: the end-of-run exam marks each lineage choice confirmed or reversed, and the report waits for every mark
## Raw request
> The end-of-run exam writes each lineage choice's '- confirmed:' or '- reversed:' line (fm genesis confirm N, or the production-model exam itself), and the §8 report gate refuses a choice still provisional (T-2171 makes the mark; nothing writes the verdict yet)
## Interpretation
T-2171 marks each lineage choice provisional until the end-of-run exam on the production model (steer 1: Haiku never decides). Nothing writes the final verdict, and the §8 report could be filed on provisional choices. This adds the verb that settles each choice from the production exam and the gate that holds the report until all are settled.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm genesis confirm N reads the production-model exam lines (not smoke, not Haiku) for gen N and its parent on the same run and writes '- confirmed: <why>' when the kept choice still wins or '- reversed: <why>' when it loses, under lineage.md's '## gen-N'; a choice with no production line stays provisional and is named; fm genesis step's report stage refuses while any choice is provisional — verify with `python3 plugin/tests/run.py test_genesis`
## Non-goals
## Approach (options → choice → why)
Options: (1) fm genesis confirm N comparing gen N's and its parent's production-model closed counts on the same run, writing the mark, plus a report-stage gate (chosen: deterministic from exam.jsonl, reuses select's comparison); (2) re-run select with a production flag (select rewrites seeds: too much); (3) mark by hand (unverifiable). Choice 1.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests: confirm writes confirmed/reversed from seeded exam lines, ignores smoke lines, leaves provisional when no production line, report stage refuses provisional
2. [x] confirm(p, n) and the report gate
3. [x] docs (MASTER fmgenesis, CHANGELOG, genesis skill)
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md, plugin/skills/genesis/SKILL.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_genesis 2>&1 | tail -25` → exit 0 · Ran 135 tests in 10.7s (16 classes, 16 at a time; slowest: GenesisRead 9s, GenesisCheck 9s, GenesisDrift 7s) / OK [ran] [tree 875d166a5902] (2026-10-31T03:12:35Z)
- (step 1) `python3 plugin/tests/run.py test_genesis 2>&1 | tail -25` → exit 0 · Ran 135 tests in 10.7s (16 classes, 16 at a time; slowest: GenesisRead 9s, GenesisCheck 9s, GenesisDrift 7s) / OK [ran] [tree 875d166a5902] (2026-10-31T03:12:35Z)
- (step 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 135 tests in 7.5s (16 classes, 16 at a time; slowest: GenesisRead 7s, GenesisCheck 7s, GenesisDrift 6s) / OK [ran] [tree 2059b5877911] (2026-10-31T03:12:53Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_docs test_genesis test_guard_cases test_paused && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [22.06s] [ran] [tree 2059b5877911] (2026-10-31T03:13:48Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis 2>&1 | tail -40` → exit 0 · Ran 142 tests in 8.0s (16 classes, 16 at a time; slowest: GenesisRead 8s, GenesisCheck 7s, GenesisDrift 6s) / OK [ran] [tree a61b96a41f17] (2026-10-31T03:20:56Z)
- (step 2) `python3 plugin/tests/run.py test_genesis 2>&1 | tail -40` → exit 0 · Ran 142 tests in 8.0s (16 classes, 16 at a time; slowest: GenesisRead 8s, GenesisCheck 7s, GenesisDrift 6s) / OK [ran] [tree a61b96a41f17] (2026-10-31T03:20:56Z)
- (step 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 142 tests in 8.1s (16 classes, 16 at a time; slowest: GenesisRead 8s, GenesisCheck 7s, GenesisDrift 6s) / OK [ran] [tree 7b06996c0416] (2026-10-31T03:21:24Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_away test_board_verbs test_cli test_code test_code_envelope test_code_hardening test_code_worker test_cost test_cost_forecast test_design_gates test_design_lint test_design_sprint test_docs test_drive_side test_economics test_edit_cards test_exam test_export test_fmpy test_genesis test_goal test_guard_cases test_guard_evasions test_hooks test_judge_home test_mandate test_map test_mcp test_memory test_motion_verify test_onwrite test_paused test_projects test_replay test_round_g test_runner_lint test_showpieces test_site test_site_build test_site_hero test_statusline_ui test_suite_hygiene test_taste_ledger test_tool_taint test_ui_signals && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.57s] [ran] [tree 7b06996c0416] (2026-10-31T03:23:15Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis 2>&1 | tail -15` → exit 0 · Ran 142 tests in 7.3s (16 classes, 16 at a time; slowest: GenesisRead 7s, GenesisCheck 7s, GenesisDrift 5s) / OK [ran] [tree 30d1e5c75818] (2026-10-31T03:27:12Z)
- (step 3) `python3 plugin/tests/run.py test_genesis 2>&1 | tail -15` → exit 0 · Ran 142 tests in 7.3s (16 classes, 16 at a time; slowest: GenesisRead 7s, GenesisCheck 7s, GenesisDrift 5s) / OK [ran] [tree 30d1e5c75818] (2026-10-31T03:27:12Z)
- `python3 plugin/tests/run.py test_genesis` → ✗ exit 1 · Ran 142 tests in 7.9s (16 classes, 16 at a time; slowest: GenesisRead 7s, GenesisCheck 6s, GenesisDrift 5s) / FAILED (3 classes) (start tree + this task's tests) [ran] [tree 9afca3ec4280] (2026-10-31T03:29:09Z)
- `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 142 tests in 7.0s (16 classes, 16 at a time; slowest: GenesisRead 7s, GenesisCheck 6s, GenesisDrift 5s) / OK [ran] [tree 9afca3ec4280] (2026-10-31T03:29:09Z)
- (step 1) `python3 plugin/tests/run.py test_genesis test_cli test_docs` → exit 0 · Ran 359 tests in 20.2s (75 classes, 16 at a time; slowest: TaskLifecycle 20s, Fences 10s, GenesisRead 9s) / OK [ran] [tree 9afca3ec4280] (2026-10-31T03:29:41Z)
- (step 2) `python3 plugin/tests/run.py test_genesis test_cli test_docs` → exit 0 · Ran 359 tests in 20.4s (75 classes, 16 at a time; slowest: TaskLifecycle 20s, GenesisRead 10s, Fences 10s) / OK [ran] [tree 9afca3ec4280] (2026-10-31T03:30:02Z)
- (step 3) `python3 plugin/tests/run.py test_genesis test_cli test_docs` → exit 0 · Ran 359 tests in 20.2s (75 classes, 16 at a time; slowest: TaskLifecycle 20s, Fences 10s, GenesisRead 9s) / OK [ran] [tree 9afca3ec4280] (2026-10-31T03:30:22Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 142 tests in 7.1s (16 classes, 16 at a time; slowest: GenesisRead 7s, GenesisCheck 7s, GenesisDrift 5s) / OK [ran] [tree 9afca3ec4280] (2026-10-31T03:30:30Z)
- (audit intent) `fm-reviewer intent+adversary+edge+maintainer: changes needed, fixed in 21b78956 and c283c5f2: a kept or reverted choice needs production lines for gen N and its parent on a common run (only a baseline choice confirms from its own), production means a stamped non-Haiku line (default is the configured production model per T-2158; unstamped pre-stamp lines don't count), confirm files an OWNED gen-N/confirm.md and the report gate needs a matching record for every mark (a hand-typed confirmed blocks), the stopped path is gated too, the blocked step's command is the production exam run when no line exists (no spin), select's output is unchanged, a reversal rewrites the seed base, genesis_confirm is logged; test_genesis 142 green; red-to-green proven` → the end-of-run exam on the production model settles each lineage choice and the report waits for every one [tree 9afca3ec4280] (2026-10-31T03:30:30Z)
- (audit adversary) `fm-reviewer intent+adversary+edge+maintainer: changes needed, fixed in 21b78956 and c283c5f2: a kept or reverted choice needs production lines for gen N and its parent on a common run (only a baseline choice confirms from its own), production means a stamped non-Haiku line (default is the configured production model per T-2158; unstamped pre-stamp lines don't count), confirm files an OWNED gen-N/confirm.md and the report gate needs a matching record for every mark (a hand-typed confirmed blocks), the stopped path is gated too, the blocked step's command is the production exam run when no line exists (no spin), select's output is unchanged, a reversal rewrites the seed base, genesis_confirm is logged; test_genesis 142 green; red-to-green proven` → confirm.md is OWNED and the gate checks it against the mark, so a typed mark counts for nothing; Haiku and unstamped lines never decide [tree 9afca3ec4280] (2026-10-31T03:30:30Z)
- (audit edge) `fm-reviewer intent+adversary+edge+maintainer: changes needed, fixed in 21b78956 and c283c5f2: a kept or reverted choice needs production lines for gen N and its parent on a common run (only a baseline choice confirms from its own), production means a stamped non-Haiku line (default is the configured production model per T-2158; unstamped pre-stamp lines don't count), confirm files an OWNED gen-N/confirm.md and the report gate needs a matching record for every mark (a hand-typed confirmed blocks), the stopped path is gated too, the blocked step's command is the production exam run when no line exists (no spin), select's output is unchanged, a reversal rewrites the seed base, genesis_confirm is logged; test_genesis 142 green; red-to-green proven` → parent with no production line, gen 1's baseline, a common run missing, a one-scenario margin, a reversed choice's seed base [tree 9afca3ec4280] (2026-10-31T03:30:30Z)
- (audit maintainer) `fm-reviewer intent+adversary+edge+maintainer: changes needed, fixed in 21b78956 and c283c5f2: a kept or reverted choice needs production lines for gen N and its parent on a common run (only a baseline choice confirms from its own), production means a stamped non-Haiku line (default is the configured production model per T-2158; unstamped pre-stamp lines don't count), confirm files an OWNED gen-N/confirm.md and the report gate needs a matching record for every mark (a hand-typed confirmed blocks), the stopped path is gated too, the blocked step's command is the production exam run when no line exists (no spin), select's output is unchanged, a reversal rewrites the seed base, genesis_confirm is logged; test_genesis 142 green; red-to-green proven` → confirm and select share _compare [tree 9afca3ec4280] (2026-10-31T03:30:30Z)
## Log
- 2026-10-30T17:57:56Z created
- 2026-10-31T03:10:22Z planned from capture
- 2026-10-31T03:10:22Z set approved=True
- 2026-10-31T03:10:28Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2197.builder.md
- 2026-10-31T03:10:53Z focused
- 2026-10-31T03:28:52Z merged worktree-agent-ab81f050df396ac52 (6 file(s))
- 2026-10-31T03:28:52Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ab81f050df396ac52
- 2026-10-31T03:28:53Z focused
- 2026-10-31T03:30:22Z scope: plugin/lib/fmgenesis.py (confirm, _prod, _compare, step's gate), plugin/lib/fmcli.py (confirm), plugin/tests/test_genesis.py, MASTER.md, CHANGELOG.md, plugin/skills/genesis/SKILL.md
- 2026-10-31T03:31:05Z done
- 2026-10-31T03:31:14Z guard authorization added: publish
- 2026-10-31T03:40:47Z guard authorization added: publish
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2171 [FIX M, done, 3 steps] fm genesis select doesn't mark lineage.md choices provisional (steer 1 rule 4): until… — lesson: A mark that a later stage must settle need…
- T-2158 [FEATURE M, done, 2 steps] Haiku scores are smoke signals only: fm exam scorecard, fm genesis select and the done… — lesson: A line that records what produced it …
- decision 2026-10-30: [revisited: until the end-of-run exam, selection] [cites: the user's steer 2026-10-30: standing rules for the rest of the genesis run] [check: pendi…
- decision 2026-10-30: [revisited: until the end-of-run exam, selection] [cites: the user's steer 2026-10-30: standing rules for the rest of the genesis run] [check: pytho…
## Lessons
- A verdict that unblocks a gate must leave a record only its verb can write, or a typed line opens the gate
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
- plugin/lib/fmcli.py
- MASTER.md
- plugin/skills/genesis/SKILL.md
- CHANGELOG.md
