# Brainstorm — lens: unspoken needs

- **Answer "what did I just ask for?" in one line at goal open** — FEATURE — value 4 — effort S — risk low — category: intake
  Why: The user's asks are long, dense and multi-clause (T-2173, the steer #3–#7 batch). Their repeated need is that the restated goal match what they meant, and several puts deadlocked on misreadings (T-2213 read only the first line of a wrapped Task paragraph). Assumption: they'd veto a wrong restatement faster than they'd notice a wrong plan.
  Done when: `fm goal open` prints a ≤25-word restatement plus the clause count it parsed, and a test with a wrapped multi-clause ask shows the count equals the clause count in the source.

- **Count the clauses of every ask and fail the plan if one has no row** — FIX — value 5 — effort M — risk low — category: coverage
  Why: T-2213 (wrapped paragraph read as its first line, so 4 of 8 briefs went unintaken) is a silent clause loss. The user had to notice it. Assumption: the same loss happens for any long ask, not only the Genesis Mission blocks.
  Done when: a fixture ask with 7 clauses yields a plan where `fm goal check` lists 7 clause-to-row links, and deleting one row makes the check exit non-zero.

- **Make every checker's own failure visible as a result, not a skip** — FIX — value 4 — effort M — risk low — category: reliability
  Why: T-2219 (a scorecard comparing 30/36 with a 1-scenario line shown as 1/36) and T-2228/T-2229 (stray quotes silently deadlocking puts) are the checker misleading the user. They had to find these themselves. Assumption: other comparisons share the unequal-denominator shape.
  Done when: any scorecard line whose two sides have different denominators prints both denominators and is flagged "not comparable"; a test pins it.

- **Warn when a goal's plan is longer than the baton can carry** — FEATURE — value 3 — effort S — risk low — category: resume
  Why: the open question about the largest absorbable baton is unanswered, and the user's goals keep growing (8-brief Missions). Assumption: a fresh session fails quietly on oversized batons.
  Done when: `fm goal card` reports its byte size against a setting and says which rows were shed, and a test with an oversized goal shows the shed order.

- **Tell me what changed while I was away, in the order I care about** — FEATURE — value 4 — effort M — risk low — category: resume
  Why: the user drives by long steers over days, then returns. Their words show them asking for outcomes (shipped to main, live site, exit 0), not process. Assumption: a return digest led by shipped/blocked/needs-your-yes beats a task list.
  Done when: `fm goal since` prints three headed sections (shipped, blocked on you, still running) from the ledger, and each blocked line names the one command that unblocks it.

- **Turn each steer into a standing rule with its check, automatically offered** — FEATURE — value 5 — effort M — risk med — category: steers
  Why: the user asked for exactly this (`fm decide --check` for a steer-cited rule), so they are tired of restating things. Assumption: they would accept an offer ("save this as a rule with this check?") more readily than writing the command.
  Done when: after a steer containing "never/always/must" the next prompt shows a proposed `fm decide --check` line, and accepting it makes `fm doctor` fail once the rule is violated.

- **Show the exam's number and the claim beside each other wherever one is quoted** — FIX — value 3 — effort S — risk low — category: honesty
  Why: the finding that a Foreman session found 6/18 while `fm find` alone found 16/18 shows the user wants uncomfortable numbers surfaced beside the README's claims. Assumption: README and site claims drift from exam results.
  Done when: a docs check fails when a quantitative claim in README, MASTER or the site has no linked exam or bench result.

- **Wild: Let the goal talk back with a "you probably also want…" note after the plan, drawn from your own past steers** — FEATURE — value 4 — effort M — risk med — category: foresight
  Why: wild. The steers come in series (#3, #4, #5, #6, #7 arrived together, each one adding something the first plan lacked). Assumption: the next steer is predictable from the earlier ones' shape (more detection, more surfaces, more harness-neutrality).
  Done when: planning a goal prints up to 3 labelled "from your past steers" suggestions, each citing the steer it came from, and the user can drop one with a single flag.

- **Wild: Make the tower grade its own ambition, so a generation that only polishes is called out** — FEATURE — value 3 — effort M — risk low — category: genesis
  Why: wild. The user added the moonshot Mission and the rule that the frame may grow, never shrink. They fear a tower that settles into upkeep. Assumption: a generation's Missions can be bucketed new-capability versus upkeep.
  Done when: `fm genesis check` prints the share of Missions that add a capability and fails when it's under a configured floor from gen 2.

- **Wild: A "second reader" that re-reads each of the user's steers a day later and asks whether it was carried out as meant** — FEATURE — value 4 — effort M — risk med — category: fidelity
  Why: wild. Many "asked" lines are corrections of work that met the letter and missed the intent (T-2173, T-2202). Assumption: a cold read of steer-versus-result catches some before the user does.
  Done when: a day after a steer, a cold reader emits one line per steer, "met / partly / missed", with a quote from the result, and a test plants a missed steer that it flags.

- **Wild: Keep a "things you asked me to stop doing" list that every new hook is tested against** — FEATURE — value 3 — effort S — risk low — category: restraint
  Why: wild. The 1,500-character note-average friction check (T-2109) and the hook byte budget show that overhead is a standing worry. Assumption: new features erode earlier restraint asks.
  Done when: a gate fails when a new hook's injected bytes push the per-turn total past the budget recorded from the user's steer.

- **Name the next harness that will matter before the user does** — FEATURE — value 3 — effort M — risk low — category: portability
  Why: T-2173 and the no-claude-binary end-to-end ask show the user moving from "for Claude Code" to harness-neutral. Open items T-0335, T-0336 and T-0337 stay blocked on live verification. Assumption: they'll want the same proof for every harness they name next.
  Done when: a conformance table lists each supported harness against hook, drive, grant and goal-card capabilities, with each cell marked verified-live, stubbed, or unsupported, and CI fails on a cell with no mark.

- **Explain every refusal in the user's vocabulary, with the one unblocking command** — FIX — value 3 — effort S — risk low — category: legibility
  Why: several drops resolved to messages that did not say what was wrong or what to run (T-2095, T-2104, and the "no gates configured" row). Assumption: other refusals are equally terse.
  Done when: every non-zero exit from `fm goal`, `fm genesis` and `fm exam` prints a reason line and a "run:" line, and a test enumerates the exit paths and asserts both.

Next question: Which of the user's steers have no automatic check yet, and how many have been silently undone since they were given?
Next question: When a user asks for something already half-built in an earlier generation, does anything tell them before the plan is written?
