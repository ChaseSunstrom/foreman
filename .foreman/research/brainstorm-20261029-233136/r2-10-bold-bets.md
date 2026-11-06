# Brainstorm — lens: bold bets

- **Run Genesis as a speciation tournament** — FEATURE — value 5 — effort L — risk med — category: selection
  Why: gen-0 selection is a single parent-vs-rewrite comparison; assumption: a population of 3–4 divergent Seeds per generation (each from a different lens mix) escapes local optima that one lineage can't. Existing `fm lane race` and `fm exam run` already score branches.
  Done when: on a fixture project, `fm genesis gen --population 4` runs four lineages in worktrees, records all four scores in lineage.md, and promotes the winner while the losers' verdicts stay readable.

- **Generate the project's capability spec from its competitors** — FEATURE — value 5 — effort L — risk med — category: spec
  Why: the pack's "complete and best-in-class for this kind of project" needs an external yardstick; the capability-map lens exists in `fm ideas` but isn't tied to a spec. Assumption: a tool-less child can name the field's top tools from its own knowledge.
  Done when: `fm genesis spec` on a fixture CLI project writes a spec with ≥20 capabilities, each tagged with the reference tool it came from and mapped to at least one exam scenario, and the held-out third is excluded from the writer's input.

- **Write gen-0 by interviewing the user's own history** — FEATURE — value 5 — effort M — risk med — category: gen-0 writer
  Why: the user's steers ("genuinely smarter, not hardcoded") say gen-0 should be learned, not templated. Mining steers, drops and asks across sessions yields MUSTs and NEVERs with provenance.
  Done when: with no argument, `fm genesis init` on a project with ≥10 recorded steers drafts a gen-0 where every MUST/NEVER cites the steer or drop it came from, and a fixture with no history yields an explicit "no evidence" gen-0, not invented rules.

- **Close the loop on planted gaps with a mutation-score exam** — FEATURE — value 4 — effort M — risk low — category: exam
  Why: the Mission 2 exam says the tower "closes the planted gaps"; assumption: gaps planted by mutating the repo (delete a test, stub a feature, drop a doc section) give an objective, regenerable key that doesn't depend on model-authored scenarios.
  Done when: `fm exam gen --mutate` plants N gaps in a copy, and `fm exam grade` reports how many the tower restored, with an oracle arm scoring 100% and an empty arm 0%.

- **Make Genesis a standing background tenant with a nightly shift** — FEATURE — value 4 — effort M — risk high — category: autonomy
  Why: the request says it "starts on its own when the queue runs dry"; the routing line is protected core, so the nightly shift must be a candidate plus the user's yes. Assumption: a per-project shift window and spend cap make this safe.
  Done when: after the user approves once, an idle project starts one capped generation in its window, stops at the cap, and leaves a one-screen digest; with no approval, nothing runs.

- **Auto-grade each generation with a cold, tool-less reviewer** — FEATURE — value 4 — effort S — risk low — category: judge
  Why: standing steer says weakness-finding comes from outside signals only. A tool-less child that sees only the diff and the spec, never the author's notes, is the cheapest outside signal.
  Done when: every generation's lineage entry holds a cold-review verdict with the reviewer's input hash, and a rewrite can't win with a "reject" verdict.

- **Reuse towers as installable genomes** — FEATURE — value 4 — effort M — risk med — category: carry-over
  Why: carry-over is listed as missing; assumption: winning Seeds, missions, lens weights and the not-yet ledger are small, text-only and portable between similar projects.
  Done when: `fm genesis export-genome` writes a ≤50 KB file with no project paths or secrets, and `fm genesis init --from genome` on a second fixture starts with those defaults marked "probation" until they win once there.

- **Retry the not-yet ledger with a different brain each time** — FEATURE — value 4 — effort M — risk low — category: ledger
  Why: the steer says a failed spike gets ≥2 different approaches before being parked. Assumption: re-running the same model with the same prompt wastes the retry.
  Done when: each ledger entry records the approach and model used per attempt, and `fm genesis retry` refuses to repeat an identical (approach, model) pair.

- **Wild: Genesis writes its own bug reports upstream as exam scenarios** — FEATURE — value 4 — effort M — risk low — category: feedback
  Why: assumption: each time Foreman itself stumbles during a tower (a hook false-positive, a stuck lane), that failure is the best planted gap for Foreman's own exam. wild
  Done when: a failure during a fixture tower run auto-creates a Foreman-repo task and an exam scenario that reproduces it, with no user action.

- **Wild: The tower plays chess with plain Claude Code** — FEATURE — value 4 — effort L — risk med — category: benchmark
  Why: the pack has Foreman-vs-plain arms in `fm exam`; assumption: running them as a live head-to-head with a moving Elo per project makes progress legible and honest. wild
  Done when: each generation appends an Elo-style rating of Foreman vs the plain arm on held-out scenarios, shown on the Genesis page, and a decline flags a regression.

- **Wild: Genesis dreams a "year ahead" roadmap and backtests it** — FEATURE — value 3 — effort L — risk med — category: foresight
  Why: assumption: replaying the project's git history, asking the tower what it would have proposed at month N, and scoring that against what actually shipped tells you whether its judgment is any good before you trust it with autonomy. wild
  Done when: `fm genesis backtest` over a fixture repo's history outputs a hit rate of proposed vs actually-shipped work, and auto-start stays off until the rate clears a user-set bar.

- **Gate autonomy on earned trust** — FEATURE — value 4 — effort M — risk low — category: trust
  Why: the user wants auto-start but the risks are overfitting, drift and self-grants. Assumption: a per-project trust level (observe → propose → run capped → run) that rises only on backtest and held-out results is safer than a boolean.
  Done when: a fresh project starts at observe, moves up one level only after meeting its recorded threshold, and any drift-check failure drops it a level.

- **Wild: Hand the tower a mystery repo and rank its first ten minutes** — FEATURE — value 3 — effort M — risk low — category: cold-start
  Why: assumption: a nightly "stranger roulette" that runs Genesis on a random open-source repo in a sandbox, grading its gen-0 against that project's actual README and CONTRIBUTING, catches cold-start regressions before a real user does. wild
  Done when: the roulette runs on three pinned fixture repos, scores each gen-0 for MUST/NEVER coverage against the human-written docs, and fails the Foreman gate if the average drops.

Next question: What does the user do with a tower once it exists, such as read it, edit gen-0, or veto a mission, and which of those moments needs a one-keystroke control rather than a file edit?
Next question: Which Genesis outputs would the user publish on the site versus keep private, and does a project's own tower ever need to stay off the Genesis page?
