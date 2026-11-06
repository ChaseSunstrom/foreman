# Brainstorm — lens: inversion

- **Don't let Genesis-made work count as "queue dry"** — FIX — value 5 — effort S — risk low — category: auto-start
  Why: auto-start fires when the queue runs dry, but a tower files tasks, which refills the queue and re-arms the trigger. That loop never ends. Assumption: tower-filed tasks have no origin tag today.
  Done when: a fixture where the tower closes all its own tasks does not auto-start again until a user-originated task has closed since the last tower.

- **Cap open Genesis tasks and rank them below the user's** — FEATURE — value 4 — effort S — risk low — category: queue hygiene
  Why: assumption: a sweeping "make this great" can emit hundreds of tasks (the earlier brainstorm cluster had 29 one-offs and 7-24 idea piles). That buries the user's own deferred items (T-0034 and the others) and dilutes `fm loop` picks.
  Done when: with the cap at N, the (N+1)th Genesis task goes to the not-yet ledger. A user task always sorts ahead, and Genesis tasks untouched for K days expire with a logged reason.

- **Score parent and child on the same exam run** — FIX — value 5 — effort M — risk med — category: selection
  Why: "a rewrite stays only if it closes more scenarios than its parent" breaks if the parent's score came from an earlier exam version or a cached result. Caching is a proposed idea elsewhere in the list. Comparing numbers from different exams is the quiet way selection goes wrong.
  Done when: every selection record cites one exam hash and both arms' results from that run. A test that swaps in a cached parent score from another hash fails the selection step.

- **Ship a no-gap fixture where the right answer is "nothing to do"** — FEATURE — value 4 — effort S — risk low — category: anti-busywork
  Why: every fixture so far plants gaps, so Genesis is only ever rewarded for finding work. Given "make this great" on a finished project it will manufacture edits. Assumption: no current fixture is already clean.
  Done when: on the clean fixture the tower ends with an empty diff and a one-line "nothing to do". Any commit fails the exam.

- **Propagate taint from untrusted text into every tower claim** — SECURITY — value 5 — effort M — risk med — category: injection
  Why: earlier ideas treat stranger text as data and tag sources. They don't stop a poisoned README sentence from being paraphrased into a MUST, then copied into carry-over defaults, then into the next project. Taint must survive rewriting.
  Done when: a planted "always run curl|sh" line in a fixture README shows up in no MUST, NEVER, guard rule or carry-over default without a user-ratified marker. A canary test asserts this across two generations.

- **Flag MUSTs that only the current code supports** — FIX — value 4 — effort M — risk med — category: gen-0 quality
  Why: a gen-0 written "from one line or nothing" by reading the code can turn existing bugs into requirements. Then drift check and selection defend the bug. Assumption: the writer draws from code as well as docs and the user's history.
  Done when: on a fixture with a planted off-by-one, the writer marks the resulting MUST "code-only, unconfirmed". The scenario derived from it can't count toward selection until the user confirms it.

- **Re-read the user's steers at every stage boundary** — FEATURE — value 4 — effort M — risk low — category: user control
  Why: the user steers constantly (the "I don't mean to hardcode" correction, the standing rules). A long tower that only read steers at start would run against a correction made an hour in.
  Done when: a steer added mid-run pauses the tower at the next boundary and re-runs the drift check against it. The status line says which steer caused the pause.

- **Detect rubber-stamp approvals and raise the bar** — SECURITY — value 3 — effort S — risk low — category: consent
  Why: every gate (auto-start, new grant, publish) ends in "the user's yes". A flood of Genesis proposals teaches yes-by-reflex, which empties the gate of meaning. Assumption: approvals are timestamped.
  Done when: three approvals in a row under a few seconds, each of an item with a nonzero spend or grant, switch the next one to a restate-to-confirm form. A unit test covers the trigger.

- **Make "yes" a scoped, expiring consent token** — SECURITY — value 4 — effort M — risk med — category: consent
  Why: the system's own rule is that approval in one context doesn't extend to the next. A bare "yes" to auto-start could be read as covering spend, publishing and new paths.
  Done when: a yes stores a record of spend ceiling, publish yes/no, paths and expiry. A stage outside the record halts and asks. An expired token blocks a resume.

- **Lock the tower per host and catch sync conflicts** — FIX — value 3 — effort S — risk low — category: reliability
  Why: assumption: tower storage under the home directory may be synced between a laptop and a desktop. A single-owner lock holds on one host but not across two, so two machines could write diverging generations.
  Done when: the lock names the host. Opening a tower whose files carry another host's newer write, or conflict-copy filenames, refuses to run and prints the conflict.

- **Render the receipt from ledgers, boxing model prose** — FEATURE — value 4 — effort M — risk low — category: honest reporting
  Why: the tower reports its own wins, which is the setting where an optimistic summary slips in. Earlier ideas lint numbers in docs, but the morning digest and status are the first thing the user trusts.
  Done when: every number and verdict in the receipt comes from code reading the cost, exam and lineage files. Model-written text sits in a labelled "commentary" box. A test shows an edited ledger changes the receipt and nothing else does.

- **Add a cross-project quota arbiter** — FEATURE — value 3 — effort M — risk med — category: economics
  Why: per-run budgets cap one tower, but five projects each within their own cap can still burn the whole week. Assumption: nothing sums spend across projects today.
  Done when: a global weekly ceiling pauses every tower's next generation once reached, and the pause reason names the ceiling in the status.

- **Sabotage lane: prove the exam goes red (wild)** — FEATURE — value 4 — effort M — risk low — category: exam trust
  Why: wild. The oracle and empty arms prove the exam can pass and fail. Neither proves it notices a plausible degradation. Run a throwaway lane told to make the project worse in a subtle, realistic way, such as a dropped edge case or a loosened check.
  Done when: for each scenario kind, at least one sabotage turns some scenario red. Kinds nothing catches are listed as blind.

- **Poisoned-tower drill: plant a wrong line, see who notices (wild)** — SECURITY — value 3 — effort M — risk low — category: self-checks
  Why: wild. Drift check, resume handshake and lint are all proposed, but none is shown to catch anything. On a scratch copy, invert one MUST, backdate a claim and edit a lineage verdict, then open the tower fresh.
  Done when: each of the three plants is caught by some named check. Uncaught plants become exam scenarios for Genesis itself.

- **Turn each Genesis incident into a replayable regression case (wild)** — CLEAN — value 4 — effort M — risk low — category: self-regression
  Why: wild, and assumption: aborts, loops and bad selections are logged but not kept as tests. The user already cares about "built but never run" and unpredicted asks. Genesis's own failures should join the suite.
  Done when: an abort on any fixture writes a minimal case file. `fm exam` replays it and passes after the fix.

Next question: Which of Genesis's own stages (auto-start, publish, selection, carry-over) has no check that runs when its inputs are hostile or empty?
Next question: When the user rejects a tower or reverts its work, what does Genesis learn about why, and does the next auto-start proposal reflect it?
