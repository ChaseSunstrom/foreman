---
id: T-2666
type: RESEARCH
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-02T20:41:56Z
updated: 2026-11-02T20:45:18Z
base: 6716f9643748e59cddc470562a16753eaa827391
base_tree: b0b4477ba78db91a673827bc4ac6e8130e8cfa6c
plan0_at: 2026-11-02T20:42:04Z
plan0_scope: []
verified: strong
unproven: [research-uncited]
---
# Genesis gen-3 Mission 5 (#12 staying lean and safe): ground the 525-idea brainstorm, record the catalogue, file the Mission and intake its briefs
## Raw request
> Genesis gen-3 Mission 5 (#12 staying lean and safe): ground the 525-idea brainstorm, record the catalogue, file the Mission and intake its briefs
## Interpretation
1. (chosen) Follow the tower's step: the brainstorm ran, so ground it, record every cluster, file the Mission with a verified slate, and intake its briefs.
2. Build first and file the Mission after. Rejected: Mission 4's critique named that order slip as a failure.
## Assumptions (confidence)
## Acceptance criteria
- [x] gen-3/mission-staying-lean-and-safe.md is filed (its cold read passed) and its briefs are in the queue — verify with `fm genesis status`
## Non-goals
## Approach (options → choice → why)
1. Three recon agents ground the 525 ideas in chunks; I spot-check the claims the slate rests on and drop false ones; the Mission names only verified gaps. Likely outcome: a 3-brief slate with each gap re-grepped. Fails if: a slate gap is already built (the T-2659 failure), caught by the spot checks.
2. use what exists: take the recon marks as given. Fails if: a recon claim is false; one of three spot checks already was (fmrelproof.py:82 is filtered).
3. do less: file the Mission with one brief. Fails if: #12 has two halves, lean and safe, and one brief serves only one.
Choice 1 (90%): the spot checks are what make the slate trustworthy.
## Risks and rollback
## Execution prompt
## Steps
1. [x] catalogue recorded with fm research add
2. [x] Mission filed with fm genesis put
3. [x] briefs taken in with fm intake
## Resume here
## Docs impact
none: the catalogue and the Mission are Foreman state (state/projects/foreman-4a056f/research/), not repo docs
## Verification evidence
- (step 1) `test -s state/projects/foreman-4a056f/research/brainstorm-20261102-m5.md` → exit 0 · (no output) [ran] [tree b0b4477ba78d] [world 2f1906870a] (2026-11-02T20:42:29Z)
- (step 2) `test -s state/projects/foreman-4a056f/research/genesis/gen-3/mission-staying-lean-and-safe.md` → exit 0 · (no output) [ran] [tree b0b4477ba78d] [world 2f1906870a] (2026-11-02T20:44:55Z)
- (step 3) `fm task show T-2669` → exit 0 · - 2026-11-02T20:44:49Z created / ## Follow-ups captured [ran] [tree b0b4477ba78d] [world 2f1906870a] (2026-11-02T20:44:56Z)
- (ac 1) `fm genesis status` → exit 0 · long-horizon (deciding): behind on 6 same goal(s): foreman 0/6 done, checks 4/20, false-done 6, regressions 0, resumes needed 0, unfinished 0, cost $13.08 vs plain 1/6 done, checks 4/20, false-done 5, [ran] [tree b0b4477ba78d] [world 2f1906870a] (2026-11-02T20:44:57Z)
- (ac 1) `fm genesis status` → exit 0 · reused: the same command passed on this tree and world at 2026-11-02T20:44:57Z [ran] [tree b0b4477ba78d] [world 2f1906870a] (2026-11-02T20:45:03Z)
- (audit intent) `self: every slate gap was re-grepped and one recon claim was refuted before filing; the Mission's cold read passed after two revisions (grounding lines naming code, a concrete Done when)` → the tower's step for Mission 5 asked for the brainstorm, the Mission and its briefs; all three exist and the critique's numbers are named [tree b0b4477ba78d] (2026-11-02T20:45:03Z)
- (audit edge) `self: every slate gap was re-grepped and one recon claim was refuted before filing; the Mission's cold read passed after two revisions (grounding lines naming code, a concrete Done when)` → one idea of 525 was lost by a recon pass; the catalogue says so rather than claiming all 525 [tree b0b4477ba78d] (2026-11-02T20:45:03Z)
- (audit intent) `self: every slate gap was re-grepped and one recon claim was refuted before filing; the Mission's cold read passed after two revisions` → the tower's step for Mission 5 asked for the brainstorm, the Mission and its briefs; all three exist and the critique's numbers are named [tree b0b4477ba78d] (2026-11-02T20:45:11Z)
- (audit edge) `self: every slate gap was re-grepped and one recon claim was refuted before filing; the Mission's cold read passed after two revisions` → one idea of 525 was lost by a recon pass; the catalogue says so rather than claiming all 525 [tree b0b4477ba78d] (2026-11-02T20:45:11Z)
- (audit intent) `self: every slate gap was re-grepped and one recon claim was refuted before filing; the Mission's cold read passed after two revisions` → the tower's step for Mission 5 asked for the brainstorm, the Mission and its briefs; all three exist and the critique's numbers are named [tree b0b4477ba78d] (2026-11-02T20:45:17Z)
- (audit edge) `self: every slate gap was re-grepped and one recon claim was refuted before filing; the Mission's cold read passed after two revisions` → one idea of 525 was lost by a recon pass; the catalogue says so rather than claiming all 525 [tree b0b4477ba78d] (2026-11-02T20:45:17Z)
## Log
- 2026-11-02T20:41:56Z created
- 2026-11-02T20:42:03Z focused
- 2026-11-02T20:45:18Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- T-2095 [FEATURE M, done, 3 steps] fm genesis step: the tower's next action from its files, resumable after any kill — lesson: A resumable state machine over files has to…
- T-2077 [RESEARCH L, blocked, 8 steps] Genesis gen 1: Missions 2-8, critiques, lineage, sweep, gen-2 Seed
- decision 2026-10-31: [cites: user steer 2026-10-31: run the remaining independent missions in parallel lanes] Parallel Missions 5-8 (user steer 2026-10-31): fm lane refu…
- similar finished tasks took 3–5 steps
## Decision
Recommendation: Mission 5 builds three measured gaps (burden counts hook_success SessionStart context and splits it by source; a guard latency test on pathological input; fm run --stall-usd), and carries the bypass lease, outbound secret scan and slopsquatting clusters to the next seed. Would change if: brief 1's recount shows injected context is not the dominant lean cost, in which case the next Mission prices spend per task instead.
## Lessons
- Recon grounding at ~8 tool calls per 170 ideas is shallow: one of three spot-checked claims was false, and a fourth look found a real measurement gap (hook_success uncounted) that no recon reported; spot-check every claim a brief rests on
