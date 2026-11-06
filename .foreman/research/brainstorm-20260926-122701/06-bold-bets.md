# Brainstorm — lens: bold bets

- **Run lens audits as headless reviewers with structured findings** — FEATURE — value 5 — effort L — risk med
  Why: Every round, three reviewers found real bugs after the agent thought it was done. Their output files are huge and the agent saves the tail by hand. The Stop hook also leaves the agent idle-waiting on background reviewers. Bundle T-0031 (`--note`) into this.
  Done when: `fm audit run` spawns read-only lens children using the `fm run`/`fmideas` machinery. It writes a findings file (severity, file:line, lens) and `fm audit` shows the same list the done gate uses, with no hand-saved tails.

- **Fall back to the last committed guard when the working copy fails** — FIX — value 5 — effort M — risk med
  Why: T-0033: a half-applied guard edit made every write fail closed, and recovery needed an unusual command. Assumption: the committed copy can be loaded from git without a network call and inside the hook budget.
  Done when: a test that corrupts `fmguard.py` in a temp checkout still blocks dangerous commands via the committed guard. Ordinary writes are not locked out, `fm doctor` reports the fallback, and p95 stays under 150 ms.

- **Add a permanent red-team corpus for the guard** — SECURITY — value 4 — effort M — risk low
  Why: Reviewers found security bugs in rounds 1–3. The guard's text heuristics also block legitimate agent edits (quoted paths, "claude plugin" strings). Assumption: the past findings are not yet stored as regression cases.
  Done when: `tests/guard_corpus` holds allow and deny command lists. Every audit-found bypass or false positive is added as a case, and `fm check` fails if any case regresses.

- **Generate rules, eval copies and doc sections from one source** — CLEAN — value 4 — effort M — risk low
  Why: Every behaviour change touches MASTER.md, CHANGELOG, the 60-line rules file and the eval copies. That is doc-drift risk, and the rules file is near its budget.
  Done when: `fm docs build` regenerates the derived copies from a single source. `fm doctor` fails on any drift, and the rules line count is checked against its budget.

- **Turn real ledger history into eval cases** — FEATURE — value 4 — effort L — risk med
  Why: Evals are 5 cases, single runs and noisy. Rounds 1–3 produced evidence of real failures (a masked failing suite, evidence typos).
  Done when: `fm eval capture <task>` emits a redacted case, with no secrets or local paths, from a finished task's record. Cases run N times and report a pass rate. At least 3 new cases are drawn from this session's failures.

- **Show hierarchical progress for umbrella tasks** — FEATURE — value 3 — effort M — risk low
  Why: T-0018 hides per-round progress behind "step 3/6" in the statusline. T-0032 also shows there is no "done elsewhere" status.
  Done when: an umbrella task with child rounds shows "T-0018 · round 4/6 · step 2/5" in the statusline. Requests finished inside another task can be closed as `done-elsewhere`, linked to that task.

- **Scope-declared edits to relax false-positive guard blocks** — FEATURE — value 3 — effort L — risk high
  Why: The agent writes multi-line heredocs to edit files and hits the guard's heuristics on its own legitimate work. Assumption: the plan can list file scope and the guard can read it.
  Done when: within a step's declared file scope, quoted-path and string-match false positives are allowed. Protected core, remote and plugin categories stay blocked regardless of scope, and the red-team corpus still passes.
