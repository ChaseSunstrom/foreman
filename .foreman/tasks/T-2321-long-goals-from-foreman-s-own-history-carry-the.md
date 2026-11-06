---
id: T-2321
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-31T11:39:54Z
updated: 2026-10-31T11:57:02Z
base: d818eeff58dfc4ad4ce1cbee00a27c4534fcca89
base_tree: 0da44ea593565e33508fe1ebc2df1446a6321ced
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-10-31T11:39:55Z
plan0_scope: []
verified: strong
---
# Long goals from Foreman's own history carry the task brief's interpretation and acceptance criteria (text only)
## Raw request
> Long goals from Foreman's own history carry the task brief's interpretation and acceptance criteria (text only)
## Interpretation
A replayed goal is only its commit subjects, while the hidden checks test the brief's contract; when the source repo is this project's own and the task's brief exists, the goal should read like the ticket a session had: the brief's Interpretation and its acceptance criteria's text, never their verify commands.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm exam long gen on the project's own repo appends the task brief's Interpretation and acceptance-criteria text to the goal (c.plain'd, bounded), with no verify command or test path; a repo with no brief for the id keeps the subject-only goal — verify with `python3 plugin/tests/run.py test_long`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red test: a fixture task with a brief whose AC has a verify command: the goal holds the AC text and not the command; then add the brief lookup to gen
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_long -k briefs_ticket` → ✗ exit 1 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: Long 0s) / FAILED (1 classes: test_long.Long) [ran] [tree d8e8151ac63c] (2026-10-31T11:40:21Z)
- `python3 plugin/tests/run.py test_long -k briefs_ticket` → ✗ exit 1 · Ran 1 tests in 3.3s (1 classes, 16 at a time; slowest: Long 1s) / FAILED (1 classes: test_long.Long) (start tree + this task's tests) [ran] [tree 86c24ce52569] (2026-10-31T11:41:12Z)
- `python3 plugin/tests/run.py test_long -k briefs_ticket` → exit 0 · Ran 1 tests in 2.2s (1 classes, 16 at a time; slowest: Long 2s) / OK [ran] [tree 86c24ce52569] (2026-10-31T11:41:12Z)
- (step 1) `python3 plugin/tests/run.py test_long` → exit 0 · Ran 37 tests in 51.5s (7 classes, 16 at a time; slowest: Long 51s, Approvals 3s, AuditPrep 2s) / OK [ran] [tree 86c24ce52569] (2026-10-31T11:42:08Z)
- (ac 1) `python3 plugin/tests/run.py test_long` → exit 0 · Ran 37 tests in 52.3s (7 classes, 16 at a time; slowest: Long 52s, Approvals 3s, AuditPrep 2s) / OK [ran] [tree f5a6c2fdf247] (2026-10-31T11:43:11Z)
- (audit intent) `self-review: _ticket runs only when src is this project's root, reads the brief through c.find_brief, takes the Interpretation (whitespace-joined, fitted to 600) and up to 8 criteria with their '— verify with' part removed (fitted to 200), all c.plain'd; both arms get the same goal text` → a replayed goal states the contract its session was given, so the checks are passable from the text more often [tree f5a6c2fdf247] (2026-10-31T11:43:11Z)
- (audit edge) `self-review: _ticket runs only when src is this project's root, reads the brief through c.find_brief, takes the Interpretation (whitespace-joined, fitted to 600) and up to 8 criteria with their '— verify with' part removed (fitted to 200), all c.plain'd; both arms get the same goal text` → no brief, an empty Interpretation or no criteria add nothing; an id from another repo never looks up this project's tasks; verify commands (which name the tests) never reach the goal [tree f5a6c2fdf247] (2026-10-31T11:43:11Z)
- (audit self) `self-review: _ticket runs only when src is this project's root, reads the brief through c.find_brief, takes the Interpretation (whitespace-joined, fitted to 600) and up to 8 criteria with their '— verify with' part removed (fitted to 200), all c.plain'd; both arms get the same goal text` → no findings [tree f5a6c2fdf247] (2026-10-31T11:43:11Z)
## Log
- 2026-10-31T11:39:54Z created
- 2026-10-31T11:39:54Z focused
- 2026-10-31T11:39:55Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-10-31T11:42:16Z scope: plugin/lib/fmlong.py (_ticket, gen), plugin/tests/test_long.py, MASTER.md, CHANGELOG.md
- 2026-10-31T11:44:35Z done
- 2026-10-31T11:44:39Z committed f6476a07 (4 files)
- 2026-10-31T11:44:52Z guard authorization added: publish
- 2026-10-31T11:57:02Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2162 [FEATURE L, dropped, 0 steps] Long-horizon exam tier, the deciding end-of-run score: replay real repos (Foreman's own…
- decision 2026-10-30: [cites: the user's steer 2026-10-30: standing rules for the rest of the genesis run] Long-horizon tier is the deciding end-of-run score for every ca…
- T-1870 [FEATURE M, done, 3 steps] Fm inbox ticket --post T-xxxx posts the closing commit back to its source issue — lesson: an outward write needs a claim under the lock…
- T-2304 [FIX M, done, 2 steps] Long-tier goals are passable from their text: checks only from the task's own commits, the goal names the new names and flags the checks re…
- similar past tasks were M: consider --tier M
## Lessons
- A replayed goal should carry what the original worker was told, no more: the ticket's text, not its tests
## Plan gaps
- failed first: step 1 Red test: a fixture task with a brief whose AC has a verify command: the goal holds the AC text and…
## Files touched
- plugin/tests/test_long.py
- plugin/lib/fmlong.py
- MASTER.md
- CHANGELOG.md
