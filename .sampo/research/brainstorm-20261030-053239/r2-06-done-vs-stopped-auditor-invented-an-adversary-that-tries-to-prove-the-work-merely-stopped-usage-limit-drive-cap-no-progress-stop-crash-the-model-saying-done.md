# Brainstorm — lens: done-vs-stopped auditor (invented): an adversary that tries to prove the work merely stopped — usage limit, drive cap, no-progress stop, crash, the model saying done

- **Write a stop-cause record at every session end** — FEATURE — value 5 — effort M — risk low — category: verdict
  Why: gap map lists "done-vs-stopped verdict" as missing; Stop drive has DRIVE_MAX, no-progress stop, contract bound, and forever-loop dry rounds, but each exits silently with no stored cause. Earlier ideas say "classify stop cause" but none define the closed set the auditor must pick from.
  Done when: every Stop/PreCompact/crash-recovery path writes one ledger event with cause ∈ {usage_limit, drive_cap, no_progress, contract_bound, dry_rounds, crash, model_claimed_done, user_stop, verified_done}, and a test fails if any Stop branch exits without one.

- **Make "verified_done" unreachable by assertion** — SECURITY — value 5 — effort M — risk med — category: verdict
  Why: "never lower your own guard" plus the model saying "done" is the very stop being audited. assumption: today a model's done text plus closed tasks can end a goal.
  Done when: a test where the session says "done" with one goal-ledger row lacking fresh evidence yields cause=model_claimed_done and the Stop hook blocks; only a row set with all evidence fresh yields verified_done.

- **Run an adversarial "stopped, not done" checklist before any done** — FEATURE — value 5 — effort M — risk low — category: auditor
  Why: the lens. A fixed list of cheap, deterministic counter-claims is run against the goal: open criteria; contents items with no task; tasks with no evidence newer than the last tree change; docs/site/pane/surface satellites missing (the MUST list); exam scenarios unrun; last session ended on a non-verified cause. Each hit is quoted as data.
  Done when: `fm goal audit` prints each counter-claim with pass/fail and the evidence line, exits nonzero on any fail, and the Stop hook cites the first failing one.

- **Give the auditor a tail-of-session fingerprint** — FEATURE — value 4 — effort S — risk low — category: detection
  Why: usage-limit and crash stops leave a recognizable tail (a truncated tool call, no final message, a limit banner, a lock left held). assumption: transcripts/state show these today.
  Done when: fixtures of five real tails (limit banner, killed mid-tool, drive-cap message, clean done, no-progress) each classify correctly, and an unknown tail yields cause=unknown, never done.

- **Treat "unknown" as stopped** — FIX — value 4 — effort S — risk low — category: verdict
  Why: both Missions found false alarms sink arms; the mirror failure is a false "done". The default must favor continuing.
  Done when: any classifier exception, missing ledger, or unparseable state yields stopped/unknown and the next SessionStart re-injects the goal.

- **Compare the stop cause with the claim in one line at resume** — FEATURE — value 4 — effort S — risk low — category: continuity
  Why: after a crash the user and model can't tell if work was finished. assumption: SessionStart can afford one line under the 10 KB budget.
  Done when: SessionStart prints "last stop: drive_cap, 6/9 contents items verified, next: X" and stays under the bench_hooks gate.

- **Make the forever loop's dry rounds file a counter-audit** — FIX — value 4 — effort M — risk low — category: loop
  Why: `fm loop on` stops after 2 dry rounds, which looks like done. A dry round only means the finders found nothing, not that contents are met.
  Done when: after 2 dry rounds with an unmet goal item, the stop cause is dry_rounds and the goal stays open with a pointer to the unmet item.

- **Add a "looks-done" scenario family to the exam** — FEATURE — value 5 — effort L — risk med — category: exam
  Why: the exam grades done only on held-out scenarios; no kind plants a goal that is 80% finished or one with a hidden missing satellite, which is exactly what the auditor must catch.
  Done when: `fm exam` has kinds G-stopped (session killed at 80%), G-claimed (done said with a missing doc/test), G-true (truly finished); the auditor must say stopped, stopped, done respectively, with a score per kind.

- **Wild: Inject a killer that kills sessions at random points** — FEATURE — value 4 — effort M — risk med — category: chaos
  Why: reliability is thin. A harness that SIGKILLs a headless `fm run` at random stage boundaries and checks the next session reports stopped with the right cause and resumes, never done.
  Done when: 20 random kills across a scripted goal each end with a correct cause and an eventual verified_done after resume.

- **Wild: Hire a rival closer** — FEATURE — value 3 — effort M — risk med — category: auditor
  Why: a cold tool-less model gets only the goal ledger and is told to argue the work only stopped; the closing needs its refutation to fail on a named line. It sees data, not the session's claims.
  Done when: the closer's argument, quoted as data, is stored with the verdict, and a planted missing satellite gets caught in at least 4 of 5 scenarios.

- **Wild: Keep a tombstone of stops that were wrongly called done** — FEATURE — value 3 — effort S — risk low — category: learning
  Why: a reopen after done is the strongest signal the auditor failed. Log each as a miss against the counter-claim that should have fired and add a new counter-claim when a class repeats.
  Done when: a reopened goal writes a miss row naming the stop cause; `fm goal audit --misses` lists them by class.

- **Show cause and distance on every surface** — FEATURE — value 4 — effort M — risk low — category: surfaces
  Why: the MUST list requires pane, MCP, fm code, other agents, and site for stateful capabilities.
  Done when: the pane line, an MCP read-only tool, the fm code banner, and the site page all render the same cause/progress string from one function, covered by one parity test.

- **Stop the audit from reading its own prior verdict as evidence** — SECURITY — value 3 — effort S — risk low — category: integrity
  Why: a cached "verified_done" could launder a stale pass; the evidence must be re-run or timestamped after the last tree change.
  Done when: editing a file after a verified_done flips the next audit to stale, and the verdict ledger event records the tree hash it covered.

Next question: What is the cheapest signal that distinguishes "user walked away" from "session crashed" when neither wrote a final message?

Next question: When the goal's contents list itself is wrong (missing a line), what does the auditor compare against to say stopped, since every item checks green?
