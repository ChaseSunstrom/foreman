---
id: T-1619
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmplaybooks.py, plugin/lib/fmcli.py, plugin/tests/test_playbook_evals.py, CHANGELOG.md, MASTER.md]
depends_on: [T-1618]
source: user
created: 2026-10-22T20:56:57Z
updated: 2026-10-22T23:41:04Z
base: e3bf1b799e9e5c07a482fa3aa14e92afae141f5f
base_tree: 49352ce99102552dbb528089bd20b03df9cc1ae7
plan0_at: 2026-10-22T23:38:15Z
plan0_scope: [plugin/lib/fmplaybooks.py, plugin/tests/test_playbook_evals.py, CHANGELOG.md]
verified: strong
---
# fm playbooks eval --ablate: each section's share of the lift, dropped one at a time
## Raw request
> fm playbooks eval --ablate: each section's share of the lift, dropped one at a time
## Interpretation
fm playbooks eval NAME --ablate drops each top-level section of the playbook in turn, reruns the lift and reports each section's share; a section with zero share is flagged as a candidate to cut (the ratchet keeps playbooks small).
## Assumptions (confidence)
## Acceptance criteria
- [x] ablation lists each section with its share and flags a zero-share section — verify with `python3 plugin/tests/run.py test_playbook_evals.Ablate`
## Non-goals
## Approach (options → choice → why)
Options: ablate by paragraph (too many runs), by heading (natural units), or by sentence. Choice: by heading: a few runs, and the result maps to an edit someone can make.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test with a playbook holding one useless section
2. [x] split by headings, rerun lift per drop
3. [x] table, zero share flagged
## Resume here
## Docs impact
MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_playbook_evals.Ablate` → red as expected (exit 1) · Ran 2 tests in 0.4s (1 classes, 16 at a time; slowest: Ablate 0s) / FAILED (1 classes) [ran] [tree 88a62c4e0c9a] (2026-10-22T23:38:26Z)
- (step 2) `python3 plugin/tests/run.py test_playbook_evals test_docs` → exit 0 · Ran 75 tests in 12.4s (17 classes, 16 at a time; slowest: Fences 12s, TaskLifecycle 4s, TaskDocsDrift 2s) / OK [ran] [tree b85f2fe3c25f] (2026-10-22T23:39:07Z)
- (step 3) `python3 plugin/tests/run.py test_playbook_evals test_docs` → exit 0 · Ran 75 tests in 13.5s (17 classes, 16 at a time; slowest: Fences 13s, TaskLifecycle 3s, Site 2s) / OK [ran] [tree b85f2fe3c25f] (2026-10-22T23:39:22Z)
- (ac 1) `python3 plugin/tests/run.py test_playbook_evals.Ablate` → exit 0 · Ran 3 tests in 1.9s (1 classes, 16 at a time; slowest: Ablate 1s) / OK [ran] [tree 83954d14bc7d] (2026-10-22T23:39:40Z)
- (ac 1) `python3 plugin/tests/run.py test_playbook_evals.Ablate` → exit 0 · Ran 3 tests in 2.9s (1 classes, 16 at a time; slowest: Ablate 1s) / OK [ran] [tree 83954d14bc7d] (2026-10-22T23:39:46Z)
- (audit intent) `self-review of the ablate diff: sections() skips ## inside fences (tested), the no-playbook pass runs once and is reused, --real's estimate counts 2+sections passes per brief; ran it on verify/tdd-workflow (Plan Handoff carries the 'untrusted' brief; redundant sections read zero, which the output now says)` → --ablate lists each top-level section with its share of the lift and flags zero-share sections as cut candidates [tree 83954d14bc7d] (2026-10-22T23:39:46Z)
- (audit edge) `self-review of the ablate diff: sections() skips ## inside fences (tested), the no-playbook pass runs once and is reused, --real's estimate counts 2+sections passes per brief; ran it on verify/tdd-workflow (Plan Handoff carries the 'untrusted' brief; redundant sections read zero, which the output now says)` → a playbook with no ## sections says so; headings inside code fences are ignored; two sections repeating each other both read zero alone, and the flag says 'or another section repeats it' [tree 83954d14bc7d] (2026-10-22T23:39:46Z)
- (audit self) `self-review of the ablate diff: sections() skips ## inside fences (tested), the no-playbook pass runs once and is reused, --real's estimate counts 2+sections passes per brief; ran it on verify/tdd-workflow (Plan Handoff carries the 'untrusted' brief; redundant sections read zero, which the output now says)` → no findings [tree 83954d14bc7d] (2026-10-22T23:39:46Z)
## Log
- 2026-10-22T20:56:57Z created
- 2026-10-22T20:56:58Z set scope=['plugin/lib/fmplaybooks.py', 'plugin/tests/test_playbook_evals.py', 'CHANGELOG.md']
- 2026-10-22T20:56:59Z split from T-1522 (L) by recon; works from Claude Code too (an fm verb, /foreman: command, skill or the foreman-ui mod)
- 2026-10-22T20:56:59Z set depends_on=['T-1618']
- 2026-10-22T21:29:48Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_playbook_evals.Ablate`
- 2026-10-22T21:30:12Z criterion 1 text: ablation lists each section with its share and flags a zero-share section — verify with python3 plugin/tests/run.py test_playbook_evals.Ablate → ablation lists each section with its share and flags a zero-share section
- 2026-10-22T23:38:14Z focused
- 2026-10-22T23:38:25Z set scope=['plugin/lib/fmplaybooks.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_playbook_evals.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-22T23:41:01Z done
- 2026-10-22T23:41:04Z committed 28249367 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1505-review: Verdict: approve with nits.** I found no HIGH issues and no failure of the acceptance criteria. I had no shell, so I read the code and ran nothin…
- T-1618 [FEATURE M, done, 3 steps] fm playbooks eval: held-out brief sets and a with/without lift on the scripted fake model — lesson: An eval whose checks copy the playb…
- research brainstorm-skills-20261022: The cause is mostly structural. Claude Code skills trigger on user words, while Foreman's hooks and rules already hand the model the…
- decision 2026-10-21: T-1298: refusals for programs the guard couldn't read drop the --allow system route instead of keeping it
- similar past tasks were M: consider --tier M
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/lib/fmplaybooks.py, plugin/tests/test_playbook_evals.py; re-ground the plan against them before editing
## Lessons
- Single-section ablation can't see redundancy: two sections saying the same thing each show zero share
## Files touched
- plugin/tests/test_playbook_evals.py
- plugin/lib/fmcli.py
- plugin/lib/fmplaybooks.py
- CHANGELOG.md
- MASTER.md
