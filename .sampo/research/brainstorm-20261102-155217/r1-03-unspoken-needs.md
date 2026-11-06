# Brainstorm — lens: unspoken needs

- **Reuse past answers to process questions** — FEATURE — value 4 — effort M — risk low — category: user value
  Why: steers say "never block on the user for process or gate questions", yet many asks are still filed as `fm ask`. assumption: the same question classes recur, such as cap raises, merge order and wording choices.
  Done when: a second `fm ask` in an already-answered class is auto-resolved from the stored answer. The resolution is recorded as "reused from T-n" in `fm decide`, and a changed-context test makes it ask again.

- **Write a behaviour changelog of what the model is told** — FEATURE — value 4 — effort M — risk low — category: observability
  Why: the tower rewrites its own skills, hook notes and steers every generation. Nothing shows the user how the agent's instructions differ from last week's. The pack shows many diffs of code and gauges, but none of the injected text.
  Done when: `fm genesis report` has a section listing added, removed and reworded injected lines (skills, SessionStart notes, rendered steers) since the previous generation tag. A test with one planted skill edit shows it.

- **Declare `needs:` when filing and check a host profile** — FEATURE — value 4 — effort M — risk low — category: reliability
  Why: the open questions ask "which of these needs the user's other machines or accounts", and T-0325, T-0335, T-0336 and T-0352 sit blocked on exactly that. Today the block is found after the work is filed.
  Done when: a brief naming sudo, a display, another CLI or an account is routed at filing to a "needs you" list unless `fm host profile` says the host has it. A brief with no needs is filed normally.

- **Make a hand edit win, and say so** — FIX — value 4 — effort M — risk med — category: reliability
  Why: the open question "when the user's hand and Foreman's hand both change the same thing, which side does each reader trust?" has no answer in the pack. assumption: readers disagree today.
  Done when: one precedence table (hand edit over Foreman edit) is documented. A test edits a tree line, a queue row and a ledger-adjacent file by hand, and every reader named in the table reports the hand version and flags the override.

- **Learn what "simplify" means for this user** — FEATURE — value 3 — effort M — risk med — category: user value
  Why: the open question asks whether the user means fewer verbs, shorter output or fewer questions. Their drops of `fm tidy --verbs` and `c16` suggest they accept subtraction where evidence is thin.
  Done when: after a "simplify"-class message, Foreman files the three candidate readings as separate S tasks. Over time it keeps a per-reading accept rate, and `fm next` offers the highest first.

- **Gate generation growth on the user's read receipt** — FEATURE — value 3 — effort S — risk low — category: simplicity
  Why: the 525-idea catalogue and three generations of Missions exist, and nothing shows the user has read the previous report. Rule 15 ("Lean substance") only waits on measurement, not on attention.
  Done when: `fm genesis` will not open a new generation's Missions until the previous report has an `fm ack` or a timed default that is recorded as a costly decision.

- **Give each steer a review-by date and an evidence query (wild)** — FEATURE — value 3 — effort M — risk low — category: user value
  Why: steers are open-ended. The T-2583 correction shows a rule can be wrong on first writing, and many were written under 2026-10-30/31 assumptions that may not hold later. wild.
  Done when: a steer stored with `--review 30d --measure "<fm command>"` shows up in `fm next` on day 30 with the command's current output next to the steer text.

- **Keep a "what I assumed about you" file the user can strike through (wild)** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: the pack makes the user correct Foreman's inferences repeatedly (T-2583, the "dropped" lines, the re-grounding notes). A visible list of inferences turns future corrections into one strike-through each. wild.
  Done when: `fm assumptions` lists every inference Foreman acted on, each with its source quote. Striking one files a sibling sweep for the same class.

- **Stage a nightly fake-clock month for unattended timers (wild)** — PERFORMANCE — value 3 — effort L — risk med — category: reliability
  Why: the first open question says no unattended path has been run end to end on a real clock across sleep or network loss. `c.clock()` with `FOREMAN_NOW` (T-2645) now makes a time-compressed run feasible. wild.
  Done when: a harness advances `FOREMAN_NOW` through 30 days with injected suspend gaps and a dead network. It reports each timer's fire count against its expected count, and any missed fire fails the run.

- **Print a first-minute card after any fail-open, and test it** — FIX — value 4 — effort M — risk low — category: observability
  Why: open question 2 asks what the user sees in the first minute after a silent fail-open and whether that moment is ever tested. assumption: nothing is shown until `fm doctor` is run.
  Done when: for each hook, a test forces an exception and checks that the next prompt's context contains one line naming the hook and the command to inspect it. A test with the exception swallowed fails.

- **Fold repeat user corrections into the next pack's "do not repeat" slice** — FEATURE — value 3 — effort S — risk low — category: developer experience
  Why: the "what earlier brainstorms missed" list has 8 entries, each a repeat of a class (grounding, canary, count). The pack already shows the entries but not the class they share.
  Done when: the pack header lists each missed-ask class with its count, and a test shows a class seen three times is promoted to a named check.

- **Make a catalogue entry carry its use evidence (wild)** — FEATURE — value 3 — effort M — risk low — category: simplicity
  Why: open question 6 asks what fraction of the 525 ideas has any measured user-felt value. wild.
  Done when: `fm genesis catalogue --used` shows, per built idea, the count of session-path calls in the last 14 days. A summary line gives the share with zero.

Next question: which of the 525 catalogue ideas has the user actually typed a command for, and what do the top three have in common?
Next question: when the user stops reading reports, which signal in the ledgers shows it first?
