# Brainstorm — lens: blind spots

**Answers to earlier questions (blind-spot lens):**
- Unattended lane failures that leave no trace: an OS kill, an expired login or a full tmpfs. The only evidence is a missing beat, so the next session start must report "expected beat at X, none" (idea 3).
- Steers that assume a session: `--round-first` and `fm ask` both need someone present. With nobody there, a lane that cannot ask must park its row, never guess (idea 6).

Each idea below comes from a missed ask, with the question that would have caught it.

- **Test every deliberation gate against every task state** — FIX — value 4 — effort M — risk low — category: reliability
  Why: T-2525 was a premise test that covered only open tasks. Question: "What state of the object did this check never meet?" The plan gate, race trigger and blast-radius check each assume open or fresh tasks, and not-yet.md, deferred, blocked and reopened tasks go unchecked.
  Done when: a table test runs each deliberation check over every task state, and the suite fails if a new state appears with no row.

- **Log every silent fallback as a named degradation event** — FIX — value 5 — effort M — risk low — category: observability
  Why: T-2532 found Stop and SessionStart switching off silently. Question: "Where does a failure turn into doing nothing?" Deliberation children that die, parsers that get corrupt output and a race with a flaky verify all fall back quietly.
  Done when: a killed brainstorm child, a corrupt parser input and a flaky verify each add a `degraded` row, and `fm doctor` lists them.

- **Beat-check every unattended deliberation job at session start** — FEATURE — value 4 — effort M — risk low — category: liveness
  Why: T-2542 asked for timers known to be alive. Question: "If this stops, who notices, and when?" Pre-race and overnight deliberation jobs have no beat today.
  Done when: killing a scheduled job makes the next SessionStart print one "missed since X" line.

- **Charge deliberation's own tokens and notes to the lean ratchet** — FEATURE — value 4 — effort S — risk low — category: lean
  Why: T-2533 showed the ratchet omitted per-call hook notes. Question: "What does this gauge leave out?" Plan-gate text, race lanes and rival planners are likely omitted too.
  Done when: the ratchet records chars per session for the deliberation blocks and trips on growth.

- **Name the commit behind each grown deliberation cost** — FEATURE — value 3 — effort S — risk low — category: attribution
  Why: T-2535 asked that a tripped ratchet name the commit. Question: "Does a red signal say who caused it?" Plan-depth cost has no attribution.
  Done when: a planted growth in a plan-gate message is named by its commit in `fm doctor`.

- **Give a lane with no user present a safe default for each ask class** — FEATURE — value 4 — effort M — risk med — category: unattended
  Why: assumption: `fm ask` and `--round-first` assume a live session, and the pack's earlier question on this is unanswered. Question: "Which steer fails when nobody is there?"
  Done when: an unattended lane that hits an irreversible and ambiguous step parks that row with a default and a deadline, and continues on the others.

- **Run a "does it already exist" check before any idea is filed** — FIX — value 4 — effort S — risk low — category: grounding
  Why: T-2534 (the guard-only arm) was dropped as already built (T-0963), and Missions 3 and 4 found the same. Question: "Did someone grep before proposing this?"
  Done when: `fm capture` on an idea whose verb or exam arm exists returns the file:line, and the idea is filed only with a reason it differs.

- **Fill the 58 cells from a probe table, not from sentences** — FEATURE — value 5 — effort M — risk med — category: coverage
  Why: the user's steer is that a templated cell does not count. Question: "Can a cell be real without its own evidence?" A cell holds a command, a grep and its output hash.
  Done when: every Exhaustive-thinking cell has a re-runnable probe, and the cell linter rejects phrasing reused across rows.

- **Score the sealed prediction against the user's next three asks** — FEATURE — value 3 — effort M — risk low — category: calibration
  Why: T-2505 is on the list of missed asks. Question: "Which asks did we fail to predict, and what class were they?" Every missed ask should become a probe case for the next brainstorm.
  Done when: `fm genesis` records predicted against actual and prints the hit rate per class.

- **Find the cleanup candidate for every added deliberation step** — CLEAN — value 3 — effort M — risk low — category: subtraction
  Why: T-2536 added ablation. Question: "What does this make removable?" Deliberation steps never run through the off arm.
  Done when: the ablation report lists each deliberation feature whose off arm changed no pass.

- **Wild: Hold a silent-failure day** — FEATURE — value 3 — effort M — risk med — category: drills
  Why: wild. Kill one component per hour (hook, child, timer, parser) and record who noticed what. This tests ideas 2 and 3 directly.
  Done when: the drill report shows a notice time for each killed component, with no row left at "never".

- **Wild: Let a blind child write the ask the user will send next** — FEATURE — value 3 — effort S — risk low — category: prediction
  Why: wild. A tool-less child reads only the changelog and the dropped-as-built list and writes the next steer. The pack's missed asks are all of that shape (ratchet, liveness, fallback).
  Done when: three predictions are sealed before the Seed and scored at the next one.

- **Wild: Print "what I would have told you if you'd asked" at session start** — FEATURE — value 3 — effort M — risk low — category: proactive
  Why: wild. Draw it from the dropped-as-built list and the degradation ledger, so the user stops having to ask for things Foreman already knows.
  Done when: SessionStart shows at most two such lines, each linked to its evidence, and a session with none shows nothing.

Next question: Which gauges, checks and exam arms did we build with a "nobody thought of" owner, and who audits the auditors?
Next question: Which of the 58 cells can only be filled by a path that runs unattended, and does that path leave a trace?
