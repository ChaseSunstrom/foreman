# Brainstorm — lens: bold bets

- **Quarantine memory writes that carry instructions** — SECURITY — value 4 — effort M — risk med — category: memory poisoning
  Why: assumption: session memory is model-written and loaded at every session start, so one injected note can persist into later sessions. No pack item binds memory writes to review.
  Done when: a memory write containing an imperative aimed at the guard, rules, or hooks is held in quarantine and absent from the next session's loaded memory.

- **Plant a decoy memory and flag any run that acts on it** (wild) — SECURITY — value 3 — effort S — risk low — category: canary
  Why: wild: a fake memory note saying to skip the guard would be read only by a poisoned run. Canary files exist, but no canary sits in the memory the model loads.
  Done when: a test run that follows the decoy's instruction writes a journal alert and is stopped before its first write.

- **Hand a half-finished run to a second provider with a state capsule** — FEATURE — value 4 — effort L — risk med — category: model failover
  Why: a usage limit or runner crash loses in-flight reasoning, and failover today happens only between whole tasks. Assumption: a capsule of the plan, the edits so far, and the last proof lets a second runner continue.
  Done when: a run killed after step 3 resumes on a second runner from the capsule and its next proof passes.

- **Turn a rejected race candidate into the next task's failing test** — FEATURE — value 3 — effort M — risk low — category: agents
  Why: race fixes discard the losing candidate, but the behaviour it got wrong is evidence. Assumption: a loser that passes its own gate but fails the winner's proof marks a real edge case.
  Done when: the loser's distinguishing behaviour is written as a test that the chosen fix passes and the journal links to it.

- **Judge the duel on a public corpus of real repos, nightly** — PERFORMANCE — value 5 — effort L — risk low — category: evaluation
  Why: the duel data behind ceremony profiles (T-1266) and the "beats bare Claude" claim comes from one repo, a sample of one. Assumption: a corpus of 20 or more repos would show which results hold across codebases.
  Done when: a nightly report lists per-repo verdicts for at least 20 repos, with the pass rate and cost for Foreman and bare Claude Code.

- **Rewrite a request with no checkable outcome before it queues** — FEATURE — value 4 — effort S — risk low — category: intake
  Why: vague requests get queued and fail only at close, when the proof has nothing to check. Assumption: a request that names no command, file, or observable result can be turned into one before any spend.
  Done when: a request such as "make it faster" is queued only after Foreman offers a provable version (for example, a benchmark command with a threshold) and the user accepts it.

- **Blind the context to the diff and the failing output** — PERFORMANCE — value 3 — effort L — risk med — category: context diet
  Why: packs grow with repo size, and most of the token cost goes to files the fix never touches. Assumption: a window of the failing output, the touched symbols, and the diff holds the pass rate at a fraction of the input tokens.
  Done when: on a 10-task set, the blind window matches the full pack's pass rate and uses under half the input tokens.

- **Start the close receipt before the last gate ends** — PERFORMANCE — value 2 — effort S — risk low — category: close latency
  Why: receipts wait for the slowest gate, so the user waits on the slowest check even when the change is already proven. Assumption: most gates pass or fail before the last one finishes.
  Done when: in a timed test, the first receipt lines print before the slowest gate exits.

- **Cite the proof for every claim in the close receipt by line** — FEATURE — value 3 — effort M — risk low — category: trust
  Why: receipts state outcomes but do not say which command backs each claim. Assumption: a claim-to-command map makes an unproven claim visible.
  Done when: each sentence in a receipt names the command and exit code behind it, and a sentence with no command is printed as "unproven".

- **Bias the pack toward the file under the editor cursor** (wild) — FEATURE — value 3 — effort M — risk low — category: context
  Why: wild: the file and symbol under the user's cursor are a strong signal of intent, and the pack ignores them. Assumption: the editor can export the cursor position through the existing mod.
  Done when: a pack built with the cursor on file X lists X's symbols and their callers first, and a test confirms the order.

- **Write each run's plan as a haiku the user must approve before the first edit** (wild) — DELIGHT-type idea filed as FEATURE — value 2 — effort S — risk low — category: approval
  Why: wild: a three-line plan in a fixed form is short enough to read at a glance. Assumption: most users skim plans, and a short form changes what they check.
  Done when: a run stops before its first edit, prints the three-line plan, and continues only after one key press.

- **Stop a run whose plan changes after its first proof** — SECURITY — value 3 — effort S — risk low — category: scope control
  Why: a plan that rewrites itself after the first pass often means the run has drifted from the request. Assumption: plan changes after the first proof are rare and worth a stop.
  Done when: a test that changes the plan after the first green proof halts the run and writes a journal line naming the drift.
