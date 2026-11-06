# Brainstorm — lens: user value

- **Preview the decisions a run will make alone** — FEATURE — value 5 — effort S — risk low — category: consent preview
  Why: The user keeps saying "just go, don't ask me," so decisions happen silently. A pre-run list shows the choices Foreman will make without waiting for a reply. Assumption: the user wants to see the plan but not approve it.
  Done when: `fm run` prints a numbered list of pre-decided choices, starts after 5 seconds with no input, and a key press during that window changes choice N before the first write.

- **Re-scope a running task when the request is amended** — FEATURE — value 4 — effort M — risk med — category: request handling
  Why: The pack shows tasks recreated after pushback ("recreated with interpretation and approach", "dropped" then redone). Editing the request in place would keep the T-id and its proof history.
  Done when: amending a running task's request keeps its T-id and reruns only the acceptance checks whose text changed.

- **Keep a personal glossary of the user's own words** — FEATURE — value 4 — effort S — risk low — category: vocabulary
  Why: The user writes in shorthand: "the reset," "the blocked pile," "tidy," "publishes" for push-to-main. Mapping these to commands and state removes re-explanation. Assumption: the same phrases recur across sessions.
  Done when: `fm status` resolves "the reset" to the next usage reset time, and a glossary file maps at least five phrases to commands and is covered by a test.

- **Flag a new request that conflicts with an open task** — FEATURE — value 4 — effort M — risk low — category: request conflicts
  Why: The user files many related asks ("fm quiet reads stdin," "fm quiet fails loudly on empty stdin") that can contradict each other. Catching the clash before queuing avoids a wasted run.
  Done when: queuing a request that contradicts an open task prints one line naming both T-ids and does not queue until the user picks a winner.

- **Show why each queued task is next** — FEATURE — value 3 — effort S — risk low — category: queue transparency
  Why: The queue has many deferred and blocked items, and the order is not explained. A one-line reason per task makes the scheduler's choices visible.
  Done when: `fm status` shows a reason string for every queued task, and the reason names the rule that placed it (blocked-by, deferred-until, or next-by-value).

- **Pin a task so auto-decisions can't change its scope** — FEATURE — value 3 — effort S — risk low — category: control
  Why: Auto-decisions are a feature the user wants, but some tasks have a settled meaning. Pinning gives the user a lock without turning auto-decide off.
  Done when: a pinned task's scope is unchanged after an auto-decision pass, and the pass logs "skipped pinned T-N."

- **Give one quiet-hours setting that silences every surface** — FEATURE — value 3 — effort S — risk low — category: interruptions
  Why: Bells, desk cards, pane alerts and phone pings each have their own settings, and the user has asked to be left alone. One switch covers them all. Assumption: the user wants quiet time as a single control.
  Done when: setting `quiet` from 22:00 to 07:00 suppresses bell, desk and push notifications, and a run that needs the user during quiet hours queues the alert for 07:00.

- **Write a plain-English status note for people outside the repo** — FEATURE — value 3 — effort S — risk low — category: sharing
  Why: Receipts use T-numbers and jargon; the user may need to report progress to others. Assumption: the user sometimes reports to a team.
  Done when: `fm note` emits at most five sentences with no T-ids or command names, checked by a fixture test against a sample receipt.

- **Turn a deadline phrase into queue order** — FEATURE — value 3 — effort M — risk med — category: scheduling
  Why: The user already phrases timing as "defer until reset," and a deadline like "before Friday" is the natural next step. Foreman should reorder the queue to meet it and say what slips.
  Done when: `fm task add --by friday` sequences the queue so the task closes before Friday, and the output names any task pushed past its deadline.

- **Wild: a thermal receipt printer on the desk** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: Wild: when a queue finishes, a cheap thermal printer prints the close receipt on paper, so the morning result is in the user's hand before coffee.
  Done when: with a printer configured, a finished queue prints its receipt and the output is under 40 columns.

- **Wild: a bet slip for the user's hunches** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: Wild: before a run, the user writes a guess that a task passes; Foreman keeps a running score of the user's hit rate and shows it on the Today chart.
  Done when: a guess recorded before a run is scored at close, and the Today chart shows the user's hit rate for the past seven days.

- **Wild: an ask jar that Foreman draws from when idle** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: Wild: the user drops one-line ideas into a jar, and when the queue is idle Foreman draws one at random, asks nothing, and files it as a low-priority task.
  Done when: `fm jar add "text"` files a deferred task, and an idle queue draws one jar item per day and records the draw in the journal.
