# Brainstorm — lens: user value

- **Autocomplete the next request from the user's accepted asks** — FEATURE — value 4 — effort S — risk low — category: request intake
  Why: the user's own words repeat the same asks (the "Cut Foreman's usage burn" request was dropped and recreated; "push to main so the site publishes" came back). Assumption: accepted requests are a good template for the next one.
  Done when: typing "push" in the prompt offers the last accepted push request with its target branch pre-filled, and Enter sends it unchanged.

- **Close the tasks your own commits already finished** — FEATURE — value 4 — effort S — risk low — category: backlog hygiene
  Why: the user pushed `a5b5cf7e` by hand and the "push foreman/build" task went stale until a redo. Evidence: "work done (pushed a5b5cf7e, site deployed)" sat as an open item.
  Done when: a queued task whose acceptance check already passes at HEAD shows as "looks done, close?" in `fm status`, and one key closes it with the proof attached.

- **Answer a blocked question from chat, not only from `fm answer`** — FEATURE — value 3 — effort S — risk med — category: unblocking
  Why: the user answers questions in conversation, and blocked items stay open after the answer was already given. Assumption: the chat answer is unambiguous only when it names the item.
  Done when: a chat reply that names a blocked item's question marks it answered in the journal, and an ambiguous reply asks once for the item's ID.

- **Say what this request will not touch** — FEATURE — value 3 — effort S — risk low — category: scope control
  Why: the user wants all ideas done with no permission asks, so surprises cost trust. Assumption: a stated out-of-scope list catches overreach earlier than a diff review.
  Done when: each new request's pack and first pane card list its explicit non-goals, and a close that touches a listed non-goal is flagged before the receipt.

- **Time-box a request by wall clock, not only by cost** — FEATURE — value 3 — effort S — risk low — category: effort limits
  Why: the user asked for efficiency and not burning usage, but spend caps don't bound how long a run holds the machine. Assumption: the user cares about elapsed time as much as tokens.
  Done when: `fm task ... --for 40m` stops at 40 minutes, closes with the proof reached so far, and lists the remaining steps.

- **Turn a bug screenshot into a failing test** — FEATURE — value 3 — effort M — risk med — category: bug intake
  Why: the user reports UI problems by describing or pasting what they see (pane key behaviour, stalled-card colours). Assumption: most screenshot bugs reduce to one visible state that a test can pin.
  Done when: attaching an image to a request produces a task whose first step is a test that fails on the current build and passes after the fix.

- **Pre-answer the question a reader will ask next** — FEATURE — value 3 — effort S — risk low — category: close receipts — wild
  Why: wild — the user keeps asking "why" (why fm isn't found, why usage burned). Each close could answer the likely follow-up in one line before it is asked.
  Done when: every close ends with one "you'll probably ask" line that is accurate against the journal, and a test fails if the line is missing.

- **Mulligan: redo a finished request with one word changed** — FEATURE — value 3 — effort M — risk low — category: redo flow — wild
  Why: wild — the user often re-words a request to get a different result ("Cut Foreman's usage burn" was reissued with a new interpretation). A side-by-side of both attempts beats a second guess.
  Done when: picking "mulligan" on a closed task reruns it with the edited request in a scratch worktree, and the pane shows both results side by side with their gates.

- **Rate each close with one key, and let ratings set the next receipt** — FEATURE — value 3 — effort S — risk low — category: feedback loop — wild
  Why: wild — the user has pushed back on length and noise ("don't ask me for anything either"), but only in prose. A single thumb per close gives a direct signal.
  Done when: after 10 ratings, the next close's length matches the median rating, and the rating history is shown in `fm digest`.

- **Pilot-style callouts: one line per decision as it happens** — FEATURE — value 2 — effort S — risk low — category: live narration — wild
  Why: wild — the user asks what Foreman is doing mid-run, and long receipts arrive too late. One line per decision, muted with one key, answers that question live.
  Done when: each auto-decision emits one line of at most 80 characters in the pane, and `m` mutes the feed without stopping the run.

- **Teach at close: one concept sized to what the user has asked about** — FEATURE — value 2 — effort S — risk low — category: learning
  Why: assumption — the user's questions (usage burn, `fm` not on PATH, the deferral clock) show what they want explained. A concept line tied to the file changed makes the next change easier to read.
  Done when: each close names one concept tied to a file:line the change touched, and the concept is drawn from the topic the user asked about most recently.

- **Show the cheapest route to the user's last-accepted outcome** — FEATURE — value 2 — effort M — risk med — category: cost to outcome
  Why: the user accepts results, not plans, and cost is reported per run. Assumption: comparing cost against the last accepted outcome of the same kind shows whether a new run is worth it.
  Done when: `fm task` shows the expected cost next to the cost of the last accepted task of the same kind, and flags a run above 2x that cost.
