# Brainstorm — lens: bold bets

- **Make every claim in a done report a clickable receipt** — FEATURE — value 5 — effort M — risk low — category: trust
  Why: the user's recurring need is "nothing is done without evidence fm ran itself", yet the final summary is still model prose. Assumption: summaries can drift from the ledger. Render the closing report only from ledger rows (criterion, run id, exit code, timestamp), and flag any sentence naming a file or test that has no matching ledger row.
  Done when: `fm done` on a fixture task prints a report where every pass claim carries a run id, and an injected unsupported claim is flagged.

- **Detect the user's hand-edits as intent signals** — FEATURE — value 4 — effort M — risk med — category: learning
  Why: assumption: when the user edits a file Foreman just wrote, that is the strongest correction signal and is rarer than their typed "no". Diff Foreman's last write against the file's next state, classify the change (rename, style, deletion, logic) and record it as a lesson candidate and a bench case.
  Done when: hand-editing a Foreman-written file produces a classified correction entry visible in `fm friction`.

- **Add a tier-escalation tripwire mid-task** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: tasks are tiered S/M/L at intake, but review passes found 3–7 issues per batch, suggesting some "S" work was really M. Track signals (files touched vs. brief, steps added, failed verifies) and when they exceed the tier's envelope, pause and re-tier, which turns on the matching gates and audit lenses.
  Done when: a fixture S task that touches 6 files triggers a re-tier note and the M gates apply from then on.

- **Verify the ground before building on it** — FIX — value 4 — effort S — risk low — category: integrity
  Why: four zero-byte git objects broke `git diff` while `fm doctor` passed. Add a preflight at brief focus that runs `git fsck --connectivity-only`-class checks and test-collection sanity, quarantining pre-existing breakage so it is not blamed on the task.
  Done when: a repo with a zero-byte loose object makes `fm doctor` fail naming the file, and focus records it as pre-existing.

- **Ship a guard "why and how to allow" receipt** — FEATURE — value 4 — effort M — risk med — category: guard UX
  Why: three false positives (`git stash list`, a heredoc edit, read-only python on state) in one pass. Each block should print the matched rule, the nearest safe rewrite, and a one-line exact-allow the user can grant. Every block is also appended to a corpus replayed as a precision gate. Never weakened, only sharpened.
  Done when: the three known false positives are allowed by replay cases, and a true positive still blocks with the explanation.

- **Merge the inbox into three pipelines and cut the rest** — CLEAN — value 4 — effort S — risk low — category: scope
  Why: the open inbox has ~20 items with heavy overlap (bench judge, regression court, shadow-user soak, counterfactual ledger, skill duels, sentinel). Assumption: they share one replay engine. Fold them into (1) replay and judge, (2) scouting (landscape, dependency watch), (3) delegation (lane subagents, debate, shadow plan). Cut the shadow-user soak and sentinel as duplicates of the regression court.
  Done when: the inbox lists ≤ 8 items, each mapped to one pipeline, and the cut items name their replacement.

- **Wild: Let Foreman rehearse the queue before the drive** — FEATURE — value 4 — effort L — risk med — category: dry run
  Why: the user asked for speed without losing cost or quality. A dry run in lane worktrees with stubbed children predicts file collisions between queued tasks, which gates fail first, and the spend. It then reorders and batches the queue. Assumption: collisions are the main cause of rework.
  Done when: a queue of three tasks touching one file gets reordered or batched with the predicted conflict named before any edit.

- **Wild: Keep a "cold start" test for the next session** — FEATURE — value 4 — effort M — risk low — category: continuity
  Why: crashes and context summaries repeatedly interrupt long drives. After each task, a tool-less child reads only the handoff files and answers "what is next, why, and what must not be touched". Mismatches against the real state are repaired in the handoff.
  Done when: a seeded handoff omission is caught and the child's answer matches `fm next` after repair.

- **Wild: Make Foreman state a time-travel database** — FEATURE — value 3 — effort L — risk med — category: observability
  Why: the user will keep asking "why did you do that". Store state as an append-only event log with periodic snapshots, so `fm at <time>` rebuilds the brief, ledger and queue as they were, and `fm rewind` restores a snapshot after a crash.
  Done when: after two mutations, `fm at` shows the earlier state and `fm rewind` restores it byte-identically.

- **Wild: Hold an idea settle court that closes the loop on brainstorms** — FEATURE — value 3 — effort M — risk low — category: meta-learning
  Why: the idea pool is huge and mostly duplicates. Each shipped idea carries its predicted value and effort. After 14 days, compare against actual usage, friction and spend, then score the brainstorm lenses by hit rate and re-weight which lenses run.
  Done when: `fm friction` shows a per-lens hit rate computed from at least one settled idea.

- **Price each gate by the failures it catches** — PERFORMANCE — value 3 — effort S — risk low — category: speed
  Why: the suite takes about 30 s and one flaky class failed under load. Log seconds spent and failures caught per gate, then order gates cheapest-first and run the expensive ones only when their inputs changed. Assumption: some gates rarely fail.
  Done when: `fm check` prints a cost-and-catch table and skips an unchanged-input gate with the reason shown.
