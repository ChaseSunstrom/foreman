# Brainstorm — lens: blind spots

Each of the 8 asks the user had to make maps to a question a brainstorm should have asked. I ask each question of the whole project below.

- **T-2691/2693:** "What is every record's full identity, and does each reader key on all of it?"
- **T-2720/2724:** "Where does a procedure's output live, and what is declared before it runs?"
- **T-2722:** "Does every rule conditioned on a state see every state the machine can emit?"
- **T-2729:** "Which two documents state the same rule, and do they agree?"
- **T-2738:** "Does a value one verb prints get accepted by the verb that takes it?"
- **T-2702 (dropped):** "Who can satisfy each clause of a Done-when?"

- **Mutate every dedupe key** — FIX — value 4 — effort M — risk low — category: reliability
  Why: T-2693 lost an earlier generation's line because a reader kept "one per run" and a shared run collided. The same class likely sits in other readers that keep one row per X.
  Done when: a test finds each reader that collapses rows and, for each, adds a twin record differing in one identity field. It fails on any reader that drops the twin, and the suite is green after fixes.

- **Draw the shared-object ownership map** — FEATURE — value 4 — effort M — risk low — category: observability
  Why: T-2691 arose because runs are graded by more than one generation. Fixtures, tower files and lane worktrees may be shared the same way (assumption).
  Done when: `fm genesis check` prints every object with more than one owner or consumer, and how each reader tells the owners apart. An undisambiguated entry is red.

- **Test that every rule's stage exists** — FIX — value 4 — effort S — risk low — category: correctness
  Why: T-2722's ship rule never fired because the tower's stage was named `genesis` and the rule only knew `idle`.
  Done when: the stage names come from one source. A test enumerates them and fails if a nudge or rule predicate names a stage the machine never emits, or if an emitted stage reaches no rule or an explicit "none".

- **Add `fm where` for every artifact** — FEATURE — value 3 — effort S — risk low — category: developer experience
  Why: T-2720 needed M-02's result moved beside its script, and T-2738's "recorded output was only its tail" shows results get lost.
  Done when: `fm where T-####` or `fm where bench/moonshot/kill_m02.py` lists the result files, ledger rows and commit that came from it. A script with no result prints "none recorded".

- **Stamp stored outputs with their original length** — FIX — value 3 — effort S — risk low — category: reliability
  Why: the recorded M-02 output was only a 301-byte tail (kill.txt), found only after a re-run.
  Done when: any stored result written from a truncated stream carries `truncated: N of M bytes` on its first line, and a test shows a clipped write gets the marker.

- **Declare the decision rule before every experiment** — FEATURE — value 3 — effort M — risk low — category: rigor
  Why: T-2724 required a "Sample" line before a run. The threshold and what each outcome triggers can still be chosen after seeing the result (assumption).
  Done when: every `bench/` kill script's docstring has `Sample`, `Pass if` and `Then` lines. A test fails a script missing any of them or whose result file predates its declaration commit.

- **Type-check printed values against the verbs that take them** — FIX — value 4 — effort M — risk low — category: developer experience
  Why: T-2738 printed ids space-separated where `fm task unblock` takes commas. The existing printed-Next-command check covers whole commands, not formats such as lists, durations and ids.
  Done when: each verb's argument types come from the parser. A test feeds every printed id list, duration and path from fixture outputs into the parser of each verb taking that type, and none are refused.

- **Find rules stated in two documents** — CLEAN — value 3 — effort M — risk low — category: docs
  Why: T-2729 found the seed's selection rule contradicting gen-0 §3 on #13, and neither check caught it.
  Done when: a zero-token pass extracts ordered or numeric claims (generation numbers, caps, order of missions) from gen-0, seeds, MASTER.md and site text, groups them by subject, and lists disagreements. A planted contradiction is caught.

- **Split a Done-when by who can satisfy each clause** — FEATURE — value 4 — effort M — risk med — category: planning
  Why: T-2702's criterion 3 bundled a user-held deletion and couldn't be edited after a failing run, so the whole brief was dropped.
  Done when: filing tags each clause `agent` or `user`. A brief with a `user` clause is split into a task and a waiting item, and a test shows a mixed brief files as two.

- **Plant a contradiction between two documents (wild)** — FEATURE — value 3 — effort M — risk low — category: observability
  Why: assumption: blind spots in prose are only found when someone trips on them.
  Done when: weekly, a child edits one sentence in a scratch copy to contradict another document, and the log shows whether any check noticed it and after how many days.

- **Replay the user's last 8 missed asks as a bank (wild)** — FEATURE — value 3 — effort S — risk low — category: brainstorming
  Why: the pack lists them but no later brainstorm is scored against them.
  Done when: before each slate is shown, a tool-less child gets the pack without the last 8 missed asks, and the report says how many its slate predicted.

- **Show a shelf of what the machine never reads (wild)** — FEATURE — value 3 — effort M — risk low — category: observability
  Why: every miss above was a field, stage or key some reader ignored.
  Done when: `fm doctor --unread` lists record fields, stages and keys written but read by no gauge or rule, and each entry names the reader that would first need it.

Next question: which readers in the project pick "the latest" or "the first" row of a group, and what makes that row the right one?
Next question: of the printed numbers and ids Foreman shows, which has the user copied by hand into another command, and did it work?
