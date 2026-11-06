# Brainstorm — lens: the irreversible door (invented): it stops for the user only when a step is irreversible and ambiguous; everything else is decided, recorded and reversible

- **Freeze the door's meaning at ask time** — FEATURE — value 4 — effort M — risk med — category: consent
  Why: assumption: a stop-and-ask can be approved against a command whose effect later shifts (a path resolves differently, a remote changes). Earlier ideas classify doors but none bind the approval to a snapshot.
  Done when: an approval records the resolved target (absolute paths, remote URL, branch sha) and a test shows the step refuses to run if any of them differ at execution.

- **Make "ambiguous" a vote, not a feeling** — FEATURE — value 4 — effort M — risk low — category: judgment
  Why: the request asks Foreman to stop only when "irreversible and ambiguous"; the pack has plan-reading disagreement ideas but no rule that fires the stop. Assumption: ambiguity can be measured by 3 cheap tool-less reads of the user's words disagreeing on the action's target or scope.
  Done when: a fixture where 3 reads give different scopes for `delete the old ones` yields an ask, and one where they agree yields a recorded decision with no ask.

- **Ship `fm doors` as the single list of one-way steps** — FEATURE — value 4 — effort M — risk low — category: guard
  Why: the guard (USER_ONLY_FM, T-2252) and the push grant already hold separate door lists; assumption: they drift. One table feeding the guard, plan gate and drive prevents that.
  Done when: a test fails if the guard denies a verb that `fm doors` calls reversible, or the reverse.

- **Make each one-way step carry a precomputed "what you lose" line** — FEATURE — value 3 — effort S — risk low — category: ask quality
  Why: assumption: when Foreman does stop, the user must dig for the stakes. The ask should say the loss in one sentence and give the default.
  Done when: every `fm ask` of kind irreversible includes loss, default, and a deadline, and a test rejects one without.

- **Decide-and-receipt for every reversible fork** — FEATURE — value 4 — effort M — risk low — category: audit
  Why: the standing request ("everything else it decides and records") lacks a ledger the model cannot write. Assumption: decisions currently sit in task prose.
  Done when: a hook-written receipts file lists each auto-decision with its undo command, and `fm doctor` flags a decision made with no receipt.

- **Reclassify a door when its inputs change mid-run** — FIX — value 3 — effort M — risk med — category: safety
  Why: assumption: a step marked reversible (e.g. edit on a branch) becomes one-way after a merge, push or publish grant spends. Nothing in the pack rechecks.
  Done when: a test where a task's branch is pushed mid-run upgrades later edits to that file's door class and triggers the stricter path.

- **Have a cold child try to reverse each shipped change** — FEATURE — value 3 — effort L — risk med — category: verification
  Why: "reversible" is claimed by the writer. Matches the open question about verbs with a model on both sides and no user-owned check. Assumption: a throwaway worktree can test undo lines.
  Done when: for a sample of receipts, running the undo line in a copy restores the pre-change tree hash, and failures are listed in `fm doctor`.

- **Price the ask: show what waiting costs** — FEATURE — value 3 — effort S — risk low — category: ask quality
  Why: assumption: stops block lanes. A parked-row mechanism exists in ideas but no cost line saying which other rows continue and which wait.
  Done when: an ask lists rows still running, rows blocked, and the minutes idle so far.

- **Treat silence as consent only for two-way doors** — FEATURE — value 3 — effort M — risk med — category: consent
  Why: the steer "stop only when irreversible and ambiguous" implies timeouts; assumption: today a timeout is uniform. A timeout on a one-way door must park, never proceed.
  Done when: a test shows an unanswered ask on a push door leaves the row parked after the deadline, while a reversible one proceeds on its default.

- **Wild: Door map overlay on the web UI repo tree** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: wild. Colour every file, remote and service by how hard a mistake there is to undo, so the user sees where Foreman will stop before it starts.
  Done when: the web page renders a tree with three door colours drawn from `fm doors`, and a keyboard-accessible legend.

- **Wild: Dress-rehearsal mode for one-way steps** — FEATURE — value 4 — effort L — risk med — category: rehearsal
  Why: wild. Before asking, run the step on a copy (database, release, force-push to a bare clone) and attach the diff to the question, so the ask becomes "approve this result".
  Done when: for a migration and a branch delete, the ask includes a rehearsal diff and the real step runs only after approval.

- **Wild: A "second key" from a different vendor's model** — FEATURE — value 3 — effort M — risk med — category: judgment
  Why: wild. For a one-way step the user is away from, require a cold model from another family to agree; disagreement parks the step. It is not consent, only a veto.
  Done when: a staged disagreement parks a push; agreement still waits for the user's grant where one is required.

- **Wild: Regret drill that replays last week's auto-decisions** — FEATURE — value 3 — effort M — risk low — category: learning
  Why: wild. A nightly cold child reads the receipts with later outcomes (reverts, reopens) and names the decisions that should have been asks, tightening the door table.
  Done when: the drill outputs a list for a fixture week with one planted bad decision, and it flags that decision.

Next question: Which of Foreman's existing grants (push, publish, mandate) have no recorded expiry or spent-on-use check, and could a stale one open a one-way door unasked?
Next question: When two doors are individually reversible but irreversible in combination (delete branch plus prune reflog), who classifies the pair?
