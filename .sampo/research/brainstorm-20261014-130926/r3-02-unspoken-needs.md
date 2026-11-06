# Brainstorm — lens: unspoken needs

- **Fail safe when the project map is stale** — FIX — value 4 — effort S — risk low — category: gates
  Why: the pack's map says "350 files, as of an older HEAD", and round 1 made `fm check --affected` the builders' default. If the test→src links are older than HEAD, `--affected` can silently pick too few tests. The "record misses and widen" idea only reacts after a miss.
  Done when: with the map stamped older than HEAD, `fm check --affected` refreshes it (or runs the full suite) and prints one line saying which. A test fixture proves a new file's test is selected.

- **Put the user's vetoes into every agent and lane brief** — FEATURE — value 4 — effort S — risk low — category: agents
  Why: round 1 gave agents `omitClaudeMd` and per-tier effort, so children may no longer see the standing rules. This user's recurring steers ("measured first", "don't build what CC already does", "by design") are exactly what a child without CLAUDE.md would break. Assumption: the agents really do omit the project's rules.
  Done when: a builder or reviewer brief contains a capped digest of at most 300 tokens of active vetoes and by-design entries. A test shows a child brief for a dropped idea cites the drop.

- **Retune `maxTurns` and effort from observed turn use** — FEATURE — value 3 — effort S — risk low — category: agents
  Why: round 1 set `maxTurns` and effort by judgment, with no record of whether any role hits its cap or finishes in a third of it. Assumption: stop reasons are recoverable from child transcripts.
  Done when: `fm doctor` or `fm cost` shows, per role, turns used against the cap and the hit rate. It flags any role that hit its cap in at least 25% of runs, or that used under 30% of it.

- **Continue a turn-limited agent instead of respawning it** — FEATURE — value 4 — effort M — risk med — category: agents
  Why: round 1's budget and turn caps mean children can now stop mid-work, and a respawn re-pays the whole read. This combines "typed partial result" with "re-review by continuing the same reviewer"; neither covers the case of a cap stop. Assumption: the child's session id is retained.
  Done when: a child killed at `maxTurns` in a test is resumed once with a "finish from here" note and returns a complete result. A second cap stop produces a typed partial rather than a loop.

- **Bench the whole hook chain per tool event** — PERFORMANCE — value 4 — effort S — risk low — category: hook latency
  Why: the bench judges hooks one at a time by CPU time, but a Bash call now triggers the guard, the compact PostToolUse, and the step and recording hooks in sequence. The user feels the sum, and wall time includes disk waits that CPU time hides.
  Done when: `bench_hooks.py --chain Bash` reports the summed wall time and Python spawn count for one simulated Bash call. It fails above a set budget and is wired into the existing gate.

- **Drill each round-1 feature's failure path** — FEATURE — value 5 — effort M — risk low — category: resilience
  Why: the "Known gaps" section admits the monitor's arming is unverified. Round 1 shipped five new dependencies (monitor, push, compact store, budget cap, worktree baseRef), and only their happy paths are tested. Dropped ideas show this user wants measured claims.
  Done when: `fm doctor --drill` kills the monitor, fills the output store, and trips a budget cap in a temp project. Each case must degrade with a visible one-line reason and never block a turn.

- **Compile each idea's "Done when" into a runnable verify at queue time** — FEATURE — value 4 — effort M — risk med — category: queue
  Why: round 1 refuses unrunnable verify commands at plan time, but brainstorm ideas arrive with prose checks. One earlier task had to be recreated because its check read the queue itself. Round 2 will queue about a dozen tasks.
  Done when: queueing an idea drafts a verify command, rejects one that references the queue or cannot run, and marks the task "needs a hand-written check" when no command is derivable.

- **Give each lens a filtered slice of the pack** — PERFORMANCE — value 4 — effort M — risk med — category: tokens
  Why: this pack carries thousands of prior idea titles to every lens child. The cluster-summary idea shrinks the pile, but a lens only needs its own neighbours and the counts for the rest. Assumption: a token-overlap retrieval is good enough.
  Done when: each child pack contains the nearest 40 prior ideas plus per-category counts. The pack is at least 60% smaller, and a duplicate-rate check on a sample round does not worsen.

- **Wild: Split an agent role automatically when it keeps hitting its cap** — FEATURE — value 3 — effort L — risk high — category: agents
  Why: assumption. This extends the turn telemetry above: a role that is capped in at least 30% of runs has probably been given two jobs.
  Done when: a proposed scout plus worker pair is written as a draft agent file and benchmarked against the original. It is installed only if first-pass success holds and cost per task drops.

- **Wild: Report the "pit-stop" lap time between rounds** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: the user's "recursive" loop is a repeated ritual of tidy, doctor, bench and page. Running these in parallel and printing one lap time ("round overhead 41 s, 9 s faster than last round") makes the loop's own cost something that can fall.
  Done when: one command runs those four jobs concurrently and prints a single card with each job's time and the total. The total is stored per round.

- **Wild: Echo what "etc." means, then proceed unless vetoed** — FEATURE — value 4 — effort M — risk med — category: intake
  Why: the user ends big asks with "etc. etc. etc." and wants Foreman to fill in scope without a question. A one-line echo ("reading 'etc.' as: speed, tests for round-1 failure paths, no new surfaces") that auto-proceeds after the first tool call keeps that autonomy and lets them redirect cheaply. Assumption: a silent first minute counts as consent.
  Done when: a trailing "etc." in a request produces the echo line and a recorded scope list. A reply within the window overrides it, and a test covers both paths.
