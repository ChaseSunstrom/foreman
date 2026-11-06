# Brainstorm — lens: performance

- **Split hook hot paths from CLI-only modules** — PERFORMANCE — value 4 — effort M — risk low
  Why: ~6,700 lines of stdlib Python start on every hook, and p95 is already 40–49 ms of a 150 ms budget. Assumption: hooks import fmcore and friends eagerly, including fmdoctor, fmtidy, fmdocs and fmplugins.
  Done when: `python -X importtime` on a PreToolUse run shows none of those CLI-only modules loading, and the measured p95 drops.

- **Add a hook latency regression test** — PERFORMANCE — value 4 — effort S — risk low
  Why: the p95 numbers are measured by hand, and every round adds behaviour to hooks (sync, guard categories, ask). Assumption: no test currently enforces the budget.
  Done when: a test runs each hook event 50 times against a fixture state with 100 tasks and fails if p95 exceeds 100 ms. `fm doctor` reports the same figure.

- **Give the guard a fast path** — PERFORMANCE — value 3 — effort M — risk med
  Why: the guard runs on every tool call, and its text heuristics are the most complex hook logic. Non-Bash tools, and Bash commands with no shell metacharacters or protected-path tokens, could skip most of it. The risk is skipping a check that mattered, so the guard's existing adversarial tests must pass unchanged.
  Done when: regexes are compiled once at import, the fast path skips the full heuristic for a plain `Read` or `ls`, and the guard test suite passes with no verdict changes.

- **Ingest reviewer output with `fm audit ingest`** — PERFORMANCE — value 4 — effort M — risk low
  Why: reviewer output files are huge and the agent hand-saves the tail. That burns context and time on every round. Streaming the file and extracting only the findings section is cheaper and less error-prone.
  Done when: ingesting a 5 MB reviewer file stores at most 2 KB of findings in under 200 ms, and the audit display shows them.

- **Detect sync changes by stat before hashing** — PERFORMANCE — value 3 — effort S — risk low
  Why: fmsync imports before every `fm` command using hash-based change detection. Assumption: it reads every mirrored file each time. An (mtime, size) cache would skip the hash for unchanged files.
  Done when: with 500 unchanged `.foreman/` files, an added `fm status` reads no file contents and costs under 10 ms. Touching or editing a file is still detected.

- **Cache statusline output by state fingerprint** — PERFORMANCE — value 3 — effort S — risk low
  Why: the statusline wrapper runs on every prompt refresh, and Foreman's statusline is one of its most frequent processes. Assumption: it re-reads and re-parses state each time.
  Done when: a second render with unchanged state mtimes skips parsing, and p95 is under 20 ms. A state write invalidates the cache.

- **Run independent `fm check` gates in parallel and reuse verdicts** — PERFORMANCE — value 3 — effort M — risk med
  Why: `fm check` runs project gates serially, and a masked failing suite was a past problem, so correctness matters. Audit freshness already uses a worktree id, so a verdict for an unchanged worktree can be reused.
  Done when: three independent 1 s gates finish in about 1 s wall time, and a repeat run on an unchanged worktree returns the cached verdict. Any gate failure still fails the check and appears in the output.
