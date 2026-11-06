# Brainstorm — lens: simplicity

- **Make a release net-negative in lines** (wild) — CLEAN — value 3 — effort S — risk low — category: simplicity
  Why: the pack shows steady growth: 1,832 files, 1,229 skills, and a list of extras added in one commit (T-1556). Nothing measures what a release removes. Wild: every merge to main must delete at least as many lines as it adds, unless the commit is tagged as a fix to a failing gate.
  Done when: a CI step prints net lines per merge to main, and a merge that adds more than it removes without the tag fails.

- **Give every fm command a budget of one** — CLEAN — value 3 — effort S — risk low — category: developer experience
  Why: `help` position 306 is shared by two commands, so `test_help` already fails. The same pressure will keep growing the command list.
  Done when: a test fails when the top-level command count rises without a matching removal or alias, and the current help table has no shared positions.

- **Let `fm init` ask nothing** — FEATURE — value 4 — effort S — risk low — category: user value
  Why: assumption: a new user faces settings in three scopes (this run, this project, everywhere) plus repo policy pins, and the pack shows settings overlap. First run should infer the defaults and print the three values it chose, with one line to change each.
  Done when: `fm init` in an empty repo finishes with no prompts and prints exactly three chosen values, and `fm config` shows the same three.

- **Fold `check --affected`, `--evidence` and the full gate into one `fm check`** — CLEAN — value 4 — effort M — risk med — category: simplicity
  Why: the pack lists three entry points that each take the machine-wide gate lock, and the open requests ask to fix their waits one at a time. One command that picks the scope from the diff would remove the choice users and agents have to make.
  Done when: `fm check` with no flags runs the affected set on a small diff and the full gate on a large one, and a test shows each path is selected from the diff size.

- **Gate the hook bench on median only, report p95** — CLEAN — value 3 — effort S — risk low — category: performance
  Why: the dropped item shows p95 flaking near its 300 ms budget (about 310 ms under load), while the median was 266.5 ms on a quiet machine. A p95 threshold is the noisy number. Assumption: the median is stable enough to gate on.
  Done when: `bench_hooks --runs 20` fails only when the median exceeds budget, and p95 still prints in the report.

- **Move every extra behind one switch** — CLEAN — value 3 — effort S — risk low — category: simplicity
  Why: T-1556 added a zine, a vase, cursor choreography, Breakout and sonic recipes to the default surface. Assumption: most users never use them, and they add startup and test cost.
  Done when: `fm extras off` (the default) removes them from the help, the pane and the test run, and a test shows the core loop runs with them disabled.

- **One line of output per command, detail behind `-v`** — CLEAN — value 4 — effort M — risk low — category: user value
  Why: the pack has several receipt, status and why-explanation requests, each adding more text to the default output. Assumption: default output should be the answer, with the reasoning optional.
  Done when: every command's default output is at most one line on success, and a test fails any command whose default output runs longer.

- **Make `fm doctor` end with one verdict line** — FEATURE — value 3 — effort S — risk low — category: user value
  Why: the doctor already runs many probes and budget checks, including the rules file over its 6,400-character budget (6,416 characters). A user wants to know whether things are fine and what to do next, not the full list.
  Done when: `fm doctor` ends with `ready` or one named fix, and the exit code matches the verdict.

- **Build the shared game block once, at build time** — CLEAN — value 2 — effort S — risk low — category: simplicity
  Why: the dropped City and graph item says ~150 lines of camera, input and survival JS are copied, and `test_showpieces` asserts the copies stay identical. A build-time include removes the copy and the test that guards it. This is smaller than the deferred runtime module.
  Done when: `city.html` and `graph.html` are generated from one source, and `test_showpieces` checks the generated output without comparing two hand-kept copies.

- **Delete code no real run has touched in 90 days** (wild) — CLEAN — value 2 — effort M — risk med — category: simplicity
  Why: assumption: coverage from real runs, recorded in the journal, shows which modules and skills are never reached. Wild: a nightly job proposes deletions as small pull requests, and each one must pass the full gate and name the last run that would have used it.
  Done when: a report lists unreached files with their last-touch date, and a proposed deletion passes the gate without changing any recorded run.

- **Silence on success** (wild) — FEATURE — value 2 — effort S — risk low — category: user value
  Why: assumption: a clean gate and clean hooks create noise in the transcript. Wild: a passing run prints only its exit code and a single word in the pane, and the full receipt is kept in the journal for anyone who asks.
  Done when: a passing `fm check` run writes at most one line to stdout and the full receipt is still readable with `fm why`.

- **Name each command as the user's verb** — CLEAN — value 2 — effort M — risk low — category: developer experience
  Why: the open items already use plain words (defer, finish, why, quiet), but the help table has grown by addition, so names overlap in meaning. Assumption: a short glossary test catches new names that clash.
  Done when: a test fails when two commands share a verb or when a new command name is not in the glossary file.
