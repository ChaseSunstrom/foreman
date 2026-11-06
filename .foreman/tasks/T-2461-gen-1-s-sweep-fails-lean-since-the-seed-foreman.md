---
id: T-2461
type: CLEAN
tier: L
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-01T08:33:55Z
updated: 2026-11-01T09:16:41Z
rival_at: 2026-11-01T08:36:40Z
rival_split: true
base: 8048b07b026ba9cfc37bbb1e98990e4b0a52a7df
base_tree: 89312189884e29652362801e1d93569eb90419eb
plan0_at: 2026-11-01T08:37:09Z
plan0_scope: []
verified: strong
---
# Lean: fold six verbs into the verbs that already hold their job (proof → prove --rollup, triggers → outcomes --triggers, calibration → outcomes --judgment, incident → capture --incident, sweep → projects --sweep, instruments → which --instruments), so gen-1's sweep lean line passes
## Raw request
> CLEAN: gen-1's sweep fails lean: since the seed Foreman added 6 verbs (calibration, goal, incident, proof, prove, triggers) and 228 description characters with nothing removed (gen-0 §6: subtract as you add). Fold verbs whose job another verb already holds (proof into prove, calibration and triggers into outcomes, or the reverse) and trim descriptions until fm genesis sweep 1's lean line passes; keep every behaviour and its tests
## Interpretation
Readings: (a) the lean line must pass by removing verbs net, behaviour kept; (b) only new verbs may be folded. (a), choosing new or unused verbs so no user integration (a status bar's fm glance, a hook's fm canary) breaks. Outcome: the sweep's lean line passes; the coverage line stays for gen 2's Seed.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm genesis sweep 1's lean line passes on verbs (net at or under the seed's count) with every folded behaviour reachable under its new home and its tests green — verify with `python3 plugin/tests/run.py test_genesis`
- [x] every reference (MCP tools, AGENTS lines, fm code, hooks, site, skills, docs) names the new home; no doc or hint names a removed verb — verify with `python3 plugin/tests/run.py test_docs`
## Non-goals
## Approach (options → choice → why)
1) Fold six verbs whose job a related verb already names, as flags or subcommands, keeping each behaviour and its tests: chosen for the six with no outside callers (new in gen 1, or used 0-2 times in 83k recorded uses); fails if: a hidden caller (a hook or script) still runs a removed verb, which a repo-wide grep and the suite catch 2) use what exists: keep the verbs and raise the sweep's verb baseline; fails if: it weakens Foreman's own lean rule, the opposite of gen-0 §6 3) do less: trim descriptions only; fails if: verbs stay +6 and the line still fails 4) aliases kept beside the new homes; fails if: an alias is still an add() line, so the count doesn't move Choice 1 (75%): six folds, one commit per pair, the suite after each
## Risks and rollback
What fails: a hook, skill or the MCP server still runs a removed verb (caught by git grep and the suite); a user's muscle memory types an old verb (fm's unknown-verb help names the near one). Undo: each fold is its own commit; git revert restores the verb, its parser and its references.
## Execution prompt
## Steps
1. [x] pin each folded verb's behaviour with a test under its new home (red)
2. [x] fold proof and calibration and triggers
3. [x] fold incident, sweep and instruments
4. [x] every reference moved; docs; fm genesis sweep 1 lean line
5. [x] trim skill descriptions (228+ chars) and the rules (4+ chars) to the seed's footprint
## Resume here
<!-- auto -->
- 2026-11-01T08:39:06Z step 3/5: fold incident, sweep and instruments
- git: foreman/build; 13 uncommitted: CHANGELOG.md, MASTER.md, README.md, plugin/lib/fmagents.py, plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmmcp.py, plugin/lib/fmprove.py, plugin/tests/test_agents.py, plugin/tests/test_proof.py
- touched since last checkpoint: /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/fold_proof.py, CHANGELOG.md, MASTER.md, README.md, plugin/lib/fmagents.py, plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmmcp.py, plugin/lib/fmprove.py, plugin/tests/test_agents.py, plugin/tests/test_proof.py, plugin/tests/test_site.py, site/pages.py, site/stats.py
## Docs impact
CHANGELOG Unreleased entry; MASTER, README, the intake and debug-test skills, the ops incident playbook and the AGENTS plan line name the new homes; unreleased CHANGELOG lines moved, released ones keep their shipped names
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_proof` → ✗ exit 1 · Ran 38 tests in 14.1s (8 classes, 16 at a time; slowest: Proof 14s, Stop 2s, Meaning 1s) / FAILED (2 classes: test_proof.Proof, test_proof.Meaning) [ran] [tree c78c74be7474] (2026-11-01T08:38:03Z)
- (step 2) `python3 plugin/tests/run.py test_proof test_agents test_site test_mcp test_docs test_cli` → exit 0 · Ran 366 tests in 22.2s (112 classes, 16 at a time; slowest: TaskLifecycle 22s, Proof 21s, Fences 9s) / OK [ran] [tree 2aa7add990dd] (2026-11-01T08:38:47Z)
- (step 1) `python3 plugin/tests/run.py test_outcomes test_incident test_ecosystem test_instruments test_suspects` → ✗ exit 1 · Ran 110 tests in 13.9s (33 classes, 16 at a time; slowest: Survival 14s, CalibrationLedgerBets 9s, ModelRouter 8s) / FAILED (8 classes: test_outcomes.CalibrationLedgerBets, test_outcomes.CalibrationBa [ran] [tree 2f8a9ab96d4b] (2026-11-01T08:44:29Z)
- (step 3) `python3 plugin/tests/run.py test_outcomes test_ecosystem test_instruments test_suspects test_incident.Incident test_incident.IncidentSentinel` → ✗ exit 1 · Ran 110 tests in 13.7s (33 classes, 16 at a time; slowest: Survival 13s, CalibrationLedgerBets 8s, ModelRouter 8s) / FAILED (1 classes: test_incident.IncidentSkill) [ran] [tree d9e34d695f22] (2026-11-01T08:46:25Z)
- (step 3) `python3 plugin/tests/run.py test_outcomes test_ecosystem test_instruments test_suspects test_incident test_docs test_site test_agents test_mcp test_cli test_ui_signals test_proof` → ✗ exit 1 · Ran 486 tests in 24.2s (151 classes, 16 at a time; slowest: TaskLifecycle 24s, Proof 23s, Survival 18s) / FAILED (2 classes: test_agents.Judgment, test_docs.Judgment) [ran] [tree 59f3046048df] (2026-11-01T08:47:26Z)
- (step 3) `python3 plugin/tests/run.py test_outcomes test_ecosystem test_instruments test_suspects test_incident test_docs test_site test_agents test_mcp test_cli test_ui_signals test_proof` → exit 0 · Ran 486 tests in 46.7s (151 classes, 16 at a time; slowest: Proof 46s, TaskLifecycle 46s, Survival 39s) / OK [ran] [tree 7c7126c10717] (2026-11-01T08:48:43Z)
- (step 4) `python3 plugin/tests/run.py test_docs test_genesis test_agents test_doctor test_which test_scaffold` → ✗ exit 1 · Ran 449 tests in 24.7s (91 classes, 16 at a time; slowest: GenesisRead 24s, GenesisCheck 20s, GenesisSweep 19s) / FAILED (1 classes: test_docs.PluginFiles) [ran] [tree e93752b773bb] (2026-11-01T08:50:59Z)
- (step 4) `python3 plugin/tests/run.py test_docs test_genesis test_agents test_doctor test_which test_scaffold test_gate_friction` → exit 0 · Ran 460 tests in 25.6s (93 classes, 16 at a time; slowest: GenesisRead 25s, GenesisCheck 21s, GenesisLive 18s) / OK [ran] [tree 1fdc556cffb9] (2026-11-01T08:56:37Z)
- (step 5) `fm genesis sweep 1 | grep '✓ lean'` → exit 0 · ✓ lean: rules chars 6395 -> 6391 (-4); descriptions chars 4237 -> 4236 (-1); largest SKILL chars 9742 -> 9269 (-473); removed: instruments, suspects, sweep; added: goal, prove, triggers; hook p95 not [ran] [tree 1fdc556cffb9] (2026-11-01T09:01:37Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 177 tests in 9.5s (18 classes, 16 at a time; slowest: GenesisRead 9s, GenesisSweep 8s, GenesisCheck 7s) / OK [ran] [tree 1fdc556cffb9] (2026-11-01T09:01:47Z)
- (ac 2) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 103 tests in 8.3s (24 classes, 16 at a time; slowest: Fences 8s, DocsProof 2s, TaskLifecycle 1s) / OK [ran] [tree 1fdc556cffb9] (2026-11-01T09:01:55Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 177 tests in 9.4s (18 classes, 16 at a time; slowest: GenesisRead 9s, GenesisSweep 8s, GenesisCheck 7s) / OK [ran] [tree 1fdc556cffb9] (2026-11-01T09:07:59Z)
- (ac 2) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 103 tests in 8.3s (24 classes, 16 at a time; slowest: Fences 8s, DocsProof 2s, TaskLifecycle 1s) / OK [ran] [tree 1fdc556cffb9] (2026-11-01T09:07:59Z)
- (step 1) `python3 plugin/tests/run.py test_outcomes test_incident test_ecosystem test_instruments test_suspects` → exit 0 · Ran 110 tests in 13.8s (33 classes, 16 at a time; slowest: Survival 13s, CalibrationLedgerBets 9s, ModelRouter 8s) / OK [ran] [tree 1fdc556cffb9] (2026-11-01T09:07:59Z)
- (audit intent) `main-thread lens pass over the whole diff (economy mode: one pass); git grep for every folded verb outside CHANGELOG's released sections, research and the seed: none left; the lean line rerun green` → six verbs folded with behaviour kept under the new homes (each old test now drives the new form); gen 1's lean line passes: verbs 165 -> 165, rules -4, descriptions -1; triggers kept (fmguard keys fm triggers set, T-2355) and burden kept (SEED_PROMPT names it), suspects folded instead [tree 1fdc556cffb9] (2026-11-01T09:07:59Z)
- (audit adversary) `main-thread lens pass over the whole diff (economy mode: one pass); git grep for every folded verb outside CHANGELOG's released sections, research and the seed: none left; the lean line rerun green` → no guard edit; old names are a did-you-mean hint, never an alias, so a user-only word (prove --yes-run, triggers set) can't ride a rewritten argv past fmguard's per-verb table; capture --incident still runs the signal through fmincident's guarded, credential-stripped path [tree 1fdc556cffb9] (2026-11-01T09:07:59Z)
- (audit edge) `main-thread lens pass over the whole diff (economy mode: one pass); git grep for every folded verb outside CHANGELOG's released sections, research and the seed: none left; the lean line rerun green` → whyred with neither CMD nor --suspects is a usage error; which with no words keeps its usage error; --incident needs words (argparse); --suspects with no FILE reads stdin (const empty); outcomes --judgment returns before outcomes' own reads [tree 1fdc556cffb9] (2026-11-01T09:07:59Z)
- (audit operator) `main-thread lens pass over the whole diff (economy mode: one pass); git grep for every folded verb outside CHANGELOG's released sections, research and the seed: none left; the lean line rerun green` → each old name exits 2 naming its new home and runs nothing (test_gate_friction); MCP tool names (calibration, proof) unchanged, their argv moved; site stats call the new forms [tree 1fdc556cffb9] (2026-11-01T09:07:59Z)
- (audit maintainer) `main-thread lens pass over the whole diff (economy mode: one pass); git grep for every folded verb outside CHANGELOG's released sections, research and the seed: none left; the lean line rerun green` → each home dispatches at its handler's top to the unchanged old function; one FOLDED table beside ALIASES says why it isn't an alias; eval cases resynced with the rules (sync_evals.py) [tree 1fdc556cffb9] (2026-11-01T09:07:59Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm ask: text in a file; a run of a documented command proves it (--yes-run) / · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a f [ran] [tree 1fdc556cffb9] (2026-11-01T09:10:35Z)
## Log
- 2026-11-01T08:33:55Z created
- 2026-11-01T08:36:16Z planned from capture
- 2026-11-01T08:37:02Z set approved=True
- 2026-11-01T08:37:08Z focused
- 2026-11-01T08:44:04Z focused
- 2026-11-01T08:44:04Z steer(self): triggers stays (fmguard's user-only table keys fm triggers set, T-2355: moving it means a guard edit); suspects (0 uses in 66k) folds into whyred --suspects instead. burden stays: SEED_PROMPT names fm burden --by-verb
- 2026-11-01T08:56:49Z scope: the folds touch every file naming a folded verb (fmcli parsers and FOLDED hint, the five home handlers, fmincident/fmdebug/fmeco/fminstr/fmcore/fmfriction/fmagents/fmmcp strings, site, MASTER/README/unreleased CHANGELOG, skills and the ops playbook, their tests), the ten longest skill/agent descriptions, one rules phrase and the eval cases that embed the rules (sync_evals.py)
- 2026-11-01T09:10:07Z done
- 2026-11-01T09:10:10Z committed 60f0bc69 (49 files)
- 2026-11-01T09:10:39Z guard authorization added: publish
- 2026-11-01T09:16:41Z publish grant used by fm ship
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Likeliest: consolidate verbs and trim text.** Merge the six new verbs (calibration, goal, incident, proof, prove, triggers) into existing ones, e.g. proof→prove and calibration/triggers→outcomes, in `plugin/lib/fmcli.py` (the verb table and dispatch). Then cut description characters until the lea…
- **Net-count reading.** The lean check may be a net comparison against the seed (verbs added minus removed, description chars added minus removed). Then removing or trimming any pre-existing verb or description also counts, not only the six new ones. The fix can come from places the six don't touch.
- **Reverse direction.** Fold outcomes into calibration/triggers, or prove into proof. This is what "or the reverse" allows, and it only matters if the lean line counts verbs by surviving name.
- **Narrow reading.** Only trim descriptions (228 chars) and leave the verb count. This is unlikely, since the request names verbs to fold and the sweep complains about both.
Approaches:
- **Fold with deprecation aliases.** Make `proof` a thin alias for `prove` (or `prove --show`), and `calibration` and `triggers` into `outcomes` subcommands. Update the argparse registration and help in `plugin/lib/fmcli.py`. Move handler code into the surviving modules, leaving the old names routing…
- **Read the sweep first.** Find where `fm genesis sweep` computes the lean line (likely under `plugin/lib/` or the genesis code behind `site/genesis/index.html`). Learn how it counts verbs (registered names vs. documented ones) and description characters (`plugin/skills/*/SKILL.md` frontmatter vs. c…
- **Trim descriptions by measured budget.** Shorten the descriptions of the new verbs and the skills touched by the folds. Take the 228 characters from there, cutting duplicated trigger phrases and keeping the `cc-skill-descriptions` card's constraints. Re-run `fm genesis sweep 1` until the line pass…
- **Fold at the skill layer only.** If verbs are counted from `plugin/skills/` directories, merge the skill docs (proof into prove) and leave the CLI handlers alone. This is cheaper but risks a mismatch with `fm doctor`.
Failure modes:
- **Test and doc references break.** Existing tests, e.g. `plugin/tests/test_guard.py` and the per-verb tests, call `fm proof` / `fm triggers` by name. If the alias is not exact (flags, exit codes, output), tests fail. `CHANGELOG.md`, `README.md` and `MASTER.md` may also list the removed verbs, and `…
- **Lean line still fails.** If the sweep counts something other than what was folded (for example, it counts aliases as verbs, or counts description characters across `SKILL.md` files), the fold passes the tests but the lean check stays red. This is why the sweep's counting has to be read before edi…
- **Trimmed descriptions lose routing.** Skill and command descriptions drive when they trigger. Cutting trigger words can silently break routing in `plugin/evals/` and the `fm replay` gate, even while unit tests pass.
- **Hooks and performance regress.** `plugin/lib/fmhooks.py` or `plugin/lib/fmguard.py` may reference the old verb names. Folding can break the hook paths or raise latency, which `plugin/tests/bench_hooks.py --runs 20` and the roundtrip e2e would show.
## Dissent
- [x] rival reading: **Likeliest: consolidate verbs and trim text.** Merge the six new verbs (calibration, goal, incident, proof, prove, triggers) into existing ones, e.g. proof→prove and calibration/triggers→outcomes, in `plugin/lib/fmcli.py` (the verb table and dispatch). Then cut description characters until the lea… — answered: adopted: consolidate verbs and trim text
- [x] rival reading: **Net-count reading.** The lean check may be a net comparison against the seed (verbs added minus removed, description chars added minus removed). Then removing or trimming any pre-existing verb or description also counts, not only the six new ones. The fix can come from places the six don't touch. — answered: adopted: the line is net (fmselfgate._verbs counts fmcli's add() lines against the seed's), so any folded verb counts; the six chosen are new or unused
- [x] rival reading: **Reverse direction.** Fold outcomes into calibration/triggers, or prove into proof. This is what "or the reverse" allows, and it only matters if the lean line counts verbs by surviving name. — answered: rejected: the home is the broader, older verb (prove, outcomes, capture, projects, which); direction doesn't change the count
- [x] rival reading: **Narrow reading.** Only trim descriptions (228 chars) and leave the verb count. This is unlikely, since the request names verbs to fold and the sweep complains about both. — answered: rejected: trimming alone leaves verbs at +6
- [x] rival approach: **Fold with deprecation aliases.** Make `proof` a thin alias for `prove` (or `prove --show`), and `calibration` and `triggers` into `outcomes` subcommands. Update the argparse registration and help in `plugin/lib/fmcli.py`. Move handler code into the surviving modules, leaving the old names routing… — answered: rejected: an alias is still an add() line, so the count wouldn't move
- [x] rival approach: **Read the sweep first.** Find where `fm genesis sweep` computes the lean line (likely under `plugin/lib/` or the genesis code behind `site/genesis/index.html`). Learn how it counts verbs (registered names vs. documented ones) and description characters (`plugin/skills/*/SKILL.md` frontmatter vs. c… — answered: adopted: read already: fmselfgate._verbs and fmgenesis._lean_row count add() lines, rules chars and skill description chars from the seed's commit
- [x] rival approach: **Trim descriptions by measured budget.** Shorten the descriptions of the new verbs and the skills touched by the folds. Take the 228 characters from there, cutting duplicated trigger phrases and keeping the `cc-skill-descriptions` card's constraints. Re-run `fm genesis sweep 1` until the line pass… — answered: adopted: a step trims skill descriptions by 228+ characters and the rules by 4+, measured by the sweep
- [x] rival approach: **Fold at the skill layer only.** If verbs are counted from `plugin/skills/` directories, merge the skill docs (proof into prove) and leave the CLI handlers alone. This is cheaper but risks a mismatch with `fm doctor`. — answered: rejected: verbs are counted from fmcli's add() lines, not skill folders
## Plan review
Self-critique: (1) A hidden caller of a removed verb (a hook, a skill, a script, the MCP server) would break silently; mitigation: git grep for each verb before and after, the full suite, and the MCP tools' argv tests. (2) The user may type a removed verb from memory; mitigation: fm's unknown-verb help already suggests near names, and each new home is in fm which. (3) Folding changes user-facing CLI; it is reversible by git revert and the behaviour stays. (4) The descriptions trim must not drop trigger phrases a skill needs to load; measure with test_docs and the skill tests. Approved under full autonomy.
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-11-01: [confidence: 75%] Fold six verbs (proof, triggers, calibration, incident, sweep, instruments) into prove, outcomes, capture, projects and which, and…
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- T-2359 [FEATURE M, done, 3 steps] Each generation's sweep fails on net growth: footprint, hook p95 and verbs at the seed vs at the sweep (Mission 8, #12) — lesson: A no-…
- T-2077 [RESEARCH L, blocked, 8 steps] Genesis gen 1: Missions 2-8, critiques, lineage, sweep, gen-2 Seed
- similar finished tasks took 3–5 steps
## Lessons
- A verb fold must leave the old name as a hint, not an alias: an argv rewrite carries user-only words past a guard table keyed by verb. And any rules edit needs tests/e2e/sync_evals.py, because the eval cases embed the rules verbatim.
## Plan gaps
- failed first: step 1 pin each folded verb's behaviour with a test under its new home (red)
- failed first: step 3 fold incident, sweep and instruments
- failed first: step 4 every reference moved; docs; fm genesis sweep 1 lean line
## Files touched
- plugin/tests/test_proof.py
- CHANGELOG.md
- MASTER.md
- README.md
- plugin/lib/fmagents.py
- plugin/lib/fmcli.py
- plugin/lib/fmcore.py
- plugin/lib/fmmcp.py
- plugin/lib/fmprove.py
- plugin/tests/test_agents.py
- plugin/tests/test_site.py
- site/pages.py
- site/stats.py
- plugin/tests/test_ecosystem.py
- plugin/tests/test_incident.py
- plugin/tests/test_instruments.py
- plugin/tests/test_outcomes.py
- plugin/tests/test_suspects.py
- plugin/tests/test_ui_signals.py
- plugin/lib/fmdebug.py
- plugin/lib/fmoutcomes.py
- plugin/lib/fmwatch.py
- plugin/lib/fmwhich.py
- plugin/lib/fmeco.py
- plugin/lib/fmfriction.py
- plugin/lib/fmincident.py
- plugin/lib/fminstr.py
- plugin/skills/debug-test/SKILL.md
- plugin/skills/intake/SKILL.md
- plugin/skills/intake/references/planning.md
