---
id: T-1736
type: CLEAN
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcodetui.py, plugin/lib/fmdesign.py, plugin/lib/fmdoctor.py, plugin/lib/fmcli.py, plugin/tests/test_help.py, plugin/tests/test_doctor.py, plugin/tests/test_docs.py, plugin/tests/test_code_tui.py, MASTER.md, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-23T04:12:22Z
updated: 2026-10-23T04:50:28Z
batch: [T-1675, T-1686, T-1687, T-1724]
base: 82ce94f4f216fbef16bf8c5cff1e8f48c622d873
base_tree: f87f039b3e0c85a2d481bf19c1f5785f457a5d04
plan0_at: 2026-10-23T04:13:35Z
plan0_scope: [plugin/lib/fmcodetui.py, plugin/lib/fmdesign.py, plugin/lib/fmdoctor.py, plugin/lib/fmcli.py, plugin/tests/test_help.py, plugin/tests/test_doctor.py, plugin/tests/test_docs.py, plugin/tests/test_code_tui.py, MASTER.md, CHANGELOG.md]
verified: strong
---
# Small cleanups: one WCAG contrast function, unique help-tier positions, doctor's variation selectors, a MASTER.md modul…
## Raw request
> T-1675: fmcodetui.contrast repeats the WCAG maths fmdesign.contrast now provides: reuse one
> T-1686: test_help: two verbs may share a help-tier position (motion and img both took 93) with no test failing; assert positions are unique
> T-1687: fmdoctor's invisible-character check still accepts U+FE0E/FE0F after a non-ASCII character, while fmcore.plain now drops them (T-1621): make them agree
> T-1724: MASTER.md's plugin/lib list: a test that every module has a bullet
## Interpretation
Do T-1675, T-1686, T-1687, T-1724 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-1736. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-1675: fmcodetui's contrast uses fmdesign.contrast; one WCAG implementation — verify with `python3 plugin/tests/run.py test_code_tui test_design_tokens`
- [x] T-1686: test_help fails when two verbs share a help-tier position, and positions are unique — verify with `python3 plugin/tests/run.py test_help`
- [x] T-1687: fmdoctor's invisible-character check refuses U+FE0E/FE0F wherever they are, agreeing with fmcore.plain — verify with `python3 plugin/tests/run.py test_doctor`
- [x] T-1724: a test fails when a plugin/lib module has no bullet in MASTER.md's plugin/lib modules list — verify with `python3 plugin/tests/run.py test_docs test_followups`
## Non-goals
## Approach (options → choice → why)
Four independent cleanups, each test-first: (1) fmcodetui.contrast becomes a call to fmdesign.contrast (or both to one fmcore helper if importing fmdesign in the TUI is heavy: measure import time, keep the TUI's start fast). (2) test_help asserts unique tier positions; fix the collision it finds. (3) fmdoctor's check uses fmcore.plain's character rules (one source). (4) a test walks plugin/lib/*.py and requires a bullet per module under '### plugin/lib modules' in MASTER.md; add any missing bullets. Behaviour lock: CLEAN — record fm check --evidence ID --step 1 before the first edit.
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-1675: Fmcodetui.contrast repeats the WCAG maths fmdesign.contrast now provides: reuse one
2. [x] T-1686: Test_help: two verbs may share a help-tier position (motion and img both took 93) with no
3. [x] T-1687: Fmdoctor's invisible-character check still accepts U+FE0E/FE0F after a non-ASCII character
4. [x] T-1724: MASTER.md's plugin/lib list: a test that every module has a bullet
## Resume here
## Docs impact
MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_code_tui test_design_tokens` → exit 0 · Ran 210 tests in 11.0s (27 classes, 16 at a time; slowest: Fuzz 10s, Command 10s, Extract 4s) / OK [ran] [tree 548479e6002e] (2026-10-23T04:18:21Z)
- (step 2) `python3 plugin/tests/run.py test_help` → exit 0 · Ran 7 tests in 1.2s (3 classes, 16 at a time; slowest: Help 1s, PromptApprovals 1s, Rules 0s) / OK [ran] [tree 6a479b431973] (2026-10-23T04:18:51Z)
- (step 3) `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 65 tests in 2.0s (22 classes, 16 at a time; slowest: Command 2s, ViewsRepair 2s, LockProbe 1s) / OK [ran] [tree fd1237860c6f] (2026-10-23T04:19:02Z)
- (step 4) `python3 plugin/tests/run.py test_docs test_followups` → ✗ exit 1 · Ran 73 tests in 16.7s (19 classes, 16 at a time; slowest: Fences 16s, TaskLifecycle 2s, Operator 1s) / FAILED (2 classes) [ran] [tree 9ab46b68512a] (2026-10-23T04:19:44Z)
- (step 4) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 67 tests in 40.0s (15 classes, 16 at a time; slowest: Fences 34s, TaskLifecycle 18s, Site 9s) / OK [ran] [tree 865cc3d2cc79] (2026-10-23T04:21:20Z)
- (ac 1) `python3 plugin/tests/run.py test_code_tui test_design_tokens` → exit 0 · Ran 210 tests in 19.3s (27 classes, 16 at a time; slowest: Command 19s, Fuzz 18s, Extract 10s) / OK [ran] [tree 4e3fde6c23f4] (2026-10-23T04:46:20Z)
- (ac 2) `python3 plugin/tests/run.py test_help` → exit 0 · Ran 7 tests in 2.1s (3 classes, 16 at a time; slowest: Help 2s, PromptApprovals 2s, Rules 0s) / OK [ran] [tree 4e3fde6c23f4] (2026-10-23T04:46:23Z)
- (ac 3) `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 65 tests in 4.5s (22 classes, 16 at a time; slowest: Command 4s, ViewsRepair 3s, LockProbe 2s) / OK [ran] [tree 4e3fde6c23f4] (2026-10-23T04:46:29Z)
- (ac 4) `python3 plugin/tests/run.py test_docs test_followups` → exit 0 · Ran 73 tests in 10.9s (19 classes, 16 at a time; slowest: Fences 11s, TaskLifecycle 3s, Operator 2s) / OK [ran] [tree 4e3fde6c23f4] (2026-10-23T04:46:41Z)
- (ac 1) `python3 plugin/tests/run.py test_code_tui test_design_tokens` → ✗ exit 1 · Ran 210 tests in 36.1s (27 classes, 16 at a time; slowest: Fuzz 35s, Command 34s, Extract 17s) / FAILED (1 classes) [ran] [tree 7729aadd139a] (2026-10-23T04:48:04Z)
- (ac 2) `python3 plugin/tests/run.py test_help` → exit 0 · Ran 7 tests in 3.0s (3 classes, 16 at a time; slowest: Help 3s, PromptApprovals 2s, Rules 0s) / OK [ran] [tree 7729aadd139a] (2026-10-23T04:48:04Z)
- (ac 3) `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 65 tests in 5.2s (22 classes, 16 at a time; slowest: Command 5s, ViewsRepair 4s, LockProbe 2s) / OK [ran] [tree 7729aadd139a] (2026-10-23T04:48:04Z)
- (ac 4) `python3 plugin/tests/run.py test_docs test_followups` → exit 0 · Ran 73 tests in 11.7s (19 classes, 16 at a time; slowest: Fences 11s, TaskLifecycle 5s, Site 3s) / OK [ran] [tree 7729aadd139a] (2026-10-23T04:48:04Z)
- (ac 1) `python3 plugin/tests/run.py test_code_tui test_design_tokens` → exit 0 · Ran 210 tests in 8.8s (27 classes, 16 at a time; slowest: Fuzz 8s, Command 7s, Extract 4s) / OK [ran] [tree 7729aadd139a] (2026-10-23T04:48:29Z)
- (audit intent) `self: read the branch diff; contrast is one lazy call into fmdesign (4-10 ms import); five help-tier collisions renumbered and a test reads every tier from the source with a count check; the doctor's invisible check matches fmcore.plain's variation-selector rule; 24 missing MASTER.md bullets added and a test walks plugin/lib; behaviour lock recorded by the builder before the first edit` → four duplicates or gaps removed without changing behaviour beyond the help order and the doctor's stricter check [tree 7729aadd139a] (2026-10-23T04:48:29Z)
- (audit maintainer) `self: read the branch diff; contrast is one lazy call into fmdesign (4-10 ms import); five help-tier collisions renumbered and a test reads every tier from the source with a count check; the doctor's invisible check matches fmcore.plain's variation-selector rule; 24 missing MASTER.md bullets added and a test walks plugin/lib; behaviour lock recorded by the builder before the first edit` → one source each for contrast and invisible characters; MASTER.md can't silently miss a module again [tree 7729aadd139a] (2026-10-23T04:48:29Z)
- (audit edge) `self: read the branch diff; contrast is one lazy call into fmdesign (4-10 ms import); five help-tier collisions renumbered and a test reads every tier from the source with a count check; the doctor's invisible check matches fmcore.plain's variation-selector rule; 24 missing MASTER.md bullets added and a test walks plugin/lib; behaviour lock recorded by the builder before the first edit` → the doctor now WARNs on emoji with FE0F (heart, flag sequences) in instruction files; the help test parses source text, so a registration written another way fails loudly [tree 7729aadd139a] (2026-10-23T04:48:29Z)
- (audit intent) `self: read the branch diff; contrast is one lazy call into fmdesign (4-10 ms import); five help-tier collisions renumbered and a test reads every tier from the source with a count check; the doctor's invisible check matches fmcore.plain's variation-selector rule; 24 missing MASTER.md bullets added and a test walks plugin/lib` → four duplicates or gaps removed without changing behaviour beyond the help order and the doctor's stricter check [tree 7729aadd139a] (2026-10-23T04:49:24Z)
- (audit maintainer) `self: read the branch diff; contrast is one lazy call into fmdesign (4-10 ms import); five help-tier collisions renumbered and a test reads every tier from the source with a count check; the doctor's invisible check matches fmcore.plain's variation-selector rule; 24 missing MASTER.md bullets added and a test walks plugin/lib` → one source each for contrast and invisible characters; MASTER.md can't silently miss a module again [tree 7729aadd139a] (2026-10-23T04:49:24Z)
- (audit edge) `self: read the branch diff; contrast is one lazy call into fmdesign (4-10 ms import); five help-tier collisions renumbered and a test reads every tier from the source with a count check; the doctor's invisible check matches fmcore.plain's variation-selector rule; 24 missing MASTER.md bullets added and a test walks plugin/lib` → the doctor now WARNs on emoji with FE0F (heart, flag sequences) in instruction files; the help test parses source text, so a registration written another way fails loudly [tree 7729aadd139a] (2026-10-23T04:49:24Z)
## Log
- 2026-10-23T04:12:22Z created
- 2026-10-23T04:12:52Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_code_tui test_design_tokens`
- 2026-10-23T04:12:52Z criterion 1 text: T-1675: Fmcodetui.contrast repeats the WCAG maths fmdesign.contrast now provides: reuse one works → T-1675: fmcodetui's contrast uses fmdesign.contrast; one WCAG implementation
- 2026-10-23T04:12:53Z criterion 2 verify: `` → `python3 plugin/tests/run.py test_help`
- 2026-10-23T04:12:53Z criterion 2 text: T-1686: Test_help: two verbs may share a help-tier position (motion and img both took 93) with no works → T-1686: test_help fails when two verbs share a help-tier position, and positions are unique
- 2026-10-23T04:12:54Z criterion 3 verify: `` → `python3 plugin/tests/run.py test_doctor`
- 2026-10-23T04:12:54Z criterion 3 text: T-1687: Fmdoctor's invisible-character check still accepts U+FE0E/FE0F after a non-ASCII character works → T-1687: fmdoctor's invisible-character check refuses U+FE0E/FE0F wherever they are, agreeing with fmcore.plain
- 2026-10-23T04:12:54Z criterion 4 verify: `` → `python3 plugin/tests/run.py test_docs test_followups`
- 2026-10-23T04:12:54Z criterion 4 text: T-1724: MASTER.md's plugin/lib list: a test that every module has a bullet works → T-1724: a test fails when a plugin/lib module has no bullet in MASTER.md's plugin/lib modules list
- 2026-10-23T04:12:55Z set scope=['plugin/lib/fmcodetui.py', 'plugin/lib/fmdesign.py', 'plugin/lib/fmdoctor.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_help.py', 'plugin/tests/test_doctor.py', 'plugin/tests/test_docs.py', 'plugin/tests/test_code_tui.py', 'MASTER.md', 'CHANGELOG.md']
- 2026-10-23T04:13:13Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1736.builder.md
- 2026-10-23T04:13:34Z focused
- 2026-10-23T04:38:55Z merged worktree-agent-aeb85f383edbbca80 (8 file(s))
- 2026-10-23T04:38:55Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aeb85f383edbbca80
- 2026-10-23T04:45:58Z focused
- 2026-10-23T04:46:54Z scope: merged lane files (fmcodetui.py, fmdoctor.py, fmcli.py tier numbers, test_help.py, test_docs.py, MASTER.md, CHANGELOG.md)
- 2026-10-23T04:50:23Z done
- 2026-10-23T04:50:28Z committed ed44de6d (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1731 [FIX M, active, 4 steps] Lane and close friction: finish --commit and shared files, CLEAN behaviour-lock in builder briefs, check --affected ski…
- T-1737 [FEATURE S, active, 2 steps] fm shot presets: --profile tv|eink|car|wrist and --reduced-motion, also in fm stories
- T-1585 [SECURITY M, done, 7 steps] Batch: Guard: interpreter one-liners that read…; Guard: env -u CLAUDECODE (or CLAUDE_COD…; Guard gaps (noticed in T-156… — lesson: Rep…
- decision 2026-10-21: Revert and drop T-1441 (auto-accepting Foreman's own plugins in the supply check)
- the similar finished task took 7 steps
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_doctor.py
## Behaviour lock
none: this lane started before T-1731 (T-1712) added the behaviour-lock line to CLEAN builder briefs; each change is covered by its own test, and the touched suites (test_code_tui, test_design_tokens, test_help, test_doctor, test_docs) pass after the merge
## Lessons
- A doc list that must cover every module needs a test that walks the modules
## Plan gaps
- failed first: step 4 T-1724: MASTER.md's plugin/lib list: a test that every module has a bullet
## Files touched
- plugin/tests/test_code_tui.py
- plugin/tests/test_help.py
- plugin/tests/test_doctor.py
- plugin/tests/test_docs.py
- plugin/lib/fmcodetui.py
- plugin/lib/fmcli.py
- plugin/lib/fmdoctor.py
- MASTER.md
- CHANGELOG.md
