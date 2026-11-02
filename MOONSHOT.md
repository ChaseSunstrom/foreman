steer: two standing additions, recorded with fm decide, each with its automatic check. Part C is exam data only: its rules are already in force, so don't apply them again or file tasks for them.

## A. Moonshot campaign (queued: starts automatically once gen-0's DONE-WHEN holds)

100 moonshots on a six-tier ambition scale, weighted to the top, built as a climb toward the biggest.

**Scale** (the anchors are calibration, not ideas to copy):
- **low:** an existing loop gets a clever new signal or check.
- **medium:** a mechanism borrowed from another field, inside one capability. Anchor: gen 2's anergy (reflex-approved
  prompts become allow rules).
- **high:** a new capability class that spans the harness.
- **xhigh:** changes how the work is done: who decides, how agents coordinate, how work is chosen or priced.
- **extreme:** changes what Foreman is. It simulates, predicts or runs things no harness does today.
- **massive:** changes what building software means for its user. It takes on whole classes of work end to end that
  today need a team.

**Mix:** 5 low, 10 medium, 15 high, 20 xhigh, 25 extreme, 25 massive.

**Generation:**
- Rotate far-domain lenses across the campaign: biology, ecology, economics and markets, military logistics, law,
  physics, neuroscience, evolution, cities, games, manufacturing, science itself, and others it adds. Each lens gets
  the frontier digest.
- For xhigh and up, also use inversion ("what makes Foreman obsolete?") and 2030-worked-back lenses.
- Crossbreed the best ideas across domains.

**Rating:**
- The tier is assigned by a cold reviewer on the strongest available model, one that never saw the generating session,
  not by the author.
- Massive must pass "would this be news to people who build agent harnesses?". Extreme must name what no current
  harness can do.
- Inflated tiers are demoted. The author's tier is kept beside the reviewer's, so inflation can be tracked.
- Each moonshot carries Prior art, Better by and Novelty lines. Duplicates of built or queued work are rejected.

**Building, as a climb:**
1. **Kill tests first.** Before building anything, run the cheapest experiment that could prove each extreme and
   massive moonshot wrong, all 50. Each viable one records the capabilities it needs that don't exist yet.
2. **Dependency map.** A map in moonshot.md links every viable big moonshot to its missing capabilities, and each
   lower-tier moonshot to the big ones it unblocks.
3. **Climb.** Build first the lower-tier moonshots that supply missing capabilities, ranked by how many big ones they
   unblock. Then climb tier by tier, each built on the ones before it. Lower-tier moonshots that unblock nothing come
   last.
4. **Staged builds.** Extreme and massive moonshots go through kill test, smallest working slice, then full build, each
   stage proven before the next.
5. **Re-check.** After every build, re-run the kill tests of the blocked big moonshots. One a new capability unblocks
   moves up the queue.
6. **Floor for the top.** Every generation advances at least one extreme or massive moonshot by a stage, so the
   campaign can't settle at the lower tiers.

Nothing is killed for ambition: a failure goes to not-yet with its blocker and is retried as new capabilities land.
Every built moonshot gets an exam kind or an outcome measure.

**Report:** a moonshot catalogue page with every moonshot by tier (author's and reviewer's), domain, novelty, the stage
it reached, what it unblocked and the evidence. It also says which ones the user would never have asked for.

## B. Steer-expansion exam (start now, for #3 Anticipation and #13)

The goal: the user sends raw words and Foreman turns them into complete standing rules on its own, provably, so
nobody has to write steers for it.

- **Cases:** the pairs in part C, plus Foreman's own history wherever a terse ask was later corrected or expanded.
- **Test:** from the raw words alone, Foreman expands each case into a standing rule.
- **Scoring:** a cold reviewer on a stronger model scores how many of the reference steer's clauses the expansion
  covers, and flags anything harmful it added. A third of the cases are held out.
