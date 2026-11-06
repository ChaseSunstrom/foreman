# Brainstorm — lens: bold bets

- **Tail other harnesses' transcripts as a trigger source** — FEATURE — value 5 — effort M — risk med — category: agents
  Why: assumption: Codex, Gemini and opencode have no Stop-gate (T-0337, T-0335 blocked), and a tick that reads their transcript files needs no install. When a transcript claims "done" with no proof command run, the tick files a verify lane. This is a trigger measured against a real signal and useful on harnesses where hooks don't exist.
  Done when: a fixture Codex transcript ending "all tests pass" with no test command makes `fm tick` file one verify task naming the unproven claim. A transcript with a run test does not.

- **Measure recall by auto-detecting misses from the user's own fixes** — FEATURE — value 5 — effort M — risk med — category: measurement
  Why: the pack's grading ideas are mostly about precision (acted-on rate, keep/kill). Recall, meaning what the tick should have caught, has only a manual `fm missed`. The user's own `revert`, `fixup!` and "fix:" commits are signals Foreman didn't author. Bisecting the event tape to the earliest moment a trigger could have seen the problem gives "missed by N hours".
  Done when: replaying a fixture history with one planted fix commit writes a miss row with a lead-time estimate. `fm doctor` shows self-triggering recall beside precision, with its denominator.

- **Estimate the value of timeliness from lateness as a natural experiment** — FEATURE — value 4 — effort S — risk low — category: measurement
  Why: session-piggyback ticks fire at uneven lateness (a lateness ledger is already proposed). That variation is free randomisation, so no install or control arm is needed. Regressing "kept / acted-on" on lateness shows whether earlier fires are worth more.
  Done when: given a synthetic ledger where outcomes decay with lateness, `fm outcomes --by lateness` recovers the planted slope within 20%. It prints "insufficient" under 30 fires.

- **Grade self-started work by line survival in git** — FEATURE — value 4 — effort M — risk low — category: measurement
  Why: assumption: the tower's standing rule asks for signals Foreman didn't author. For commits a trigger started, `git blame` 14 and 30 days later gives the share of lines still alive. That is an external, install-free grade of whether the fire was useful.
  Done when: a fixture where half of a self-started commit's lines were later rewritten reports 50% survival at 30 days, split by trigger.

- **Tune trigger thresholds by searching over the replay tape** — PERFORMANCE — value 4 — effort M — risk low — category: triggers
  Why: assumption: every interval, debounce and storm cap is hand-set. Searching them against a recorded tape gives a precision/recall/spend Pareto front the user can pick from. It runs offline at zero tokens, so it works before any timer exists.
  Done when: `fm tick tune <trigger>` prints at least 3 non-dominated settings with spend, and the chosen one is stored with the tape digest it was tuned on.

- **Model-check the trigger table for storms, cycles and starvation** — SECURITY — value 3 — effort M — risk low — category: verification
  Why: the pack lists cycle checks and storm breakers as separate ideas. A bounded exhaustive search over (trigger table × small event alphabet) can prove "no event sequence of length ≤ N spawns more than K lanes", or produce a counterexample tape that is saved as a regression.
  Done when: a fixture table with a self-feeding trigger yields a counterexample tape under 12 events. The shipped table passes the same bound.

- **Show the trigger-behaviour diff in every release** — FEATURE — value 3 — effort S — risk low — category: release
  Why: the guard has a verdict-diff idea, but triggers don't. Replaying the golden tape through the old and new table shows which fires appeared, vanished or moved, so a silent behaviour change is caught at `fm ship`.
  Done when: a release that changes one debounce prints "+2 fires, −1 fire, 1 later" against the golden tape. An unchanged table prints "no change".

- **Let the model write its own wake plan at Stop, vetted before arming** — FEATURE — value 4 — effort M — risk med — category: agents
  Why: assumption: at session end the model holds the best knowledge of what is fragile ("rerun when CI finishes", "recheck after the dep bump"). It drafts triggers in the table format, and each one must pass a shadow replay and a different-model cold read before it arms. This differs from mining the user's habits.
  Done when: a session ending with a flaky-test note leaves one draft trigger in shadow with its condition and expiry, and nothing arms without the replay and read.

- **Wild: Foreman Town, a generated micro-world with a calibrated stub user** — FEATURE — value 4 — effort L — risk med — category: exam
  Why: wild. The week of live ticks can't be graded without the install. Five generated fake repos with a scripted forge and 30 simulated days run in minutes at zero tokens. The stub user only grades fires once its keep/drop agreement with the real dropped ledger passes a held-out threshold.
  Done when: `fm exam town` runs 30 simulated days and prints per-trigger precision and recall. Its stub user shows at least 80% agreement on 20 held-out real drops, or the grade prints "uncalibrated".

- **Wild: have a tool-less child act as the scheduler, from English rows only** — FEATURE — value 3 — effort S — risk low — category: exam
  Why: wild. Give a child the one-sentence-per-row trigger table and an event tape, then ask which fires happen. Any disagreement with the real dispatcher marks an ambiguous spec or a bug. It comes from outside Foreman's code, in line with the weakness-finding steer.
  Done when: on a 40-event fixture tape the child and dispatcher agree on all but a planted ambiguity. The report lists each disagreement with its row.

- **Wild: make the install card a replay of the user's own last week** — FEATURE — value 4 — effort M — risk low — category: delight
  Why: wild. Before asking for the timer, Foreman replays the user's real last 7 days of git and CI events through the table and shows the fires it would have made, marked "would have acted / would have stayed quiet / unsure". The user judges real moments, not a pitch, and each answer is a graded label.
  Done when: a repo with 7 days of history produces a card of at most 10 fires, each with a one-word answer, and the answers are stored as labels for the precision grade.

Next question: which self-triggering result would the user change a decision on, and which of these measures could be wrong in a way that never shows in any ledger?
Next question: what happens to a trigger's grade when the user's behaviour changes (new job, new repo) and the tape no longer resembles their week?
