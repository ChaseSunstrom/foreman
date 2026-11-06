# Brainstorm — lens: bold bets

- **Run the Mission at three widths and let outcomes pick** — FEATURE — value 5 — effort L — risk med — category: exhaustiveness
  Why: the pack's carried gap is "says what it left out", yet the scope width is chosen once and silently. Assumption: lanes (`fm lane`) can run three Mission variants (narrow, as asked, exhaustive) in worktrees in parallel.
  Done when: one request produces three briefs sets with price and Exam readings side by side, and the page records which width the user kept.

- **Ship Exam capsules that run with no Foreman installed** — FEATURE — value 4 — effort M — risk low — category: proof
  Why: Exams that name a live-state reading depend on session state that won't exist for a cold process (earlier open question). Assumption: a capsule is a tarball of the commit, one POSIX-sh script, and the expected line.
  Done when: `sh exam.sh` in an empty directory on a machine without `fm` prints the same pass/fail line as `fm` did, and the capsule is attached to the closed brief.

- **Settle every dissent automatically at +14 days from existing records** — FEATURE — value 5 — effort M — risk low — category: calibration
  Why: the request's first carried gap is "dissents scored against outcomes", and `fm outcomes` already has a 14-day close-survival signal. Assumption: reuse that signal rather than a new one.
  Done when: a dissent filed 14+ days ago shows right, wrong or never-observed in `fm outcomes`, and a lens's dissent hit rate appears in the next pack.

- **Make a clause-ablation gate for requests** — FEATURE — value 4 — effort M — risk med — category: coverage
  Why: "covers the whole space" is unfalsifiable now. Assumption: re-running intake with each clause deleted is cheap with a Haiku child.
  Done when: any clause whose deletion changes no brief is listed under "possibly ignored", and a test with a planted ignored clause fails without the gate.

- **Run a nightly Foreman-vs-itself cold reconstruction of the last Mission** — SECURITY — value 3 — effort M — risk low — category: trust
  Why: standing rule wants signals Foreman didn't author. Assumption: a tool-less child sees only the request and the filed briefs, then lists what it expects was left out.
  Done when: the diff between that list and the real "left out" slip is recorded each night, and a miss shows on `fm doctor`.

- **Seal unattended Missions inside a no-network, no-write capsule for Exam readings** — SECURITY — value 4 — effort M — risk med — category: sandbox
  Why: live-state commands in Exams run on the user's machine; one could write or phone out. Assumption: bubblewrap or Landlock is available on this hardened kernel.
  Done when: an Exam command that writes a file or opens a socket is refused and recorded as "unsafe reading" instead of passing.

- **Keep a local-only brainstorm mode with a pack-egress diff** — PRIVACY — value 4 — effort M — risk low — category: local-first
  Why: packs contain the user's verbatim asks; the cloud send is implicit. Assumption: a local engine can run at least the capability-map and approaches lenses.
  Done when: `fm ideas --local` sends zero bytes off-box (verified by a network-denied run) and the cloud mode prints the exact bytes first.

- **Add a pocket "left-out" digest pushed to phone** — FEATURE — value 3 — effort S — risk low — category: devices
  Why: unattended Missions end with a slip the user finds only at the terminal. Assumption: ntfy or a mail monitor exists as a sink.
  Done when: a finished Mission sends one message of five lines or fewer with the sting cell first, and replying "do 2" files a task.

- **Cap sub-agent breadth by a Mission's measured dissent yield** — PERFORMANCE — value 3 — effort M — risk low — category: agents
  Why: lenses that go dry still cost a child (T-0829 deferred). Assumption: lens_rates already records dry runs.
  Done when: a lens dry three Missions in a row is skipped and named on the slip, and costs drop in `fm burden` without a drop in accepted ideas.

- **Delete a Mission field for every one it adds** — CLEAN — value 3 — effort S — risk low — category: simplicity
  Why: Exam now owes outcome and live-state lines; the brief template only grows. Assumption: a lint can count fields per template.
  Done when: a change to the brief template that raises the field count fails `fm check` unless it removes one.

- **Generate the Exam cookbook in MASTER.md from real passing Exams** — FEATURE — value 3 — effort S — risk low — category: docs
  Why: builders invent outcome measures from scratch and can game them. Assumption: closed briefs hold working examples.
  Done when: MASTER.md has a section of ten measure patterns each linked to a closed brief, and a new Exam can cite one.

- **(wild) Let the dissenter stake its lens weight** — FEATURE — value 3 — effort M — risk med — category: market
  Why: assumption: a lens that bets and loses loses brainstorm slots, a cheap honest signal. wild
  Done when: a lost dissent lowers that lens's next-pack share and the page shows the stake and result.

- **(wild) Send a dated postcard from the future Mission** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: assumption: a child writes "what went wrong after this shipped" at close; it resurfaces at +30 days beside the real record. wild
  Done when: the postcard appears in the session-start card on its date and the user can mark it "right".

- **(wild) Hunt Foreman's own blind spots with a hostile first-day user child** — SECURITY — value 3 — effort M — risk med — category: red team
  Why: assumption: a child told only "you are impatient, typing odd things" drives `fm` in a pty and logs every refusal that gave no Next line. wild
  Done when: the run's list of dead-end outputs is filed as tasks, and each dead end gains a Next line.

Next question: which clauses of past requests did the user have to restate a second time, and which grid cell would have caught each?
Next question: does the user read the left-out slip at all, or only the briefs, and what does that say about where to put it?
