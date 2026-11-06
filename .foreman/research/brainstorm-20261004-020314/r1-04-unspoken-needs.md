# Brainstorm — lens: unspoken needs

- **Stop the drive on a stall-detector, not a turn cap** — FEATURE — value 5 — effort M — risk low — category: drive
  Why: the user keeps asking for "numerous multiple passes" and recursion, and 18 drive turns ended only to wait; the unspoken need is that endless self-improvement stops itself when returns vanish. Assumption: pass yield (accepted ideas, bench delta, review findings per pass) is already derivable from the ledger.
  Done when: a fixture of three passes with zero accepted items and zero bench delta makes `fm drive` stop and print the yield table, and a fixture with a positive delta continues.

- **Add a yield ledger per self-improvement pass** — FEATURE — value 4 — effort S — risk low — category: self-improvement
  Why: the user says "better better better" but nothing records whether pass 2 beat pass 1. Ideas so far lists ~300 items with no measure of how many shipped, were cut, or changed an outcome. Assumption: tasks carry a pass or origin tag.
  Done when: `fm friction` prints, per pass, ideas proposed, built, cut, bench delta and review issues found.

- **Cut the idea list to a ranked shortlist with a duplicate collapse** — CLEAN — value 4 — effort S — risk low — category: brainstorm
  Why: the "ideas so far" list repeats the same themes (flake quarantine ×6, doctor integrity ×5, bench ablation ×8, research cache ×5). The user said they want groundbreaking ideas, not volume, so near-duplicates waste each child's context and tokens.
  Done when: `fm ideas` clusters its prior list by BM25 similarity and passes one line per cluster to children, and the prompt shrinks by at least half on the current list.

- **Pin the "don't re-propose" list to what actually shipped** — FIX — value 3 — effort S — risk low — category: brainstorm
  Why: the pack's exclusion list mixes built, planned and merely proposed items, so children can't tell a dead idea from an open one. Assumption: the inbox and ledger know each item's state.
  Done when: each excluded idea carries a state tag (built, inbox, cut, proposed) generated from the ledger, and a test fails if a built item appears untagged.

- **Make reviewer findings a standing pre-review checklist** — FEATURE — value 4 — effort M — risk low — category: review
  Why: every review batch found 3–7 real issues, mostly new-parser edge cases and privacy of exported text, which is the same classes repeatedly. The implementer should be told them before writing, not after.
  Done when: `fm next` on a step that adds a parser or export shows the top three recurring finding classes, and a test confirms a past finding class is surfaced for a matching step.

- **Ask one question at the start of a long autonomous run, then never again** — FEATURE — value 4 — effort M — risk med — category: autonomy
  Why: the user sets "full autonomy" and also denied an `rm` of the dev-mods copy, so they want authority bounded in ways they haven't listed. Assumption: a short boundary interview (what is never auto-deleted, what is never pushed) would capture it.
  Done when: `fm drive` start prompts for the boundary list once, stores it as vetoes, and a later matching action is blocked with the stored reason.

- **Wild: Let the user grade a pass in one line and train the shortlist taste** — FEATURE — value 3 — effort M — risk low — category: taste
  Why: wild. The user's dropped and steered items (premise false, criterion widened) show consistent taste: measured over speculative, permanent checks over one-offs. A one-word grade per built item could weight future ranking.
  Done when: after `fm grade T-ID good|meh|bad`, the next `fm ideas` ranking demonstrably moves similar ideas up or down in a replay fixture.

- **Wild: Make Foreman audit its own premises before building a task** — FEATURE — value 4 — effort M — risk low — category: premise
  Why: wild. Two dropped items had a false premise, proved only after work started (ghost background tasks, replay skip). A cheap measurement of the claimed problem at intake would have saved those tasks.
  Done when: a brief whose context claims a measurable problem must record one measurement before step 1, and a fixture with a false premise gets flagged at intake.

- **Wild: Keep a "things the user never had to ask twice" scoreboard** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: wild. Steers are visible, but the absence of a repeated correction is the real success signal.
  Done when: the pane shows a count of corrections from the last month that never recurred, computed from the ledger.

- **Reconcile the open inbox into a cut list with reasons** — CLEAN — value 3 — effort S — risk low — category: planning
  Why: about 18 planned items overlap: second-Foreman review, debate pair, shadow plan review and regression court all serve "judge without tests". Merge them or cut some.
  Done when: the inbox shows each overlapping item either merged into a named pipeline or marked cut with a one-line reason.

- **Wild: Let a pass replay the last pass's fixes as a regression pack** — FEATURE — value 3 — effort M — risk med — category: recursion
  Why: wild. The adversary pass found a class the first missed; replaying the guard's earlier fixes against each new change would catch regressions like the one HIGH found.
  Done when: `fm check` replays a stored set of earlier review findings and fails if any reproduces.
