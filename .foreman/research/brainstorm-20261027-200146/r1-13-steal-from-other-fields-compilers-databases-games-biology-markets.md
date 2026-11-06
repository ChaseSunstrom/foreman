# Brainstorm — lens: steal from other fields (compilers, databases, games, biology, markets)

- **Cache the context pack prefix so every lens reuses it** — PERFORMANCE — value 5 — effort S — risk low — category: token cost
  Why: each brainstorm child gets the whole pack, and the user wants usage cut. Compilers reuse a parsed prefix across translation units. Assumption: the pack is identical across lenses apart from the lens line.
  Done when: `fm cost` for one brainstorm round shows input tokens for lenses 2..N down by about the pack size versus the measured baseline.

- **Turn the gate lock into a ticket queue, not one mutex** — FIX — value 4 — effort M — risk med — category: gate lock
  Why: `fm check --affected` waits behind full checks, and the user asked for the 15-minute cap. A fair ticket lock lets small scopes go ahead, as a fair scheduler does.
  Done when: with a full check holding the lock, an `--affected` run finishes without waiting, and both logs show the lock order.

- **Expire edit leases like apoptosis: die when the heartbeat stops** — FIX — value 5 — effort S — risk low — category: edit leases
  Why: the user reported that a run's leases outlive it and block the next run on the same code for 20 minutes. Cells die when their survival signal stops.
  Done when: killing a run mid-edit lets the next run on that code take the lease within one heartbeat interval, and a test asserts it.

- **Trim the rules file with a linker: drop unused rules before the budget check** — FIX — value 4 — effort S — risk low — category: rules budget
  Why: the rules file is 6,416 chars against a 6,400 budget, over since T-1520. Dead-code elimination removes what never fires.
  Done when: `fm doctor` reports the rules file under 6,400 chars, and every rule that fired in the last 30 days still fires in the fixtures.

- **Route playbooks with a bloom filter and a cost-based planner** — PERFORMANCE — value 5 — effort M — risk med — category: playbook routing
  Why: the user wants 10,000+ playbooks routed fast and accurately. Databases skip scans with bloom filters and pick the cheapest index from statistics.
  Done when: on 10k synthetic playbooks, route p95 stays at or under today's, and the top 3 match a brute-force scan on the test set.

- **Memoize `fm check --affected` by content hash, like a build cache** — PERFORMANCE — value 5 — effort M — risk low — category: check cache
  Why: ccache and Bazel skip work whose input hash is unchanged. The affected run re-runs gates whose inputs did not change.
  Done when: a second `fm check` with no input changes runs zero gate commands and reports a cache hit for each gate.

- **Stream skills in like a game world, by proximity to the file being edited** — PERFORMANCE — value 4 — effort M — risk low — category: skill loading
  Why: 1,229 skills under `plugin/skills/`, and the user wants them "not all loaded". Games stream assets near the player.
  Done when: a session editing one area loads no more than a fixed skill count, and `fm cost` shows the drop from baseline.

- **Recover a crashed run by replaying its journal as a write-ahead log** — FEATURE — value 4 — effort M — risk med — category: recovery
  Why: `fm code why` already reads the journal. Databases recover by replaying the WAL, not by restarting.
  Done when: `kill -9` during a run, then `fm code resume` continues from the last journal record without repeating a completed step.

- **Gate the hook bench on a confidence bound, not one noisy p95** — FIX — value 3 — effort S — risk low — category: bench stability
  Why: PreToolUse p95 measured 310 ms against a 300 ms budget, yet it was 272 ms on a quiet machine. Markets report intervals, not points.
  Done when: `bench_hooks` fails only when the lower 95% bound of p95 exceeds 300 ms.

- **Race your last run as a ghost, split by split** — FEATURE — value 3 — effort S — risk low — category: run feedback
  Why: wild: speedrun ghosts for runs. Assumption: `fm code` already journals per-stage timings.
  Done when: `fm code why` on a finished run prints per-stage deltas against the best prior run of the same kind.

- **Auction the weekly usage budget across lanes by expected value** — FEATURE — value 3 — effort L — risk med — category: budget allocation
  Why: wild: lanes and fleets compete for one usage limit, and markets clear scarce capacity by price. Assumption: each lane's expected value can be estimated from past duel results.
  Done when: a simulated week of lane requests allocates the budget to the highest-value runs and never exceeds the cap.

- **Schedule unbounded work to the usage-reset cycle, as organisms time costly work to the day** — FEATURE — value 3 — effort M — risk low — category: scheduling
  Why: wild: `fm task defer --until` already waits for the 02:00 reset. Extending that to any queued work that has no deadline spends the full allowance once it refreshes.
  Done when: a run queued with no deadline starts within the first hour after the weekly reset whenever budget is full.

- **Share playbook fragments across projects by provenance, like gene transfer** — FEATURE — value 3 — effort L — risk high — category: playbook sharing
  Why: wild: assumption: playbooks recur across repos. An imported fragment carries its source and the test that proved it, and the receiving project must pass its own check before use.
  Done when: an imported fragment is refused until the receiving project's check passes, and its source is recorded in the fragment.
