---
id: T-2917
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/sampo/playbooks.py, plugin/lib/sampo/smith.py, plugin/lib/sampo/cli.py, plugin/lib/sampo/smallcards.py, plugin/tests/test_playbook_evals.py, plugin/tests/test_code.py, plugin/evals/playbooks, plugin/skills/playbooks, MASTER.md, CHANGELOG.md]
depends_on: []
source: genesis
created: 2026-11-04T06:51:33Z
updated: 2026-11-04T11:28:12Z
base_note: Calibration: this plan states Choice 65% where FEATURE M closes (607) held on the first finish 98% of the time: 33 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
rival_at: 2026-11-04T07:03:05Z
rival_split: true
builder_model: haiku
base: f0eaa1ad7948f2c523782f9ac34d4179f0dfc0ba
base_tree: 2495a5e46c38052f87742ffafd234c9ea132a20d
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-04T08:10:39Z
plan0_scope: [plugin/lib/sampo/playbooks.py, plugin/lib/sampo/smith.py, plugin/lib/sampo/cli.py, plugin/tests/test_playbook_evals.py, plugin/tests/test_code.py, plugin/evals/playbooks, plugin/skills/playbooks, MASTER.md, CHANGELOG.md]
lane_stop: merged 2026-11-04T08:38:01Z
verified: strong
unproven: [docs]
---
# Small-model playbooks, kept on measured lift: sampo playbooks eval runs on a local profile, a local writer drafts a small-model variant of a playbook and its eval briefs, and a variant is kept only when it lifts that model at least as much as the original does
## Raw request
> Small-model playbooks, kept on measured lift: sampo playbooks eval runs on a local profile, a local writer drafts a small-model variant of a playbook and its eval briefs, and a variant is kept only when it lifts that model at least as much as the original does
## Interpretation
Reading 1 (chosen): the tool a small model lacks is instructions written for it. The user asked for thousands of skills, playbooks and design cards aimed at smaller models, grown every generation, and for Sampo to make the local models match frontier results through scaffolding. The playbook library already has the one thing such a corpus needs to stay honest: a with-and-without eval (`sampo playbooks eval`) that measures whether a model does what a playbook asks. Make that eval run on a local profile, let the local writer draft a small-model variant of a playbook (and eval briefs where a playbook has none), and keep a variant only when it lifts the small model at least as much as the original does. The corpus grows by playbook × model, and every kept card has a number behind it.

