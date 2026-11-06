# Mission 8 — moonshot (gen 4): regrow Sampo's own code from its intent, and an ecology of minds

Task: T-2918 (brief 1: M-02's slice, plus filing this Mission's ecology moons in the catalogue).

Parent: gen-4/seed.md row 8 → the Moonshot section (far-domain lens: ecology; judged on novelty and value only).
gen-0's goal, MUSTs and NEVERs are quoted in the seed and apply here unchanged.

## Capability
Two things this generation, both far from any coverage cell.
1. The floor: advance one extreme or massive moon by a stage. The record points at M-02 (massive, "Keep code as a
   regenerable cache of intent clauses and proofs"). It is the only big moon whose kill test came back viable: 3 of 3
   spec-suite modules were rebuilt blind and passed every original test (bench/moonshot/m02-result.json, T-2679). Its
   kill line names the next stage: "the slice must regenerate a module of Foreman's own, whose spec is its briefs".
   The gen-4 prediction, sealed before the user's next steers, expects the user to ask for exactly this step. The
   standing intent says to act on what the user would say before they say it.
2. The lens: ecology. Moons that borrow a mechanism no harness has and are wild enough that people who build agent
   harnesses ask whether it is even possible (the user's 2026-11-03 steer; never pricing, auction or warranty
   mechanics).

## Grounding (each read on 2026-11-04)
- The catalogue (`sampo moons status`): 58 of 100. Author's tiers: low 1/5, medium 2/10, high 3/15, xhigh 4/20,
  extreme 29/25, massive 19/25. 1 of 18 extreme or massive kill-tested, 0 built. The climb (`sampo moons order`) opens
  with M-18 full (low, unblocks M-02), then kills for M-21 to M-28. Toward the mix means massive and xhigh, not more
  extreme.
- M-02's block: Needs M-18 (prove a rewrite against the old build on recorded inputs), Stage kill. The slice lands
  nothing, so M-18 stays the need of M-02's full build, not of its slice.
- The module set for the slice: in plugin/lib/sampo, 20 leaf modules under 260 lines have their own test file, from
  backtest.py (36 lines, 1 importer) to repeats.py (222 lines, 2 importers). raster.py (156 lines, a 376-line test,
  1 importer) and away.py (102 lines, 141-line test) are typical. Counted by a shell loop over `wc -l` and the test
  files, not chosen by hand.
- The local call and routing: plugin/lib/sampo/models.py:786 `complete`, plugin/lib/sampo/moonscale.py:379 `_local`.
  The 27B's Smith record: `sampo code bench` (state/code-bench.jsonl) closed 1 of 5 seeds on endpoint errors, while
  the 4B and e4b GPU models closed 4 of 5. So the slice names Haiku as its second approach before any not-yet.
- Moons at scale (the user's steer a): `sampo moons coverage` reads 4,879 candidates (3,362 kept, 1,517 rejected),
  420 of 420 grid cells touched, 24 of 24 mechanisms, and the local 27B's keep rate is 83% against Haiku's 36%.
  Mission 6 (T-2916) puts grow and funnel on the nightly timer at $0, which is how the catalogue reaches 10,000.
- Frontier digest: gen-2/frontier.md stands (gen-3/frontier.md: "Off the cadence"). Gen 4 is off the cadence too.
- Not-yet in this campaign: M-12 (no decider beat chance) waits on a close-time forecaster (verification grade and
  unproven kinds). M-13's kill needs 20 answered questions, and the ledger holds 2 `question_answered` rows. Neither is
  unblocked by anything built since. Both carried.

## Ideas (each with its prior art, how ours is better, and a novelty mark)
fm mission, then fm ideas --rounds 4 --falsify --crossbreed --seen-latest 6 with three ecology lenses, inversion, 2030
worked back, bold bets, crossbreeding and an invented lens (research/brainstorm-20261104-003815: 405 distinct ideas;
--deepen dropped by today's risk budget, recorded). Most of its ecology ideas were funnel mechanics (succession-staged
funnels, rarefaction stops, diversity alarms). Those are tools inside a moon, never the moon, so they go to Moonscale's
own backlog. The three below are the wild ones, each crossbred and named with its parents.

### M-59 · Fuse two small models into a lichen that outthinks the frontier model neither can match
- Tier: xhigh
- Domain: model orchestration and small-model uplift
- Lens: ecology: symbiosis (a lichen is an alga and a fungus that become one organism neither can be alone);
  crossbred from "Pair two weak models as a lichen" × "Rate each local model as a symbiont, with a cheater cut-off"
- What: Sampo pairs a fast small model (the alga: a 4B that proposes) with the large local model (the fungus: the 27B
  that holds structure and memory) and evolves the exchange between them over nightly rounds on Sampo's own closed
  tasks: what each passes the other, when, and in what shape. Neither model is fine-tuned. The protocol is the
  organism, kept as a versioned card the pair carries. The jaw-drop is a pair that closes held-out tasks the frontier
  model closes, at no cloud cost, while each partner alone closes half as many.
- Prior art: mixture-of-agents and LLM debate (fixed protocols, peer models); speculative decoding (a small model
  drafts tokens for a large one, by a hand-fixed protocol); Sampo's routing (local first, then Haiku, never a pair).
- Better by: the protocol is evolved and selected on the user's own held-out work, and the pair is judged against the
  frontier arm, not against either partner.
- Novelty: 4
- Needs: T-2878 (a Louhi smith arm on local models), T-2917 (small-model playbooks kept on lift)
- Unblocks: none
- Kill: on 20 train-split Louhi scenarios, run the 4B alone, the 27B alone and three hand-written pair protocols
  (propose and critique, outline and fill, test-first and implement), graded by each scenario's hidden checks.
  Viable if the best pair beats the better partner alone by 5 or more scenarios; not-yet if by 1 or fewer.
- Stage: idea

### M-60 · Grow a mycorrhizal network under every repo on the machine, trading failure shapes as nutrients
- Tier: massive
- Domain: cross-project learning
- Lens: ecology: mycorrhizal networks (fungi join the roots of different trees and carry carbon and alarm signals
  between them); crossbred from "Grow a mycorrhizal lesson network between repos and lanes" × "Federate failure shapes
  between Sampo installs"
- What: Every repo Sampo serves grows hyphae: compressed failure shapes from its proven fixes, the outline of a bug's
  syntax and data flow and never its code. The network carries each shape to repos whose code is near it, and a repo
  that receives one is warned before it writes that bug. Trees that fix more feed more. A sensitive repo neither sends
  nor receives. Over months the network learns which of the user's repos are kin, and a new repo is inoculated from
  its nearest kin on day one.
- Prior art: GitHub's multi-repository variant analysis (people write the query for one known bug); Semgrep registry
  rules (shared by hand); federated learning (shares gradients, not failure shapes); Sampo's lessons (one project's).
- Better by: shapes move by measured kinship between the user's own repos, unasked, and a delivered warning counts
  only when the receiving repo later fixes that shape.
- Novelty: 4
- Needs: a failure-shape miner from proven FIX tasks (the miner M-22 also needs), kinship from import graphs and stack
  cards, a cross-project store under the sensitive rule
- Unblocks: M-22
- Kill: over every project in Sampo's state with 5 or more proven FIX tasks, ask of each fix whether a shape mined
  from another project's earlier fixes flags the lines the fix changed, before the fix, at under one false flag per
  2,000 lines. Report each project's era (first and last fix date) and fail the run if the eras don't overlap.
  Viable if 10% or more of fixes were foreseen by a kin repo; not-yet if under 3%.
- Stage: idea

### M-61 · Breed a Red Queen: a predator that evolves new bugs against Sampo's own detectors every night
- Tier: massive
- Domain: verification by adversarial co-evolution
- Lens: ecology: Red Queen dynamics (predator and prey must keep evolving to stay where they are); crossbred from "Run
  a Red Queen arms race between generator and critic" × "Reintroduce an apex predator into the funnel"
- What: A predator lineage on the local models writes plausible bugs into throwaway copies of the user's repos, aimed
  at slipping past Sampo's finders, guard, review lenses and tests. Every bug that escapes is a lesson the prey (the
  detectors) must learn before the next night, and every detector that improves forces the predator to evolve. Both
  populations are scored, and the arms race's trace is a living map of where Sampo is blind.
