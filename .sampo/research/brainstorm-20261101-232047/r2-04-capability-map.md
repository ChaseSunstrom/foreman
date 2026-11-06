# Brainstorm — lens: capability map

- **Rank suspects by fault localization before planning a FIX** — FEATURE — value 4 — effort M — risk low — category: diagnosis
  Why: Agentless and SWE-agent run spectrum-based localization (which files the failing tests touch and the passing ones don't). The pack's deliberation ideas start from the plan, not from a ranked suspect list. assumption: Foreman can get per-test coverage cheaply for Python.
  Done when: for a seeded failing test, `fm task focus` prints a ranked list of at most 5 suspect files, and the planted-fault file is in the top 3 on 8 of 10 fixture bugs.

- **Keep a debugging hypothesis table** — FEATURE — value 4 — effort S — risk low — category: diagnosis
  Why: Scientific-method debugging means hypothesis, predicted observation, experiment, result. The existing "readings" and "assumption probes" ideas cover requests, not root causes. assumption: FIX plans currently let the model guess a cause and edit.
  Done when: the plan gate refuses a FIX plan with fewer than 2 hypotheses, or with none carrying an experiment command that distinguishes them. Closing the task records which hypothesis survived.

- **Shrink every failing repro to a minimal case** — FEATURE — value 3 — effort M — risk low — category: diagnosis
  Why: Delta debugging (ddmin, C-Reduce) is standard in mature debugging tools, and the pack has no minimizer. Small repros make "test the fix in parallel lanes" cheaper and sharper. assumption: failing evidence can be replayed deterministically.
  Done when: `fm repro shrink CMD` reduces a seeded 200-line failing input to at most 20 lines that still fail with the same signature.

- **Mine git history for prior attempts at the same change** — FEATURE — value 4 — effort S — risk low — category: prior art
  Why: Pickaxe (`git log -S/-G`) and revert detection show whether the obvious approach was already tried and backed out. The existing ideas remember rejections within a session or in the ledger, but the repo's own history is untouched. assumption: reverts and "Revert" commits are common enough to matter here.
  Done when: for a task touching a file with a past revert, the plan's Approach section is refused unless it names that commit and says what differs. A fixture repo covers this.

- **Require a threat-model line on trust-boundary tasks** — FEATURE — value 3 — effort S — risk low — category: security
  Why: Tools like OWASP Threat Dragon and STRIDE-lite templates force a spoofing, tampering, disclosure and privilege check when input crosses a boundary. The pack has an FMEA table for L tasks but no boundary-triggered check. assumption: a diff scan can detect new parsing of external input, subprocess calls or file writes outside the repo.
  Done when: a diff adding `subprocess` use on a variable string gets a plan-gate prompt with 4 STRIDE answers. A diff with no boundary change gets none.

- **Estimate cost and complexity before building** — FEATURE — value 3 — effort M — risk med — category: performance
  Why: Fully featured planners (Copilot Workspace, Devin) estimate size and effort. The pack quotes cost for fan-outs but never makes the plan predict its own runtime or complexity change on hot paths. assumption: hook p95 and exam time are the main hot paths.
  Done when: a plan touching a file listed in the hot-path budget must state the expected change in ms or bytes. Close compares it with `bench_hooks` and logs the error.

- **Infer invariants from passing runs and re-check them after the change** — FEATURE — value 3 — effort L — risk med — category: verification
  Why: Daikon-style invariant inference catches "worked but changed behaviour elsewhere" across a blast radius, which the pack handles only by running tests. assumption: a Python tracing hook over the existing suite is cheap enough to run in a lane.
  Done when: on a seeded refactor that silently changes a return type, the check reports the violated inferred invariant while the existing tests stay green.

- **Cross-validate candidates with generated tests, then vote** — FEATURE — value 4 — effort M — risk med — category: candidate selection
  Why: AlphaCode and CodeT sample many candidates, generate tests, and choose by agreement. The pack's race ideas choose by the user's rubric or one verify. A model-free agreement score (which candidates pass each other's tests) is missing. assumption: it is cheaper than a full lane per candidate.
  Done when: `fm race` with 3 candidates prints a pass matrix and picks the candidate that passes the most peer-written tests, with a tie going to the smaller diff. A fixture with one subtly wrong candidate shows it ranked last.

- **Emit a decision record from each L plan with a revisit trigger** — FEATURE — value 3 — effort S — risk low — category: docs
  Why: ADR tooling (adr-tools, Kiro design docs) keeps the chosen option, rejected options and the date or condition to revisit. `decisions.md` exists but not a per-plan record in this shape. assumption: it can reuse the plan's Approach section.
  Done when: closing an L task appends an ADR file listing context, options with rejection reasons, the decision and a revisit condition. `fm doctor` flags one whose condition now holds.

- **Wild: Hold a pre-mortem with a child told the change already failed in production** — FEATURE — value 4 — effort S — risk low — category: deliberation
  Why: wild. Gary Klein's pre-mortem is the best-known technique for finding failure modes, and a tool-less child with the diff and the sentence "this caused an incident last week" lists causes the author won't.
  Done when: L tasks get 5 or more ranked failure stories in the plan file, and at least one is turned into a test or an explicit "accepted risk" line.

- **Wild: Re-run the thinking in a mirror universe** — FEATURE — value 3 — effort L — risk med — category: verification
  Why: wild. Metamorphic testing runs the winner on perturbed inputs: shuffled order, renamed identifiers, other locale or timezone, a different Python minor. A fix that holds only in one world is flagged.
  Done when: a seeded order-dependent fix passes the normal suite but `fm perturb` fails it under shuffled test order and a TZ change.

- **Wild: Give the plan a "would a stranger approve this" PR rehearsal** — FEATURE — value 3 — effort S — risk low — category: review
  Why: wild. Reviewers like CodeRabbit and Greptile work from the diff cold. Before building, a child reads only the plan and writes the review comments it would leave, and the plan answers them.
  Done when: the plan file has a "reviewer questions" section with at least 3 entries, each answered or deferred, before the first edit.

- **Wild: Offer "explain the road not taken" as a replayable branch** — FEATURE — value 2 — effort M — risk low — category: deliberation
  Why: wild. After close, one command re-opens the runner-up in a scratch worktree and shows its diff size and test result, so the user can switch cheaply.
  Done when: `fm road-not-taken T-N` creates a worktree with the runner-up's plan applied (or a stub with its plan) and prints its test status.

Next question: Which of the 58 empty cells are about capabilities that need a language or tool Foreman doesn't ship detectors for (tracing, coverage, shrinking), and what is the fallback for a repo without them?

Next question: What does the user see when a deliberation step is skipped because the task is S-tier, and has any skipped step ever turned out to be the missing one?
