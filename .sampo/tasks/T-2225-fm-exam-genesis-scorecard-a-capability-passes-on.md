---
id: T-2225
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T22:39:15Z
updated: 2026-10-31T05:49:23Z
group: exam grading robustness
base: d325c4de16d9491ea252e7cc1bd1f117c4161465
base_tree: 48f7ebb63acbb78f33e180d2d9be603e7544f18d
plan0_at: 2026-10-31T04:44:24Z
plan0_scope: []
verified: strong
---
# fm exam/genesis scorecard: a capability passes on a --lang-narrowed run (3 python…
## Raw request
> fm exam/genesis scorecard: a capability passes on a --lang-narrowed run (3 python scenarios read as pass); a pass should need each language of the draw graded, or say the languages it covers
## Interpretation
fmgenesis.scorecard passes a capability on 3 graded held-out scenarios at or over the bar, whatever their languages, so a --lang python run passes #1 for every language. Ids are kind-lang-hash, so the language is known per result.
## Assumptions (confidence)
## Acceptance criteria
- [x] a capability whose graded held-out results cover only some of fmexam.LANGS is partial, not pass, and its row names the languages covered and missing; one with every language graded at or over the bar still passes — verify with `python3 plugin/tests/run.py test_genesis test_exam`
## Non-goals
## Approach (options → choice → why)
1) like T-2217's per-kind rule: a row lists the languages its graded results cover (row 'langs'), and pass needs at least one graded result in each of fmexam.LANGS; else partial, with why 'no graded <langs> scenarios yet'. For the draft-genesis pool (#13), apply it only if its ids carry a language. 2) require the run's own --lang draw only — rejected: a narrowed draw is exactly the gap. 3) weight by language — rejected: more machinery, same honesty. Choice 1. The fm exam scorecard text and the §8 report show the covered languages.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests: 3 python-only results stay partial; all six languages pass; row langs and why
2. [x] scorecard per-language rule and the scorecard text
3. [x] CHANGELOG, MASTER scorecard line
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_genesis test_exam 2>&1 | grep -E "^(FAIL|ERROR)|Ran|OK" | head -20` → ✗ exit 1 · Ran 183 tests in 81.2s (26 classes, 16 at a time; slowest: ExamAuthors 81s, ExamGen 61s, GenesisRead 25s) / FAILED (2 classes) [ran] [tree ae1778abc3c1] (2026-10-31T04:47:48Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis test_exam 2>&1 | grep -E "^(FAIL|ERROR)|Ran|OK|Error" | head -20` → ✗ exit 1 · Ran 183 tests in 113.2s (26 classes, 16 at a time; slowest: ExamAuthors 113s, ExamGen 73s, GenesisRead 35s) / FAILED (1 classes) [ran] [tree da7465c63d8c] (2026-10-31T04:50:16Z)
- (step 1) `python3 plugin/tests/run.py test_genesis test_exam` → exit 0 · Ran 183 tests in 94.3s (26 classes, 16 at a time; slowest: ExamAuthors 93s, ExamGen 70s, GenesisRead 36s) / OK [ran] [tree 518ffbecc6f9] (2026-10-31T04:52:15Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_docs test_genesis && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [45.19s] [ran] [tree 518ffbecc6f9] (2026-10-31T04:53:39Z)
- (step 2) `python3 plugin/tests/run.py test_genesis test_exam` → exit 0 · Ran 185 tests in 80.6s (26 classes, 16 at a time; slowest: ExamAuthors 80s, ExamGen 62s, GenesisRead 29s) / OK [ran] [tree bf384c4b2ce7] (2026-10-31T05:08:01Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_dirty_at_focus test_docs test_genesis test_map test_round_g && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [32.76s] [ran] [tree bf384c4b2ce7] (2026-10-31T05:08:54Z)
- `python3 plugin/tests/run.py test_genesis` → ✗ exit 1 · Ran 150 tests in 8.5s (17 classes, 16 at a time; slowest: GenesisRead 7s, GenesisCheck 6s, GenesisDrift 6s) / FAILED (2 classes) (start tree + this task's tests) [ran] [tree 3764f6f58280] (2026-10-31T05:33:44Z)
- `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 150 tests in 7.6s (17 classes, 16 at a time; slowest: GenesisRead 7s, GenesisCheck 6s, GenesisDrift 6s) / OK [ran] [tree 3764f6f58280] (2026-10-31T05:33:44Z)
- (step 1) `python3 plugin/tests/run.py test_genesis test_exam` → exit 0 · Ran 188 tests in 66.4s (27 classes, 16 at a time; slowest: ExamAuthors 66s, ExamGen 52s, GenesisRead 16s) / OK [ran] [tree 3764f6f58280] (2026-10-31T05:34:50Z)
- (step 2) `python3 plugin/tests/run.py test_genesis test_exam` → exit 0 · Ran 188 tests in 66.2s (27 classes, 16 at a time; slowest: ExamAuthors 66s, ExamGen 52s, GenesisRead 16s) / OK [ran] [tree 3764f6f58280] (2026-10-31T05:35:57Z)
- (step 3) `grep -c T-2225 MASTER.md CHANGELOG.md` → ✗ exit 1 · MASTER.md:0 / CHANGELOG.md:0 [ran] [tree 3764f6f58280] (2026-10-31T05:35:57Z)
- `python3 plugin/tests/run.py test_genesis` → ✗ exit 1 · Ran 153 tests in 13.8s (17 classes, 16 at a time; slowest: GenesisRead 12s, GenesisCheck 11s, GenesisDrift 10s) / FAILED (2 classes) (start tree + this task's tests) [ran] [tree c552faee2d77] (2026-10-31T05:42:13Z)
- `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 153 tests in 12.2s (17 classes, 16 at a time; slowest: GenesisRead 12s, GenesisCheck 11s, GenesisDrift 9s) / OK [ran] [tree c552faee2d77] (2026-10-31T05:42:13Z)
- (step 1) `python3 plugin/tests/run.py test_genesis test_exam test_docs` → exit 0 · Ran 273 tests in 71.0s (49 classes, 16 at a time; slowest: ExamAuthors 71s, ExamGen 56s, GenesisRead 20s) / OK [ran] [tree c552faee2d77] (2026-10-31T05:43:24Z)
- (step 2) `python3 plugin/tests/run.py test_genesis test_exam test_docs` → exit 0 · Ran 273 tests in 72.0s (49 classes, 16 at a time; slowest: ExamAuthors 72s, ExamGen 56s, GenesisRead 20s) / OK [ran] [tree c552faee2d77] (2026-10-31T05:44:36Z)
- (step 3) `grep -c T-2225 MASTER.md CHANGELOG.md` → exit 0 · MASTER.md:1 / CHANGELOG.md:1 [ran] [tree c552faee2d77] (2026-10-31T05:44:37Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis test_exam` → exit 0 · Ran 191 tests in 72.9s (27 classes, 16 at a time; slowest: ExamAuthors 73s, ExamGen 57s, GenesisRead 19s) / OK [ran] [tree 802db5f26117] (2026-10-31T05:45:58Z)
- (audit intent) `self + one fm-reviewer pass (1 medium, 4 low; all fixed with tests)` → a capability passes only with a graded result in every language its spec drew, so a --lang-narrowed run can't pass for all languages; rows list languages and why names the closing command (test_genesis red-to-green) [tree 802db5f26117] (2026-10-31T05:45:58Z)
- (audit adversary) `self + one fm-reviewer pass (1 medium, 4 low; all fixed with tests)` → a score can't be met in one language and read as all: ids from unknown languages don't count toward graded or closed [tree 802db5f26117] (2026-10-31T05:45:58Z)
- (audit edge) `self + one fm-reviewer pass (1 medium, 4 low; all fixed with tests)` → a python-only spec passes on python; no spec falls back to every exam language; a malformed id never crashes the scorecard; #13's pass path is exercised over all its languages [tree 802db5f26117] (2026-10-31T05:45:58Z)
## Log
- 2026-10-30T22:39:15Z created
- 2026-10-31T04:44:07Z set tier=M
- 2026-10-31T04:44:08Z planned: it has criteria and steps
- 2026-10-31T04:44:09Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2225.builder.md
- 2026-10-31T04:44:23Z focused
- 2026-10-31T05:41:45Z merged worktree-agent-a96877a6908206464 (4 file(s))
- 2026-10-31T05:41:45Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a96877a6908206464
- 2026-10-31T05:41:45Z focused
- 2026-10-31T05:44:45Z scope: plugin/lib/fmgenesis.py (scorecard, _lang), plugin/tests/test_genesis.py, MASTER.md, CHANGELOG.md
- 2026-10-31T05:46:21Z done
- 2026-10-31T05:46:23Z committed c4fb8f08 (1 file)
- 2026-10-31T05:46:29Z guard authorization added: publish
- 2026-10-31T05:49:23Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2097 [FEATURE M, done, 3 steps] fm exam scorecard: per §2 capability, the held-out split's pass rate from graded runs,… — lesson: A gate that reads hand-written fixtur…
- T-2112 [FEATURE M, done, 4 steps] fm genesis exam: #13's held-out exam (draft kinds graded by cover; G-tower as a genesis session arm) — lesson: Score an arm both strict…
- research T-2097-review: Verdict** — approve with nits. The scorecard logic is correct on the cases I traced. The real `fm genesis exam` path that feeds #13 has no test. …
- decision 2026-10-30: T-2112: #13's draft kinds live in fmgenesis (fm genesis exam) reusing fmexam.draw/render and cover; G-tower is a 'genesis' session arm on fmexam's d…
## Lessons
- A coverage bar must come from what was asked (the spec's draw), not from everything the tool supports, or a narrow project can never pass
## Plan gaps
- failed first: step 3 CHANGELOG, MASTER scorecard line
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
- MASTER.md
- CHANGELOG.md
- plugin/lib/fmbench.py
- plugin/lib/fmcli.py
- plugin/lib/fmhooks.py
- plugin/lib/fmlong.py
- plugin/lib/fmrecall.py
- plugin/lib/fmrelease.py
- plugin/skills/genesis/SKILL.md
- plugin/tests/test_hooks.py
- plugin/tests/test_long.py
- plugin/tests/test_recall.py
- plugin/tests/test_ship.py
