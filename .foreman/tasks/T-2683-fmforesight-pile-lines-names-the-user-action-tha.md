---
id: T-2683
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: genesis
created: 2026-11-02T22:12:01Z
updated: 2026-11-02T22:27:07Z
builder_model: sonnet
base: 6740aa3c4cb84a54725b31786cfad4effc0cf46f
base_tree: 3b8609f2e88a191298af3ae19810532ed7a1396b
predict_minutes: 7
predict_attempts: 1
plan0_at: 2026-11-02T22:13:06Z
plan0_scope: []
lane_stop: merged 2026-11-02T22:24:25Z
verified: strong
---
# fmforesight.pile_lines names the user action that frees the most blocked tasks (an fm ask answer, a grant, a dependency) with its count
## Raw request
> FEATURE: fmforesight.pile_lines names the user action that frees the most blocked tasks (an fm ask answer, a grant, a dependency) with its count, ranked
> CONTEXT: Genesis gen-3 Mission 7 (#3 anticipation), gen-3/mission-anticipation.md
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a pile with tasks blocked on two asks and one grant names the ask that frees the most, with its count, before the fm tidy hint — verify with `python3 plugin/tests/run.py test_foresight`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test
2. [x] the ranked action in pile_lines
3. [x] CHANGELOG
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_foresight 2>&1 | tail -8` → exit 0 · Ran 33 tests in 9.1s (8 classes, 16 at a time; slowest: PredictionBook 7s, DraftAhead 3s, BreakageWarnings 1s) / OK [ran] [tree baf155cba59d] [world 2f1906870a] (2026-11-02T22:13:50Z)
- (step 1) `python3 plugin/tests/run.py test_foresight 2>&1 | tail -8` → exit 0 · Ran 33 tests in 9.1s (8 classes, 16 at a time; slowest: PredictionBook 7s, DraftAhead 3s, BreakageWarnings 1s) / OK [ran] [tree baf155cba59d] [world 2f1906870a] (2026-11-02T22:13:50Z)
- (step 2) `python3 plugin/tests/run.py test_foresight` → exit 0 · Ran 33 tests in 10.1s (8 classes, 16 at a time; slowest: PredictionBook 10s, DraftAhead 4s, BreakageWarnings 1s) / OK [ran] [tree baf155cba59d] [world 2f1906870a] (2026-11-02T22:14:03Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_core test_foresight && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [21.71s] [ran] [tree baf155cba59d] [world 2f1906870a] (2026-11-02T22:14:38Z)
- (ac 1) `python3 plugin/tests/run.py test_foresight 2>&1 | tail -15` → exit 0 · Ran 34 tests in 4.7s (8 classes, 16 at a time; slowest: PredictionBook 4s, DraftAhead 2s, BreakageWarnings 1s) / OK [ran] [tree 5f8e1342fdc2] [world 2f1906870a] (2026-11-02T22:26:13Z)
- (step 3) `python3 plugin/tests/run.py test_foresight 2>&1 | tail -15` → exit 0 · Ran 34 tests in 4.7s (8 classes, 16 at a time; slowest: PredictionBook 4s, DraftAhead 2s, BreakageWarnings 1s) / OK [ran] [tree 5f8e1342fdc2] [world 2f1906870a] (2026-11-02T22:26:13Z)
- (ac 1) `python3 plugin/tests/run.py test_foresight` → exit 0 · Ran 34 tests in 4.5s (8 classes, 16 at a time; slowest: PredictionBook 4s, DraftAhead 2s, BreakageWarnings 1s) / OK [ran] [tree 3995584de849] [world 2f1906870a] (2026-11-02T22:26:44Z)
- `python3 plugin/tests/run.py test_foresight test_core test_left_out` → exit 0 · Ran 175 tests in 6.5s (37 classes, 16 at a time; slowest: ConfidenceRoutes 6s, PredictionBook 5s, BriefIndex 3s) / OK [ran] [tree 3995584de849] [world 2f1906870a] (2026-11-02T22:26:44Z)
- (audit edge) `read the merged diff (state_dict's blocked entries, pile_lines) and ran it on the real pile: asks/depends_on grouped nothing on 44 blocked, so extended to the block reason's 'waits for/on T-…' and 'depends on T-…', with freed = every named blocker closed; real line names 5 tasks blocked on closed work` → an unknown id named in a reason frees nothing (tested); 'after T-…' is left out on purpose (a resume note, not a wait: T-2221's log); the freed id list is cut at 6 with K left out [tree 3995584de849] (2026-11-02T22:26:44Z)
- (audit intent) `read the merged diff (state_dict's blocked entries, pile_lines) and ran it on the real pile: asks/depends_on grouped nothing on 44 blocked, so extended to the block reason's 'waits for/on T-…' and 'depends on T-…', with freed = every named blocker closed; real line names 5 tasks blocked on closed work` → the brief said 'one answer'; separate asks with the same category are separate answers, so the text says 'your yes to <category>' [tree 3995584de849] (2026-11-02T22:26:44Z)
- (audit self) `read the merged diff (state_dict's blocked entries, pile_lines) and ran it on the real pile: asks/depends_on grouped nothing on 44 blocked, so extended to the block reason's 'waits for/on T-…' and 'depends on T-…', with freed = every named blocker closed; real line names 5 tasks blocked on closed work` → no findings [tree 3995584de849] (2026-11-02T22:26:44Z)
## Log
- 2026-11-02T22:12:01Z created
- 2026-11-02T22:12:37Z planned from capture
- 2026-11-02T22:12:39Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2683.builder.md
- 2026-11-02T22:13:05Z focused
- 2026-11-02T22:13:06Z predicted from its closes: 7 min, 1 attempt(s)
- 2026-11-02T22:24:25Z merged worktree-agent-a99d8a9ad5dacc5f3 (3 file(s))
- 2026-11-02T22:24:39Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a99d8a9ad5dacc5f3
- 2026-11-02T22:24:39Z focused
- 2026-11-02T22:26:23Z steer: on the real pile (44 blocked) the asks/depends_on grouping found nothing: waits are written in block reasons. Extended: 'waits for/on T-…' and 'depends on T-…' in the reason count; a task whose named blockers all closed is 'freed' and grouped under fm task unblock. Real line now: 5 of them wait on tasks already closed
- 2026-11-02T22:27:04Z done
- 2026-11-02T22:27:07Z committed 9ff9c524 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2682 [FEATURE S, active, 3 steps] with commits main lacks, the queue closed and the user's standing push grant on record, fm next makes fm ship the required action; wi…
- T-2113 [FEATURE M, done, 3 steps] fm genesis charter seal + privilege diff (mission-genesis brief 8, tier 3): init seals… — lesson: A seal file beside the file it seals …
- research brainstorm-20261102-m7: 393 ideas in 64 clusters, each grounded in the code: 34 built, 13 false-premise, 170 new, 176 partial. 16 clusters marked build.
- decision 2026-11-02: Recommendation: Mission 7 builds four anticipation gaps where Foreman computes what the user will need but it never reaches them (the booked next-re…
## Files touched
- plugin/tests/test_foresight.py
- plugin/lib/fmforesight.py
- plugin/lib/fmcore.py
- CHANGELOG.md
