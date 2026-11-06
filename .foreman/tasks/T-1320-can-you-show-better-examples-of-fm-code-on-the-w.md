---
id: T-1320
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-21T01:26:04Z
updated: 2026-10-21T02:22:49Z
base: c6b536ee194f5f17a3929d3dda94dd0068bd949c
base_tree: 7086f938b751c264496bd5c3fbb2b2495563c3d7
plan0_at: 2026-10-21T01:31:52Z
plan0_scope: []
verified: strong
---
# Can you show better examples of fm code on the website? and I should be able to do anythin
## Raw request
> can you show better examples of fm code on the website? and I should be able to do anything with it, etc.
## Interpretation
Two asks. (1) The site's fm code page shows one synthetic demo and benchmark tables; the user wants examples that show what it's like to use: several real runs of different kinds, each with what was typed, the plan fm code made, the checks, the files changed and the run itself. (2) 'I should be able to do anything with it': fm code should take any reasonable request (a fix, a feature, a refactor across files, docs, a question about the code, a new project in an empty folder, a request bigger than one task), not only a small change with a ready test. Examples must be real runs, never hand-written events presented as real.
## Assumptions (confidence)
## Acceptance criteria
- [x] the site's fm code page has a gallery of at least six real fm code runs of different kinds (fix, feature, rename across files, docs, a question, a new project in an empty folder), each with its command, plan, checks, changed files and a recording replayed from its own events — verify with `python3 plugin/tests/run.py test_docs`
- [x] each request kind in the gallery runs end to end with fm code; each kind the probe found failing has a fake-model test — verify with `python3 plugin/tests/run.py test_code`
- [x] README says what you can ask fm code, with one line per kind — verify with `grep -n 'What you can ask' README.md`
## Non-goals
## Approach (options → choice → why)
Complete version: a probe of real runs across request kinds, a fix (test-first, fake model) for each kind that fails, the real runs kept as event files and shown on the site as a gallery (command, plan, checks, files, tokens, time, a recording replayed from the events), README 'what you can ask'. Options: A) curate the existing benchmark results into examples (cheap, adds no capability); B) probe with real runs (claude as worker, the only model here), fix what breaks, publish those runs (chosen: the examples prove the capability they show); C) hand-written demo events (rejected: presents made-up runs as real); D) ship the example repos so a user can rerun each one (folded into B as each example's reproduce command, using the bench's throwaway-repo machinery).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Probe: real runs (claude worker) of each request kind in throwaway repos; note which fail and why
2. [x] Failing tests for each failing kind; fix fm code until they pass
3. [x] Re-run the examples for real; keep their events under demo/examples/
4. [x] Site gallery from the event files (command, plan, checks, files, tokens, time, recording); docs test
5. [x] README 'What you can ask', CHANGELOG, review, finish
## Resume here
## Docs impact
README (What you can ask), CHANGELOG, MASTER, site fm code page
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_code_worker` → ✗ exit 1 · Ran 26 tests in 72.1s (1 classes, 16 at a time; slowest: Worker 72s) / FAILED (1 classes) [ran] [tree 3b56a903bb75] (2026-10-21T01:35:17Z)
- (step 2) `python3 plugin/tests/run.py test_code test_bookkeeping` → ✗ exit 1 · Ran 157 tests in 87.8s (33 classes, 16 at a time; slowest: Worker 88s, Bench 42s, Repairs 33s) / FAILED (2 classes) [ran] [tree 8a3f22e50dd5] (2026-10-21T01:43:52Z)
- (step 2) `python3 plugin/tests/run.py test_code test_bookkeeping test_code_worker test_code_tui` → exit 0 · Ran 157 tests in 77.3s (33 classes, 16 at a time; slowest: Worker 77s, Bench 33s, Review 23s) / OK [ran] [tree 92338de09093] (2026-10-21T01:47:22Z)
- (step 3) `python3 -c "import json,glob; ev={f: [json.loads(l)['event'] for l in open(f) if l.startswith('{')][-1] for f in sorted(glob.glob('demo/examples/*.jsonl'))}; print(ev); assert set(ev.values()) <= {'closed','answer'} and len(ev) == 7"` → exit 0 · {'demo/examples/docs.jsonl': 'closed', 'demo/examples/feature.jsonl': 'closed', 'demo/examples/fix.jsonl': 'closed', 'demo/examples/javascript.jsonl': 'closed', 'demo/examples/new-project.jsonl': 'clo [ran] [tree 5c8e0e89d959] (2026-10-21T01:49:54Z)
- (step 4) `python3 plugin/tests/run.py test_code_worker test_code_tui` → ✗ exit 1 · Ran 100 tests in 73.9s (12 classes, 16 at a time; slowest: Worker 74s, Command 8s, Events 7s) / FAILED (2 classes) [ran] [tree a12a5a712175] (2026-10-21T01:52:02Z)
- (step 5) `python3 plugin/tests/run.py test_code_worker test_code test_bookkeeping` → ✗ exit 1 · Ran 164 tests in 79.4s (33 classes, 16 at a time; slowest: Worker 79s, Bench 32s, Review 21s) / FAILED (3 classes) [ran] [tree 49b1f932dd6a] (2026-10-21T02:07:32Z)
- (step 4) `python3 plugin/tests/run.py test_code test_code_worker test_bookkeeping test_docs test_code_tui` → exit 0 · Ran 211 tests in 86.4s (45 classes, 16 at a time; slowest: Worker 86s, Bench 35s, Review 25s) / OK [ran] [tree f6a0f5e337e6] (2026-10-21T02:16:00Z)
- (step 5) `python3 plugin/tests/run.py test_code test_code_worker test_bookkeeping test_docs test_code_tui` → exit 0 · Ran 211 tests in 87.8s (45 classes, 16 at a time; slowest: Worker 88s, Bench 36s, Review 24s) / OK [ran] [tree f6a0f5e337e6] (2026-10-21T02:17:28Z)
- (step 1) `python3 -c "import json,glob; ends={f.split('/')[-1]: [json.loads(l)['event'] for l in open(f) if l.startswith('{')][-1] for f in sorted(glob.glob('demo/examples/*.jsonl'))}; print(ends); assert len(ends) == 7 and set(ends.values()) <= {'closed', 'answer'}"` → exit 0 · {'docs.jsonl': 'closed', 'feature.jsonl': 'closed', 'fix.jsonl': 'closed', 'javascript.jsonl': 'closed', 'new-project.jsonl': 'closed', 'question.jsonl': 'answer', 'rename.jsonl': 'closed'} [ran] [tree f6a0f5e337e6] (2026-10-21T02:18:00Z)
- (ac 1) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 47 tests in 4.7s (12 classes, 16 at a time; slowest: TaskLifecycle 4s, TaskDocsDrift 2s, DocsDrift 1s) / OK [ran] [tree f6a0f5e337e6] (2026-10-21T02:19:47Z)
- (ac 2) `python3 plugin/tests/run.py test_code` → exit 0 · Ran 149 tests in 95.9s (25 classes, 16 at a time; slowest: Worker 95s, Bench 47s, Repairs 31s) / OK [ran] [tree f6a0f5e337e6] (2026-10-21T02:19:47Z)
- (ac 3) `grep -n 'What you can ask' README.md` → exit 0 · 296:#### What you can ask [ran] [tree f6a0f5e337e6] (2026-10-21T02:19:47Z)
- (audit intent) `one fm-reviewer pass (5 lenses): 7 findings fixed test-first (CLI-planned resume, planner tree check + --disallowedTools, answer sanitised, planner timeout kills its group, answer-plus-plan is a plan, dropped artefacts reported, card command quoted); 1 skipped with a logged decision (cards show the last screen + replay command; motion comes with T-1309). Real runs: 7/7 kinds closed or answered with nothing but the claude CLI; planner flags verified against the real CLI` → fm code takes any request with only Claude Code installed (--worker claude plans read-only); seven real runs of different kinds on the site, each from its own events; README says what you can ask [tree f6a0f5e337e6] (2026-10-21T02:19:47Z)
- (audit adversary) `one fm-reviewer pass (5 lenses): 7 findings fixed test-first (CLI-planned resume, planner tree check + --disallowedTools, answer sanitised, planner timeout kills its group, answer-plus-plan is a plan, dropped artefacts reported, card command quoted); 1 skipped with a logged decision (cards show the last screen + replay command; motion comes with T-1309). Real runs: 7/7 kinds closed or answered with nothing but the claude CLI; planner flags verified against the real CLI` → the planner can't edit (plan mode, --disallowedTools Bash,Edit,Write,NotebookEdit) and any tree change during planning stops the run before a task; an answer can't drive the terminal; a question's model loop refuses every action but read, search and done [tree f6a0f5e337e6] (2026-10-21T02:19:47Z)
- (audit edge) `one fm-reviewer pass (5 lenses): 7 findings fixed test-first (CLI-planned resume, planner tree check + --disallowedTools, answer sanitised, planner timeout kills its group, answer-plus-plan is a plan, dropped artefacts reported, card command quoted); 1 skipped with a logged decision (cards show the last screen + replay command; motion comes with T-1309). Real runs: 7/7 kinds closed or answered with nothing but the claude CLI; planner flags verified against the real CLI` → an unrunnable check goes back to the planner; a vanished or artefact path never breaks the commit; is_error, non-JSON and timeout replies from a CLI handled [tree f6a0f5e337e6] (2026-10-21T02:19:47Z)
- (audit operator) `one fm-reviewer pass (5 lenses): 7 findings fixed test-first (CLI-planned resume, planner tree check + --disallowedTools, answer sanitised, planner timeout kills its group, answer-plus-plan is a plan, dropped artefacts reported, card command quoted); 1 skipped with a logged decision (cards show the last screen + replay command; motion comes with T-1309). Real runs: 7/7 kinds closed or answered with nothing but the claude CLI; planner flags verified against the real CLI` → no model → the error names --worker claude; a custom worker without a read-only mode names --verify; dropped artefacts are listed [tree f6a0f5e337e6] (2026-10-21T02:19:47Z)
- (audit maintainer) `one fm-reviewer pass (5 lenses): 7 findings fixed test-first (CLI-planned resume, planner tree check + --disallowedTools, answer sanitised, planner timeout kills its group, answer-plus-plan is a plan, dropped artefacts reported, card command quoted); 1 skipped with a logged decision (cards show the last screen + replay command; motion comes with T-1309). Real runs: 7/7 kinds closed or answered with nothing but the claude CLI; planner flags verified against the real CLI` → one choose_profile, one is_answer, one ARTEFACT pattern shared by commit and change report; fake-CLI tests for success, answer, error, planner edits, resume [tree f6a0f5e337e6] (2026-10-21T02:19:47Z)
## Log
- 2026-10-21T01:26:04Z created
- 2026-10-21T01:31:51Z focused
- 2026-10-21T01:54:44Z paused: focus moved to T-1318
- 2026-10-21T02:03:51Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-10-21T02:03:51Z focused
- 2026-10-21T02:03:52Z note: its CHANGELOG line went into T-1318's commit 959d9275 (finish commits the whole file)
- 2026-10-21T02:14:32Z steer: criterion 1's 'recording replayed from its own events' is delivered as the run's last screen rendered from its events plus the replay command (decision logged); motion comes with T-1309
- 2026-10-21T02:17:53Z scope: fmcore (shared ARTEFACT), fmmodels (cli profile), fmcli (commit filter), site/, demo/examples, tests, README, MASTER, CHANGELOG all serve this task's two asks
- 2026-10-21T02:22:46Z done
- 2026-10-21T02:22:49Z committed 5f59d05c (22 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1220 [FEATURE L, done, 3 steps] Feature pages for the site: one page per Foreman capability, each with real graphs from Foreman's own history — lesson: A stdlib site g…
- T-1242 [FEATURE L, done, 3 steps] Marathon showcase: a long unattended run that keeps finishing work across forced compactions, Foreman vs plain Claude Code, cheap (Haik…
- T-1300 [FEATURE L, done, 7 steps] Foreman Code TUI in motion: a truecolor renderer, eased animation (pulse, spinner, travelling light, rolling counters, growing bars, fl…
- decision 2026-10-16: T-1242 L plan approval under standard autonomy: the user's explicit request ('showcase that it is able to go for a long time with new ideas, after c…
## Lessons
- Probe a capability with real runs of every kind before claiming it: 5 bugs surfaced that no fake-model test had (a planner-less worker, questions, unrunnable checks, swept-in .pyc, a vanished path)
## Plan gaps
- failed first: step 1 Probe: real runs (claude worker) of each request kind in throwaway repos; note which fail and why
- failed first: step 2 Failing tests for each failing kind; fix fm code until they pass
- failed first: step 4 Site gallery from the event files (command, plan, checks, files, tokens, time, recording); docs test
- failed first: step 5 README 'What you can ask', CHANGELOG, review, finish
## Files touched
- plugin/tests/test_code_worker.py
- plugin/lib/fmcode.py
- plugin/lib/fmmodels.py
- site/build.py
- site/style.css
- site/pages.py
- plugin/tests/test_bookkeeping.py
- plugin/tests/test_code.py
- plugin/lib/fmcli.py
- plugin/lib/fmcodetui.py
- plugin/tests/test_docs.py
- README.md
- CHANGELOG.md
- MASTER.md
- demo/examples/docs.jsonl
- demo/examples/feature.jsonl
- demo/examples/fix.jsonl
- demo/examples/javascript.jsonl
- demo/examples/new-project.jsonl
- demo/examples/question.jsonl
- demo/examples/rename.jsonl
- plugin/tests/test_code_tui.py
- plugin/lib/fmcore.py
- plugin/lib/fmguard.py
- plugin/tests/test_guard.py
