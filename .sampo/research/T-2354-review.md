**Verdict: changes needed.** I could not run anything (read-only), so these are from reading the code.

## lens: adversary
- HIGH — plugin/lib/fmlanes.py:420-429, 520-530 (test at plugin/tests/test_lanes.py:865-879) — A live builder can lose its worktree.
  - `builder_proc` is the main session's, so it is always "alive". For `lane_conflict` or `merge_refused`, `stop_causes` reports a cause at once, and `recover` accepts any lane with no file newer than the marker plus 2 s.
  - The conflict brief (fmlanes.py:1192) tells the main thread to SendMessage the builder. A resumed builder spends its first minutes reading, with no edit yet.
  - In full autonomy, `fm next` and the Stop drive then say "Recover now, no need to ask". `recover` passes the "no work since" test, commits a WIP, unlocks the worktree and removes it under the running builder. It then launches a second builder on the same branch.
  - Committed and WIP files survive, since `worktree remove` without `--force` fails on a dirty tree. But the live builder's cwd is gone, and its absolute-path writes recreate orphan directories. The test at 865-879 asserts this "quiet, so take it back" behaviour.
  - Fix: for an alive builder, count conflict and red as causes only once the marker is at least `_stall_limit()` minutes old with no lane work since. Put that check in `stop_causes`, so `fm next` never orders recovery earlier.
- MEDIUM — fmlanes.py:506-515 — The cap check comes before the live-builder guards (lines 517-529). With two recoveries spent, `recover` on a conflicted lane that is alive and being worked sets the task `blocked` under a running builder. Fix: move the block after the guards, or apply the same quiet check first.

## lens: edge
- MEDIUM — fmhooks.py:3923-3925 — `d["recover"]` is never cleared once the causes vanish. A lane recovered in this session that stops again with the same cause gives the same key, so the drive stays silent on the second stop, and the third-stop block is never driven. Fix: `else: d.pop("recover", None)` when `recovery` is empty.
- MEDIUM — fmlanes.py:1129, 426-427 — A guard refusal (`merge_refused`, reason "guard: …") is classed `red_after_merge`. It needs a grant, not a rebuild, yet the builder is told "Fix it, re-run every criterion". Two wasted builders per lane in full autonomy. Fix: exclude reasons starting `guard:` from `_marker`, or give them their own cause that names the grant.
- LOW — fmlanes.py:385, 522 — `ledger_tail(500)` can drop the marker. Then `at is None` makes `recover` refuse, and a stopped lane reads as "uncommitted". Fix: widen the tail or store the marker on the brief.
- LOW — fmlanes.py:588 — `_ignored()` refuses `recover` (nothing removed), while `fm next` keeps saying "Recover now" and the error points to `resume --force`. Fix: say so in `recovery_line`, or skip the line for that lane.
- LOW — fmlanes.py:443-445 — The recovery count is lifetime. After a person unblocks a task, its next stop blocks it again at once.

## lens: operator
- LOW — fmlanes.py:433-434 vs fmcore.py:3469-3489 — `stop_causes` calls `finished_lanes` on a subset of briefs, while `awaiting_merge` calls it on all of them. The cache key (`finished.json`) differs whenever an unknown-process lane exists, so the two callers overwrite each other's cache. Each prompt and Stop then repeats about 4 git calls per stopped lane, 2-3 times over. Fix: pass the full list and filter afterwards.
- LOW — fmlanes.py:457 — `recoveries()` scans the whole ledger and archives once per cause per prompt. Today that is about 1.5k lines, so it is cheap; it grows without bound. Fix: count with `ledger_tail` or keep a counter in the brief meta.
- The drive messages once per cause set, so there is no endless nag apart from the key bug above. `fm next` repeats each prompt, which is intended.

## lens: intent
- AC1 (table plus a test per cause): met (test_lanes.py:747).
- AC2 (resume only after the process ended; a stalled live builder never forced): met for stalled and plain-alive lanes (tests 840 and 849). Not met for the conflict and red cases, which resume over a live builder.
- AC3 (`fm next` in full autonomy, drive once, old notes gone): met. The old strings no longer appear; the drive repeat is broken as above.
- AC4 (two recoveries, then a block with the cause and both attempts): met (test 915).

## lens: maintainer
- No further findings. The cause table is clear.

**Implicit decisions**
- "Alive" means the main session is alive.
- The "no work since" margin is 2 s on `ls-files -co` mtimes and `%ct`.
- A spent 5-hour or weekly window reads as "usage limit".
- The recovery cap counts events over the task's whole life.
- `fm lane rm` and `fm lane merge` are left to the model.

**Not checked:** I ran no tests. I did not read delegate.md, MASTER.md or the CHANGELOG. I did not measure real `proc_state` or `/proc` cost.

**Noticed:** `fm task unblock` should reset a lane's recovery count.
