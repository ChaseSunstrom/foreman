---
id: T-1150
type: RESEARCH
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-16T10:13:12Z
updated: 2026-10-16T10:46:41Z
base: 72f7222091b108cedef8858dc990bc200b5037a0
base_tree: 14d05781106d988df90348752dd35fa470e47fb2
plan0_at: 2026-10-16T10:13:23Z
plan0_scope: []
verified: strong
---
# Forever loop round 2: brainstorm past everything shipped through 1.2.32, ground every idea, queue what's real
## Raw request
> Forever loop round 2: brainstorm past everything shipped through 1.2.32, ground every idea, queue what's real
## Interpretation
The forever loop's next round. Brainstorm past everything shipped through 1.2.32, with the main thread's review of what's weak in the pack and the six earlier idea lists marked seen. Then ground every idea against the code, queue the real and new ones, and record the yield (fewer than 3 is a dry round).
## Assumptions (confidence)
## Acceptance criteria
- [x] every idea of the round is grounded and either queued as a brief or marked with why not; fm loop yield recorded — verify with `fm loop status`
## Non-goals
## Approach (options → choice → why)
fm ideas, 2 rounds with deepen 2, on the round-2 pack. Cluster the deduplicated ideas.md, ground each cluster with a grep or read (or fm-recon for big ones), and score value against effort. One fm intake block for the build marks. fm research add holds the whole catalogue, then fm loop yield N.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Run fm ideas on the round-2 pack
2. [x] Cluster, ground (fm-recon), score; fm intake the build marks; fm research add the catalogue
3. [x] fm loop yield N
## Resume here
## Docs impact
none: research only
## Verification evidence
- (step 1) `head -2 state/projects/foreman-4a056f/research/brainstorm-20261016-051317/ideas.md` → exit 0 · # Ideas by round (deduplicated titles; details in the lens files; "near T-…" names a finished task that shares most of an idea's words) / Ideas: 218 distinct (the bullets under Round, Deepened and Cro [ran] [tree 16315f879933] (2026-10-16T10:22:42Z)
- (step 2) `test -s state/projects/foreman-4a056f/research/brainstorm-20261016-round2.md && fm queue | grep -c 'T-11[56]'` → exit 0 · 1 [ran] [tree d1c78d64a70d] (2026-10-16T10:46:09Z)
- (step 3) `fm loop status` → exit 0 · Forever loop: on · round 3 [ran] [tree d1c78d64a70d] (2026-10-16T10:46:10Z)
- (ac 1) `fm loop status` → exit 0 · Forever loop: on · round 3 [ran] [tree d1c78d64a70d] (2026-10-16T10:46:17Z)
- (audit intent) `self: 218 ideas clustered into 38 clusters by a general-purpose agent, each grounded by grep/read; spot-checked fm away and fm todo absent; 15 build lines intaken (one softened from refuse to warn-and-exclude), the rest marked skip/queued/partial in the catalogue` → round past everything seen, every idea grounded, nothing dropped silently [tree d1c78d64a70d] (2026-10-16T10:46:17Z)
- (audit adversary) `self: 218 ideas clustered into 38 clusters by a general-purpose agent, each grounded by grep/read; spot-checked fm away and fm todo absent; 15 build lines intaken (one softened from refuse to warn-and-exclude), the rest marked skip/queued/partial in the catalogue` → brainstorm output treated as untrusted data; intake lines rewritten where a design would hurt users (dirty-file refuse) [tree d1c78d64a70d] (2026-10-16T10:46:17Z)
- (audit edge) `self: 218 ideas clustered into 38 clusters by a general-purpose agent, each grounded by grep/read; spot-checked fm away and fm todo absent; 15 build lines intaken (one softened from refuse to warn-and-exclude), the rest marked skip/queued/partial in the catalogue` → ideas that duplicated in-flight tasks marked queued, not re-captured [tree d1c78d64a70d] (2026-10-16T10:46:17Z)
- (audit operator) `self: 218 ideas clustered into 38 clusters by a general-purpose agent, each grounded by grep/read; spot-checked fm away and fm todo absent; 15 build lines intaken (one softened from refuse to warn-and-exclude), the rest marked skip/queued/partial in the catalogue` → catalogue filed under research/, build titles visible in fm queue [tree d1c78d64a70d] (2026-10-16T10:46:17Z)
- (audit maintainer) `self: 218 ideas clustered into 38 clusters by a general-purpose agent, each grounded by grep/read; spot-checked fm away and fm todo absent; 15 build lines intaken (one softened from refuse to warn-and-exclude), the rest marked skip/queued/partial in the catalogue` → yield 15 recorded; loop continues to round 3 [tree d1c78d64a70d] (2026-10-16T10:46:17Z)
- (audit intent) `self: 218 ideas clustered into 38 clusters, each grounded by grep/read; spot-checked fm away and fm todo absent; 15 build lines intaken (one softened from refuse to warn-and-exclude), the rest marked in the catalogue` → round past everything seen, every idea grounded, nothing dropped silently [tree d1c78d64a70d] (2026-10-16T10:46:34Z)
- (audit adversary) `self: 218 ideas clustered into 38 clusters, each grounded by grep/read; spot-checked fm away and fm todo absent; 15 build lines intaken (one softened from refuse to warn-and-exclude), the rest marked in the catalogue` → brainstorm output treated as untrusted data; intake lines rewritten where a design would hurt users [tree d1c78d64a70d] (2026-10-16T10:46:34Z)
- (audit edge) `self: 218 ideas clustered into 38 clusters, each grounded by grep/read; spot-checked fm away and fm todo absent; 15 build lines intaken (one softened from refuse to warn-and-exclude), the rest marked in the catalogue` → ideas duplicating in-flight tasks marked queued, not re-captured [tree d1c78d64a70d] (2026-10-16T10:46:34Z)
- (audit operator) `self: 218 ideas clustered into 38 clusters, each grounded by grep/read; spot-checked fm away and fm todo absent; 15 build lines intaken (one softened from refuse to warn-and-exclude), the rest marked in the catalogue` → catalogue filed under research/, build titles in fm queue [tree d1c78d64a70d] (2026-10-16T10:46:34Z)
- (audit maintainer) `self: 218 ideas clustered into 38 clusters, each grounded by grep/read; spot-checked fm away and fm todo absent; 15 build lines intaken (one softened from refuse to warn-and-exclude), the rest marked in the catalogue` → yield 15 recorded; loop continues to round 3 [tree d1c78d64a70d] (2026-10-16T10:46:34Z)
## Log
- 2026-10-16T10:13:12Z created
- 2026-10-16T10:13:22Z focused
- 2026-10-16T10:14:10Z paused: focus moved to T-1148
- 2026-10-16T10:22:41Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-16T10:22:41Z focused
- 2026-10-16T10:24:19Z paused: focus moved to T-1152
- 2026-10-16T10:46:02Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-16T10:46:02Z focused
- 2026-10-16T10:46:41Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0818 [RESEARCH M, done, 3 steps] Round 2 brainstorm: improvements on top of round 1 (what shipped today), past every earlier idea — lesson: Round 2 of a recursive loop…
- T-1057 [FEATURE M, done, 3 steps] Forever loop: fm loop on makes Foreman improve itself without end: when the queue and inbo — lesson: An invariant that ends a loop must…
- T-1076 [FEATURE M, done, 2 steps] Upstream watch: fm doctor matches recurring Claude Code errors to known upstream issues an — lesson: A bundled list of upstream facts n…
- decision 2026-10-15: Stop the brainstorm loop after round 8: dry (1 grounded build of value 3, none of value 4+, out of 45)
- similar finished tasks took 2–3 steps
## Decision
Recommendation: build the 15 grounded items T-1155..T-1169 with up to 4 builders, then run round 3 against the improved tree; would change if: round 3 grounds fewer than 3 new valuable ideas (a dry round).
## Lessons
- one grounding agent over a whole catalogue is cheaper than per-cluster recon and kept every idea
## Files touched
- plugin/lib/fmbus.py
- plugin/tests/test_claims.py
