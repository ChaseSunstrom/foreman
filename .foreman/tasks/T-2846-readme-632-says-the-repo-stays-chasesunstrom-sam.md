---
id: T-2846
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-03T21:35:43Z
updated: 2026-11-03T22:17:10Z
base: ede1c14514e70a93773cd61853f6c4f508eef36c
base_tree: a153b15882073efb3748ae6689519c605a44a5ee
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-03T22:16:05Z
plan0_scope: []
verified: strong
unproven: [docs]
---
# README ~632 says the repo stays ChaseSunstrom/sampo 'until it is renamed', stale since…
## Raw request
> FIX: README ~632 says the repo stays ChaseSunstrom/sampo 'until it is renamed', stale since the repo became ChaseSunstrom/sampo (T-2811)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] README's upgrade paragraph names ChaseSunstrom/sampo as the repo, without 'until it is renamed' — verify with `! grep -q 'until it is renamed' README.md`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] reword the sentence
## Resume here
## Docs impact
README.md
## Verification evidence
- (step 1) `! grep -q 'until it is renamed' README.md` → exit 0 · (no output) [ran] [tree bbad91c5a1b9] [world 2f1906870a] (2026-11-03T22:16:13Z)
- (ac 1) `! grep -q 'until it is renamed' README.md` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T22:16:13Z [ran] [tree bbad91c5a1b9] [world 2f1906870a] (2026-11-03T22:16:23Z)
- `python3 plugin/tests/run.py test_docs test_rename_scan` → ✗ exit 1 · Ran 117 tests in 8.5s (26 classes, 16 at a time; slowest: Fences 8s, RenameScan 3s, DocsProof 2s) / FAILED (1 classes: test_rename_scan.RenameScan) [ran] [tree bbad91c5a1b9] [world 2f1906870a] (2026-11-03T22:16:23Z)
- `python3 plugin/tests/run.py test_docs test_rename_scan` → ✗ exit 1 · Ran 117 tests in 8.4s (26 classes, 16 at a time; slowest: Fences 8s, RenameScan 3s, DocsProof 2s) / FAILED (1 classes: test_rename_scan.RenameScan) [ran] [tree bbad91c5a1b9] [world 2f1906870a] (2026-11-03T22:16:35Z)
- `python3 plugin/tests/run.py test_docs test_rename_scan` → exit 0 · Ran 117 tests in 9.8s (26 classes, 16 at a time; slowest: Fences 9s, RenameScan 5s, DocsProof 3s) / OK [ran] [tree 4d989dd254ba] [world 2f1906870a] (2026-11-03T22:16:58Z)
- (audit intent) `self: the sentence now names the current repo and says GitHub forwards links using the old name, without spelling the old address (the rename ratchet counts it); no other surface carries the phrase` → the upgrade note no longer implies a pending rename [tree 4d989dd254ba] (2026-11-03T22:16:58Z)
- (audit edge) `self: the sentence now names the current repo and says GitHub forwards links using the old name, without spelling the old address (the rename ratchet counts it); no other surface carries the phrase` → GitHub forwards renamed repos for git and web; the old Pages URL doesn't forward, and no line here points at it [tree 4d989dd254ba] (2026-11-03T22:16:58Z)
- (audit self) `self: the sentence now names the current repo and says GitHub forwards links using the old name, without spelling the old address (the rename ratchet counts it); no other surface carries the phrase` → no findings [tree 4d989dd254ba] (2026-11-03T22:16:58Z)
## Log
- 2026-11-03T21:35:43Z created
- 2026-11-03T22:16:04Z set tier=S
- 2026-11-03T22:16:05Z planned: it has criteria and steps
- 2026-11-03T22:16:05Z focused
- 2026-11-03T22:16:05Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-03T22:17:08Z done
- 2026-11-03T22:17:10Z committed f228f2c9 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2811 [FIX S, done, 3 steps] FIX: links point at the renamed repo: chasesunstrom.github.io/foreman now 404s since the repo became ChaseSunstrom/sampo, so README, site, …
- T-2768 [CLEAN M, done, 3 steps] The skills, commands and output style say Sampo (T-2742 step 5b): every prose Foreman in plugin/skills, plugin/commands and plugin/output…
- T-2807 [CLEAN M, done, 3 steps] The foreman-ui mod says Sampo on screen: pane, band, toasts, README and tools text (T-2742 step 5) — lesson: Merge overlapping renames by…
- decision 2026-11-03: [outward] [cites: user steer: read SAMPO.md (plugin foreman@foreman becomes sampo@sampo; nothing a user already has may break)] [check: pending T-27…
## Regression test
none: a one-sentence docs fix; test_rename_scan's OLD_ADDR check already counts links to the old address, and the criterion's grep pins the stale phrase out
## Files touched
- README.md
