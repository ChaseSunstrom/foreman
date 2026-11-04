# Mission 7 — getting the tools it lacks (gen 4, #5): instructions written for small models, kept on lift

Task: T-2917 (brief 1).

Parent: gen-4/seed.md row 7 → gen-0.md #5: "Getting the tools it lacks. When it hits something it can't do, it finds an
existing plugin, skill or MCP server (`fm plugins find`, `fm lib search`) or builds one (`fm mcp new`, a script, a
project skill), tests it, and uses it. Install grants are queued for me, never self-granted." gen-0's goal, MUSTs and
NEVERs are quoted in the seed and apply here unchanged.

## Capability
The tool a small model lacks is instructions it can follow. The user's standing steer (2026-11-03, T-2878): make the
local models match frontier results through scaffolding, and build "thousands of skills, playbooks, UI instructions
and designs written for smaller models", grown every generation. Read on this machine before planning:
- `sampo code bench` history (state/code-bench.jsonl, 2026-11-04): the 4B qwen and the e4b gemma each closed 4 of 5
  seeds as Smith workers. The 27B closed 1 of 5, its four misses endpoint errors, not wrong code. Small models can do
  the work. What they lack is measured help.
- The playbook library has 130 playbooks under plugin/skills/playbooks/references and a with-and-without eval that
  says whether a model does what a playbook asks. It has eval briefs for one playbook
  (plugin/evals/playbooks/verify/tdd-workflow.json), and two runs on record, both on the scripted "literal" model
  (state/playbook-evals.jsonl). Nothing has measured a real model against a playbook, small or large.
So the corpus the user asked for has a home and a gate already. It lacks a writer, a small-model path through the
gate, and briefs.

## Grounding (each read in the code on 2026-11-04)
- plugin/lib/sampo/playbooks.py:1351 `real_model` answers every brief through `ideas.run_child`, which is `claude -p`
  (ideas.py:78), so no local profile can be evaluated. playbooks.py:1342 `literal` is the scripted model.
  playbooks.py:1372 `evaluate` returns {n, with, without, lift}. playbooks.py:1397 `ablate` gives each section's share.
  playbooks.py:1409 `cmd_eval` writes the row. playbooks.py:1331 `passes` grades has/not/re checks.
- playbooks.py:1273 `EVALS` = plugin/evals/playbooks/<stage>/<name>.json, one file today.
- The module docstring (playbooks.py:1-30): `fm playbooks show NAME` is how the skill loads a playbook, with the
  project's overlay after it. That is the place a per-profile variant is served from.
- plugin/lib/sampo/models.py:786 `complete` is the local call; plugin/lib/sampo/moonscale.py:379 `_local` is the
  routing (own or loopback, loopback only when sensitive).
- The session path that will use a kept variant: plugin/lib/sampo/smith.py:824 `phase` builds each step's system
  prompt from `ACT_PROMPT` (smith.py:169) for whatever profile runs it, and loads no playbook today. A `sampo code`
  run on a local profile is where a small model meets Sampo's instructions. plugin/lib/sampo/playbooks.py:609
  `route(stage)` already names the books for a task's type or stage.
- T-2878 (open, L) plans this as its step 4 ("corpus: the card store, grid and coverage, the A/B gate; bulk on the
  local models"). T-2917 is that step's first M, cut to reuse the playbook library instead of a new store.

## Not-yet items in this area (retried, read only)
- jeff, selfjev-4b: the model bench (`sampo exam models show`, run m20261103-223621959) now has them. jeff scores 0.52
  on intake type and 0.235 on tier, against the majority baseline's 0.595 and 0.58. The `orchestrator` row (the path
  they would replace) has n=0, because no held-out task has a shadow row of the orchestrator's own call. Still blocked.
  It unblocks once orchestrator rows exist on held-out tasks, and the bench shows jeff under the baseline anyway.
- d3:4b (a decision model, not a not-yet item) reads 0.73 on intake type against 0.595: the first local arm to beat a
  baseline on Sampo's own work. Carried to the next #8 or model-layer Mission.

## Gaps this Mission targets (coverage: #5)
- build × CLI: `sampo playbooks small` builds the instruction a small model lacks and tests it before keeping it.
- learn × headless/server: the corpus grows on the local models with no session and no spend.

