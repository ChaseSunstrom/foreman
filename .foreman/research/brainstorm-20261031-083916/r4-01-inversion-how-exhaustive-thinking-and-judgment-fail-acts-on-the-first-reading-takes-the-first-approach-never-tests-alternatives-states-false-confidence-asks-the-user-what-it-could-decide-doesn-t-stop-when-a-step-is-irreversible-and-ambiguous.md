# Brainstorm — lens: inversion: how exhaustive thinking and judgment fail: acts on the first reading, takes the first approach, never tests alternatives, states false confidence, asks the user what it could decide, doesn't stop when a step is irreversible and ambiguous

- **Replay the user's last 20 corrections as a plan-gate regression suite** — FEATURE — value 5 — effort M — risk low — category: judgment testing
  Why: the "asked" list is full of gate misses the user had to file by hand (T-2285 flag-led options, T-2288, T-2289). Each is a plan that passed but shouldn't have. assumption: the original plans are recoverable from task files.
  Done when: `fm gate replay` runs the plan gate on each past plan that later drew a correction and reports how many it now refuses; the count is nonzero before the fixes and zero after.

- **Fail the plan when its options are one idea in three costumes** — FIX — value 4 — effort M — risk med — category: plan gate
  Why: T-2285 shows the gate counts text, not distinctness; the gate checks "3+ options" by markers only.
  Done when: a fixture plan with three paraphrased options is refused, naming the pair with the highest token overlap, and a fixture with three real alternatives passes.

- **Require a falsifier beside every low-confidence assumption** — FEATURE — value 4 — effort S — risk low — category: calibration
  Why: the gate demands "a research note or spike" for low-confidence assumptions, but a note can be filler. assumption: the note is free text today.
  Done when: a plan whose low-confidence assumption lacks a line "would be wrong if: <observable>" is refused at focus.

- **Stamp the first reading and diff it against the user's words at close** — FEATURE — value 4 — effort M — risk med — category: first-reading lock-in
  Why: the request text is the only signal Foreman didn't author. Closing a task should show which clause of the user's ask no row or test touches. assumption: the verbatim ask is stored on the task.
  Done when: `fm task finish` prints "unmatched clauses: N" with each clause quoted, and a fixture ask with an unaddressed clause yields N=1.

- **Make every stop-and-ask carry its failed attempt to decide** — FEATURE — value 4 — effort M — risk low — category: asking discipline
  Why: standing rule 3 says to ask only when something only the user can raise blocks; nothing checks that `fm ask` first tried. assumption: `fm ask` has a free-text body.
  Done when: `fm ask` refuses a body missing "decided-against:", "reversible:" and "default:" lines unless the ask is tagged user-only, and logs refused asks.

- **Classify each ask as avoidable after the fact** — FEATURE — value 3 — effort M — risk low — category: asking discipline
  Why: the earlier ideas log stops, but none reads the user's reply for "whatever you think" style answers. assumption: replies are stored.
  Done when: `fm triggers` lists asks whose answer matched the offered default, as a rate per question class.

- **Hold irreversible steps to a pre-image receipt** — SECURITY — value 5 — effort M — risk med — category: irreversibility
  Why: the guard blocks known-bad commands, but a step that is merely one-way (migration, publish, force-push under a grant) has no required undo line. The push grant is spent on use, so a wrong push stays pushed.
  Done when: running a step the door table marks one-way without a recorded "undo:" or explicit "no undo" line is refused, and the refusal names the line to add.

- **Flag races won by the first approach on a rigged verify** — FIX — value 3 — effort M — risk med — category: race integrity
  Why: T-2271 races the runner-up after 3 failures, but if the verify command is weak, any approach passes. assumption: the verify is shared between lanes.
  Done when: a race refuses to name a winner when a deliberately broken third lane also passes the verify, reporting "verify can't tell lanes apart".

- **Cap stated confidence by the strongest evidence kind present** — FEATURE — value 4 — effort S — risk low — category: calibration
  Why: the unproven rollup already counts typed or inconclusive evidence (Mission 7); confidence in prose is not tied to it.
  Done when: a close note claiming "high" with only typed evidence is rewritten to "medium at most" by the finish audit, with the reason shown.

- **Score the plan's first-instinct against the runner-up on closed tasks** — FEATURE — value 3 — effort L — risk med — category: judgment metrics
  Why: nobody knows whether racing pays. assumption: closed tasks keep their Approach text.
  Done when: `fm doctor` prints how many closed M/L tasks named a runner-up that a later fix or revert effectively adopted.

- **Wild: Run a "stubborn reader" child that must argue the user meant the opposite** — FEATURE — value 3 — effort M — risk low — category: readings
  Why: wild; a cold Haiku forced to defend the least likely reading exposes which readings were never checked against the user's steers.
  Done when: the L plan gate shows the reading it argued and whether any steer or past ask contradicts it.

- **Wild: Pre-commit a "surprise me" bet on each irreversible step** — FEATURE — value 3 — effort M — risk low — category: calibration
  Why: wild; before a one-way step the builder writes the one thing most likely to go wrong. Reviewing real failures against those bets shows where judgment is blind.
  Done when: a close receipt shows "predicted failure: X; happened: yes/no" for each one-way step.

- **Wild: Give every plan a "kill switch sentence" the user can paste to stop it** — FEATURE — value 2 — effort S — risk low — category: user control
  Why: wild; the user's steers repeatedly redirect running work. A one-line abort phrase per goal, recognised at intake, ends a lane cleanly with a parked card.
  Done when: sending that phrase stops lanes for the goal and writes a resumable baton.

- **Audit the stops Foreman didn't make** — FEATURE — value 4 — effort M — risk med — category: irreversibility
  Why: past ideas count asks; the costly failure is a one-way step taken silently. assumption: the guard log records one-way commands.
  Done when: `fm doctor` lists one-way actions run in the last week with no ask, receipt or grant, and the fixture with one such action shows it.

Next question: Which of Foreman's own refusals have never once been triggered on real work, and would they fire on the user's past corrections?
Next question: When the user rejects a plan, which clause of their ask did the plan read differently from them?
