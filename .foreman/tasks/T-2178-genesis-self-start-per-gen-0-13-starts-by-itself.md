---
id: T-2178
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T15:38:15Z
updated: 2026-10-31T04:27:12Z
base: 634388b46f9fd2d6e850dc3e11ae0b819e9040e3
base_tree: 9fed4e52e6d153b521b87aaacde9f5bbe9d7492a
plan0_at: 2026-10-31T03:45:32Z
plan0_scope: []
verified: strong
---
# Genesis starts by itself on a drained queue under full autonomy when a standing goal holds the user's words
## Raw request
> Genesis self-start per gen-0 #13 ('starts by itself when the queue runs dry'): T-2105 made the offer wait on the user's yes, so it can never start by itself; under full autonomy start it in the tower folder and local lanes with a fm decide row (offer only under standard), reconciling decisions.md 2026-10-30 T-2105 (found by T-2166's cold read of mission-genesis.md)
## Interpretation
gen-0 #13 says Genesis starts by itself when the queue runs dry; T-2105 made it an offer waiting on the user's yes whatever the autonomy, so it never starts by itself. The user's words are what gen-0 needs; a standing goal or mandate is exactly that, so under full autonomy it can start from them.
## Assumptions (confidence)
## Acceptance criteria
- [x] with autonomy full, a drained queue, 10+ done tasks, no tower and a standing goal or mandate (the user's text), the scout drafts gen-0 from that text (fmgenesis.draft), seals it (init) and records a decision naming the source, once; with no goal or mandate, or autonomy standard, it is the offer that waits on the user's yes as before; a sensitive project never auto-starts — verify with `cd plugin/tests && python3 -m unittest -q test_scout test_genesis`
## Non-goals
## Approach (options → choice → why)
Options: (1) auto-start only from the user's own standing goal/mandate text under full autonomy, else offer (chosen: never invents a goal, keeps T-2105's yes where no words exist); (2) always auto-start under full autonomy (would invent a goal); (3) keep offering (fails #13). Choice 1, decided 2026-10-31.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests: full + goal starts once with a decision; full without a goal offers; standard offers; sensitive never starts
2. [x] probe_genesis branches on autonomy and the standing goal
3. [x] docs (MASTER fmscout, CHANGELOG, genesis skill)
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md, plugin/skills/genesis/SKILL.md
## Verification evidence
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_scout test_genesis 2>&1 | grep -v Warning | tail -6` → exit 0 · Ran 175 tests in 59.000s / OK [ran] [tree 332c9857195c] (2026-10-31T03:50:02Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_scout test_genesis 2>&1 | grep -v Warning | tail -6` → exit 0 · Ran 175 tests in 59.000s / OK [ran] [tree 332c9857195c] (2026-10-31T03:50:02Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_scout.GenesisSelfStart` → exit 0 · Ran 5 tests in 0.318s / OK [ran] [tree 332c9857195c] (2026-10-31T03:50:05Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_scout test_genesis 2>&1 | grep -E "^(FAIL|ERROR|Ran|OK|FAILED)"` → exit 0 · Ran 182 tests in 67.521s / OK [ran] [tree 685a14a863d3] (2026-10-31T03:57:57Z)
- (step 2) `cd plugin/tests && python3 -m unittest -q test_scout test_genesis 2>&1 | grep -E "^(FAIL|ERROR|Ran|OK|FAILED)"` → exit 0 · Ran 182 tests in 67.521s / OK [ran] [tree 685a14a863d3] (2026-10-31T03:57:57Z)
- `cd plugin/tests && python3 -m unittest -q test_scout test_genesis` → ✗ exit 1 · Ran 182 tests in 105.181s / FAILED (failures=4) (start tree + this task's tests) [ran] [tree 4839ace78394] (2026-10-31T04:22:51Z)
- `cd plugin/tests && python3 -m unittest -q test_scout test_genesis` → exit 0 · Ran 182 tests in 78.696s / OK [ran] [tree 4839ace78394] (2026-10-31T04:22:51Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_scout test_genesis` → exit 0 · Ran 182 tests in 65.315s / OK [ran] [tree 4839ace78394] (2026-10-31T04:24:02Z)
- (step 2) `cd plugin/tests && python3 -m unittest -q test_scout test_genesis` → exit 0 · Ran 182 tests in 64.781s / OK [ran] [tree 4839ace78394] (2026-10-31T04:25:07Z)
- (step 3) `grep -c T-2178 CHANGELOG.md MASTER.md plugin/skills/genesis/SKILL.md` → exit 0 · MASTER.md:1 / plugin/skills/genesis/SKILL.md:1 [ran] [tree 4839ace78394] (2026-10-31T04:25:07Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_scout test_genesis` → exit 0 · Ran 182 tests in 64.656s / OK [ran] [tree 4839ace78394] (2026-10-31T04:26:33Z)
- (audit intent) `self + one fm-reviewer pass (2 medium, 4 low; all fixed with tests); spot-checked _auto_start ordering and _user_backed` → full autonomy + drained queue + 10 done + an unexpired standing goal backed by the user's words starts Genesis once, with a decision row, key and a note finding; anything else keeps the T-2105 offer (test_scout red-to-green proven) [tree 4839ace78394] (2026-10-31T04:26:33Z)
- (audit adversary) `self + one fm-reviewer pass (2 medium, 4 low; all fixed with tests); spot-checked _auto_start ordering and _user_backed` → a session-written mandate not backed by a user-sourced brief or user steer gets the offer, not a start; MUST/NEVER lines quoted from other briefs force the offer; no model call (draft model=False); the start is local and reversible (a tower folder); ceiling: brief source defaults to user, so the check stops unrelated goals, not a session that also writes a matching brief [tree 4839ace78394] (2026-10-31T04:26:33Z)
- (audit edge) `self + one fm-reviewer pass (2 medium, 4 low; all fixed with tests); spot-checked _auto_start ordering and _user_backed` → two sessions racing init: the loser returns [] and the winner's gen-0 stands; a failure after init still leaves the audit rows [tree 4839ace78394] (2026-10-31T04:26:33Z)
## Log
- 2026-10-30T15:38:15Z created
- 2026-10-31T03:45:02Z planned from capture
- 2026-10-31T03:45:02Z set approved=True
- 2026-10-31T03:45:02Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2178.builder.md
- 2026-10-31T03:45:30Z focused
- 2026-10-31T04:19:38Z merged worktree-agent-ad6662c0115a1e2ef (7 file(s))
- 2026-10-31T04:19:38Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ad6662c0115a1e2ef
- 2026-10-31T04:19:39Z focused
- 2026-10-31T04:25:28Z scope: plugin/lib/fmscout.py (_auto_start, _user_backed), plugin/lib/fmgenesis.py (draft model=False), plugin/tests/{test_scout,test_genesis}.py, MASTER.md, CHANGELOG.md, plugin/skills/genesis/SKILL.md
- 2026-10-31T04:27:05Z done
- 2026-10-31T04:27:12Z guard authorization added: publish
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-10-31: [cites: T-2178; gen-0 §2 #13; decisions 2026-10-30 T-2105] Genesis self-start (gen-0 #13, reconciling T-2105): under full autonomy, a drained queue …
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- research draft-mission-genesis-gen1: Task: T-2093 (brief 1, fm genesis check), T-2095 (brief 2, fm genesis step), T-2099 (brief 3, fm genesis draft/spec), T-2102 (brief …
- research T-2105-review: Verdict** — changes needed. The confirm task shows the user a false reason, and nothing tests the site export that AC3 relies on. Both fixes are …
## Lessons
- Self-starting on stored text needs that text's provenance checked, not just its presence: an unguarded setter makes presence mean nothing
## Files touched
- plugin/tests/test_scout.py
- plugin/lib/fmscout.py
- MASTER.md
- plugin/skills/genesis/SKILL.md
- plugin/lib/fmgenesis.py
- plugin/tests/test_genesis.py
- CHANGELOG.md
