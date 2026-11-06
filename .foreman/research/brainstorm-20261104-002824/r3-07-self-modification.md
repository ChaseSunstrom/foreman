# Brainstorm — lens: self-modification

- **Bisect self-edits automatically** — FEATURE — value 5 — effort M — risk low — category: self-repair
  Why: assumption: the earlier ideas type, seal and revert each self-edit, but none says what to do when quality dips and nobody knows which of 20 edits did it. The replay exam over closed briefs and `fm outcomes` can be the oracle.
  Done when: `sampo selfedit bisect` takes a planted bad edit out of 16 typed self-edit commits in ≤4 replay runs and prints its id.

- **Test pairs of pending self-edits together** — FEATURE — value 4 — effort M — risk low — category: self-edit safety
  Why: assumption: every gate in the list judges one edit alone. Two edits that each pass can still conflict, for example a shorter note wording plus a tighter injected-line budget.
  Done when: with two seeded edits that pass alone and fail together, the combined replay fails and both are held.

- **Gate self-edits on the weakest model** — FEATURE — value 5 — effort M — risk low — category: local models
  Why: the standing steer is local models scaffolded to frontier results. An edit to an injected note or brief template that only helps the frontier model quietly widens the gap.
  Done when: a seeded edit that passes on frontier but breaks the smallest Ollama decision model's parse is rejected, with the model named.

- **Re-tune scaffolds when the served model changes** — PERFORMANCE — value 4 — effort M — risk low — category: local models
  Why: the pack says a llama-swap switch costs about 3 min and the 27B and 35B MoE differ. Scaffold settings tuned for one go stale silently on the other.
  Done when: changing the model hash behind a profile files a re-bench task, and the scaffold rung choice shows the model hash it was tuned on.

- **Put a lease on every self-edit** — FEATURE — value 4 — effort S — risk low — category: self-edit lifecycle
  Why: assumption: edits only get added. A lease of 14 days means the edit reverts unless an outcome reading re-earns it, which fits the lean steers and the "pending measurement" rows that never resolve.
  Done when: a seeded edit with no supporting reading reverts at day 14, and one with a reading renews.

- **Make the explain-back gate** — FEATURE — value 4 — effort M — risk med — category: legibility
  Why: unattended night edits reach the user as a morning digest. If a cold local child, given only the plain-words summary, can't reconstruct the diff's file set and intent, the user couldn't review it either.
  Done when: an edit whose summary misses a touched file is held, and one that matches releases.

- **Set edit quiet hours** — FEATURE — value 3 — effort S — risk low — category: self-edit governance
  Why: assumption: self-edits that land while the user is mid-task, or just before a `fm ship`, confound the outcome and cause surprises. Hold edits until after the user's presence window.
  Done when: no self-edit applies while a session was active in the last N minutes; the hold shows in `fm next`.

- **Govern the edit rate by revert rate** — FEATURE — value 3 — effort S — risk low — category: self-edit governance
  Why: reverts are already a ledger signal. If more than 1 in 4 recent edits reverted, the proposer should slow, then stop, so it can't churn overnight.
  Done when: replaying a ledger with a 40% revert rate drops the night's edit cap from its default to 1, with the reason printed.

- **Cap what the editor can touch with a time-lock** — SECURITY — value 4 — effort M — risk med — category: self-edit safety
  Why: edits to the self-edit pipeline, judge or manifest are the highest-risk class. They should need a 48-hour visible delay and the user's one-key ack, beyond "freeze the judge".
  Done when: a seeded edit to the pipeline stays pending for 48 h and never applies without the ack.

- **Wild: Delete a new feature on day 3 if unused** — FEATURE — value 3 — effort M — risk med — category: lean — wild
  Why: assumption: the lean steers say additions need earned measurement. A birth-day deletion proposal files itself with a one-key keep, so unused features lose by default instead of lingering.
  Done when: a feature with zero session-path calls in 3 days gets a deletion patch filed with a keep key.

- **Wild: Run a test-only night** — FEATURE — value 4 — effort M — risk low — category: self-repair — wild
  Why: the only change allowed to land unattended is a new regression test derived from the user's corrections that day. The code changes wait for the morning.
  Done when: a night run applies only files under `tests/`, each red on the pre-fix state, and the morning card lists them.

- **Wild: Let a local model keep a rival Sampo** — FEATURE — value 3 — effort L — risk med — category: local models — wild
  Why: the 27B role-plays a rewrite of one module each week. The live code is scored against it on closed briefs, and it is never merged, only compared. Steers favour wild ideas and use of idle local hardware.
  Done when: the weekly rival's score against live appears in `fm doctor`, with the module and the margin.

- **Wild: Seal a self-edit prediction in a sentence** — FEATURE — value 3 — effort S — risk low — category: calibration — wild
  Why: every edit carries "the user will re-ask X less", sealed before it applies and settled at +14 days. A running Brier score then says whether the self-editor is learning or just busy.
  Done when: a settled edit shows its sealed sentence and hit or miss, and the Brier score prints in the morning card.

Next question: which self-edit surfaces have the oracle needed to bisect and revert them (replay exam, outcomes), and which edit only on belief?
Next question: does the user read a morning self-edit digest at all, or only the first line of it?
