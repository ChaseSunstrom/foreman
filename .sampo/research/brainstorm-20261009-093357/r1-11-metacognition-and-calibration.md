# Brainstorm — lens: metacognition and calibration

- **Score every forecast and feed it back into thresholds** — FEATURE — value 5 — effort M — risk low — category: calibration
  Why: the pack covers predicting gate outcomes, sub-agent confidence and brief assumptions "with confidence", but none of it is scored afterwards. Assumption: the confidences are currently stated and never compared to results. Each step, assumption and sub-agent report carries a probability. A ledger Brier-scores them per task type, tier and model. Intake and the drive then use the measured curve to decide when to plan deeper, race attempts or ask.
  Done when: `fm calibration` prints a reliability table per task type, and a test shows a type with 50% real pass rate and "90%" claims raises the plan depth Foreman requests.

- **Tag every claim with its epistemic status** — FEATURE — value 5 — effort M — risk med — category: honesty
  Why: "evidence before claims" exists, but briefs and done summaries don't say how a statement is known. Assumption: summaries mix observed and inferred facts. Statements carry observed (ledger event), inferred, remembered (lesson or recall) or assumed. The done-gate rejects "observed" with no matching event and shows the assumed ones.
  Done when: a done summary that says "verified X" with no run event for X is refused, and the allowed form renders as "inferred".

- **Grade decisions apart from outcomes** — FEATURE — value 4 — effort M — risk low — category: learning
  Why: lessons are recorded at finish and scored by outcome (T-0217), which teaches luck as well as skill. At finish, a cold reader sees only what was known at each decision point and rates the choice sound or unsound. The outcome is stored separately. Lessons only form from sound-but-unlucky or unsound-but-lucky cases, and from the consistent ones.
  Done when: the lesson record has a `decision_quality` field distinct from `outcome`, and a lucky pass by an unsound choice yields a warning lesson, not a confirmation.

- **Meter marginal information and stop research when it dries up** — FEATURE — value 4 — effort M — risk low — category: stopping rules
  Why: the first brainstorm produced 835 ideas and recursive rounds see prior ideas, but no round decides when it has stopped finding anything new. Recon, audit and `fm ideas` rounds report new-fact or new-idea rate per query (novelty versus prior output). The orchestrator stops below a threshold and says why.
  Done when: an `fm ideas` run ends early with "round 3 novelty 4% < 10%" and a test with a duplicate-heavy fake child triggers it.

- **Audit which deliberation passes ever change anything** — FEATURE — value 4 — effort M — risk low — category: deliberation cost
  Why: intake has 3+ options for M/L, planning passes, second opinions and audit lenses. Assumption: nobody measures which ones alter the final plan or catch a defect. Using bench replays and the ledger, record per pass whether it changed the plan, produced an accepted finding, or did neither. Passes that never earn their tokens are made conditional.
  Done when: `fm friction` lists passes ranked by "changed outcome" rate, and one pass is gated on a measured condition.

- **Build a competence atlas of where Foreman is weak** — FEATURE — value 4 — effort M — risk low — category: self-model
  Why: bench, failures and blocks exist as separate data. Aggregate first-attempt pass rate, rework and block rate by area, task type and model into a map. At intake, a weak cell triggers a named response (race, reviewer, human check) and the brief says "I'm weak here: 3 of 7 prior attempts reworked".
  Done when: a brief touching a weak area shows the atlas line and its chosen safeguard, and a strong area shows nothing.

- **Trip a re-frame when effort passes the estimate** — FEATURE — value 4 — effort S — risk low — category: sunk cost
  Why: the only brake today is "3 failed attempts → block". At 1.5× estimated time or steps, force a short "should this still be this task?" step: split, descope, abandon or continue, with the reason recorded. Assumption: estimates exist per task (T-0451 is queued).
  Done when: a task exceeding its estimate cannot start its next step until a reframe entry exists in the ledger.

- **Model what the user believes and correct the gap** — FEATURE — value 4 — effort M — risk low — category: shared understanding
  Why: the user's steers repeatedly show a mismatch (cleanup "never got done", a budget gate that blocked early). Track what the user last saw or said about each task and decision, compare it with ground truth, and open the return screen with "you probably think X; actually Y".
  Done when: after a task silently changes state while the user is away, the next session start lists it as a belief correction, and a fixture test shows no entry for state the user already saw.

- **Lint certainty language against evidence strength** — CLEAN — value 3 — effort S — risk low — category: wording
  Why: assumption: summaries say "fixed" or "works" regardless of the evidence rung. A done-gate lint maps words ("fixed", "should", "likely") to the strength of proof recorded. An overclaim is rewritten or refused.
  Done when: "fixed" with only a unit test of a mock is flagged, and the same line with a red→green proof passes.

- **Give Foreman a blind self-grading exam** — FEATURE — wild — value 4 — effort M — risk low — category: self-knowledge
  Why: wild. Foreman rereads old transcripts with the outcome hidden, rates them done-well or not, and is compared to what actually happened (rework, reverts, steers). That measures whether its judgment of its own work can be trusted before relying on it for reviews and "done" claims.
  Done when: `fm exam` outputs agreement rate and a bias direction (too lenient or too harsh) over N held-out finished tasks.

- **Require a teach-back before editing unfamiliar code** — FEATURE — wild — value 4 — effort M — risk med — category: comprehension
  Why: wild. Before editing a flagged-weak area, the builder writes a short explanation of how it works. A cold fm-scout answers questions about the code using only that explanation, and a miss means the builder hasn't understood and must read more.
  Done when: a lane touching a weak-atlas file shows a teach-back score in its brief, and a deliberately wrong explanation fails the check.

- **Reread each L plan with its rationale stripped** — FEATURE — wild — value 3 — effort S — risk low — category: plan quality
  Why: wild. A fresh agent receives only the steps and acceptance criteria, not the reasoning, and has to say what each step is for. Steps it can't justify, or gaps it finds, return to the planner before any code. This catches plans that only make sense inside their author's context.
  Done when: an L plan with a step whose purpose appears nowhere in its criteria is bounced with a note naming that step.
