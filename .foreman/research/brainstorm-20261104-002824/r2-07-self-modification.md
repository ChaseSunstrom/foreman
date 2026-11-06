# Brainstorm — lens: self-modification

- **Land every self-edit as a typed commit with a sealed prediction** — FEATURE — value 5 — effort M — risk low — category: provenance
  Why: assumption: edits to skills, prompts, thresholds and rules are scattered, with no single record of what changed, why, and what it should do. `Self-edit:` commits carry the trigger signal, the before and after hashes, and one predicted effect, such as "re-asks of X fall". They are settled at 14 days against `fm outcomes`.
  Done when: `git log --grep '^Self-edit:'` lists every edit made overnight, and each has a settle line after 14 days.

- **Freeze the judge during a self-edit** — SECURITY — value 5 — effort S — risk low — category: self-guard
  Why: assumption: a tuner that raises its own hit rate can edit the measure that scores it. Files an Exam reads are hashed before the edit, and any edit that changes them is refused.
  Done when: a planted edit touching an Exam's measure file is rejected by a test.

- **Give the tuner a sealed holdout week** — SECURITY — value 5 — effort S — risk low — category: Goodhart
  Why: the repo has unit tests but no outcome signal the tuner can't see. The predictor tuner backtests on weeks A to C. Week D is sealed, and promotion needs lift over the recency baseline on D, read once.
  Done when: promoting a tuned predictor writes one D reading, and a second read of D is refused.

- **Edit data, never code, overnight** — FEATURE — value 5 — effort M — risk low — category: safe-mutation
  Why: the user is asleep and wants progress by morning. Anticipation rules become table rows (event, ask template, evidence, expiry) that the tuner may write while the code stays frozen. Rows expire in 14 days unless a hit renews them.
  Done when: an overnight run changes only rows, `git diff -- plugin/lib` is empty, and a stale row disappears on its own.

- **Hold self-edits for a morning digest with per-edit revert** — FEATURE — value 4 — effort S — risk low — category: user control
  Why: prompts must not shift under a running session. Edits queue in a staging area and land at the next SessionStart. The morning card says "I changed 3 things about myself", each with a one-key revert.
  Done when: no `Self-edit:` commit lands during an open session, and `fm` reverts one edit by its id.

- **Replay old vs new brief templates on closed briefs** — FEATURE — value 4 — effort M — risk low — category: self-eval
  Why: draft quality is judged by the user's rewrites. A template edit is replayed through the local 27B on the last 20 closed briefs. It must raise the share whose Exam parses and runs.
  Done when: an edit that lowers that share is refused, with both counts printed.

- **Compile frontier traces into local scaffolds** — FEATURE — value 5 — effort L — risk med — category: local models
  Why: steer: local models scaffolded to frontier results. Each closed frontier-model task of a kind is distilled into a checklist plus two few-shot examples per task kind and per local model. A scaffold stays only if the local pass rate on closed tasks rises.
  Done when: `fm` shows per-kind pass rates for the local model with and without the scaffold, and one scaffold clears the bar.

- **Remember rejected self-edits and stop proposing them** — FEATURE — value 3 — effort S — risk low — category: memory
  Why: the same rewrite can be proposed nightly. A graveyard stores each reverted patch with its reason, and near-matches by shingle similarity are skipped.
  Done when: a re-proposed reverted edit is skipped and logged with the graveyard id.

- **Cap unsettled self-edits** — CLEAN — value 3 — effort S — risk low — category: edit debt
  Why: attribution breaks when many edits are live at once. No new self-edit is staged while more than 3 are unsettled, so a regression can be traced to one edit.
  Done when: a fourth staged edit is queued, not applied, and the morning card names the three unsettled ones.

- **Tier self-edit surfaces with promotion clocks** — SECURITY — value 4 — effort M — risk low — category: authority
  Why: assumption: rows, prompts, skills, hooks and the guard all carry different risk. Data needs one check, prompts need a replay, skills need a cross-family read, and hooks and the guard are never self-edited. A surface moves up a tier only after 30 days of clean settles.
  Done when: a table maps each path to a tier, and a test fails if a self-edit touches a path above the tuner's tier.

- **Keep self-written skills in a personal overlay, not core** — CLEAN — value 4 — effort M — risk low — category: lean
  Why: a standing lean rule applies. Skills and recipes generated from the user's repeated asks go to `~/.local/share/sampo/overlay`, are listed by `fm`, and are promoted to core only by the user.
  Done when: a generated skill never appears in `git status` of the repo, and removing the overlay dir removes it.

- **Wild: breed lens prompts** — FEATURE — value 3 — effort M — risk med — category: brainstorm
  Why: wild. Lens prompts are genomes. Between rounds, each lens mutates one sentence and is kept only if its ideas survive grounding at a higher rate. The lineage is stored.
  Done when: after 3 rounds one lens prompt differs from its seed and has a recorded survival delta.

- **Wild: duel today's build against a 30-day-old self** — PERFORMANCE — value 4 — effort M — risk low — category: regression
  Why: wild. A pinned old install and the current self-edited one run the same held-out closed tasks on the local 27B. If "improvements" fail to beat the old build, the scorecard says so.
  Done when: `fm` prints a win/loss table by task kind, old against new.

- **Wild: add a fuse that reverts to last-good after two interrupts** — FIX — value 4 — effort M — risk med — category: safe mode
  Why: wild. Interrupts after Foreman output are the felt-cost signal (asked about earlier). If the user interrupts twice within an hour of a self-edit landing, all edits from the last day revert and a card says why.
  Done when: simulating two interrupts after a landed edit reverts it and logs the trigger.

Next question: which self-edit would the user veto on sight, and can their past drops and reverts predict that veto before the edit is staged?
Next question: does a self-edit's measured effect at 14 days survive once the user's own behaviour shifts in response to the edit?
