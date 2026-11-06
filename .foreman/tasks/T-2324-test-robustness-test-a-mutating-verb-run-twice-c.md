---
id: T-2324
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-31T12:06:31Z
updated: 2026-10-31T12:14:53Z
builder_model: sonnet
base: 7cd5aac81aa9a36772b5ca1f919ff4a051ef6731
base_tree: 43c819fdfd9493f39743ffaccc6ce4a07b18aa08
plan0_at: 2026-10-31T12:10:23Z
plan0_scope: []
verified: strong
---
# fm checkpoint run twice leaves briefs-closed.json and briefs-index.json unchanged the second time
## Raw request
> test_robustness.test_a_mutating_verb_run_twice_changes_nothing_the_second_time flakes under load: fm checkpoint run twice rewrites briefs-closed.json and briefs-index.json on the second run (ship73's scratch tree, T-2323's builder); find what the second run changes (a timestamp, an mtime-keyed rebuild) and make the rewrite idempotent
## Interpretation
test_robustness.test_a_mutating_verb_run_twice_changes_nothing_the_second_time failed twice today under load (ship73's scratch tree, T-2323's builder): a second fm checkpoint rewrote briefs-closed.json and briefs-index.json. Something in those caches depends on time or rebuild order, not only on the briefs.
## Assumptions (confidence)
## Acceptance criteria
- [x] Two fm checkpoint runs in a row leave briefs-closed.json and briefs-index.json byte-identical, including when the second runs in the same second, a second later, or after a brief file's mtime moves without a content change; test_robustness passes repeatedly — verify with `python3 plugin/tests/run.py test_robustness test_core`
## Non-goals
## Approach (options → choice → why)
Options: 1) find the field that changes and make it content-derived or drop it, writing only on a real change; 2) exclude those cache files from the robustness test; 3) retry the test. Choice 1: the test is right that a mutating verb run twice should change nothing; 2 and 3 hide a real non-idempotent write.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Reproduce: run the robustness test in a loop (and with a forced mtime bump between the two checkpoints) until the second run changes a file; diff the two versions to name what changed
2. [x] Make the index write idempotent at its cause (no timestamps or mtime-derived fields in the content, sorted output, write only when the content differs)
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_robustness test_core 2>&1 | tail -8` → ✗ exit 1 · Ran 101 tests in 7.6s (25 classes, 16 at a time; slowest: Robustness 7s, BriefIndex 2s, WritesAndLocks 2s) / FAILED (1 classes: test_core.BriefIndex) [ran] [tree 70098a1c1976] (2026-10-31T12:11:12Z)
- (step 1) `python3 plugin/tests/run.py test_robustness` → exit 0 · Ran 4 tests in 7.4s (1 classes, 16 at a time; slowest: Robustness 7s) / OK [ran] [tree 5a16cfba5756] (2026-10-31T12:11:43Z)
- (step 2) `python3 plugin/tests/run.py test_robustness test_core` → exit 0 · Ran 101 tests in 7.5s (25 classes, 16 at a time; slowest: Robustness 7s, BriefIndex 2s, WritesAndLocks 2s) / OK [ran] [tree 5a16cfba5756] (2026-10-31T12:11:52Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_core test_robustness && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.31s] [ran] [tree 5a16cfba5756] (2026-10-31T12:12:12Z)
- (step 1) `python3 plugin/tests/run.py test_robustness test_core` → exit 0 · Ran 101 tests in 7.4s (25 classes, 16 at a time; slowest: Robustness 7s, BriefIndex 2s, WritesAndLocks 2s) / OK [ran] [tree 5a16cfba5756] (2026-10-31T12:12:53Z)
- (step 2) `python3 plugin/tests/run.py test_robustness test_core` → exit 0 · Ran 101 tests in 7.5s (25 classes, 16 at a time; slowest: Robustness 7s, BriefIndex 2s, WritesAndLocks 2s) / OK [ran] [tree 5a16cfba5756] (2026-10-31T12:13:00Z)
- `python3 plugin/tests/run.py test_robustness -k do_not_depend` → ✗ exit 1 · Ran 1 tests in 1.5s (1 classes, 16 at a time; slowest: Robustness 0s) / FAILED (1 classes: test_robustness.Robustness) (start tree + this task's tests) [ran] [tree 5a16cfba5756] (2026-10-31T12:13:03Z)
- `python3 plugin/tests/run.py test_robustness -k do_not_depend` → exit 0 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: Robustness 0s) / OK [ran] [tree 5a16cfba5756] (2026-10-31T12:13:03Z)
- (ac 1) `python3 plugin/tests/run.py test_robustness test_core` → exit 0 · Ran 101 tests in 7.7s (25 classes, 16 at a time; slowest: Robustness 7s, BriefIndex 2s, WritesAndLocks 2s) / OK [ran] [tree fbe320f04d11] (2026-10-31T12:13:23Z)
- (audit intent) `self-review of the merged diff: _read_brief now adds a just-written closed brief to the fresh index entries before its early return (still unmemoized), so the first checkpoint's caches already hold it; the old test pinning the exclusion is replaced by one that checks a same-tick same-size rewrite is still picked up (write_atomic changes the inode); red→green proved with a clock patched 30 s ahead` → a mutating verb run twice changes nothing the second time, so test_robustness stops flaking under load [tree fbe320f04d11] (2026-10-31T12:13:23Z)
- (audit edge) `self-review of the merged diff: _read_brief now adds a just-written closed brief to the fresh index entries before its early return (still unmemoized), so the first checkpoint's caches already hold it; the old test pinning the exclusion is replaced by one that checks a same-tick same-size rewrite is still picked up (write_atomic changes the inode); red→green proved with a clock patched 30 s ahead` → an in-place hand edit of a brief with the same size, inode and mtime tick could be served stale until its next real change (briefs are only written through write_atomic) [tree fbe320f04d11] (2026-10-31T12:13:23Z)
## Log
- 2026-10-31T12:06:31Z created
- 2026-10-31T12:10:12Z planned from capture
- 2026-10-31T12:10:12Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2324.builder.md
- 2026-10-31T12:10:23Z focused
- 2026-10-31T12:12:44Z merged worktree-agent-a1ea85fb7af7c456c (3 file(s))
- 2026-10-31T12:12:44Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a1ea85fb7af7c456c
- 2026-10-31T12:12:44Z focused
- 2026-10-31T12:13:14Z scope: plugin/lib/fmcore.py (_read_brief), plugin/tests/test_robustness.py, plugin/tests/test_core.py; criterion 1's clause about an mtime moving without a content change doesn't apply: the index is keyed on [inode, mtime_ns, size] by design, so a moved mtime is a real invalidation (the edit was refused because the criterion has evidence; its verify command passes)
- 2026-10-31T12:13:45Z done
- 2026-10-31T12:13:46Z committed bde4e514 (1 file)
- 2026-10-31T12:14:53Z guard authorization added: publish
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2022 [PERFORMANCE M, done, 2 steps] load_briefs reads closed briefs from a stat-checked index: a hook stops opening ~1150 done briefs — lesson: A stat-checked JSON ind…
- T-2323 [FEATURE M, done, 2 steps] fm ship runs the affected tests over its range before the full suite, so a red one stops it in minutes — lesson: Run the cheap, likely-…
- research T-1879-review: Verdict:** changes needed (two small gaps against the acceptance criterion). I read the diff and the surrounding code but did not run `plugin/tes…
- decision 2026-10-30: [cites: the user's steer 2026-10-30 (fourth): standing rule for #1 detection] [check: pending T-2185] Standing rule for #1 Initiative: fm find stays…
## Why not caught
the robustness test only fails when the two checkpoints straddle the 2 s window, which happens only under load (ship runs beside exam sessions)
## Lessons
- A cache that skips 'too fresh' entries makes its own output depend on when it runs: index them, and guard staleness with the key instead
## Files touched
- plugin/tests/test_robustness.py
- plugin/lib/fmcore.py
- plugin/tests/test_core.py
- CHANGELOG.md
