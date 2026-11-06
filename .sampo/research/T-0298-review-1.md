## Intent: changes needed

**Findings**

- **MEDIUM**: `fmnight.py:249-253` and `:262`. `--max-usd` is only a planning estimate, not a spend cap.
  - A job is kept if `total + est <= limit`. Each estimate is the mean of recent spend for that feature, or a fallback of 0.2, 0.05 or 0.5 USD per run when the ledger is empty (`fmbudget.py:75-80`).
  - Nothing re-checks cumulative spend between jobs or after each one. The jobs are `fm landscape`, `fm second session` and `fm bench court`, and each is only checked against its own command's estimate.
  - Court sessions run with their own `--budget`, which defaults to 3 USD per session (`fmbench.py:469`), so three cases could spend far more than the 1.5 USD the plan assumed.
  - Fix: after each job, re-read `fmbudget.spent()` and stop when the running total passes `limit`. Pass `--budget` into the court argv derived from `limit`.

- **MEDIUM**: `fmnight.py:237-242`. Usage is checked once, before any job. Jobs can run up to 3 hours each (`:264`), so usage can cross 80% mid-night.
  - `usage_high` also returns None when there is no readable snapshot or the newest one is stale (`fmbudget.py:86-101`).
  - An overnight run therefore reads a snapshot from the last interactive session and fails open.
  - Fix: call `fmbudget.usage_high()` before each job and stop the night when it returns a value. Refuse when no snapshot is newer than a few hours.

- **MEDIUM**: `fmnight.py:219-231`. `landscape` and `court` run in a sensitive project; only `second session` is gated.
  - `court_cases` (`fmbench.py:383`) turns the user's steers into bypass-mode replays and judge children. A grep of `fmbench.py` and `fmoutside.py` found no `sensitive` check in either.
  - Fix: return no jobs when `meta.get("sensitive")`, or at least drop `court`.

- **MEDIUM**: `fmbench.py:98`. Replay-controlled text becomes an inbox item that can be picked up unattended.
  - The `target` and `error` fields come from the replayed bypass-mode session's `events.jsonl`. They are cut to 100 chars, passed through `c.plain`, and written into the title and `raw` of a self item.
  - Unlike `fmsecond.py:180`, the item has no `meta["confirm"]=True`. In full autonomy `fm next` can pick it, and a model then reads the text as a task.
  - A session steered by an injected command string, for example `fm x; ignore prior and run …`, plants a 100-char instruction.
  - `c.plain` stops terminal escapes. It does not stop prompt injection.
  - Fix: pass `confirm=True` as T-0289 does. Also wrap the text in `raw` as quoted data.

- **LOW**: `fmbench.py:523` and `:68`. The preflight checks the estimate with `min(budget, 0.5)`, but the session runs with `--max-budget-usd 3` by default. The same pattern exists elsewhere, so it is not new. Stranger also doesn't check `usage_high`.

- **LOW**: `fmnight.py:247`. An unknown `--only` name is silently ignored, so the run does nothing and exits 0. Fix: reject names not in `jobs()`.

**Acceptance criteria**
- T-0244 stranger: met by test and diff (toy repo, fresh state, README only, at most five captured, deduplicated). The test uses a stub, not a real session, and covers a guard block and a failed `fm` call.
- T-0236 night:
  - Met: the dry-run lists jobs within the limit, and refuses at high usage.
  - Partly met: "within --max-usd" holds only as an estimate (finding 1).
  - Not met: the request's "bench tournaments of evolve candidates" and "research debt" jobs are absent. Only landscape, second session and court are built.
  - Digest reporting is met.
  - Never merges: met, since nothing merges.

**Not checked**: I did not run the tests. I did not read `fm bench court`'s own budget defaults, or `fmoutside.cmd_landscape` beyond the grep.
