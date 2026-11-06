# Brainstorm — lens: steal from other fields (compilers, databases, games, biology, markets)

- **Break gate-lock deadlocks with a wait-for graph** — FIX — value 4 — effort S — risk low — category: concurrency
  Why: the gate lock already waits up to 15 minutes, and a hung check in another project held it for over 40. Databases find deadlocks by building a wait-for graph and aborting the youngest holder. Foreman can record which run holds the lock and which run waits on it, then break a cycle or a stale holder with a stated reason.
  Done when: two simulated runs that wait on each other are detected within one poll, and exactly one is aborted with a message naming both.

- **Order gate steps by a query planner's cost and failure odds** — PERFORMANCE — value 4 — effort M — risk low — category: check ordering
  Why: a full `fm check` runs every step even when the cheapest step often fails first. A query planner orders work by cost and selectivity. Foreman can keep a per-step cost and failure rate in the journal and run the cheap, likely-to-fail steps first.
  Done when: on the fixture repo with a seeded failure, the failing step runs first and the total time is at least 30% lower than the fixed order.

- **Start an expensive check only when a quorum of lanes is ready** — PERFORMANCE — value 3 — effort M — risk med — category: lane coordination
  Why: the `--affected` and `--evidence` runs each queue behind the others for the gate. Quorum sensing in bacteria starts a shared behaviour only after enough cells signal. Lanes can post a ready signal, and the shared expensive check starts once a set threshold is met or a timer runs out.
  Done when: with three simulated lanes, the shared check starts only after two signal ready, and starts after the timeout if they don't.

- **Explore playbooks with a bandit, not a fixed route** — FEATURE — value 4 — effort M — risk med — category: playbook routing
  Why: routing is a fixed match, so a playbook that never helps keeps getting loaded and a better one never gets tried. A multi-armed bandit (epsilon-greedy, or Thompson sampling) gives a small share of matches to alternatives and learns from pass and fail outcomes, which fits the playbook scale the user asked for.
  Done when: after 200 simulated routes with one better playbook, that playbook wins at least 80% of the final 50 routes, and exploration stays at or below 10% of routes.

- **Specialise each hook for the repo's config and recompile on change** — PERFORMANCE — value 3 — effort M — risk med — category: hook latency
  Why: the PreToolUse Bash hook's p95 sits near its 300 ms budget, and most of each call is generic branching on config that rarely changes. A JIT compiles a hot path for the current config and falls back to the generic path on any change.
  Done when: the specialised hook returns the same decisions as the generic one on the full guard test suite, and the p95 median over 20 bench runs drops by at least 25%.

- **Place lanes on machines by consistent hashing** — FEATURE — value 2 — effort L — risk med — category: fleet
  Why: the lanes plan already contemplates several machines, and a naive modulo placement reshuffles every lane when one box drops. Consistent hashing moves only the lanes that lived on the lost box.
  Done when: removing one of five simulated machines moves at most about 20% of 200 lanes, and every other lane keeps its machine.

- **Read backlog state from versioned snapshots, as MVCC does** — PERFORMANCE — value 3 — effort M — risk low — category: state reads
  Why: `fm status` and the pane read state files that writers also touch, so a reader can wait on a write. Multi-version concurrency control lets readers take the last committed version and never block, and writers publish a new version atomically.
  Done when: with a writer holding a state file for 5 seconds in a test, `fm status` returns in under 100 ms and shows the last committed version.

- **Speculate the next queued task in a shadow worktree, and keep it only if the guess holds** — FEATURE — value 3 — effort M — risk med — category: speculation — wild
  Why: assumption: CPUs run predicted branches and throw them away on a miss. While a task runs, Foreman can start the likely next task in a throwaway worktree, then commit that work only if the next task's inputs match the guess.
  Done when: when the predicted inputs match, the next task's proof completes with no added wall time, and when they don't, the shadow worktree is removed and the queue shows no residue.

- **Trade each task's odds on a board as a price** — FEATURE — value 2 — effort S — risk low — category: planning — wild
  Why: assumption: the user asks for many ideas and wants to see which ones land. A prediction market prices each queued task by its chance of passing the gate, updated as evidence comes in, so the user can see the likeliest wins and the riskiest bets at a glance.
  Done when: each queued task shows a price between 0 and 1 that moves after a gate pass or fail, and the order of tasks by price matches their actual pass rate across 50 simulated closes.

- **Give each lane a token bucket that refills at the reset rate** — FEATURE — value 3 — effort S — risk low — category: usage control
  Why: the usage governor is a single threshold, so one busy lane can spend the whole weekly allowance before the others run. A token bucket per lane caps bursts and refills at a rate that adds up to the weekly budget.
  Done when: in a simulated week with two lanes, a lane that tries to spend more than its share is delayed, and the total spend across lanes stays at or below the weekly budget.

- **Prove a gate passed without sharing the code** — SECURITY — value 2 — effort L — risk high — category: verification — wild
  Why: assumption: a teammate or a reviewer may need to trust a pass without seeing the diff. A zero-knowledge proof, or a commitment to the test output, lets the proof be checked against the diff's hash while the code stays local. A full zero-knowledge system is heavy, so start with a signed commitment to the gate's output and the diff hash.
  Done when: a verifier with only the commitment and the diff hash confirms a pass, and a changed diff fails the same verifier.

- **Charge each lane a decay on idle context, like a cell's metabolism** — FEATURE — value 2 — effort M — risk low — category: context hygiene — wild
  Why: assumption: idle lanes keep their full context and cost tokens every reply. Context that no step has read for a while can decay out of the active window and be reloaded on demand, so a busy lane keeps its working set and an idle one sheds it.
  Done when: a lane idle for 30 simulated minutes drops at least half its context, and its next reply reloads the needed files with the proof unchanged.
