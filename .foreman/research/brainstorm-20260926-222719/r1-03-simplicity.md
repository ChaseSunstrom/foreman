# Brainstorm — lens: simplicity

Most remaining simplicity ideas are already on the list. These six are the ones I think add something, and four of them remove or reduce things rather than add them.

- **Put new gates on an advisory-to-blocking ladder** — CLEAN — value 4 — effort M — risk low
  Why: the candidate added roughly 15 done-time checks (scope drift, behaviour lock, before/after numbers, verify lint, and others) in one session with no evidence yet that any of them catches anything. "Gate-yield ledger" only demotes gates after the fact. Assumption: every check can emit a one-line advisory instead of a refusal.
  Done when: each new gate starts advisory and is promoted to blocking only after N recorded catches with no waived false positives. A test shows `fm task done` prints an advisory line without refusing for a gate with zero catches.

- **Fold every ledger into one typed event log** — CLEAN — value 4 — effort L — risk med
  Why: the ideas so far propose many separate stores: flake ledger, assumptions ledger, gate-yield ledger, guard-denial log, skip log, lens yield, lesson hit counts, usage, cost, corrections. Each one adds a file format, a writer and a reader. Assumption: state today is spread over per-purpose files.
  Done when: one append-only `events.jsonl` per project with a `kind` field feeds `fm cost`, `fm usage`, `fm digest`, and the flake and gate-yield views, and the per-purpose writers are deleted.

- **Measure ceremony on canonical tasks as a test** — PERFORMANCE — value 4 — effort S — risk low
  Why: the user burned 20% of weekly usage in one session. The complexity ratchet caps Foreman's own size but not what a task costs. Assumption: a scripted replay of hook events can count `fm` calls and injected characters.
  Done when: a test replays a trivial S FIX and a typical M FEATURE against a fixture repo, and fails if `fm` calls or injected characters exceed a stored budget.

- **Default the verify command from the project map** — FEATURE — value 3 — effort S — risk low
  Why: the plan writes bespoke verify commands per criterion, then the lint checks them for being off PATH, unable to fail, or hiding an exit code. The map already knows the gates and the test↔source links. Assumption: most criteria can be checked with `fm check --affected`.
  Done when: a criterion with no `verify:` line resolves to `fm check --affected`, and a plan with only such criteria passes the focus gate and the verify lint.

- **Key gates on a declared proof kind, not the task type** — CLEAN — value 3 — effort M — risk med
  Why: `done` now branches on FIX, CLEAN, PERFORMANCE and SECURITY, and each type's special check is its own code path. Assumption: the checks are separable from the type.
  Done when: the brief carries `proof: red-green | behaviour-lock | before-after | none`, defaulted from the type. `fm gates` reads a single table, and adding a new proof kind touches one entry.

- **Make `fm task done` choose the S fast path itself** — CLEAN — value 2 — effort S — risk low
  Why: `fm task finish` and `fm task done` are two verbs for one intent, and the model must pick correctly. Assumption: tier S is reliably known at done time.
  Done when: `done` on an S task does exactly what `finish` does, `finish` is a deprecated alias, and the rules and skills no longer mention it.

Beyond these, I expect additional ideas to be marginal. The higher-value step is to consolidate and measure what is already built before adding more.
