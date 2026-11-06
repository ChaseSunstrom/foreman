# Brainstorm — lens: unspoken needs

- **Map each sentence of the request to the proof that covers it** — FEATURE — value 5 — effort M — risk low — category: request coverage
  Why: the user asks for "anything and everything" and keeps re-sending items, so "done" should mean every sentence has evidence. Assumption: requests can be split into sentences that a verifier can match to a check.
  Done when: closing a task with an uncovered sentence lists that sentence under "not proven" and does not print a clean receipt.

- **Recognise a re-sent request and link it to the earlier task** — FEATURE — value 5 — effort S — risk low — category: request memory
  Why: "Cut Foreman's usage burn" was recreated after it was dropped, and "Push foreman/build to main" was redone. Each redo started from zero, so the earlier decisions were lost.
  Done when: a new request that matches a dropped or closed task's wording opens with a link to that task and its recorded outcome, and a fixture pair of matching requests produces the link.

- **Predict a likely re-drop before a task is queued** — FEATURE — value 4 — effort S — risk low — category: drop prediction
  Why: the drops ledger shows the same kinds of work (site publish, usage burn, fm quiet) dropped more than once. Assumption: a request similar to a past drop is more likely to be dropped again.
  Done when: queuing a task similar to a recorded drop prints the drop's reason and asks nothing, and a fixture with a known drop triggers the warning.

- **Count the questions Foreman asks and publish the rate** — CLEAN — value 4 — effort S — risk low — category: interruption budget
  Why: "dont ask me for anything either" is a clear steer, and the system prompt treats reversible choices as Foreman's to make. Nothing measures how often it still stops to ask.
  Done when: `fm status` shows questions asked this week, and a fixture with only reversible choices records zero questions.

- **Show a finish estimate for the whole queue, updated as tasks close** — FEATURE — value 4 — effort M — risk low — category: queue visibility
  Why: a user who says "full force" usually wants to know when the queue will be empty without checking. Assumption: past task durations are a good enough predictor for a rough range.
  Done when: `fm status` prints an estimated finish range with the count of queued tasks, and the range narrows after a task closes in a fixture run.

- **Give each blocked item a default that runs if the user stays silent** — FEATURE — value 4 — effort M — risk med — category: silence policy
  Why: blocked items sit until the user returns, and the user prefers to be left alone. A reversible default lets work continue without a question.
  Done when: each blocked item records a default and a reversal command, and a fixture with an expired silence window applies only reversible defaults and logs them.

- **Show what each blocked item costs in days of waiting** — FEATURE — value 3 — effort S — risk low — category: blocked cost
  Why: T-0325, T-0335 and T-0352 have been blocked for a long time with no sense of what the wait costs. Assumption: a rough days-blocked count plus the queued work it holds is enough to rank them.
  Done when: `fm status` lists each blocked item with its age in days and the number of tasks it holds back.

- **Approve a whole queue once, with the approval ending when the queue empties** — FEATURE — value 4 — effort M — risk med — category: scoped approval
  Why: the user said "go, full force" but the harness rules say approval in one context does not carry to the next. A scoped approval that ends with the queue removes repeated prompts without a standing grant.
  Done when: a fixture approval covers the queued tasks, a task added after the queue empties is refused until re-approved, and outward-facing steps are still excluded.

- **Adjust the auto-decide threshold from undo history** — FEATURE — value 3 — effort M — risk med — category: adaptive autonomy
  Why (wild): each auto-decision that the user undoes is a signal that the threshold is too loose, and each one kept is a signal it can widen. A trust dial could make Foreman quieter over time without a setting change.
  Done when: a fixture with three undone auto-decisions raises the bar for that decision kind, and a fixture with none keeps it unchanged.

- **Shorten the receipt when the user's messages are short and fast** — FEATURE — value 2 — effort S — risk low — category: hurry-aware output
  Why (wild): the user's requests are terse and urgent, and a long receipt costs them reading time. Message length and gap between messages can set how much detail to print.
  Done when: a fixture with a run of short messages prints a one-line receipt, and a fixture with a long message prints the full receipt.

- **Predict how many tasks the rest of the week's budget buys** — FEATURE — value 3 — effort M — risk low — category: budget forecast
  Why (wild): the user does not want usage burned, but the budget is only visible as a number. Turning it into "about N small fixes left" answers the unspoken question of what to spend it on.
  Done when: `fm cost` prints an estimated count of remaining small tasks from the recorded per-task cost, and a fixture with a known budget and cost history produces the expected count.

- **Write a one-line note for the next session's first prompt** — FEATURE — value 3 — effort S — risk low — category: session continuity
  Why: the user should not have to re-explain standing preferences each session. A short note at session end, shown to the next session as its first context line, carries them over.
  Done when: a session ending with an open queue writes a note under the note size limit, and the next session's first context includes it.
