# Brainstorm — lens: bold bets

- **Auto-recall on intake: surface related past work at the moment of planning** — FEATURE — value 5 — effort M — risk low
  Why: decisions.md, research/ and archived briefs are never surfaced when a related request arrives; lessons only exist if reflect is run by hand.
  Done when: `fm recall "<request>"` (stdlib TF-IDF over archived briefs, decisions, research, audit findings) returns the top 3 hits with one-line reasons, intake calls it before planning, and a test seeded with a past decision on "login timeout" shows it appears in the new brief's evidence.

- **Build a living project map for grounding and impact analysis** — FEATURE — value 5 — effort L — risk med
  Why: every intake re-reads code from scratch; no entry points, test commands, module ownership, hot files, or "what calls this / which tests cover it".
  Done when: `fm map` writes map.json (test commands, import graph by regex/AST for Python and simple patterns for others, git-churn hot files, conventions), refreshes incrementally on PostToolUse edits, and `fm impact <file>` lists dependents and likely covering tests; intake's Ground step cites it; a fixture repo yields correct dependents.

- **Learn tier and effort from outcomes (calibration ledger)** — FEATURE — value 4 — effort M — risk low
  Why: `guess_tier` is a regex plus a length check; the ledger already records steps, attempts and files but nothing feeds back.
  Done when: on `task done`, actual steps/attempts/files/duration are logged against the predicted tier. `fm calibrate` replaces the regex with nearest-neighbour matches over past tasks. Replaying the ledger shows misclassification below the regex baseline, and the intake note says "similar tasks took N steps".

- **Map tests to files and detect weak or flaky tests during verification** — PERFORMANCE — value 4 — effort M — risk med
  Why: `fm check` runs everything; there's no coverage mapping, flake detection, or baseline comparison, and a test that passes without the change goes unnoticed.
  Done when: `fm check --affected` runs only the tests mapped to the frozen diff (mapping learned from co-failure and coverage or from the project map). `fm task evidence --red-green` stashes the change, requires the new test to fail, then restores it and requires a pass. Reruns of failures flag flaky tests in the ledger. Assumption: the project's test runner can be targeted per file.

- **Failure memory: fingerprint failures and match them against earlier fixes** — FEATURE — value 4 — effort M — risk low
  Why: three failed attempts block a task, but causes aren't collected or matched, so the same bug gets re-debugged.
  Done when: PostToolUseFailure and failed evidence store a normalized fingerprint (error class, top frame, command). On a repeat the per-turn note reads "seen in T-00NN, fixed by <summary>" (≤ 400 chars). A test replays two similar failures and gets the link.

- **Decision review: track whether autonomous decisions held up** — FEATURE — value 3 — effort S — risk low
  Why: in full autonomy Claude records a default and nothing revisits it. Assumption: reversals show up as later edits to the same files or as a contradicting decision.
  Done when: each decision gets scope globs and a review trigger. `fm decisions audit` flags entries whose files were later changed by an unrelated task or that were superseded. The SessionStart line shows "N decisions to re-check", and a test flags a seeded reversed decision.

- **Cross-project lessons: promote proven lessons to a global playbook** — FEATURE — value 3 — effort M — risk med
  Why: each project's learning is siloed and reflect is manual.
  Done when: `fm lessons promote` copies lessons tagged general (stack, tool, process) with provenance to ~/.claude/foreman/lessons.jsonl. Intake in another repo with a matching stack retrieves them through `fm recall`, and uninstall removes the file. Assumption: lessons carry stack tags or can be derived from the file extensions in scope.

- **Escalate hints into gates for the highest-value procedures, and route effort by step** — FEATURE — value 3 — effort M — risk med
  Why: "Next" is only a hint; Claude can skip a regression test or approach comparison, and subagent types are fixed.
  Done when: a step flagged `hard` in the brief causes the note to recommend a deeper-reasoning subagent, and a step flagged `mechanical` recommends a cheaper one. Stop-hook checks that a FIX task has a red-then-green evidence pair before completion. A test shows a FIX with no red evidence is refused and evals stay 5/5.
