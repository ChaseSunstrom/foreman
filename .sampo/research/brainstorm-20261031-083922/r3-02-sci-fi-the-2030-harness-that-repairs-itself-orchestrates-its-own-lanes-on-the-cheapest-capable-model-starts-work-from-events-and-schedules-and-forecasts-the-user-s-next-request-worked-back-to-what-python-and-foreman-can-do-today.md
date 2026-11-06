# Brainstorm — lens: sci-fi: the 2030 harness that repairs itself, orchestrates its own lanes on the cheapest capable model, starts work from events and schedules and forecasts the user's next request, worked back to what Python and Foreman can do today

- **Open one incident record per trouble, fed by every signal** — FEATURE — value 4 — effort M — risk low — category: self-repair
  Why: the signal-to-fix loop (T-2272), triggers (T-2276), predictions (T-2290) and the user's "asked" corrections each keep their own store, so one root cause shows up as three unrelated events. Assumption: they can be joined by file path plus failure signature.
  Done when: `fm incident show ID` lists a CI red, two corrections and a recurring signature that share a signature as one timeline, and closing the FIX task closes the incident.

- **Explain any autonomous act with `fm why`** — FEATURE — value 5 — effort M — risk low — category: trust
  Why: model picks (T-2291), self-fixes, trigger fires and lane recoveries all happen unattended. The user can only see them by reading logs. Assumption: each act already records its inputs somewhere.
  Done when: `fm why LANE|FIX|TRIGGER` prints the rule or history rows that caused it, and the choice it overrode, in under 10 lines.

- **Set an autonomy dial from 0 to 5, shown in the status line** — FEATURE — value 4 — effort S — risk low — category: simplicity
  Why: Missions 8/#11 and #12 stack timers, triggers, self-fixes and speculative lanes, and each has its own setting. A single level that names exactly what is allowed is easier for one yes to cover. Assumption: the existing grants can be grouped into levels.
  Done when: `fm autonomy 2` makes every trigger or self-fix above level 2 refuse with the level named, and a test shows each level's allowed list.

- **Run unattended lanes in a bubblewrap sandbox** — SECURITY — value 4 — effort M — risk med — category: sandbox
  Why: file, CI and issue triggers start work with nobody watching, and the steers demand the guard stays intact. Assumption: bwrap is available on Linux (the environment is Arch).
  Done when: a self-triggered lane that tries to write outside its worktree, or read `~/.ssh`, fails in a test, and an interactive lane is unaffected.

- **Forecast merge conflicts before spawning parallel lanes** — FEATURE — value 4 — effort M — risk low — category: orchestration
  Why: Missions 5-8 ran as parallel lanes merged in order, and the conflict-brief test (T-2208) exists only after a conflict happens. fm graph blast already gives co-change neighbours. Assumption: blast sets overlap enough to predict most conflicts.
  Done when: `fm lane brief` for two tasks with overlapping blast radius warns, names the shared paths, and offers to serialize them or assign an owner for each file.

- **Compile repeated lane move sequences into stdlib verbs** — PERFORMANCE — value 4 — effort L — risk med — category: lean
  Why: the user's rule is that a free arm beating a session arm is a top gap, and the lean ratchet wants fewer tokens. Lanes that repeat the same deterministic steps spend model tokens on them. Assumption: lane transcripts keep tool-call sequences.
  Done when: a sequence seen in 5+ lanes with identical shape becomes a draft `fm new tool` scaffold with a failing-first test, and the next lane calls it instead of repeating the steps.

- **Make `fm me` the user model, readable, editable and deletable** — FEATURE — value 4 — effort M — risk low — category: privacy
  Why: anticipation (#3) builds a model of the user's habits and machines, but nothing says what is in it. Local-first means the user should own it. Assumption: it is stored as scattered ledger rows today.
  Done when: `fm me` lists each learned fact with its source event and age, `fm me forget ID` removes it, and the predictor measurably stops using it.

- **Log every outbound model call in an egress ledger** — SECURITY — value 4 — effort S — risk low — category: privacy
  Why: tool-less children and `claude -p` lanes send context packs outward, and nothing records what left. The privacy rule is that nothing leaves without an explicit setting. Assumption: all calls go through a few spawn points.
  Done when: `fm egress` lists each call with destination, byte count, a hash of the content and the task, and a test fails if a new spawn path skips the ledger.

- **Check the diff against the lane brief at merge** — FIX — value 4 — effort M — risk low — category: verification
  Why: the lane writer and the merger are the same pipeline, and the open question is which verbs have no check between writer and judge. Assumption: the brief lists scope paths and clauses.
  Done when: a lane that touches files outside its brief's scope, or leaves a brief clause with no change, gets held at merge with the delta named.

- **Wild: Share failure signatures between the user's machines over git** — FEATURE — value 3 — effort L — risk med — category: federation
  Why: wild; the user model includes "my machines", and a bug found on one laptop should immunize the other. Assumption: signatures can be shared without code or paths.
  Done when: a signature recorded on machine A makes machine B's `fm doctor` warn before B hits it, and no file content crosses.

- **Wild: Spend idle cheap-model budget on adversarial exam scenarios** — FEATURE — value 3 — effort M — risk low — category: self-test
  Why: wild; the steers want child-authored scenarios in languages fm find wasn't written for, and the overnight shift has idle capacity. Assumption: the tool-less child can write a scenario without seeing Foreman's code.
  Done when: a nightly pass adds at least 3 new held-out scenarios to a pool that the self-fixer cannot read, and the morning note reports the miss rate on them.

- **Wild: Let Foreman rehearse the day's first likely request in a throwaway lane before the user types it** — FEATURE — value 3 — effort M — risk low — category: anticipation
  Why: wild; predictions are scored but only drafted on spec. A rehearsal reports the first failure the user would hit, not only a draft. Assumption: prediction precision is high enough to justify the spend.
  Done when: a rehearsed lane for a predicted task records its first red step, and the real request, when it matches, starts with that note.

- **Wild: Let the user type "again" and have Foreman find which of its autonomous acts the user means** — FEATURE — value 3 — effort S — risk low — category: user value
  Why: wild; user corrections are the best signal and today they have to be turned into a task by hand. Assumption: a short reply right after an autonomous act is reliably about it.
  Done when: replying "again" or "no" within a turn of a lane merge or self-fix opens a correction task linked to that act, and `fm why` shows the link.

Next question: Which autonomous acts has the user never seen the result of, and how would the user know one went wrong?
Next question: Which of Foreman's stores would a second machine need to read to act as the user's twin, and which must never leave the first?
