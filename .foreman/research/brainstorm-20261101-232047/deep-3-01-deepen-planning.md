# Brainstorm — lens: deepen: planning

- **Make the plan a single object with a falsifier** — FEATURE — value 5 — effort M — risk med — category: planning
  Why: the category already holds "plan lint", "one sentence plus a falsifier" and "derive depth from one number"; combined they become one stored record: readings, chosen approach, stated percent, and one observable check that would prove the plan wrong. `fm task finish` replays the falsifier. Assumption: plans are free text today, so nothing can replay them.
  Done when: a task whose plan lacks a runnable falsifier is refused at the plan gate, and finish runs it and prints held or refuted.

- **Pre-register the plan's risk tier from blast radius** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: the request says to scale depth to risk and the pack says `fm graph blast` exists. Today depth is a floor (raise-the-floor idea); it should come from measured blast plus task kind, so an S task pays S. Assumption: blast output is machine-readable.
  Done when: `fm plan` for a one-file S task asks for 1 reading and 2 approaches, and for a 30-file change asks for 3 and 4, with the tier and its reason printed.

- **Carry rejected approaches across tasks as a ledger** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: "remember rejected approaches" plus the user's dropped items (e.g. the guard-only arm that was already built and the fifth BEYOND row) show approaches get re-proposed. Key the ledger by file or area and show it when a new plan touches the same place.
  Done when: planning on a file that a closed task rejected an approach for prints that approach and the reason, and re-choosing it needs a stated difference.

- **Ground-check every idea before the plan accepts it** — FEATURE — value 5 — effort M — risk low — category: planning
  Why: the Missions 3 and 4 lesson says most ideas were already built. The plan gate should grep MASTER.md, plugin/lib and the ledger for each named capability and attach "built at path:line" or "no hit" to every approach.
  Done when: a plan proposing an existing verb is flagged with its file path before any edit.

- **Run the blind rival planner only when the first plan is confident and cheap to be wrong about** — FEATURE — value 3 — effort M — risk med — category: planning
  Why: a rival plan on every task costs L-sized effort on S tasks. Trigger it from the stated percent compared against the base rate (already built) when the gap is 20 points or more, and show only the disagreement.
  Done when: a plan stating 95% on a type with a 60% base rate spawns one rival and prints only the differing choices; one at 62% spawns none.

- **Test candidate designs in parallel lanes and pick by a judge file** — FEATURE — value 4 — effort L — risk med — category: planning
  Why: the capability text says "test them in parallel lanes, choose by evidence"; the idea "delete race, a race is N lanes plus a judge file" gives the shape. The judge file lists the command, the pass condition and the cost cap, so choosing is a rerunnable check, not an opinion.
  Done when: two lanes run the same judge file, and the chosen one's output is stored in the plan with the loser's failure.

- **Turn every closed miss into a plan-gate question** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: "What earlier brainstorms missed" lists 8 asks (T-2505, T-2525, T-2532…). Each carries a question a plan should have asked; the deck asks the matching ones when a new plan touches the same area. Assumption: misses can be tagged by area from their task diff.
  Done when: a plan touching hook-event code shows the T-2532 question and requires an answer line.

- **Make plans safe for unattended runs** — FIX — value 4 — effort M — risk med — category: planning
  Why: a left question asks which steers assume a session is present. A plan with an "ask the user" step stalls overnight. Plans must mark each step autonomous or human-only, and unattended lanes pick the autonomous branch and record the costly decision.
  Done when: an unattended drive meeting a plan with a human-only step parks that step, runs the rest, and lists it in the morning report.

- **Score plans against outcomes, not just bets** — FEATURE — value 3 — effort M — risk low — category: planning
  Why: bets are scored by Brier, but the plan's quality (did the chosen approach survive, or did the rejected one end up built later?) isn't. Record "regretted choice" when a later task reverses it.
  Done when: `fm outcomes` prints a regret rate per plan depth tier.

- **Wild: Pre-mortem child that has already seen the failure** — FEATURE — value 4 — effort M — risk low — category: planning, wild
  Why: a tool-less child is told the task failed in review and writes the three most likely causes, from the plan alone. Cheap and independent of Foreman's code, which matches the steer on signals Foreman didn't author. Assumption: a Haiku child is enough.
  Done when: each L plan carries three child-written causes, and at least one is addressed by a plan step or marked accepted.

- **Wild: A plan that predicts its own diff size** — FEATURE — value 3 — effort S — risk low — category: planning, wild
  Why: the plan states files and lines it expects to touch; finish compares them. A big overshoot means the plan missed something, which is a cheap signal that needs no model.
  Done when: finish prints predicted versus actual files, and a 3x overshoot reopens the plan step.

- **Wild: Replay old plans as a planner exam** — FEATURE — value 4 — effort L — risk med — category: planning, wild
  Why: closed tasks hold request, plan and outcome. A tool-less child plans from the request only, and the result is compared with what actually worked. This gives exhaustive thinking a held-out score from signals Foreman didn't author. Assumption: enough closed tasks have clear outcomes.
  Done when: `fm exam` reports planner agreement on 20 replayed tasks, split by task kind.

- **Wild: Morning plan diff for the returning user** — FEATURE — value 3 — effort M — risk low — category: planning, wild
  Why: a left question asks what the user sees after a week away. One page shows each plan decision made unattended, the alternative rejected, and a one-line undo.
  Done when: the web UI page lists every unattended costly decision with a working undo command.

Next question: Which plan-gate checks have never once blocked a plan that later failed, so they could fold into the plan lint without a loss?
Next question: Does any plan field get read by something other than the plan gate (finish, status, the exam), and if not, who would notice if it were nonsense?