- **Live use:** when a user message arrives, Foreman expands it, files the expansion in the queue with its exam score,
  and acts on it without asking. The user reads it only when the score is low.
- **Learning:** every user correction of an expansion becomes a new case.
- **Reporting:** the held-out coverage rate goes on the Genesis page.

## C. Exam data: the user's raw words and the steers they became

The raw words are the user's, lightly trimmed. The reference steers are condensed to their clauses.

1. **Raw:** "I want it to be able to find ideas itself too, and not just in foreman... able to find/fix/do anything,
   and I shouldn't even need to prompt/ask it for things."
   **Steer:** Initiative in any repo with no request: map it, find real problems, rank them by value, prove each one,
   fix it on a lane. Unprompted actions stay local and reversible. Anything outward needs a grant and goes to the final
   report.
2. **Raw:** "and not just that either, all the things, everything. and I want it to be able to seed itself for a seed
   that then prompts itself to prompt that then does everything."
   **Steer:** A prompt tower: gen-0 (fixed) writes a Seed, the Seed writes Missions, the Missions write and build
   briefs. Each level critiques and proposes a rewrite of the level above. A rewrite survives only if it beats its
   parent on the exam. Lineage is recorded, plus a drift check against gen-0. Scope covers Foreman, any repo, all the
   user's projects, the ecosystem and work beyond code.
3. **Raw:** "no token budget, but everything should be complete."
   **Steer:** No spend cap on building and proving; usage limits are waited out. A capability is done only with its
   tests, exam, docs, site page, pane surface and every surface it belongs on. A completeness sweep must come back
   clean before the next generation.
4. **Raw:** "I want it to be able to find/do anything in its own right, and think of every possible
   outcome/possibility/fix entirely on its own... I don't want it to burn tokens on random repos, but I want it to build
   everything needed."
   **Steer:** A 12-capability spec (initiative, exhaustive thinking, anticipation, goal to finish, getting tools,
   verifying anything, self-repair, calibrated judgment, orchestration, beyond code, self-triggering, lean and safe).
   A gap map first. No clone-and-read sweeps of outside repos; targeted research only when stuck. A local generated
   exam with hidden keys, a third held out.
5. **Raw:** "will this inevitably unlock the feature itself of being able to seed/do this autonomously, without me
   having to ask you to write the seed?"
   **Steer:** Capability #13: Genesis as a shipped feature. fm genesis writes its own gen-0 from one line or nothing,
   writes a per-project spec, runs the tower in any project, auto-starts from routing, the loop and scout, and carries
   over its winning templates. Its exam: a self-written gen-0 must cover the hand-written one.
6. **Raw:** "I don't want ambitious good features to be killed, and I want every single possible coverage, not just a
   few."
   **Steer:** No idea is killed for ambition: two or more new approaches, then the not-yet ledger, retried every
   generation, removed only for proven harm or duplication. A coverage grid (capability areas × surfaces × stages) where
   every cell holds a grounded idea, an existing path or a reason. Empty cells are filled first.
7. **Raw:** "it needs to be able to find its own areas and weaknesses that need improvement. That's why I made it, so it
   could just be."
   **Steer:** Weakness-finding uses signals Foreman didn't author: outcome survival, cold reviews by a different model,
   foreman vs plain on held-out scenarios. Exam scenarios come from a separate tool-less author. A capability that is
   strong on self-checks but weak on outside signals becomes a top gap.
8. **Raw:** "on full complex codebases and things where I want it running autonomously, there is genuinely a huge
   difference, but foreman won't be able to quantify that."
   **Steer:** A long-horizon exam tier: replayed real repos rolled back to a past commit, faults planted mid-run,
   foreman vs plain. Scored per finished goal: true-done rate, false-done claims, regressions, interventions, cost per
   finished goal. Lean or cost changes can't be accepted on small scenarios alone.
