**Verdict:** changes needed. The sweep never runs in a default project (finding 1), and its GitHub path has several failure modes (findings 2–5).

## lens: intent / operator / edge / adversary / maintainer

- HIGH — plugin/lib/fmcost.py:458 and plugin/lib/fmforesight.py:86 — The sweep only runs inside `fm cost --refresh-cache`. The only spawner is `_refresh_detached`, which is reached only through `cached_costs(refresh=True)`. Its callers are `check_cap` for a task with a `cost_cap` (fmhooks.py:3538-3541, fmserve.py:281) and `fmcontract.over` for a contract with a tokens bound (fmcontract.py:65). A default project has neither, so nothing writes `state/foresight.json` and session start never shows CI red or a setup change. The tests call `fs.refresh` directly, so they pass anyway. Fix: spawn a detached refresh from the Stop hook (or at the end of SessionStart) with its own stamp, independent of caps and contracts. — high
- MEDIUM — plugin/lib/fmforesight.py:67-76, 94-109 — `ci_main` catches only `OSError` and `ValueError`. `http.client.HTTPException` (IncompleteRead, BadStatusLine) escapes. If `capture_once` raises, the same thing happens. `refresh` then aborts before it stores `checked` and before it writes the file. The spawn stamp allows one refresh a minute, so the GitHub call repeats every refresh (up to 60/h from one project) and exhausts the 60/h limit. Fix: catch `HTTPException`, and set `ci[p.slug]={"checked": now}` before the capture (or use try/finally). — high
- MEDIUM — plugin/lib/fmforesight.py:99-109 — When the fetch returns None (a 403 rate limit, offline), `mine` is replaced by `{"checked": ...}`. That drops the known red sha, workflows and task, so the red line vanishes from session start until the next successful fetch. Fix: keep the previous `mine` fields when `got is None`. — high
- MEDIUM — plugin/lib/fmforesight.py:88, 111 — This is an unlocked read-modify-write of one global file, with up to about 10 s of git and network work between the read and the write. Project B's write drops project A's `ci` entry or the `changed` note. Fix: fetch first, then take a lock on the state dir, re-read, merge only your own slug, and write. — high
- MEDIUM — plugin/lib/fmforesight.py:99 — Cost at scale: calls are keyed by `p.slug`, not by repo, so every clone or worktree of one repo makes its own call. At 2 calls an hour each, 30 projects reach the 60/h per-IP limit. Private repos get a 404 every time, and that counts against the limit too. Fix: key the cache and `checked` by repo. Consider `gh api` (already used by fmci.py) for authenticated, private-repo access. — medium
- MEDIUM — plugin/lib/fmforesight.py:103-105 and `lines()` — Workflow names and the sha from the API go unsanitized into the brief title and raw text, and into the SessionStart context, which is a model prompt. A workflow name containing a newline can forge `CONTEXT:` or `CI-red:` lines. An empty `head_sha` gives the key `"CI-red: "`, which matches any earlier CI-red brief and suppresses the capture. fmci.py uses `c.plain`, `defang` and `fit` on this kind of data. Fix: `c.fit(c.plain(name), 40)`, cap the list at 5, and require `re.fullmatch(r"[0-9a-f]{40}", sha)`. — medium
- LOW — plugin/lib/fmhooks.py:600-605 — One `try` now wraps `lines`, `burn_line` and `pile_lines`. A malformed cache (`ci` as a list, or `failed` without `sha`, which gives a `KeyError`) silently drops the Blocked and Tidy lines. Before this change those were outside the `try`. Fix: give `pile_lines` its own `try`. — medium
- LOW — plugin/lib/fmforesight.py:67-80 — `branch=main` is hardcoded, so a repo on `master` gets nothing and no message. `sha` is the newest run's sha, but a path-filtered workflow's newest failing run may be at an older sha, which gives a mislabelled "red at <sha>". The line "fix it first: T-x" persists after T-x is closed. — medium
- LOW — plugin/tests/test_foresight.py — `ci_main` is untested (newest per workflow, cancelled runs, HTTP failure). Nothing tests the `session_context` wiring or the `cmd_cost` `changed` path, which is what the AC means by session start. — high
- LOW — plugin/lib/fmforesight.py:9 — `import urllib.request` at module top is loaded on every SessionStart via fmhooks. Move it into `ci_main`. — medium

Your four points: (1) addressed by the cost-at-scale, failure-loop and rate-limit findings. (2) Session start does no network or slow work, only a `foresight.json` read and the `urllib` import. (3) addressed by the locking finding. (4) `capture_once` de-duplicates per project and includes the archive; the one gap is the empty-sha case above.

## Acceptance criteria
- Sweep names CI red, setup change, stale pile and tidy, each with its action, from caches only: partly met. The text and no-network-at-start parts hold, but the cache is never filled by default (finding 1).
- The reviewer multiplies cost at scale in every review: met (fm-reviewer.md rule 5a, plus the test).

## Implicit decisions
- The public unauthenticated GitHub API, 30 min per project, branch `main`.
- The latest finished run per workflow counts as red; `cancelled` is ignored.
- A setup change is shown for 3 days; "stale blocked" means 14 days.
- The only visible fields of a setup change are model, window and CC version.
- A first-seen setup counts as the baseline, not a change.

## Not checked
The CHANGELOG convention for MASTER.md, statusline and fmcost; the design lens (the statusline change adds one JSON field and no UI); the full test run.

**Noticed:** the T-1800 burn scan has the same gap, because `burn.json` is also written only from `--refresh-cache`, so it is likewise absent without a cap or contract.
