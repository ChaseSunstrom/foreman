---
id: T-3045
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/sampo/moonscale.py, plugin/tests/test_moons_scale.py]
depends_on: []
source: user
created: 2026-11-05T00:08:38Z
updated: 2026-11-05T01:58:18Z
builder_model: haiku
inferred_deps: [T-3042]
inferred_why: T-3042: named in its request
base: 53d75b0e4313993d0b6a5566f453fcc1f249f0ec
base_tree: 33bfe050a99ef2541400cb78263714c2440f8e4e
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-05T00:10:06Z
plan0_scope: [plugin/lib/sampo/moonscale.py, plugin/tests/test_moons_scale.py]
lane_stop: merged 2026-11-05T01:53:25Z
verified: strong
unproven: [ui-unshot]
---
# Moons yield: normalise and re-admit, a Sampo grid, kill repair, data-fed prompts (T-3042 part 1)
## Raw request
> Moons yield: normalise and re-admit, a Sampo grid, kill repair, data-fed prompts (T-3042 part 1)
## Interpretation
Reading 1 (taken): raise the share of generated moons that survive, so 10,000 kept is reachable (format misses re-admitted, failed one-day kill tests rewritten once, prompts fed the cell's own reject reasons), and open a Sampo grid so moons can be about Sampo itself. Reading 2 (ruled out): only widen the grid and leave yield alone: at 3% it needs ~350,000 generated moons, the waste the user's ask is about.
## Assumptions (confidence)
## Acceptance criteria
- [x] A with_this missing only 'With this,' is normalised at write, and the old write rejects that now pass are re-admitted by a new write event — verify with `python3 plugin/tests/run.py test_moons_scale`
- [x] Moons on anything related to Sampo: a Sampo grid of its areas (problem solving, memory, efficiency and each coverage.md area), read thinnest first with the user grid; its cells accept Sampo's own parts as the payoff — verify with `python3 plugin/tests/run.py test_moons_scale`
- [x] A kill-rejected moon gets one rewritten kill test as a new row with its parent, judged like any row; each cell's prompt carries its top reject reasons and two kept moons — verify with `python3 plugin/tests/run.py test_moons_scale`
## Non-goals
## Approach (options → choice → why)
1) fix yield at each stage (normalise at write, repair at kill, data-fed prompts): likely outcome: yield from ~3% to 10%+ with the same bars. 2) a second, laxer funnel for repaired rows: fails if: repaired moons skip the bars the rest meet. 3) loosen the kill judge's rule: fails if: tame or untestable moons pass, against the wild steer. 4) use what exists: playbooks small grow's repair pass (761 of 1,804 refused cards repaired) as the repair's pattern; the funnel's stages unchanged: likely outcome: little new machinery. 5) do less: only the write normalise and re-admit: likely outcome: +~1,400 rows to the funnel but the kill stage still drops 58%. Choice 1 (80%): one funnel, same bars, each stage's gain measurable on the live store, built on 4's pattern.
## Risks and rollback
Blast radius (sampo graph blast): co-changes plugin/lib/sampo/cli.py, plugin/lib/sampo/rune.py, MASTER.md, plugin/lib/sampo/night.py, plugin/tests/test_night.py; past FIXes T-2940.
## Execution prompt
The parent's brief holds the live data, the design and the measured numbers: read its Execution prompt first (state/projects/foreman-4a056f/tasks/T-3042-and-with-the-10000-moons-thing-i-want-it-to-lite.md). Stores stay append-only (candidates.jsonl, funnel.jsonl are never rewritten; a fate is a row's last event). Never print LLM_API_KEY (models.secret() reads it). Work test-first in plugin/tests/test_moons_scale.py; run python3 plugin/tests/run.py test_moons_scale before each commit. Part 1 = the parent's items (1) normalise and re-admit, (2) the Sampo grid, (3) kill repair and data-fed prompts. Report: tests added, and a dry count on a copy of the live store of how many old write rejects the re-admit would recover (never write to the live store from a test).
## Steps
1. [x] normalise and re-admit (tests first)
2. [x] the Sampo grid (tests first)
3. [x] kill repair and data-fed prompts (tests first)
## Resume here
<!-- auto -->
- 2026-11-05T01:15:12Z steps 3/3 done
- git: worktree-agent-a7d74509f785ada30; 19 uncommitted: CHANGELOG.md, MASTER.md, mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx, mods/foreman-ui/types/index.d.ts, plugin/lib/sampo/bench.py, plugin/lib/sampo/budget.py, plugin/lib/sampo/cli.py, plugin/lib/sampo/hooks.py, plugin/lib/sampo/models.py
- touched since last checkpoint: CHANGELOG.md, MASTER.md, mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx, mods/foreman-ui/types/index.d.ts, plugin/lib/sampo/bench.py, plugin/lib/sampo/budget.py, plugin/lib/sampo/cli.py, plugin/lib/sampo/hooks.py, plugin/lib/sampo/models.py, plugin/lib/sampo/moonscale.py, plugin/lib/sampo/night.py, plugin/lib/sampo/rune.py, plugin/lib/sampo/watch.py, plugin/lib/ui-demo.json
## Docs impact
CHANGELOG line
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_moons_scale 2>&1 | tail -40` → ✗ exit 1 · Ran 57 tests in 11.0s (13 classes, 16 at a time; slowest: StoreLock 9s, Funnel 7s, Yield 6s) / FAILED (1 classes: test_moons_scale.Funnel) [ran] [tree 6734cbaee6ed] [world 2f1906870a] (2026-11-05T00:15:29Z)
- (ac 2) `python3 plugin/tests/run.py test_moons_scale 2>&1 | tail -40` → ✗ exit 1 · Ran 57 tests in 11.0s (13 classes, 16 at a time; slowest: StoreLock 9s, Funnel 7s, Yield 6s) / FAILED (1 classes: test_moons_scale.Funnel) [ran] [tree 6734cbaee6ed] [world 2f1906870a] (2026-11-05T00:15:29Z)
- (ac 3) `python3 plugin/tests/run.py test_moons_scale 2>&1 | tail -40` → ✗ exit 1 · Ran 57 tests in 11.0s (13 classes, 16 at a time; slowest: StoreLock 9s, Funnel 7s, Yield 6s) / FAILED (1 classes: test_moons_scale.Funnel) [ran] [tree 6734cbaee6ed] [world 2f1906870a] (2026-11-05T00:15:29Z)
- (ac 1) `python3 plugin/tests/run.py test_moons_scale 2>&1 | grep -B3 -A12 "^FAIL\|^ERROR" | head -60` → ✗ exit 1 · Ran 57 tests in 18.7s (13 classes, 16 at a time; slowest: StoreLock 16s, Funnel 10s, Yield 10s) / FAILED (1 classes: test_moons_scale.Funnel) [ran] [tree 01249aa5ba31] [world 2f1906870a] (2026-11-05T00:16:20Z)
- (ac 2) `python3 plugin/tests/run.py test_moons_scale 2>&1 | grep -B3 -A12 "^FAIL\|^ERROR" | head -60` → ✗ exit 1 · Ran 57 tests in 18.7s (13 classes, 16 at a time; slowest: StoreLock 16s, Funnel 10s, Yield 10s) / FAILED (1 classes: test_moons_scale.Funnel) [ran] [tree 01249aa5ba31] [world 2f1906870a] (2026-11-05T00:16:20Z)
- (ac 3) `python3 plugin/tests/run.py test_moons_scale 2>&1 | grep -B3 -A12 "^FAIL\|^ERROR" | head -60` → ✗ exit 1 · Ran 57 tests in 18.7s (13 classes, 16 at a time; slowest: StoreLock 16s, Funnel 10s, Yield 10s) / FAILED (1 classes: test_moons_scale.Funnel) [ran] [tree 01249aa5ba31] [world 2f1906870a] (2026-11-05T00:16:20Z)
- (ac 1) `python3 plugin/tests/run.py test_moons_scale 2>&1 | grep -A14 "^FAIL"` → ✗ exit 1 · Ran 57 tests in 5.9s (13 classes, 16 at a time; slowest: StoreLock 6s, Funnel 3s, Yield 2s) / FAILED (1 classes: test_moons_scale.Funnel) [ran] [tree b67a51f60276] [world 2f1906870a] (2026-11-05T00:18:40Z)
- (ac 2) `python3 plugin/tests/run.py test_moons_scale 2>&1 | grep -A14 "^FAIL"` → ✗ exit 1 · Ran 57 tests in 5.9s (13 classes, 16 at a time; slowest: StoreLock 6s, Funnel 3s, Yield 2s) / FAILED (1 classes: test_moons_scale.Funnel) [ran] [tree b67a51f60276] [world 2f1906870a] (2026-11-05T00:18:40Z)
- (ac 3) `python3 plugin/tests/run.py test_moons_scale 2>&1 | grep -A14 "^FAIL"` → ✗ exit 1 · Ran 57 tests in 5.9s (13 classes, 16 at a time; slowest: StoreLock 6s, Funnel 3s, Yield 2s) / FAILED (1 classes: test_moons_scale.Funnel) [ran] [tree b67a51f60276] [world 2f1906870a] (2026-11-05T00:18:40Z)
- (ac 1) `python3 plugin/tests/run.py test_moons_scale 2>&1 | grep -A12 "^FAIL"` → ✗ exit 1 · Ran 57 tests in 6.7s (13 classes, 16 at a time; slowest: StoreLock 6s, Funnel 4s, Yield 3s) / FAILED (1 classes: test_moons_scale.Funnel) [ran] [tree 69d862cda23e] [world 2f1906870a] (2026-11-05T00:18:57Z)
- (ac 2) `python3 plugin/tests/run.py test_moons_scale 2>&1 | grep -A12 "^FAIL"` → ✗ exit 1 · Ran 57 tests in 6.7s (13 classes, 16 at a time; slowest: StoreLock 6s, Funnel 4s, Yield 3s) / FAILED (1 classes: test_moons_scale.Funnel) [ran] [tree 69d862cda23e] [world 2f1906870a] (2026-11-05T00:18:57Z)
- (ac 3) `python3 plugin/tests/run.py test_moons_scale 2>&1 | grep -A12 "^FAIL"` → ✗ exit 1 · Ran 57 tests in 6.7s (13 classes, 16 at a time; slowest: StoreLock 6s, Funnel 4s, Yield 3s) / FAILED (1 classes: test_moons_scale.Funnel) [ran] [tree 69d862cda23e] [world 2f1906870a] (2026-11-05T00:18:57Z)
- (step 1) `python3 plugin/tests/run.py test_moons_scale` → ✗ exit 1 · Ran 57 tests in 5.9s (13 classes, 16 at a time; slowest: StoreLock 6s, Funnel 4s, Yield 2s) / FAILED (1 classes: test_moons_scale.Funnel) [ran] [tree cb7b370250e7] [world 2f1906870a] (2026-11-05T00:19:08Z)
- (step 2) `python3 plugin/tests/run.py test_moons_scale` → ✗ exit 1 · Ran 57 tests in 8.0s (13 classes, 16 at a time; slowest: StoreLock 8s, Funnel 4s, Yield 3s) / FAILED (1 classes: test_moons_scale.Funnel) [ran] [tree cb7b370250e7] [world 2f1906870a] (2026-11-05T00:19:17Z)
- (step 3) `python3 plugin/tests/run.py test_moons_scale` → ✗ exit 1 · Ran 57 tests in 8.4s (13 classes, 16 at a time; slowest: StoreLock 8s, Funnel 5s, Yield 4s) / FAILED (1 classes: test_moons_scale.Funnel) [ran] [tree cb7b370250e7] [world 2f1906870a] (2026-11-05T00:19:26Z)
- (ac 1) `python3 plugin/tests/run.py test_moons_scale 2>&1 | grep -A14 "^FAIL"` → ✗ exit 1 · Ran 57 tests in 7.2s (13 classes, 16 at a time; slowest: StoreLock 7s, Funnel 5s, Yield 4s) / FAILED (1 classes: test_moons_scale.Funnel) [ran] [tree cb7b370250e7] [world 2f1906870a] (2026-11-05T00:19:26Z)
- (ac 2) `python3 plugin/tests/run.py test_moons_scale 2>&1 | grep -A14 "^FAIL"` → ✗ exit 1 · Ran 57 tests in 7.2s (13 classes, 16 at a time; slowest: StoreLock 7s, Funnel 5s, Yield 4s) / FAILED (1 classes: test_moons_scale.Funnel) [ran] [tree cb7b370250e7] [world 2f1906870a] (2026-11-05T00:19:26Z)
- (ac 3) `python3 plugin/tests/run.py test_moons_scale 2>&1 | grep -A14 "^FAIL"` → ✗ exit 1 · Ran 57 tests in 7.2s (13 classes, 16 at a time; slowest: StoreLock 7s, Funnel 5s, Yield 4s) / FAILED (1 classes: test_moons_scale.Funnel) [ran] [tree cb7b370250e7] [world 2f1906870a] (2026-11-05T00:19:26Z)
- (ac 1) `python3 plugin/tests/run.py test_moons_scale 2>&1 | tail -4` → exit 0 · Ran 57 tests in 5.9s (13 classes, 16 at a time; slowest: StoreLock 5s, Funnel 4s, Yield 3s) / OK [ran] [tree 5530128c33de] [world 2f1906870a] (2026-11-05T00:19:37Z)
- (ac 2) `python3 plugin/tests/run.py test_moons_scale 2>&1 | tail -4` → exit 0 · Ran 57 tests in 5.9s (13 classes, 16 at a time; slowest: StoreLock 5s, Funnel 4s, Yield 3s) / OK [ran] [tree 5530128c33de] [world 2f1906870a] (2026-11-05T00:19:37Z)
- (ac 3) `python3 plugin/tests/run.py test_moons_scale 2>&1 | tail -4` → exit 0 · Ran 57 tests in 5.9s (13 classes, 16 at a time; slowest: StoreLock 5s, Funnel 4s, Yield 3s) / OK [ran] [tree 5530128c33de] [world 2f1906870a] (2026-11-05T00:19:37Z)
- (step 1) `python3 plugin/tests/run.py test_moons_scale` → exit 0 · Ran 57 tests in 8.2s (13 classes, 16 at a time; slowest: StoreLock 8s, Funnel 4s, Yield 3s) / OK [ran] [tree 5530128c33de] [world 2f1906870a] (2026-11-05T00:19:57Z)
- (step 2) `python3 plugin/tests/run.py test_moons_scale` → exit 0 · Ran 57 tests in 11.0s (13 classes, 16 at a time; slowest: StoreLock 11s, Funnel 4s, Yield 3s) / OK [ran] [tree 5530128c33de] [world 2f1906870a] (2026-11-05T00:20:09Z)
- (step 3) `python3 plugin/tests/run.py test_moons_scale` → exit 0 · Ran 57 tests in 9.3s (13 classes, 16 at a time; slowest: StoreLock 9s, Funnel 3s, Yield 2s) / OK [ran] [tree 5530128c33de] [world 2f1906870a] (2026-11-05T00:20:19Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_doctor test_left_out test_models test_moons_scale test_rename_scan test_small_cards && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 162 tests across 6 files. [12.10s] [ran] [tree 5530128c33de] [world 2f1906870a] (2026-11-05T00:20:42Z)
- `python3 plugin/tests/run.py test_moons_scale.Yield` → ✗ exit 1 · Ran 16 tests in 3.2s (1 classes, 16 at a time; slowest: Yield 2s) / FAILED (1 classes: test_moons_scale.Yield) (start tree + this task's tests) [ran] [tree 65965b24d9e9] [world 2f1906870a] (2026-11-05T01:56:30Z)
- `python3 plugin/tests/run.py test_moons_scale.Yield` → exit 0 · Ran 16 tests in 3.1s (1 classes, 16 at a time; slowest: Yield 3s) / OK [ran] [tree 65965b24d9e9] [world 2f1906870a] (2026-11-05T01:56:30Z)
- (step 1) `python3 plugin/tests/run.py test_moons_scale test_night test_louhi` → exit 0 · Ran 144 tests in 20.2s (34 classes, 16 at a time; slowest: LouhiModels 19s, Night 16s, Yield 8s) / OK [ran] [tree 106df4e763e5] [world 2f1906870a] (2026-11-05T01:56:58Z)
- (step 2) `python3 plugin/tests/run.py test_moons_scale test_night test_louhi` → exit 0 · Ran 144 tests in 17.8s (34 classes, 16 at a time; slowest: LouhiModels 17s, Night 14s, Yield 7s) / OK [ran] [tree 106df4e763e5] [world 2f1906870a] (2026-11-05T01:57:17Z)
- (step 3) `python3 plugin/tests/run.py test_moons_scale test_night test_louhi` → exit 0 · Ran 144 tests in 17.1s (34 classes, 16 at a time; slowest: LouhiModels 17s, Night 14s, Yield 7s) / OK [ran] [tree 106df4e763e5] [world 2f1906870a] (2026-11-05T01:57:35Z)
- (ac 1) `python3 plugin/tests/run.py test_moons_scale` → exit 0 · Ran 76 tests in 4.1s (15 classes, 16 at a time; slowest: Yield 4s, Funnel 3s, KeepGrow 3s) / OK [ran] [tree 106df4e763e5] [world 2f1906870a] (2026-11-05T01:57:50Z)
- (ac 2) `python3 plugin/tests/run.py test_moons_scale` → exit 0 · Ran 76 tests in 4.1s (15 classes, 16 at a time; slowest: Yield 4s, Funnel 3s, KeepGrow 3s) / OK [ran] [tree 106df4e763e5] [world 2f1906870a] (2026-11-05T01:57:50Z)
- (ac 3) `python3 plugin/tests/run.py test_moons_scale` → exit 0 · Ran 76 tests in 4.1s (15 classes, 16 at a time; slowest: Yield 4s, Funnel 3s, KeepGrow 3s) / OK [ran] [tree 106df4e763e5] [world 2f1906870a] (2026-11-05T01:57:50Z)
- (audit intent) `one fm-reviewer (intent, adversary, edge, operator, maintainer): 1 HIGH (add() copied parent and repair from the model's own reply: a list parent crashed the nightly funnel, a real id skipped the dedupe), 2 MEDIUM ('With this, you get' admitted against the user's line; repair spent the night's cap before tier and novelty) and 6 LOW; all fixed test-first; the merge with T-3046 resolved by the builder (both test sets kept; one test pinned to user cells since Sampo cells accept internal payoffs); red→green proved on the Yield class` → the 300 goes up by yield: 847 of 1,614 old write rejects re-admitted (dry count on the live store), one rewritten kill test per kill-rejected moon, prompts fed each kind's reject themes and kept anchors; moons on anything related to Sampo: a Sampo grid of coverage areas plus problem solving, memory and efficiency [tree 106df4e763e5] (2026-11-05T01:57:50Z)
- (audit adversary) `one fm-reviewer (intent, adversary, edge, operator, maintainer): 1 HIGH (add() copied parent and repair from the model's own reply: a list parent crashed the nightly funnel, a real id skipped the dedupe), 2 MEDIUM ('With this, you get' admitted against the user's line; repair spent the night's cap before tier and novelty) and 6 LOW; all fixed test-first; the merge with T-3046 resolved by the builder (both test sets kept; one test pinned to user cells since Sampo cells accept internal payoffs); red→green proved on the Yield class` → parent and repair come only from _repair's own argument, never the model's object (a list or a real id in a reply stores no link, pinned); repair text is data, escaped by _safe in later prompts [tree 106df4e763e5] (2026-11-05T01:57:50Z)
- (audit edge) `one fm-reviewer (intent, adversary, edge, operator, maintainer): 1 HIGH (add() copied parent and repair from the model's own reply: a list parent crashed the nightly funnel, a real id skipped the dedupe), 2 MEDIUM ('With this, you get' admitted against the user's line; repair spent the night's cap before tier and novelty) and 6 LOW; all fixed test-first; the merge with T-3046 resolved by the builder (both test sets kept; one test pinned to user cells since Sampo cells accept internal payoffs); red→green proved on the Yield class` → a repair row is never repaired again and a parent at most once; 'none' answers marked so reruns don't re-ask; a one-stage run doesn't repair; louhi's generation benchmark doesn't repair [tree 106df4e763e5] (2026-11-05T01:57:50Z)
- (audit operator) `one fm-reviewer (intent, adversary, edge, operator, maintainer): 1 HIGH (add() copied parent and repair from the model's own reply: a list parent crashed the nightly funnel, a real id skipped the dedupe), 2 MEDIUM ('With this, you get' admitted against the user's line; repair spent the night's cap before tier and novelty) and 6 LOW; all fixed test-first; the merge with T-3046 resolved by the builder (both test sets kept; one test pinned to user cells since Sampo cells accept internal payoffs); red→green proved on the Yield class` → repair runs after novelty on the calls the cap leaves, so a backlog can't starve tier and novelty; coverage shows the Sampo grid's size and thinnest cells [tree 106df4e763e5] (2026-11-05T01:57:50Z)
## Log
- 2026-11-05T00:08:38Z created
- 2026-11-05T00:09:19Z set approved=True
- 2026-11-05T00:09:43Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3045.builder.md
- 2026-11-05T00:10:04Z focused
- 2026-11-05T00:10:06Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-05T01:53:25Z merged worktree-agent-a7d74509f785ada30 (2 file(s))
- 2026-11-05T01:53:26Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a7d74509f785ada30
- 2026-11-05T01:56:21Z focused
- 2026-11-05T01:56:37Z scope: CHANGELOG.md (the task's line); louhi.py untouched (the review's item 7 was met by passing stage= in _gen_funnel's existing calls)
- 2026-11-05T01:58:15Z done
- 2026-11-05T01:58:18Z committed b3ac10ff (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2865 [FEATURE L, done, 5 steps] Moons at scale: grow the Moons catalogue to 10,000 candidate moons about what Sampo can do for its user, by grid, through a cheap-first…
- decision 2026-11-05: T-3042 plan: raise the funnel's yield (normalise, re-admit, kill repair, data-fed prompts), add a Sampo grid, count kept moons, export all
- T-3042 [FEATURE L, planned, 4 steps] 10,000 moons kept and used, and moons on anything related to Sampo
- T-3046 [FEATURE M, planned, 3 steps] Count kept moons: grow --keep with funnel rounds, the night counts survivors, families from stored links (T-3042 part 2)
- similar past tasks were L: consider --tier L
- the similar finished task took 5 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_moons_scale.py, plugin/tests/test_small_cards.py
## Preflight
Changed in scope since this was planned (2026-11-05): plugin/lib/sampo/moonscale.py, plugin/tests/test_moons_scale.py; re-ground the plan against them before editing
## Lessons
- Fields that steer the pipeline (a parent link, a repair flag) must come from Sampo's own call, never from a model's reply, even when the reply is ours
## Plan gaps
- failed first: step 1 normalise and re-admit (tests first)
- failed first: step 2 the Sampo grid (tests first)
- failed first: step 3 kill repair and data-fed prompts (tests first)
## Files touched
- plugin/tests/test_moons_scale.py
- plugin/lib/sampo/moonscale.py
- .fm-scratch/dry.py
- CHANGELOG.md
- MASTER.md
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/types/index.d.ts
- plugin/lib/sampo/bench.py
- plugin/lib/sampo/budget.py
- plugin/lib/sampo/cli.py
- plugin/lib/sampo/hooks.py
- plugin/lib/sampo/models.py
- plugin/lib/sampo/night.py
- plugin/lib/sampo/rune.py
- plugin/lib/sampo/watch.py
- plugin/lib/ui-demo.json
- plugin/tests/test_budget.py
- plugin/tests/test_models.py
- plugin/tests/test_night.py
