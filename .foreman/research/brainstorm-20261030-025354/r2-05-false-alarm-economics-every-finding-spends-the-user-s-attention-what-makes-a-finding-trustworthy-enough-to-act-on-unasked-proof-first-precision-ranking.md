# Brainstorm — lens: false-alarm economics: every finding spends the user's attention; what makes a finding trustworthy enough to act on unasked (proof first, precision, ranking)

- **Price every finding in attention-minutes before it is shown** — FEATURE — value 5 — effort M — risk low — category: ranking
  Why: the exam shows 0/108 found by finders, so any new finder will be noisy at first; the user's attention is the scarce budget. assumption: a finding costs ~2 min to read, ~10 to judge, ~30 to fix by hand.
  Done when: every finding line shows `P(real)`, minutes-to-judge and minutes-saved-if-real, and a test confirms findings with expected value below the cost are written to the ledger but never surfaced.

- **Make the red-on-untouched-tree test the only admission ticket** — FEATURE — value 5 — effort M — risk low — category: proof
  Why: Mission 3 asks to "prove each finding with a failing test"; plain Claude's 3/3 comes from running code, not reading it. Hypotheses must not reach the user.
  Done when: a finding with no test that fails on the clean checkout is stored as `hypothesis` and a test asserts `fm find list` omits it by default.

- **Reject proofs that fail for the wrong reason** — FIX — value 5 — effort M — risk med — category: proof
  Why: a test that is red from an ImportError, a missing fixture or a timeout is a false alarm that looks proven. assumption: the finder will write tests itself.
  Done when: each proof records a pinned failure signature (the assertion text, not just exit code), and a fixture where the test fails on a missing import is rejected as `proof-invalid`.

- **Score finders on clean repos before they may file anywhere** — FEATURE — value 5 — effort M — risk low — category: precision
  Why: the exam has a `none` kind graded on never-seen repos; a finder that cries wolf on clean code fails Mission 3 directly.
  Done when: `fm find calibrate` runs each finder over a set of clean fixture repos, and a finder with any filed finding is flagged `muted` and cannot queue tasks.

- **Make "clean" a first-class, evidenced verdict** — FEATURE — value 4 — effort S — risk low — category: trust
  Why: `none` exam kind; silent empty output is indistinguishable from "didn't look".
  Done when: a scan of a clean fixture prints `clean: N files read, M probes run, K candidates refuted`, and exits 0.

- **Keep a refutation ledger so dismissed findings never return** — FEATURE — value 4 — effort S — risk low — category: memory
  Why: the user's steers show repeat annoyance (re-ship, re-match); a dropped finding re-filed is the costliest false alarm. assumption: fingerprint = test name + normalised failure text + file hash of the symbol.
  Done when: dropping a finding then rescanning an unchanged tree surfaces zero repeats, and a changed symbol resurrects it with a note.

- **Auto-mute a probe by measured precision, per ecosystem** — FEATURE — value 4 — effort M — risk med — category: precision
  Why: finders span python, js, ts, ruby, rust and c; precision will differ widely.
  Done when: each probe has `kept/filed` over its last 20 filings, and one below a configurable floor stops queuing and says so in `fm find status`.

- **Cap unasked findings per day and spend the cap on the top-ranked** — FEATURE — value 4 — effort S — risk low — category: budget
  Why: unasked work competes with what the user requested; assumption: a default of 3 per day.
  Done when: with 10 proven findings only the 3 highest-value surface, the rest are listed as `held` with their score.

- **Stop Foreman's own setup faults from becoming user-project findings** — FIX — value 4 — effort S — risk low — category: noise
  Why: the pack notes probe_doctor may queue Foreman setup failures as tasks in user projects.
  Done when: a project with a broken hook install produces a doctor warning and zero backlog tasks.

- **Wild: Plant canary bugs in a scratch copy and publish the recall/precision before trusting a scan** — FEATURE — value 4 — effort L — risk med — category: calibration
  Why: wild; Foreman's finders scored 0/108, so a self-measured score on the user's own repo shows whether this scan deserves attention.
  Done when: a scan begins with `canaries: caught 4/5, false alarms 0` and a scan with recall below 3/5 is labelled low-confidence.

- **Wild: A cold refuter model must reproduce each finding from its text alone** — FEATURE — value 4 — effort M — risk med — category: second opinion
  Why: wild; a finding that a context-free agent cannot reproduce is probably unclear or false, and it is cheaper than the user finding that out.
  Done when: a finding whose report fails cold reproduction is demoted to `unconfirmed`, and the receipt records both agents' verdicts.

- **Wild: A "do nothing" receipt that credits restraint** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: wild; the best result of a nightly scan is often silence, and the user should see it earned.
  Done when: a morning with no surfaced findings prints one line with candidates examined, refuted and held, plus tokens spent.

- **Revert-learning: a reverted fix lowers its probe's rank weight** — FEATURE — value 3 — effort M — risk low — category: ranking
  Why: the strongest outside signal is `fm outcomes` 30-day survival; the user's reverts show which findings were not wanted.
  Done when: reverting a fix commit lowers that probe's weight in the next ranking, and a test shows the order changing.

Next question: What does a true positive earn the user in minutes saved, so the attention price in the ranking is measured rather than assumed?
Next question: When two independent provers disagree on one finding, which one does the user see, and is the disagreement itself a signal worth showing?
