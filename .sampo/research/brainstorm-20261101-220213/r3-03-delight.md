# Brainstorm — lens: delight

- **Show the lean weigh-in as a receipt on every task close** — FEATURE — value 4 — effort S — risk low — category: lean UX
  Why: Pack measures hook p95 278 ms and 387k context per reply, but the user sees none of it at close; lean is only a sweep row. Subtract-as-you-add is a gen-0 rule with no felt moment.
  Done when: `fm task finish` prints one line (hook p95 delta, injected bytes delta, verbs ±) and a test asserts it appears with a nonzero delta fixture.

- **Turn each guard block into a one-line story with the safe alternative** — FEATURE — value 5 — effort S — risk low — category: guard UX
  Why: `core:interpreter-code-driving-foreman` blocked 42x in 7 days. A bare refusal teaches nothing; the user's steers want the unblocking command named.
  Done when: every deny reason in fmguard carries a "do this instead" command, checked by a test over the whole deny table.

- **Make false positives one-keystroke fixable** — FIX — value 4 — effort M — risk med — category: guard UX
  Why: 2 brief-guard false positives read a dict key and a `.join(` call as paths. Today the user has to diagnose them.
  Done when: after a block, `fm guard wrong` appends the input to a false-positive corpus and files a task; the two known cases pass in that corpus test.

- **Give the SessionStart note a diet: hash first, delta after** — PERFORMANCE — value 4 — effort M — risk med — category: context
  Why: Note is ~2k chars × 89 sessions, unchanged most of the time. Gen-0 forbids injected context growing.
  Done when: a second session start with unchanged state injects ≤200 bytes, and a test compares byte counts.

- **Add a weight-class gauge to the pane and status line** — FEATURE — value 3 — effort M — risk low — category: UI motion
  Why: The foreman-ui pane already has bars and lanes; hook time and context bytes are invisible. A small gauge that eases when a hook runs slow makes leanness something you watch.
  Done when: the pane shows hook p95 and injected bytes with a colour change at budget, and a snapshot test covers the over-budget state.

- **Print the guard's weekly save as plain words** — FEATURE — value 3 — effort S — risk low — category: guard UX
  Why: Block counts exist in fm friction but never reach the user as a benefit. "Stopped 42 attempts to drive fm from Python this week."
  Done when: `fm doctor` or the night digest prints a plain-words paragraph generated from block-log data, with a test on a fixture log.

- **Lint the 61 coverage cells as they are written, with a friendly nudge** — FEATURE — value 4 — effort S — risk low — category: coverage
  Why: Steers reject templated or duplicated cells and the cold read fails late. Catching phrase reuse at write time saves a round trip.
  Done when: writing a cell whose text matches another row beyond a similarity threshold prints the matching row and refuses, with a test.

- **Celebrate a deletion with a receipt** — FEATURE — value 3 — effort S — risk low — category: lean UX
  Why: The rule says each generation removes as much as it adds, but deletions earn nothing visible, so they get skipped.
  Done when: closing a CLEAN task that nets negative lines prints "−N lines, −M verbs, p95 unchanged" and records it for the sweep's lean row.

- **Wild: Offer a guard playground on the site** — FEATURE — value 3 — effort M — risk med — category: site
  Why: wild. A visitor pastes a command and sees the guard's verdict, reason and safe alternative, computed client-side from the shipped rule table, with nothing sent anywhere.
  Done when: a static page returns the same verdict as `fmguard` for a 30-command corpus, checked by a test comparing both.

- **Wild: Run a "diet week" mode** — FEATURE — value 3 — effort M — risk med — category: lean
  Why: wild. Each day disables one optional hook or injection and logs whether any correction, retry or reopen followed; the report names the weights that nobody noticed. It gives gen-0's "pays for itself or gets cut" real data (assumption: hooks can be toggled per day safely).
  Done when: `fm diet start` disables one named optional injection for a day and `fm diet report` prints its outcome comparison.

- **Wild: Plant a harmless forbidden command weekly to prove the guard is alive** — SECURITY — value 4 — effort M — risk low — category: guard
  Why: wild. A silent guard looks the same as a broken one. A canary that must be denied each week, with a visible "guard alive, last proved Tuesday" line, makes safety felt.
  Done when: a scheduled canary runs through the real hook path, `fm doctor` shows the last proof date, and a test with the guard disabled turns that line red.

- **Show a "since you left" lean line on resume** — FEATURE — value 2 — effort S — risk low — category: resume
  Why: Users return to goals after hours or days. One line: "guard blocked 3, hooks p95 262 ms, context ↓4%".
  Done when: the first prompt of a resumed goal includes the line under the byte budget, with a test.

Next question: Which of Foreman's felt moments (close, block, resume, morning digest) does the user actually read, and which are already ignored?
Next question: What would the user say if asked to delete one capability today, and does leanness data agree with them?