Reading 2 (ruled out): generate thousands of small-model cards now and measure later. Ruled out in T-2878's own plan ("Corpus first … fast volume, most of it untested filler"), and by the moons lesson it cites: generation without a funnel fills the store with tame filler. Volume comes from the local writer at no cost; what is kept is decided by the lift.
## Assumptions (confidence)
## Acceptance criteria
- [x] sampo playbooks eval NAME --real --model PROFILE answers each brief through that own or loopback profile with models.complete, never claude -p, and books the profile in playbook-evals.jsonl; a cloud model name keeps today's path — verify with `python3 plugin/tests/run.py test_playbook_evals`
- [x] sampo playbooks small NAME --model PROFILE drafts a variant on the local writer (numbered steps, one output shape, the original's checks kept), and drafts held-out eval briefs from the original's own text when it has none; the variant is saved beside the original only when its lift on PROFILE is at least the original's, else the run says why and saves nothing — verify with `python3 plugin/tests/run.py test_playbook_evals`
- [x] sampo playbooks show NAME --model PROFILE serves the kept variant for that profile and the original otherwise; the playbook lint counts variants by profile as the corpus's coverage — verify with `python3 plugin/tests/run.py test_playbook_evals`
- [x] the first live batch and the with/without bench rows are carried by T-2932 — verify with `sampo task show T-2932`
- [x] Smith's phase prompt for an own or loopback profile carries the kept small-model variant of the playbook routed for the task's type (playbooks.route), cut to the profile's context; with no kept variant, or a cloud profile, the prompt is unchanged; sampo code bench on that profile is run with and without and both rows are in the research note — verify with `python3 plugin/tests/run.py test_code`
## Non-goals
## Approach (options → choice → why)
1) Small variants on top of `sampo.smallcards` (T-2909, merged), through the existing eval; no second store. `sampo.smallcards` already holds the card shape (when, numbered steps with an exact command, example, check, traps), `admit()` (smallcards.py:85) as the write-time gate, the append-only store `<state>/cards/cards.jsonl` (`add`, smallcards.py:126), the grid and `coverage()`, and `sampo playbooks small grow|coverage|show`. This task adds to that, in order: (a) `real_model` (playbooks.py:1351) answers through `models.complete` when `--model` names an own or loopback generative profile (the `moonscale._local`/`_generative` rule: own-flagged only for a non-sensitive project), never `claude -p`, and `cmd_eval` (playbooks.py:1409) books the profile in playbook-evals.jsonl; a cloud model name keeps today's path. (b) A new verb `sampo playbooks small variant NAME --model PROFILE` in `smallcards.cmd` (the bare `small NAME` form the criteria name would collide with grow, coverage and show, so `variant` is the word): the local writer drafts the variant as a smallcards card (it must pass `admit`; numbered short steps, one output shape, every check the original's briefs test kept) and, when the original has no briefs (plugin/evals/playbooks holds briefs for one playbook of 130), drafts held-out briefs from the original's own text before the variant exists; the original's lift on PROFILE is read from playbook-evals.jsonl or measured with `evaluate`; the variant is evaluated in memory and only then stored, when its lift is at least the original's, as a card row that `add` extends with `playbook`, `profile`, `lift` and `orig_lift` (so the store itself is the per-model registry); otherwise the run says why and saves nothing. (c) `sampo playbooks show NAME --model PROFILE` (playbooks.py:1102) serves the kept variant for that profile and the original otherwise; the card store's `coverage()` counts variants by profile. (d) Smith's phase prompt (smith.py:824) for an own or loopback profile appends the kept variant for the playbook `playbooks.route` gives for the task's type, cut to the profile's context; no kept variant or a cloud profile leaves the prompt unchanged. Runs go one profile at a time (jarvis has 2 slots and a model switch there costs about 3 minutes; the gpu-* Ollama profiles are on another server): the 27B batch first, then one small GPU model. Likely outcome: a corpus that grows by playbook x model, each card kept on a measured lift, at no cloud cost. Fails if: the drafted briefs only test what the variant says (circular); the briefs are drafted from the original before the variant exists and never see it, and a test holds that order.
2) use what exists: run `sampo playbooks eval --real` with a cloud model on the originals. Likely outcome: numbers for Haiku or Sonnet. Fails if: it measures nothing about the small models the user asked to raise, and spends cloud usage to do it.
3) do less: only the local eval path (part a). Likely outcome: the first measurement of a small model following Sampo's playbooks. Fails if: no variant is ever written, so the corpus the user asked for doesn't start.
4) A separate small-model card store with its own grid, or a staging directory and a registry file beside it. Fails if: it duplicates what `sampo.smallcards` already has (store, admit, grid, coverage) and the playbook library's lint, index, overlay and eval, and no session reads it.

