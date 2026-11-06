# Brainstorm — lens: groundbreaking: 10x, not 10%

- **Bisect the Claude Code release that broke a run** — FEATURE — value 5 — effort M — risk low — category: reliability
  Why: When a run regresses, nothing says which Claude Code release caused it. assumption: old CLI versions can be installed side by side or pinned.
  Done when: a fixture regression seeded at a known release is pinned to that release in at most 8 bench runs.

- **Delta-debug a failing run to its smallest repro** — FEATURE — value 4 — effort M — risk low — category: developer experience
  Why: A failed `fm check` reports the failing test but not the minimal input that triggers it. assumption: the failing input can be re-run cheaply.
  Done when: a fixture that fails on a 300-line file produces a repro under 20 lines that still fails when re-run.

- **Route playbooks with a local embedding model, zero network** — FEATURE — value 4 — effort M — risk med — category: privacy
  Why: The request for 10,000+ playbooks means keyword routing will miss paraphrases. assumption: a small embedding model runs on the owner's machine.
  Done when: on a 10k fixture, the top 5 contains the right playbook for at least 90% of paraphrased queries, and the routing call makes no network request.

- **Race two runners on a task and keep the first that passes the gate** — FEATURE — value 3 — effort L — risk med — category: quality
  Why: The duel against bare Claude Code is the measure, and racing two runners may lift the pass rate. assumption: a 1.3x token ceiling per task is acceptable to the user.
  Done when: on the duel fixtures, the racing pass rate beats the single-runner rate while staying under the 1.3x token cap.

- **Abort a run the moment it edits outside its task's file set** — SECURITY — value 4 — effort M — risk low — category: scope guard
  Why: The file set is recorded at plan time, but out-of-scope edits are currently seen only at close. assumption: the plan's file set is written to the journal.
  Done when: a fixture run that edits an out-of-scope file is stopped within 2 seconds, and the journal names that file.

- **Learn a codemod from one before/after edit** — FEATURE — value 4 — effort M — risk med — category: mechanical edits
  Why: Mechanical edits currently cost model tokens on every site. assumption: a rewrite rule can be generalized from a single example.
  Done when: from one example, the generated rule rewrites all 12 fixture sites and leaves the 3 decoy sites unchanged.

- **Attach each task's proof to its commit as a git note** — FEATURE — value 3 — effort S — risk low — category: auditability
  Why: Proofs live in Foreman's own store and drop out of the git history. assumption: the commit exists when the task closes.
  Done when: after `fm task close`, `git notes show <commit>` prints the proof command, its exit code and the run id.

- **Mine closed tasks into fresh regression probes** — FEATURE — value 4 — effort M — risk low — category: regression testing — wild
  Why: Every closed fix carries a real failure and its proof, which becomes a probe nobody has written yet. assumption: a closed task's failing test can be re-run standalone.
  Done when: a finished fix yields a probe that fails on the pre-fix commit and passes on the fix, with no hand-written test.

- **Pre-run the likely gates while the model is still typing** — PERFORMANCE — value 3 — effort M — risk med — category: latency — wild
  Why: Gates wait for the edit to finish, but the likely changed files are often visible early in the run. assumption: the run's edit targets can be predicted from the plan.
  Done when: on a timed fixture, the gate result arrives at least 30% sooner after the last edit, and a wrong prediction is discarded without changing the verdict.

- **Have a second model audit the rules file for contradictions** — CLEAN — value 3 — effort S — risk low — category: rules hygiene — wild
  Why: The rules file has grown past its budget, so it likely contains rules that conflict. assumption: a contradiction is detectable from the text alone.
  Done when: a planted contradiction in a fixture rules file is flagged, and the clean fixture produces no flags.

- **Learn accept and revert signals from kept and reverted diffs** — FEATURE — value 3 — effort M — risk med — category: taste
  Why: The user's pushback ("just go", "don't ask") carries preferences that the pack records only as prose. assumption: kept and reverted diffs are distinguishable in git.
  Done when: after 10 reverted diffs in one style, the next plan in that style follows the learned rule, shown by a fixture.

- **Cache model replies by pack hash across projects** — PERFORMANCE — value 4 — effort S — risk low — category: token cost
  Why: Identical packs, such as repeated lens runs and reviews, are resent to the model. assumption: the key can include the model ID and Claude Code version so stale replies never return.
  Done when: a second identical request costs zero model tokens and `fm cost` reports a cache hit.
