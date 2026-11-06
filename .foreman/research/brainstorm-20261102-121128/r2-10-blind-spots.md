# Brainstorm — lens: blind spots

- **Publish-time leak scan for auto-published data** — SECURITY — value 5 — effort S — risk low — category: privacy
  Why: T-2624 shows pasted keys reach intake, and the standing rule has `fm genesis live` push site/genesis data to main on every tower change. Question missed: "which Foreman-written stores can contain text the user pasted?"
  Done when: a test plants a fake `sk-…` key and a home-directory path in an intake item. `fm genesis live` then refuses to publish and names the file and line.

- **Print the denominator on every "nothing found"** — FIX — value 4 — effort M — risk low — category: observability
  Why: T-2566 (select decides on no held-out answers) is silent abstention. Existing ideas make deciders report coverage, but finders, doctor rows and sweeps also say "none". Question missed: "what does this report say when it saw nothing?"
  Done when: `fm doctor`, `fm find` and `fm genesis sweep` each print "checked N of M" when clean. A test with M=0 prints "checked 0 of 0 (not a pass)".

- **Scan for deciders that carry no sample size** — CLEAN — value 4 — effort M — risk low — category: reliability
  Why: T-2566 was found by the user, not by a check. Assumption: other keep/revert/pass functions in `plugin/lib` (131 files) return a verdict without an n.
  Done when: a lint lists every function that returns a verdict enum and never reads a count. Each is allow-listed with a reason or fixed, and a new unlisted one fails `fm check`.

- **Bind task-text numbers to the code constants** — FIX — value 3 — effort S — risk low — category: developer experience
  Why: T-2583 said 8+ characters while its own example had 7, and a steer fixed it by hand. Existing ideas lint criteria against their examples. This one goes further and compares thresholds in DONE-WHEN text, MASTER.md clauses and docs against the constants the tests pin.
  Done when: a test extracts "N+", "N days" and "N points" from MASTER.md and task criteria. It fails when a nearby named constant differs.

- **Boundary-test every windowed metric against clock changes** — FIX — value 4 — effort M — risk med — category: reliability
  Why: T-2610 added 30-day windows and "newest N" reads, and T-2334 added a late start point. Assumption: none are tested at window edges, across a DST jump, or after a host clock step.
  Done when: a fake-clock suite replays each windowed reader at day 29, 30 and 31, and across a +1h shift. A bet maturing at the boundary is counted exactly once.

- **Run a hook × failure-mode matrix** — FIX — value 4 — effort M — risk low — category: reliability
  Why: The non-tool hook import-failure fix was another user ask. It shows hooks were tested per event but not for each failure.
  Done when: a generated matrix covers every hook event against {import error, timeout, corrupt state file, missing home, read-only disk}. Each cell asserts either "guard still enforced" or "fail-open noted", and none crashes the session.

- **Detect circular evidence in Foreman's own scores** — SECURITY — value 4 — effort M — risk med — category: measurement
  Why: The steers demand signals Foreman didn't author, and T-2554 found Mission briefs counted as user asks. Question missed: "does any score read data that an earlier Foreman step wrote?"
  Done when: each ledger record carries an `author` and a `derived_from` field. `fm doctor` names any metric whose input chain includes its own output. A planted loop turns the check red.

- **Report alive-but-idle timers** — FIX — value 3 — effort S — risk low — category: observability
  Why: T-2542 checks that a timer fired. It does not check that the tick did work, and T-2607 shows ticks can silently skip things.
  Done when: each tick writes a yield count. `fm doctor` WARNs when 5 consecutive ticks ran with zero actions while the inbox was non-empty.

- **Check new requests against standing rules** — FEATURE — value 4 — effort M — risk med — category: user value
  Why: There are 30+ steers, some in tension (pace-off vs risk budget, hold Foreman-filed items). Existing ideas cover already-built duplicates, not conflicts. Assumption: a new ask can contradict a steer without anyone noticing.
  Done when: `fm capture` of "drop work when usage is low" prints "conflicts with 2026-11-01 steer (pace off)". The conflict is recorded on the task.

- **Measure blind-spot latency per bug class (wild)** — FEATURE — value 4 — effort L — risk low — category: measurement
  Why: assumption: the real measure of a blind spot is how long a bug lived before any check caught it. For each user-found bug (T-2554, T-2566, T-2542), run the current sweep against historical commits to find the first one where a check would have flagged it.
  Done when: `fm doctor` shows, per class, "median commits undetected" and the checks that would have caught each historical bug. (wild)

- **Simulate a newcomer from README alone (wild)** — FEATURE — value 4 — effort M — risk low — category: user value
  Why: assumption: authors and the user are blind to first-hour gaps, and T-0862/T-0863 are deferred for lack of evidence. A tool-less child reads only the README and site, then lists where it would get stuck or what it would ask.
  Done when: a nightly job saves the child's stuck-points list. Each point becomes a docs or `fm doctor` task, or is recorded as answered by an existing line. (wild)

- **Plant canaries to detect exam contamination (wild)** — SECURITY — value 3 — effort S — risk low — category: measurement
  Why: the steers require exam scenarios written by a child that never sees Foreman's code. Nothing checks that scenario text hasn't leaked into the repo, lessons or memory, which would let Foreman win by recall.
  Done when: each scenario carries a unique token. A scan fails when any token appears in the repo, lessons, memory files or the published site. (wild)

- **Generate task histories to test state-machine readers (wild)** — CLEAN — value 3 — effort M — risk low — category: reliability
  Why: T-2334 (late start point only for open tasks) and T-2616 (diffs to a task's own commit) are readers wrong for one task state. Question missed: "which state of a task breaks each reader?"
  Done when: a property test generates random histories (reopen, merge, defer, rename id) and runs every ledger reader. The test fails if any reader crashes or contradicts another on the same task. (wild)

Next question: Which of Foreman's published numbers or verdicts were produced by a code path no test ever drove with empty, stale or contradictory input?
Next question: Which fixes after a user correction were applied to the one reported case only, and what is the sibling list for each?
