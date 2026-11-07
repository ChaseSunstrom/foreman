---
id: T-2415
type: RESEARCH
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-31T14:56:33Z
updated: 2026-11-01T06:35:09Z
revisit: 2026-11-02
group: Mission 3 critique spikes
base: c22061b58df1bf3fe1ad2178d9482c9b69145c1a
base_tree: 96d345cc8aadebc9a72fcdec4e82385b1e4bfcc9
plan0_at: 2026-11-01T06:30:24Z
plan0_scope: []
verified: ok
---
# Mission 3 spike, replay git history: run fm find (zero tokens) on the parents of past…
## Raw request
> Mission 3 spike, replay git history: run fm find (zero tokens) on the parents of past fix: commits in Foreman's history; does a lead point at the lines each fix changed? Misses are blind spots that become rules, tools or checks (from gen-1/critique-initiative.md)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the replay ran fm find on the parent of each of the last 40 FIX-task commits and reports how many fixes a lead sat within 3 lines of, with each miss's file kind; the verdict and the blind-spot classes are in the brief and feed Mission 3's critique — verify with `python3 /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/replay_fixes.py --summary`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] write the replay script (throwaway worktrees, zero tokens)
2. [x] run it; record the verdict and blind-spot classes
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 -m py_compile /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/replay_fixes.py && echo compiled` → exit 0 · compiled [ran] [tree 96d345cc8aad] (2026-11-01T06:30:50Z)
- (step 2) `python3 /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/replay_fixes.py --summary` → exit 0 · miss 8da84f2ce fm ci-watch: a cancelled run is not a failure (T-2287) / miss 9f67b04d2 The plan gate counts options that start with a flag, code or a quote (T-2285) [ran] [tree 96d345cc8aad] (2026-11-01T06:34:44Z)
- (ac 1) `python3 /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/replay_fixes.py --summary` → exit 0 · miss 8da84f2ce fm ci-watch: a cancelled run is not a failure (T-2287) / miss 9f67b04d2 The plan gate counts options that start with a flag, code or a quote (T-2285) [ran] [tree 96d345cc8aad] (2026-11-01T06:34:44Z)
- (ac 1) `python3 /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/replay_fixes.py --summary` → exit 0 · miss 8da84f2ce fm ci-watch: a cancelled run is not a failure (T-2287) / miss 9f67b04d2 The plan gate counts options that start with a flag, code or a quote (T-2285) [ran] [tree 96d345cc8aad] (2026-11-01T06:34:54Z)
- (audit self) `self: the method checked against two sanity points: fm find's 44 current leads on this tree are mostly untested symbols, and the same-day exam sweep gives the same blind spot (bug 0/72); worktrees were throwaway and removed, fm find without --capture saves no flags, nothing in the repo changed` → no findings [tree 96d345cc8aad] (2026-11-01T06:34:54Z)
- (audit self) `self: the method checked against two sanity points: fm find's 44 current leads on this tree are mostly untested symbols, and the same-day exam sweep gives the same blind spot (bug 0/72); worktrees were throwaway and removed, fm find without --capture saves no flags, nothing in the repo changed` → no findings [tree 96d345cc8aad] (2026-11-01T06:35:07Z)
## Log
- 2026-10-31T14:56:33Z created
- 2026-10-31T17:28:11Z deferred: Mission 3 spike: it feeds Mission 3's critique, which standing rule 2 orders after Missions 5-8 finish building; it comes back with the critique pass (revisit 2026-11-02)
- 2026-11-01T06:30:24Z focused
- 2026-11-01T06:35:09Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2127 [FEATURE M, done, 2 steps] Initiative surfaces: fm code, MCP tool, site page, pane line, MASTER, README, CHANGELOG (Mission 3 brief 8) — lesson: An allowed non-ze…
- T-2221 [RESEARCH S, blocked, 1 steps] File gen-1/critique-initiative.md (Mission 3's critique) through the cold read
- T-2102 [FEATURE M, done, 5 steps] fm genesis select/seed — exam-gated selection into lineage.md; the feature writes the… — lesson: c.lock is not reentrant: a lock around…
- decision 2026-10-30: [cites: the user's steer 2026-10-30 (fourth): standing rule for #1 detection] [check: pending T-2185] Standing rule for #1 Initiative: fm find stays…
- similar past tasks were M: consider --tier M
- similar finished tasks took 2–5 steps
## Verdict
Replay (2026-11-01, zero tokens, scratchpad replay_fixes.py): fm find --json on the parent of each of the last 40
FIX-task commits in Foreman's history, a hit when a lead sits within 3 lines of a line the fix changed in a code file.
14 of the 40 changed no code (docs or tests only). 0 of the other 26 had a lead near their changed lines.

Verdict: on Foreman's own history the finders have no recall on real fixes. Every one of the 26 is a logic or behaviour
fix (a wrong condition, a missed case, a path that resolves wrong, an environment difference: T-2449, T-2443, T-2438,
T-2435, T-2333, T-2311, T-2287, T-2285 ...), and no finder looks for that class. The exam sweep the same day (s21-013)
agrees: finders found 180/261 planted defects with 0 false alarms, 100% of dep, docs, flaky, fork, slow, untested and
vuln, and 0/72 of bug (planted logic bugs) and 0/9 of trigger (a schedule that's missing).

Blind-spot classes: (1) logic and behaviour bugs, all 26 misses; (2) absence (a missing schedule, a missing case).
Neither becomes a lexical rule. What could find them: the session arm with fm find prove's red-first proof (a test
that fails for the bug's reason), mutation or property tests on hot files (fm find --hotspots names them), and the
recurring-failure signal (#7's recur kind). This goes to Mission 3's critique and gen 2's Seed, not to a new rule.
## Decision
Recommendation: no new lexical finder rule from these misses (none of the 26 has a pattern a rule could match); gen 2's #1 work aims at logic bugs through proofs (the session arm with fm find prove's red-first test), mutation or property tests on fm find --hotspots files, and #7's recurring-failure signal; the finders stay the zero-token hygiene arm. Would change if: a replay over a user project (not Foreman's own mature tree) shows lexical misses a rule could catch.
## Lessons
- Replay the finders on the project's own fix history before trusting exam recall: 180/261 on planted kinds, 0/26 on real fixes
