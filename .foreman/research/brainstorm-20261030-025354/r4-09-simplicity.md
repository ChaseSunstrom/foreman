# Brainstorm — lens: simplicity

- **Ship the 15-line plain-Claude hunt prompt as `fm find` v0** — FEATURE — value 5 — effort S — risk low — category: initiative core
  Why: plain Claude found 3/3 and fixed 3/3 at about 0.17 USD, while Foreman's finders found 0 of 108. A prompt file plus one `claude -p` call is the least that can beat that.
  Done when: on the held-out exam's `bug` and `none` kinds, `fm find` scores at least the plain-Claude arm and spends no more than 0.25 USD per repo.

- **Let the model write the test before any prose** — FEATURE — value 5 — effort S — risk low — category: proof
  Why: assumption: a bug description written first anchors the model and leads to hand-waved findings. The prompt says "write a test you believe fails". If it passes on the untouched tree, the candidate is discarded silently, and the description is generated only after the test is red.
  Done when: no finding in the ledger has a description whose test was green on the untouched tree.

- **Give `fm find` a three-value exit code** — CLEAN — value 4 — effort S — risk low — category: contract
  Why: the exam harness, the night job and the user all need the same answer. 0 means clean, 1 means a proven finding, 2 means cannot prove here (no runnable test command). One contract replaces per-caller parsing and makes "none" a normal result.
  Done when: tests assert the exit code for a planted-bug repo, a clean repo and a repo with no test runner.

- **Order candidates by time-to-red, not by value** — PERFORMANCE — value 4 — effort S — risk low — category: ranking
  Why: the pack shows a heavy ranking apparatus and zero proven findings. Running the cheapest-to-prove candidates first yields a proof within minutes, and value (touch count from `fm map`) breaks ties. Assumption: early proofs matter more than perfect order.
  Done when: on a fixture with three candidates, the one with the fastest test runs first, and the receipt shows seconds-to-first-proof.

- **Store a finding as a branch, not a ledger row** — CLEAN — value 4 — effort M — risk med — category: state
  Why: `find/<slug>` holds one commit with the failing test, and the fix is the second commit. `git branch --list 'find/*'` is the whole state, and landing or dropping is a merge or a branch delete. This removes a new store, a check verb and drift against the backlog. Assumption: users will accept git as the UI.
  Done when: a killed hunt resumes from `git branch` alone, and dropping a finding deletes exactly one branch.

- **Keep dismissals in git notes** — CLEAN — value 3 — effort S — risk low — category: memory
  Why: settled findings must not return, but a new file is another thing to sync. A note on the test's blob hash survives rebases and travels with the repo. It is gone when the file changes, which is the right expiry.
  Done when: a dismissed finding is not re-filed on the next hunt and is re-filed after its file changes.

- **Run initiative one lane at a time** — CLEAN — value 3 — effort S — risk low — category: lanes
  Why: `PARALLEL_MAX 3` buys speed that unasked work doesn't need, and parallel lanes bring collision, disk and review-pile problems. A serial initiative lane is simpler to reason about, cap and kill.
  Done when: initiative jobs never hold more than one lane, and a test shows a second `fm find` waiting.

- **Gate scout probes on "is this Foreman's project"** — FIX — value 4 — effort S — risk low — category: scout
  Why: the pack notes `probe_doctor` may queue Foreman setup failures in user projects. One `if` at the probe registry stops it, with no new taxonomy.
  Done when: scout run in a non-Foreman fixture never emits a doctor-derived task.

- **Cap the whole initiative module at 300 lines, enforced by a test** — CLEAN — value 3 — effort S — risk low — category: budget (wild)
  Why: wild. Foreman has 2008 files and 29-plus deferred "later" items, and simplicity rarely survives. A line-count test makes any addition prove it deserves the space.
  Done when: `fmfind.py` fails the suite at 301 lines.

- **Ablate the pipeline one stage at a time** — PERFORMANCE — value 4 — effort M — risk low — category: exam
  Why: wild. Every extra stage (refuter, ranker, scout probes, deterministic finders) must move the exam score. Nightly, drop one stage and rerun, and a stage that changes nothing is a delete task filed automatically.
  Done when: a report lists each stage with its score delta, and at least one zero-delta stage is flagged.

- **Write tests from signatures and docstrings only** — FEATURE — value 4 — effort M — risk med — category: bug finding
  Why: wild. The model sees the signature and docs but not the body, writes tests from the spec, and a failure shows the code diverging from its documented contract. This avoids the model rationalizing the implementation. Assumption: docstrings exist in most exam repos.
  Done when: on planted bugs in documented functions, this mode finds at least one the full-source mode missed.

- **Emit the fix as a patch file when called by the exam** — FEATURE — value 3 — effort S — risk low — category: harness
  Why: Mission 3 is graded on never-seen repos, so lanes and worktrees are overhead there. `--patch` writes one diff plus the test, and the exam applies it and runs hidden keys.
  Done when: `fm find --patch` on an exam repo produces a diff that applies cleanly and the key test turns green.

- **Print "nothing proven in N files, $X" as the whole clean receipt** — FEATURE — value 3 — effort S — risk low — category: none verdict
  Why: the exam grades `none`, so the clean answer must be cheap and unambiguous. One line, with files read and cost, and no ceremony.
  Done when: a clean fixture prints exactly one line and exits 0.

Next question: Which of Foreman's existing finders and ranking stages would survive an ablation, and has anyone run that experiment on the exam?
Next question: What is the cheapest model and prompt that still holds the plain-Claude arm's score on `none` repos?
