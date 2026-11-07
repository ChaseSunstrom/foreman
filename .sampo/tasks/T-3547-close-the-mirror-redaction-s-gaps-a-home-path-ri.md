---
id: T-3547
type: SECURITY
tier: S
status: done
priority: normal
scope: [CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/fleet, .sampo/fleet.md, .sampo/README.md, .sampo/research, .sampo/tasks, scripts/probe-plugin-rename.sh, plugin/lib/sampo/core.py, plugin/lib/sampo/sync.py, plugin/tests/test_cockpit.py, plugin/tests/test_ecosystem.py, plugin/tests/test_sync.py]
depends_on: []
source: user
created: 2026-11-07T00:11:38Z
updated: 2026-11-07T02:18:07Z
base: afca369d5306798d95690ce1a45d2cb7977963e6
base_tree: 26dea69e852fd2d4d59227aa10701119e0110227
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-07T00:12:03Z
plan0_scope: []
lane_stop: merged 2026-11-07T02:10:19Z
verified: strong
lane_verified: 6adf0566370c96f3c9cbd6c9828020913d2b6fa4
---
# Close the mirror redaction's gaps: a home path right after a word character ($NOPE/home/<user>/), brief meta values (lane: paths) and the Claude project folder form, and the two tests that name the JARVIS login
## Raw request
> Close the mirror redaction's gaps: a home path right after a word character ($NOPE/home/<user>/), brief meta values (lane: paths) and the Claude project folder form, and the two tests that name the JARVIS login
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] sync export leaves no home path, private term or private host in any mirrored file (meta values included), and no test names the JARVIS login — verify with `python3 plugin/tests/run.py test_sync test_private_terms test_cockpit test_ecosystem`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] the three redaction gaps and the two tests, test-first
## Resume here
## Docs impact
the lane diff carries its own doc edits (merged as reviewed); a CHANGELOG line is added here
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_sync` → ✗ exit 1 · Ran 37 tests in 45.0s (2 jobs, 16 at a time; slowest: Sync 27s, BoardSurfaces 1s) / FAILED (1 classes: test_sync.Sync) [ran] [tree 10de42660387] [world 2f1906870a] (2026-11-07T00:16:46Z)
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_sync test_private_terms test_cockpit test_ecosystem` → exit 0 · Ran 60 tests in 19.7s (47 jobs, 16 at a time; slowest: HarnessCanary 8s, Sweep 2s, AdoptHistory 2s) / OK [ran] [tree 28ac013f65bc] [world 2f1906870a] (2026-11-07T00:17:26Z)
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_sync test_private_terms test_cockpit test_ecosystem` → exit 0 · Ran 60 tests in 113.6s (48 jobs, 16 at a time; slowest: HarnessCanary.test_a_new_claude_code_version_runs_the_checks 19s, Sync.test_a_private_term_added_later_rewrites_the_mirrored_copies_once 5s, Syn [ran] [tree e60a94fbad84] [world 2f1906870a] (2026-11-07T00:20:29Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 5c5088b75b1e] (2026-11-07T02:13:01Z)
- (ac 1) `python3 plugin/tests/run.py test_sync test_private_terms test_cockpit test_ecosystem` → exit 0 · Ran 60 tests in 117.9s (48 jobs, 16 at a time; slowest: HarnessCanary.test_a_new_claude_code_version_runs_the_checks 6s, Sweep 1s, AdoptHistory 1s) / OK [ran] [tree 5c5088b75b1e] [world 2f1906870a] (2026-11-07T02:15:04Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree 5c5088b75b1e] (2026-11-07T02:15:04Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree 5c5088b75b1e] (2026-11-07T02:15:04Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree 5c5088b75b1e] (2026-11-07T02:15:04Z)
- (audit self) `lane review before merge, review findings fixed in a further round; self audit after the merge` → no findings [tree 5c5088b75b1e] (2026-11-07T02:15:04Z)
## Log
- 2026-11-07T00:11:38Z created
- 2026-11-07T00:11:55Z lane: ~/.claude/foreman.lanes/T-3547 on foreman/T-3547
- 2026-11-07T00:12:02Z focused
- 2026-11-07T00:12:03Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-07T02:10:19Z merged foreman/T-3547 in merge train
- 2026-11-07T02:13:01Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/fleet', '.sampo/fleet.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'scripts/probe-plugin-rename.sh', 'plugin/lib/sampo/core.py', 'plugin/lib/sampo/sync.py', 'plugin/tests/test_cockpit.py', 'plugin/tests/test_ecosystem.py', 'plugin/tests/test_sync.py']
- 2026-11-07T02:13:01Z scope: widened at merge to the reviewed lane's own diff (6adf05663), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902), and scripts/probe-plugin-rename.sh (an untracked stray copy T-3549 removed between closes; a base taken before that counts its removal)
- 2026-11-07T02:16:55Z done
- 2026-11-07T02:17:00Z committed fab94fc38 (417 files)
- 2026-11-07T02:17:03Z lane removed: ~/.claude/foreman.lanes/T-3547; dropped: merged and closed
- 2026-11-07T02:18:07Z verified: the full suite is green on 9b743b958, which contains 6adf05663
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2746 [FEATURE M, done, 3 steps] sampo migrate: move ~/.claude/foreman and its siblings (foreman.draft, foreman.evolve, foreman.lanes) to ~/.claude/sampo once, leave sy…
- research T-2995-review: Verdict: changes needed.** Two privacy gaps and one fail-open on the Claude rule need fixing. I could only read files in this session, so I did n…
- research T-1606-review: Verdict: changes needed.** The core works, but the note's "logs keep it redacted" claim is false on one path, and the report-and-file flow puts t…
- decision 2026-11-06: Sync is off until T-3342 (.sampo mirror rename) lands: main's old code exports to an untracked .foreman/ while .sampo/ is tracked, and the import si…
## Lessons
- A filter that runs only on files it rewrites misses the files it skips on purpose: every skip path needs the same scrub as the write path.
## Plan gaps
- failed first: step 1 the three redaction gaps and the two tests, test-first
## Files touched
- CHANGELOG.md
- plugin/lib/sampo/core.py
- plugin/lib/sampo/sync.py
- plugin/tests/test_cockpit.py
- plugin/tests/test_ecosystem.py
- plugin/tests/test_sync.py
