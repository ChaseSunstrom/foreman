# Brainstorm — lens: user value

- **Open one cross-repo inbox** — FEATURE — value 4 — effort M — risk low — category: user value
  Why: assumption: the user runs Foreman in several repos, and every surface in the pack is per-repo.
  Done when: `fm inbox --all` lists decisions, blocked items and finished work from every registered repo in one ranked list, and a fixture with 3 repos shows items from all 3.

- **Search your own history in your own words** — FEATURE — value 4 — effort M — risk low — category: recall
  Why: the user re-pastes steers and asks "did we ever…" style questions. The pack lists `fm why` and the "did we ever check X?" idea, but no free-text search over sessions, tasks, decisions and steers.
  Done when: `fm recall "the thing about stalled spend"` returns T-2669 with the quoted user line and date, and a test checks 5 known phrases against 5 known tasks.

- **Plan the queue backward from a deadline** — FEATURE — value 4 — effort M — risk med — category: scheduling
  Why: assumption: users have real dates ("demo Friday"). The queue is ranked by value, effort and risk, not by date.
  Done when: `fm due T-x Fri` makes `fm next` order work by slack and print "infeasible: needs ~9h, 6h left" when it can't fit. A fixture queue shows the reorder.

- **Confirm Foreman's model of the repo on first contact** — FEATURE — value 4 — effort M — risk low — category: onboarding
  Why: the first-run and tour items are deferred (T-0862/63), and `fm map` is derived without the user seeing it. A wrong build or test command silently poisons every later proof.
  Done when: first run prints the detected gates, conventions and no-go paths as 6 or fewer lines with accept/fix, a fix is stored as a steer, and a fixture with a wrong test command is caught.

- **Make the answer to a question citation-checked** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: finish claims get proofs, but plain Q&A about the code does not. Wrong `file:line` references in answers are the cheapest lie to catch.
  Done when: a post-answer check resolves every cited path and line against the tree, appends "2 of 7 citations unverified" when any fail, and a planted bad cite is flagged.

- **Break out when the user repeats themselves** — FIX — value 4 — effort S — risk low — category: recovery
  Why: the "missed asks" list shows the user re-asking. A near-duplicate user message in one session is a signal that nothing in the pack reads live.
  Done when: a near-duplicate prompt within a session triggers a one-screen "here is what I understood, here is what's done, here is what I didn't do". A replay of 3 real repeated asks fires, and 3 unrelated pairs don't.

- **Save a finished task as a named recipe** — FEATURE — value 3 — effort M — risk low — category: reuse
  Why: the user's asks come in recurring shapes (the "c11…c24" PERF/FEATURE patterns). Skill distillation is automatic; the user can't say "do that again, but for X".
  Done when: `fm recipe save T-2669 stall-guard` stores parameterised steps with their proof command, and `fm recipe run stall-guard --target fmwatch` files a task whose criteria are filled from it.

- **Let Foreman object once, with evidence** — FEATURE — value 4 — effort M — risk med — category: honesty
  Why: the user drops ideas as "mostly built" or "value 2", which shows they want pushback, but only after filing. Pushback before building is absent from the pack.
  Done when: at intake, a request that conflicts with a steer, a built feature or a measured cost gets one evidence-backed objection with "proceed anyway" as one word, and proceeding is never blocked. A fixture with a duplicate request shows the objection.

- **Draft maintainer replies to incoming issues, with a repro attempt** — FEATURE — value 3 — effort L — risk med — category: open-source
  Why: assumption: the user publishes a GitHub repo with CI, and issues are the only inbound channel the pack ignores. "Adopt-an-issue" is about fixing, not answering.
  Done when: a fixture issue yields a local draft reply plus a repro result (reproduced, not reproduced or unclear), nothing is posted without a grant, and the draft quotes the failing command.

- **Write the user a brag document** — FEATURE — value 3 — effort S — risk low — category: user value
  Why: assumption: the tasks, bets and yield data already exist, and the user never gets them as a performance-review or portfolio artifact. The digests all report for Foreman, not the user.
  Done when: `fm brag --since 90d` prints a dated list of outcomes in plain words, each linked to a task id and its proof state, with "unproven" items flagged and none counted as wins.

- **Port a fix to the user's other repos** — FEATURE — value 3 — effort M — risk low — category: reach
  Why: assumption: sibling repos share code shape. Neighbour priming exists only for harm incidents, not for ordinary fixes.
  Done when: closing a FIX runs its test pattern on registered sibling repos, files tasks for any that fail, and a fixture with one buggy sibling gets exactly one task.

- **Export decisions and lessons as a linked notes vault** (wild) — FEATURE — value 3 — effort M — risk low — category: data ownership
  Why: assumption: the user would value owning their history in plain linked markdown. Ledgers are JSON, and the "readable with `cat` and `grep`" idea falls short of a browsable graph.
  Done when: `fm vault out/` writes one note per decision, steer and lesson with `[[T-####]]` backlinks and a quoted source line. A link checker finds zero dangling links.

- **Forecast the user's objections before the finish card** (wild) — FEATURE — value 3 — effort M — risk med — category: review
  Why: the user's drops and corrections follow patterns (privacy surface, value-2 re-grounding). A cheap model fed their past drops could predict the pushback.
  Done when: the finish card lists up to 3 predicted objections, and a backtest on the last 30 closed tasks scores them against what the user actually did. It is shown only if precision beats a no-prediction control.

- **Swap a redacted failing-task capsule with a friend** (wild) — FEATURE — value 2 — effort L — risk high — category: social
  Why: assumption: a second human's one-line steer on a stuck task is worth more than another model retry. This is opt-in only and sends nothing without an explicit setting.
  Done when: `fm capsule export T-x` writes a scrubbed file, and `fm capsule import` files it as a read-only task. A canary secret planted in the source never appears in the capsule.

- **Quote a price and odds before taking a task** (wild) — FEATURE — value 3 — effort M — risk low — category: expectations
  Why: the forecast and spend-receipt ideas show the numbers only after the fact. A quote built from the user's own duel and yield data, and later settled as a bet, turns them into a promise.
  Done when: each filed task carries "quote: ~$1.8, 70% pass, ~25 min". Closing it settles the quote, and `fm doctor` reports the quote error over the last 20 tasks.

Next question: which of these would the user actually open in a week, given they say "Foreman" but never ask for a surface?
Next question: what does the user do with Foreman's output between sessions (copy it elsewhere, show it to someone, forward it), and can that be captured without logging their shell?
