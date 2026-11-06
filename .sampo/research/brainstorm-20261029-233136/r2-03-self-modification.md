# Brainstorm — lens: self-modification

- **Calibrate the exam against outside signals** — FEATURE — value 5 — effort M — risk med — category: self-measurement
  Why: the user's standing steer is weakness-finding by outside signals only (`fm outcomes` 30-day survival, `fm second`). Selection trusts exam closure, so a self-change that raises the exam without raising real outcomes is Goodhart.
  Done when: `fm genesis calibrate` prints the correlation between exam gain and 30-day survival per self-change, and self-change promotion refuses when the correlation is below a set floor or there is too little data.

- **Stage every self-edit in a candidates sandbox** — SECURITY — value 5 — effort M — risk low — category: guard
  Why: the routing line in `rules/foreman.md` is protected core and needs "a candidate plus the user's yes". Genesis editing its own templates, lenses or selection rule should use the same path.
  Done when: Genesis cannot write to its live templates, only to `candidates/`, and a separate `fm genesis promote ID` verb (which needs the user's yes) is the only way a candidate goes live. A test shows a direct write is denied.

- **Lint self-changes for hardcoding** — CLEAN — value 4 — effort S — risk low — category: self-quality
  Why: the user steered "I don't mean to have foreman be hardcoded to that, I want foreman to just genuinely be smarter", which replaced the face/verb list with `fmmap.drift`. A self-rewriting template can slide back into enumerated project-specific literals.
  Done when: a candidate containing a literal project path, a file name or a verb list that could be derived from git history is rejected with the offending lines quoted. A fixture with the old face/verb list is rejected.

- **Mutation-test the exam generator** — FEATURE — value 4 — effort M — risk med — category: exam integrity
  Why: the oracle/empty/finders canary only shows that an exam can fail and pass. It doesn't show that the exam notices small wrong answers, and Genesis will want to edit `fm exam gen`.
  Done when: for each generated exam, N seeded off-by-one or wrong-branch bugs are applied to the oracle solution, and a mutation score is stored. An exam-generator change that lowers the score is blocked.

- **Bisect the self-change ledger on regression** — FEATURE — value 4 — effort M — risk low — category: reversibility
  Why: assumption: self-changes accumulate, and two that each pass alone can interact. A revert command alone doesn't say which change to revert.
  Done when: given a drop in the frozen mini-exam, `fm genesis bisect` replays ledger entries and names the first one that causes the drop, with no model calls beyond the exam.

- **Gate self-changes with the fixed-point test on Foreman itself** — FEATURE — value 4 — effort M — risk med — category: regression gate
  Why: Mission 2's exam says the self-written gen-0 must cover every MUST, NEVER and section of the hand-written one. Used as a gate, Genesis writing gen-0 for Foreman, the one project with a hand-written answer, scores each self-change.
  Done when: every candidate prints its coverage of gen-0's MUST/NEVER/section list, and a drop below the parent's is blocked. The check is marked as one sample, to avoid overfit.

- **Re-ablate self-changes when the model changes** — PERFORMANCE — value 4 — effort M — risk low — category: maintenance
  Why: the environment lists a new model family. Template clauses that patched an older model's habits become dead weight, or harm.
  Done when: on a model-id change, `fm genesis` queues an ablation of each ledger entry. Entries whose removal ties or wins at lower cost are proposed for retirement.

- **Give every self-change a sunset clause** — FEATURE — value 3 — effort S — risk low — category: probation
  Why: assumption: self-changes that won once on a small exam stay forever by default. Past drops show the user dislikes stale rules.
  Done when: each promoted change carries a hypothesis and an expiry. At expiry it reverts unless fresh evidence re-confirms it, and the revert is visible in `status`.

- **Stamp artifacts with the Genesis vintage** — FEATURE — value 3 — effort S — risk low — category: provenance
  Why: if a vintage turns out bad and is reverted, towers it wrote stay in other projects with no flag.
  Done when: every gen-0, spec and exam carries a vintage hash. `fm genesis revoke VINTAGE` lists and marks every tower made by it as suspect, and the site page shows the mark.

- **Limit self-change to typed mutation operators** — CLEAN — value 3 — effort M — risk low — category: attribution
  Why: assumption: free-form template rewrites can't be attributed to a cause. A fixed set (add clause, delete clause, reorder, swap lens, change threshold) makes each change testable and its payoff countable.
  Done when: the ledger records the operator for every change, and a free-form edit is refused. Win-rate per operator shows in `status`.

- **Store reverted changes as an immune memory (wild)** — FEATURE — value 3 — effort M — risk low — category: learning
  Why: wild. The not-yet ledger retries ideas, but nothing stops Genesis re-proposing a self-change that was already reverted for proven harm.
  Done when: a reverted change leaves a signature (operator, target and reason). A new candidate that matches one is auto-rejected with the quoted reason, unless it carries a new approach and new evidence.

- **Plant a honeypot to catch reward hacking (wild)** — SECURITY — value 3 — effort M — risk med — category: alignment test
  Why: wild. The main worry about a self-writing harness is that it edits the exam toward easier scenarios, and a decoy is a direct way to test whether it would.
  Done when: in a sandbox run, a tempting weakened exam file is available. If any candidate reads or edits it, the run halts and reports the attempt. Unit tests prove the tripwire fires on a scripted cheater.

- **Publish Genesis release notes on the site (wild)** — FEATURE — value 2 — effort S — risk low — category: transparency
  Why: wild. The tower page is already kept live, but nothing shows what Genesis changed about itself.
  Done when: the Genesis page has a "what Genesis changed in itself" list, each entry with its reason, its measured effect and a copyable revert command.

Next question: When an outside signal and the exam disagree about a self-change, which wins, and who decides?
Next question: What is the smallest set of Genesis parts that must never be self-edited, and how is it enforced if Genesis can write files?
