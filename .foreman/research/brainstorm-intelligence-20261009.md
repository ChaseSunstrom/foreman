# Foreman intelligence catalogue (brainstorm 2026-10-09)

768 ideas from 15 lenses over 4 rounds plus 3 deepened categories, in 106 capabilities; every idea under exactly one capability. Build marks became T-0593..T-0667.

## I030 New specialist agents [Agent types and roles]
Adds roles such as interrogator, historian, integrator, reproducer, profiler, designer and release captain.
- mark: build — Add fm-reproducer (FIX: writes failing test/repro before any fix; feeds fm task prove) and an fm-profiler lens for PERF; skip the rest (historian is fm why/recall, closer/remediator overlap fm second). New agent files need user's plugin yes.
- status: partial; value 4/5; effort M; risk low
- evidence: 5 agents exist (builder, debugger T-0207, recon, reviewer, scout); audit.md has 5 lenses; fm oracle (T-0226) covers spec-first interrogation
- ideas: #218 Add an fm-closer agent for the done tail; #219 Add an fm-remediator that consumes audit findings; #348 Instrument first: add a tool-building agent before hard debugging; #349 Add an architect agent whose design ships with fitness functions; #383 Add an fm-interrogator agent for intake; #384 Add an fm-historian agent (Chesterton's fence); #385 Add an fm-integrator that owns lane seams; #534 Distil the project's human reviewers into audit lenses; #569 Add a shared-file steward agent; #570 Add an fm-reproducer agent for FIX tasks; #571 Add an fm-profiler agent for PERFORMANCE work; #572 Add an fm-designer reviewer lens for UI tasks; #573 Add a mid-task discovery triager; #574 Add a release-captain agent; #576 Dispatch stack-specialist builders from the project map

## I031 What agents hand back [Agent types and roles]
Has every agent return a typed noticed field, interview on exit, and log grievances.
- mark: build — Add a 'Noticed:' line to each agent's return format (agents/*.md) and have fm research add --from-agent extract it into fm capture --source discovered; skip interviews and values cards.
- status: partial; value 3/5; effort S; risk low
- evidence: fm-builder returns structured report; fm surprise logs expectation misses; fm research add saves agent output; no typed noticed field or yield table
- ideas: #221 Add a "noticed" channel to every agent's return; #225 Interview every sub-agent on exit; #387 Return a typed "noticed" field from every agent; #434 Keep an agent-handoff yield table: which sub-agent outputs the main thread used or threw away; #512 Brief children with a values card; #524 Keep a transactive-memory directory; #528 Wild: Keep a common-ground ledger per delegation; #575 Let agents file grievances against instructions

