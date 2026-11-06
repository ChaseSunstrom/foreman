# Brainstorm — lens: unspoken needs

I answer one earlier question first. Asked what the user would want when a private goal needs a remote-only capability, their pattern points to `fm ask` once, with the default recorded as a costly decision. They have repeatedly said not to block on process questions, so the ask should happen once per goal and not per step.

- **Run a criterion's own examples against its rule at birth** — FEATURE — value 4 — effort S — risk low — category: criteria
  Why: T-2583's criterion says "8+ characters" but its own example "4% lost" has 7, and a human had to catch it. T-2606 and T-2341 were also corrected after filing.
  Done when: `fm task new` with a DONE-WHEN whose quoted example fails its stated threshold is refused, naming the example and the rule.

- **Show "last seen red" on every prover verdict** — FEATURE — value 4 — effort M — risk low — category: trust
  Why: assumption: the user's recurring worry is a gauge that reads green while broken (T-2533, T-2554). A green from a prover never seen failing is the weakest kind.
  Done when: a verdict line reads "green, prover last red 12d ago on fixture X" or "never seen red" for any prover with a recorded planted-fault run.

- **Calibrate the "unproven" label against later reopens** — FEATURE — value 4 — effort M — risk low — category: calibration
  Why: the user asked for unproven things to be labelled, but nothing shows the label predicts anything. T-2610 shows calibration reads are already trusted elsewhere.
  Done when: `fm outcomes` prints the 30-day reopen rate for proven vs unproven finishes, with counts, once at least 20 of each are settled, and says "insufficient" below that.

- **Keep user-signed risk acceptance apart from unproven** — FEATURE — value 3 — effort S — risk low — category: ledger
  Why: assumption: the user will eventually want to say "I know, ship it" without that claim being nagged or counted as a hole. It should carry a reason and an expiry.
  Done when: `fm task finish` lists "unproven (N) / accepted by you (M, expires …)" separately, and an expired acceptance reappears as unproven.

- **Check that a revert restores the earlier proof state** — FEATURE — value 3 — effort M — risk med — category: undo
  Why: assumption: the user will revert often (they steer abruptly), and a revert is a change nobody proves.
  Done when: after `git revert` of a closed task, the proof ledger shows the pre-task verdicts re-run and matching, or names each one that differs.

- **Show an ETA before a long proof starts** — PERFORMANCE — value 3 — effort S — risk low — category: wait
  Why: the bench and the exams are slow and run unattended (T-2605), and the user has no idea how long a wait will be. Per-command durations are already in the ledgers.
  Done when: `fm prove` and `fm flow` print "usually 90s (median of 7)" before running, and say "no history" when there is none.

- **Name where the sentence and the proof parted after a dispute** — FEATURE — value 4 — effort M — risk med — category: meaning
  Why: "does it do what the user meant" is the stated request, and the failure point is a later "that's not what I meant". T-2613 shows false dones on names the goal never states.
  Done when: `fm dispute T-N "<words>"` prints the user's original phrase, the claim the proof covered, and the first noun or number in the user's phrase the proof never touched.

- **Render shots under the user's real desktop settings** — FEATURE — value 2 — effort M — risk low — category: ui proof
  Why: assumption: the user runs a hardened Arch setup with their own scale, theme and fonts. T-1217 (pane colour mismatch) shows terminal-specific rendering already bites.
  Done when: `fm shot` records the scale, theme and font it used, and a second run under different settings is reported as a separate baseline.

- **Wild: set aside a verification reserve for disputed finishes** — FEATURE — value 3 — effort M — risk low — category: budget
  Why: wild: proof effort is spent before finish, when it is least informed. Holding back a fixed share for the week after, when a dispute shows where the risk really was, matches the user's reopen pattern.
  Done when: a disputed finish can spend its reserve on a deeper prover, and the reserve's use is shown in `fm cost`.

- **Wild: dim the web UI as proof goes stale** — FEATURE — value 2 — effort S — risk low — category: ambient
  Why: wild: "commits landed, no proof ran" is invisible until someone looks. A repo card that desaturates by days since its last run gives a glance-level dead man's switch.
  Done when: the web UI card for a repo with 5+ commits and no proof run in 7 days is visibly desaturated and carries a "last proved: date" caption.

- **Wild: let the user's "not what I meant" mint a red fixture** — FEATURE — value 4 — effort M — risk med — category: regression
  Why: wild: each dispute is the most valuable test case Foreman ever gets, and today it only becomes a conversation. Related to, but not the same as, the existing "missed ask → probe".
  Done when: a dispute produces a fixture that fails on the disputed commit and passes on the fix, and a later regression is caught by it.

Next question: Which Foreman verdicts has the user ever overruled by hand, and does any prover's verdict agree with their overrule better than with Foreman's own call?
Next question: If the user stopped reading finish receipts entirely for a month, which single line would they most regret not having read?
