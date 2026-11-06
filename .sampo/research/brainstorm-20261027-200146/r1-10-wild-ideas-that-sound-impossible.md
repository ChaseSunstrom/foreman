# Brainstorm — lens: wild: ideas that sound impossible

- **Route playbooks by compiled index, not per-request search** — FEATURE — value 5 — effort L — risk med — category: routing
  Why: the pack asks for tens of thousands of playbooks, routed but not loaded, and fm playbooks route is the path that must stay fast. Wild: assumption that a prebuilt, incrementally updated index (trie or inverted map over triggers) can route 10k+ entries without reading any playbook body.
  Done when: on a synthetic 10,000-playbook library, `fm playbooks route` picks the same playbook as the current router on 200 sample queries, with p95 under 5 ms and zero playbook bodies read.

- **Stop the Claude Code window from fighting the gate lock** — FIX — value 4 — effort S — risk low — category: concurrency
  Why: the user reported that `fm check --affected` and `--evidence` take the machine-wide gate lock, so every builder's affected run waits behind the others.
  Done when: a test runs two `fm check --affected` invocations concurrently in one repo and asserts neither acquires the gate lock and neither waits.

- **Bound the full-check gate wait and say so** — FIX — value 3 — effort S — risk low — category: concurrency
  Why: a hung check in another project held the lock for over 40 minutes; the user asked for a 15-minute cap, then a run beside it with a notice.
  Done when: with a fake lock holder that never releases, `fm check` proceeds after 15 minutes and prints a line naming the holder.

- **Make `fm quiet` pass stdin through** — FIX — value 4 — effort S — risk low — category: CLI
  Why: the user reported that a heredoc script fed to `fm quiet` does nothing and exits 0.
  Done when: `fm quiet bash <<'EOF'` with `echo hi` prints `hi` and its exit code matches the inner command's exit code, asserted by a test.

- **Tie edit leases to process liveness, not a 20-minute timer** — FIX — value 4 — effort S — risk low — category: concurrency
  Why: the user reported that a model run's edit leases outlive it (drop_session ran only for worker runs), so the next run on the same code is refused for 20 minutes.
  Done when: after a model run is killed mid-edit, a new run on the same code acquires the lease within 1 second, asserted by a test.

- **Skip "n/a" and "new playbook" in the catch-it-earlier follow-up** — FIX — value 2 — effort S — risk low — category: task close-out
  Why: the user reported that `fm task finish` files a "Catch it earlier" follow-up for why-not-caught answers like "n/a" or "new playbook", where there is nothing to catch.
  Done when: `fm task finish` with a why-not-caught of "n/a" or "new playbook" creates no follow-up task, while a real answer still creates one.

- **Put the headless-rendering probe in fm doctor** — FEATURE — value 3 — effort S — risk low — category: diagnostics
  Why: the user asked for a probe that reports whether headless rendering is available, or why not.
  Done when: `fm doctor` prints "headless render: available" on a machine with a working browser and the specific missing piece otherwise, checked on both.

- **Trim the rules file under the doctor's budget and keep it there** — CLEAN — value 3 — effort S — risk low — category: docs budget
  Why: the rules file is 6,416 characters against the doctor's 6,400 budget, a state that has held since T-1520.
  Done when: `fm doctor` reports the rules file at or under 6,400 characters and a test fails if a later edit pushes it over.

- **Predict a task's token cost before it runs** — FEATURE — value 5 — effort M — risk low — category: usage budget
  Why: the user said Foreman should have noticed its own usage burn unprompted, and the pack shows the cost was found only after the fact; assumption: past run journals hold enough per-task token data to fit a rough estimate.
  Done when: `fm cost --predict` on 10 closed tasks reports an estimate within 30% of the measured tokens for at least 8 of them.

- **Sign every allowed command into a local hash-chained log** — FEATURE — value 3 — effort M — risk low — category: audit wild
  Why: wild; the guard hook already decides each Bash call, and a tamper-evident record of what was allowed is an unusual extra for a local plugin; assumption: users will want to prove later what ran.
  Done when: each allowed Bash call appends one hash-chained line, and `fm verify` reports the first line as broken after a single line is edited by hand.

- **Send a red-team subagent after every fix before close** — FEATURE — value 4 — effort M — risk med — category: verification wild
  Why: wild; `fm task prove` shows the test fails without the change, but nothing tries to break the fix itself; assumption: an adversarial subagent catches regressions the author's test misses.
  Done when: on 5 seeded regressions that pass the existing tests, the red-team step flags at least 3 and each flag names a failing command.

- **Replay closed tasks overnight in a shadow copy to catch silent breakage** — FEATURE — value 3 — effort L — risk high — category: regression wild
  Why: wild; the pack shows repeated post-merge breakage (test_followups, the test that broke on the 300-character help position) that a nightly replay of closed tasks against main could surface before the user does; assumption: replay time and cost fit an overnight budget.
  Done when: a scheduled run replays 20 closed tasks in a temp copy and writes a report that lists any task whose checks now fail, with zero changes to the real repo.
