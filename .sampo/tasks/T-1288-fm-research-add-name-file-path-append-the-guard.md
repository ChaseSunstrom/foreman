---
id: T-1288
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-20T20:56:58Z
updated: 2026-10-20T21:53:03Z
base: d0662fb828646839bd481fea2f2121e73f67750b
base_tree: ef019e9cf00067b3ca4c53362f3eb8173b80153e
plan0_at: 2026-10-20T21:41:33Z
plan0_scope: []
verified: strong
---
# fm research add NAME --file PATH --append adds to a research file instead of replacing it, and the guard's state-direct hint names --append
## Raw request
> fm research add NAME --file PATH --append: the guard's state-direct hint (fmguard.py:147) sends agents to fm research add, which replaces the file (cmd_research, fmcli.py:3262), so following the hint on an existing research file erases it; add --append and name it in the hint. Done when two appends leave both texts
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm research add X --file a --append then --file b --append leaves both texts in research/X.md, without --append it still replaces; the guard's hint for a direct write to a research file names --append — verify with `python3 plugin/tests/run.py test_research test_safety`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test for --append and the hint
2. [x] --append in the parser and cmd_research (inside the existing lock); the hint text
## Resume here
## Docs impact
CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_research test_guard test_safety` → exit 0 · Ran 231 tests in 25.3s (75 classes, 16 at a time; slowest: GuardAgainstBash 24s, GuardCases 11s, Hook 9s) / OK [ran] [tree 0e626bef86f8] (2026-10-20T21:43:12Z)
- (step 2) `python3 plugin/tests/run.py test_research test_guard test_safety` → exit 0 · Ran 231 tests in 27.6s (75 classes, 16 at a time; slowest: GuardAgainstBash 25s, GuardCases 12s, Cross 8s) / OK [ran] [tree 0e626bef86f8] (2026-10-20T21:43:41Z)
- (step 1) `python3 plugin/tests/run.py test_research test_safety` → exit 0 · Ran 39 tests in 3.1s (16 classes, 16 at a time; slowest: Cross 3s, DriveSide 3s, SecretsGate 3s) / OK [ran] [tree b7222a43a421] (2026-10-20T21:51:07Z)
- (step 2) `python3 plugin/tests/run.py test_research test_safety` → exit 0 · Ran 39 tests in 3.2s (16 classes, 16 at a time; slowest: DriveSide 3s, Cross 3s, DecisionsResearchSelf 3s) / OK [ran] [tree b7222a43a421] (2026-10-20T21:51:11Z)
- (ac 1) `python3 plugin/tests/run.py test_research test_safety` → exit 0 · Ran 39 tests in 3.3s (16 classes, 16 at a time; slowest: DriveSide 3s, CleanupGate 3s, Cross 3s) / OK [ran] [tree b7222a43a421] (2026-10-20T21:51:15Z)
- (ac 1) `python3 plugin/tests/run.py test_research test_safety` → exit 0 · Ran 39 tests in 3.1s (16 classes, 16 at a time; slowest: DriveSide 3s, Cross 3s, DecisionsResearchSelf 3s) / OK [ran] [tree b7222a43a421] (2026-10-20T21:51:24Z)
- (audit intent) `self review of the builder's branch: --append reads the old note and appends inside the existing lock, the new text still goes through defang(redact()); the hint names --append; tests red first (builder), green on main` → two appends keep both texts, a plain add still replaces [tree b7222a43a421] (2026-10-20T21:51:24Z)
- (audit adversary) `self review of the builder's branch: --append reads the old note and appends inside the existing lock, the new text still goes through defang(redact()); the hint names --append; tests red first (builder), green on main` → appended text is redacted and defanged like a new note; old text was redacted when first written [tree b7222a43a421] (2026-10-20T21:51:24Z)
- (audit edge) `self review of the builder's branch: --append reads the old note and appends inside the existing lock, the new text still goes through defang(redact()); the hint names --append; tests red first (builder), green on main` → --append on a missing note creates it; a blank line separates notes [tree b7222a43a421] (2026-10-20T21:51:24Z)
- (audit operator) `self review of the builder's branch: --append reads the old note and appends inside the existing lock, the new text still goes through defang(redact()); the hint names --append; tests red first (builder), green on main` → the guard's hint now leads to the safe command [tree b7222a43a421] (2026-10-20T21:51:24Z)
- (audit maintainer) `self review of the builder's branch: --append reads the old note and appends inside the existing lock, the new text still goes through defang(redact()); the hint names --append; tests red first (builder), green on main` → one flag, one branch in cmd_research [tree b7222a43a421] (2026-10-20T21:51:24Z)
- (audit self) `self review of the builder's branch: --append reads the old note and appends inside the existing lock, the new text still goes through defang(redact()); the hint names --append; tests red first (builder), green on main` → no findings [tree b7222a43a421] (2026-10-20T21:51:24Z)
## Log
- 2026-10-20T20:56:58Z created
- 2026-10-20T21:41:16Z planned from capture
- 2026-10-20T21:41:22Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1288.builder.md
- 2026-10-20T21:41:33Z focused
- 2026-10-20T21:50:43Z merged worktree-agent-a905bea8d40eb7a19 (4 file(s))
- 2026-10-20T21:50:43Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a905bea8d40eb7a19
- 2026-10-20T21:50:58Z focused
- 2026-10-20T21:51:11Z criterion 1 verify: `python3 plugin/tests/run.py test_research test_guard` → `python3 plugin/tests/run.py test_research test_safety`
- 2026-10-20T21:53:01Z done
- 2026-10-20T21:53:03Z committed 14074119 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0817 [FIX M, done, 3 steps] Guard refusals read better: /dev/null on a data-only python -c, a state-direct hint that points to fm research, and pat… — lesson: A refusa…
- T-0802 [FEATURE S, done, 2 steps] fm research list and fm research show NAME — lesson: when users and criteria keep reaching for a command that doesn't exist, add it
- research t0018-final-maintainer: MEDIUM** — `~/.claude/foreman/plugin/lib/fmcli.py:607-622` (`_agent_report`) and `:625-631` (`cmd_research`) vs `:705-714` (`_…
- decision 2026-10-04: Friction pass 2026-10-04: drop recon findings 1-3 (guard)
- similar finished tasks took 2–3 steps
## Lessons
- A refusal hint must name a command that does what the refused action meant: replacing a file when the agent meant to add to it loses work
## Files touched
- plugin/tests/test_safety.py
- plugin/tests/test_research.py
- plugin/lib/fmcli.py
- plugin/lib/fmguard.py
- CHANGELOG.md
- plugin/tests/test_guard.py
