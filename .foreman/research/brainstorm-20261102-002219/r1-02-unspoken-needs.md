# Brainstorm — lens: unspoken needs

- **Re-derive "done" from the repo at every resume** — FEATURE — value 5 — effort M — risk low — category: done-detection
  Why: the capability text says "knows when it's actually done rather than merely stopped". Assumption: the done check reads stored row status, not the tree. 
  Done when: a fixture goal with one row silently reverted by a later commit reports "not done: row 3 no longer holds" at the next resume, with the failing probe shown.

- **Fill the 58 cells from a lifecycle trace, not prose** — FEATURE — value 5 — effort M — risk med — category: coverage
  Why: the standing rule says a cell counts only if it is grounded and not templated. Assumption: the stages are roughly create, decompose, order, persist, compact, crash, resume, done-check. 
  Done when: a fixture goal runs through every stage on the web UI and the CLI, and each filled cell cites a trace line (file plus event) that `fm genesis sweep` re-resolves; the empty-cell count reads 0 or names a recorded n/a.

- **Tier the finished version into must, should and stretch** — FEATURE — value 5 — effort S — risk low — category: scope
  Why: "best-in-class" plans (pillar 2) grow without limit. The user keeps pushing for "finish", so a cut line is the need behind it. Assumption: goal rows have no tier today. 
  Done when: a goal reports "finished" when all must rows are proven and every should row is done or explicitly deferred with a reason, and stretch rows never block it.

- **Flag drift between tasks and goal rows** — FEATURE — value 4 — effort M — risk low — category: plan-integrity
  Why: assumption: over days, queue items accumulate that serve no goal row, and rows go untouched. Standing steers show the user policing exactly this kind of unrequested growth. 
  Done when: `fm goal` lists orphan tasks and rows idle for N days, and a planted orphan appears in the list on a fixture.

- **Add a goal page to the web UI** — FEATURE — value 4 — effort M — risk low — category: web UI
  Why: web UI is the only surface in this mission. Assumption: goal state is only readable through CLI text. The page shows rows as proven, claimed or open, plus "why not done yet" and the next action, with empty, loading and stale states. 
  Done when: a screenshot of a half-finished fixture goal shows proven and claimed rows distinctly, with a stale banner when the data is older than the last commit.

- **Run a kill-and-resume drill for goals** — FIX — value 4 — effort M — risk med — category: reliability
  Why: the capability promises survival across crashes and compactions, and the user's long-horizon tier plants these faults. Assumption: no goal-specific drill exists. 
  Done when: a scripted run SIGKILLs the session at each plan-write boundary and resumes, and the resulting rows and order are byte-identical to an unkilled run.

- **Collect user-only items in one running list** — FEATURE — value 4 — effort S — risk low — category: unattended
  Why: pillar 7 says user-only items go in the final report, and the steer "never block on the user" means they must be gathered as the goal runs. Assumption: items are scattered across notes. 
  Done when: a goal containing a row that needs a human credential ends with that row in a `user-only` section of the report, and the run was not blocked on it.

- **Write a finish receipt that proves what changed** — FEATURE — value 3 — effort S — risk low — category: reporting
  Why: "proof before presentation" is a standing theme. Assumption: the goal end report is prose. 
  Done when: finish prints each row with its proof command, exit status and age, and fails to print "finished" if any proof is older than its inputs.

- **Check goal resume on every harness from files alone** — FEATURE — value 4 — effort M — risk med — category: harness-neutral
  Why: the standing rule is that Foreman is not Claude-specific. The prior open question was whether probes depend on Claude Code. Assumption: resume leans on hooks. 
  Done when: with no `claude` on PATH, `fm code` resumes a fixture goal at the right row using only on-disk state.

- **Review each finished goal for late-added rows** — FEATURE — value 3 — effort S — risk low — category: learning
  Why: assumption: rows added after the plan was accepted show what the planner missed, and nothing records that today. 
  Done when: finishing a goal writes a "missed at plan time" list that the next decomposition's prompt cites, shown on a fixture with one late row.

- **Wild: Run an adversary lane that tries to prove the goal isn't done** — FEATURE — value 4 — effort M — risk med — category: done-detection
  Why: wild. A cold child gets only the user's original words and the repo, and must name one requirement with no covering row. Assumption: a tool-less child can do this from a context pack. 
  Done when: on a fixture where one requested clause is uncovered, the child names it; on a fully covered fixture it abstains.

- **Wild: Write the demo script before the plan** — FEATURE — value 4 — effort M — risk med — category: planning
  Why: wild. The finished-version section starts as an executable demo of the goal working, and rows are derived backward from its steps. Assumption: this gives sharper done checks than a prose list. 
  Done when: a fixture goal's demo script fails at the start and passes only when the last must row closes.

- **Wild: Reverse-plan a finished repo and score the decomposer** — FEATURE — value 3 — effort L — risk med — category: planner quality
  Why: wild. Take a project's git history, give the decomposer only its first-commit goal, and compare the rows it plans against what was shipped. This yields a backtest in the spirit of "a heuristic ships only behind a backtest". 
  Done when: one replayed repo yields a recall/precision figure for planned rows versus shipped features, stored in the exam output.

- **Wild: Send a one-line goal status to a pocket surface** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild. The user is away for days; one line like "6/9 must rows proven, next: X, blocked on you: none" would let them check in without opening a session. Assumption: a notification path exists. 
  Done when: after a row closes, a single line is written to the configured channel and respects quiet hours.

Next question: Which of the 58 cells does a real goal lifecycle never reach on the web UI, and so should be a recorded n/a rather than a fill?
Next question: When a goal "finishes", which row did the user later reopen, and which proof would have caught it?
