# Brainstorm — lens: false done

- **Strip unproven "completed" claims from compaction summaries** — FIX — value 5 — effort M — risk med — category: resume
  Why: resume is the worst area, and a compaction summary is prose the model wrote about itself. After a compact, "auth done" reads as fact. assumption: a SessionStart(compact) hook can diff the summary text against the clause ledger.
  Done when: in a planted run, a compaction summary claims a step finished that the ledger holds as unproven, and the restored context lists it as "claimed, unproven".

- **Tag every handoff-note line as observed or asserted** — FEATURE — value 4 — effort S — risk low — category: resume
  Why: multi-day goals pass state through notes. A day-3 agent trusts a day-1 "tests pass", and the first inherited wrong claim becomes a false done. assumption: the notes are written through a verb, so tags can be enforced.
  Done when: a note line without a command id and tree hash is stored as "asserted", and resume replays or demotes it before it counts toward a clause.

- **Flag evidence substitution** — FIX — value 5 — effort M — risk low — category: evidence
  Why: evidence and lease commands fail inside the builder worktree. An agent whose proof command errors tends to cite a different, passing command instead. assumption: the ledger sees the failed attempt and the next claim as separate records.
  Done when: a clause whose evidence command failed and was then "proved" by a different command shows as "substituted", and the done gate rejects it until the original command runs or the user approves the swap.

- **Mutate the six false-done scenarios into held-out variants** — FEATURE — value 5 — effort M — risk med — category: eval
  Why: tier 0/6 has been unchanged since gen 2. Fixes aimed at six known scenarios can pass those six and miss the next. A tool-less child that never sees the code (per the standing exam rule) rewrites each scenario with a different fault site, test names and misleading signal.
  Done when: each scenario has at least 3 variants, and the gate's true-done count is reported on the variants alone.

- **Pair every false-done scenario with an honest twin** — FEATURE — value 5 — effort S — risk low — category: eval
  Why: a gate that never lets anything finish scores zero false dones. A twin with the same fault, honestly fixed, must pass.
  Done when: `fm exam` prints two numbers per scenario (false-done caught, honest-done released), and a gate change that drops the second fails the check.

- **Attribute every diff hunk to a clause or flag it** — FEATURE — value 4 — effort M — risk med — category: collateral damage
  Why: some false dones are "the goal is met, but something else broke". Hunks that no clause covers are where this hides. assumption: attribution can be done from clause file lists plus a cheap model pass.
  Done when: the close receipt lists unattributed hunks, and a planted unrelated edit makes done "provisional".

- **Track discovery rate and distrust a plan that never grew** — FEATURE — value 4 — effort S — risk low — category: planning
  Why: a multi-day goal that finishes with the clause list exactly as drafted on day 1 found nothing new, and real work always turns up something. assumption: clause adds and removals are timestamped.
  Done when: a goal with zero clause additions after N hours of work triggers an exploratory "what did the plan miss" pass before done is allowed.

- **Lint the final message's assertions against the ledger** — FEATURE — value 4 — effort M — risk med — category: done claim
  Why: "all tests pass" and "fixed X" in prose are the sentence the user acts on. assumption: checkable claim shapes ("tests pass", "no errors", "all N") are few enough to match with a regex.
  Done when: a final message saying "all tests pass" with no matching passing run on the closing tree is held, and the reply names the missing record.

- **Re-run time-sensitive evidence with a shifted clock** — FEATURE — value 3 — effort M — risk low — category: evidence
  Why: assumption: goals mentioning schedules, expiry, retries or timezones pass today and fail tomorrow, and nothing in the pack covers them.
  Done when: for a goal whose clause text matches a time keyword, evidence is also run under a fake clock +48h and +45d, and a failure makes done provisional.

- **Mine public overfitting-patch trajectories for the false-done corpus** — FEATURE — value 4 — effort L — risk med — category: eval
  Why: six cases is too few to learn from. Public agent benchmarks document patches that pass tests and are still wrong. It must be opt-in and local, with data fetched only under an explicit setting.
  Done when: the corpus holds at least 30 external cases labelled by mechanism, and the zero-token arm reports recall per mechanism.

- **Plant an unsatisfiable clause as a honeypot** — FEATURE — value 4 — effort S — risk low — category: eval — wild
  Why: assumption: if an agent says done on a goal that includes a clause no honest work can meet (a file the harness has made unreachable), you have a direct measure of how readily it claims done.
  Done when: a scratch goal with the honeypot is run nightly, and any "done" without a "could not meet clause N" report counts as a false done on the dashboard.

- **Ask for the one more hour list at done** — FEATURE — value 3 — effort S — risk low — category: done claim — wild
  Why: assumption: an agent asked "what would you check with another hour" names real gaps that a yes/no done question does not surface.
  Done when: every close carries that list, each item is run or explicitly dismissed with a reason, and the share of lists that turned up a real defect is reported.

- **Hold a "wrong-done" recording when a user says it was not done** — FEATURE — value 4 — effort S — risk low — category: feedback — wild
  Why: the user is the one signal Foreman did not author. One word ("missed", "broke", "wrong goal") plus the last 20 ledger lines becomes a labelled false-done case and a draft scenario.
  Done when: one command files the case with its mechanism guess, and the corpus grows without a manual write-up.

Next question: when a gate blocks a true done, how much does that cost the user (waiting, reruns, distrust), and has anyone measured the honest-done release rate against that cost?
Next question: which of the six known false dones would the user have caught by reading the diff in under a minute, and which only by running the thing?
