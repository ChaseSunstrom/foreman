# Brainstorm — lens: reasoning ahead

- **Forecast the blocked pile's expiry dates** — FEATURE — value 4 — effort S — risk low — category: blocked pile

  Why: the pack lists about 20 blocked or deferred items (T-0325, T-0335, T-0418, T-1207, and others) with no date on any of them. Each sits until someone notices. Assumption: an item's "blocked on" condition (a platform, a release, an install) has a rough expected unblock time that can be estimated from history.

  Done when: `fm status` shows, for each blocked item, the days since it was blocked and the date it becomes stale, and a test with a fixture pile of ten items prints all ten dates.

- **Warn on version skew before the first write** — FIX — value 5 — effort S — risk low — category: version skew

  Why: T-1791 failed ten bench tests because an inherited window setting leaked in. T-0418 notes that the installed foreman-ui is one version behind. The Claude Code version, the plugin version and the installed `fm` can each drift from the last green gate. Assumption: each run already records these versions in its journal.

  Done when: changing the installed plugin version in a test fixture makes the first `fm` write print one line naming the old and new versions, and the write waits for `--accept-skew`.

- **Gate the plugin install path, not only the checkout** — PERFORMANCE — value 5 — effort M — risk med — category: plugin parity

  Why: the request says every feature must work in the Claude Code plugin. Today the gates run against the repo checkout, while users run the copy written by `fm install-user`. Assumption: the two can diverge in files or paths.

  Done when: the roundtrip test runs against a fresh plugin install in a temp home, and it fails when a command exists in the checkout but not in the installed copy.

- **Route CI jobs by the paths a push touched** — PERFORMANCE — value 4 — effort M — risk med — category: CI cost

  Why: T-1809 cancelled main's newest tests run when the experimental macOS job hit its 35-minute limit, and that cancellation later caused a false red. Assumption: most pushes touch only one platform's code, so the other platform's jobs add cost and no signal.

  Done when: a push that changes only `site/` or docs schedules no macOS job, and a push that changes `plugin/lib/` schedules every job.

- **Classify CI cancellations by cause and rerun the timeouts** — FIX — value 4 — effort S — risk low — category: CI signal

  Why: the session-start sweep already ignores a cancelled newest run, but it cannot tell a superseded run from a timed-out one. A timeout is a real signal that should trigger a rerun or a flag. Assumption: the GitHub run conclusion or the job log distinguishes the two.

  Done when: a fixture with one timed-out and one superseded run produces "rerun" for the first and "ignore" for the second.

- **Show the fixed overhead per run and what it costs at fan-out** — FEATURE — value 4 — effort S — risk low — category: cost at scale

  Why: T-1800 says rules and the operator lens multiply cost at scale, but the output names causes and does not give a number. Each child receives the same pack and the same system prompt, so the overhead scales with lens count times rounds. Assumption: `fm cost` can read the byte size of each always-loaded file.

  Done when: `fm cost --fanout 100` prints the fixed bytes, the tokens they cost and the dollar figure, and that figure matches the sum of the parts in a test.

- **Flag file-set overlap between queued tasks before they run** — FEATURE — value 4 — effort M — risk low — category: conflict forecast

  Why: leases and per-lane worktrees keep parallel edits from clobbering each other, but they detect a clash only after it happens. Two queued tasks that both touch `plugin/lib/fm_queue.py` should run in sequence from the start. Assumption: each task's likely file set can be read from its acceptance checks and past diffs.

  Done when: two fixture tasks sharing one file are queued with a "serialized: shares X" note, and a disjoint pair runs in parallel.

- **Publish a dated list of what will break next** — FEATURE — value 3 — effort S — risk low — category: horizon scan

  Why: T-1804 pinned Node 24 action versions by SHA. Each pin will eventually fall behind a runtime deprecation or a removed action. Assumption: the pinned runtimes and their known end-of-life dates can be listed in a file.

  Done when: `fm doctor` prints a "breaks by" date for each pinned action and runtime, and a fixture with a date already past prints FAIL.

- **Put an expiry on every feature unless the duel earns it** — FEATURE — value 3 — effort M — risk med — category: feature retirement

  Why: the backlog carries more than 300 catalogued ideas, and many features have no measured use. Assumption: duel and usage data can show whether a feature changed an outcome.

  Done when: a feature with no recorded use in 90 days is listed in `fm doctor` with its expiry date, and a feature with recorded use shows no expiry.

- **Replay the hook timing budget across the weekly reset** — PERFORMANCE — value 3 — effort M — risk low — category: hook budget

  Why: the hook bench was noisy at load 0.6 per core, and a single p95 was enough to fail the build. The load on a laptop changes during the day, so one run tells you little. Assumption: the bench can run at several times and loads without much extra cost.

  Done when: the bench reports a verdict from a median over runs at three load levels, and it fails only when the median exceeds the budget at all three.

- **Wild: play the next four weeks forward before choosing the queue** — FEATURE — value 4 — effort L — risk med — category: lookahead planning

  Why: the reset, CI windows, Claude Code releases and blocked items all land on known dates, but the queue is ordered as if they arrive all at once. Assumption: the calendar of resets and releases can be read or approximated.

  Done when: `fm plan --weeks 4` lists which queued tasks run in which week, names the event that gates each, and produces the same plan from the same inputs in two runs.

- **Wild: a tripwire that compares this run's first steps to failed runs' first steps** — SECURITY — value 3 — effort M — risk med — category: early warning

  Why: runs that eventually fail often start the same way, with the same stalled read or the same repeated tool error. Assumption: the journal records each run's first twenty events in a comparable form.

  Done when: a run whose first twenty events match a recorded failure pattern prints a warning before its first edit, and a run with no match prints nothing.

- **Wild: a pre-mortem written by the run, read before it edits** — DEVELOPER EXPERIENCE — value 3 — effort S — risk low — category: pre-mortem

  Why: the proof step catches a failed fix only after the edit. Assumption: a short prediction written before the first edit can be checked against the proof afterward.

  Done when: each closed task's journal contains a one-line prediction and an outcome field, and a fixture task whose prediction is wrong is marked as such in the receipt.