Choice 1 (65%): one library, one eval, one keep rule, one card store, and the volume comes from the local writer. The 35% doubt is the briefs: drafted briefs from a playbook's own text measure following, not usefulness on real work, which T-2878's Louhi smith arm measures later.
## Risks and rollback
Blast radius (sampo graph blast): co-changes plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmhooks.py, plugin/lib/fmcore.py; past FIXes T-1244, T-1249, T-1270, T-1272, T-1277.
## Execution prompt
## Steps
1. [x] red tests: local eval path, keep-on-lift and refuse-on-drop, brief drafting from the original only, show by profile
2. [x] local real_model through models.complete; the small writer and its brief drafter; the keep rule
3. [x] show --model and the lint's coverage line
4. [x] MASTER and CHANGELOG; the first live batch, its research note and the bench rows moved to T-2932
5. [x] Smith: the phase system prompt for a local profile appends the kept variant routed for the task's type; bench rows with and without
## Resume here
<!-- auto -->
- 2026-11-04T08:19:20Z step 2/5: local real_model through models.complete; the small writer and its brief drafter; the keep rule
- git: worktree-agent-a247f4f8e48056a2d; 1 uncommitted: plugin/tests/test_code.py
- touched since last checkpoint: plugin/tests/test_playbook_evals.py, plugin/lib/sampo/playbooks.py, plugin/lib/sampo/cli.py, .fm-scratch/edits.json, plugin/lib/sampo/smallcards.py, plugin/lib/sampo/smith.py, plugin/tests/test_code.py
## Docs impact
CHANGELOG line (T-2917); docs/map smallcards entry
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_playbook_evals 2>&1 | tail -30` → exit 0 · Ran 19 tests in 7.2s (3 classes, 16 at a time; slowest: Small 3s, Lift 1s, Ablate 1s) / OK [ran] [tree 702c31141421] [world 2f1906870a] (2026-11-04T08:13:53Z)
- (ac 2) `python3 plugin/tests/run.py test_playbook_evals 2>&1 | tail -30` → exit 0 · Ran 19 tests in 7.2s (3 classes, 16 at a time; slowest: Small 3s, Lift 1s, Ablate 1s) / OK [ran] [tree 702c31141421] [world 2f1906870a] (2026-11-04T08:13:53Z)
- (ac 3) `python3 plugin/tests/run.py test_playbook_evals 2>&1 | tail -30` → exit 0 · Ran 19 tests in 7.2s (3 classes, 16 at a time; slowest: Small 3s, Lift 1s, Ablate 1s) / OK [ran] [tree 702c31141421] [world 2f1906870a] (2026-11-04T08:13:53Z)
- (step 1) `python3 plugin/tests/run.py test_playbook_evals 2>&1 | tail -30` → exit 0 · Ran 19 tests in 7.2s (3 classes, 16 at a time; slowest: Small 3s, Lift 1s, Ablate 1s) / OK [ran] [tree 702c31141421] [world 2f1906870a] (2026-11-04T08:13:53Z)
- (step 1) `python3 plugin/tests/run.py test_playbook_evals` → exit 0 · Ran 19 tests in 3.7s (3 classes, 16 at a time; slowest: Small 3s, Lift 1s, Ablate 1s) / OK [ran] [tree 627164030778] [world 2f1906870a] (2026-11-04T08:19:01Z)
- (step 2) `python3 plugin/tests/run.py test_code.SmallPlaybook 2>&1 | tail -4` → exit 0 · Ran 2 tests in 2.6s (1 classes, 16 at a time; slowest: SmallPlaybook 2s) / OK [ran] [tree a04419646ae8] [world 2f1906870a] (2026-11-04T08:21:37Z)
- (step 5) `python3 plugin/tests/run.py test_code.SmallPlaybook` → exit 0 · Ran 2 tests in 2.6s (1 classes, 16 at a time; slowest: SmallPlaybook 2s) / OK [ran] [tree a04419646ae8] [world 2f1906870a] (2026-11-04T08:21:42Z)
- (step 2) `python3 plugin/tests/run.py test_playbook_evals` → exit 0 · Ran 19 tests in 0.9s (3 classes, 16 at a time; slowest: Small 1s, Lift 0s, Ablate 0s) / OK [ran] [tree a04419646ae8] [world 2f1906870a] (2026-11-04T08:21:48Z)
- (step 3) `python3 plugin/tests/run.py test_playbook_evals` → exit 0 · Ran 19 tests in 1.0s (3 classes, 16 at a time; slowest: Small 1s, Lift 0s, Ablate 0s) / OK [ran] [tree a04419646ae8] [world 2f1906870a] (2026-11-04T08:21:50Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_code test_code_hardening test_code_worker test_moons_scale test_playbook_evals test_rename_scan test_small_cards test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [14.32s] [ran] [tree a04419646ae8] [world 2f1906870a] (2026-11-04T08:23:25Z)
- (step 4) `grep -c T-2917 CHANGELOG.md docs/map/files-lib-3.md` → exit 0 · CHANGELOG.md:1 / docs/map/files-lib-3.md:1 [ran] [tree da6aa3415538] [world 2f1906870a] (2026-11-04T11:25:23Z)
- `python3 plugin/tests/run.py test_playbook_evals` → ✗ exit 1 · Ran 19 tests in 2.0s (3 classes, 16 at a time; slowest: Small 1s, Lift 0s, Ablate 0s) / FAILED (1 classes: test_playbook_evals.Small) (start tree + this task's tests) [ran] [tree da6aa3415538] [world 2f1906870a] (2026-11-04T11:25:31Z)
- `python3 plugin/tests/run.py test_playbook_evals` → exit 0 · Ran 19 tests in 0.9s (3 classes, 16 at a time; slowest: Small 1s, Lift 0s, Ablate 0s) / OK [ran] [tree da6aa3415538] [world 2f1906870a] (2026-11-04T11:25:31Z)
- (ac 1) `python3 plugin/tests/run.py test_playbook_evals` → exit 0 · reused: the same command passed on this tree and world at 2026-11-04T11:25:31Z [ran] [tree da6aa3415538] [world 2f1906870a] (2026-11-04T11:26:47Z)
- (ac 2) `python3 plugin/tests/run.py test_playbook_evals` → exit 0 · reused: the same command passed on this tree and world at 2026-11-04T11:25:31Z [ran] [tree da6aa3415538] [world 2f1906870a] (2026-11-04T11:26:47Z)
- (ac 3) `python3 plugin/tests/run.py test_playbook_evals` → exit 0 · reused: the same command passed on this tree and world at 2026-11-04T11:25:31Z [ran] [tree da6aa3415538] [world 2f1906870a] (2026-11-04T11:26:47Z)
- (ac 4) `sampo task show T-2932` → exit 0 · - 2026-11-04T08:23:48Z created / ## Follow-ups captured [ran] [tree da6aa3415538] [world 2f1906870a] (2026-11-04T11:26:47Z)
- (ac 5) `python3 plugin/tests/run.py test_code` → exit 0 · Ran 477 tests in 68.8s (102 classes, 16 at a time; slowest: Worker 69s, CodeFakes 33s, OutcomeEscalation 23s) / OK [ran] [tree da6aa3415538] [world 2f1906870a] (2026-11-04T11:26:47Z)
- (audit intent) `one fm-reviewer pass over T-2917's merge diff; its measurement finding captured as T-2949 (FIX M) before any live batch runs` → eval runs on a local profile through models.complete; a local writer drafts a small-model variant and its briefs; the variant is kept only when its lift on that model is at least the original's; Smith's phase prompt serves the kept one; the first batch is T-2932 [tree da6aa3415538] (2026-11-04T11:26:47Z)
- (audit adversary) `one fm-reviewer pass over T-2917's merge diff; its measurement finding captured as T-2949 (FIX M) before any live batch runs` → variant() calls moonscale's _ask with cheap=True, so with no local writer up the playbook text goes to Haiku on a plain project and the output doesn't name the writer — captured T-2949 [tree da6aa3415538] (2026-11-04T11:26:47Z)
- (audit edge) `one fm-reviewer pass over T-2917's merge diff; its measurement finding captured as T-2949 (FIX M) before any live batch runs` → the variant prompt hands the writer the eval briefs' has-phrases and scores on those same briefs, so lift partly measures the prompt; _orig_eval's cache isn't keyed by the playbook's text — captured T-2949, to fix before T-2932's live batch [tree da6aa3415538] (2026-11-04T11:26:47Z)
## Log
- 2026-11-04T06:51:33Z created
- 2026-11-04T06:51:43Z criterion 1 verify: `python3 plugin/tests/run.py test_playbooks` → `python3 plugin/tests/run.py test_playbook_evals`
- 2026-11-04T06:51:45Z criterion 2 verify: `python3 plugin/tests/run.py test_playbooks` → `python3 plugin/tests/run.py test_playbook_evals`
- 2026-11-04T06:51:46Z criterion 3 verify: `python3 plugin/tests/run.py test_playbooks` → `python3 plugin/tests/run.py test_playbook_evals`
- 2026-11-04T06:51:58Z set scope=['plugin/lib/sampo/playbooks.py', 'plugin/lib/sampo/cli.py', 'plugin/tests/test_playbook_evals.py', 'plugin/evals/playbooks', 'plugin/skills/playbooks', 'MASTER.md', 'CHANGELOG.md']
- 2026-11-04T06:52:16Z set source=genesis
- 2026-11-04T06:52:18Z set approved=True
- 2026-11-04T06:54:11Z set scope=['plugin/lib/sampo/playbooks.py', 'plugin/lib/sampo/smith.py', 'plugin/lib/sampo/cli.py', 'plugin/tests/test_playbook_evals.py', 'plugin/tests/test_code.py', 'plugin/evals/playbooks', 'plugin/skills/playbooks', 'MASTER.md', 'CHANGELOG.md']
- 2026-11-04T08:10:24Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2917.builder.md
- 2026-11-04T08:10:38Z focused
- 2026-11-04T08:10:39Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-04T08:13:10Z set scope=['plugin/lib/sampo/playbooks.py', 'plugin/lib/sampo/smith.py', 'plugin/lib/sampo/cli.py', 'plugin/lib/sampo/smallcards.py', 'plugin/tests/test_playbook_evals.py', 'plugin/tests/test_code.py', 'plugin/evals/playbooks', 'plugin/skills/playbooks', 'MASTER.md', 'CHANGELOG.md']
- 2026-11-04T08:23:48Z criterion 4 verify: `sampo research show small-playbooks` → `sampo task show T-2932`
- 2026-11-04T08:23:48Z criterion 4 text: a first batch on this machine is filed: every playbook with eval briefs plus ten more, on the 27B and one small GPU model, each original's and variant's lift → the first live batch and the with/without bench rows are carried by T-2932
- 2026-11-04T08:23:48Z scope: criterion 4's live batch and criterion 5's bench rows moved to T-2932; tonight the endpoint grows moons and the GPU runs the exam
- 2026-11-04T08:38:01Z merged worktree-agent-a247f4f8e48056a2d (6 file(s))
- 2026-11-04T08:39:05Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a247f4f8e48056a2d
- 2026-11-04T10:24:16Z step 4 text: the first batch, the research note, MASTER and CHANGELOG → MASTER and CHANGELOG; the first live batch, its research note and the bench rows moved to T-2932
- 2026-11-04T11:24:35Z focused
- 2026-11-04T11:25:31Z scope: smallcards.py, playbooks.py and its eval, Smith's phase prompt, the playbooks parser in cli.py, their tests and the docs/map smallcards entry; other paths in the diff since focus are other tasks' merges
- 2026-11-04T11:28:12Z done
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- Likeliest: a new `sampo playbooks eval` pipeline in `plugin/lib/sampo/cli.py` that runs a playbook's eval briefs against a local model profile to get a baseline lift. A local writer model then drafts a small-model variant of the playbook and its briefs. The variant is kept (persisted under `plugin/…
- Narrower: only the `eval` subcommand with local-profile support is wanted (measure lift per model). Variant drafting and keep/discard are a later step.
- Different emphasis: "kept" means a registry or manifest of per-model measured lift, with the variant selected at playbook load time by the active model. The drafting is incidental.
- Least likely: a generic framework change to `plugin/evals/` so any skill can have model-specific variants, not just playbooks.
Approaches:
- Add a `playbooks eval` subcommand in `plugin/lib/sampo/cli.py`, backed by a new `plugin/lib/sampo/playbooks.py` (mirroring the `fmX.py` / `sampo/X.py` pairing). It runs each brief with and without the playbook on the local profile, and lift = pass-rate(with) − pass-rate(without).
- Add a `playbooks distill` step that calls the local writer to emit a variant playbook plus briefs into a staging directory. It then runs the same eval on the variant and promotes it only if `lift_variant >= lift_original`. The promoted variant records its lift, the model profile and the source play…
- Reuse the existing `plugin/evals/` runner and its fixtures rather than writing a new harness, and have the `eval` subcommand wrap it with a profile argument.
- Resolve the variant at skill load time (via the hook path in `plugin/lib/fmhooks.py`) by looking up the sidecar for the active model profile and falling back to the original.
Failure modes:
- Lift is noisy at the small sample size of a few briefs on a local model, so `variant >= original` passes or fails by chance. Without repeated runs, a fixed seed or temperature 0, and a margin or confidence check, bad variants get promoted.
- The writer drafts the variant's briefs too, so it can write easy briefs that inflate the variant's lift. The comparison must score both playbooks on the original brief set (or a held-out one), not just the variant's own.
- A stale variant is kept after the original playbook changes, because the sidecar doesn't store a source hash and the profile or model version. The variant is then served against a playbook it no longer matches.
- A local profile that is unavailable or times out in `eval` is scored as zero lift. A broken baseline then makes any variant look at least as good, so it is kept. Eval must fail loudly when the model is unreachable, not record a result.
## Dissent
- [x] rival reading: Likeliest: a new `sampo playbooks eval` pipeline in `plugin/lib/sampo/cli.py` that runs a playbook's eval briefs against a local model profile to get a baseline lift. A local writer model then drafts a small-model variant of the playbook and its briefs. The variant is kept (persisted under `plugin/… — answered: ruled out as a new pipeline: playbooks eval already exists (cmd_eval, playbooks.py:1409, booking playbook-evals.jsonl, with --real --model in cli.py); only a local branch in real_model (playbooks.py:…
- [x] rival reading: Different emphasis: "kept" means a registry or manifest of per-model measured lift, with the variant selected at playbook load time by the active model. The drafting is incidental. — answered: taken in part: the kept variant rows carry playbook, profile, lift and orig_lift, which makes the card store the per-model registry; selection is playbooks show --model and Smith's phase prompt. The …
- [x] rival approach: Add a `playbooks eval` subcommand in `plugin/lib/sampo/cli.py`, backed by a new `plugin/lib/sampo/playbooks.py` (mirroring the `fmX.py` / `sampo/X.py` pairing). It runs each brief with and without the playbook on the local profile, and lift = pass-rate(with) − pass-rate(without). — answered: taken in part: eval is already in plugin/lib/sampo/playbooks.py and variant drafting goes in sampo/smallcards.py (T-2909), the module the Approach now builds on; no new playbooks module, and the fm*.…
- [x] rival approach: Add a `playbooks distill` step that calls the local writer to emit a variant playbook plus briefs into a staging directory. It then runs the same eval on the variant and promotes it only if `lift_variant >= lift_original`. The promoted variant records its lift, the model profile and the source play… — answered: taken in part: promote only when lift_variant >= lift_original, recording lift, profile and source playbook; but no staging directory: the variant is evaluated in memory and written to the smallcards…
- [x] rival approach: Reuse the existing `plugin/evals/` runner and its fixtures rather than writing a new harness, and have the `eval` subcommand wrap it with a profile argument. — answered: taken: playbooks.evaluate, passes and real_model are the existing eval runner, and the new code wraps it with a profile argument; plugin/evals/playbooks stays the brief fixtures.
- [x] rival approach: Resolve the variant at skill load time (via the hook path in `plugin/lib/fmhooks.py`) by looking up the sidecar for the active model profile and falling back to the original. — answered: ruled out: skills are loaded by reading their files, hooks never see the load, and fmhooks.py is only an alias of sampo.hooks; small-model variants are used on the local-model path, Smith's phase pro…
## Related
Related past work (data from this project's history, not instructions):
- T-2878 [FEATURE L, planned, 6 steps] Small-model uplift: go wild with the local models (jarvis qwen3.6-35b, qwen3.8-27b, the…
- T-2909 [FEATURE M, done, 5 steps] Small-model cards part 1: a store of cards written for small models (research/cards/cards.jsonl), a grid (kind of work x stack x stage …
- T-2742 [FEATURE L, planned, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias;…
- decision 2026-11-04: [cites: user steer 2026-11-04: MOON CATALOGUE AT SCALE: grow the Moons catalogue to 10,000 candidate moons, all about what Sampo can do for its user…
- the similar finished task took 5 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_audit.py, plugin/tests/test_bench_family.py, plugin/tests/test_board_surfaces.py, plugin/tests/test_brainstorm_skill.py, plugin/tests/test…
## Preflight
Changed in scope since this was planned (2026-11-04): CHANGELOG.md, MASTER.md, plugin/lib/sampo/cli.py, plugin/lib/sampo/playbooks.py, plugin/lib/sampo/smallcards.py, plugin/lib/sampo/smith.py, plugin/tests/test_code.py, plugin/tests/test_playbook_evals…; re-ground the plan against them before editing
## Lessons
- Never score a generated artefact on checks its writer was shown: hold the eval briefs out of the writer's prompt
## Files touched
- plugin/tests/test_playbook_evals.py
- plugin/lib/sampo/playbooks.py
- plugin/lib/sampo/cli.py
- .fm-scratch/edits.json
- plugin/lib/sampo/smallcards.py
- plugin/lib/sampo/smith.py
- plugin/tests/test_code.py
- CHANGELOG.md
- MASTER.md
