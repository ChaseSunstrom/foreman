**Verdict:** approve with nits. I found no way to make the guard treat an outside write as inside a project, or a project or state write as outside, through a planted link in /tmp, in $TMPDIR, or as a state fallback. The state fallbacks can't turn every write into state either.

I had no shell here, so I couldn't run `git show 9854ffc4 23577904` or any tests. I reviewed the working-tree code at HEAD, plus the T-1284 diff file, reading only the hunks that belong to T-1284.

## lens: adversary
- MEDIUM — plugin/lib/fmguard.py:548 (also :471, :505) — Only the state fallbacks get the real-path treatment (:65-66). `ctx.state_dir` and `foreman_home/state` are compared as the raw strings `fmcore` returns (fmcore.py:94, 146 use `abspath`, not `realpath`). With `FOREMAN_STATE=/tmp/fm` on macOS, or `~/.claude` symlinked into a dotfiles repo, a Write to `/private/tmp/fm/tasks.json` or `~/dotfiles/claude/foreman/state/x` matches neither the path nor its `realpath` variant, so it isn't classed `state-direct`. `_is_core` already resolves `foreman_home` (:1495), so the two checks disagree. Fix: give `Ctx` the same dict.fromkeys(raw, dirname-real/leaf) treatment for `state_dir` and `foreman_home/state`. Confidence: medium. The code path is certain; whether it's exploitable depends on the layout.
- LOW — plugin/lib/fmguard.py:65-66 — Leaving the leaf unresolved is right against a planted /tmp/foreman-state-<uid> -> /. Fm itself follows a legitimately linked leaf, because `_private` and `open(marker)` use `stat` and `open`. State then lives at the link's target, and a Write straight to that target isn't `state-direct`. Fix: also add the leaf's realpath when the target passes the same test as fmcore `_private` (owned by the user, not group- or world-writable). Confidence: low.

No time-of-check/time-of-use gap I could find. `realpath(dirname)` is taken when the `Ctx` is built, and its parent is /tmp (root-owned, sticky) or the user's own $TMPDIR. Only the leaf can be planted, and it isn't followed.

## lens: intent
Not reviewed. The brief gave me the adversary lens plus a few specific questions.

## lens: edge
- LOW — plugin/tests/test_reaper.py:174-175, 263 — `@skipUnless(isdir("/proc"))` on `Sweep` makes `SweepWithoutProc` skip on macOS too, because unittest inherits `__unittest_skip__` through subclasses. On macOS the ps-path sweep never runs, and the skip text wrongly says it covers that path. Linux still exercises it, so the criterion holds. Fix: put the skip on `Sweep`'s tests, or move the shared body into a base class.

## lens: operator
- LOW — .github/workflows/test.yml:18 — The comment "not yet run green here" is stale now that macOS CI is green. Fix: update it, or drop `continue-on-error` if macOS is meant to block.

## lens: maintainer
- test_guard.py:991-1022 — The two new tests check what they claim. Without the change, the first (state fallback named through a link) fails: the fallback string isn't under `cwd`. A whole-path `realpath` of the fallback makes the second (planted leaf) fail, because the fallback becomes `/` or `work`.
- test_guard_cases.py:29-31 — The comment says the corpus "runs pinned to /tmp", but the test patches `tempdir` to /var/tmp to prove `drift` re-pins it. That is clear enough.
- test_context_tax.py:44-45 — `text.count(self.tmp)` misses the realpath form (`/private/var/…`) on macOS, so the discount can under-count there. It is never lenient on Linux.

## Acceptance criteria
- Worker judge keeps the fix through a linked temp folder: not verifiable here. The worker tests now use a portable `fix-calc`. The diff shows no change to fmcode's real-path code; those realpath calls are already in HEAD.
- Hard reset in a linked /tmp is refused: met. The state fallbacks are added at their real path (fmguard.py:65), and `classify_tree` checks each `_variants` form against them. The test at test_guard.py:991 covers it.
- Reaper interrupt counted without /proc, passing on Linux: met. `TimeoutWithoutProc` sets `fmideas.PROC` to a missing folder, `PROC` is honoured at fmideas.py:118, 126 and 170, and the `pr not in prs` filter is in the test.
- Relate's background start waited out, and SessionStart under budget with long temp paths: met by reading the tests. Not run.
- Time limit: met. test.yml:23 sets 35 minutes for the experimental macOS job.

## Implicit decisions
- Resolve `dirname` only, never the leaf.
- Keep both the raw and real forms of each fallback.
- Pin `tempfile.tempdir` to /tmp for the guard corpus.
- Use `os.kill(pid, 0)` as the "gone" test when there's no /proc.
- Set the macOS limit to 35 minutes, as the measured 1285 s of tests plus headroom.

## Not checked
Any test run, the full CHANGELOG/MASTER/README diffs, and the unrelated tasks sharing the diff file.

Noticed: fmcore.py:159-165 — `_activate_fallback` accepts a planted `/tmp/foreman-state-<uid>` link whose target is a victim-owned 0700 directory such as ~/.ssh, then copytrees state into it and chmods the copy (a theory from reading the code, not a tested exploit); worth a task.