## I029 Roles as data with benches [Agent types and roles]
Defines each agent role as data, benches it, and compiles it per harness.
- mark: build — First step: fm bench case-type that runs one role (reviewer) on seeded diffs with known planted bugs and scores catch rate; reuse fm evolve to mutate that agent file.
- status: partial; value 3/5; effort M; risk low
- evidence: plugin/agents/*.md are 5 hand-written role files; fm bench/evolve (T-0212,T-0224,T-0280) bench plugin instruction files and routing.json is data, but no per-role bench
- ideas: #33 Define agent roles as data and bench each one; #175 Give each agent type a reasoning strategy, not only a role; #222 Compile role cards into per-harness agents with a conformance report; #227 Hire an agent by sentence; #386 Define agent roles as data with a per-role bench; #579 Wild: Audition agent configurations on a one-minute probe; #580 Wild: Exchange role cards with bench provenance; #581 Add a grader-of-graders for new roles

## I032 Overseeing agents [Agent types and roles]
Tracks role drift, delegation ROI and per-agent scorecards, and lets an ombudsman watch.
- mark: build — Per-agent-type scorecard in fm usage: spawns, tokens, findings confirmed vs false positive (from fm task audit results) and builder lanes merged vs discarded. Skip ombudsman, spokespersons, chronicler.
- status: partial; value 3/5; effort M; risk low
- evidence: fm budget records subagent tokens at SubagentStop; fm usage counts skill/command use; fm cost; no per-agent scorecard or verdict-fate join
- ideas: #223 Detect role drift in the ledger; #224 Keep a delegation ROI ledger and a spawn-or-not rule; #228 Give each module a spokesperson agent; #229 Hold a weekly staff meeting per role; #260 Keep a per-agent-type scorecard from verdicts and later fate; #388 Pair every builder with a rotating critic role; #577 Write a chronicler that narrates from raw events only; #578 Wild: Employ an ombudsman agent that works for the user against Foreman

## I033 Lane control in flight [Agent types and roles]
Lets any lane raise an andon or point of order and proceed on declared assumptions.
- mark: build — First step: builders write an 'andon' note file in the lane that fm lane list and fm next surface to the main thread (stop-and-ask with declared assumptions). Skip ghost owners and prediction duels.
- status: partial; value 3/5; effort M; risk med
- evidence: fm lane, fm run --parallel with relate groups/co-change footprints (T-0445); builders stop and report on guard block/3 failures per fm-builder.md; no mid-flight signal channel
- ideas: #38 Wild: Give hot files a ghost owner; #226 Pull an andon cord from any lane; #313 Let any lane raise a point of order mid-execution; #605 Wild: A "second pair of hands" that does the boring half of each step in parallel; #729 Wild: Run a pre-registered prediction duel between lanes

## I025 Know when to stop brainstorming [Brainstorming and ideation]
Detects saturation, maps coverage and feeds holes back into the next round.
- mark: build — Add a coverage map (cluster counts by capability axis, from the category tags ideas already carry) and a 'holes' pack line listing empty or thin categories fed to the next --rounds pass; reuse the existing category regex.
- status: partial; value 4/5; effort M; risk low
- evidence: lib/fmideas.py:263 --dry stops a round adding <N new; SKILL.md step 3 defines grounded-yield dry; --seen skips old ideas; no coverage map or holes brief
- ideas: #19 Stop brainstorming when novelty saturates; #210 Convert the idea pile into a coverage map by capability axis; #212 Cache brainstorm answers per lens so reruns only pay for new angles; #371 Mine the brainstorm's own ledger for saturation; #372 Feed prior-round gaps back as a "holes" brief; #561 Balance each round by horizon and require a stop-doing idea

## I026 Rank and triage ideas [Brainstorming and ideation]
Ranks by tournament, falsifies in one line, clusters duplicates and measures novelty.
- mark: build — First version: a tool-less 'kill it fast' child (via fmsecond-style _child) that gets each cluster's one-line claim and returns a one-line falsifier, stored beside the grounding; tournament and novelty score skipped as lower value than the falsifier.
- status: partial; value 4/5; effort M; risk low
- evidence: lib/fmideas.py _is_new word-overlap dedupe, nearest_done marks 'near T-' (fmrecall.py:180); SKILL step 4 clusters and scores by hand; no falsify pass or pairwise rank
- ideas: #17 Gate option sets on measured distinctness; #20 Rank ideas by pairwise tournament, not scores; #207 Cluster ideas into duplicates before showing them; #209 Measure idea novelty against the corpus with an embedding-free score; #211 Add a "kill it fast" triage pass that tries to falsify each idea in one line; #217 Tag each idea with its originating need so repeats collapse into needs; #353 Fake-door every idea before building it; #382 Detect when an idea is a rename of something already built; #533 Extract the shared primitives behind the idea pile

## I027 Learn which ideas the user keeps [Brainstorming and ideation]
Backtests the ideator and lenses against what the user kept and dropped.
- mark: build — Record each brainstorm catalogue's cluster->lens->mark, then on later turns join to briefs that were actually built/kept/dropped to produce per-lens keep rates in fm taste; use it to choose default lenses and --deepen. Needs the catalogue stored structurally (research add already holds it).
- status: partial; value 4/5; effort M; risk low
- evidence: fmideas.taste() / fm taste (fmideas.py:132) feeds kept/dropped/steered into packs; no per-lens hit-rate or backtest
- ideas: #21 Tune lens budgets from which ideas the user keeps; #86 Learn which brainstorm lens and round pays off; #214 Wild: Hold an idea-market where prior brainstorm rounds are scored by the user's later keeps; #264 Wild: Let rejected ideas come back to life when the world changes; #345 Backtest every idea against the ledger; #374 Brainstorm from the user's complaint log, not the project description; #556 Backtest the ideator on the project's own past

## I023 Reframe before ideating [Brainstorming and ideation]
Climbs the abstraction ladder, flips assumptions and distils insights as reframings.
- mark: build — First version: a 'flip assumptions' lens plus a 'reframe' lens added to fm ideas lenses and an assumption-flip bullet in R1 of intake/planning.md (Assumptions section already exists to flip).
- status: partial; value 3/5; effort S; risk low
- evidence: skills/intake/SKILL.md R1-R3 expand/anticipate; no abstraction-ladder or assumption-flip step
- ideas: #22 Climb the abstraction ladder at intake; #187 Run a reframing pass before approaches; #192 Distil insights as reframings, not facts; #557 Invent the lenses per project; #558 Flip every assumption in the brief

## I028 Wild idea generators [Brainstorming and ideation]
Provocations, cross-breeding, devil's ideas and persona-driven brainstorms.
- mark: build — First step: 3 extra optional lenses (oblique provocation from fm recall of past lessons and failures, devil's idea, worst-bugs persona) as prompt text only; cross-breeding as a final fm ideas round that combines top ideas. Cheap since lens infra exists.
- status: missing; value 3/5; effort S; risk low
- evidence: No provocation/cross-breed/persona lens in ideas-prompt.md or fmideas.py
- ideas: #25 Wild: Fire oblique provocations from the project's own history; #26 Wild: Cross-breed top ideas automatically; #27 Wild: Let a "devil's idea" argue for the opposite product; #213 Wild: Run an "ideas that would embarrass us" lens; #215 Wild: Brainstorm backwards from the user's next complaint; #216 Wild: Let ideas mate by incompatibility; #379 Wild: Let ideas carry a stake that decays unless someone defends them; #380 Wild: Brainstorm in a persona of the project's three worst past bugs; #565 Wild: Cross-pollinate with a sibling project's pack; #566 Wild: Draw three cards: capability × surface × user moment; #567 Wild: Dig up ideas from the graveyard on schedule

## I022 Route problems to ideation methods [Brainstorming and ideation]
Picks a named method (SCAMPER, TRIZ, HMW, JTBD, hats) for the problem at hand.
- mark: skip — Lenses already cover the angle diversity; SCAMPER/TRIZ/hats are re-labelings of lenses. If wanted, add 2-3 prompt lenses to ideas-prompt.md rather than a router.
- status: partial; value 2/5; effort S; risk low
- evidence: skills/brainstorm/SKILL.md step 3: fixed lenses (8 default) plus performance/security by request; no named methods
- ideas: #15 Route each problem to a named ideation method; #16 Fill a morphological box before listing approaches; #189 Brainstorm under oblique constraints; #205 Seed ideation with a constraint-inversion deck; #373 Run a SCAMPER pass on each shipped capability; #375 Add a "jobs to be done" reframing lens; #378 Run reverse brainstorming on every L plan; #559 Generate "How might we" questions before ideas; #560 Use TRIZ-style contradiction prompts; #562 Borrow from fields that already solved it; #563 Run a shortlist through fixed thinking hats

## I024 Blind rounds and divergent/convergent split [Brainstorming and ideation]
Runs independent first rounds, then informed rounds, with separate divergent and convergent agents.
- mark: skip — Round 1 is already blind per lens and --rounds adds informed rounds; the convergent split is the main-thread grounding step. Nothing material to add.
- status: partial; value 2/5; effort S; risk low
- evidence: lib/fmideas.py cmd_ideas: round 1 is lens-parallel and blind to siblings; later rounds (--rounds) see all; ideas-prompt is one divergent prompt, grading is in the main thread
- ideas: #18 Add a blind first round to `fm ideas`; #208 Run a blind-then-informed two-phase round; #377 Split divergent from convergent into separate agents with different temperatures; #564 Run the speed round against the slow round

## I101 Memory by activation and episode [Cognitive architecture and wild bets]
Recalls by activation, segments episodes, distils schemas and finds analogues across projects.
- mark: build — Add activation to recall: boost hits by recent touch of the same files and repeated failure signatures; keep schema distillation as a night job over lessons. Skip REM recombination and causal model.
- status: partial; value 3/5; effort M; risk low
- evidence: fmrecall.py BM25 recall with recency, stale-citation check, tripwires and failure signatures; fm share cross-project lessons
- ideas: #174 Build a causal model of the project from outcomes; #176 Distil episodic memory into reusable schemas; #333 Recall by activation, not text match; #340 Map problems by relational structure to find cross-project analogues; #343 Wild: Recombine distant memories in a night "REM" pass; #344 Wild: Detect "aha" moments and promote them instantly; #518 Warn on false-friend analogies; #523 Segment episodes at surprise boundaries for recall

## I105 Cognitive evaluation [Cognitive architecture and wild bets]
Audits Foreman against cognitive models and tests faculties by lesion.
- mark: build — Use fm evolve --drop to run lesion tests on each instruction file/skill (is it ever used, does bench drop without it) and report in fm usage; ties to fm usage's never-used list. Skip Common Model audit and K-lines.
- status: partial; value 3/5; effort M; risk low
- evidence: fm bench and fm evolve ablate instruction files against replayed tasks (T-0224)
- ideas: #529 Wild: Lesion one faculty at a time to find double dissociations; #712 Audit Foreman against the Common Model of Cognition; #714 Wild: Store mindset bundles as K-lines; #715 Wild: Ablate priming before committing to a plan

## I106 Dream-time and sleep simulation [Cognitive architecture and wild bets]
Counterfactual simulation, night passes and sleeping on problems.
- mark: build — Add a night job that replays the day's surprises/failed steps into a bench case or tripwire candidate (counterfactual: would the new rule have caught it). Skip sandboxed overnight plan dreaming.
- status: partial; value 3/5; effort M; risk med
- evidence: fm night (fmnight.py) runs budgeted background jobs: second read, landscape, court, evolve candidate
- ideas: #178 Wild: Let Foreman reason in a dream-time counterfactual simulator; #739 Wild: Dream the plan overnight in a sandbox and keep the survivors

## I103 Reflex, habit and inhibition [Cognitive architecture and wild bets]
Adds a reflex layer, arbitrates habit against deliberation, and logs suppressed urges.
- mark: skip — The guard and vetoes are the reflex layer already; an inhibition ledger and habit devaluation add little and touch the guard path.
- status: partial; value 2/5; effort M; risk med
- evidence: Guard (fmguard.py) is the reflex layer below the model; vetoes; drive ignores-hint decay (T-0262)
- ideas: #520 Monitor conflict at action time; #521 Add a reflex layer below the model; #522 Keep an inhibition ledger of suppressed urges; #527 Wild: Arbitrate habit against deliberation, with devaluation probes

## I102 Attention and global workspace [Cognitive architecture and wild bets]
Auctions context and drives attention from appraisal and one uncertainty currency.
- mark: skip — Hooks already cap and rank injected notes; an auction adds complexity and risk of dropping needed warnings. Wild pieces (attention schema, pandemonium) are low value.
- status: missing; value 2/5; effort L; risk med
- evidence: Context is injected by hooks (Next line, tripwires, vetoes) with fixed caps; no admission auction
- ideas: #334 Auction context admission through a global workspace; #341 Drive attention from an affect-like appraisal state; #342 Wild: Use one expected-uncertainty currency for every action choice; #706 Hold a sensemaking frame and count the anomalies against it; #713 Wild: Keep an attention schema; #717 Detect pandemonium: cheap demons shout over the event stream

## I104 Critic and selector layers [Cognitive architecture and wild bets]
Layers a critic–selector and a subgoal-on-impasse architecture over the ledger.
- mark: skip — fm next plus audits already form critic and selector; a separate layer duplicates them.
- status: partial; value 2/5; effort L; risk med
- evidence: fm next as selector over briefs; foreman:fm-reviewer critic; fm friction/evolve
- ideas: #335 Run a critic–selector layer over the ledger; #347 Run Foreman's methods on a small workflow runtime; #710 Build an environment affordance memory

## I054 Prove the diagnosis [Debugging and diagnosis]
Separates a working fix from a correct diagnosis using fix-removal and blind-guess probes.
- mark: build — Add fix-removal to fm task prove: stash the fix hunks in a scratch worktree, confirm the repro goes red, then green with them; record as evidence. Mostly reuses prove --hunks machinery.
- status: partial; value 4/5; effort S; risk low
- evidence: fm task prove --hunks (T-0271) mutation proof; fix-removal is its inverse, not a diagnosis check
- ideas: #119 Separate "the fix works" from "the diagnosis is right"; #232 Promote the probe that worked into the verify; #456 Separate "symptom gone" from "cause removed" with a fix-removal probe; #464 Verify the diagnosis independently with a fresh agent's blind guess; #649 Prove the diagnosis, not just the fix, with a fix-removal probe; #747 Prove the diagnosis with fix-removal and fix-isolation runs; #760 Prove the diagnosis with a fix-removal and blind-guess pair

## I055 Why was this not caught [Debugging and diagnosis]
Demands a finding and a guard or regression for every fix.
- mark: build — FIX tasks require a 'why not caught' line at finish plus a regression test or gate/guard action captured as a task. First step: gate in fm task finish for FIX type, text field and auto-capture of a follow-up.
- status: partial; value 4/5; effort S; risk low
- evidence: audit.md lenses; T-0417 product checks; lessons at fm task finish; no mandatory finding for FIX
- ideas: #112 Demand a "why did the test not catch this" finding on every FIX; #118 Wild: Post-mortem a misdiagnosis, not just a bug; #460 Auto-write the "why wasn't this caught" regression into the guard/gates; #650 Demand "why didn't anything catch this" on every FIX; #652 Wild: Run a misdiagnosis post-mortem when the second theory wins; #748 Turn every FIX into a "why wasn't this caught" action with an owner

## I050 Hypothesis tournament [Debugging and diagnosis]
Ranks hypotheses by cost-to-test, picks probes that split them, and escalates through a ladder when stuck.
- mark: build — Replace the flat 3-attempt block with an escalation ladder in fm next (repeat -> fm-debugger -> differential table -> block), keyed on hypothesis ledger state and failure frontier. First step: derive stuck state from attempts + hypotheses and emit the next rung.
- status: partial; value 4/5; effort M; risk low
- evidence: T-0207 ledger: fm task hypo with probe/status, fmcore.py:886 and next at :1713; agents/fm-debugger.md ranks with probes; flat 3-attempt block at execute.md:19
- ideas: #100 Choose the next debugging probe by how well it splits the hypotheses; #106 Run a differential-diagnosis table for FIX tasks; #182 Debug by posterior and discriminating probe; #231 Track the failure frontier, not just the failure count; #392 Rank hypotheses by cost-to-test over probability, not probability alone; #454 Require a discriminating probe before each hypothesis is ranked; #589 Blame a red criterion three ways before editing; #594 Find the pivot belief behind every failure; #646 Keep a hypothesis tournament with elimination evidence; #647 Replace the flat 3-attempt block with a diagnosis ladder; #648 Pick the next probe by hypothesis split; #745 Replace the 3-attempt block with an escalation ladder that changes mode; #746 Classify the stuck state from the attempt history

## I051 Locate the cause [Debugging and diagnosis]
Bisects commits, config and environment and compares passing and failing traces.
- mark: build — fm bisect: run the task's failing criterion over git history (git bisect run in a scratch worktree) and report the first bad commit plus the diff; env/config bisect later. First step: commit bisect only.
- status: partial; value 4/5; effort M; risk low
- evidence: fm-debugger suggests git bisect run (agents/fm-debugger.md:15); fm why; fm task start snapshot diff (T-0078); no fm bisect
- ideas: #107 Bisect the cause automatically, not just the regression; #113 Trace a bad value backwards through the ledger of runtime probes; #117 Wild: Run a "what changed since it last worked" detective across everything, not just git; #452 Bisect the environment, not just the commit; #455 Diagnose from the first divergence in a passing-vs-failing trace pair; #707 Localize FIX suspects by reference-frame voting; #750 Bisect across commits, config and environment in one search

## I052 Classify and fingerprint failures [Debugging and diagnosis]
Classifies failures, sorts flakes and indexes fingerprints and bug magnets across tasks.
- mark: build — Fingerprint failures (normalised error + test id) into a per-project index, linked to the task that fixed them; recall surfaces matches at FIX start, plus per-file bug-magnet counts from fm why/git. First step: fingerprint on red fm check and lookup in fm recall.
- status: partial; value 4/5; effort M; risk low
- evidence: fmcore.py:1848 note_flakes (rerun-to-classify); fm surprise (T-0253); fm recall; no fingerprint index or bug-magnet map
- ideas: #84 Keep per-project root-cause priors for FIX work; #108 Classify the failure before touching code; #109 Rerun-to-classify flakes with statistics; #110 Keep a symptom-to-cause casebook; #271 Fingerprint failures and look them up upstream; #453 Build a failure fingerprint index across tasks; #459 Maintain a per-file "bug magnet" map for FIX priors; #749 Build the failure fingerprint index and use it across projects; #755 Learn root-cause priors from finished FIX tasks and feed them back into case files

## I056 Debug case file and instruments [Debugging and diagnosis]
Unifies hypotheses, probes and evidence in a rerunnable case file with trusted instruments.
- mark: skip — Hypothesis ledger already is the case file; remaining parts (thrash detector, hunch lane) are minor. Fold thrash detection into the escalation ladder under 'Hypothesis tournament'.
- status: partial; value 3/5; effort M; risk low
- evidence: T-0207 hypotheses, probes, assumptions in brief; fm-debugger; thrash detection absent
- ideas: #114 Detect thrashing from edit patterns; #120 Require a check that tells interpretations apart; #190 Race a hunch lane against systematic debugging; #438 Wild: Run a "same bug twice" detector that prosecutes the earlier fix; #458 Verify the instrument before trusting its reading; #724 Keep investigations as re-runnable notebooks; #744 Run a debugging case file that unifies hypotheses, probes and evidence

## I053 Minimise and reproduce [Debugging and diagnosis]
Shrinks the failing input and builds a minimal or synthetic reproduction.
- mark: skip — Generic input minimisation needs project-specific tooling; synthetic twins are expensive. Lower value than bisect and fingerprints; revisit if bisect lands.
- status: missing; value 3/5; effort L; risk med
- evidence: no shrinker or synthetic repro command
- ideas: #111 Minimise the failing input before diagnosing; #116 Wild: Rebuild the bug in a minimal synthetic repo and hand it to a fresh agent; #121 Match the FIX repro to the reported symptom; #462 Wild: Grow a synthetic twin of the bug for blind retesting; #752 Wild: Grow a synthetic twin of the bug and test fixes on it blind

## I057 Wild debugging theatre [Debugging and diagnosis]
Cross-examines, freezes or duels over the bug.
- mark: skip — Role-play adds spend without evidence. The useful kernel, a duel of two committed root causes, is a lane-based variant of Hypothesis tournament.
- status: missing; value 2/5; effort M; risk low
- evidence: none; fm lane and fm-debugger exist for duelling
- ideas: #461 Wild: Interrogate the bug as a witness cross-exam; #463 Wild: Keep a "crime scene" snapshot that freezes everything at first failure; #651 Wild: Hold a crime-scene freeze at first failure; #751 Wild: Hold a cross-examination of the bug, where one agent plays the bug and another the investigator; #753 Wild: Freeze a crime-scene snapshot at first failure and let later agents replay it; #754 Wild: Run an adversarial "debug duel" where two debuggers must commit to different root causes

## I097 Dissent that survives [Deliberation and multi-agent thinking]
Keeps minority reports, dissent registers and what-we-did-not-discuss sections.
- mark: build — Save refuted/unresolved objections as a Dissent section in the brief and make fm task done list those still open. Small extension of fm second.
- status: partial; value 3/5; effort S; risk low
- evidence: fmsecond.py plan returns objections; debate CONFIRMED/REFUTED; no register carried to done
- ideas: #36 Preserve the minority report from agent panels; #146 Score disagreement as the escalation signal; #148 Make a dissent register that survives to done; #155 Require the judge to write a minority report; #503 Escalate by dissent shape, not count; #504 Give each panel a written "what we did not discuss" section

## I096 Panel design and roles [Deliberation and multi-agent thinking]
Fixes the panel's charter, roles and protocols as data, and sizes the panel by the stakes.
- mark: build — Make panel charters data: a protocols file naming roles, count and stop rule, sized by tier/risk, reused by fm ideas and fm second. First step: a size-by-stakes rule so S tasks skip panels and L get fm second plan automatically.
- status: partial; value 3/5; effort M; risk low
- evidence: fm ideas lenses (fmideas.py:18), fm second plan/debate/session (fmsecond.py), fm budget caps (T-0227); roles/protocols hard-coded, not data
- ideas: #144 Run a structured plan deliberation with fixed roles; #145 Hold a pre-registered vote before any tiebreak; #147 Assign each panelist a distinct failure to hunt; #151 Cap deliberation cost by stakes; #315 Pair the inside view with a base-rate view; #492 Elect a facilitator who may not vote; #493 Run a charter-first panel: agree the question before answering it; #494 Rotate roles between rounds; #495 Make the panel's output a decision record with a stop-loss; #496 Price a panel by the cost of being wrong, and skip it when cheap; #679 Seat jurors by voir dire; #684 Define deliberation protocols as data; #685 Stop seating panelists once the verdict is stable; #691 Keep standing boards with minutes

## I098 Evidence-bound debate [Deliberation and multi-agent thinking]
Requires probes and citations behind each claim, tracks flips, and settles conflicts between code, tests, docs and brief.
- mark: skip — DEBATE already demands cited evidence; argument graphs and steelman rounds add cost. Near-duplicate of Dissent that survives and Panel design.
- status: partial; value 3/5; effort S; risk low
- evidence: fmsecond.py DEBATE requires file:line per finding; fm audit prep; no argument graph
- ideas: #149 Run a steelman-then-attack debate on risky decisions; #306 Sort every disagreement by its cause, then route it; #307 Mine the interests behind each position; #308 Co-design the deciding experiment with adversarial collaboration; #309 Compute the verdict from an argument graph; #311 Audit every flip in a panelist's position; #497 Debate with evidence budgets: no claim without a probe result

## I099 Panel quality control [Deliberation and multi-agent thinking]
Detects groupthink, blinds and anonymises proposals, weights panelists by track record and credits arguments.
- mark: skip — Panels are 1-3 tool-less children; groupthink and calibration need volume Foreman does not have. Value 2.
- status: missing; value 2/5; effort M; risk low
- evidence: no panelist track record; fm second plan single reader
- ideas: #150 Calibrate panelists by how often they were right; #156 Detect groupthink between panelists; #312 Keep case law for panel rulings; #314 Credit panelists by marginal contribution; #498 Detect a panel that agrees too fast; #500 Wild: Run a two-model panel where each is blind to who the other is; #502 Score panelists by what happened after, and re-weight votes; #680 Anonymize and shuffle every proposal; #683 Assign credit to the argument that carried the verdict

## I100 Theatrical councils [Deliberation and multi-agent thinking]
Empty chairs, séances, gavels and speed-dating pair rounds.
- mark: skip — Theatre; no grounded benefit. Delphi/overnight adjourn covered by fm night.
- status: missing; value 1/5; effort M; risk low
- evidence: none
- ideas: #152 Wild: Seat a standing devil's advocate who is paid only for being right; #153 Wild: Convene the past-failure jury; #154 Wild: Let panelists trade a limited budget of probes; #316 Watch the council live and bang the gavel (wild); #317 Seat an empty chair for whoever isn't in the room (wild); #318 Draw a stranger juror from another field (wild); #319 Hold a Delphi rounds mode with a convergence stop (wild-ish); #499 Wild: Hold a séance with the superseded plan; #501 Wild: Let the lane that will do the work vote last, and cast a veto on infeasibility; #688 Adjourn unresolved disputes to an overnight experiment (wild); #689 Relay briefs through a telephone chain (wild); #690 Run speed-dating pair rounds before the full panel (wild)

## I067 One-way and two-way doors [Judgment, taste and decisions]
Classifies forks by reversibility and prices care by the cost of being wrong.
- mark: build — Make the existing decide kinds the door classifier: a line in execute.md saying classify each fork, spend a plan note/second read only on costly/outward, decide-and-log the reversible ones. Mostly a prompt rule on existing fields.
- status: partial; value 3/5; effort S; risk low
- evidence: fm decide --kind reversible|costly|outward (fmcli.py:1467) plus standard-autonomy approval for irreversible work (intake SKILL.md line ~29); no mid-task fork classification
- ideas: #34 Classify each mid-task fork as a one-way or two-way door; #69 Sort every fork into one-way and two-way doors; #248 Price each decision by cost of being wrong and spend care in proportion; #305 Add a doubt budget that scales with irreversibility; #414 Rank decisions by reversibility-weighted stakes before choosing how to decide; #667 Set every escalation threshold from a cost matrix

## I071 Notice decisions made by default [Judgment, taste and decisions]
Flags implicit decisions in diffs and defaults presented as choices.
- mark: build — First version: reviewer lens 'implicit decisions' in audit.md/fm-reviewer asking for each default taken (library, naming, schema, behaviour) with one line, recorded to brief; dumb-question cards skipped.
- status: missing; value 3/5; effort S; risk low
- evidence: Assumptions section in planning.md records assumptions with confidence but nothing flags defaults taken; no diff-level implicit decision detector
- ideas: #250 Record the default-versus-deliberate split in every plan; #419 Detect when Foreman is deciding by default and flag the choice as a choice; #595 Deal a dumb-question card at each phase change; #610 Surface the implicit decisions in every diff

## I072 Good enough and gold-plating [Judgment, taste and decisions]
Sets a bar at intake, argues against features, and guards against over-build.
- mark: build — Add a FEATURE-tier M/L step in intake: one tool-less fm second-style child argues the cheapest version meets the request, saved as a brief section; reuse fmsecond.plan with a different prompt.
- status: partial; value 3/5; effort S; risk low
- evidence: DONE-WHEN/SKIP intake lines, Non-goals section, ponytail-style rules, audit.md maintainer lens; no pre-build 'argue against this FEATURE' step
- ideas: #75 Argue against each FEATURE before it is built; #614 Audit nuisance controls for a quiet-until-it-matters threshold; #617 Re-rank audit findings by what this user acts on

## I075 Pre-answer the follow-ups [Judgment, taste and decisions]
Anticipates the next questions and complaints and answers them in the close-out.
- mark: build — First version: fm task finish --followups records the 3 likely questions with answers into the brief and digest, plus a one-line 'insight' field; R3 already produces the questions at plan time so reuse them.
- status: partial; value 3/5; effort S; risk low
- evidence: intake SKILL.md R3 Anticipate pre-mortem (three likely follow-ups); capture --source followup; no close-out pre-answer or insight line
- ideas: #130 Pre-write the user's next bug report (wild); #326 Pre-answer the likely follow-ups; #327 Make intelligence legible with one insight line per task

## I069 Precedent and case law [Judgment, taste and decisions]
Decides by citing the user's past rulings and their words.
- mark: build — First version: a precedence note in execute/planning (user words > vetoes > decisions > lessons) and have fm decide accept --cites pointing at the user message or decision it rests on; fm recall already retrieves the candidates.
- status: partial; value 3/5; effort M; risk low
- evidence: fm vetoes, fm taste, fm recall over decisions.md/lessons/research (fmrecall.py:53 _documents); bench court of user steers (fmnight.py court); no explicit precedence order or citation requirement
- ideas: #77 Order precedence between the user's words, vetoes, decisions, lessons and defaults, and show which one won; #246 Make every judgment call cite which of the user's words it rests on; #252 Run a tie-break protocol that falls back to the user's past resolutions; #415 Keep a precedent file of the user's past rulings, cited at decision time; #609 Route every fork through one judgment call; #721 Judge calls by case law

## I070 Taste model [Judgment, taste and decisions]
Learns taste from exemplars, overwrites and reference apps, separately from correctness.
- mark: build — First step: learn from overwrites by diffing agent commits against later user edits of the same lines (fm why/git blame has the pieces) into taste output; exemplar pinning as a brief field. Pairwise duels and visual taste skipped.
- status: partial; value 3/5; effort M; risk low
- evidence: fm taste (fmideas.py:132); fm bench judged cases use user preferences (CHANGELOG T-0280); no exemplar pinning or overwrite learning
- ideas: #78 Pin exemplar files as the taste reference for builders and reviewers; #79 Wild: Play a ten-second taste duel in idle moments; #245 Keep a taste exemplar set the user curates by ranking pairs of real diffs; #251 Audit "which taste call did this review comment represent" over time; #418 Score taste calls separately from correctness in reviews; #516 Wild: Defy the taste model on purpose; #612 Learn taste from the user's overwrites of agent code; #613 Promote taste inferences only after three unlike cases; #616 Arbitrate between the user's preference and the repo's convention; #702 Learn visual taste from reference apps

## I073 Back-test and regret [Judgment, taste and decisions]
Replays past decisions against what the user would choose and grades decisions apart from outcomes.
- mark: build — First step: join decisions.md rows to later reversals ([reverses:]/revisited tags) and user corrections to report a per-kind reversal rate in fm digest. Re-decision audits and spend-by-regret skipped until that data exists.
- status: partial; value 3/5; effort L; risk med
- evidence: fm bench replays finished tasks and court of user steers (fmbench/fmnight court); fm grades in digest; nothing grading decisions apart from outcomes
- ideas: #80 Wild: Hold a coin-flip re-decision audit; #134 Grade decisions apart from outcomes; #185 Spend deliberation by decision regret; #421 Run a "would the user have chosen this" back-test on past decisions; #422 Wild: Keep a "reasons ledger" where the user can strike a reason and watch decisions fall; #423 Wild: Offer a "swap chairs" replay that shows a decision as the user would have made it; #424 Wild: Grow a "regret tab" where the user taps one button on any shipped choice

## I068 Decision records [Judgment, taste and decisions]
Writes the rejected options, runner-up and what would change the decision.
- mark: skip — Rejected options, reversal and revisit triggers already ship; regret ledger and decision memo are covered by Back-test and regret if built at all.
- status: exists; value 2/5; effort S; risk low
- evidence: fm decide table has Decision, Why, Alternatives rejected, --reverses, --revisit trigger (fmcli.py:1467-1500, c.revisit_tag); fm vetoes
- ideas: #43 Pick the approach with a decision matrix that records the rejected options' kill reasons; #73 Write a regret ledger by comparing outcomes with the rejected options; #81 Wild: Keep a "road not taken" shelf; #82 Score approach choices by regret; #244 Write a decision-quality rubric the judge applies before any merge or approve; #417 Write a "decision memo" that fits on one screen for every ask; #420 Reopen a decision when the evidence behind it changes, with a one-line diff; #425 Require the loser's best argument in each plan's chosen-approach line; #611 Make every decision flippable with a prepared runner-up

## I074 Judgment oddities [Judgment, taste and decisions]
Gut-call scoring, apologies, conscience critics and judgment diaries.
- mark: skip — Mostly novelty; the useful part (surfacing the one call it is least sure of) is covered by Notice decisions made by default and fm decide --kind.
- status: missing; value 2/5; effort S; risk low
- evidence: No judgment diary, apology or gut-call scoring anywhere in skills or lib
- ideas: #254 Wild: Keep a "judgment diary" in which Foreman writes the one call it is least sure of each day; #255 Wild: Seat an "ex-user" persona built from the user's rejected ideas who vetoes new ones that resemble them; #618 Wild: Pre-write the apology before any one-way call; #619 Wild: Record a gut call before deliberating, and score it; #620 Wild: Seat a conscience critic who needs a user quote or stays silent

## I076 Outcome ledger [Learning from outcomes]
Joins every decision and plan step to its eventual fate, with delayed checks.
- mark: build — fm outcomes: join each done task with later events (reverts via git, reopened/follow-up tasks naming it, sentinel failures, fm smoke at +24h/+7d via fm night) and record fate; start with revert/follow-up detection from git and #T-ids.
- status: partial; value 4/5; effort M; risk low
- evidence: Ledger events + task_done data, fm bench replay diagnostics by stage (T-0220), fm sentinel re-runs finished checks, fm decide --revisit (T-0262); no decision-to-fate join or delayed post-merge checks
- ideas: #87 Score the brief's risks against what happened; #90 Wild: Interview the decisions, not the outcomes; #91 Wild: Keep scar tissue on the code; #92 Wild: Hold an outcome autopsy for near-misses; #256 Build an outcome ledger that joins every decision to its eventual fate; #257 Attribute each failure to a pipeline stage; #259 Hold delayed-feedback checkpoints on every closed task; #430 Run a post-merge reality check at 24h and 7d; #669 Score the brief's assumption confidences at close

## I077 Lesson lifecycle [Learning from outcomes]
Traces, tests, gates, minimises and retires lessons by measured benefit.
- mark: build — Give lessons stable ids, log when a recalled lesson is shown in fm focus, and flag lessons never recalled or followed by repeat failures (fm recall note_failure sig); then bench-gated retire via fm evolve. Skip tournaments, interference tests, confounder adjustment.
- status: partial; value 4/5; effort M; risk low
- evidence: Lessons are one-line prose in brief Lessons section, recalled by fmrecall.py and shared by fm share; no lesson ids, benefit measurement or retirement; fm evolve/bench could measure
- ideas: #263 Mine "first-time-right" tasks for what they had in common; #266 Wild: Run a "lessons tournament" where lessons compete on held-out tasks; #355 Minimise each lesson by cheap-model replay; #429 Trace each lesson to the failure it was born from and the failure it later prevented; #439 Gate lesson injection on measured benefit, per task type; #450 Wild: Give every lesson a footnote trail to the evidence that taught it; #519 Reconsolidate lessons when they're recalled; #525 Extract explicit rules from implicit outcome statistics; #526 Test new lessons for interference; #625 Adjust lesson-benefit estimates for confounders

## I080 Agent and pass yield [Learning from outcomes]
Tracks which passes, lenses and sub-agent outputs ever mattered.
- mark: build — Extend fm usage/digest with per-lens yield (findings confirmed vs false positives from recorded audits) and per-pass: second-read/oracle/brainstorm hits that changed the plan. Data already in ledger.
- status: partial; value 3/5; effort S; risk low
- evidence: fm usage reports commands/skills used and Next followed (T-0051); fm second exists; audit findings recorded per lens via fm task audit; no yield ranking of passes
- ideas: #85 Yield-rank the planning passes; #88 Track second-opinion yield; #136 Audit which deliberation passes ever change anything

## I081 Reflection and track record [Learning from outcomes]
Writes what it would do differently and a track record page it reads before claiming confidence.
- mark: build — Add a one-line 'would do differently' field to fm task finish (--lesson already exists, extend) and render a short track record (verified-first-time rate by type/tier) in fm digest and injected at fm focus for same type.
- status: partial; value 3/5; effort S; risk low
- evidence: foreman:reflect skill and task_done --lesson, fm digest (T-0071) weekly with grades; fm taste; no track-record page read before confidence claims
- ideas: #265 Wild: Keep a "Foreman's track record" page that the model reads before claiming confidence; #267 Wild: Write a one-line "what I'd do differently" at every task close and aggregate them weekly; #436 Wild: Give Foreman a seasonal report card written to its future self

## I078 Self-regression and eval hygiene [Learning from outcomes]
Attributes Foreman's own regressions, retires weak evals and audits rules.
- mark: build — First step: fm bench report listing cases that pass/fail identically across all plugin versions (non-discriminating) and propose dropping them; reuse bench result history. Skip island models and bounties.
- status: partial; value 3/5; effort M; risk low
- evidence: fm evolve is bench-gated with change per generation, fm bench duel/compare, fm sentinel; no bisect of outcome regressions or non-discriminating case retirement
- ideas: #623 Keep self-changes attributable with a change budget and washout windows; #627 Bisect Foreman's own outcome regressions to the commit; #628 Estimate pass probability of finished tasks by resampling; #629 Retire eval cases that don't discriminate; #630 Wild: Run an island model for instruction variants across projects; #631 Wild: Post bounties for recurring failure patterns; #632 Wild: Hold a "did that even matter?" audit of Foreman's own rules

## I079 Counterfactual and hindsight learning [Learning from outcomes]
Replays what would have happened and relabels failed attempts.
- mark: build — Cheapest step: fm tidy/next reopens blocked tasks when a task they depend on (#T-id) or a file named in the block reason changes (reuse decide --revisit triggers); wrong-turn registry from reverted commits feeds fm recall.
- status: partial; value 3/5; effort M; risk low
- evidence: fm bench replays finished tasks with candidate plugin; steering-as-data (T-0264) stores user corrections; decide --revisit exists; blocked tasks not auto-reopened
- ideas: #89 Reopen blocked tasks when the world learns something; #258 Run a counterfactual replay to see whether a pass or agent mattered; #431 Classify each user correction by the stage that should have caught it; #432 Add a wrong-turn registry mined from reverted commits and abandoned lanes; #435 Wild: Hold a replayed "what-if I'd listened" for every ignored warning

## I082 Process mining [Learning from outcomes]
Discovers the workflow Foreman really follows, mines smooth and failed tasks, and learns learning curves and give-up points.
- mark: build — First step: fm friction extension that mines the ledger for stage-transition sequences and flags smooth-but-unverified tasks (few events, weak grade) and common give-up points (blocks after N failures). Skip learning curves until more data.
- status: missing; value 3/5; effort M; risk low
- evidence: No ledger process-mining; fm usage/friction/cost count events but nothing discovers workflow or learning curves
- ideas: #296 Alarm on suspiciously smooth tasks; #539 Process-mine the ledger for the workflow Foreman actually follows; #582 Track what Foreman actually saw; #624 Count the outcomes the ledger never saw; #709 Fit learning curves per task class and act on plateaus

## I090 Calibrate confidence [Metacognition and calibration]
Scores forecasts and confidence per axis and tag against outcomes.
- mark: build — Record confidence number with each assumption/plan; at finish, score vs outcome (reopened, review findings, bench) into a calibration table in fm digest. Start with one axis.
- status: partial; value 4/5; effort M; risk low
- evidence: Assumptions tagged assumed/verified/false (T-0254); verification grades in fm digest; no confidence-vs-outcome scoring
- ideas: #45 Calibrate stated confidence against outcomes; #104 Calibrate predictions to earn reading budget (wild); #133 Score every forecast and feed it back into thresholds; #294 Split confidence into four separate axes; #295 Make confidence trigger falsification in proportion; #301 Refit calibration on every model change; #485 Calibrate each epistemic tag against outcomes; #668 Forecast in 80% intervals and score coverage

## I093 Competence atlas and self-model [Metacognition and calibration]
Maps where Foreman is weak and predicts its own failure modes.
- mark: build — fm atlas-like report from bench + review findings + reopened tasks, grouped by tag/file area/language, feeding fm next caution hints and the friction pass. Start by aggregating existing grades by area.
- status: partial; value 4/5; effort M; risk low
- evidence: fm bench (fmbench.py) replays finished tasks; fm friction; fm taste; fm usage; no per-area weakness map
- ideas: #137 Build a competence atlas of where Foreman is weak; #179 Wild: Keep a self-model that predicts Foreman's own failure modes; #338 Run a cognitive battery of faculty micro-evals; #670 Scale caution by distance from experience; #675 Seed calibration on a new repo from its git history

## I094 Honest close-outs [Metacognition and calibration]
Detects hindsight rewriting, confidence laundering and suspiciously smooth results, and diagnoses each escape as a monitoring, control or knowledge failure.
- mark: build — Finish lint: compare final criteria text to the one at approval (hash in Log) and flag edits; flag all-green with zero red runs ever as 'suspiciously smooth'. First step is the AC diff check.
- status: partial; value 3/5; effort M; risk low
- evidence: fm task finish requires --audit/--lens; verification grades; fm second debate; no hindsight-rewrite or smooth-result detection
- ideas: #300 Detect hindsight rewriting in close-outs; #394 Write the "what I did not consider" section last, from the diff; #478 Sample ground-truth audits to unbias calibration labels; #486 Diagnose each escape as a monitoring, control or knowledge failure; #672 Audit stopping rules for early and late closure

## I092 Know when to ask or pause [Metacognition and calibration]
Sets ask thresholds from cost and learns when to check.
- mark: skip — Full autonomy deliberately never asks; learning thresholds has no signal beyond decisions.md. Near-dup of Calibrate confidence.
- status: partial; value 3/5; effort M; risk low
- evidence: fm decide, autonomy full self-decides; fm ask categories; fm surprise; no ask-threshold learning
- ideas: #400 Track which kinds of questions Foreman answers from memory instead of checking; #481 Abstention bench with an ask-threshold curve; #483 Learn when to pause and check; #673 Break classification ties with evidence before asking

## I091 Infer confidence from behaviour [Metacognition and calibration]
Reads confidence from tells, trajectories and inflation instead of words.
- mark: skip — Needs a labelled corpus of failures first; the calibration table (Calibrate confidence) is the stronger base. Revisit after it has data.
- status: missing; value 3/5; effort L; risk low
- evidence: no tell mining; events logged in ledger could feed it
- ideas: #140 Lint certainty language against evidence strength; #299 Track confidence laundering across handoffs; #479 Estimate confidence from behaviour, not words; #480 Mine the empirical tells that precede failures; #482 Propagate confidence along task chains; #484 Detect confidence-trajectory shapes mid-task; #487 Measure in-session confidence inflation

## I095 Self-testing for sycophancy and credulity [Metacognition and calibration]
Plants poisoned lessons and false corrections, runs bets and sure-and-wrong journals to expose its own weak spots.
- mark: skip — Sealed-ground-truth judge testing overlaps fm bench judged and fm evolve; planting poison in live lessons risks corrupting memory. Fold one bench case 'false correction' into bench if wanted.
- status: missing; value 3/5; effort L; risk med
- evidence: fm bench judged cases (fmbench.py:127) and fm evolve exist; no poisoned-lesson or false-correction injection
- ideas: #302 Wild: Make the user and Foreman bet on outcomes; #303 Wild: Re-derive each L decision cold the next morning; #304 Wild: Keep a journal of "I was sure and wrong" moments; #488 Wild: Probe reviewers for authority bias; #489 Wild: Plant a poisoned lesson to test memory credulity; #490 Wild: Inject a false user correction to test sycophancy; #491 Wild: Show calibration health in the statusline; #676 Wild: Hunt overconfidence overnight; #677 Wild: Draw a random blind-spot card; #678 Wild: Keep a "sure and wrong" journal that shapes the prompt; #692 Test the judge with sealed ground truth (wild)

## I011 Replan on surprise [Planning and decomposition]
Re-plans in rolling waves, at checkpoints and on steers, keeping a revision history.
- mark: build — When fm surprise or a failed assumption verify is logged on an active M/L task, fm next injects 'replan: re-read Steps/Execution prompt' once and logs a plan revision line in the brief.
- status: partial; value 4/5; effort M; risk low
- evidence: skills/next/SKILL.md:10 and execute.md:31 re-plan after phase groups; fm surprise (T-0261) logs misses; no trigger from a surprise to a replan
- ideas: #5 Plan in rolling waves with versioned replans; #28 Re-plan mid-flight when a surprise lands; #57 Re-plan at checkpoints, not only on failure; #171 Replan on evidence, with a plan-revision history; #363 Rebase the plan on a mid-task steer; #396 Re-read the brief after the third step, not just at the end; #532 Reroute from the acceptance criterion when a step blocks; #736 Checkpoint a plan with a surprise budget

## I013 Stress-test the plan before running [Planning and decomposition]
Attacks the plan with pre-mortems, naive readers, tabletop runs, courts and fuzzing before any edit.
- mark: build — Extend fm second plan with selectable roles (pre-mortem, naive reader, plan court prosecutor/defender) as extra prompt variants for L plans; reuse the child_cmd and budget path. Skip personas with memory and throwaway-copy rehearsal.
- status: partial; value 4/5; effort M; risk low
- evidence: fm second plan (fmsecond.py:59, another model reads the plan, L tier); R3 anticipate in planning.md; rubric self-critique
- ideas: #12 Write the plan to fail, then invert it; #23 Replay a plan under forced constraints; #31 Table-read the plan with a naive agent; #32 Run a simplifier against every L plan; #39 Wild: Hold a pre-mortem with a cast of the task's likely failures; #42 Run a premise check before planning; #49 Wild: Play out the plan in a "tabletop" before touching files; #64 Wild: Run the plan as a rehearsal on a throwaway copy first; #105 Rehearse the plan with the repo's past authors (wild); #143 Reread each L plan with its rationale stripped; #173 Add a Socratic problem-framing pass before decomposition; #177 Wild: Hold an inner council with persistent personas that argue the plan; #186 Let the user challenge one node of the plan; #202 Fuzz the plan against its request (wild); #535 Wild: Drill a six-month-later maintainer on each L diff; #727 Wild: Keep the user's nightmare list as a standing exam; #730 Wild: Let Foreman explain its plan to a skeptic who may only ask "so what?"; #734 Hold a plan court with a prosecutor and a defender; #737 Offer the user a plan counter-proposal at the one risky node; #740 Wild: Cast the plan as a debate between persistent personas with memory

## I010 Order steps by risk and information [Planning and decomposition]
Puts the riskiest or most informative steps first and schedules slow or human-dependent ones early.
- mark: build — Add a rubric line to planning.md R2 and a brief Steps lint: spikes/unknowns/human-dependent steps first, reversible before irreversible. Pure instruction text, no code.
- status: partial; value 3/5; effort S; risk low
- evidence: references/planning.md has tiers/R2 but no step-ordering rule; fm queue orders tasks only; T-0364 hides latency
- ideas: #2 Sequence plans riskiest-unknown first; #41 Decompose by risk-first spike ordering; #58 Order steps by information value (riskiest first); #70 Order plan steps by uncertainty removed per cost; #181 Plan the investigation by value of information; #547 Order plan steps by reversibility and rehearse the rollback; #548 Sequence human-dependent decisions before the unattended stretch; #549 Hide latency by scheduling slow steps first

## I012 Decomposition recipes and seams [Planning and decomposition]
Splits work by named recipes, oracles, tests, cost of seams and commit-sized steps.
- mark: build — Add a decomposition-recipes reference (expand/migrate/contract, test ladder, walking skeleton, one observable per step) linked from planning.md; later lint step granularity. Skip the co-change seam cutter, already T-0445.
- status: partial; value 3/5; effort S; risk low
- evidence: fm relate and fm run footprints (T-0445) cover cross-task seams; planning.md has no recipes; oracle (T-0226) covers examples
- ideas: #6 Decompose along oracle availability; #7 Trace plan steps to criteria; #9 Ship a library of named decomposition recipes; #10 Cut lane seams with the co-change graph; #14 Plan tasks by their ending; #195 Plan in cut-line tiers; #197 Plan as a test ladder; #199 Decompose RESEARCH into a question tree; #367 Design once, derive the cluster's tasks; #370 Wild: Slice features along a storyboard; #543 Plan breaking changes as expand, migrate, contract; #555 Split any step whose commit message needs "and"; #583 Escalate patch trains to a design pass; #597 Lint steps for single-observable granularity at plan time; #726 Score decomposition by what the seams cost

## I020 Spike and skeleton first [Planning and decomposition]
Builds a walking skeleton, throwaway spike or empty-commit skeleton before the real plan.
- mark: build — Add a walking-skeleton rule for FEATURE L (first step: thinnest end-to-end path with a failing acceptance test) and a throwaway-spike step type to planning.md. Skip empty-commit skeletons and simulators.
- status: missing; value 3/5; effort S; risk low
- evidence: No spike/skeleton guidance in planning.md or execute.md; T-0445 unrelated
- ideas: #8 Build a walking skeleton first on FEATURE L; #11 Test decomposition on a cold cheap model; #368 Wild: Build one to throw away, then plan; #369 Wild: Make the plan a skeleton of empty git commits; #536 Wild: Settle design arguments with a throwaway simulator; #728 Wild: Turn the top brainstorm ideas into watchable spikes

## I021 Planned obligations and safe ends [Planning and decomposition]
Makes cleanup, rollback and breaking-change phases explicit plan items, and plans by the ending.
- mark: build — Planning rubric adds: every FIX has contain/cure/inoculate steps, every migration has a cleanup/rollback step; fm next warns at finish if rollback section empty on L.
- status: partial; value 3/5; effort S; risk low
- evidence: Briefs have Risks and rollback section; FIX staged flow is in debugging.md; cleanup not a plan item
- ideas: #358 Derive plan steps from the breakage; #360 Stage every FIX as contain, cure, inoculate; #738 Ensure cleanup is a planned obligation

## I015 Bind plans to assumptions [Planning and decomposition]
Ties steps to assumptions and beliefs so only dependent steps are invalidated when one breaks.
- mark: build — Let steps cite assumption numbers; when an assumption goes [false], fm next names the steps that cite it for re-check. Known-unknowns ledger is the same list.
- status: partial; value 3/5; effort M; risk low
- evidence: fm task assume add|verify (T-0261) tags assumptions; stale_refs (fmcore.py:2461) flags vanished paths; no step-to-assumption link
- ideas: #93 Open a known-unknowns ledger before planning; #194 Mark plans stale when their footprint changes; #366 Score plans by how much reality rewrote them; #545 Bind steps to assumptions and invalidate only their dependents; #584 Rank assumptions by plan sensitivity and bind them to steps; #719 Invalidate plans by belief dependency

## I016 Size and estimate plans [Planning and decomposition]
Estimates steps, effort and footprint from measured history and Monte Carlo.
- mark: build — Trip a re-frame note in fm next when on-task time passes 2x the typical median, and record planned scope vs real changed files at finish for a correction factor. Skip Monte Carlo and working-memory span.
- status: partial; value 3/5; effort M; risk low
- evidence: T-0116 typical minutes per type/size in fm ui; fm cost; fm batch T-0257; no trip on overrun, no footprint calibration
- ideas: #138 Trip a re-frame when effort passes the estimate; #196 Calibrate step size from history; #200 Size the plan from measurements; #238 Trip on step size, not only on time; #261 Learn the real cost of each plan step type; #339 Measure working-memory span and size plans to fit; #350 Learn step size per task type; #356 Track a thinking clock per phase and learn the ratio that predicts first-pass success; #364 Run Monte Carlo over the step graph; #433 Compare a planned footprint with the real one, and learn the correction factor; #544 Plan on a critical chain with one shared buffer

## I019 Plan from history [Planning and decomposition]
Reuses a pattern library, scores plans and templates against replayed outcomes and spots novel problem classes.
- mark: build — Record per-step outcomes at finish (steps added late, steps that failed) and have fm recall surface 'steps similar plans forgot' for the new brief. Falsifiable plan predictions graded at finish piggyback on it.
- status: partial; value 3/5; effort M; risk low
- evidence: fmrecall.py recalls briefs/lessons by BM25 (fm recall); fm bench replays finished tasks; no step-outcome table
- ideas: #3 Learn the steps plans forget; #24 Keep a pattern library that plans can cite; #427 Join plan steps to their fates in a step-level outcome table; #428 Make plan templates earn their place by outcome; #733 Score plans against replayed history; #742 Detect when a plan's problem-class is novel and escalate effort; #743 Write plans as falsifiable predictions and grade them at finish

## I014 Plan as a graph or compiled object [Planning and decomposition]
Treats the plan as a living graph with conditions, named passes and live prediction of file changes.
- mark: build — First step: optional 'requires/produces' notes per step and an fm task step lint that flags steps whose postcondition already holds (cheap git/file check). Full living graph and timeline UI are wild; skip.
- status: missing; value 3/5; effort L; risk med
- evidence: Steps are a flat list in the brief; fm relate only orders tasks; no step pre/postconditions
- ideas: #55 Compile the plan into a step graph with pre/postconditions; #193 Ground every plan against the repo; #198 Run optimiser passes over the plan; #201 Check declared step order against the real dependency graph; #203 Fold plans like origami (wild); #204 Draw the plan as a fog-of-war map (wild); #359 Prune steps whose postcondition already holds; #537 Show a what-if view when a brief is edited; #553 Predict the file tree after every step and diff it live; #731 Unify the plan as one living graph object; #732 Run a plan compiler with named passes; #741 Wild: Let the plan be a playable timeline the user can scrub

## I017 Plan the queue and lanes [Planning and decomposition]
Orders and fuses queued tasks, shares prefixes and keeps parallel lanes apart.
- mark: skip — Mostly shipped (T-0445 footprints, T-0257 batching, relate). Remaining ideas (salvage failed lane hunks, remainder carry) are low value over what exists.
- status: exists; value 2/5; effort M; risk low
- evidence: fm relate (order and group), fm run --parallel with relate groups and co-change footprints (T-0445), fm batch (T-0257), fm lane
- ideas: #1 Hoist shared prerequisites across the queue; #220 Let lanes proceed on a declared assumption; #351 Find queued tasks that obsolete or undo each other; #361 Carry the remainder of every scoped-down task; #365 Start the common prefix while plans compete; #531 Plan the shared prefix of rival interpretations; #538 Salvage a failed lane's hunks for other queued tasks; #542 Assign every single-writer artifact to one owning step; #550 Fuse small queued tasks that share a footprint; #701 Steer the queue by theme budget; #735 Forecast the plan's blast radius from co-change history

## I018 Compete and sample plans [Planning and decomposition]
Generates several plans, compares by disagreement, Pareto front or search value, and races a lazy baseline.
- mark: skip — Sampling several plans per M/L task multiplies spend for modest gain; near-duplicate of the stress-test capability (fm second plan variants) which is stronger and cheaper.
- status: partial; value 2/5; effort M; risk med
- evidence: fm second plan is one alternative model; fm ideas runs lens children; no plan sampling
- ideas: #4 Give every M/L plan a pivot table; #13 Run planning poker across agent roles; #172 Search over approaches with a value function; #352 Show the Pareto front of plans for L tasks; #517 Plan by recognition before enumeration; #546 Sample several plans and use their disagreement as the risk map; #551 Relax the task, then restore constraints one by one; #552 Plan from both ends and treat the gap as the unknown work; #554 Write a plan by exquisite corpse across agent roles; #681 Negotiate the plan as tracked changes; #725 Race a lazy baseline against the plan

## I039 Stuck ladder [Reasoning and thought process]
Replaces a flat three-attempt block with a ladder that classifies the stall and changes mode.
- mark: build — fm next on 2 failed attempts on a step: classify the stall from evidence lines (same error, new errors, no progress, env) and name the mode: fm-debugger, smallest-next-step, re-read spec/oracle, or block. Stall-aware ladder in fmcore next logic and execute.md.
- status: partial; value 5/5; effort M; risk low
- evidence: execute.md:19 flat 3-attempt block; fm-debugger agent; fm task hypo; debugging.md phase 4 fresh eyes
- ideas: #37 Wild: Wake a lateral-thinking squad when a task is stuck; #60 Run a "stuck ladder" instead of a flat 3-attempt block; #62 Add a "smallest next step" mode for bogged-down tasks; #397 Wild: Let Foreman "sleep on" a stuck problem and return with a different framing; #457 Keep a stuck-state classifier that picks the debugging mode; #590 Require a re-representation before the third attempt; #607 Classify each stall by type and switch the move; #626 Learn the give-up point from attempt curves

## I037 Catch reasoning biases [Reasoning and thought process]
Reviews its own transcript and stated reasons for bias, sunk cost and silent question changes.
- mark: build — Add a 'devil' lens to fm second plan: a tool-less child must argue for the rejected approach options and flag steps that change the question vs the request nouns; run before approval on M/L, flagged in Plan review.
- status: partial; value 4/5; effort M; risk low
- evidence: fm second plan (T-0276) critiques plans; audit.md lenses (intent, adversary); drive 3-attempt block
- ideas: #29 Watch reasoning for known biases; #44 Replace the third failed attempt with a structured "what do I now know" reset; #46 Add a devil's-advocate pass that must argue for the rejected option; #48 Wild: Hold an inner monologue review where a cheap model reads the transcript for reasoning errors; #72 Detect sunk cost and replan fresh at half budget; #298 Test whether stated reasons are the real reasons; #393 Detect when a plan step silently changes the question; #602 Add a mid-step "am I still on the task" tripwire based on the brief's nouns; #708 Detect action slips against the step's declared intent

## I035 Working memory and case file [Reasoning and thought process]
Keeps a typed scratchpad per task that survives compaction and a live view of the current question.
- mark: build — Add a typed 'Notes' (facts/open questions) section to the brief that fm checkpoint and fm resume print, with fm task note ID add; reuses the brief store, no new store.
- status: partial; value 3/5; effort S; risk low
- evidence: fm checkpoint/Resume here, fm task hypo/assume, fm resume; brief sections survive compaction
- ideas: #35 Keep a working-memory scribe through long tasks; #47 Reason in a scratch ledger that survives compaction; #59 Keep a per-step working set, and flush it at boundaries; #169 Keep a typed working-memory scratchpad per task; #337 Snapshot situation awareness at step boundaries; #346 Keep one case file per task that every thinking pass writes into; #354 Show the live mind: an editable board of the current question, hypotheses and bets

## I036 Belief and hypothesis board [Reasoning and thought process]
Holds falsifiable beliefs, known unknowns and epistemic tags with kill criteria.
- mark: build — Extend assume with kill criteria and 'changes my mind if' fields on Approach options and surface open ones in fm next; assume/hypo already do the rest.
- status: partial; value 3/5; effort S; risk low
- evidence: fm task assume ([assumed]/[verified]/[false], T-0261), fm task hypo with probes, fm surprise
- ideas: #40 Keep a falsifiable-belief board per task; #50 Wild: Keep a "what would change my mind" line on every decision; #63 Write a "why not" line for every rejected approach and test it later; #96 Tag every claim with its epistemic status; #125 Type every claim and require its proof shape; #183 Give every approach kill-criteria; #297 Triage every unknown as know, find out, or ask; #591 Keep a units-and-frames register for each task; #671 Mark beliefs as observed, inferred or carried over from a summary across compaction

## I038 Blind second opinions [Reasoning and thought process]
Gets independent opinions from readers who see only the claim or question.
- mark: skip — fm second plan already gives another model's read and fm oracle is spec-blind; a claim-only mode is a flag at most. Covered by fm second.
- status: exists; value 3/5; effort S; risk low
- evidence: fm second plan/debate/session (fmsecond.py:59,78,127); fm bench oracle (fm oracle) sees spec only
- ideas: #54 Wild: Let a second Foreman argue the user's side of every steer; #115 Wild: Keep a rubber-duck cross-examiner that asks the builder "what would you bet this isn't?"; #168 Wild: Let Foreman argue the user's side in its own plan review; #391 Make the second opinion see only the question, not the answer; #398 Wild: Keep a "tell me I'm wrong" agent that only reads the claim, never the work

## I034 Named reasoning moves [Reasoning and thought process]
Chooses and names a reasoning move or problem-solving heuristic before non-trivial steps.
- mark: skip — Prompt-level ritual with unmeasurable effect; fm next + intake tiers already route procedures. Stronger: Stuck ladder.
- status: partial; value 2/5; effort M; risk low
- evidence: fm next names stage skills (T-0205); debugging.md phases; no move-naming/routing by difficulty
- ideas: #51 Classify the kind of difficulty and pick the agent mix from it; #53 Learn which reasoning moves worked per task type; #99 Route tasks to a named problem-solving method; #184 Select a named problem-solving heuristic when stuck; #332 Resolve impasses with typed subgoals, then chunk the result; #336 Route by a feeling-of-knowing probe; #390 Name the reasoning move before each non-trivial step

## I040 Comprehension before action [Reasoning and thought process]
Requires teach-back, quizzes and neighbour-reading before editing unfamiliar code.
- mark: skip — Teach-back is token cost with no gate to check it; the real wins are fm why/recall already offered at R2. Near-duplicate of Chesterton check in Domain pitfall packs.
- status: partial; value 2/5; effort M; risk low
- evidence: fm why FILE:LINE, fm outline, fm map, fm impact give the means; none required before edit
- ideas: #52 Separate "understood" from "done" with a comprehension check before editing; #141 Give Foreman a blind self-grading exam; #142 Require a teach-back before editing unfamiliar code; #188 Quiz Foreman on each subsystem and keep a scored model card; #403 Insert a read-the-neighbours step before every edit of unfamiliar code

## I042 Value-of-information search [Reasoning and thought process]
Chooses approaches and probes by information gained and kills approaches by criteria.
- mark: skip — Marginal-information metering has no reliable signal; weak versus Question-first research memo, which covers the stop rule.
- status: partial; value 2/5; effort M; risk low
- evidence: fm second plan, fm oracle, approach options in planning.md; research ask stops by sub-questions
- ideas: #94 Settle approaches with discriminating experiments; #101 Stop researching when the decision stops moving; #135 Meter marginal information and stop research when it dries up; #191 Model-check L designs before coding

## I041 Thinking as an artifact [Reasoning and thought process]
Makes reasoning replayable, forkable, narrated or shared with the user.
- mark: skip — Replay/fork of reasoning has no hook to capture thinking; ledger + decisions already record the visible trail. Wild but no grounded first step beyond what exists.
- status: partial; value 2/5; effort L; risk low
- evidence: ledger events, decisions.md, fm tour, fm task log
- ideas: #66 Wild: Keep a "breadcrumb trail" so any step can be reverted and replayed with a different choice; #180 Wild: Make thinking itself a replayable, forkable artifact; #399 Wild: Play the task backwards as a children's "how did we get here" story; #603 Wild: Make the executor narrate its next move in the ledger before acting, then grade the narration; #718 Wild: Run a narrator stream the main model can query; #723 Think with me: `fm think` partner mode

## I085 Dependency truth [Research and knowledge]
Closes the knowledge-cutoff gap by probing installed dependencies, release notes and upstream.
- mark: build — fm deps --calls: for each package behind, grep the project's call sites of imported names and attach release-note questions; plus a hook-free 'fm probe' note in intake that checks the installed version's source/--help before trusting docs. Start with installed version vs latest and import-site listing.
- status: partial; value 5/5; effort M; risk low
- evidence: fm deps (major-behind + migration question, fmoutside), context7 in intake R2; no installed-version probe or call-site mapping
- ideas: #268 Compile research claims into probes; #269 Detect the knowledge-cutoff gap; #272 Map release notes onto call sites; #444 Detect a stale-knowledge hazard before using a library API; #636 Check the installed dependency's behaviour with a throwaway probe before trusting docs; #644 Detect the knowledge-cutoff gap on API use and force a look-up

## I083 Question-first research [Research and knowledge]
Builds a question tree before reading, stops when the decision stops moving, and ends in a memo saying what would change it.
- mark: build — Make fm research ask end its note with a Decision section: recommendation plus 'would change if' lines, from the same child call; tie to the RESEARCH task finish.
- status: partial; value 4/5; effort S; risk low
- evidence: fm research ask splits sub-questions, recall first, quorum (T-0206, T-0277); no decision memo with 'what would change this'
- ideas: #443 Run a research-to-decision memo pipeline with a recommendation and an explicit "what would change it"; #634 Build a question-first research plan before any reading; #637 Run a "what is this question really asking" literature pass for RESEARCH asks that names prior art; #639 Ask the research question twice from two framings and diff the answers; #643 Write a decision memo with "what would change this" from each research pass

## I089 Domain pitfall packs [Research and knowledge]
Collects pitfalls per domain and runs reference-frame voting.
- mark: build — Chesterton gate as a CLEAN-type step: fm next on a task that deletes files or lines runs fm why on them and requires one line of origin per deletion in the brief (warning, not a hard block). Pitfall packs skipped.
- status: partial; value 4/5; effort S; risk low
- evidence: fm why FILE:LINE (commits+lessons behind code), audit.md maintainer lens, lessons via fm recall
- ideas: #30 Ask the historian before deleting or refactoring; #71 Run a Chesterton's-fence check before any deletion; #95 Block deletion until the fence's origin is found (Chesterton gate); #98 Accumulate domain pitfall packs

## I086 Prior art [Research and knowledge]
Searches the user's repos and the market before building.
- mark: build — fm recall --repos: grep/ripgrep other registered projects (fm projects) for the request's identifiers and titles, local read-only, redact per share rules; cite file:line. FEATURE L intake lists hits in Approach.
- status: partial; value 4/5; effort M; risk med
- evidence: fm recall (project) and fm share cross-project lessons (fmrecall.py:420); no search of user's other repos for code
- ideas: #270 Search the user's own repos for prior art; #276 Compare prior art for FEATURE L; #445 Maintain a cross-project "how I solved X before" index across the user's repos; #451 Compare tools in the space before building a FEATURE L; #642 Wild: Interview the user's own repos for prior solutions before researching outward

## I087 Project knowledge base [Research and knowledge]
Keeps verified facts, glossaries and cited walkthroughs of how things work.
- mark: build — fm recall --explain QUESTION: a cited walkthrough from fm map, fm why and outline hits via fm second child; start by emitting the file:line citations without a child.
- status: partial; value 3/5; effort M; risk low
- evidence: fm recall indexes briefs, decisions, research, lessons; fm map; assume [verified]; no glossary or cited walkthrough
- ideas: #280 Wild: Compile the repo's tribal knowledge into a Q&A deck; #441 Answer "how does X work here" with a cited walkthrough; #442 Build a per-project glossary of internal terms from code and ledger; #446 Score recall quality against the ledger; #635 Keep a project knowledge base of verified facts with dependency tags; #641 Wild: Grow a "questions I had to look up" deck from the ledger

## I088 Known-world map and idle study [Research and knowledge]
Maps what has never been read and studies dependencies and changelogs when idle.
- mark: build — Cheap first step: fm night job that tracks which files the sessions never read (from transcripts/ledger) in fm map hot-vs-cold, then queues a recon of cold hot-path files as research debt. Skip curiosity engine and git-blame style.
- status: partial; value 3/5; effort M; risk low
- evidence: fm night jobs (landscape, second session, research debt), fm landscape, fm deps; no read-coverage map
- ideas: #277 Wild: Study dependencies at idle; #278 Wild: Run a curiosity engine on open questions; #279 Wild: Duel rival researchers; #447 Wild: Keep a "known world" map of what Foreman has never looked at; #448 Wild: Hold a nightly "read the changelog of the world" job; #449 Wild: Interview the codebase's git blame authors' style from history; #541 Wild: Map the repo's traps by quizzing cold agents; #640 Wild: Keep a "known world" fog map of the codebase and docs; #645 Wild: Hold a monthly "what do I believe that is probably false" audit

## I084 Source grading and citations [Research and knowledge]
Grades sources and checks that citations resolve.
- mark: skip — Citation checking and corroboration already shipped; a reliability ledger over domains adds little. Covered by fm research ask.
- status: exists; value 3/5; effort S; risk low
- evidence: fm research ask: quotes fetched and checked ✓/✗/?, tiering, single-source marks (T-0206, T-0277)
- ideas: #97 Answer from the installed dependency's source, with sources graded; #273 Keep a source reliability ledger; #274 Check citations mechanically; #310 Bind arguments to citations that resolve mechanically; #633 Pin each research answer to a re-runnable evidence recipe; #638 Grade every research source and show the grade next to each claim

## I043 Gate steps on observables [Steps and execution craft]
Declares a prediction, observable or done-snippet before each step and checks it after.
- mark: build — Add optional 'expect:' text on a step (step text '... :: cmd') recorded at plan time; fm task evidence compares the run output to it and logs a match/miss. First step: reuse the AC '::' parser for steps.
- status: partial; value 4/5; effort S; risk low
- evidence: fmcore.py:851 mark_step requires evidence per step; criteria carry '<done> :: <verify>'; no pre-step prediction/observable field
- ideas: #56 Commit to a falsifiable prediction before each step; #61 Add a definition-of-done rehearsal at plan time; #170 Run a deliberate–act–reflect loop with a step-level prediction; #401 Gate each step on a pre-declared observable; #406 Name the step's exit move before starting: continue, split, or escalate; #587 Diff the predicted call path against the traced one; #608 Require a "done looks like" command output snippet in each step before starting; #656 Record a verification oath before the build

## I044 Check the step against the plan [Steps and execution craft]
Verifies each step by a different method and compares the diff to the step and the brief.
- mark: build — fm audit prep adds per-step section: diff files vs step text and scope; a second-read prompt asks whether each hunk serves a step. Build on fm second and audit prep.
- status: partial; value 4/5; effort M; risk low
- evidence: fm check --mutate hunk-revert (fmcli.py:650, T-0271); fm tour; fm second plan/debate (T-0276); no step-vs-diff compare
- ideas: #67 Verify each step by a different method than the one that built it; #68 Compare the diff to the step's plan, not just the brief; #606 Reconcile steps against the brief at the halfway mark; #686 Close every objection to a diff hunk

## I046 Step ledgers and handoffs [Steps and execution craft]
Records what was tried, why the order, and a handoff stub per step.
- mark: build — Hook-level repeat detector: a third identical failing evidence cmd on a step logs 'tried' and nudges (T-0440 does this for refusals); add tried list to Resume here.
- status: partial; value 3/5; effort S; risk low
- evidence: Brief Log + hypotheses + assumptions ledgers (fmcore.py:887-934); fm surprise; no per-step tried ledger blocking repeats
- ideas: #389 Carry an invariant ledger across the plan's steps; #411 Record the "why this order" line between consecutive steps; #596 Make every step produce a handoff stub; #600 Keep a per-step "tried" ledger that blocks identical retries

## I048 Overlap and script the work [Steps and execution craft]
Runs verification in the background, scripts repetition and prepares before step one.
- mark: build — fm task start preflight: git clean, deps import, gate baseline cached, scope files exist; reports before step 1. Fold with BASELINE.
- status: partial; value 3/5; effort S; risk low
- evidence: fm check background guidance in foreman.md rules; drive names queued work while bg runs (T-0401); fm repeats finds repeated commands; no preflight
- ideas: #237 Script the repetition; #241 Wild: Mise en place before step 1; #362 Preflight the plan's world before step 1; #405 Run a step's verify in the background while the next step reads

## I045 Checkpoint, undo and resume [Steps and execution craft]
Gives each step a cheap undo and a clean baseline, and reconciles half-done work on resume.
- mark: build — On resume, re-run the last green step's evidence command and report drift; skip per-step commits (git-write risk, lanes cover isolation).
- status: partial; value 3/5; effort M; risk med
- evidence: fm checkpoint/resume + Resume here notes (fmcore, resume skill); fm lane worktrees; no per-step commit/revert or replay-last-green on resume
- ideas: #230 Reconcile a half-done step on resume; #235 Retry from a clean step baseline; #239 Declare safe interrupt points per step; #402 Checkpoint commits per step with a step-scoped revert; #407 Replay the last green step's command as the first act on resume; #601 Give every step a cheap undo point and a "step diff" view

## I047 Keep steps in scope [Steps and execution craft]
Attributes hunks to steps, flags foreign rewrites, skipped steps and scaffolding, and time-boxes exploration.
- mark: build — fm check/finish scan the added diff lines for debug scaffolding (print, console.log, TODO-debug, breakpoint) in files the task touched; first step is a regex lint on added lines.
- status: partial; value 3/5; effort M; risk low
- evidence: fmhooks.py:1070 _scope_note, _tripwire_note; scope globs per task; no hunk-to-step attribution or debug-scaffolding check
- ideas: #74 Set a "good enough" bar and a gold-plating tripwire at intake; #233 Attribute every diff hunk to a step and spin off orphans; #234 Keep every step green; #236 Detect foreign rewrites after every edit; #293 Declare a working mode and flag mode violations; #404 Make the smallest-diff rehearsal a step type; #412 Fail a step if it left debug scaffolding behind; #413 Time-box exploration steps and force a written finding at expiry; #598 Run a pre-edit "blast sketch" for each step; #599 Detect step-skipping and reorder at execution

## I049 Odd executor ideas [Steps and execution craft]
Baton passing, shadow executors, haikus and sprinter-versus-cautious duels.
- mark: skip — Duels and haikus are gimmicks; fm second and lanes already give the independent second executor. Value low.
- status: partial; value 2/5; effort L; risk med
- evidence: fm second plan (other model), fm lane/fm-builder; rest is novelty
- ideas: #65 Wild: Give each step a "pair" voice that interrupts at the moment of a risky choice; #240 Wild: Pass the baton; #242 Wild: Sample a shadow executor; #243 Wild: Hand-written postcondition haiku; #408 Wild: Keep a typed "hands" journal so any step can be re-executed by a cheaper model; #409 Wild: Pit a "step sprinter" against a "step cautious" on the same step and keep the cleaner diff; #410 Wild: Show a metronome of steps in the statusline that speeds up with stalls; #604 Wild: Let a step run in "dry-run script" form first

## I001 Split a message into its parts [Understanding the request and the user]
Separates questions, orders and venting, accounts for every clause, and resolves 'it', 'those' and how much latitude a phrase grants.
- mark: build — Add a clause ledger at intake: every clause of a multi-part message maps to a captured task, an answer, or an explicit 'noted'; fm next flags unaccounted clauses. First step: a check in fm intake/capture that lists clauses with no task id.
- status: partial; value 4/5; effort S; risk low
- evidence: intake skill tags + references/language.md:28 override words; fm intake parses blocks; no clause accounting
- ideas: #102 Split questions from orders at intake; #157 Account for every clause of a multi-part message; #159 Read the latitude a phrase grants; #160 Resolve "those", "it" and "the above" and echo the result; #161 Expand verbs into the obligations they imply; #165 Separate question, command, venting and delegation at intake; #322 Resolve "almost all" into its exceptions; #324 Restate every delegation as a bounded mandate; #509 Resolve which Foreman a request is about; #615 Judge whether a mid-task message preempts the task

## I003 Turn steers into lasting rules [Understanding the request and the user]
Generalises each steer into a principle, tells standing preferences from one-offs, and pins dictated numbers and stances.
- mark: build — Tag each steer standing or one-off, and for standing ones write a veto/rule candidate and sweep siblings. First step: classify steers in the ledger at close-out and propose fm vetoes entries via fm ask-style yes.
- status: partial; value 4/5; effort M; risk low
- evidence: fm vetoes (fmcli.py:280), fm taste (T-0112), fm bench court (T-0280) replays steers; no generalise/sweep or standing-vs-one-off tag
- ideas: #158 Generalize each steer into a principle and sweep for siblings; #247 Detect when a rule was applied rigidly against the user's evident intent; #262 Convert every user steer into a graded rule candidate with an expiry trial; #416 Distinguish a standing preference from a one-off in every steer; #505 Pin the numbers the user dictates; #506 Keep a stance ledger with supersession; #508 Treat silence as ratification, with a revoke

## I007 Learn from the user's reactions [Understanding the request and the user]
Turns corrections, overrides, silence and follow-up edits into labelled feedback.
- mark: build — Label each finished task's outcome (kept, corrected, reverted, dropped) from the next user message and later commits, store in ledger, feed fm taste and bench. First step: outcome label on task finish plus revert/follow-up-edit detection from git.
- status: partial; value 4/5; effort M; risk low
- evidence: fm taste kept/dropped; fm bench court (T-0280); fm friction counts steers/corrections; no per-task outcome label
- ideas: #83 Label every task's outcome from the user's next message; #206 Add a user-pull score from kept/dropped history; #321 Grade the endorsement on every task; #323 Predict over-build from the user's past drops; #325 Learn from the user overriding Foreman's own ranking; #376 Score ideas by user-keep prediction using the captured/skipped history; #437 Wild: Let the user's silence count as a signal, with a per-task "no complaint" streak; #621 Fuse noisy outcome signals into one label; #622 Read the user's follow-up edit as the corrected answer; #722 Relabel failed attempts with hindsight

## I002 Defend against misreading [Understanding the request and the user]
Generates likely misreadings and ambiguity up front and adds probes so the wrong reading is caught early.
- mark: build — Extend fm oracle to also emit the worst plausible misreading and one intake probe per misreading class, saved in the brief. Reuses existing oracle child.
- status: partial; value 3/5; effort S; risk low
- evidence: fm oracle (T-0226) lists ambiguities from spec alone; Interpretation section in briefs
- ideas: #103 Generate the worst plausible misreading (wild); #162 Classify each misreading and add the matching intake probe; #167 Wild: Show the interpretation as a version history; #720 Find spec ambiguity by blind-implementation divergence

## I009 Track open asks and who is asking [Understanding the request and the user]
Keeps answer debt, wrong-turn buttons and interpretation history visible.
- mark: build — Answer-debt list: fm second session already finds missed requests; first step is to surface it in fm next/status as 'unanswered asks' with a default and expiry. Small wiring.
- status: partial; value 3/5; effort S; risk low
- evidence: fm ask TTL + drive stop; fm second session (fmsecond.py SESSION) finds unanswered requests; vetoes
- ideas: #249 Keep a "when to stop asking" ledger of asks the user answered identically; #395 Give every ask a default and an expiry before it interrupts; #510 Track answer debt; #511 Add a wrong-turn button on every ledger line; #586 Name the hidden trade-off at intake

## I004 Model what the user believes [Understanding the request and the user]
Tracks the user's mental model and surfaces gaps and unsaid needs before obeying.
- mark: skip — Speculative mind-modelling with no ground truth; wish jar/vignette/future-self are theatre. Its useful core (surface gaps) is covered by 'Split a message' and 'Track open asks'.
- status: missing; value 3/5; effort M; risk med
- evidence: no belief model; fm taste shows choices only (fmideas.py:132)
- ideas: #139 Model what the user believes and correct the gap; #166 Wild: Mirror back the need they keep not saying; #328 Elicit abstract wishes with vignettes; #329 Wild: Provoke a correction with a confident wrong guess; #330 Wild: Keep a wish jar that ripens; #331 Wild: Write the letter from the user's future self; #513 Surface mental-model gaps before obeying; #700 Detect the decision the user keeps dodging

## I005 Predict how the user will react [Understanding the request and the user]
Rehearses the user's first glance at a result and tunes length, depth and pushback to what they act on.
- mark: skip — Reaction prediction is unverifiable; 'tune length by what user acts on' is subsumed by 'Learn from the user's reactions'. Acceptance glance already served by fm smoke.
- status: partial; value 3/5; effort M; risk low
- evidence: fm smoke (T-0417) checks product as user uses it; reply format quiet (T-0095); fm taste
- ideas: #163 Rehearse the user's acceptance glance; #164 Tune report length and depth by what the user acts on; #253 Wild: Hold a "would they frame it" test: render the close-out as the user's likely screenshot reaction; #426 Judge by the user's acceptance glance: predict the first thing they will look at; #474 Wild: Play the user's acceptance glance as an automated screenshot test; #515 Wild: Run a tired-you glance on every close-out; #694 Protect the user's muscle memory; #695 Calibrate pushback from overrides; #697 Show completion by request kind; #768 Verify the user's intent with a one-glance acceptance artifact

## I006 Learn the user's loss function and context [Understanding the request and the user]
Infers what the user values, why each project exists, and which role they speak from.
- mark: skip — Mostly already covered by fm taste + fm mission; dialect bake-offs and shell-history mining add privacy risk for low gain. Keep 'which hat' out.
- status: partial; value 3/5; effort M; risk med
- evidence: fm taste, fm mission (T-0375) composes mission from project, fm friction (T-0435), fm repeats
- ideas: #320 Keep an aspiration ledger and alarm on drift; #357 Run a request-dialect bake-off on the user's last 100 messages; #507 Map where the user has strong opinions; #674 Predict the user's next message category every turn; #693 Read the project's season; #696 Fit the user's loss function; #698 Tag which hat the user wears; #699 Infer why each project exists; #703 Wild: Read the workstation for implied values; #704 Wild: Mine shell history for the user's own repeated routines; #705 Wild: Know the user's reporters; #716 Wild: Split wanting from liking in the user's signals

## I008 Elicit preferences by interview [Understanding the request and the user]
Asks short, contrast-based or card-based questions to learn rules and prune idea piles.
- mark: skip — User wants autonomy and fewer questions; quizzing increases interruptions. Value 2 for this user.
- status: missing; value 2/5; effort M; risk low
- evidence: no interview command; AskUserQuestion only used for single asks
- ideas: #76 Learn the user's rules by quizzing with contrast cases; #381 Wild: Hold an idea tasting where the user reacts in one keystroke per card; #514 Wild: Let the user underline the word that matters; #530 Prune the idea pile with a 20-questions interview; #568 Wild: Interview the user with five rapid idea cards

## I058 Typed claims and proof contracts [Verification reasoning]
Types each done claim, requires its proof shape, and splits close-outs into claims with evidence.
- mark: build — Close-out via fm task finish gains per-claim lines tagged checked/inferred/not evaluated with an evidence pointer; fm pr renders them. Three-valued verdict is the core.
- status: partial; value 4/5; effort M; risk low
- evidence: execute.md:42 evidence rules; --inconclusive and assumptions (T-0261); verification grade (fmcore.py:1125); fm pr proof sections (T-0263); no claim typing or checked/inferred split
- ideas: #122 Track where each expected value came from; #123 Make verdicts three-valued: pass, fail, not evaluated; #128 Declare frame conditions: what must not change; #281 Check quantifiers against an enumeration; #468 Add a verdict taxonomy for "done" claims with per-claim residuals; #659 Separate "I checked" from "I inferred" in close-outs; #756 Compile every criterion into a Proof Contract; #759 Split the close-out into a claims ledger with evidence pointers

## I060 Verify the verifier [Verification reasoning]
Tests whether a check could ever fail by mutation, broken siblings and executed-test counts.
- mark: build — Record executed-test count for verify commands (parse pytest/unittest summary) and flag zero or unchanged counts as inconclusive; add negative-twin criterion suggestion in oracle. Hunk ablation exists, skip.
- status: partial; value 4/5; effort M; risk low
- evidence: fm task prove (red-green) and --hunks (T-0271); inconclusive evidence (T-0261); no executed-test count or negative twin
- ideas: #124 Write semantic mutants aimed at the brief's risks; #126 Ablate the diff hunk by hunk; #285 Detect tests that only assert their own doubles; #467 Verify the verification of the last fix with a "would the old bug have failed this?" replay; #470 Detect verification that tests the wrong layer; #475 Wild: Run a "lying tests" pass where a model rewrites the product to fake each test; #653 Pair each criterion with a negative twin; #654 Count tests actually executed by each verify; #655 Verify the verifier's selector against the diff; #660 Replay the verify against an intentionally broken sibling; #757 Run a mutation-backed verify audit on each changed file

## I061 Stale evidence [Verification reasoning]
Gives evidence a half-life and re-verifies when inputs change.
- mark: build — Evidence entries record the tree id they ran on; fm task done flags evidence older than the last edit to a file the check reads (reuse the audit staleness code). Skip half-lives.
- status: partial; value 3/5; effort S; risk low
- evidence: fm check reuses a pass on the same tree (fmcore flaky/tree record ~1849); audits stale after later edits (fmcore.py:1012); fm sentinel re-runs old checks (T-0263)
- ideas: #132 Give verified claims a half-life (wild); #283 Index evidence by what it read, and stale it on touch; #440 Pin a verified-facts cache with expiry triggers; #472 Re-verify old closed criteria when their dependencies change; #665 Age evidence and re-verify when its inputs change; #761 Re-verify automatically when evidence inputs change

## I062 Verify the need and the observable [Verification reasoning]
Checks the user's need, observable outcome and interpretations, not only the request.
- mark: build — Add an 'observable' line to criteria: what the user will see, checked by intent lens and fm smoke; paraphrase-verify via oracle on the paraphrased brief. Instruction plus small template change.
- status: partial; value 3/5; effort S; risk low
- evidence: fm oracle (T-0226) derives behaviour from the spec; intent audit lens; fm smoke checks product as user
- ideas: #131 Rebuild the brief from the tests alone (wild); #289 Verify the need, not just the request; #292 Verify under a paraphrased brief; #593 Hire a genie to hunt loopholes in the criteria; #664 Check claims against what the user would observe; #687 Duel interpretations with failing tests; #762 Make interpretation-splitting checks part of the oracle

## I059 Independent evidence [Verification reasoning]
Checks evidence for independence and triangulates criteria, tests and behaviour.
- mark: build — Make audit prep require a reproducer for each reviewer finding (already verified by hand per audit.md step 4) and add a 'weakest link' line to the builder brief. Skip cross-validating verifiers.
- status: partial; value 3/5; effort M; risk low
- evidence: fm oracle (T-0226), fm audit prep with fresh-context lenses, fm second debate; no independence check on evidence
- ideas: #127 Audit evidence for independence; #282 Make the unverifiable observable first; #284 Require a reproducer on every reviewer finding; #286 Make the builder name its weakest link; #288 Triangulate criteria, tests and observed behaviour; #291 Run a builder confessional; #469 Cross-validate verifiers against each other; #592 Add a Fermi check to performance and size claims

## I063 Adversarial verification [Verification reasoning]
Panels and red teams try to forge or break a pass.
- mark: build — Add a 'forge a pass' reviewer brief to fm audit prep: read-only agent tries to name a change that satisfies the verify command yet breaks the criterion. Skip auctions and betting; wild pieces are low value.
- status: partial; value 3/5; effort M; risk low
- evidence: Adversary lens in audit.md, fm second debate rebuts findings; fm evolve gate
- ideas: #473 Wild: Hold a "verdict auction" where verifiers stake credibility; #661 Wild: Hold a "verification heist" where a red-team agent forges a pass; #663 Wild: Keep a "lie detector" cheap model that reads only the close-out and the diff stat; #763 Rehearse the verdict with an adversarial verifier panel; #765 Wild: Hire a "future you" saboteur to break the shipped change; #767 Wild: Bet the verify against a pre-registered failure prediction

## I065 Verification budgets and track records [Verification reasoning]
Chooses verify methods and spend by cost, risk and historical catch rate.
- mark: build — Compute per-verify-command catch rate from ledger (times it failed then passed, hunks noticed) and show a done-confidence line in fm task done; do not gate on it at first.
- status: partial; value 3/5; effort M; risk low
- evidence: fm budget (T-0227) spend ledger; fm bench; fm sentinel; no per-check catch rate
- ideas: #129 Show a done-confidence meter built from check track records; #465 Run a verification-method selector at plan time; #466 Keep a failure-mode checklist per verify command; #471 Track a verification-cost ledger and spend it by risk; #477 Score each criterion's "surprise value" to prioritise review attention; #657 Score verification by what it could have caught historically; #666 Expose one trust number for everything Foreman produces; #758 Gate done on a historical catch-rate score

## I066 Docs and diagrams match reality [Verification reasoning]
Checks docs, help text and diagrams against behaviour.
- mark: skip — fm docs and the operator lens already check doc drift; cold-user docs test and proof receipts are low value for this user.
- status: partial; value 2/5; effort S; risk low
- evidence: fm docs reports markdown drift (T-0296); operator audit lens checks docs; fm doctor MASTER.md file map
- ideas: #275 Check the docs against reality; #290 Test the documentation with a cold user; #476 Verify that docs and help text claims still match behaviour after each task; #585 Settle disagreements between code, tests, docs and brief with a verdict; #588 Prove "unused" across dynamic references before deleting; #662 Wild: Print a "proof receipt" users can verify without Foreman; #711 Verify plan diagrams against the code; #766 Wild: Keep a verification flight recorder that can replay the proof

## I064 Perturbed and repeated runs [Verification reasoning]
Re-runs under paraphrase and perturbation to test fragility.
- mark: skip — Rerunning verifications under paraphrase burns spend for little; flaky detection and fm second cover the fragility concern. Stronger sibling: Verify the verifier.
- status: partial; value 2/5; effort M; risk low
- evidence: fm research ask cross-checks (T-0206/T-0277); bench duels; flaky detection records same-tree reruns (fmcore ~1849)
- ideas: #287 Treat verification as sequential testing; #540 Sample a claim several times before trusting it; #658 Verify across a perturbed second run; #682 Test verdict fragility by flip and paraphrase; #764 Run perturbed double verification

