# Brainstorm — lens: capability map

Capability map, by what the best tools do: anacron and systemd (catch-up, persistence), Airflow (sensors, backfill), Renovate (schedule windows, dashboard), Cronitor (expected-run monitors), Temporal (durable timers), direnv, pre-commit and devcontainers (edge launchers). The pack already covers most scheduler basics, so these are the gaps left.

Answering an earlier question first: the output the user acts on unchecked is silence. "Nothing arrived" is read as "nothing found", and ideas 2 and 3 are the cheapest external checks on that.

- **Route every time read through one injectable clock** — CLEAN — value 5 — effort M — risk low — category: testability
  Why: assumption: the pack only shows an injected clock for the tick. Expiring grants, n/a expiries, deferred revisit dates, quiet hours and lesson decay are all time-dependent features that can't be exercised without waiting.
  Done when: `FM_NOW=<ts>` shifts every module, a ratchet fails on bare `time.time()`/`datetime.now()` outside `fmclock`, and a test replays 30 days across expiry, deferral and quiet hours in under 10 seconds.

- **Re-prove a rotating sample of closed tasks each tick** — FEATURE — value 5 — effort M — risk low — category: ground truth
  Why: the gap is "unmeasured until the exam". A closed task's proof command failing now is an objectively real hit, so precision is measurable with no user and no install.
  Done when: each tick (timer, session edge or manual) re-runs N closed tasks' proof commands and logs pass, fail or could-not-run. A planted regression is caught within one full rotation, and `fm doctor` shows the coverage fraction.

- **Measure readiness lead for every fire** — FEATURE — value 4 — effort S — risk low — category: usefulness metric
  Why: assumption: "useful" is currently proxied by acted-on rate. Whether a result was ready before the user's next session start (completion time minus next SessionStart, from existing logs) is a timing metric that needs no click.
  Done when: `fm doctor` prints the median and the share of fires with lead > 0, computed from ledgers on a fixture of 10 fires.

- **Launch the lazy tick from repo-edge surfaces** — FEATURE — value 4 — effort M — risk med — category: no-install triggers
  Why: the pack covers session edges and git hooks, but not VS Code `folderOpen` tasks, `.envrc`, devcontainer `postStartCommand`, or a global `core.hooksPath`. Each is a smaller ask than a systemd timer and fires on opening the project.
  Done when: `fm triggers launchers` prints the exact snippet for each, and opening a fixture folder writes a tick row with `source=editor|envrc|devcontainer|hook`.

- **Test watchers against a fake forge with faults** — FEATURE — value 4 — effort M — risk low — category: offline testing
  Why: assumption: watchers will poll GitHub. Failure modes such as ETag/304, pagination truncation, rate-limit headers and out-of-order events can't be reproduced from fixture packs.
  Done when: a stdlib fake forge serves a seeded scenario with injected 403/304/page-cut faults, and the watcher files exactly one capture per event while using ≤ 1 API call per quiet poll.

- **Supersede a fired lane when its cause resolves** — FEATURE — value 4 — effort M — risk med — category: stale work
  Why: assumption: a red-CI draft can land after CI went green again (a flake, or a human fix). Nothing in the pack cancels a fire whose premise has since disappeared.
  Done when: a fixture where CI turns green mid-lane marks the draft `superseded` with the reason, and `fm next` doesn't offer it.

- **Smoke-run the docs' commands on a trigger** — FEATURE — value 4 — effort M — risk med — category: useful fires
  Why: the README demo and the site make claims. Extracting fenced shell blocks from README/MASTER and running them in a scratch copy catches rot, with ground truth from exit codes.
  Done when: a planted broken command in a fixture README yields a filed fix capture on the next trigger, and a clean README yields "checked, nothing found".

- **Give each trigger a keep/kill posterior** — FEATURE — value 3 — effort S — risk low — category: statistics
  Why: assumption: a week of live ticks yields few samples. A Beta posterior over useful fires, with a credible interval, says "need 9 more fires to decide" instead of a false verdict.
  Done when: `fm triggers` shows the interval and fires-to-decide per trigger, and a fixture of 3 hits in 4 fires reports "undecided".

- **Mutation-test the due-time logic** — CLEAN — value 3 — effort S — risk low — category: test strength
  Why: the due, catch-up and lease code is where one off-by-one silently skips a day. Existing tests could pass vacuously.
  Done when: a script mutates operators and constants in the due functions, and every mutant is killed or listed as survivor in the report.

- **Follow user activity with an adaptive cadence** — PERFORMANCE — value 3 — effort S — risk low — category: cost
  Why: assumption: a fixed interval wastes ticks overnight and lags during active work. Backoff to hourly when idle and a short interval after commits would cost less.
  Done when: a replayed idle week runs ≥ 50% fewer ticks and the median lateness for a commit-triggered check is unchanged.

- **Run an unwatched-event census** — FEATURE — value 3 — effort M — risk low — category: gap finding
  Why: assumption: triggers get chosen from imagination. Counting what actually happened (reflog, red CI, force-pushes, stale branches) against which events any trigger watches ranks the missing ones.
  Done when: `fm triggers census` lists the top 5 event kinds with count and zero coverage, from a fixture repo history.

- **Wild: set trigger priors from public event archives** — FEATURE — value 3 — effort L — risk med — category: base rates
  Why: wild. Public GH Archive dumps would show how often a human fixes red main within an hour, so Foreman can estimate offline whether an auto-draft would be redundant before it fires.
  Done when: a local script turns one archive day into a per-event-kind "human fixed in under 1h" rate that `fm triggers` cites as the prior.

- **Wild: attach a post-landing obligation to a patch** — FEATURE — value 3 — effort M — risk med — category: git-native triggers
  Why: wild. `fm after` is time-based; a git note keyed by patch-id such as "re-verify X once this lands" would survive rebase and cherry-pick and fire when it reaches main.
  Done when: a note on a commit fires once after a rebased copy lands on main, and never fires if it doesn't.

- **Wild: generate a repo-month with seeded ground truth** — FEATURE — value 3 — effort L — risk med — category: simulation
  Why: wild. A procedural generator (commits, red CI, issues, a user who is away on some days) with held-out seeds scores the tick on cases it can't have been tuned to.
  Done when: seed A tunes and seed B scores, and recall and false-fire rates print for both.

Next question: which time-dependent Foreman features (grants, expiries, deferrals) have never been exercised past their deadline in a test?
Next question: what does a trigger do when its premise is true but the user already handled it by hand minutes earlier?
