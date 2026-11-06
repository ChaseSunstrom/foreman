# Brainstorm — lens: measured self-evolution with fm bench

- **Bench the rules: ablate each Foreman rule/gate/playbook against fm bench** — FEATURE — value 5 — effort M — risk low — category: self-evolution
  Why: fm bench has 8 cases and A/B compare (pass rate, cost, turns), but nothing uses it to *remove* things. Prior ideas ("prove skills earn their load", "gate cost-per-catch") are unbuilt. `fm bench ablate` would run the suite with one rule block, skill or gate disabled per variant in the temp worktree and report lift or cost delta.
  Done when: `fm bench ablate --item <rule-id>` outputs paired pass/cost/turn deltas versus baseline for at least 2 items, and the report marks an item "no measurable lift" only when the delta is within the measured noise floor.

- **Measure bench noise with repeats and a variance floor** — FEATURE — value 5 — effort S — risk low — category: bench rigor
  Why: the pack says evals are "single runs, noisy"; a live replay was $0.16 for 1 case. Without a noise floor every A/B verdict is a coin flip. `fm bench run --repeat K` stores per-case pass rates, computes a floor from baseline-vs-baseline runs, and `compare` refuses to call a winner inside it.
  Done when: `fm bench compare` on two identical candidates reports "no difference" and prints the floor it used.

- **Auto-grow bench from every finished task, with a held-out split** — FEATURE — value 4 — effort M — risk med — category: bench coverage
  Why: 8 cases come from history; new tasks arrive constantly. At `fm task finish`, a commit with hidden-testable change is queued as a candidate case, and ~25% are marked held-out so the improve loop never sees them (guards against overfitting self-improvement).
  Done when: finishing a task with tests adds a case record, and `/foreman:improve` output shows held-out pass rate separately from the tuning pass rate.

- **Add a promotion gate: no self-change ships without bench non-regression** — SECURITY — value 4 — effort M — risk med — category: self-evolution
  Why: the improve loop is eval-gated by 5 noisy cases. Make `fm bench gate` the only path to merging a plugin-side candidate: held-out non-regression, cost not up beyond a threshold, guard replay unchanged, and a recorded reversible changelog entry.
  Done when: a candidate that lowers held-out pass rate in a fixture run is refused with the failing case named; a neutral one is accepted.

- **Mine bench failures into targeted rule candidates** — FEATURE — value 4 — effort M — risk low — category: self-evolution
  Why: assumption: failed replays carry transcripts. A recon pass reads only failing-case transcripts plus the diff against the passing candidate and proposes one change per failure cluster, each re-benched on those cases first, then on the full set. This closes the loop from measurement to hypothesis rather than from friction digests alone.
  Done when: `fm bench diagnose` emits at least one candidate change tied to named case ids and its re-run result on them.

- **Bench the models and tiers: pick cheapest model per task type from data** — PERFORMANCE — value 4 — effort M — risk low — category: cost routing
  Why: the user is usage-sensitive, and the delegation policy fixes models (Sonnet, Haiku) by guess. Run the cases under haiku/sonnet/opus variants and store pass-rate per cost by task type; `fm next` and the delegation advice read that table.
  Done when: `fm bench models` prints a per-type table with pass rate and cost, and a routing hint cites it.

- **Wild: Run a nightly bench "tournament" of rule-set variants that spends leftover weekly quota** — FEATURE — value 4 — effort L — risk med — category: autonomous evolution
  Why: wild. Combine the economy-mode usage reading with bench: when the weekly budget would otherwise expire unused, run queued candidate variants (from diagnose/ablate), keep the Pareto front of pass vs cost, and leave a morning card with one yes/no to adopt.
  Done when: with fake usage data showing headroom, a run executes a bounded number of variants and writes a ranked card; with no headroom it does nothing.

- **Wild: Synthesize adversarial bench cases from the user's pushback** — FEATURE — value 4 — effort L — risk med — category: bench coverage
  Why: wild. Each user correction ("don't hand me commands", "quiet output") becomes a behavior case: a scripted request where the transcript is checked by a mechanical predicate (no command handed to user, output length under N). Pass rate on these is the "does Foreman act like this user wants" metric nothing measures today.
  Done when: at least 3 correction-derived cases exist, and a deliberately violating rule variant fails at least one.

- **Wild: Race two competing candidate fixes on bench and keep the winner automatically for low-risk categories** — FEATURE — value 3 — effort L — risk high — category: autonomous evolution
  Why: wild. For friction clusters, spawn two candidate patches in separate worktrees, bench both on related cases plus a regression slice, and auto-merge only text-only changes (rules, playbooks, hints) that win beyond the noise floor; code changes still need a yes.
  Done when: a fixture friction cluster yields two candidates, a recorded winner and a reversible commit, with code changes left unmerged.

- **Track the bench scoreboard over time and alarm on drift** — FEATURE — value 3 — effort S — risk low — category: self-evolution
  Why: the pack's "scoreboard that proves it's improving" idea has no store. Append each bench run (version, pass, cost, turns) to a series; the session-start line flags a drop beyond the noise floor after any Foreman or Claude Code model change.
  Done when: two runs on different versions yield a trend line in `fm bench history`, and a simulated 2-case regression triggers the alarm.

- **Bench plugin interop: replay cases with each third-party plugin enabled** — FEATURE — value 4 — effort M — risk low — category: plugin compat
  Why: the user asks for better plugin compat; conflicts are a hard-coded dict. Run the suite with plugin X enabled versus not and record pass/cost/turn deltas, replacing guessed KNOWN_CONFLICTS with measured ones.
  Done when: `fm plugins check --measure X` reports a delta against baseline and `fm plugins check` cites it in place of the static note for that plugin.
