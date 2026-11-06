# Brainstorm — lens: simplicity

- **Cluster the idea catalog before every round** — FIX — value 4 — effort S — risk low — category: ideation
  Why: "Ideas so far" runs to about 700 lines and repeats itself ("Replay a finished run" appears five times, "factory floor" four). Each round pays the context cost again and the next round echoes the repeats.
  Done when: `fm ideas` hands the next round one title per cluster, with a count and the best exemplar. A test on this pack's list shows at most 150 lines and no two titles above a similarity threshold.

- **Turn on an autonomy dial: `fm trust 0-3`** — FEATURE — value 5 — effort M — risk med — category: permissions
  Why: the user pushed back three times ("stop asking me if you can release", "full auto"). The publish-grant message still sends them through `fm ask` and then `--allow publish`. One dial would replace the grant ritual.
  Done when: at level 3, `fm release --push` runs with no prompt. A guard-corpus replay shows verdicts identical to level 0, and `fm trust` prints what each level allows in five lines.

- **Release when the queue drains (wild)** — FEATURE — value 4 — effort M — risk med — category: release
  Why: six of the user's recent requests are "Release 1.2.4x and push" with a hand-written summary of closed tasks. Release permission is already given as standing.
  Done when: with the setting on and the queue empty and gates green, one command bumps the version, writes the changelog from closed task titles, tags and pushes. A dry-run test on a fixture repo produces the same notes the user would have typed.

- **Expire "Later from" tasks after N releases without evidence** — CLEAN — value 3 — effort S — risk low — category: backlog
  Why: about 35 deferred FEATURE-M tasks (T-0788 to T-0869) are wrappers around idea clusters. They crowd the home screen's queue and inbox, which T-1330 is about to show across projects.
  Done when: a deferred task untouched for 5 releases is moved to the catalog with a one-line receipt, and `fm task list` shows no deferred wrapper older than that.

- **Add `fm where`, one command listing every path Foreman reads or writes** — FEATURE — value 3 — effort S — risk low — category: debuggability
  Why: the user hit a missing PATH link, duplicate Foreman as plugin and CLI, and two separate `models.json` lookups. Which Foreman is live, and where its state sits, is currently guesswork.
  Done when: `fm where` prints the active install, state dir, config, run logs and runner registry, flagging a second install. A test with a planted second copy shows the flag.

- **Classify a task's verify command by why it is red at creation** — FIX — value 3 — effort S — risk low — category: task quality
  Why: the dropped and steered items include a verify with a `<placeholder>` and a test module that doesn't exist. Only the missing-module case is caught.
  Done when: `fm task new` runs each verify once and labels the result "fails on an assertion", "can't start (not found / import / syntax)" or "passes already". Only the first is accepted without a warning, covered by three fixture tasks.

- **Scale the ceremony to the request** — FEATURE — value 4 — effort M — risk med — category: harness
  Why: questions already skip the task. A one-line typo fix still walks plan, task, red check, steps and close, and the user's "it just isn't doing anything" is partly that long wait.
  Done when: a request that touches one file with a one-line diff runs in at most 2 visible stations and still ends with a proved check and a commit. The bench shows the guard verdicts unchanged.

- **Make an unknown command do the nearest sensible thing and say so** — FIX — value 4 — effort S — risk low — category: CLI
  Why: the user's friction phrases include "how come … isn't recognized" and "why can't I…", and `fm code` alone errored with "needs a request".
  Done when: `fm cod`, `fm code tui2` and `fm code --help me` each print "ran: X because you typed Y" or a single "did you mean" line. None exits with a bare usage dump, and a table test covers 10 mistypes.

- **Run `fm gate`, one command for the three gates** — FEATURE — value 3 — effort S — risk low — category: developer experience
  Why: the map lists three separate gate commands (`fm doctor`, `roundtrip.py`, `bench_hooks.py --runs 20`). The recurring CI-red requests suggest they get run unevenly.
  Done when: `fm gate` runs all three and prints one pass/fail line with the failing step's name. CI calls only `fm gate`.

- **Use seven outcomes everywhere** — CLEAN — value 3 — effort M — risk low — category: vocabulary
  Why: assumption: the CLI, TUI, notifications and receipts name results differently ("finish names a red step", "needs you", "blocked", "refused"). A fixed list of done / needs you / stuck / refused / no runner / red / stopped would carry through exit codes, the home screen and the tab title.
  Done when: a lint finds no outcome word outside the list in `fm code` output, and exit codes map one-to-one.

- **Print a "won't do this session" line at start (wild)** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: assumption: with full-auto granted, the user's reassurance is the limits. The line would read like "won't touch other projects, publish, or hooks config".
  Done when: every `fm code` start prints that line, derived from the live grants and guard. A test changes a grant and the line changes with it.

- **Give each setting a sunset test (wild)** — CLEAN — value 3 — effort M — risk low — category: config
  Why: the user wants better config but also less to learn. Each config key would declare the evidence that would let it be deleted, such as "no non-default value in local history for 60 days".
  Done when: `fm doctor` lists keys whose sunset condition is met, and CI fails when a new key has no condition.
