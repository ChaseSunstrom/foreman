---
id: T-3053
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/sampo/rune.py, plugin/lib/sampo/cli.py, plugin/lib/sampo/moonscale.py, plugin/lib/sampo/steer.py, plugin/lib/sampo/louhi.py, plugin/tests/test_kalevala.py, MASTER.md]
depends_on: []
source: user
created: 2026-11-05T00:20:51Z
updated: 2026-11-05T12:44:00Z
builder_model: haiku
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-05T00:21:10Z
plan0_scope: [plugin/lib/sampo/rune.py, plugin/lib/sampo/cli.py, plugin/lib/sampo/moonscale.py, plugin/tests/test_kalevala.py]
lane_stop: merged 2026-11-05T12:39:16Z
base: 4b6d7f0cd032a0ebb3ca52c8d2ecba676d9b670d
base_tree: ca2fbf6a1ea72e91c527a4b3bb026a20054cf2b1
verified: strong
unproven: [docs]
---
# Kalevala part 1: tower namespaces: each Rune tower its own home under one project, sampo genesis --tower NAME, a shared root for moons and the user's steers (T-3050)
## Raw request
> Kalevala part 1: tower namespaces: each Rune tower its own home under one project, sampo genesis --tower NAME, a shared root for moons and the user's steers (T-3050)
## Interpretation
Reading 1 (taken): the groundwork for Kalevala (T-3050): many Rune towers in one project, each its own home, gen-0, lineage and exam record, the root tower untouched, and the stores every tower should share (moons, exam scenarios, the user's steers) kept at the root. Reading 2 (ruled out): one project per tower: splits the moons and exam stores and makes towers' state hard to read together.
## Assumptions (confidence)
## Acceptance criteria
- [x] Every sampo genesis verb takes --tower NAME and works on that tower's own home (research/genesis/towers/NAME): init seals its gen-0, step, seed, drift, sweep, select and status read and write only there; without --tower the root tower behaves exactly as today — verify with `python3 plugin/tests/run.py test_kalevala test_genesis`
- [x] Shared, not split: the moons store, the exam scenarios and the user's steers stay at the root for every tower; a tower's own steer file adds to them — verify with `python3 plugin/tests/run.py test_kalevala test_genesis`
- [x] sampo genesis towers lists each tower with its aspect, generation, last select verdict and drift verdict; a bad tower name is refused — verify with `python3 plugin/tests/run.py test_kalevala test_genesis`
## Non-goals
## Approach (options → choice → why)
1) use what exists: rune.home(p) honours a tower name set by --tower for the process, and a new rune.root(p) serves the shared stores; every rune verb follows home: likely outcome: a small diff, the four proven generations unchanged. 2) a tower field on Project: fails if: every Project constructor across the code changes for one feature. 3) an environment variable naming the tower: fails if: Claude Code's shell strips SAMPO_* variables, so builders and tests can't set it. 4) do less: towers as subfolders without verbs knowing: fails if: drift, seal and select read the root's files. Choice 1 (80%): one switch, one function; moonscale's store moves to rune.root.
## Risks and rollback
Blast radius (sampo graph blast): co-changes plugin/tests/test_moons_scale.py, plugin/lib/sampo/louhi.py, MASTER.md, plugin/tests/test_lanes.py, plugin/lib/sampo/core.py; past FIXes T-2814, T-2836, T-2863, T-2940, T-2993.
## Execution prompt
Read the parent's brief first (state/projects/foreman-4a056f/tasks/T-3050-is-it-possible-to-have-orchestrators-of-orcehstr.md): Kalevala runs many Rune towers at once on aspects of Sampo with Väinämöinen overseeing; you build only part 1. rune.py (4,100 lines) keeps every path behind home(p) (line ~28); add the tower switch (set by the genesis verb's --tower flag; name ^[a-z0-9][a-z0-9-]{0,39}$), rune.root(p) for shared stores, and make moonscale's _dir use rune.root(p). Find every place under plugin/lib/sampo that builds a path to research/genesis without home() and decide shared or per-tower (grep 'research", "genesis' and 'genesis/'). The root tower's behaviour and files must not change: the existing genesis tests stay green unchanged. Tests in plugin/tests/test_kalevala.py. Another builder works on moonscale.py (T-3045, T-3047): touch only _dir there.
## Steps
1. [x] rune.home per tower and rune.root for the shared stores (tests first)
2. [x] --tower on every genesis verb, the towers list, name checks (tests first)
## Resume here
<!-- auto -->
- 2026-11-05T00:32:46Z steps 2/2 done
- git: worktree-agent-a8d6e91bb90952d63; 3 uncommitted: plugin/lib/sampo/louhi.py, plugin/lib/sampo/rune.py, plugin/tests/test_kalevala.py
- touched since last checkpoint: .fm-scratch/edits.json, plugin/lib/sampo/moonscale.py, plugin/lib/sampo/steer.py, .fm-scratch/e2.json, plugin/lib/sampo/cli.py, plugin/lib/sampo/rune.py, plugin/lib/sampo/louhi.py, plugin/tests/test_kalevala.py
## Docs impact
CHANGELOG line; genesis --tower and genesis towers in their argparse help
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_kalevala test_genesis test_moons_scale test_steer 2>&1 | tail -15` → exit 0 · Ran 293 tests in 32.0s (46 classes, 16 at a time; slowest: GenesisRead 30s, GenerationReview 29s, GenesisCheck 27s) / OK [ran] [tree 75e396b9b7fe] [world 2f1906870a] (2026-11-05T00:24:26Z)
- (step 1) `python3 plugin/tests/run.py test_kalevala test_genesis` → exit 0 · Ran 221 tests in 41.9s (25 classes, 16 at a time; slowest: GenesisRead 41s, GenerationReview 36s, GenesisCheck 35s) / OK [ran] [tree 75e396b9b7fe] [world 2f1906870a] (2026-11-05T00:25:21Z)
- (step 2) `python3 plugin/tests/run.py test_kalevala test_genesis` → exit 0 · Ran 221 tests in 47.9s (25 classes, 16 at a time; slowest: GenesisRead 47s, GenerationReview 41s, GenesisCheck 38s) / OK [ran] [tree 75e396b9b7fe] [world 2f1906870a] (2026-11-05T00:27:01Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_doctor test_kalevala test_left_out test_mint test_models test_moons_scale test_rename_scan test_small_cards test_steer test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 162 tests across 6 files. [35.94s] [ran] [tree 75e396b9b7fe] [world 2f1906870a] (2026-11-05T00:29:13Z)
- (step 1) `python3 plugin/tests/run.py test_kalevala test_genesis test_louhi` → exit 0 · Ran 246 tests in 46.8s (29 classes, 16 at a time; slowest: GenesisRead 43s, LouhiModels 43s, GenerationReview 39s) / OK [ran] [tree 4a1af9fc7e91] [world 2f1906870a] (2026-11-05T00:34:48Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_core test_docs test_doctor test_exam test_kalevala test_left_out test_louhi_models test_mint test_models test_moons_scale test_rename_scan test_small_cards test_steer test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 162 tests across 6 files. [13.11s] [ran] [tree 4a1af9fc7e91] [world 2f1906870a] (2026-11-05T00:39:01Z)
- (step 2) `python3 plugin/tests/run.py test_kalevala test_genesis` → exit 0 · Ran 228 tests in 28.5s (25 jobs, 16 at a time; slowest: GenesisRead 28s, GenesisCheck 23s, ProofBeforePresentation 23s) / OK [ran] [tree 96592bfa731d] [world 2f1906870a] (2026-11-05T12:40:07Z)
- `python3 plugin/tests/run.py test_kalevala` → ✗ exit 1 · Ran 9 tests in 7.2s (1 jobs, 16 at a time; slowest: Kalevala 4s) / FAILED (1 classes: test_kalevala.Kalevala) (start tree + this task's tests) [ran] [tree 7c22f501de9d] [world 2f1906870a] (2026-11-05T12:40:39Z)
- `python3 plugin/tests/run.py test_kalevala` → exit 0 · Ran 9 tests in 6.3s (1 jobs, 16 at a time; slowest: Kalevala 5s) / OK [ran] [tree 7c22f501de9d] [world 2f1906870a] (2026-11-05T12:40:39Z)
- (ac 1) `python3 plugin/tests/run.py test_kalevala test_genesis` → exit 0 · Ran 228 tests in 31.3s (25 jobs, 16 at a time; slowest: GenesisRead 31s, ProofBeforePresentation 26s, GenesisCheck 26s) / OK [ran] [tree 7c22f501de9d] [world 2f1906870a] (2026-11-05T12:41:18Z)
- (ac 2) `python3 plugin/tests/run.py test_kalevala test_genesis` → exit 0 · Ran 228 tests in 31.3s (25 jobs, 16 at a time; slowest: GenesisRead 31s, ProofBeforePresentation 26s, GenesisCheck 26s) / OK [ran] [tree 7c22f501de9d] [world 2f1906870a] (2026-11-05T12:41:18Z)
- (ac 3) `python3 plugin/tests/run.py test_kalevala test_genesis` → exit 0 · Ran 228 tests in 31.3s (25 jobs, 16 at a time; slowest: GenesisRead 31s, ProofBeforePresentation 26s, GenesisCheck 26s) / OK [ran] [tree 7c22f501de9d] [world 2f1906870a] (2026-11-05T12:41:18Z)
- (audit intent) `re-ran test_kalevala + test_genesis on main after the merge: 228 OK; proved red on the start tree; read rune.py's tower naming and home/root split` → the three criteria hold: every genesis verb takes --tower and works in research/genesis/towers/NAME, the moons store, exam scenarios and steers stay at the root (a tower's steer file adds), and genesis towers lists aspect, generation and verdicts; no --tower is the root tower as before [tree 7c22f501de9d] (2026-11-05T12:41:18Z)
- (audit adversary) `re-ran test_kalevala + test_genesis on main after the merge: 228 OK; proved red on the start tree; read rune.py's tower naming and home/root split` → a tower name becomes a path, so it is refused unless it fullmatches [a-z][a-z0-9-]{0,23}, doesn't end in '-' and isn't 'root' (rune.py:29-33): no '/', '..' or absolute path can reach the filesystem [tree 7c22f501de9d] (2026-11-05T12:41:18Z)
- (audit edge) `re-ran test_kalevala + test_genesis on main after the merge: 228 OK; proved red on the start tree; read rune.py's tower naming and home/root split` → an unknown or bad tower name is refused with a message (tested); the root tower keeps today's paths, so existing generations read unchanged [tree 7c22f501de9d] (2026-11-05T12:41:18Z)
## Log
- 2026-11-05T00:20:51Z created
- 2026-11-05T00:20:52Z set approved=True
- 2026-11-05T00:20:53Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3053.builder.md
- 2026-11-05T00:21:08Z focused
- 2026-11-05T00:21:10Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-05T00:23:12Z set scope=['plugin/lib/sampo/rune.py', 'plugin/lib/sampo/cli.py', 'plugin/lib/sampo/moonscale.py', 'plugin/lib/sampo/steer.py', 'plugin/tests/test_kalevala.py']
- 2026-11-05T00:32:25Z set scope=['plugin/lib/sampo/rune.py', 'plugin/lib/sampo/cli.py', 'plugin/lib/sampo/moonscale.py', 'plugin/lib/sampo/steer.py', 'plugin/lib/sampo/louhi.py', 'plugin/tests/test_kalevala.py', 'MASTER.md']
- 2026-11-05T01:12:24Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a8d6e91bb90952d63 (branch worktree-agent-a8d6e91bb90952d63 kept: not merged)
- 2026-11-05T03:08:30Z blocked: built (cdb03d85, branch kept after a gate hold); last in the merge queue
- 2026-11-05T05:18:28Z lane: ~/.claude/foreman.lanes/T-3053 on foreman/T-3053
- 2026-11-05T12:39:16Z merged worktree-agent-a8d6e91bb90952d63 (7 file(s))
- 2026-11-05T12:39:17Z lane removed: ~/.claude/foreman.lanes/T-3053 (branch foreman/T-3053 kept: not merged)
- 2026-11-05T12:39:34Z focused
- 2026-11-05T12:40:45Z scope: CHANGELOG.md line added at close
- 2026-11-05T12:43:56Z done
- 2026-11-05T12:44:00Z committed 4205131f (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- T-2766 [FEATURE M, done, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as t…
- T-3050 [FEATURE L, planned, 5 steps] Kalevala: many Rune towers at once on every aspect of Sampo, overseen by Väinämöinen, and evolving its own setup
- decision 2026-11-05: Kalevala (T-3050): namespaced Rune towers per aspect run at once, Väinämöinen oversees against the user's intent, Kalevala's own generations evolve …
- similar finished tasks took 3–9 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py, plugin/tests/test_mint.py, plugin/tests/test_moons_scale.py, plugin/tests/test_rename_scan.py, plugin/tests/test_small_cards.py, p…
## Preflight
Changed in scope since this was planned (2026-11-05): MASTER.md, plugin/lib/sampo/cli.py, plugin/lib/sampo/louhi.py, plugin/lib/sampo/moonscale.py, plugin/lib/sampo/rune.py, plugin/lib/sampo/steer.py, plugin/tests/test_kalevala.py; re-ground the plan against them before editing
## Lessons
- A name that becomes a path is validated by a full-match allowlist before any join, never by stripping
## Files touched
- plugin/tests/test_kalevala.py
- plugin/lib/sampo/rune.py
- .fm-scratch/edits.json
- plugin/lib/sampo/moonscale.py
- plugin/lib/sampo/steer.py
- .fm-scratch/e2.json
- plugin/lib/sampo/cli.py
- plugin/lib/sampo/louhi.py
- MASTER.md
- CHANGELOG.md
