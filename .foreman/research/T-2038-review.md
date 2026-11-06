**Verdict: approve with nits.** The acceptance tests cover the two stated behaviours: a clean, quiet lane that is ahead gets a merge line, and a dirty or fresh lane does not. I read the code but did not run the tests. The findings below are about cost and edge cases.

## lens: intent
ok. `next_for` feeds SessionStart (`fmhooks.py:608`), the per-prompt context (`:1290`) and the drive (`:3715`), so the "Active: none" case from the request is covered. `fm lane merge` uses `--no-ff` (`fmlanes.py:746`), so a merged lane stops reading as ahead and does not nag afterwards.
- LOW — plugin/lib/fmcore.py:3347 — "Finished" never checks whether the builder is still alive. A live builder that committed, then sits more than 30 minutes on a long test run with a clean tree, is named "finished, merge it". The tests only use a stopped builder (`test_lanes.py:290`). — Skip lanes that `fmbus.proc_state(builder_proc)` reports as live, or say so in the AC if the user's wording ("ahead and clean") is the intent. — confidence 70%

## lens: adversary
ok. The only inputs are git output read through `_git`, which strips `GIT_*` variables and runs with an argument list, not a shell. I found no injection or authorization path.

## lens: edge
- LOW — plugin/lib/fmcore.py:3328-3329 — When the main checkout is on a detached HEAD, `rev-parse --abbrev-ref HEAD` returns "HEAD". The lane's `rev-list HEAD --not HEAD` is then 0, so finished lanes go unnamed. This happens mid-rebase or bisect, and nothing says so. — Use the main checkout's commit SHA (`rev-parse HEAD`) as the base, which also works on a branch. — confidence 75%
- LOW — plugin/lib/fmcore.py:3332-3335 — The ahead count is against the main checkout's current branch, not the branch the lane forked from. If main is switched to a branch that lacks the lane's ancestry, the whole history reads as ahead. — Compare against the brief's recorded `base` if one exists. — confidence 50%

Timeouts fail closed: a `log` or `rev-list` timeout returns "", and a `status` timeout returns "?", so none of them reads as finished. Inside a lane, `p.lane` makes the function return [].

## lens: operator
- MEDIUM — plugin/lib/fmcore.py:3318-3336, plugin/lib/fmcli.py:5363 — There is no cache. Each `next_for` call costs one `rev-parse` plus 1 to 3 git subprocesses per lane directory (`log` always, then `rev-list`, then `status` only if the lane is ahead). The callers include every prompt (`fmhooks.py:1290`), SessionStart, each Stop (`:3715`), and the pane's `fm ui` refresh, which `register.tsx:303` ticks every 2 s. `fm next` computes it twice, once in `next_for` and again at `fmcli.py:5363`. The Stop-hook call runs under the project lock. For example, 3 lanes cost about 10 subprocesses (about 50 ms or more, since `status` runs on a full worktree) per 2 s while the pane is open. `fmlanes.stalled` caches for 60 s for this reason (`fmlanes.py:181`). — Add a similar 60 s cache file for `finished_lanes`, and have `cmd_next` reuse the result. — confidence 80%
- LOW — plugin/lib/fmhooks.py:3591 — The `d["lanes"]` format changed from `held` to `held + ["done"] + done`, so a session already running repeats the "builders hold…" notice once. — Ignore, or note in the CHANGELOG. — confidence 60%

## lens: maintainer
- LOW — plugin/tests/test_lanes.py:307-312 — There is no test for a lane that is not ahead (already merged), for `p.lane` set, for a closed task, or for a detached main. The early-return branches at `fmcore.py:3326` and the `not in ("", "0")` check are untested. — Add one test where the lane has been merged and `finished_lanes` returns []. — confidence 70%
- LOW — plugin/lib/fmcore.py:3358 — The ternary that orders the merge text before or after `action` is one dense line. — Use an if/else. — confidence 40%

## Acceptance criteria
- A clean, quiet lane ahead of main is named for merge, and a dirty or fresh one is not: met by the code (`fmcore.py:3330-3335`) and by the tests at `test_lanes.py:298` and `:322`. I did not run them.

## Implicit decisions
- The 30-minute quiet window is hard-coded, with no env override (`stalled` has `FM_STALL_MIN`).
- "Finished" means the lane has a clean tree and a quiet last commit. Builder liveness is not part of it.
- The base is the main checkout's current branch.
- The drive message is said once per set of lanes. After that, a Stop hook returns None and skips the rest of the drive logic, as the held-only case did before.
- The `fm lane resume` line is suppressed for finished lanes in `fm next` only.

## Not checked
I did not run the tests, the pane, or `fm doctor`. I did not check MASTER.md for stale wording about lane hints.

**Noticed:** `fmcli.py:5363` `cmd_next` recomputes work `next_for` already did (finished lanes), and the same duplication may exist for `stalled` and `stopped`.
