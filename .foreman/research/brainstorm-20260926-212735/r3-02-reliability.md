# Brainstorm — lens: reliability

- **Reconcile `--affected` against a full run** — FIX — value 5 — effort M — risk low
  Why: `fm check --affected` runs only tests linked to changed files, so a wrong test↔source link means a silent green.
  Mechanism: at `fm task done`, and on a sampled 1-in-N basis for S tasks, run the full suite once. If it fails where affected passed, record a "map miss" (file→test) in state, add the link to `fm map`, and warn once.
  Done when: a fixture repo with an unlinked failing test produces a recorded miss, and the next `--affected` run includes that test.

- **Sandbox verify commands** — FIX — value 4 — effort M — risk med
  Why: hooks, `fm check` and `fm run` all execute criterion verify commands. A hung or tree-mutating command stalls the Stop gate, and nothing in the pack limits that.
  Mechanism: run each verify command with a per-command timeout in its own process group, killing the whole group on expiry. Snapshot `git status --porcelain` before and after, and report unexpected tree changes as "verify has side effects".
  Done when: a `sleep 999` verify is killed at the timeout and reported as such, and a verify that writes a tracked file is flagged.

- **Keep hook latency independent of history** — PERFORMANCE — value 4 — effort M — risk low
  Why: the hook budget is ~30 ms p50, but state (briefs, logs, recall index) only grows.
  Mechanism: `fm` maintains a small `hot.json` (active task, step, queue heads, inbox count, last Next) rewritten atomically on every state change. Hooks read only that file, and bulk state loads only in `fm` commands.
  Done when: a test with 5,000 finished briefs shows hook p95 within 20% of an empty project, and hooks never open `briefs/*`.

- **Add scenario tests that replay recorded hook traces** — FEATURE — value 4 — effort M — risk low
  Why: 435 tests are probably unit-level. Regressions in hook sequencing (focus → edit → done → Stop drive) or compaction restore would slip past them.
  Mechanism: `fm hook` optionally appends a bounded, redacted trace of payload and output pairs. A `tests/scenarios/` runner replays traces against a temp state dir and diffs the outputs. `fm doctor` can promote a failing trace into a fixture.
  Done when: a trace covering a full FIX task replays green, and deliberately breaking the Stop gate fails it.

- **Put an environment fingerprint in the cached-pass key** — FIX — value 3 — effort S — risk low
  Why: cached passes on an identical tree ignore toolchain drift such as interpreter version, lockfile hash, or gate-relevant env vars.
  Mechanism: hash the tool versions from `fm map`'s gate commands, the lockfiles, and an allowlist of env vars into the cache key. On a fingerprint change, print "cache skipped: env changed".
  Done when: changing a lockfile or Python version invalidates the cache with that message, and an identical environment still hits it.

- **Demote stale recall hits** — FIX — value 3 — effort M — risk low
  Why: recall surfaces past lessons and decisions into a "Related" section. Entries that cite deleted files, or decisions since reversed, mislead at focus.
  Mechanism: at index time, extract path mentions and check they exist. Cross-check reversal tracking, and multiply the BM25 score by a staleness factor. Mark the hit "(stale: path gone)" rather than hiding it.
  Done when: a lesson citing a deleted file ranks below an equivalent live one and carries the stale tag.

- **Keep a per-test flake ledger** — FEATURE — value 3 — effort S — risk low
  Why: `fm check` already reruns flaky failures and labels pre-existing ones, but that knowledge isn't kept, so the same flake gets re-diagnosed.
  Mechanism: record (test id, pass-on-rerun) counts in state. Tests above a threshold get a "known flaky" label in gate output. Past a higher threshold, queue a CLEAN task to fix them. A flaky-only failure never counts as a red→green proof.
  Done when: a test that fails once then passes 3 times is labelled known-flaky on the next run, and the CLEAN task appears at the higher threshold.

- **Record exit status and cwd with auto-captured evidence** — SECURITY — value 3 — effort S — risk low
  Why: PostToolUse auto-records evidence when a Bash run matches a criterion's verify command exactly. Nothing in the pack says it checks that the run exited 0 in the project root.
  Done when: assumption (unverified in the pack) that only the command text is matched. Evidence from a non-zero exit, a different cwd, or a `cmd || true` wrapper is rejected with a reason, and a test covers each.
