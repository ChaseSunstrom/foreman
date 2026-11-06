# Brainstorm — lens: bold bets

- **Replay the user's real sessions as bench cases** — FEATURE — value 5 — effort M — risk med — category: bench
  Why: fm bench builds cases only from finished tasks with commits and tests. The user's actual requests that ended in corrections, "dropped" or "steered" entries are the strongest ground truth and never become cases. Pushback-as-test appears in earlier ideas, but nothing builds it from the session transcript plus the git state at that turn. Assumption: transcripts record enough to recover the repo commit at each prompt.
  Done when: `fm bench build --from-sessions` makes at least 3 cases from the last 20 sessions, each with prompt, parent commit and a correction-derived check, and `fm bench run` replays one.

- **Add a stage-skill trial gate before routing** — FEATURE — value 4 — effort M — risk low — category: interop
  Why: `fm next` routes installed skills from a cached index, and the "steered" entry asks to learn which hints help. A new skill is trusted by description only. Run each candidate skill on 3 relevant bench cases with and without the hint, and route it only if pass rate is no worse and cost is within +10%.
  Done when: `fm plugins trial SKILL` prints a paired pass-rate and cost table and writes an allow/deny flag that `fm next` honors.

- **Evolve the router, not only the prose** — FEATURE — value 4 — effort M — risk med — category: self-improvement
  Why: fm evolve mutates one instruction file, but STAGE_REFERENCE in fmcore.py and the skill-routing weights decide which text is ever seen. Mutate the stage-to-reference table and hint ranking, gated by `fm bench gate`.
  Done when: `fm evolve --target router` proposes a table change on an evolve branch and reports a gate verdict against live.

- **Add a request-to-oracle child** — FEATURE — value 4 — effort M — risk med — category: problem solving
  Why: criteria are written by the same thread that executes, so they can bend to the solution. A tool-less `claude -p` child sees only the raw request and the repo map, then writes the failing check. The main thread cannot see it until the red→green proof. Assumption: the bench can measure whether this lowers rework.
  Done when: `fm task plan --oracle` stores a hidden check hash, and `fm task done` runs it and records pass/fail in the brief.

- **Export gates as a stdlib MCP server** — FEATURE — value 4 — effort L — risk med — category: interop
  Why: other harnesses and bare Claude Code lack "done needs evidence." The only user-visible surface today is the plugin. A stdio MCP server exposing `task_done`, `evidence_add`, `recall` and `research_ask` lets any client use them. Stdlib JSON-RPC is feasible.
  Done when: a scripted JSON-RPC session lists the tools and `evidence_add` followed by `task_done` is refused without fresh evidence.

- **Mine a feature census from other harnesses on a schedule** — FEATURE — value 3 — effort M — risk low — category: research
  Why: the user asked to research what people want from harnesses. A landscape pass was done once by hand. `fm research ask` plus cached pages can re-run a fixed question set, diff against the last census, and file only new capabilities as inbox captures.
  Done when: `fm landscape` run twice prints only changed or new entries the second time and captures at most 5 inbox items.

- **Wild: Run a shadow-user soak** — FEATURE — value 4 — effort L — risk med — category: bench (wild)
  Why: a child role-plays the user from their verbatim steers and corrections, feeding a candidate build a whole queue of requests. It scores whether the output would trigger the same complaints, using a judge built from the user's drops and steers. Assumption: a judge from about 20 past corrections correlates with real acceptance.
  Done when: `fm bench soak A B` outputs complaint-count per build for the same scripted queue.

- **Wild: Let ideas be bets that settle** — FEATURE — value 3 — effort M — risk low — category: brainstorm (wild)
  Why: the last probe went dry, with 1 of 40 grounded. Each accepted idea records a predicted metric (turns, cost, pass rate) on a bench subset. After it ships, fm compares and scores the lens that produced it. Lenses with poor settled accuracy are dropped.
  Done when: an idea brief carries a `bet:` line and `fm ideas stats` shows per-lens settled hit rate.

- **Wild: Build a counterfactual ledger across plugin versions** — FEATURE — value 3 — effort L — risk med — category: self-improvement (wild)
  Why: fm bench compares A and B on demand. Nightly, replay the day's finished tasks with the previous plugin snapshot using leftover quota, and keep a trend of who would have won. This catches silent regressions between releases.
  Done when: `fm bench ledger` prints one row per night with pass rate and cost for current versus previous, and warns on a drop beyond the variance floor.

- **Wild: Add a stranger test** — FEATURE — value 3 — effort M — risk low — category: onboarding (wild)
  Why: Foreman's docs and hints are only tested by the people who wrote them. A fresh child gets only the README and a toy repo, attempts a task, and the run logs each stall, guard block or confusing hint as friction.
  Done when: `fm bench stranger` produces a transcript summary listing at least the first three points where the child hit a block or stall.

- **Add a sub-question disagreement check to research ask** — FEATURE — value 3 — effort S — risk low — category: research
  Why: research ask re-fetches quotes, but two researchers answering the same sub-question can both cite real pages that conflict. Detect differing conclusions per sub-question and mark them contested instead of merging them.
  Done when: a test with two stubbed researchers that disagree yields a note with a "contested" marker on that sub-question.
