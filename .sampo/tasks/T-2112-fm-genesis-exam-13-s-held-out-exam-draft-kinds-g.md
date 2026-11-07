---
id: T-2112
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-30T06:42:29Z
updated: 2026-10-30T07:22:11Z
base: 82b80338b98d0ef52dd6623ee4f780e640d84ec9
base_tree: bbf97c416fd40e77cfab0c16447dfdf7595d720f
plan0_at: 2026-10-30T06:42:40Z
plan0_scope: []
verified: strong
---
# fm genesis exam: #13's held-out exam (draft kinds graded by cover; G-tower as a genesis session arm)
## Raw request
> fm genesis exam: #13's held-out exam (draft kinds graded by cover; G-tower as a genesis session arm)
## Interpretation
Mission 2 brief 7 (mission-genesis.md §Exam): #13 needs its own held-out exam. Kinds: G-line (a generated project + 'make this great' + a planted MUST/NEVER), G-none (nothing given; the draft must name what it assumed), G-sweep ('super improve this'; no §2 capability without an exam kind), G-tower (planted defects; one Genesis generation closes them). Each draft kind is graded deterministically: cover(gen-0 + planted lines, draft) is empty, the scenario's planted defect kind is in the draft's §2 kinds, plus the kind's own check. The checklist (gen-0) never reaches the writer: the draft runs on a temp Project for the scenario repo.
## Assumptions (confidence)
## Acceptance criteria
- [x] oracle closes every scenario, empty none, and the oracle minus any one gen-0 MUST/NEVER fails — verify with `python3 plugin/tests/run.py test_genesis.GenesisExam`
- [x] the genesis arm closes held-out line/none/sweep scenarios, the draft names what it assumed, and gen-0 never reaches the writer — verify with `python3 plugin/tests/run.py test_genesis.GenesisExam`
- [x] fm exam run --agent genesis prompts one Genesis generation; --request overrides the prompt and is recorded — verify with `python3 plugin/tests/run.py test_exam`
## Non-goals
## Approach (options → choice → why)
Complete version: four kinds x 9 scenarios (3 held out, fmexam.draw's hash), four arms (genesis = draft(), plain = a bare child with no template, oracle = the checklist itself, empty), exam-of-the-exam tests (oracle 100%, empty 0, any one MUST/NEVER removed fails, held-out never in train, no leak), lines in exam.jsonl (agent draft-ARM) the site already lists, cost per arm. Approaches: (a) new fmexam kinds 'line/none/sweep' inside fmexam's render/grade (grade is defect-shaped: no fit); (b) fm genesis exam in fmgenesis reusing fmexam.draw/render and cover (chosen: smallest, the scorer exists); (c) a model judge grading drafts (rejected: non-deterministic, selection needs exact counts); (d) G-tower as its own scenario generator (rejected: fmexam's defect scenarios already are 'a project with planted gaps'; a genesis session arm reuses them). G-sweep's 'a tier on every brief' has no briefs at draft time: read as 'no unmapped §2 capability' (fm decide).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Tests first: GenesisExam (oracle/empty/mutation/holdout/no-leak/assumed) and the exam genesis arm
2. [x] fmgenesis: assumed CONTEXT line, _kinds helper, exam() + fm genesis exam
3. [x] fmexam: genesis session arm and --request
4. [x] Docs, skill, site check; run the held-out third for real (genesis vs plain, with cost); gates; review
## Resume here
<!-- auto -->
- 2026-10-30T07:10:29Z step 4/4: Docs, skill, site check; run the held-out third for real (genesis vs plain, with cost); gates; review
- git: foreman/build; 10 uncommitted: CHANGELOG.md, MASTER.md, README.md, plugin/lib/fmcli.py, plugin/lib/fmexam.py, plugin/lib/fmgenesis.py, plugin/skills/genesis/SKILL.md, plugin/tests/test_exam.py, plugin/tests/test_genesis.py, site/genesis/genesis.js
- touched since last checkpoint: /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/t2112d.py, plugin/lib/fmexam.py, plugin/lib/fmgenesis.py, plugin/tests/test_exam.py, plugin/tests/test_genesis.py, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/t2112e.py, CHANGELOG.md, MASTER.md, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/t2112f.py, site/genesis/genesis.js, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/t2113a.py
- failures met: ls: cannot access 't0b.py': no such file or directory
## Docs impact
MASTER.md: fm genesis usage gains exam/--arm/--split/--seed and a T-2112 sentence on fmgenesis.exam; fm exam usage gains genesis/--request and a fmexam sentence. CHANGELOG Unreleased bullet. README genesis bullet. plugin/skills/genesis/SKILL.md Start step 4. Site: genesis.js exam table shows draft-* rows as 'N/S drafts'.
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_genesis.GenesisExam test_exam.ExamAuthors` → ✗ exit 1 · Ran 11 tests in 2.2s (2 classes, 16 at a time; slowest: ExamAuthors 2s, GenesisExam 1s) / FAILED (2 classes) [ran] [tree 6e11ed4a00af] (2026-10-30T06:51:55Z)
- (step 2) `python3 plugin/tests/run.py test_genesis.GenesisExam test_genesis.GenesisDraft` → exit 0 · Ran 13 tests in 1.7s (2 classes, 16 at a time; slowest: GenesisDraft 2s, GenesisExam 1s) / OK [ran] [tree 800baf087ba2] (2026-10-30T06:56:24Z)
- (step 3) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 18 tests in 18.1s (9 classes, 16 at a time; slowest: ExamGen 18s, ExamRust 12s, ExamC 11s) / OK [ran] [tree 800baf087ba2] (2026-10-30T06:56:43Z)
- (audit intent) `fm-reviewer pass over the diff; the real held-out run (genesis 9/9, plain 0/9)` → fixed: arms were graded on gen-0 lines no writer sees; now closed (strict) plus given (what each arm was handed), both reported [tree 08cbf19d8bbc] (2026-10-30T07:08:17Z)
- (audit edge) `reviewer: fallback draft, empty request, unknown arm, --request on a key agent` → fixed: a fallback or errored draft counts in errors and closes nothing; none check needs 'no goal ... assum'; unknown arm and --request on oracle raise; tests for each [tree 08cbf19d8bbc] (2026-10-30T07:08:17Z)
- (audit operator) `reviewer: a 9-scenario run is silent for minutes; cost line` → fixed: one stderr progress line per scenario; cost shown as ~$ (matched by feature/project/time, may include a parallel session); serial child calls kept (ponytail) [tree 08cbf19d8bbc] (2026-10-30T07:08:17Z)
- (audit maintainer) `reviewer: ARMS unused, genesis default request split across two places` → fixed: ARMS validated; the default request set once in run_agent and recorded in the row [tree 08cbf19d8bbc] (2026-10-30T07:08:18Z)
- (audit adversary) `untrusted README goes to the child inside <project> marked as data; model text is only parsed, never run; no credentials, no outbound host` → clean: no new trust boundary; the plain child's reply is scored by regex only [tree 08cbf19d8bbc] (2026-10-30T07:08:18Z)
- (step 4) `python3 plugin/tests/run.py test_cli test_docs test_exam test_genesis test_statusline_ui` → exit 0 · Ran 299 tests in 23.8s (77 classes, 16 at a time; slowest: TaskLifecycle 24s, ExamGen 17s, ExamRust 12s) / OK [ran] [tree edbdab5e05e7] (2026-10-30T07:12:20Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis.GenesisExam` → exit 0 · Ran 6 tests in 2.1s (1 classes, 16 at a time; slowest: GenesisExam 2s) / OK [ran] [tree edbdab5e05e7] (2026-10-30T07:16:57Z)
- (ac 2) `python3 plugin/tests/run.py test_genesis.GenesisExam` → exit 0 · Ran 6 tests in 2.1s (1 classes, 16 at a time; slowest: GenesisExam 2s) / OK [ran] [tree edbdab5e05e7] (2026-10-30T07:16:57Z)
- (ac 3) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 18 tests in 17.9s (9 classes, 16 at a time; slowest: ExamGen 18s, ExamRust 11s, ExamC 11s) / OK [ran] [tree edbdab5e05e7] (2026-10-30T07:16:57Z)
- (step 1) `python3 plugin/tests/run.py test_genesis.GenesisExam test_exam.ExamAuthors` → exit 0 · Ran 12 tests in 2.5s (2 classes, 16 at a time; slowest: ExamAuthors 2s, GenesisExam 2s) / OK [ran] [tree edbdab5e05e7] (2026-10-30T07:16:57Z)
- (audit intent) `fm-reviewer five-lens pass on the exam diff; findings fixed test-first (fallback/error drafts no longer count as closed, unknown arm raises, --request only for session agents, none check wants a no-goal CONTEXT line); real held-out run genesis 9/9 strict vs plain 0/9 strict, 9/9 given` → #13 now has a held-out exam scored strictly and on what each arm was handed; the real run shows the genesis arm's edge is gen-0 access at a third of the cost [tree edbdab5e05e7] (2026-10-30T07:16:57Z)
- (audit adversary) `fm-reviewer five-lens pass on the exam diff; findings fixed test-first (fallback/error drafts no longer count as closed, unknown arm raises, --request only for session agents, none check wants a no-goal CONTEXT line); real held-out run genesis 9/9 strict vs plain 0/9 strict, 9/9 given` → model drafts are untrusted text graded by regex; a fallback or errored draft can't count as closed; stub-only tests never reach claude [tree edbdab5e05e7] (2026-10-30T07:16:57Z)
- (audit edge) `fm-reviewer five-lens pass on the exam diff; findings fixed test-first (fallback/error drafts no longer count as closed, unknown arm raises, --request only for session agents, none check wants a no-goal CONTEXT line); real held-out run genesis 9/9 strict vs plain 0/9 strict, 9/9 given` → empty request, unknown arm, non-session agent with --request, plain-arm error all tested [tree edbdab5e05e7] (2026-10-30T07:16:57Z)
## Log
- 2026-10-30T06:42:29Z created
- 2026-10-30T06:42:40Z focused
- 2026-10-30T06:46:43Z paused: focus moved to T-2053
- 2026-10-30T06:48:16Z focused
- 2026-10-30T07:12:43Z real held-out run (9 scenarios, all held out): genesis closed 9/9 strict, 9/9 given, 0 errors, ~$0.09; plain closed 0/9 strict, 9/9 given, 0 errors, ~$0.24. On what each was handed they tie; the strict gap is gen-0's own lines, which only the genesis arm reads, at about a third of the cost.
- 2026-10-30T07:17:23Z done
- 2026-10-30T07:17:25Z committed 581a3820 (10 files)
- 2026-10-30T07:17:35Z guard authorization added: publish
- 2026-10-30T07:22:11Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2099 [FEATURE M, done, 5 steps] fm genesis draft/spec — gen-0 from a line or nothing; per-project spec with a held-out… — lesson: cover() tag words counted as shared w…
- T-2102 [FEATURE M, done, 5 steps] fm genesis select/seed — exam-gated selection into lineage.md; the feature writes the… — lesson: c.lock is not reentrant: a lock around…
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- decision 2026-10-30: Genesis selection (fm genesis select) scores the exam's train split, never the held-out third; held-out only grades a capability done
- similar finished tasks took 5–5 steps
## Lessons
- Score an arm both strictly and on what it was handed: a strict-only gap can be pure information access, not skill.
## Plan gaps
- failed first: step 1 Tests first: GenesisExam (oracle/empty/mutation/holdout/no-leak/assumed) and the exam genesis arm
## Files touched
- plugin/tests/test_exam.py
- plugin/tests/test_genesis.py
- plugin/lib/fmcli.py
- plugin/lib/fmexam.py
- plugin/lib/fmgenesis.py
- site/genesis/genesis.js
- CHANGELOG.md
- MASTER.md
- README.md
- plugin/skills/genesis/SKILL.md
- INSTALL.md
- plugin/tests/test_docs.py
