---
id: T-2682
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: genesis
created: 2026-11-02T22:12:01Z
updated: 2026-11-02T22:35:40Z
builder_model: sonnet
base: 1191a91c6b11702e73c1a8d4d8062af4a8661cdb
base_tree: 7196ba08899006d0fb06bc79a123ee7423d619e8
predict_minutes: 7
predict_attempts: 1
plan0_at: 2026-11-02T22:12:59Z
plan0_scope: []
lane_stop: merged 2026-11-02T22:33:15Z
verified: strong
---
# with commits main lacks, the queue closed and the user's standing push grant on record, fm next makes fm ship the required action; without the grant, one line names the count and the command
## Raw request
> FEATURE: when commits on the work branch are missing from main and the queue is closed, fm next makes fm ship the required action under the user's standing push grant (a decision citing it), else one line names the count and the command; silent when nothing waits
> CONTEXT: Genesis gen-3 Mission 7 (#3 anticipation), gen-3/mission-anticipation.md
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm next names fm ship when the branch has commits main lacks, nothing runnable is open and decisions.md holds a user-steer push grant; without the grant it prints the count and the command; with nothing waiting it says nothing — verify with `python3 plugin/tests/run.py test_ship_next`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test
2. [x] the ship step in fm next
3. [x] CHANGELOG
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_ship_next 2>&1 | tail -15` → ✗ exit 1 · Ran 5 tests in 3.1s (1 classes, 16 at a time; slowest: ShipNext 2s) / FAILED (1 classes: test_ship_next.ShipNext) [ran] [tree 2c44cf61b0b6] [world 2f1906870a] (2026-11-02T22:13:59Z)
- (ac 1) `python3 plugin/tests/run.py test_ship_next 2>&1 | tail -15` → exit 0 · Ran 6 tests in 3.4s (1 classes, 16 at a time; slowest: ShipNext 3s) / OK [ran] [tree 74d378f310bf] [world 2f1906870a] (2026-11-02T22:14:09Z)
- (step 1) `python3 plugin/tests/run.py test_ship_next 2>&1 | tail -15` → exit 0 · Ran 6 tests in 3.4s (1 classes, 16 at a time; slowest: ShipNext 3s) / OK [ran] [tree 74d378f310bf] [world 2f1906870a] (2026-11-02T22:14:09Z)
- (step 1) `python3 plugin/tests/run.py test_ship_next` → exit 0 · Ran 6 tests in 2.8s (1 classes, 16 at a time; slowest: ShipNext 2s) / OK [ran] [tree 74d378f310bf] [world 2f1906870a] (2026-11-02T22:14:14Z)
- (step 2) `python3 plugin/tests/run.py test_ship_next` → exit 0 · Ran 6 tests in 2.7s (1 classes, 16 at a time; slowest: ShipNext 2s) / OK [ran] [tree 74d378f310bf] [world 2f1906870a] (2026-11-02T22:14:17Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_core test_ship_next && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [20.32s] [ran] [tree 74d378f310bf] [world 2f1906870a] (2026-11-02T22:14:49Z)
- (ac 1) `python3 plugin/tests/run.py test_ship_next` → exit 0 · Ran 8 tests in 1.9s (1 classes, 16 at a time; slowest: ShipNext 2s) / OK [ran] [tree 9cfdfd32a988] [world 2f1906870a] (2026-11-02T22:35:17Z)
- (step 3) `python3 plugin/tests/run.py test_ship_next test_core` → exit 0 · Ran 146 tests in 6.4s (29 classes, 16 at a time; slowest: ConfidenceRoutes 6s, BriefIndex 2s, ShipNext 2s) / OK [ran] [tree 9cfdfd32a988] [world 2f1906870a] (2026-11-02T22:35:17Z)
- (audit edge) `read ship_waiting and the next_for hook after the merge; ran it on the real repo: (8, True) with 8 first-parent commits since the last ship; found and fixed the tree-diff rule that main's own site/ pushes break, the bare 'fm ship' action that fm ship itself would refuse, and the negated-steer match` → no shipped ref falls back to git cherry by patch (a re-picked commit under another sha isn't waiting, tested); a shipped ref that isn't an ancestor (rebase) falls back too; open work silences it (tested) [tree 9cfdfd32a988] (2026-11-02T22:35:17Z)
- (audit adversary) `read ship_waiting and the next_for hook after the merge; ran it on the real repo: (8, True) with 8 first-parent commits since the last ship; found and fixed the tree-diff rule that main's own site/ pushes break, the bare 'fm ship' action that fm ship itself would refuse, and the negated-steer match` → the grant comes only from decisions citing a user steer (steer_rules); a forbidding steer voids it; the action still routes through fm ship's full gates and its publish grant, so nothing pushes from fm next itself [tree 9cfdfd32a988] (2026-11-02T22:35:17Z)
- (audit self) `read ship_waiting and the next_for hook after the merge; ran it on the real repo: (8, True) with 8 first-parent commits since the last ship; found and fixed the tree-diff rule that main's own site/ pushes break, the bare 'fm ship' action that fm ship itself would refuse, and the negated-steer match` → no findings [tree 9cfdfd32a988] (2026-11-02T22:35:17Z)
## Log
- 2026-11-02T22:12:01Z created
- 2026-11-02T22:12:37Z planned from capture
- 2026-11-02T22:12:39Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2682.builder.md
- 2026-11-02T22:12:58Z focused
- 2026-11-02T22:12:59Z predicted from its closes: 7 min, 1 attempt(s)
- 2026-11-02T22:33:15Z merged worktree-agent-a89dad37b45a2fa6c (2 file(s))
- 2026-11-02T22:33:15Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a89dad37b45a2fa6c
- 2026-11-02T22:33:16Z focused
- 2026-11-02T22:35:08Z steer: the builder's whole-tree diff would always read 'waiting' here (main takes fm genesis live's site/ pushes HEAD never has); now counts what fm ship would pick (first-parent since refs/foreman/shipped, else git cherry). The action names the full path because fm ship refuses without the active task's publish grant. A steer that says never/don't push to main voids the grant
- 2026-11-02T22:35:08Z scope: CHANGELOG.md
- 2026-11-02T22:35:37Z done
- 2026-11-02T22:35:40Z committed 33b4ee6f (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- T-1943 [FEATURE M, done, 2 steps] Fm ship lands finished commits on the remote's main: fetch, scratch worktree at the fetche — lesson: git cherry matches by patch, so co…
- research mission-20261101-105530.pack: (none given: improve the project in every way that matters to its user) [stale: site/genesis/index.html changed since it was writt…
- decision 2026-11-02: Recommendation: Mission 7 builds four anticipation gaps where Foreman computes what the user will need but it never reaches them (the booked next-re…
## Files touched
- plugin/tests/test_ship_next.py
- plugin/lib/fmcore.py
- CHANGELOG.md
