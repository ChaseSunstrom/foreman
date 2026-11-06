# Brainstorm — lens: blind spots

Answers to the earlier questions my lens can reach:

- **A gauge the user can't falsify by hand:** the bet and calibration gauges. Foreman states and settles those bets itself. The cheapest outside check is to settle a sample against git survival and print the raw rows.
- **Which jobs need to run on time:** assumption: only usage-limit resume and CI watch. Bet settlement has a 30-day window and the digest can be late.

- **Name the user-visible delta of each week** (the recent commits are almost all gauges, exams, ratchets and tick internals) — FEATURE — value 4 — effort S — risk low — category: product balance
  Why: T-2598 to T-2611 mostly change how Foreman measures itself, and few change anything the user types or sees. assumption: the user would want that ratio surfaced.
  Done when: `fm doctor` and the nightly digest print "user-visible commits: N of M this week" from a file-path rule, and a fixture week with only internal commits prints 0.

- **Age-stamp every maturing rate** — FIX — value 4 — effort M — risk low — category: measurement
  Why: T-2610 fixed this for bets only. Held-rate, trigger precision, lesson confidence (T-0217) and reopen rate also have outcomes that mature, and they can share the same flaw.
  Done when: each rate line prints "N too young to count", and a test with one item younger than its window shows it excluded and counted.

- **Link each user ask to the task it follows from** — FEATURE — value 4 — effort M — risk low — category: blind-spot detection
  Why: the eight missed asks (T-2534 to T-2566) each correct an earlier gauge or learner. No ledger says which shipped task spawns the most corrective asks.
  Done when: `fm intake` records a `follows:` task id, and a report lists the top 5 tasks by corrective-ask count from a fixture.

- **Type every drop reason** — FIX — value 3 — effort S — risk low — category: user model
  Why: the dropped ledger mixes "dismissed: folded into #22" with real rejections. Negative learning from it would punish ideas that were merely merged.
  Done when: each dropped row carries one of rejected, folded, superseded, mistaken or built, and non-goal derivation reads only rejected rows.

- **Prove the tower's DONE-WHEN can converge** — FEATURE — value 4 — effort M — risk med — category: termination
  Why: `fm genesis grow` only adds categories and never removes them, while "no empty cells" ends the run. Growth can outpace filling forever.
  Done when: `fm genesis check` prints empty cells, cells added by grow and the net trend per generation. A fixture where grow outpaces fill prints "not converging".

- **Census every loop's exit** — FEATURE — value 3 — effort M — risk low — category: autonomy
  Why: the tower, drive, usage-limit wait-out and brainstorm rounds all run "until success". Steer 3 forbids stopping for budget but not reporting a plateau.
  Done when: `fm doctor` lists each loop with its non-success exit. After N generations with no exam gain it prints a one-line plateau notice and does not stop.

- **Scan for held-out leakage before the final exam** — SECURITY — value 4 — effort M — risk low — category: exam integrity
  Why: scenarios are meant to stay unseen by Foreman's code, but nothing checks that skills, lessons or Seeds absorbed their text over generations.
  Done when: a planted held-out sentence in a skill file makes `fm exam run --final` refuse and name the file.

- **Sample a cross-family second read** — FEATURE — value 3 — effort M — risk low — category: verification
  Why: cold reads go Haiku, then Sonnet, so writer and reader share a model family. The codex and gemini adapters exist, but T-0336 live-verify is blocked. assumption: one adapter is usable.
  Done when: about 1 in 10 cold reads also goes to a non-Claude agent, and `fm doctor` shows the shared-pass rate. With no adapter it says "unmeasured".

- **Keep an aging question ledger** — FEATURE — value 3 — effort S — risk low — category: brainstorm hygiene
  Why: the "Questions earlier brainstorms left" about the tick recur across rounds and are never closed with evidence. The idea list is thousands of lines.
  Done when: each question has an id, an age and an answer or drop reason. Any question open for 3 rounds is filed as a task or dropped with a reason.

- **Rate the novel asks** — FEATURE — value 3 — effort S — risk low — category: blind-spot detection
  Why: the eight missed asks are the only evidence of a gap. assumption: a rising novel-ask rate means brainstorming is stale.
  Done when: asks with zero overlap against MASTER.md and the idea catalog are tagged "novel". The nightly digest prints a 4-week novel-ask rate and lists each new class once.

- **Add a publish ledger and revert for `fm genesis live`** — FEATURE — value 3 — effort S — risk med — category: outward actions
  Why: the standing rule publishes site data to main on every tower change, with no rate cap or rollback verb.
  Done when: each publish is logged, and `fm genesis live --revert` restores the previous data through `fm ship`'s gate. A test publishes twice and reverts once.

- **Wild: run an opposite-steer twin** — FEATURE — value 3 — effort L — risk low — category: portability
  Why: "wild": the 40-plus steers belong to one user. Running the gates with the key steers negated (such as "always ask") would show which behaviour is hardcoded to this user.
  Done when: a fixture run with 5 negated steers reports which gates changed behaviour and which did not.

- **Wild: board the zeros** — FEATURE — value 3 — effort M — risk low — category: observability
  Why: "wild": "no empty cells", "0 WARN" and "no regressions" can all read green while the check is dead. Plant one real instance of each in a scratch copy daily.
  Done when: the board shows each zero-capable gauge with the date it last read non-zero on a planted fault.

- **Wild: run a grandparent test on the final report** — FEATURE — value 2 — effort S — risk low — category: legibility
  Why: "wild": the steers use Mission, Seed, cell, lens and generation freely, and T-0795 asks for plain receipts.
  Done when: a tool-less child restates the report in two sentences, undefined terms are counted, and a ratchet fails if the count grows.

Next question: Which of Foreman's recurring outputs would the user fail to notice if they stopped for a month, and is that known from the user's behaviour or only assumed?
Next question: Which steer's wording promises more than its automatic check can verify, and who compares the two?
