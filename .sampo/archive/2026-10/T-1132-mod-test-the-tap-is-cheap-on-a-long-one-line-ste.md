---
id: T-1132
type: FIX
tier: S
status: done
priority: normal
scope: [mods/foreman-ui/tests/foreman-ui.test.tsx, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-16T08:36:58Z
updated: 2026-10-16T08:54:03Z
base: b5e4debe2bbcb210db2a75ba6327a0032e42d861
base_tree: e3663f76485546033e2eb707963a6bc285f4edf2
plan0_at: 2026-10-16T08:52:45Z
plan0_scope: [mods/foreman-ui/tests/foreman-ui.test.tsx, CHANGELOG.md]
verified: ok
---
# Mod test 'the tap is cheap on a long one-line step… (T-1090)' times out at 5 s under load
## Raw request
> Mod test 'the tap is cheap on a long one-line step… (T-1090)' times out at 5 s under load (seen at load 43 in the T-1050 lane): measure relative to a baseline or loosen the bound so it isn't a flake
## Interpretation
The T-1090 review test streams 2000 tokens for each of 46 turns (about 92k events), so it exceeds the harness's 5 s per-test limit under load. Only the main session's turn needs the long single line; the 45 agent turns test eviction and word shrinking and need only a short line.
## Assumptions (confidence)
## Acceptance criteria
- [x] the T-1090 review test keeps its assertions and runs in well under a second — verify with `cd mods/foreman-ui && ~/.local/bin/claude plugin test .`
## Non-goals
## Approach (options → choice → why)
Stream 2000 tokens on the session's own turn and 20 on agent turns. The test keeps every assertion and does about 3% of the work. Options considered: a longer timeout (hides cost), or skipping under load (hides the test).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Short lines on agent turns; time the test before and after
## Resume here
## Docs impact
## Verification evidence
- (step 1) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 120 tests across 2 files. [10.15s] [ran] [tree 9aa58a4eb55a] (2026-10-16T08:53:22Z)
- (ac 1) `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 120 tests across 2 files. [10.11s] [ran] [tree 0acc2a1841b1] (2026-10-16T08:53:34Z)
- (audit self) `self: every assertion kept (the long single line still tested on the session's turn; eviction past 40 agents and word shrinking unchanged); measured 1,178 ms → 104 ms` → no findings [tree 0acc2a1841b1] (2026-10-16T08:53:34Z)
## Log
- 2026-10-16T08:36:58Z created
- 2026-10-16T08:51:45Z set scope=['mods/foreman-ui/tests/foreman-ui.test.tsx', 'CHANGELOG.md']
- 2026-10-16T08:52:45Z focused
- 2026-10-16T08:53:23Z scope: CHANGELOG.md — release note
- 2026-10-16T08:54:02Z done
- 2026-10-16T08:54:03Z committed bf663e2 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1090-review: MEDIUM — `register.tsx:688-698`, `:709`. The note says "a failure here never touches the stream", but the `await $.clock.now()` sits outside the …
- T-1031 [FEATURE M, done, 4 steps] Chat UI matches the panel look: section-style headers (bold label, fading colour rule) for — lesson: clean() drops newlines: split a to…
- research T-0909-review: Verdict: changes needed.** The 14-day bars are wrong on this repo today, and the pane order does not match the third acceptance criterion. I coul…
- decision 2026-10-03: T-0166 deferred: splitting the band/pane out of register.tsx is a rewrite under the mod engine's $/atom rules; T-0130 took the rows out, the rest wa…
## Regression test
none: a timing flake, not a behaviour bug; measured: the test took 1,178 ms (earlier run today), now 104 ms, so the 5 s limit has about 50x headroom
## Lessons
- A test that times out under load usually does more work than its assertions need
## Files touched
- mods/foreman-ui/tests/foreman-ui.test.tsx
- CHANGELOG.md
