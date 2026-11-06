# Brainstorm — lens: blind spots

Each idea starts from a missed-ask class in the pack. I put the question a brainstorm should have asked in the Why line and asked it of the whole project.

- **Bind every push to the tree hash the gate passed** — SECURITY — value 4 — effort S — risk low — category: ship
  Why: T-2534/2535/2566 were controls, causes and partial inputs. The class here is "what was checked vs what was shipped". The question is "between the gate and the push, what can change?". Evidence: the push grant is spent per task, and T-2598 lands via cherry-picks onto main. Assumption: nothing today compares the pushed tree to the gated one.
  Done when: a test that edits a file between `fm ship`'s gate pass and its push sees the push refused with both hashes named.

- **Diff main's landed tree against the gated tree after each cherry-pick ship** — FIX — value 4 — effort M — risk low — category: ship
  Why: T-2598 made main be "fed by ship's cherry-picks", so the commit that passed the suite is not the commit on main. The question is "is what's live the thing we tested?". Assumption: no post-landing equality check exists.
  Done when: a ship with a planted conflict-resolution drift reports "landed tree differs from gated tree" and names the files.

- **Stamp every context pack and map with its HEAD and age, and make children say when it's stale** — FIX — value 3 — effort S — risk low — category: freshness
  Why: this pack's own Map line says "as of an older HEAD", so brainstormers reason from stale layout. The question is "which reads are older than the thing they describe?".
  Done when: a pack built 50 commits behind HEAD opens with a one-line staleness banner, and a unit test covers it.

- **Run a sibling sweep when a missed ask is filed** — FEATURE — value 4 — effort M — risk med — category: blind spots
  Why: the eight missed asks (T-2534 to T-2566) each fixed one gauge, but each class (control arm, cause naming, silent death, already built, grounding, input contamination, partial input) probably has unfixed siblings. The question is "which other gauges have this same hole?". Assumption: that sweep is currently done by hand.
  Done when: filing a task tagged with a class lists every verb or gauge that fails the class probe, with one candidate task per hit.

- **Check each verb's refusal text for an actionable next command** — CLEAN — value 3 — effort S — risk low — category: UX
  Why: T-2606 had to teach that "a criterion whose runs matched no test can have its verify command fixed". That was a refusal the user had to ask about. The question is "which refusals leave the user stuck?". Assumption: other locks like T-2606's exist.
  Done when: a lint over all refusal strings fails any that lacks a command, and it passes on the current tree after fixes.

- **Add a stale-installed-component line to `fm doctor`** — FIX — value 3 — effort S — risk low — category: drift
  Why: T-0418 (foreman-ui installed at an old version) sits blocked, and the mod pins Claude Code 2.1.301 behaviour (T-1217, pane colour). The question is "which of the user's installed parts are behind the source?". Assumption: doctor doesn't compare versions of mods and units.
  Done when: doctor prints installed vs source version for the mod, units and hooks, and WARNs on a mismatch.

- **Mark the gap between blocked-on-user items and their weekly cost** — FEATURE — value 3 — effort S — risk low — category: unblocking
  Why: T-0325 (needs a `sudo pacman` install), T-0335 to T-0337 and T-0352 have been blocked for a long time with no price. The question is "what does a wait cost the user?". Assumption: the cost is estimable from queue age and dependents.
  Done when: the digest names the single blocked item gating the most open tasks, with its one-line unblock command.

- **Run an arithmetic-consistency lint on DONE-WHEN text** — FIX — value 3 — effort S — risk low — category: criteria
  Why: T-2583's text said 8+ characters while its own example had 7. The question is "do a criterion's numbers contradict its examples?". The "test a criterion against its own examples" idea exists; this one extracts numeric thresholds and checks quoted examples mechanically.
  Done when: the T-2583 text fails the lint and a corrected one passes.

- **Pin every hash-modulo selection to a stable content key** — FIX — value 3 — effort S — risk low — category: stability
  Why: the BEYOND-row steer found `list(BEYOND)[hash % len]` reassigns items when a row is added. The question is "what else is indexed by position or length?". Assumption: other modulo picks exist in exam and Mission code.
  Done when: grep finds no `% len(` pick over a mutable list, and a test adds an element and sees no old assignment move.

- **Wild: Hold a "missed-ask forecast" bounty** — FEATURE — value 3 — effort M — risk low — category: meta
  Why: wild. Each generation, a blind child lists the user's next eight missed asks from the changelog alone, and the ones that land are scored. This turns the blind-spot lens into a measured arm. Assumption: ask records carry enough text to match.
  Done when: a scoreboard shows predicted vs actual misses per generation.

- **Wild: Inject a typo'd gauge on purpose** — FEATURE — value 2 — effort M — risk low — category: gauges
  Why: wild. Plant one wrong-but-green gauge in a fixture and see whether any cold read catches it. This tests whether blind-spot hunts work at all. Assumption: there is a fixture project to host it.
  Done when: the exam reports caught or missed for each planted gauge.

- **Wild: Print a "what I can't see" page at the end of every report** — FEATURE — value 3 — effort S — risk low — category: honesty
  Why: wild. Each report ends with a fixed block: inputs Foreman wrote itself, gauges with no outside check, and timers not confirmed alive. Assumption: those facts are derivable from existing doctor data.
  Done when: the final report contains the block with counts, and a test fails if a listed source goes missing.

Answers to the earlier questions that my lens can take:
- **Gauges the user can't falsify by hand:** any gauge built only from Foreman's own ledgers, such as the calibration Brier and the held-rate. The cheapest outside check is one line quoting a raw ledger row or git hash beside the number.
- **Jobs that must run on time:** settled bets and the nightly digest. Everything else can wait for the next session edge.

Next question: Which verbs or gauges still have no probe for each of the eight missed-ask classes, and who would notice a wrong answer first?
Next question: When a human edits a Foreman-generated file by hand (steers, goals, coverage), which reader overwrites or ignores that edit?
