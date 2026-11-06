# Brainstorm — lens: unspoken needs

**Earlier questions I can answer:** I can't see the Mission-page click data, so "which cell opens first" stays an assumption. The cell most likely read first is the one with the most user-visible sting, so the grid should open on it. Exam measures that read session state, such as "the user did not re-ask", can't be re-run cold. Only `--json` and ledger-derived readings can.

- **Audit the twin before closing a fix** — FEATURE — value 4 — effort M — risk low — category: follow-ups
  Why: the user's asks arrive in pairs that touch the same line. T-2683's output was followed by T-2738 (commas, not spaces). T-2691 was followed by T-2693 (per-gen lines). T-2720 was followed by T-2724. Each second ask is a sibling of a close that passed.
  Done when: closing a task whose diff changes printed output or a keyed record runs a sibling scan (same file, same format family, last 14 days of closes). A planted sibling defect is named in the close output.

- **Keep a by-design register that every review reads first** — FEATURE — value 4 — effort S — risk low — category: noise
  Why: the user dropped review items #23 and #25 as "review.md marks it gap" and #24 as "by design" (the guard refusing interpreter writes). Each cost a task, a cold read and a drop. Assumption: this recurs every generation.
  Done when: a dropped item's reason, with its file:line, is stored as a register entry. A re-filed finding with the same anchor is suppressed and counted. A test shows #24 would not be refiled.

- **Brake generation speed on review debt** — FEATURE — value 4 — effort M — risk med — category: pacing
  Why: the steers say "never block on the user", so closes pile up unread, while the user's own asks are mostly "Ship N commits". Assumption: unread closes grow faster than the user reads them.
  Done when: `fm next` shows "N closes since you last opened a receipt". Past a threshold the tower still finishes open tasks but won't start a new generation, and it says so in one line.

- **Report churn: how much of a Mission repairs the last one** — FEATURE — value 3 — effort S — risk low — category: self-measurement
  Why: the recent closes (T-2691, 2693, 2720, 2722, 2724, 2729, 2738) are mostly fixes to the tower's own earlier output.
  Done when: each Mission close prints "x of y briefs repair earlier Mission output". Above a set share it files one task to find the shared cause.

- **Audit unanimity as a signal** — FEATURE — value 3 — effort M — risk low — category: dissent
  Why: dissents are being scored against outcomes, but a brief where nobody dissented never gets scored. Assumption: most briefs have no dissent at all.
  Done when: for each brief with no dissent, a cold child writes the strongest objection. That objection joins the dissent scoring ledger tagged "elicited", so unanimous and dissented briefs can be compared.

- **Pin the unit and direction of every outcome measure** — FIX — value 3 — effort S — risk low — category: exam
  Why: the `fm task unblock` comma-versus-space slip (T-2738) shows that value formats drift. An outcome measure like "survives 14 days" can be silently inverted or unit-swapped.
  Done when: filing rejects an Exam whose `outcome:` line lacks a unit, a direction and a threshold. A test with a flipped threshold fails.

- **Print who can unblock each waiting item, in the user's words** — FEATURE — value 3 — effort S — risk low — category: blocked pile
  Why: 44 blocked tasks have waits written only in free-text reasons (T-0325 needs a package, T-0418 an install, T-0352 a publish). Assumption: the user can't tell which three they alone can clear.
  Done when: `fm next` ends with "you can clear 3 of 44 with: <commands>". It reads reason text, not metadata.

- **Show the tower's weather at session start (wild)** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: assumption: the user wants an ambient read of "is the tower healthy" without opening anything.
  Done when: one line reads "clear", "unsettled" or "stormy", derived from red sweeps, unshipped commits, review debt and churn. Each word cites its inputs.

- **Draft the user's next ask from their own phrasing and score it (wild)** — FEATURE — value 3 — effort M — risk med — category: anticipation
  Why: the user's asks follow a template ("X, so a cold read never Y"). Assumption: a child that has only the last 30 asks can predict the next one's shape.
  Done when: the predicted ask is sealed at session end and graded at the next session by title overlap with the real ask. A running hit rate is shown.

- **Write a one-line obituary for each tower rule that stops firing (wild)** — FEATURE — value 2 — effort M — risk low — category: lean
  Why: each steer became an automatic check, and with 40 or more rules some will go silent. Silent is not the same as safe.
  Done when: a check that has never failed in 60 days gets a plain line: "never failed, last would-have-fired test: <date>". The user can keep or retire it with one command.

- **Replay the last Mission's overruled dissent against today's outcomes (wild)** — FEATURE — value 3 — effort M — risk low — category: dissent
  Why: the carried gap is "dissents scored against outcomes". Assumption: the cheapest honest first score is a retroactive one on gen-3's briefs.
  Done when: a table of gen-3 dissents shows overruled or accepted, outcome and delta, with "unscored" where no outcome exists.

Next question: Which of the tower's own outputs has the user never once opened, and would they notice if it stopped being written?
Next question: What does the user type by hand after a Foreman close, and does Foreman see those commands at all?