9. **Raw:** "can we have it do all testing near the end? ...because we don't want to just burn tokens, unless it uses
   haiku or something."
   **Steer:** Testing cadence: unit tests and gates on every task. Every generation, only the free arms plus a Haiku
   smoke run, and Haiku never decides "done". The full exam and the long tier run at the end, or early only for a
   regression. Selection is marked provisional until the final exam.
10. **Raw:** "I shouldn't even need to ask for this kind of stuff... why was foreman not able to catch what it was doing
    itself?"
    **Steer:** A cold read of every tower file before it's filed, checking against gen-0 and for metric-gaming. Every
    user steer becomes a standing rule plus an automatic check in the same task.
11. **Raw:** "if it's just regex, how can we make sure it finds everything/anything, especially in different languages,
    since we don't want to hardcode things?"
    **Steer:** Detection is never hand-written per language. In order: the ecosystem's own tools (compilers, linters,
    OSV-Scanner, Semgrep, gitleaks); tree-sitter structural rules; runtime signals (tests, coverage, fuzzing, mutation
    testing, git hotspots); AI review aimed at hotspots, proven by a failing test; blind spots become new rules. Recall
    reported per language and bug type.
12. **Raw:** "I want it to be able to genuinely come up with groundbreaking ideas/features without me asking for
    anything."
    **Steer:** One moonshot Mission per generation that fits no cell and no capability: a far-domain lens, a frontier
    digest, Prior art / Better by / Novelty lines, a cold read marking obvious ideas, every pick spiked.
13. **Raw:** "should it be able to come up with new categories and everything on its own? like more things to
    reference/think through, then building on top of those?"
    **Steer:** The frame may grow, never shrink. Foreman adds capabilities, coverage rows, columns and stages, lenses and
    exam kinds, each with evidence, a cold read and a measure. Gen-0 stays fixed.
14. **Raw:** "can you tell it to wait on the long stuff? and just finish everything? it had stopped for budget, but I
    want it to just fully complete everything."
    **Steer:** Pause long-horizon runs until the end. Finish the round in order. Don't stop for budget or pace; wait out
    real limits. A cap only the user can raise is named once.
15. **Raw:** "how come it hasn't finished all of the missions for gen 1 yet?"
    **Steer:** Run independent Missions in parallel lanes, each with its own critique, merged in mission order.
16. **Raw:** "include functionality of something like jev or a self hosted model that's similar to better
    organize/structure things, and even more types of models like that, self hosted and all."
    **Steer:** A model layer: a decision interface (choice, score, probability) tried cheapest first (rules, local
    models such as selfjev, jeff, Von and Jevlike, then hosted, then Claude), plus embeddings, rerankers, vision and
    local code models. Never inside the guard or the gates. Sensitive repos stay local. Installs need the user's yes.
    Each use is kept only if its exam beats the path it replaces.
17. **Raw:** "how can we have it start gen2 automatically without me doing anything? and keep going."
    **Steer:** The tower advances itself. A red sweep files its own fix tasks; a clean sweep writes the next Seed at
    once. It never blocks on the user for rules or process questions: it picks the option most consistent with gen-0,
    records it as costly, and continues. Coverage blocks only the end of the run, not a generation.
18. **Raw:** "what steer could I send to fix all of those? and even find things it didn't even think about."
    **Steer:** Per generation: a cross-cutting cold review on a stronger model; the gap map redrawn and Missions ranked
    by value, not cell count; lean measured by code, hooks, context and verbs; proof before presentation; a sealed
    prediction of the next steers, plus a blind-spot hunt from inputs Foreman didn't author.
19. **Raw:** "maybe you could write one final steer to rule them all, since you should probably understand what I am
    wanting/asking for by this point."
    **Steer:** Standing intent: anticipate (generalize the pattern behind each steer); act, don't advise; next-level,
    not polish; complete, with a frame that grows; general across repos; truth over self-image; spend where it decides
    something; every lesson becomes code; never trade safety for autonomy.
