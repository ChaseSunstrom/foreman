# Brainstorm — lens: unspoken needs

- **Show a "what I need from you" desk, ranked by what each item blocks** — FEATURE — value 5 — effort M — risk low — category: user-blockers
  Why: T-0325, T-0335, T-0352, T-0418 are blocked for months on user-only actions (sudo pacman, publish), and the standing rule says "if a cap only the user can raise stops the work, say which once with fm ask". Nothing aggregates them; the user must remember. Assumption: the user would clear them in one sitting if listed with the exact command.
  Done when: `fm next --blocked-on-me` prints each user-only blocked task with the one command or decision that frees it and the count of tasks behind it, in descending order.

- **Draft the steer the user is about to give from a repeated correction** — FEATURE — value 4 — effort M — risk med — category: learning
  Why: The pack shows steers like T-2583's "8+ characters vs 7" fixed by user correction and many Genesis steers restating the same themes (lean, outside signals, no blocking). Repeat-correction classes recur. Assumption: a third occurrence of a correction class is detectable from the steers ledger.
  Done when: after the second correction of the same class, Foreman files a proposed standing rule plus its check with one-key accept, and a fixture with two planted corrections produces it.

- **Print a "while you were away" card at session start with money, closes and stops** — FEATURE — value 4 — effort S — risk low — category: return-brief
  Why: The user runs long unattended drives (--stall-usd, pace off, budget $200) and told Foreman not to block on them; what they need on return is spend, tasks closed, why it stopped, and what was held. Assumption: the receipt data exists across fm run, burden and outcomes.
  Done when: SessionStart after a gap over 4 hours prints ≤8 lines: dollars spent, tasks closed, stop reason, items awaiting the user; a test with a fixture ledger asserts it.

- **Quote the user's own words beside every "Foreman-filed" item** — FEATURE — value 4 — effort S — risk low — category: provenance
  Why: The "what earlier brainstorms missed" list shows slate-origin items are indistinguishable from user asks (T-2659 label ask). The user needs to know whose idea a task is. Assumption: filing source is recorded.
  Done when: `fm next` and `fm show` tag each task as user-asked, steer-derived, or self-filed, with the originating sentence for the first two.

- **Warn when a new request contradicts a standing steer, before work starts** — FEATURE — value 4 — effort M — risk med — category: steer-conflicts
  Why: 40+ steers now in force (e.g. "never block on the user" vs "say which once with fm ask"; round-first holds vs urgency). Conflicts will surface mid-run as surprise. Assumption: steers are searchable text.
  Done when: filing a task whose title/brief matches two steers with opposing verbs prints both and which one wins by recorded precedence; a fixture of the known conflicting pair triggers it.

- **Give every unattended stop a single plain-language reason line on the status surface** — FEATURE — value 4 — effort S — risk low — category: legibility
  Why: Stops now come from stall-usd, usage limit waits, round-first holds, cold-read gates, pace off. Users must reconstruct why nothing is happening. Assumption: reasons are scattered across receipts.
  Done when: `fm status` prints "idle because: <reason> (releases when: <condition>)" for each of six known stop causes, tested with fixtures.

- **Mark the cost of each standing rule in injected tokens and blocked actions** — FEATURE — value 3 — effort M — risk low — category: steer-cost
  Why: fm burden --by-source (T-2667) now measures injection by source; the user keeps adding steers without seeing their weight. Assumption: steers are injected at session start.
  Done when: `fm steers --cost` lists each steer with characters injected per session and times its check fired in 30 days.

- **Verify a pasted outside claim against the repo before it enters a brief** — FEATURE — value 3 — effort M — risk low — category: grounding
  Why: Dropped items repeatedly "mostly built" (fm replay, fm usage --prune, check_predictions); the user had to re-ground. Assumption: grounding can be mechanized by greping verbs and help strings.
  Done when: a brief naming "fm tidy --verbs" is auto-annotated "similar: fm usage --prune (fmcost.py:1480)" at filing, tested on three known dropped examples.

- **(wild) Write the user's reply before they do** — FEATURE — value 3 — effort M — risk med — category: prediction
  Why: assumption: the user's accept/drop history is a stable signal. Predict accept/drop on each slate item, show the guess, then score it when they answer.
  Done when: a slate prints predicted verdicts and `fm exam` reports hit rate against the actual drops in the pack's history (above chance).

- **(wild) Print a monthly "things I decided for you" ledger with a one-key veto** — FEATURE — value 4 — effort S — risk low — category: delegated-decisions
  Why: the standing rule "never block on the user; record with fm decide --kind costly" means many decisions land in a final report the user may not read until late. Wild: a weekly digest with reversal cost and a veto key.
  Done when: `fm decisions --since 7d` lists costly decisions with reversal cost and `fm decisions veto ID` files the reverting task.

- **(wild) Leave an "if I vanish" file per long run** — FEATURE — value 3 — effort S — risk low — category: resilience
  Why: the user is running multi-generation unattended work; a crash or their absence leaves no single entry point. Wild: one file naming how to stop, resume, and where the money went.
  Done when: starting `fm run` writes `RESUME.md` in the state dir with the stop, resume and spend commands, and it updates on each task close.

- **Notice when the user re-runs a proof command by hand and treat it as distrust** — FEATURE — value 3 — effort M — risk med — category: trust-signal
  Why: the transcript bash-input channel exists (noted in dropped ideas); a hand re-run after "proven" shows the receipt was not enough. Assumption: bash-input records are readable.
  Done when: a fixture session where the user re-runs a task's prove command within an hour yields a "distrust" row in `fm outcomes`.

Next question: Which of the user's silences (items never opened, receipts never read) are signal that something is wrongly presented, rather than fine?
Next question: What does the user do in the first five minutes after a long unattended run, and does any surface support that exact routine?
