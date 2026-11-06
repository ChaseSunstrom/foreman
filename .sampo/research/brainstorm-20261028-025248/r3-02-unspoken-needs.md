# Brainstorm — lens: unspoken needs

- **Expand "etc." into the siblings it implies, and list them before the first write** — FEATURE — value 4 — effort S — risk low — category: request scope
  Why: "I want any and ALL ideas implemented" and "etc." read as an open set, but the request names only one item. Assumption: the user means the sibling items of the one they named. Listing them makes the scope visible without asking.
  Done when: a request ending in "etc." produces a sibling list in the receipt before the first file is written, and no question is asked.

- **Escalate a request the user has sent twice to the top of the queue** — FEATURE — value 4 — effort S — risk low — category: request priority
  Why: "Cut Foreman's usage burn" was sent, dropped, then recreated, and "Push foreman/build to main" came back as a redo. A re-send is the strongest signal the user gives, and the queue doesn't treat it as one.
  Done when: a second copy of an earlier request moves to the front of the queue, and its receipt says it was a re-send and why it was moved.

- **Mark a finding settled so later sweeps stop re-filing it** — FEATURE — value 4 — effort S — risk low — category: sweep hygiene
  Why: the hook-bench p95 finding was dropped after a quiet-machine rerun disproved it, and the CI-red alarm was raised again after it had been a false alarm. Sweeps re-raise closed findings because nothing records that they were settled.
  Done when: a sweep that re-finds a settled finding files nothing unless the inputs it depends on (commit, model, budget) have changed, and the sweep log names the settled record it skipped.

- **Answer "did I already decide this?" from the user's own past words** — FEATURE — value 4 — effort M — risk low — category: decision memory
  Why: several dropped items came back in new words, such as the midnight defer bug and the `fm` not-found question. Assumption: the user would rather see their earlier decision with its date than be asked again.
  Done when: asking whether something was already decided returns the user's original quote, its date and the task id in one reply.

- **Ship a cheap first slice of every large request, with the rest queued behind it** — FEATURE — value 4 — effort M — risk low — category: cost pacing
  Why: "full force, but efficient, to not burn tokens" asks for both breadth and frugality, and large asks such as the usage-burn and playbook-scale requests run to the whole budget in one go. Assumption: a usable first slice lands sooner and keeps the rest from consuming the weekly budget unseen.
  Done when: a request above a cost threshold is split into a first slice that closes and a queued remainder, and the receipt shows the spend of each slice.

- **Give each queue a departure card before the user walks away** — FEATURE — value 4 — effort S — risk low — category: unattended safety
  Why: the user keeps saying "just go" and "don't ask me", which means they leave runs going. Nothing currently lists, in one place, what the run may do alone, its spend cap and what is waiting on them.
  Done when: starting a queue with the user marked away prints one card with the unattended actions allowed, the spend cap, and the blocked items that need them, and the card is in the journal.

- **Wild: a one-key nod that banks the last result as a standing pattern** — FEATURE — value 3 — effort S — risk low — category: approval signal
  Why: the user gives feedback mostly by pushing back, which is costly. Assumption: a silent positive signal lets Foreman learn which defaults were right without a question. Wild.
  Done when: pressing the nod key after a receipt records the choices in that receipt as approved, and the next run of the same kind uses them with the receipt naming the precedent.

- **Wild: a question coin wallet with three coins a week** — FEATURE — value 3 — effort M — risk low — category: question budget
  Why: the user has said not to be asked for permission, so each question should have a price. Assumption: a fixed weekly allowance makes Foreman choose its questions carefully. Wild.
  Done when: each question Foreman asks spends one coin, questions with a default ask nothing, and the weekly receipt shows coins spent and what each one bought.

- **Wild: a Monday rehearsal that replays the user's last ten requests in a sandbox** — FEATURE — value 3 — effort L — risk med — category: self-audit
  Why: "I shouldn't have even had to tell you" means the user wants Foreman to catch its own misreads before they do. Assumption: rerunning recent asks against today's rules shows which decisions would now change. Wild.
  Done when: each Monday a sandboxed replay of the last ten requests reports, per request, which decisions differ from the original run, and the report is one screen.
