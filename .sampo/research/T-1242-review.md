**Verdict: changes needed.** The acceptance criterion's published result is missing, and per-request passes aren't reported.

## lens: intent
- HIGH — site/data/stats.json:359 — This is the AC's "marathon pair has run and its result is on the Benchmarks page". The diff doesn't touch stats.json, whose duels are only `quality`, `hard` and `hard-haiku`. The new `_long` sections will render "Not run yet" (site/pages.py `_long`). The page also states no dollar cap. Fix: run the Haiku `long` and `marathon` duels, rerun `site/stats.py --duel long=DIR@haiku marathon=DIR@haiku`, rebuild the page and state the cap. — high
- MEDIUM — plugin/lib/fmbench.py:137 — T-1240 and the AC ask for per-request passes. `together()` keeps `requests[].tests`, but grading runs one verify command and reports only `tests: [passed, total]` plus up to 60 failed names. Nothing maps a result to a request. Fix: attribute `failed` names to `case["requests"][k]["tests"]` and report passed/total per request. — high
- MEDIUM — plugin/lib/fmhooks.py:671 — `REQUEST_HEAD.split(...)[1:]` drops any text before `## Request 1`. With "NEVER touch tests/.\n\n## Request 1 …", no task or compaction note carries that rule. Fix: prepend the preamble to each request's raw text, or queue it with the first. — high

## lens: edge
- MEDIUM — plugin/lib/fmhooks.py:678 — The "within 3.5 s of the hook's 5" budget isn't enforced. The loop checks the clock only before each `fm task new`, but each call has `timeout=3` and the focus call another 3. A start at 3.4 s can run past the 5 s hook limit. A `TimeoutExpired` exception also leaves a half-made task with no `first_brief` event. Fix: pass `timeout=max(0.5, 4.5 - elapsed)` to each call, and make the break check account for the focus call. — medium
- LOW — plugin/lib/fmhooks.py:390 — `_requests_note` caps only its own text at 6,000 characters. The SessionStart base context (queue, other notes) is added on top and the total is never checked. Claude Code saves a context over about 10 KB to a file and shows a 2 KB preview. Fix: cap = 9,500 − len(existing context). — medium
- LOW — plugin/lib/fmbench.py:162 — The substring `'"compact_boundary"' in line` also matches transcript lines that quote it. A tool result from reading fmbench.py would do it. Fix: `json.loads` each line and test `subtype == "compact_boundary"`. — medium
- LOW — plugin/lib/fmbench.py:137 — A hidden test file that fails to import yields "Ran 1 test … errors=1". The total then shrinks, so the page can show "0 of 1" against "90 of 105". Fix: use `case["tests"]` or an expected total as the denominator. — low

## lens: maintainer
- LOW — plugin/tests/test_dirty_at_focus.py:89 — `EditedUnderAnotherTask` is defined after the `if __name__ == "__main__": unittest.main()` block at :83, so it never runs when the file is run directly. Fix: move the class above the block. — high
- LOW — plugin/lib/fmbench.py:431 — `capped` is computed for the bare arm too, so a bare arm that hits the cap in a marathon duel gets `error=None` and is graded. A bare arm that hits the cap in a non-marathon duel is an error. Fix: `capped = bool(marathon and not bare and …)`. — high
- LOW — plugin/lib/fmcli.py:1327 — The T-1235 hunk and its tests are a second task bundled into this diff. They are justified by CHANGELOG and the commit message, but no step here names them. `rest` also lists every untracked file (`-uall`), so a dirty tree will print noise on each finish. — medium

## lens: adversary
No findings. Raw text comes from the user's own prompt, and the task commands use argv, not a shell. Site titles go through `esc()`.

## Acceptance criteria
- Multi-request case with forced compaction on both arms, reporting compactions and cost: met. Evidence: `together`, `--compact-at`, `Marathon` tests.
- Per-request passes: not met (see intent MEDIUM).
- Haiku marathon pair run under a stated cap with its result on the Benchmarks page: not met (stats.json has no long or marathon duel).
- Weaknesses fixed or captured: met. The hook fixes are tested.

## Implicit decisions
- `tier "?"` and id `M-<sha10>` for combined cases.
- Marathon passes are bench-only in practice, but any `FOREMAN_MARATHON` env var enables them.
- A request with step-1 evidence is auto-closed at stop.
- The session transcript is deleted after counting, unless `FOREMAN_BENCH_SESSIONS` names a folder.

## Not checked
I didn't run the tests or any benchmarks. I didn't check `c.redact` and `c.plain_lines` internals, the CHANGELOG or MASTER.md prose, or the site CSS.

**Noticed:** none
