# Brainstorm — lens: performance

- **Digest reviewer output on ingest** — PERFORMANCE — value 5 — effort M — risk low
  Why: reviewer output files are huge and the agent saves the tail by hand each round, which wastes context tokens and invites mistakes. Ties into T-0034's structured findings file.
  Done when: `fm audit ingest <file>` stores a findings digest (severity, location, claim) under a size cap, and a 200 KB fixture yields ≤ 8 KB in `fm audit show`, with the full file kept only under `local/`.

- **Add a hook latency and import-time regression test** — PERFORMANCE — value 4 — effort S — risk low
  Why: the 41 → 29 ms win in round 6 is protected only by a doctor measurement, not by a test. Any new import in fmcore or fmhooks can quietly undo it.
  Done when: a test runs each hook event 20 times on a fixture repo and fails if p95 exceeds a set ceiling (e.g. 60 ms), and prints the top `-X importtime` modules on failure.

- **Load only the modules each hook event needs** — PERFORMANCE — value 3 — effort M — risk med
  Why: the p50 is dominated by interpreter start plus imports. Assumption: PostToolUse and Notification still import fmcore paths they don't use (doctor, plugins, docs).
  Done when: a test asserts that `sys.modules` after a PostToolUse run contains none of fmdoctor, fmplugins, fmideas, fmserve, fmtidy or fmdocs, and p50 drops or stays equal.

- **Short-circuit the sync pre-import with stat checks** — PERFORMANCE — value 3 — effort S — risk low
  Why: fm sync imports before each fm command and detects changes by hash. Assumption: it reads and hashes every file under `.foreman/` each time.
  Done when: with an unchanged `.foreman/` (mtime and size match the cached index), an `fm status` call opens no synced file for reading (verified by a test counting `open` calls), and it still detects an edit that changes the content but not the size.

- **Give the guard a proven-equivalent fast path for read-only commands** — PERFORMANCE — value 3 — effort M — risk med
  Why: PreToolUse runs on every Bash call, and its text heuristics run on every command even for `ls`, `git status` or `cat`. Risk is security drift, so equivalence must be proven.
  Done when: a corpus test of at least 500 commands, including the existing adversarial cases, shows fast-path and full-path verdicts are identical, and the fast path skips the regex passes for the plain read-only forms.

- **Add `fm audit wait` so reviewers don't cost idle turns** — PERFORMANCE — value 4 — effort M — risk med
  Why: background reviewers make the agent idle-wait, and the Stop hook drives continuation. Each empty turn spends tokens and time.
  Done when: `fm audit wait` blocks with low-cost polling until the findings files exist or a timeout passes, and it exits with a compact status. A test with a fake reviewer shows it returns within 1 s of the file appearing.

- **Measure always-on injected context and enforce a byte budget** — PERFORMANCE — value 3 — effort S — risk low
  Why: the rules file is 60 lines and near budget, and SessionStart and UserPromptSubmit inject text on every session and prompt.
  Done when: `fm doctor` reports bytes injected per event, and a test fails if the total for SessionStart plus one UserPromptSubmit exceeds the budget (the specific figure is an assumption to set).

- **Speed up the 389-test suite** — PERFORMANCE — value 3 — effort M — risk low
  Why: every round re-runs the full suite after each audit fix, so suite time multiplies the round cost. Assumption: much of the time goes to subprocess spawns and per-test fixture repos.
  Done when: the full suite runs at least 40% faster than the recorded baseline, with the same 389 passing, using shared read-only fixtures and in-process calls where the subprocess isn't the thing under test.
