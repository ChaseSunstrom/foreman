# Brainstorm — lens: approaches

- **Admit review findings only with a reproducer that fails at HEAD** — FEATURE — value 4 — effort M — risk low — category: review
  Why: four of five recent drops were "already built", "already fixed in T-1847" or "covered in T-1848". Reviewers are citing code that has since changed. The round 5 review also ended with "fixing test-first".
  Done when: a finding with no reproducer, or whose reproducer passes at HEAD, is auto-dropped with the reason "already holds at HEAD" and never reaches the task list.

- **Make triage one JSON-lines engine with thin clients** — CLEAN — value 4 — effort M — risk med — category: backlog
  Why: the review counts four triage surfaces (first, swipe TTY, swipe --serve, app view I) and none has undo or a count of cards left. One engine owns the deck, verdict journal, undo and remaining count. TTY, browser, app and `--pipe` are clients of it.
  Done when: `fm inbox swipe --pipe` reads y/n/d lines on stdin and prints cards on stdout, and the TTY and served variants pass the same engine test, including undo and cards-left.

- **Load ticket providers as `fm-ticket-<name>` executables** — FEATURE — value 4 — effort M — risk low — category: intake
  Why: T-1859 hard-codes Jira and Linear, and GitHub issues are the missing common case. A git-style external subcommand lets `gh issue view --json` and similar tools supply both the fetch and the user's existing auth. Foreman then holds no tokens (assumption: `gh` is installed for most users).
  Done when: `fm inbox ticket https://github.com/o/r/issues/1` works through a `fm-ticket-github` shim, and a dummy provider on PATH is picked up with no core change.

- **Race the last round's tag against this build on the frozen bench** — FEATURE — value 4 — effort L — risk med — category: verification
  Why: "improve past everything shipped" is currently a feeling. T-0866 (bench vs plain Claude) is deferred for lack of cases, so this depends on seeding a small corpus (assumption).
  Done when: `fm round close` runs the corpus on the previous round's tag and on HEAD, prints a pass, cost and time delta, and refuses to close the round if any of the three regressed.

- **Crawl every served page and assert its security and a11y contract** — SECURITY — value 4 — effort M — risk low — category: served pages
  Why: settings serve and swipe serve use a one-shot token and each carries its own style block. The checks cover token on every POST, Host and Origin allow-list against DNS rebinding, labelled controls, and no third-party URLs. CI already turns browser tests off, so a stdlib `html.parser` crawl is the portable proof.
  Done when: a forged Host or Origin header gets 403 on every POST route of every served page, and the crawl test fails if a new page adds a route without the token check.

- **Author the round review from friction in the journal** — FEATURE — value 4 — effort M — risk low — category: feedback loop
  Why: the round 5 review is written from imagination. The journal already holds guard denials (6 destructive blocks today), undos and re-asked questions.
  Done when: `fm review --friction` prints a table per verb of refusals, retries, undos and time-to-success for the last 7 days, and the top 5 rows seed the next round's pack.

- **Prime each session with the model's own top collisions** — FIX — value 3 — effort S — risk low — category: guard
  Why: the risk budget tripped mostly on the model's own `$VAR` paths and `rm` on `/tmp` globs. Refusal text is the late fix, so this is the early one.
  Done when: session start prints at most 3 lines naming the collision patterns seen at least twice in the last 7 days with their safe forms, and prints nothing when there are none.

- **Backtest known fixes against the journal before reporting hit rates** — FEATURE — value 3 — effort M — risk low — category: reliability
  Why: T-1865 made matching safer, but nothing says how often it is right. Replaying past failures through the matcher gives precision and recall now, with no waiting for new data.
  Done when: `fm doctor` shows "known fixes: N offered, M would have been right, K wrong" computed offline, and a signature below 80% precision is flagged for demotion.

- **Express perf assertions in CPU time against a calibration loop** — FIX — value 3 — effort S — risk low — category: tests
  Why: the hook bench and CI browser tests already proved flaky under parallel load, and the scene gallery would add a 1 s render test. Budgets stated as multiples of a tiny reference loop timed in the same process do not care about machine load.
  Done when: a scene render test passes unchanged at `-j1` and `-j16`, and fails when a scene is made 3× slower.

- **Stop the swipe deck once the ranking is stable** — FEATURE — value 3 — effort M — risk med — category: backlog
  Why: more than 30 deferred "Later from" items exist, and the user keeps asking for fewer questions. Showing the card whose verdict would change the ranking most (uncertainty sampling) ends the session early. Assumption: the prefer model exposes a confidence score.
  Done when: on a fixture backlog of 40 items the deck ends in fewer than 40 cards with the same top-10 as a full pass.

- **Ship the swipe deck as a self-contained HTML file** — FEATURE — value 3 — effort M — risk low — category: served pages
  Why: no server means no one-shot token and no Ctrl-C. The page keeps verdicts and undo locally, then exports a verdicts file that `fm inbox swipe --import` applies. The trade-off is no live sync.
  Done when: `fm inbox swipe --html out.html` opens from `file://`, supports undo, and a downloaded verdicts file imports to the same state as the served version.

- **Wild: let the guard search for its own safe rewrite** — FEATURE — value 3 — effort M — risk med — category: guard
  Why: a refusal today just says no. The guard tries a bounded list of mechanical rewrites (literal path, quoted variable, narrowed glob) and uses itself as the oracle. Only a rewrite that passes the guard and is equivalent on a dry-run listing gets printed.
  Done when: a refused `rm -rf $TMPDIR/x*` prints a literal-path form that the guard then accepts, and no rewrite is offered for a genuinely destructive command.

- **Wild: serve bookmarkable pages by socket activation** — FEATURE — value 2 — effort L — risk med — category: served pages
  Why: replaces "launch, copy token, Ctrl-C" with stable `localhost` URLs that start on demand and exit when idle, with a plain-process fallback where there is no systemd. Assumption: most users are on Linux with a user systemd.
  Done when: `/swipe` and `/settings` open from a bookmark after a reboot, and the process exits after 10 idle minutes.

- **Wild: add a silence-as-consent countdown mode to triage** — FEATURE — value 2 — effort S — risk med — category: backlog
  Why: the user dislikes being asked and has said "I shouldn't have had to tell you". In `--auto` mode each card shows its default verdict and a 5-second ring. Touching it overrides, and silence applies the default, which is always reversible.
  Done when: an untouched deck resolves all cards to their defaults, and every auto-verdict can be undone from the verdict journal.