## Ideas (from the brainstorm, grounded)
fm mission, then fm ideas --rounds 4 --falsify --crossbreed --seen-latest 6 (research/brainstorm-20261104-003757: 369
distinct ideas; --deepen dropped by today's risk budget, one grid lens failed in round 2, both recorded). Grounded:
- "Build the Card Foundry: mine failures, write, cold-test, keep only measured lift" (cross-bred) and "Have the 27B
  write cards, and a different small model test them cold": new, and brief 1. The 27B writes, a small GPU model is
  measured, and lift decides.
- "Gate every card on a bare-model exam before it enters the store": partial. `evaluate` already measures with and
  without. Brief 1 runs it on the bare small model.
- "Re-measure cards when the served model changes, and retire the ones that stopped helping": new. It builds on brief
  1's rows, which book the profile, and is held for the next #5 Mission.
- "Wild: A 'dumbest model' floor: find the smallest model that passes each card's task and print it on the card":
  new. It falls out of running the same variant across the 27B and the 4B/9B profiles. Held.
- Friction seen while grounding: sessions reached for `fm models` (this one too), `fm andon` and `fm shot 1440 --full`
  (`sampo friction`, 2026-11-04). These are tools a session lacked by name. Carried as a #5 lead: an unknown verb a
  session reaches for twice becomes an alias or a capture.

## Approaches
1. Small variants through the existing eval: a local `real_model`, a `small` writer that also drafts briefs from the
   original when it has none, keep-on-lift, `show --model`, coverage in the lint. Smith's phase prompt for a local
   profile carries the kept variant routed for the task's type, so every `sampo code` run on a small model uses it.
   Likely outcome: a corpus growing by playbook × model, each card with a lift, read by the runs it was written for. Fails if: the briefs only test what the variant says. The briefs are
   drafted from the original before the variant exists, and a test holds the order.
2. use what exists: `eval --real` on a cloud model. Fails if: it measures nothing about small models and spends usage.
3. do less: the local eval path only. Fails if: the corpus never starts.
4. A separate card store. Fails if: it duplicates the library's lint, index and eval, and nobody reads it.

Choice: 1 (65%).

## Exam (an outcome measure, with a live reading)
- Outcome measure: per playbook and profile, the original's lift and the variant's lift on held-out briefs, for every
  playbook with briefs plus ten more, on the 27B and one small GPU model. Filed as research/small-playbooks. A
  variant counts only when its lift is at least the original's. The note reports how many were kept, how many
  refused and the mean lift gained.
- Live reading at close: `sampo playbooks show <a kept one> --model <profile>` serves the variant, the lint's
  coverage line counts it, and `sampo code bench` on that profile runs with and without the variant in Smith's
  prompt, both rows in the note (five seeds are a smoke signal, never the verdict).
- Which way the measure may differ from real work: brief-following is an upper bound on usefulness. T-2878's Louhi
  smith arm measures real closes later.
- Exam kinds: #5's tool-find, tool-build and tool-grant scenarios are unchanged.

## Long-horizon goal (end of run)
On a held-out goal worked by a local model through Smith, the small-model playbooks raise its true-done count over
the same model with the originals.

## Risks
- Circular grading: briefs drafted from the original before the variant, held by a test, and a different small model
  measures the 27B's writing.
- Library bloat: variants sit beside originals under the existing lint (title and shingle duplicates, size ceilings),
  and a refused variant is never saved.
- Context limits: the GPU profiles hold 32,768 tokens. A variant must fit with its task, and the writer is told the
  target profile's context.
- Spend: local only. A cloud model name keeps today's budgeted path.

## Lean
No new store and no new verb: a subcommand and a flag on `sampo playbooks`. The reach is real from the first day,
because Smith's local runs read the kept variants (smith.py:824), and `sampo playbooks show` is the skill's own load
path. No hook.

## Tier share
Brief 1 is tier 3: the first measured scaffold for small models in Sampo's own instructions.

## Hands to the next generation
The first lift table per playbook and model. The next #5 Mission grows the corpus to design and UI cards on the same
gate, retires cards whose lift decays when a model changes, and gives T-2878's Louhi smith arm (step 1) the variants to
measure on real closes.

## Done when
T-2917's five criteria are green, the research note is filed, and MASTER.md (fmplaybooks) and CHANGELOG say it.
