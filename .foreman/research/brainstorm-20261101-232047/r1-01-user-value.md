# Brainstorm — lens: user value

- **Show a one-screen decision card at plan accept** — FEATURE — value 5 — effort M — risk low — category: user value
  Why: the user's steers say "never block on the user" and "decide, record, keep going", so they review decisions after the fact. A card with readings, options tried, the pick, "what would change my mind" and the undo line makes that review take 20 seconds.
  Done when: `fm task plan` on an M task prints or serves a card under 25 lines, and a test asserts all five fields are present.

- **Record whether deliberation changed the outcome** — FEATURE — value 5 — effort M — risk low — category: measurement
  Why: the lean substance rule says growth waits for a measurement. Nothing here says whether exhaustive thinking ever beats the first instinct. Log per task: first-instinct approach, final approach, and whether they differ.
  Done when: `fm outcomes --thinking` prints the share of tasks where the final pick differed from the first, split by tier.

- **Skip deliberation for S tasks and log the skip** — PERFORMANCE — value 4 — effort S — risk low — category: speed
  Why: gen-0 #2 says "an S task doesn't pay an L task's cost". Assumption: S tasks still run the full plan-gate ceremony today.
  Done when: an S task closes with zero race and zero research lanes and a "skipped: S" row in the ledger, and an L task still gets them.

- **Keep an edge-case deck per task kind, built from reopens** — FEATURE — value 4 — effort M — risk low — category: reliability
  Why: gen-0 #2 requires edge cases. Hand-written lists rot. Mine them from fix-after-done commits and the user's corrections, then offer 3 to 5 relevant ones at plan time.
  Done when: planning a FIX shows at least 3 edge cases that each cite a past reopen or correction, and a test checks the citations resolve.

- **Fill the 58 cells from live deliberation traces, not prose** — CLEAN — value 4 — effort M — risk med — category: coverage
  Why: the standing rule says a cell counts only if it names a concrete capability grounded in a file or a real gap, and templated cells don't count. Each cell should cite a plan, decision or probe row.
  Done when: `fm genesis sweep` passes the coverage check with the 58 cells filled, none templated or duplicated, and each citing a path or ledger id.

- **Explain blast radius in plain words** — FEATURE — value 4 — effort S — risk low — category: docs/UX
  Why: `fm graph blast` prints a graph. The user needs "touches 12 files, 3 callers, runs on every prompt". Report "unknown" instead of "none" when the graph is blind.
  Done when: the plan's Risks section carries a sentence generated from `fm graph blast`, and an unindexed language yields "unknown".

- **Let the user override depth with one word** — FEATURE — value 3 — effort S — risk low — category: control
  Why: assumption: depth is chosen only by the tier. The user will sometimes want "think hard on this S" or "just do it" without editing config.
  Done when: `fm task focus --depth deep|quick` changes the lanes run, and the choice is recorded.

- **Run a deliberation budget alarm** — PERFORMANCE — value 3 — effort S — risk low — category: cost
  Why: nothing visible caps thinking spend against the work. The user's pace steer means usage matters.
  Done when: a task whose planning spend exceeds half its build spend prints one warning line at close, and a test covers it.

- **Add a pre-ask precedent check** — FEATURE — value 4 — effort M — risk low — category: autonomy
  Why: "never block on the user for rules, gates or process" and the avoidable-ask logging both show asks are costly. Search decisions.md and steers before `fm ask` and answer from precedent if one matches.
  Done when: `fm ask` on a question matching a recorded decision answers it with the cited decision id and sends nothing to the user.

- **Wild: add an "argue for the runner-up" button** — FEATURE — value 3 — effort M — risk med — category: web UI
  Why: wild. Assumption: the user sometimes distrusts the pick but has no cheap way to see the alternative. One click spawns a lane that builds the runner-up in a scratch tree and shows both diffs.
  Done when: clicking it in the web UI produces a side-by-side result without touching the working tree.

- **Wild: build a steer-twin that flags plans violating a steer** — FEATURE — value 4 — effort L — risk med — category: agents
  Why: wild. The steer list is long and the user keeps restating rules. A tool-less child that reads only the steers and the plan answers "which steer does this break?" before the plan is accepted.
  Done when: a seeded plan that breaks a known steer is flagged, and a clean plan is not, on 10 held-out cases.

- **Wild: replay the thinking as a scrubbable tree** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: wild. Options, prunes and the reasons for each are already recorded. A web UI page shows them as a tree you can step through, so "why did you choose this" has a visual answer.
  Done when: a finished L task's page renders its option tree with a reason on every pruned branch, and an empty state for tasks with no deliberation.

- **Add a "nothing to think about" receipt** — FEATURE — value 2 — effort S — risk low — category: observability
  Why: when exhaustive thinking finds one obvious approach, say so in one line, not three costume options. This matches the "options are one idea in three costumes" gap.
  Done when: a trivial task's plan prints "one viable approach, because X" and passes the plan gate.

Next question: Which of the 58 empty cells would the user notice missing, and which are only bookkeeping for the tower?
Next question: Does the user read the decision card, or do they only open it after something goes wrong, and which surface do they open first?
