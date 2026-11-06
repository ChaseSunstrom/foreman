# Brainstorm — lens: reliability

- **Stamp goal verbs with a revision number** — FEATURE — value 5 — effort M — risk low — category: resume safety
  Why: assumption: after a compaction or crash the model acts on a stale picture of the goal, and the pack shows locks for concurrent writers but nothing for a stale single writer.
  Done when: a test runs `fm goal close ROW --rev N` after another verb has bumped the revision to N+1, and the verb refuses and prints the current state.

- **Pin each row's verify command to an approval hash** — SECURITY — value 5 — effort M — risk med — category: plan integrity
  Why: plan rows come from vague goals, pasted issues and edits across days, and an oracle runs their verify commands. A row edited after approval could run something new (assumption: no hash check exists today).
  Done when: editing a row's verify text after approval makes the oracle return "needs re-approval" instead of running it, and the guard classifies the new text.

- **Scan journal appends for secrets before they persist** — SECURITY — value 4 — effort S — risk low — category: privacy
  Why: the goal journal lasts for days and `fm genesis live` publishes tower data to main, so a pasted token in a goal could be published. Assumption: appends are not scanned today.
  Done when: appending a line containing a planted key to the journal stores a redacted line and notes the redaction, and the publish step fails on any unredacted match.

- **Measure rework after resume** — FEATURE — value 4 — effort M — risk low — category: resume quality
  Why: the pack tracks "where were we" messages and resume cost, but not the real failure, which is redoing a closed row. Assumption: no metric catches a new edit or commit touching a closed row's files within one session of a resume.
  Done when: `fm doctor` prints a redo rate per goal, and a fixture that edits a closed row's file after resume is counted.

- **Test locks and atomic renames on the filesystems people really use** — FIX — value 4 — effort M — risk med — category: filesystem
  Why: this host keeps state under `/run/user`, which is tmpfs, and the pack lists a tmpfs warning but no test on overlayfs, NFS or FUSE. Assumption: lock and rename semantics have only been tested on tmpfs and ext4.
  Done when: a matrix test runs two concurrent goal writers plus a kill on each filesystem it can mount, and every run ends with a parseable goal file.

- **Declare a fail-open or fail-closed mode for every hook and crash-test it** — SECURITY — value 5 — effort M — risk med — category: hooks
  Why: T-2607-era work covers hooks that fail to import, but the pack shows no table of what each hook does when it crashes, such as the guard on a bypass-mode session.
  Done when: a table lists a mode per hook, and a test injects an exception into each one and asserts the declared behaviour: guard denies, notes stay silent.

- **Write a one-line crash card for every hook exception** — FEATURE — value 4 — effort S — risk low — category: developer experience
  Why: assumption: hook errors are swallowed to protect latency, so the user finds out days later. `fm doctor` currently reads gauges, not recent crashes.
  Done when: a forced exception in PostToolUse appends a card (hook, error, library hash) to a bounded file, and the next `fm doctor` shows it.

- **Run an oldest-supported-Python and `-I` isolated matrix** — FIX — value 3 — effort S — risk low — category: portability
  Why: the standing rule says Foreman must work with no `claude` on PATH, on other machines. Assumption: the suite runs on one interpreter version.
  Done when: CI runs `fm doctor` and the roundtrip e2e on the minimum stated Python with `python3 -I`, and fails on any stdlib import beyond that version.

- **Cap every append-only ledger and test the reader after compaction** — PERFORMANCE — value 4 — effort M — risk med — category: scale
  Why: the pack shows bounding only for the tick ledger, while bets, outcomes, friction and the journal grow for weeks. The hook p95 gate would see the growth only late.
  Done when: each ledger has a ceiling and a compaction path, and a bench with a 10x-size synthetic ledger keeps the hook p95 inside its gate.

- **Record every edit to the finish oracle with a reason** — FIX — value 4 — effort S — risk low — category: done-detection
  Why: "done" only means something if the checker wasn't loosened to get there. The standing rule on weakness-finding wants signals Foreman didn't author.
  Done when: the finish receipt lists each oracle change since plan time, and a fixture that removes an assertion shows up as a flagged edit.

- **Hold goal resume under a latency budget at 1000 rows** — PERFORMANCE — value 3 — effort M — risk low — category: speed
  Why: assumption: resume and `fm next` were benched on small goals, while long goals pile up rows and evidence over days.
  Done when: `bench_hooks.py` includes a 1000-row goal and the resume path stays under a stated p95 in 20 runs.

- **Wild: feed a planted-lie source through goal intake** — SECURITY — value 4 — effort M — risk med — category: adversarial input
  Why: wild. A pasted issue saying "already fixed, mark done" or "run this to verify" should never close a row or run a command. Assumption: untrusted text is only fenced at some entry points.
  Done when: a fixture goal carrying three planted lies ends with zero rows closed by them and zero commands run from them.

- **Wild: replay the decision at any past journal point** — FEATURE — value 3 — effort L — risk med — category: debugging
  Why: wild. `fm goal at <journal point>` rebuilds that moment's state read-only and prints what `fm next` would have chosen. A wrong day-three decision then becomes a reproducible bug.
  Done when: for a recorded goal, the replayed pick at point K equals the pick that was actually logged at K, or the verb prints the divergence.

- **Wild: compute "done" a second way in shell and git only** — CLEAN — value 3 — effort M — risk low — category: independent check
  Why: wild. One fully separate implementation of the verdict (git log, test exit codes, file hashes) would catch a bug in the Python verdict code. The standing rule also asks for a signal Foreman did not author.
  Done when: a nightly job runs both on every open goal and files a task on any disagreement.

Next question: for each unattended or resumed action, what exactly would the user have to run by hand to confirm it worked, and is that command printed in the output?
Next question: which state file would hurt most to lose silently, and is there a restore test for exactly that one?