- Prior art: mutation testing (random, not adaptive); coverage-guided fuzzing (finds crashes, not quiet logic bugs);
  GANs (images, not code); LLM red-teaming (prompts); Sampo's hunk-mutation proof (T-0271), which mutates one task's
  hunks once.
- Better by: the bug writer adapts to the detectors Sampo actually runs, and the detectors are scored only on bugs
  nobody wrote for them, on the user's own code.
- Novelty: 4
- Needs: T-2910 (local brainstorm volume), the exam's planted-defect renderer, a night slot (T-2916)
- Unblocks: M-22
- Kill: on the exam's throwaway repos, have the local 27B write 100 bugs over three rounds, each round shown which
  earlier bugs `sampo find` caught. Viable if the third round's escape rate is at least twice the first's (the
  predator learns); not-yet if it is flat.
- Stage: idea

The novelty marks above are the author's. `fm genesis novelty` marks the obvious ones by a cold read, and a typed mark
counts for nothing.

## The spike: M-02's slice (brief 1)
`sampo regen PATH --model PROFILE` works in a throwaway worktree only. It removes the module and gives a tool-less
model the module's intent and never its code: the Raw request, Interpretation and criteria of every brief whose
scope or touched files name it, its MASTER.md entry, its test file and the names its importers use. The reply is
checked (it compiles, and imports nothing the original didn't), written, and the module's own tests run, each result
printed. There are two tries, and the main checkout is never written. The slice run covers all 20 leaf modules, with
the 27B first and Haiku second where the 27B fails, its sample stated before it runs and its result kept beside the
script (T-2721, T-2724).

## Approaches
1. `sampo regen` as a verb plus the slice run over the leaf set. Likely outcome: a round-trip rate per module, and
   the failures show where Sampo's briefs and tests don't pin its code, which is M-02's claim. Fails if: briefs
   written as change requests are too thin to rebuild anything. Then not-yet with that blocker and both approaches.
2. use what exists: rerun kill_m02.py on Sampo modules. Fails if: it is a script, not the working slice the stage
   asks for.
3. do less: one module by hand. Fails if: it is one anecdote, and nothing reruns it.
4. Regenerate and land on green tests. Fails if: passing tests isn't equivalence on real inputs. That is M-18, the
   full build's need.

Choice: 1 on the leaf set (60%). The doubt is real, and a failure is a finding.

## Exam
No exam kind (a moonshot is judged on novelty and value). The slice's check: of the 20 leaf modules, 2 or more
round-trip (every original test green) on the 27B or, second, on Haiku → "Advanced: M-02 slice (T-2918)" goes into
this file and the catalogue's Stage line becomes slice, with Evidence: T-2918. Fewer → not-yet.md gets M-02's slice
with its blocker and both approaches, and M-02 stays at kill. Measure (for the catalogue's Measure: line): the
round-trip rate over the leaf set, rerun each generation, where a rising rate means intent and proofs pin more code.

## Campaign (MOONSHOT.md part A)
- Planned: M-02 slice (T-2918). The Advanced line is written only when the slice result is filed.
- Added toward the mix: M-59 (xhigh), M-60 (massive), M-61 (massive), each with a Kill line. T-2918 files them in
  moonshot.md and runs `sampo moons rate`, so the strongest model tiers them blind.
- Carried: M-12 and M-13 not-yet (see Grounding). M-18 full stays first in the climb as M-02's full-build need.

## Long-horizon goal (end of run)
Any module of Sampo's can be deleted and regrown from its intent and proofs on a local model, and the modules that
can't are the ones whose briefs and tests are listed as too weak, each with a task to strengthen them.

## Risks
- Leakage: the module's code must never reach the prompt. Its docstring, comments and any MASTER.md line that quotes
  code are cut. A test holds that no line of the original appears in the prompt.
- Running model code: a reply runs only inside the throwaway worktree, under the module's own tests, after a compile
  and import check. Nothing lands.
- Overlap with Mission 5: T-2915 moves MASTER.md's module entries into docs/map shards. `regen` reads the entry
  through the same union helper, or whichever lands second adapts.
- Spend: the 27B first, at $0. Haiku only where it fails, inside the per-command cap.

## Lean
One verb that later becomes M-02's standing check. The slice script is a run of that verb, not a second code path.
No hook.

## Tier share
Brief 1 is tier 4: no harness regrows its own modules from intent as a check on how well that intent pins them.

## Hands to the next generation
The round-trip table per module. M-02's full build waits on M-18. The three ecology moons wait on their kill tests:
M-60 and M-61 are massive and get the cheapest kill next generation, and M-59's kill waits on T-2878's smith arm.

## Done when
T-2918's four criteria are green, the slice result and the M-02 stage (or its not-yet entry) are filed, the three
moons are in the catalogue and `sampo moons check` passes, and MASTER.md and CHANGELOG say it.
