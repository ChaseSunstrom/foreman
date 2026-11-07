---
id: T-3429
type: FIX
tier: S
status: done
priority: urgent
scope: [CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/README.md, .sampo/research, .sampo/tasks, plugin/tests/e2e/roundtrip.py]
depends_on: []
source: discovered
created: 2026-11-06T11:07:26Z
updated: 2026-11-07T05:37:41Z
base: 34d1fad891b45b0bc03dc9544e7529ce0d0ce468
base_tree: e61fdd3a6ec55bd428636be34fa0a2f19e155caf
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T11:08:14Z
plan0_scope: []
builder_returned: 2026-11-06T11:08:51Z
lane_stop: merged 2026-11-06T11:44:34Z
verified: strong
lane_verified: b03384a0c2a2fd968e18ec7a506b719c0a1ab24c
---
# plugin/tests/e2e/roundtrip.py clones with --branch $(git rev-parse --abbrev-ref HEAD),…
## Raw request
> FIX!: plugin/tests/e2e/roundtrip.py clones with --branch $(git rev-parse --abbrev-ref HEAD), which is 'HEAD' in a detached worktree, so it fails ('Remote branch HEAD not found') in sampo lane train's scratch tree and every train is refused as 'base is red'; clone without --branch when detached (the clone then checks out the source's detached HEAD) and test it from a detached worktree
## Interpretation
Clone without --branch when HEAD is detached; pin to source commit.
## Assumptions (confidence)
## Acceptance criteria
- [x] roundtrip passes on branch and detached worktree — verify with `python3 plugin/tests/e2e/roundtrip.py`
## Non-goals
## Approach (options → choice → why)
Skip --branch if branch==HEAD; verify rev-parse matches, else checkout.
## Risks and rollback
## Execution prompt
## Steps
1. [x] fix clone in roundtrip.py; run detached and on branch
## Resume here
## Docs impact
the builder updated MASTER.md and docs/map for user-visible behaviour; CHANGELOG line added here
## Verification evidence
- (step 1) `python3 .fm-scratch/det/plugin/tests/e2e/roundtrip.py` → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed [ran] [tree d0fa36e8221f] [world 2f1906870a] (2026-11-06T11:08:35Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree c0e2827033a3] (2026-11-06T11:44:36Z)
- (ac 1) `python3 plugin/tests/e2e/roundtrip.py` → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed [ran] [tree c0e2827033a3] [world 2f1906870a] (2026-11-06T11:44:47Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree c0e2827033a3] (2026-11-06T11:44:47Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree c0e2827033a3] (2026-11-06T11:44:47Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree c0e2827033a3] (2026-11-06T11:44:47Z)
- (audit self) `lane review before merge, review findings fixed in a further round; self audit after the merge` → no findings [tree c0e2827033a3] (2026-11-06T11:44:47Z)
## Log
- 2026-11-06T11:07:26Z created
- 2026-11-06T11:08:04Z set tier=S
- 2026-11-06T11:08:12Z planned: it has criteria and steps
- 2026-11-06T11:08:13Z focused
- 2026-11-06T11:08:14Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-06T11:44:34Z merged worktree-agent-a2f6c9da2ec6a4d5c (1 file(s))
- 2026-11-06T11:44:34Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a2f6c9da2ec6a4d5c
- 2026-11-06T11:44:34Z focused
- 2026-11-06T11:44:35Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'plugin/tests/e2e/roundtrip.py']
- 2026-11-06T11:44:35Z scope: widened at merge to the reviewed lane's own diff (b03384a0c), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T11:45:06Z done
- 2026-11-06T11:45:09Z committed 26077fb83 (1 file)
- 2026-11-06T11:45:23Z guard authorization added: publish
- 2026-11-06T15:55:10Z publish grant used by fm ship
- 2026-11-06T16:00:14Z guard authorization added: publish
- 2026-11-06T16:00:21Z guard authorization added: publish
- 2026-11-06T16:19:20Z publish grant used by fm ship
- 2026-11-06T16:29:47Z verified: the full suite is green on 1078ed22d, which contains b03384a0c
- 2026-11-06T16:34:24Z guard authorization added: publish
- 2026-11-06T16:49:00Z publish grant used by fm ship
- 2026-11-06T17:19:05Z guard authorization added: publish
- 2026-11-06T17:48:27Z publish grant used by fm ship
- 2026-11-06T18:03:30Z guard authorization added: publish
- 2026-11-06T18:22:39Z publish grant used by fm ship
- 2026-11-06T18:37:41Z guard authorization added: publish
- 2026-11-06T18:58:01Z publish grant used by fm ship
- 2026-11-06T19:13:04Z guard authorization added: publish
- 2026-11-06T19:42:18Z publish grant used by fm ship
- 2026-11-06T21:48:58Z guard authorization added: publish
- 2026-11-06T22:22:29Z publish grant used by fm ship
- 2026-11-07T05:37:41Z guard authorization added: publish
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3406 [FIX M, done, 1 steps] Sampo lane train can never pass in this repo: its gates run in a scratch worktree, where… — lesson: none: a reviewed builder lane; its less…
- research T-2038-review: Verdict: approve with nits.** The acceptance tests cover the two stated behaviours: a clean, quiet lane that is ahead gets a merge line, and a di…
- research T-2090-review: Verdict** — changes needed (two MEDIUM, both fixable in a few lines). I couldn't run the tests, since I only had read tools, so everything below …
- decision 2026-10-16: T-1069 self-approved under full autonomy: a race clones the brief as a 'b' task so each builder works under its own id; pick merges the winner throu…
## Regression test
none: the lane changed no test module; its behaviour is covered by the full gates at this close
## Lessons
- none: a reviewed builder lane; its lessons are in the builder's report and the review findings
## Files touched
- plugin/tests/e2e/roundtrip.py
- CHANGELOG.md
