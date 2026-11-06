# Brainstorm — lens: bold bets

- **Make the usage governor pick model and context per task** — FEATURE — value 5 — effort M — risk med — category: usage budget
  Why: The user asked Foreman to notice its own burn ("foreman should've figured it out itself"). T-1796 moved builders to Sonnet and compacts at 200k by hand. Assumption: fmbudget can read the weekly remaining and feed the choice.
  Done when: With a simulated 20% weekly budget, `fm run` on a 10-task queue picks Sonnet and compacts at 200k, and each choice is logged with its reason.

- **Route a 20,000-playbook library without loading it** — FEATURE — value 5 — effort L — risk med — category: playbook scale
  Why: The user wants tens of thousands of playbooks, all routed, none loaded. Assumption: routing currently reads every entry.
  Done when: `fm playbooks route` resolves a generated 20,000-entry fixture in under 200 ms, keeps fewer than 50 entries in memory, and gets the correct top hit on 100 held-out queries.

- **Replay the safety corpus on every Claude Code release** — SECURITY — value 4 — effort M — risk low — category: release safety
  Why: T-1268 is blocked. The guard hook stops bypass-mode commands, and a harness change can break it without warning.
  Done when: A pinned guard corpus runs under each new CLI version in CI, and any failing case blocks the release tag.

- **Run Foreman's loop on any model or CLI** — FEATURE — value 5 — effort L — risk high — category: model portability
  Why: T-1207 is blocked. Assumption: the codex, gemini and opencode adapters show the loop can run off Claude Code.
  Done when: `fm code` finishes a one-task queue (plan, edit, `fm task prove`, close) on a non-Claude runner, and the transcript shows the same stage rail.

- **Resume a dead run from its journal and free its leases** — FIX — value 5 — effort M — risk med — category: recovery
  Why: The user reports that a model run's edit leases outlive it, so the next run on the same code is refused for 20 minutes. T-0798 covers recovery.
  Done when: Killing a run mid-edit and running `fm code resume` completes with no 20-minute refusal, and the lease is released.

- **Lanes that fork from a planner and report to a registry** — FEATURE — value 4 — effort L — risk med — category: parallel agents
  Why: T-0792 is deferred. The user wants all ideas run at full force, so parallel lanes are the lever.
  Done when: Three tasks run in separate lanes at once, each closes with its own prove receipt, and ListAgents shows all three with their state.

- **Stop gate-lock waits between projects** — PERFORMANCE — value 4 — effort M — risk low — category: gate contention
  Why: `fm check --affected` waits behind other builders' runs. A hung check in another project held the lock for over 40 minutes.
  Done when: Two builders in different projects run `fm check --affected` at once, and neither waits more than 5 s.

- **Wild: a nightly brainstorm that argues with its last round and retires its own ideas** — FEATURE — value 3 — effort M — risk low — category: recursive ideation
  Why: wild. The user asked for a recursive brainstorm that builds on the finished product each round (T-1331). Assumption: prior rounds are stored in the brainstorm clusters.
  Done when: Round N+1 retires at least one round-N idea with a stated reason, and its receipt cites the prior round's id.

- **Wild: a public duel scoreboard, Foreman against bare Claude Code** — FEATURE — value 4 — effort L — risk med — category: public benchmark
  Why: wild. T-1231 and T-0866 want duel data, and the site already publishes. Assumption: the case corpus can be shared.
  Done when: One command generates a page listing cases, pass rate, cost and time for both arms, with raw run logs linked.

- **Enforce a budget on every always-loaded file, with a trim proposal** — CLEAN — value 3 — effort S — risk low — category: context budget
  Why: The rules file is 6,416 characters against a 6,400 budget, and the user asked for it to be trimmed back under.
  Done when: A check fails any always-loaded file over budget and proposes a diff, and the current rules file passes.

- **Wild: mutate the fix and require the test to go red** — FEATURE — value 3 — effort M — risk low — category: proof strength
  Why: wild. `fm task prove` already shows a test failing without the change. Assumption: reverting single lines is a cheap next step.
  Done when: A fix whose test still passes when one line of the fix is reverted is rejected, and the rejection names the surviving mutant.

- **Wild: a headless renderer that judges UI diffs against the spec** — FEATURE — value 3 — effort L — risk med — category: UI verification
  Why: wild. The user asked for a headless-rendering probe in `fm doctor`. T-0797 covers verification through native tools.
  Done when: `fm doctor` reports headless rendering as available or gives the reason it isn't, and a UI task fails when its screenshot diff exceeds the threshold.

- **Run overnight lanes as cloud routines with a morning receipt** — FEATURE — value 3 — effort L — risk high — category: unattended work
  Why: T-0793 is deferred. The user is often away, so unattended work is the point.
  Done when: A queued task runs as a remote routine with no local process, and the next session reads a receipt naming the commit and the prove result.
