# Brainstorm — lens: agents of agents

- **Broadcast antibodies to running lanes** — FEATURE — value 4 — effort M — risk med — category: orchestration
  Why: the same refusals recur across sessions (the `fm focus …; sed -i …` loop hit twice in a row, the `rm` symlink case, tool caches in `lane rm`), and each lane learns it separately. Assumption: lanes can read a shared, live rules file mid-run.
  Done when: a failure pattern first seen in lane A reaches a running lane B as a one-line warning within one tool call, and a test shows lane B avoids the pattern without being restarted.

- **Let idle lanes steal work from slow ones** — FEATURE — value 4 — effort L — risk med — category: scheduling
  Why: the drive idled with 20+ tasks queued (T-0401), and a single L task can hold one lane while others sit empty. Assumption: plan steps carry file footprints, so independent steps can be carved off safely.
  Done when: in a fixture with one 6-step task whose steps 4–6 don't overlap steps 1–3, an idle lane takes steps 4–6 and both merge cleanly. The ledger records the split, who took what, and the merge.

- **Park lanes on preemption and resume them at the exact step** — FEATURE — value 4 — effort M — risk med — category: orchestration
  Why: the main thread is mid-task while lanes finish (JARVIS T-0278/T-0280), and a higher-priority FIX can't reach a busy lane. Resume-at-step already exists for sessions; this extends it to lanes.
  Done when: an urgent task parks a running builder lane with a checkpoint, runs, and the parked lane resumes at its recorded step with no repeated work.

- **Share a blackboard of retractable facts across live agents** — FEATURE — value 4 — effort L — risk med — category: shared state
  Why: reviewers, scouts and builders each rediscover the same facts, and one wrong claim spreads through summaries. Assumption: facts can be keyed by file and tree hash.
  Done when: scout A posts "module X has no callers" with provenance. Builder B reads it. After A retracts it, B's dependent plan step is flagged stale on its next read.

- **Audit what each child's summary dropped** — FEATURE — value 5 — effort M — risk low — category: handoff fidelity
  Why: the orchestrator trusts a child's returned summary, which is lossy. Caveats, skipped tests and "I couldn't verify" vanish at the seam. Assumption: the child's transcript is available to a checker.
  Done when: a seeded transcript with a buried "tests not run" line produces a summary-audit finding naming that line. A summary that omits no caveat produces none.

- **Grade the briefs the orchestrator writes for children** — FEATURE — value 4 — effort M — risk low — category: delegation quality
  Why: builder briefs have needed repeated fixes (T-0399 "edit with Edit/Write", T-0428 CHANGELOG ownership). Each came from a bad brief discovered the hard way.
  Done when: `fm friction` reports per-brief-template rework and clarification rates from the ledger, and a template with a high rate is flagged with the child's own complaint quoted.

- **Choose the orchestration shape per task, learned from bench** — FEATURE — value 4 — effort L — risk med — category: topology
  Why: single lane, fan-out review, tournament and pipeline all exist, but the user or the plan picks one by hand. `fm bench` already replays tasks with candidate plugins. Assumption: finished tasks have enough features (type, tier, footprint, past cost) to predict the best shape.
  Done when: `fm bench` compares an auto-chosen shape against a fixed default on the replay set and reports pass rate and cost for each. Auto-select ships only if it wins.

- **Brief children with commander's intent and log their deviations** — FEATURE — value 3 — effort S — risk low — category: delegation
  Why: guard refusals interrupt lanes over details the intent never needed. Intent plus constraints plus stop conditions lets a child adapt where the brief was wrong, and it logs where it did.
  Done when: a lane brief has intent, hard limits and stop conditions sections. A deviation is recorded as a ledger event the reviewer sees at done.

- **Add breakpoints to a live fleet** — FEATURE — value 3 — effort M — risk med — category: fleet debugging
  Why: the desktop app already controls sessions, but the user can only watch or kill. Assumption: spawn and merge are the only points where pausing is safe.
  Done when: "pause before the next spawn or merge" halts there, shows the brief about to be sent, accepts an edit, and resumes. The ledger shows the edited brief.

- **Run lanes against mock neighbours until the real one arrives** — FEATURE — value 4 — effort L — risk high — category: parallel lanes
  Why: dependent tasks wait for each other and queues sit idle. Assumption: a task can name the interface it needs, so a stub or mock can be generated from that.
  Done when: lane B builds against a generated mock of lane A's interface. When A merges, B's tests rerun against the real code and any mismatch fails B's done-gate.

- **Wild: Fractal Foremen — a task can own a child Foreman scope** — FEATURE — value 5 — effort L — risk high — category: recursion
  Why: the user asked for "super recursive". An L task becomes a sub-project with its own queue, gates and ledger, returning one receipt (diff, proof, unverified list) to the parent. Assumption: the nesting depth and budget are capped by the lineage tree.
  Done when: a parent task spawns a child scope, the child closes with its own gate run, and the parent's ledger links the child's receipt. A depth-3 attempt is refused.

- **Wild: Drill handoff fidelity by swapping the model mid-task** — FEATURE — value 4 — effort M — risk low — category: resume robustness
  Why: resume after `/compact` is a core promise, yet nothing proves STATE and the brief are enough for a different reader. Assumption: a cheap model, or the same one with no history, works as the fresh reader.
  Done when: a nightly drill halts a finished-half lane, restarts it with only brief and STATE, and reports whether it reached the same next action. Any divergence names the missing fact.

- **Wild: Consult peers by asking agents on a rate-limited line** — FEATURE — value 3 — effort M — risk med — category: peer help
  Why: a stuck builder can only ask the user or give up. A "second opinion" line to a scout or another lane's specialist, with a budget and a depth limit, would unstick it. Assumption: answers are logged as typed receipts.
  Done when: a stuck builder in a fixture asks a peer and receives an answer within its cap. The ledger shows question, answer and cost. A fifth question is refused.
