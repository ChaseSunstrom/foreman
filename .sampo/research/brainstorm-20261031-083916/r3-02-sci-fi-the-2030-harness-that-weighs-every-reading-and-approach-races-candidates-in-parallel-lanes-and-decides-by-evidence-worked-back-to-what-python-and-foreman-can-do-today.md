# Brainstorm — lens: sci-fi: the 2030 harness that weighs every reading and approach, races candidates in parallel lanes and decides by evidence, worked back to what Python and Foreman can do today

Two answers to the earlier questions from this lens:
- **Writer and judge with no user-owned check:** `fm lane race` is one. A builder writes both the fix and its tests, then those tests pick the winner. Cold reads are another.
- **Numbers never checked by another party:** the "winner" line of a race and the confidence figure.

- **Cross-examine candidates with each other's tests** — FEATURE — value 5 — effort M — risk low — category: race
  Why: T-2271 races the runner-up, but each lane's own tests judge it, so a model sits on both sides (assumption: lanes ship tests).
  Done when: a fixture race where lane A's test catches lane B's bug records B as failing A's test, and the verdict shows the full candidate×test matrix.

- **Have a blind child write the race's acceptance checks** — FEATURE — value 5 — effort M — risk low — category: verification
  Why: the standing rule requires signals Foreman didn't author, and exam scenarios already come from a child that never sees the code. Apply the same rule to live races.
  Done when: a tool-less child sees only the task text and writes checks, the racing lanes never see them, and the verdict names which checks decided.

- **Mutation-grade every done-when command** — FEATURE — value 4 — effort M — risk low — category: proof
  Why: "proves its work with commands it really ran" is only as good as the command. Assumption: weak verifies exist (a `grep` that passes on anything).
  Done when: `fm task prove` flips small mutants (negate a condition, delete a line) in the touched files, reports the survivor count, and fails a verify that kills none.

- **Race performance candidates with interleaved benchmarks and an Occam tie-break** — PERFORMANCE — value 4 — effort S — risk low — category: race
  Why: T-2287's `--bench` times start tree versus current tree. Two candidates within noise should tie, and a tie should go to the smaller diff and blast radius.
  Done when: A/B runs are interleaved, the medians come with an interval, an overlapping interval is reported as "indistinguishable", and the smaller diff wins.

- **Run a 5-minute probe per option before choosing** — FEATURE — value 4 — effort M — risk med — category: planning
  Why: T-2269 forces 3+ options on paper only. Time-boxed scout lanes ("how far does each get before its first red?") turn the options into evidence before the full race.
  Done when: an M/L Approach lists a probe result per option (first-red step, minutes spent) and the choice cites it.

- **Collapse near-identical candidates before racing** — CLEAN — value 3 — effort S — risk low — category: cost
  Why: the Ideas list already worries about "one idea in three costumes". Compare the diffs, not the prose.
  Done when: two lanes sharing >90% of hunks are merged into one, the log says so, and the race cost drops.

- **Record lanes as replayable cassettes** — FEATURE — value 4 — effort L — risk med — category: reliability
  Why: a lost race is only explained from memory. Recorded tool calls and results would let `fm lane replay` rerun a lane offline to find where it diverged. Assumption: lane transcripts are capturable.
  Done when: replaying a recorded lane reproduces its final diff without a model call, or names the first diverging call.

- **Keep per-archetype win ratings for approaches** — FEATURE — value 3 — effort M — risk low — category: learning
  Why: Mission 8 learns from outcomes at the task level. "Add a flag", "refactor first" and "new module" each have a win rate by task type, which gives the planner priors, and the race would be the evidence source.
  Done when: `fm triggers` or its sibling lists approach archetypes with races, wins and surprises, and the plan gate reads them.

- **Race the same task across different runners** — FEATURE — value 3 — effort L — risk med — category: diversity
  Why: T-0335 and T-0336 are blocked on Codex, Gemini and opencode. Different model families fail differently, so a cross-runner race is the cheapest decorrelation (assumption: `fm agents` works live).
  Done when: one task runs on two runners, and the verdict records which runner's candidate merged.

- **Wild: Pick the probe that kills the most readings** — FEATURE — value 4 — effort L — risk med — category: planning
  Why: wild. Treat the request's readings as hypotheses and choose the cheap command (a grep, a dry run) that best splits them, like Mastermind. Intake then eliminates readings by running probes instead of asking.
  Done when: for a vague goal with 3 readings, intake runs ≤2 probes and prunes the readings with a recorded reason.

- **Wild: Pre-race deferred tasks overnight** — FEATURE — value 4 — effort L — risk med — category: autonomy
  Why: wild. The queue holds about 30 "Later from T-07xx" deferred bundles (T-0788–T-0799). A dream shift races approaches on them in lanes and leaves unmerged branches with evidence cards for the morning.
  Done when: the user wakes to ≥1 branch with a card, can accept or drop it with one word, and nothing has touched main.

- **Wild: Autopsy each decision a week later** — FEATURE — value 4 — effort M — risk low — category: calibration
  Why: wild. A scheduled routine (T-0793) rereads a closed task's chosen approach against what happened: reverts, re-fixes, tripwire hits. It then scores the confidence stated at the time.
  Done when: seven days after a close, a one-line verdict ("held", "re-fixed in T-NNNN", "reverted") appears on the task and feeds the calibration ledger.

Next question: Which race verdicts did the user later overrule, and what did the lane that lost have that the evidence couldn't see?
Next question: What does a lane's verify cost versus the cost of the mistakes it catches, and where does racing stop paying for itself?
