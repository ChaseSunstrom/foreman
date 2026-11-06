---
id: T-1618
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmplaybooks.py, plugin/lib/fmcli.py, plugin/evals/playbooks, plugin/tests/test_playbook_evals.py, CHANGELOG.md, MASTER.md, plugin/skills/playbooks/SKILL.md]
depends_on: []
source: user
created: 2026-10-22T20:56:54Z
updated: 2026-10-22T23:32:59Z
base: 393b00413a5e52337645bbc0c2182c3b9cf42ffd
base_tree: 54d7f710c1b69631ed76bb2a7f45e53ef5b104ef
plan0_at: 2026-10-22T23:20:31Z
plan0_scope: [plugin/lib/fmplaybooks.py, plugin/lib/fmcli.py, plugin/evals/playbooks, plugin/tests/test_playbook_evals.py, CHANGELOG.md]
verified: strong
---
# fm playbooks eval: held-out brief sets and a with/without lift on the scripted fake model
## Raw request
> fm playbooks eval: held-out brief sets and a with/without lift on the scripted fake model
## Interpretation
fm playbooks eval NAME scores a playbook against held-out briefs: each brief in plugin/evals/playbooks/NAME.json has a task text and checks the answer must meet; the eval runs each brief with and without the playbook loaded and records the lift (pass rate with minus without) under FOREMAN_HOME. A scripted fake model makes it deterministic in tests; --real uses claude -p under fm budget. An fm verb, so it works from Claude Code.
## Assumptions (confidence)
## Acceptance criteria
- [x] eval NAME prints and records lift (with minus without) for a fixture playbook's held-out briefs; a real model only with --real, budgeted — verify with `python3 plugin/tests/run.py test_playbook_evals.Lift`
## Non-goals
## Approach (options → choice → why)
Options: hand-graded reviews (slow, subjective); an LLM judge only (noisy, costly); checks written per brief (substring, regex, a command) with a fake model for tests and the real one opt-in. Choice: per-brief checks plus the fake model: reproducible in the suite, cheap, and the real run is explicit and budgeted.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: two briefs, a fake model that obeys a line only when loaded, lift 1.0
2. [x] brief-set format under plugin/evals/playbooks/<name>.json
3. [x] runner and recorded result under FOREMAN_HOME
## Resume here
## Docs impact
plugin/skills/playbooks/SKILL.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_playbook_evals.Lift` → red as expected (exit 1) · Ran 6 tests in 0.5s (1 classes, 16 at a time; slowest: Lift 0s) / FAILED (1 classes) [ran] [tree 0c56c43096b4] (2026-10-22T23:27:15Z)
- (step 2) `python3 plugin/tests/run.py test_playbook_evals test_playbook_check test_docs` → exit 0 · Ran 99 tests in 11.5s (24 classes, 16 at a time; slowest: Fences 11s, TaskLifecycle 3s, Repo 3s) / OK [ran] [tree 22e76c988215] (2026-10-22T23:27:58Z)
- (step 3) `python3 plugin/tests/run.py test_playbook_evals test_playbook_check test_docs` → exit 0 · Ran 99 tests in 14.1s (24 classes, 16 at a time; slowest: Fences 14s, TaskLifecycle 4s, Repo 4s) / OK [ran] [tree 22e76c988215] (2026-10-22T23:28:13Z)
- (ac 1) `python3 plugin/tests/run.py test_playbook_evals.Lift` → exit 0 · Ran 6 tests in 1.2s (1 classes, 16 at a time; slowest: Lift 1s) / OK [ran] [tree 22e76c988215] (2026-10-22T23:28:16Z)
- (step 3) `python3 plugin/tests/run.py test_playbook_evals` → red as expected (exit 1) · Ran 9 tests in 1.0s (1 classes, 16 at a time; slowest: Lift 1s) / FAILED (1 classes) [ran] [tree 6b4917338bdc] (2026-10-22T23:30:20Z)
- (step 3) `python3 plugin/tests/run.py test_playbook_evals test_playbook_check test_docs test_doctor` → exit 0 · Ran 163 tests in 8.7s (45 classes, 16 at a time; slowest: Fences 9s, Snippets 3s, Command 2s) / OK [ran] [tree 97977ea2d54d] (2026-10-22T23:31:43Z)
- (ac 1) `python3 plugin/tests/run.py test_playbook_evals.Lift` → exit 0 · Ran 9 tests in 0.6s (1 classes, 16 at a time; slowest: Lift 0s) / OK [ran] [tree 97977ea2d54d] (2026-10-22T23:31:44Z)
- (ac 1) `python3 plugin/tests/run.py test_playbook_evals.Lift` → exit 0 · Ran 9 tests in 0.6s (1 classes, 16 at a time; slowest: Lift 0s) / OK [ran] [tree 97977ea2d54d] (2026-10-22T23:31:45Z)
- (audit intent) `fm-reviewer full pass (intent, adversary, edge, operator, maintainer); MEDIUMs fixed: the literal model is now named a text-presence check (not an upper bound) and the shipped-set test holds each brief; brief regexes over 200 chars or with a nested quantifier refused; LOWs fixed test-first: deep JSON, empty checks, failing child names its brief, library name wins over a same-path file, absolute brief path, docs` → fm playbooks eval prints and records the lift for a playbook's held-out briefs; the default literal model is a deterministic text-presence check, --real measures a model [tree 97977ea2d54d] (2026-10-22T23:31:45Z)
- (audit adversary) `fm-reviewer full pass (intent, adversary, edge, operator, maintainer); MEDIUMs fixed: the literal model is now named a text-presence check (not an upper bound) and the shipped-set test holds each brief; brief regexes over 200 chars or with a nested quantifier refused; LOWs fixed test-first: deep JSON, empty checks, failing child names its brief, library name wins over a same-path file, absolute brief path, docs` → a cloned repo's brief file can't hang the run (long/nested-quantifier regexes refused before any search); --real children are tool-less and each checked and recorded against fm budget after an up-front estimate; a non-library .md path is announced on stderr [tree 97977ea2d54d] (2026-10-22T23:31:45Z)
- (audit edge) `fm-reviewer full pass (intent, adversary, edge, operator, maintainer); MEDIUMs fixed: the literal model is now named a text-presence check (not an upper bound) and the shipped-set test holds each brief; brief regexes over 200 chars or with a nested quantifier refused; LOWs fixed test-first: deep JSON, empty checks, failing child names its brief, library name wins over a same-path file, absolute brief path, docs` → bad JSON, deep nesting, empty or unknown checks and bad regexes refused with the reason; a failed --real child names its brief [tree 97977ea2d54d] (2026-10-22T23:31:45Z)
- (audit operator) `fm-reviewer full pass (intent, adversary, edge, operator, maintainer); MEDIUMs fixed: the literal model is now named a text-presence check (not an upper bound) and the shipped-set test holds each brief; brief regexes over 200 chars or with a nested quantifier refused; LOWs fixed test-first: deep JSON, empty checks, failing child names its brief, library name wins over a same-path file, absolute brief path, docs` → rows land in playbook-evals.jsonl with absolute paths; MASTER.md and the playbooks skill name the verb [tree 97977ea2d54d] (2026-10-22T23:31:45Z)
- (audit intent) `fm-reviewer full pass (intent, adversary, edge, operator, maintainer); MEDIUMs fixed: the literal model is now named a text-presence check (not an upper bound) and the shipped-set test holds each brief; brief regexes over 200 chars or with a nested quantifier refused; LOWs fixed test-first: deep JSON, empty checks, failing child names its brief, library name wins over a same-path file, absolute brief path, docs` → fm playbooks eval prints and records the lift for a playbook's held-out briefs; the default literal model is a deterministic text-presence check, --real measures a model [tree 97977ea2d54d] (2026-10-22T23:32:25Z)
- (audit adversary) `fm-reviewer full pass (intent, adversary, edge, operator, maintainer); MEDIUMs fixed: the literal model is now named a text-presence check (not an upper bound) and the shipped-set test holds each brief; brief regexes over 200 chars or with a nested quantifier refused; LOWs fixed test-first: deep JSON, empty checks, failing child names its brief, library name wins over a same-path file, absolute brief path, docs` → a cloned repo's brief file can't hang the run (long/nested-quantifier regexes refused before any search); --real children are tool-less and each checked and recorded against fm budget after an up-front estimate; a non-library .md path is announced on stderr [tree 97977ea2d54d] (2026-10-22T23:32:25Z)
- (audit edge) `fm-reviewer full pass (intent, adversary, edge, operator, maintainer); MEDIUMs fixed: the literal model is now named a text-presence check (not an upper bound) and the shipped-set test holds each brief; brief regexes over 200 chars or with a nested quantifier refused; LOWs fixed test-first: deep JSON, empty checks, failing child names its brief, library name wins over a same-path file, absolute brief path, docs` → bad JSON, deep nesting, empty or unknown checks and bad regexes refused with the reason; a failed --real child names its brief [tree 97977ea2d54d] (2026-10-22T23:32:25Z)
- (audit operator) `fm-reviewer full pass (intent, adversary, edge, operator, maintainer); MEDIUMs fixed: the literal model is now named a text-presence check (not an upper bound) and the shipped-set test holds each brief; brief regexes over 200 chars or with a nested quantifier refused; LOWs fixed test-first: deep JSON, empty checks, failing child names its brief, library name wins over a same-path file, absolute brief path, docs` → rows land in playbook-evals.jsonl with absolute paths; MASTER.md and the playbooks skill name the verb [tree 97977ea2d54d] (2026-10-22T23:32:25Z)
## Log
- 2026-10-22T20:56:54Z created
- 2026-10-22T20:56:55Z set scope=['plugin/lib/fmplaybooks.py', 'plugin/lib/fmcli.py', 'plugin/evals/playbooks', 'plugin/tests/test_playbook_evals.py', 'CHANGELOG.md']
- 2026-10-22T20:56:56Z split from T-1522 (L) by recon; works from Claude Code too (an fm verb, /foreman: command, skill or the foreman-ui mod)
- 2026-10-22T21:29:48Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_playbook_evals.Lift`
- 2026-10-22T21:30:12Z criterion 1 text: eval NAME prints and records lift (with minus without) for a fixture playbook's held-out briefs; a real model only with --real, budgeted — verify with python3 plugin/tests/run.py test_playbook_evals.Lift → eval NAME prints and records lift (with minus without) for a fixture playbook's held-out briefs; a real model only with --real, budgeted
- 2026-10-22T23:20:30Z focused
- 2026-10-22T23:28:16Z scope: plugin/lib/fmcli.py (eval flags), plugin/evals/playbooks (the first brief set), plugin/skills/playbooks/SKILL.md (names the verb for the CC plugin)
- 2026-10-22T23:31:13Z set scope=['plugin/lib/fmplaybooks.py', 'plugin/lib/fmcli.py', 'plugin/evals/playbooks', 'plugin/tests/test_playbook_evals.py', 'CHANGELOG.md', 'MASTER.md', 'plugin/skills/playbooks/SKILL.md']
- 2026-10-22T23:32:24Z scope: plugin/tests/fixtures/skill_triggers.json and test_docs.py came from merging T-1704's lane while T-1618 was focused; T-1704 closes them
- 2026-10-22T23:32:57Z done
- 2026-10-22T23:32:59Z committed 82d79883 (7 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1522 [FEATURE L, dropped, 4 steps] Round 3 (T-1520): Playbook evals: A/B each playbook against none on held-out briefs, ablat
- T-1621 [FEATURE M, done, 3 steps] Playbook load resolves {{fact}} from fm map and appends a project's .foreman/playbooks overlays — lesson: Repo-supplied text spliced in…
- T-1032 [FEATURE L, done, 6 steps] Learn a fix once, apply it every time: when a session hits an obstacle and resolves it (e. — lesson: Never name a unittest helper fail(…
- decision 2026-10-16: T-0275: a script over the guard's parse budget stays allowed after the literal scan, not refused
- similar finished tasks took 3–6 steps
- likely tests for the scope: plugin/tests/test_cli.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmplaybooks.py; re-ground the plan against them before editing
## Lessons
- An eval whose checks copy the playbook's wording measures presence, not behaviour; say so in its output and measure behaviour with a real model
## Files touched
- plugin/tests/test_playbook_evals.py
- plugin/lib/fmplaybooks.py
- plugin/evals/playbooks/verify/tdd-workflow.json
- plugin/lib/fmcli.py
- plugin/skills/playbooks/SKILL.md
- CHANGELOG.md
- MASTER.md
- plugin/tests/fixtures/skill_triggers.json
- plugin/tests/test_docs.py
