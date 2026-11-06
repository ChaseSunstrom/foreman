# Brainstorm — lens: blind spots

**Question 1: where does a protection switch off without a trace?** (T-2532, T-2542)

- **Log every silent fallback in one degradation ledger** — FEATURE — value 5 — effort M — risk low — category: reliability
  Why: T-2532 found Stop and SessionStart could switch off when the working copy failed to import, and T-2542 found timers whose death nobody saw. Assumption: other fallbacks exist (state-dir read-only, a missing `claude`, a failed settings parse) that have no named event.
  Done when: forcing each of five injected faults produces one ledger row with an event name, and `fm doctor` lists the rows from the last 7 days.

- **Show the morning-after read for each unattended failure class** — FEATURE — value 5 — effort M — risk low — category: observability
  Why: the pack's open question asks what the user sees after an OS kill, a logged-out session or expired auth. Nothing answers it. Assumption: today these leave no trace.
  Done when: a fixture kills a lane with SIGKILL, with auth expired, and with the session logged out, and the next SessionStart line names each cause.

- **Run a nightly "tick can still run" self-test** — RELIABILITY (FEATURE) — value 4 — effort S — risk low — category: reliability
  Why: T-2542 checks that systemd fired a timer, not that the fired code works. Assumption: an unreadable interpreter path or library would pass the liveness check.
  Done when: breaking the unit's interpreter path in a fixture turns the doctor row red within one tick.

**Question 2: which measure counts only part of what it names?** (T-2533, T-2535)

- **Audit every gauge for what it omits** — FIX — value 4 — effort M — risk low — category: observability
  Why: the lean ratchet missed per-call hook notes until T-2533, which suggests other gauges share the problem (MCP schemas, skill bodies, SessionStart deltas). Earlier ideas covered attribution by source but not a test that the total equals the sum of its parts.
  Done when: `fm doctor` prints, per gauge, the measured total next to an independent count (a raw byte sum of the transcript), and any gap above 5% is red.

- **Reconcile injected bytes against the real transcript** — PERFORMANCE — value 4 — effort M — risk low — category: lean
  Why: the pack cites 387k context per reply, which looks like a measure no one cross-checked. Assumption: the ratchet's sums are lower than the real injected bytes.
  Done when: a run on a recorded session produces a source-by-source table summing to within 2% of the transcript's injected bytes.

**Question 3: which fix applies only to the state it was found in?** (T-2525)

- **Sweep every premise-test for the state it never tried** — FIX — value 4 — effort M — risk low — category: tests
  Why: T-2334's start-point rule covered open tasks only, and its sibling test assumed there was no start commit. Earlier ideas touched "sibling premises" in the abstract, with no state-matrix mechanism.
  Done when: a check lists task-state × feature pairs (open, deferred, blocked, closed, captured) with no test, and the first run files the gaps.

- **Test each task-state feature against all task states** — CLEAN — value 3 — effort S — risk low — category: tests
  Why: assumption: `fm task` features are written for the state the author was in. A property test could loop every verb over every state.
  Done when: a parametrised test runs each `fm task` verb on a task in each state and fails on any traceback.

**Question 4: what exists that the user still had to ask for?** (T-2534, plus the dropped "already built" items)

- **Answer "is this already built?" at capture time** — FEATURE — value 5 — effort M — risk low — category: discoverability
  Why: three of the dropped asks (guard-only arm, child authoring, status naming) were already built, and the user spent a request finding out. Only the tower, not the user, checks MASTER.md.
  Done when: capturing "a guard-only exam arm" prints the existing flag, file and line with a "built" verdict in under 2 seconds.

- **Add `fm can "<phrase>"` backed by the verb index** — FEATURE — value 4 — effort S — risk low — category: discoverability
  Why: the pack lists `fm can` as an idea but doesn't connect it to the user's own asks. Assumption: a keyword match over verbs, flags and MASTER headings is enough.
  Done when: five past dropped-as-built asks each return their real verb as the top hit.

**Question 5: which cleanup has no evidence trigger?** (T-2536)

- **Raise cleanup candidates from ablation, in the same report as growth** — FEATURE — value 3 — effort M — risk med — category: lean
  Why: T-2536 files a candidate only when the off arm changed no pass at no more cost. Assumption: no equivalent exists for steers, skills or cards.
  Done when: an ablation run files one candidate per card or skill whose removal changed nothing, each labelled "candidate", never a cut.

**Question 6: which prediction was never written down before the user needed it?** (T-2505)

- **Score the sealed prediction against the user's next three asks** — FEATURE — value 4 — effort S — risk low — category: planning
  Why: T-2505 itself was a missed ask. Assumption: no hit rate is kept.
  Done when: `fm doctor` shows hits out of 3 for the last generation and names the miss class of each miss.

- **Make every missed ask an automatic regression probe** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: the missed-ask list is data the pack prints but nothing replays. Assumption: the next brainstorm would repeat the same gaps.
  Done when: each of the eight listed T-numbers has a one-line probe that fails on a build lacking its fix.

**Wild**

- **Wild: Hold a "silent failure day" that kills one component per hour and records who noticed** — FEATURE — value 4 — effort L — risk med — category: reliability
  Why: wild; assumption: the user finds failures by chance, not by the design.
  Done when: a fixture day runs ten kills and the report shows how many surfaced within a tick.

- **Wild: Have a tool-less child read the changelog and write the ask the user would send next** — FEATURE — value 3 — effort S — risk low — category: planning
  Why: wild; the child never sees Foreman's code, so its guesses are free of Foreman's own blind spots.
  Done when: the child's three guesses are logged before the next steer and scored afterwards.

- **Wild: Print "things I would have told you if you had asked" at session start, from the dropped-as-built list** — DELIGHT (FEATURE) — value 3 — effort S — risk low — category: discoverability
  Why: wild; turns the wasted asks into a teaching line.
  Done when: a session after a dropped-as-built ask shows one line naming the verb.

Next question: Which of the 59 or 61 empty coverage cells exist because a failure is silent and so nobody has noticed it should have a cell?
Next question: Which numbers on the web UI are computed from a part of the data, and does any page state its denominator?
