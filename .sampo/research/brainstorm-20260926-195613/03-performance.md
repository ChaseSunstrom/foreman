# Brainstorm — lens: performance

- **Cache an incremental project map for grounding** — PERFORMANCE — value 5 — effort M — risk med
  Why: every intake re-reads the code from scratch, and no per-project map exists. Store `map.json` (entry points, test commands, module ownership, hot files) in the project state dir. Key it on file mtimes or git tree hash, refresh only changed paths, and have `fm focus` and planning read it.
  Done when: a second intake on an unchanged repo makes zero repo-wide scans, and after one edited file only that file is rescanned (test with a call counter).

- **Index decisions, research and archived briefs for sub-30 ms recall** — FEATURE — value 5 — effort M — risk med
  Why: decisions.md and research/ are never surfaced automatically. Build a stdlib inverted index (token to doc ids) updated by `fm` on every write. UserPromptSubmit looks up the request terms and injects at most one ≤120-char pointer inside the 400-char per-turn note.
  Done when: a fixture request that matches an earlier decision gets the pointer, and the lookup p95 is under 20 ms on 500 docs.

- **Run only impacted tests per step, full suite at done** — PERFORMANCE — value 4 — effort M — risk med
  Why: `fm check` runs every gate and has no test-to-file mapping. Derive the mapping from import and name heuristics, refined by which tests failed or changed together in the ledger. Add `fm check --impacted`. `fm task done` still requires the full run.
  Done when: on a fixture repo, a one-file change runs a strict subset of tests, and `done` refuses without a recorded full pass.

- **Order and time verify commands, and retry-once flaky failures** — PERFORMANCE — value 3 — effort S — risk low
  Why: nothing tracks check duration or flakiness. Record duration and outcome per check in ledger.jsonl. Run fast, historically failing checks first and fail fast. Rerun a failure once, and mark a fail-then-pass as "flaky" evidence instead of a plain pass.
  Done when: a test double that fails once then passes is recorded as flaky, and the check order follows the recorded stats.

- **Calibrate tier and effort from the ledger** — FEATURE — value 4 — effort M — risk low
  Why: `guess_tier` is a regex plus a length check and ignores real outcomes. Record steps, attempts, files touched and wall time at `task done`. Predict tier by nearest neighbour over the project's own past tasks, and fall back to the regex when there are fewer than 5.
  Done when: a replay over ledger fixtures gives a lower tier-misclassification rate than the regex baseline, and there is a test for the fallback.

- **Route `fm run` tasks to models by tier** — PERFORMANCE — value 3 — effort S — risk med
  Why: there is no model or cost routing, and every headless task uses the same session settings. `fm run` passes `--model` and effort by task type and tier (S CLEAN on a small model, L on the deepest). Log tokens and time per task.
  Done when: the `claude -p` argv differs by tier in unit tests, `claude plugin eval` still passes 5/5, and cost per task appears in the ledger. Assumption: `claude -p` reports usage in a parseable form.

- **Add a hook-latency benchmark and mtime-keyed state cache to `fm doctor`** — PERFORMANCE — value 3 — effort S — risk low
  Why: the 30 ms p50 and 150 ms p95 budgets are stated, but nothing in the pack shows they are measured continuously. Assumption: hooks reparse state files on every call. Cache parsed briefs and meta by mtime, and have `fm doctor` time each hook against a synthetic large project.
  Done when: `fm doctor` prints p50/p95 per hook, fails above budget, and the cache is verified by an invalidation test.
