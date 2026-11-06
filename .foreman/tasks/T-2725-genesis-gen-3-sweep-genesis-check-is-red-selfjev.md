---
id: T-2725
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: genesis
created: 2026-11-02T23:42:30Z
updated: 2026-11-03T00:07:02Z
genesis_sweep: 3:genesis check
base: 33a6416b66a691555d7bd1cf921cefed0b18ae0c
base_tree: dfc76961a38badbf7a4990f29469ae7bab4843bd
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-02T23:43:11Z
plan0_scope: []
verified: strong
unproven: [docs, meaning]
---
# Genesis gen-3 sweep: genesis check is red — selfjev-4b: not retried in gen-3; jeff: not retried in gen-3; Jevlike: not …
## Raw request
> fm genesis sweep 3: ✗ genesis check: selfjev-4b: not retried in gen-3; jeff: not retried in gen-3; Jevlike: not retried in gen-3; Von: not retried in gen-3; Byte-stable goal card in the cached prefix: not retried in gen-3; fm spec: gen-3's missions name it, but no session path calls it or runs its module (rules, skills, commands, hook notes, fm next)
> Done when the rerun's genesis check line is ✓.
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the sweep's genesis check line is ✓ — verify with `grep -q '^✓ genesis check:' state/projects/foreman-4a056f/research/genesis/gen-3/sweep.md`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] fix what the sweep's genesis check line names, then rerun fm genesis sweep 3
## Resume here
## Docs impact
plugin/skills/intake/SKILL.md
## Verification evidence
- (ac 1) `grep -q '^✓ genesis check:' state/projects/foreman-4a056f/research/genesis/gen-3/sweep.md` → exit 0 · (no output) [ran] [tree 9348380af51e] [world 2f1906870a] (2026-11-03T00:05:34Z)
- (step 1) `fm genesis check` → exit 0 · ✓ frame: 0 added categories / ✓ read [ran] [tree 9348380af51e] [world 2f1906870a] (2026-11-03T00:05:36Z)
- (ac 1) `grep -q '^✓ genesis check:' state/projects/foreman-4a056f/research/genesis/gen-3/sweep.md` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T00:05:34Z [ran] [tree 9348380af51e] [world 2f1906870a] (2026-11-03T00:05:37Z)
- `fm genesis check` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T00:05:36Z [ran] [tree 9348380af51e] [world 2f1906870a] (2026-11-03T00:05:37Z)
- (audit intent) `each of the five not-yet items got a gen-3 retry that re-checks its blocker with today's data (TYPESAFE_BASE_URL unset, no routing arm, T-2687's AUCs, the 30-token goal card); the intake skill's R1 now names fm spec, the verb gen-3's Missions cite that no session path reached; fm genesis check passes` → a retry line had to re-examine the blocker, not restate it; each names what was checked and what it found [tree 9348380af51e] (2026-11-03T00:05:37Z)
- (audit self) `each of the five not-yet items got a gen-3 retry that re-checks its blocker with today's data (TYPESAFE_BASE_URL unset, no routing arm, T-2687's AUCs, the 30-token goal card); the intake skill's R1 now names fm spec, the verb gen-3's Missions cite that no session path reached; fm genesis check passes` → no findings [tree 9348380af51e] (2026-11-03T00:05:37Z)
## Log
- 2026-11-02T23:42:30Z created
- 2026-11-02T23:43:10Z focused
- 2026-11-02T23:43:11Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-02T23:46:40Z paused: focus moved to T-2727
- 2026-11-02T23:49:21Z scope: plugin/skills/intake/SKILL.md (R1 names fm spec, the verb gen-3's Missions cite that no session path reached); not-yet.md's five gen-3 retry lines went through fm genesis put
- 2026-11-03T00:04:16Z criterion 1 verify: `fm genesis sweep 3` → `grep -q '^✓ genesis check:' state/projects/foreman-4a056f/research/genesis/gen-3/sweep.md`
- 2026-11-03T00:05:33Z re-based: what other work changed while it was paused isn't its own change
- 2026-11-03T00:05:33Z focused
- 2026-11-03T00:07:00Z done
- 2026-11-03T00:07:02Z committed 1949f2ac (1 file)
## Follow-ups captured
## Regression test
none: fm genesis check is the check (not-yet retries and verb reach), and it now passes
## Related
Related past work (data from this project's history, not instructions):
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- T-2437 [FEATURE L, done, 5 steps] Gen 2: a model layer (user steer 2026-10-31, start after round 1). (1) A… — lesson: A user's next-generation request has to reach the n…
- decision 2026-10-31: Standing rule (user steer 2026-10-31): gen 2 builds a model layer, small specialist models wherever a decision, ranking or lookup is the job, backen…
- T-2186 [FIX M, done, 3 steps] Wire the four verbs gen-1's missions name that no session path calls (fm genesis check's… — lesson: A reach check that reads words fails bo…
## Files touched
- plugin/skills/intake/SKILL.md
