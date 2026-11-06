# Brainstorm — lens: blind spots

Each idea below is tied to a class of ask the user had to make: "what does this part earn" (T-2534, T-2536), "which commit did it" (T-2535), "is it alive" (T-2542), "is it already built" (T-2546), "is it grounded" (T-2547), "who authored this input" (T-2554), and "what happens on partial input" (T-2566).

- **Ablate each tick job in a no-op arm** — FEATURE — value 4 — effort M — risk low — category: measurement
  Why: T-2536 and T-2534 were asks for "what does this part earn". The pack shows `fm night`'s tick running maintain, the digest and ci-watch, with no per-job control. Assumption: jobs can be switched off individually.
  Done when: `fm night tick --ablate JOB` replays one recorded tick tape with that job off, and the report lists each job's marginal outputs. Jobs with none are flagged as cleanup candidates.

- **Refuse a tick job with no named consumer** — CLEAN — value 4 — effort S — risk low — category: grounding
  Why: T-2547 refused Missions without grounding. The same blind spot applies to the tick: a job can write output that no session path reads, and the pack's standing rule says every capability needs a calling path.
  Done when: registering a tick job without a `reads_by:` session path fails a test. `fm doctor` lists existing jobs that lack one.

- **Exclude tick-filed work from the base rates the tick is graded against** — FIX — value 4 — effort S — risk med — category: contamination
  Why: T-2554 showed Foreman's own output leaking into the user model. Bets that the tick settles and tasks it files feed `fm outcomes` base rates, so the tick would grade itself. Assumption: there is an origin tag on tick-filed rows.
  Done when: a planted tick-filed task changes neither the Brier base rate nor the foresight asked stream, in a test.

- **Name the commit behind a drop in tick usefulness** — FEATURE — value 3 — effort M — risk low — category: attribution
  Why: T-2535 asked for commit-level blame on grown metrics. Tick lateness and useful-fire rate have no equivalent.
  Done when: a recorded tape replayed at two commits prints the first commit where the useful-fire rate fell by more than a threshold.

- **Say "insufficient" for any tick grade built on partial data** — FIX — value 4 — effort S — risk low — category: honesty
  Why: T-2566 let a held-out-only exam decide a keep or revert. A tick grade from two nights, or from a single source, is the same hazard.
  Done when: below N ticks or one source, the grade prints `insufficient (n=…)` and `fm genesis select` skips it. A test pins this.

- **Ask "already built" for tick jobs at birth** — FEATURE — value 3 — effort S — risk low — category: duplication
  Why: T-2546 added birth-time checks for requests only. A new tick job that restates `fm ci-watch`, `fm night` or a drive resume is an unchecked path.
  Done when: registering a job whose description matches a MASTER.md clause above a threshold prints that clause and its task id.

- **Count tick sources alive at session start** — FEATURE — value 3 — effort S — risk low — category: liveness
  Why: T-2542 covered installed timers only. Without an install, the clock is session edges, the web UI and CI, and nothing says which of them last ran.
  Done when: the session-start note says "tick last ran 3h ago via session-stop, timer: none". The line is absent when the tick is fresh.

- **Hold out one share of fires as a causal control** — FEATURE — value 4 — effort M — risk med — category: measurement
  Why: this goes past T-2534's arms. A rate of useful fires has no baseline for what the user would have done unprompted. Assumption: a random 1 in 5 skip is acceptable.
  Done when: held-out fires are logged, and a report compares the user's later hand-action rate on held-out versus fired items.

- **Put a one-line external check on every self-started result** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: this answers an earlier question the pack left open ("what does the user act on without checking?"). A tick result stays unchecked unless it carries a command the user can paste.
  Done when: every tick-filed item prints a `verify:` line that runs a command outside Foreman, such as `git log` or `systemctl`. A test rejects items without one.

- **Wild: Seal the tick's predicted morning card and settle it at wake** — FEATURE — value 3 — effort M — risk low — category: calibration
  Why: wild. A tick seals what it expects to report, and the real morning shows whether it was right, the same shape as the sealed-prediction idea.
  Done when: a prediction row is written before each tick and scored hit or miss at the next session start.

- **Wild: Query the tick's blind spots with a stranger child** — FEATURE — value 3 — effort M — risk low — category: exam
  Why: wild. A tool-less child that sees only the tick's output names events that should have fired and did not. It reuses the pack's standing rule on signals Foreman did not author.
  Done when: planted events missed by the tick appear in the child's list at a recorded recall rate.

- **Wild: Dead-letter drill that kills a tick job mid-run** — FIX — value 3 — effort M — risk low — category: resilience
  Why: wild. The pack shows no kill-at-boundary test on the tick. It would ask what partial input the next run sees.
  Done when: a kill after each job leaves a state from which the next tick completes and reports "recovered" once.

Next question: Which question would a brainstorm have needed to ask to predict the eight missed asks as a class: "does it earn, is it alive, is it real, who wrote it"? Does every capability have all four checks?
Next question: What does the user do with a self-start when they are mid-flow and the tick has no one to tell?
