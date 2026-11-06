# Brainstorm — lens: blind spots

- **Fix the brief-guard's path false positives** — FIX — value 4 — effort S — risk low — category: guard
  Why: the pack records two brief-guard false positives, a dict key and a `.join(` call read as written paths. An intact guard that cries wolf trains the user to bypass it.
  Done when: a fixture corpus containing both strings passes the guard, and a real written path in the same corpus is still blocked.

- **Offer the safe verb on every guard block** — FEATURE — value 4 — effort S — risk low — category: guard UX
  Why: `core:interpreter-code-driving-foreman` blocked 42x in 7 days. Each block is a moment where the agent needed something Foreman could have given it. This asks the question "what was it trying to do?".
  Done when: the top 5 block rules each print one runnable `fm` command, and a test asserts none of the 5 prints a bare refusal.

- **Lint that every ledger row carries its dimensions** — CLEAN — value 4 — effort M — risk low — category: data schema
  Why: T-2500 (bets by harness) was missing because rows had no harness field. The question to ask is "what will we want to split this by later?". Evidence is the T-2500 ask, which no earlier brainstorm predicted. Bets, friction, hook runs and outcomes should all be checked for harness, model, version and surface.
  Done when: `fm doctor` lists any ledger writer whose rows lack harness, model or surface, and the list is empty for the bets, friction and outcomes ledgers.

- **Shrink the SessionStart note to a delta after the first** — PERFORMANCE — value 4 — effort S — risk low — category: injected context
  Why: the pack measures a note of about 2k chars sent 89 times. Pillar #12 says to keep context small.
  Done when: a second SessionStart in the same repo within an hour emits 200 chars or fewer, and a test shows the standing rules still arrive in full (the steer says never to truncate them).

- **Attribute injected bytes to their source per reply** — FEATURE — value 4 — effort M — risk low — category: observability
  Why: context per reply averages 387k, but nothing shows which hook, skill or note contributed what. T-2503 measures lean in substance, which needs that breakdown. Assumption: most of the 387k is cache and history, so only the attributable part is under Foreman's control.
  Done when: `fm cost --by-source` prints bytes per injector, and the sum matches the hook-logged total within 5%.

- **Prove the guard fires on every surface with a deny-class matrix** — FEATURE — value 5 — effort M — risk med — category: guard coverage
  Why: the coverage cells for Codex, Gemini, opencode, `fm code` and MCP are empty for this capability. T-0335/T-0336 are blocked on live-verification, so "guard intact" is only evidenced for Claude Code. The question to ask is "intact where?".
  Done when: a table of command class × harness exists, each cell is either a passing test or an explicit "unguarded: reason", and `fm doctor` fails on a blank cell.

- **Run the unattended paths under the same guard and hook budget** — SECURITY — value 4 — effort M — risk med — category: sessionless safety
  Why: T-2499 moved bet settling into `fm night`'s tick, which has no session. The question is "what else now runs without a session, and does the guard and the lean budget reach it?". Candidates are `ci-watch`, lane children and the night tick. Assumption: their guard coverage is untested.
  Done when: a test launches a lane child and a night tick with a planted forbidden command and sees the block logged, and `fm doctor` reports the tick's p95 beside the hook p95.

- **Fuzz the ordering of task-state writes** — FIX — value 3 — effort M — risk low — category: state invariants
  Why: T-2334/T-2525 show a start-point bug that appeared only when events arrived late or out of order (git timeouts, finish before evidence). That class likely recurs for other fields.
  Done when: a randomized test permutes focus, evidence, finish and timeout events for 200 seeds, and every seed ends with a start point and a consistent status.

- **Check lean claims in public text against their producing command** — FIX — value 3 — effort S — risk low — category: proof before presentation
  Why: T-2504 covers claims generally. The lean claims (hook p95, "context small", verb counts) are the cheapest numbers to let drift, and 278 ms is in the pack as a live figure.
  Done when: the sweep goes red when a hook-speed or verb-count number in README or the site is more than 10% off `fm doctor`'s current value.

- **Archive stack cards unused for 90 days into a cold index** — CLEAN — value 3 — effort M — risk low — category: subtraction
  Why: 5 of 1219 cards are used, and gen-0 says to subtract as you add. A prior steer says unmeasured growth waits, so this is the matching subtraction. Assumption: the 1214 unused cards cost map and disk time.
  Done when: unused cards move to an archive that `fm lib show` still reads, and the map and doctor timings do not rise.

- **Wild: Plant a weekly harmless forbidden command to prove the guard is alive** — SECURITY — value 4 — effort M — risk low — category: guard liveness
  Why: wild; assumption: a guard that silently stopped working looks identical to a guard with nothing to block. A canary per harness turns "intact" into a dated fact.
  Done when: a weekly canary per harness logs "blocked at <time>", and killing the guard in a test copy makes `fm doctor` go red within one run.

- **Wild: Run the exam with every optional hook off to show what the weight earns** — PERFORMANCE — value 4 — effort L — risk med — category: lean evidence
  Why: wild; builds on the deferred Lite mode (T-0794). Lean claims need a counterfactual: pass rate and time at zero optional hooks against the full set. The long-horizon exam waits for the end of the run, so a Haiku smoke run does this first.
  Done when: one table lists each hook's removal delta in pass rate, seconds and context bytes, and a hook with no gain gets a subtraction task.

- **Wild: Show a "weight class" scale in the pane with a budget per hook event** — FEATURE — value 3 — effort M — risk low — category: delight/lean
  Why: wild; the user never sees what Foreman costs per turn. A live scale with SessionStart, prompt and tool hooks, each against its budget, makes the ratchet felt.
  Done when: the pane shows per-event ms and bytes against budget, and a budget breach turns the row visibly red.

Next question: Which of Foreman's costs does the user pay in waiting time, such as `fm check`, `finish` and ship gates, rather than in tokens or hook ms, and is any of that time growing unmeasured?

Next question: Which safety properties hold only because a human is watching the session, and what stops being true on the first fully unattended night?
