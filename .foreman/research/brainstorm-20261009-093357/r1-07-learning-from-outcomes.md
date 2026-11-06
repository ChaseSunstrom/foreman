# Brainstorm — lens: learning from outcomes

- **Score approach choices by regret** — FEATURE — value 5 — effort M — risk low — category: planning
  Why: M/L briefs already list 3+ approaches, but nothing records which one was picked, why, or whether a rejected option would have done better after a retry or block. assumption: briefs keep approaches in a parseable form.
  Done when: `fm task done` stores the chosen approach with a win/regret outcome, and `fm recall --approaches "<topic>"` shows past picks with their outcomes.

- **Calibrate stated confidence** — FEATURE — value 5 — effort M — risk low — category: calibration
  Why: briefs state assumptions "with confidence", but no one checks whether 80% assumptions hold 80% of the time. An uncalibrated number is decoration.
  Done when: `fm calibrate` prints a reliability table (stated vs. observed hit rate) over finished briefs, and intake warns when a bucket is off by more than 20 points.

- **Label every task's outcome from the user's next message** — FEATURE — value 5 — effort M — risk med — category: outcome labels
  Why: the lessons, bench and friction pipelines all need an "outcome", but today it is mostly gate-green or hand-captured steers. The user's reply after done (thanks, a correction, a re-ask, silence) is a free label. The pack shows steers and drops being recorded already. assumption: the next user prompt is reachable in the hook stream.
  Done when: each finished task gets a `reaction` field (accepted / corrected / re-asked / ignored) in the ledger, and `fm friction` groups by it.

- **Keep per-project root-cause priors for FIX work** — FEATURE — value 4 — effort M — risk low — category: debugging
  Why: fm-debugger ranks hypotheses, and `fm task hypo` records them, but the ranking starts from nothing every time. Which cause classes (stale cache, env drift, off-by-one in the hook parser…) actually won in this repo is known from closed hypotheses.
  Done when: fm-debugger's brief includes a "historical winners" prior from closed hypotheses, and a test shows the prior reorders the ranking on a seeded history.

- **Yield-rank the planning passes** — FEATURE — value 4 — effort M — risk low — category: thinking cost
  Why: planning.md has many passes, but nobody measures which ones changed a plan. A pass that never alters a plan on S/M work is cost; one that often does is worth making mandatory.
  Done when: each pass logs "changed plan: y/n", and `fm friction` lists passes with under 5% change rate per tier over the last 30 tasks, as candidates for `fm evolve --drop`.

- **Learn which brainstorm lens and round pays off** — FEATURE — value 4 — effort S — risk low — category: brainstorming
  Why: `fm ideas` runs a fixed set of lenses and rounds. Whether an idea was later captured, built and kept is already in the task data, so lens yield can be computed. Today every lens gets equal weight.
  Done when: `fm ideas --stats` shows built-and-survived counts per lens and round, and the next mission pack suggests dropping or doubling lenses.

- **Score the brief's risks against what happened** — FEATURE — value 4 — effort S — risk low — category: planning
  Why: briefs name risks up front. If the real failure was not on the list, the risk-finding step missed it, and that is a systematic blind spot worth surfacing.
  Done when: at done, `fm task done` records for each declared risk whether it occurred and which unlisted problems occurred, and `fm friction` reports the hit rate and the blind-spot categories.

- **Track second-opinion yield** — FEATURE — value 3 — effort S — risk low — category: delegation
  Why: `fm second` (plan / debate / session) costs tokens and time, but nothing records when it changed the plan or caught something. Foreman should invoke it where it historically paid and skip it where it didn't.
  Done when: each second-opinion run logs "changed plan / caught bug / no effect", and intake's tier guidance cites the measured rate.

- **Reopen blocked tasks when the world learns something** — FEATURE — value 4 — effort M — risk med — category: persistence
  Why: three-failures-then-block records a diagnosis, but a blocked task stays dead even after a new lesson, a Claude model upgrade or a fix elsewhere removes its cause (T-0316, T-0335, T-0336 are blocked now).
  Done when: a block records a machine-checkable "unblock when" probe, and the drive re-runs probes after upgrades or lesson changes and moves tasks back to planned when a probe passes.

- **Wild: Interview the decisions, not the outcomes** — FEATURE — value 4 — effort L — risk med — category: decision quality
  Why: a good outcome can follow a bad decision, and Foreman learns from the outcome alone. A decision journal (options, odds, information available) is graded by a cold reviewer who sees only that, so the lesson targets the process rather than luck. wild
  Done when: `fm decide --review` grades a sample of closed decisions as "good process / lucky / unlucky", and lessons are tagged with which of the three they came from.

- **Wild: Keep scar tissue on the code** — FEATURE — value 4 — effort M — risk med — category: risk memory
  Why: every revert, rework and guard block on a file adds pain to it, and the pain decays. Plans touching a painful file automatically escalate the tier, add a review lens and cite the history. This is learned from outcomes rather than declared, unlike hand-set tripwires. wild
  Done when: `fm map --pain` ranks files by decayed pain, and a seeded S task touching a painful file gets an automatic extra review lens.

- **Wild: Hold an outcome autopsy for near-misses** — FEATURE — value 3 — effort M — risk low — category: reflection
  Why: lessons are written from failures, but tasks that passed on a retry or after a human nudge hold the same signal at lower cost. Foreman reads the diff between attempt 1 and the final state and drafts a "what almost went wrong" note. wild
  Done when: a task finished after at least one failed gate produces a drafted autopsy note, and `fm recall` returns it alongside the lessons.
