# Brainstorm — lens: simplicity

- **Auto-draft the lesson at done; confirm or skip** — CLEAN — value 4 — effort S — risk low
  Why: `fm task done` requires a hand-written lesson for every M/L task, and the pack has no sign that these lessons are read later. Checkpoints already record "ruled out:" lines, failures met, and user corrections.
  Done when: `fm task done` on an M task with a failure or correction in its log pre-fills a one-line lesson from that log. On a clean-pass task it needs no lesson, and a test covers both cases.

- **Derive tier from the tree, with a one-way ratchet** — CLEAN — value 4 — effort M — risk med
  Why: tier (S/M/L) is chosen by hand, and `fm focus` refuses briefs that aren't planned for their tier. Foreman already has the inputs: the recall tier hint, scope-glob count, hot files, security paths, and the effort of similar tasks. Assumption: today's tier choice is often wrong or wasted deliberation.
  Done when: `fm task new` proposes a tier from scope size and risk signals. At done, tier can only be bumped up when the real diff exceeds it, and the bump prints the gate it adds. A replay over past briefs agrees with the recorded tier at least 80% of the time.

- **Pick audit lenses from diff signals, not tier** — CLEAN — value 3 — effort S — risk low
  Why: security paths already force the adversary lens, but the tier-to-lens table still exists alongside that special case. Generalising the special case removes the table.
  Done when: `fm audit prep` lists lenses chosen by rule. Tests-only diffs get none, perf-tagged diffs get the perf lens, and security paths get adversary. The tier-to-lens table is deleted and the review brief shrinks on tests-only diffs.

- **Replace cost/usage/digest with one incremental transcript scan** — CLEAN — value 3 — effort M — risk low
  Why: `fm cost`, `fm usage`, `fm digest` and the weekly SessionStart line each read transcripts. Assumption: they parse them separately and rescan from the start.
  Done when: one scanner keeps a byte-offset cache per transcript, and the three commands become views over it. A second run over unchanged transcripts reads zero new bytes, and output is identical to before.

- **Make prove, sentinel, evals add and `--affected` modes of one stored check** — CLEAN — value 3 — effort M — risk med
  Why: each criterion's verify command is now re-run by four separate features (`fm task prove`, `fm sentinel`, `fm evals add`, `fm check --affected`). Each has its own code path and its own flakiness and timeout handling.
  Done when: there is one check record per criterion, with its command, start-tree result and last-green tree. The four features call it, and net lines in plugin/lib drop while the 474 tests still pass.

- **Give lessons hit counts and auto-retire the ones that never fire** — CLEAN — value 3 — effort S — risk low
  Why: lessons feed recall, tripwires and cross-project sharing, and they grow with every M/L task. Without retirement they add noise to injections and to the 2,000-char SessionStart budget.
  Done when: each lesson counts recalls and tripwire hits. A lesson with zero hits after N finished tasks, or one that contradicts a newer decision, is archived by `fm doctor`. Its recall entry disappears, and the per-project lesson count stays under a set cap.

- **Give brainstorm packs only the nearest already-considered ideas** — PERFORMANCE — value 3 — effort S — risk med
  Why: this pack carries about 150 already-considered titles as prose, and every lens child pays for them on every round. Assumption: most are irrelevant to any one lens.
  Done when: `fm ideas` stores considered titles as records and includes only the top 15 by BM25 match to the lens, plus the total count. Pack size drops by at least 40%, and a replay shows no increase in duplicate ideas.
