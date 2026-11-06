---
id: T-1505
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmplaybooks.py, plugin/lib/fmcli.py, plugin/tests/test_playbook_check.py, plugin/skills/playbooks, CHANGELOG.md, MASTER.md, plugin/tests/test_docs.py]
depends_on: []
source: followup
created: 2026-10-22T17:36:16Z
updated: 2026-10-22T19:55:17Z
base: 3943593ee874a1944048b111569760cda290c8cb
base_tree: ed72982cdd0bc0b962648fef18100cfc4a8be7c9
plan0_at: 2026-10-22T18:43:03Z
plan0_scope: [plugin/lib/fmplaybooks.py, plugin/lib/fmcli.py, plugin/tests/test_playbook_check.py, plugin/skills/playbooks, CHANGELOG.md]
verified: strong
---
# fm check playbooks: index, duplicates, token budget and reach
## Raw request
> fm check playbooks: index, duplicates, token budget and reach
## Interpretation
Brainstorm T-1479 cluster 11: 48 playbooks today and about 30 more coming; nothing checks them. fm check playbooks: every references/**/*.md is listed in SKILL.md and every listed path exists; no two playbooks share a title or most of their text; each has a Use-when line; a token ratchet (a playbook may not grow past its recorded size without saying so); and a reach report naming playbooks no task has read in 60 days (from fm cost's playbook use).
## Assumptions (confidence)
## Acceptance criteria
- [x] the lint finds an unlisted file, a dead index line, a near-duplicate and a playbook over its ratchet; the repo's own playbooks pass — verify with `cd plugin/tests && python3 -m unittest test_playbook_check`
- [x] each playbook has a numbered procedure (a line starting '1. '), every 'fm lib show NAME' it names resolves to a card, and every fenced python block not marked no-run runs with python3 -I in a temp folder and exits 0 (the self-checks in ops, ui and fix playbooks) — verify with `python3 plugin/tests/run.py test_playbook_check`
## Non-goals
## Approach (options → choice → why)
Options: fold into fm doctor (slow path for every doctor run); chosen: its own fm check sub-verb, run by the release gates; the duplicate test is word-shingle Jaccard over 0.6. The index scales by stage: when SKILL.md nears its 10,000-char budget (doctor's footprint check), each stage gets a references/<stage>/INDEX.md with the per-file lines and SKILL.md keeps one line per stage; test_docs' index check accepts a path named in the stage index.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests
2. [x] plugin/lib/fmplaybooks.py and fm check playbooks
3. [x] reach report from fm cost data
4. [x] numbered-procedure, card-name and runnable-snippet checks (absorbs T-1580, T-1584)
## Resume here
## Docs impact
MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_playbook_check` → ✗ exit 1 (never ran: no tests ran) · Ran 0 tests in 0.6s (1 classes, 16 at a time; slowest: _FailedTest 0s) / FAILED (1 classes) [ran] [tree 46c5cbb1bf9e] (2026-10-22T18:48:52Z)
- (step 2) `python3 plugin/tests/run.py test_playbook_check test_docs 2>&1 | tail -30` → exit 0 · Ran 71 tests in 7.0s (19 classes, 16 at a time; slowest: TaskLifecycle 6s, Repo 4s, Snippets 3s) / OK [ran] [tree fec64d7e0933] (2026-10-22T18:55:26Z)
- (step 3) `python3 plugin/tests/run.py test_playbook_check test_docs 2>&1 | tail -15` → exit 0 · Ran 72 tests in 5.2s (19 classes, 16 at a time; slowest: TaskLifecycle 5s, Repo 4s, Snippets 3s) / OK [ran] [tree df93f18d18b7] (2026-10-22T18:56:34Z)
- (step 2) `python3 plugin/tests/run.py test_playbook_check test_docs` → exit 0 · Ran 72 tests in 4.3s (19 classes, 16 at a time; slowest: TaskLifecycle 4s, Repo 3s, Snippets 3s) / OK [ran] [tree df93f18d18b7] (2026-10-22T18:56:47Z)
- (step 3) `python3 plugin/tests/run.py -k test_playbook_check.Reach` → exit 0 · Ran 2 tests in 0.5s (1 classes, 16 at a time; slowest: Reach 0s) / OK [ran] [tree df93f18d18b7] (2026-10-22T18:56:52Z)
- (step 4) `python3 plugin/tests/run.py -k test_playbook_check.Shape -k test_playbook_check.Snippets -k test_playbook_check.Repo` → exit 0 · Ran 9 tests in 3.1s (3 classes, 16 at a time; slowest: Repo 3s, Snippets 2s, Shape 0s) / OK [ran] [tree df93f18d18b7] (2026-10-22T18:56:57Z)
- (ac 2) `python3 plugin/tests/run.py test_playbook_check 2>&1 | grep -E "^(FAIL|ERROR):|^Ran|^OK|FAILED" | head -20` → ✗ exit 1 · Ran 30 tests in 2.7s (8 classes, 16 at a time; slowest: Cli 2s, Snippets 2s, Repo 1s) / FAILED (4 classes) [ran] [tree c61983b8db12] (2026-10-22T19:21:10Z)
- (step 1) `python3 plugin/tests/run.py test_playbook_check` → ✗ exit 1 · Ran 30 tests in 2.5s (8 classes, 16 at a time; slowest: Cli 2s, Snippets 2s, Repo 1s) / FAILED (4 classes) [ran] [tree c61983b8db12] (2026-10-22T19:21:17Z)
- (step 4) `python3 plugin/tests/run.py test_playbook_check test_docs` → exit 0 · Ran 79 tests in 2.5s (20 classes, 16 at a time; slowest: Snippets 2s, TaskLifecycle 1s, Repo 1s) / OK [ran] [tree 9608acd619df] (2026-10-22T19:22:51Z)
- (step 4) `python3 plugin/tests/run.py test_playbook_check test_docs` → exit 0 · Ran 79 tests in 2.4s (20 classes, 16 at a time; slowest: Snippets 2s, Repo 1s, TaskLifecycle 1s) / OK [ran] [tree ed749870ff83] (2026-10-22T19:23:45Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_playbook_check` → exit 0 · Ran 30 tests in 4.856s / OK [ran] [tree 939f04bbddf1] (2026-10-22T19:53:44Z)
- (ac 2) `python3 plugin/tests/run.py test_playbook_check` → exit 0 · Ran 30 tests in 2.7s (8 classes, 16 at a time; slowest: Snippets 2s, Repo 2s, Cli 1s) / OK [ran] [tree 939f04bbddf1] (2026-10-22T19:53:47Z)
- (step 1) `fm check playbooks` → exit 0 · ✓ playbooks: 76 checked, 0 problem(s) / unread in 60 days (the event log covers 6.6): 35 of 76: build/cpp-build, build/csharp-build, build/go-build, build/jvm-build, build/rust-build, build/shell-buil [ran] [tree 939f04bbddf1] (2026-10-22T19:53:51Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_playbook_check` → exit 0 · Ran 30 tests in 5.749s / OK [ran] [tree db50e146559e] (2026-10-22T19:54:01Z)
- (ac 2) `python3 plugin/tests/run.py test_playbook_check` → exit 0 · Ran 30 tests in 2.7s (8 classes, 16 at a time; slowest: Snippets 2s, Repo 2s, Cli 1s) / OK [ran] [tree db50e146559e] (2026-10-22T19:54:01Z)
- (audit intent) `one fm-reviewer pass: approve with nits; 3 MEDIUM + 5 LOW fixed in 120b0beb, merged with main twice (76 playbooks, 0 problems)` → unlisted files, dead index lines, near-duplicates, size growth, Use-when lines, numbered procedures, card names and runnable python blocks are checked; the repo passes [tree db50e146559e] (2026-10-22T19:54:01Z)
- (audit adversary) `one fm-reviewer pass: approve with nits; 3 MEDIUM + 5 LOW fixed in 120b0beb, merged with main twice (76 playbooks, 0 problems)` → python blocks run with HOME and PATH only, stdin closed, a timeout, memory and process limits and a process-group kill; documented as hygiene, not a sandbox [tree db50e146559e] (2026-10-22T19:54:01Z)
- (audit edge) `one fm-reviewer pass: approve with nits; 3 MEDIUM + 5 LOW fixed in 120b0beb, merged with main twice (76 playbooks, 0 problems)` → the ratchet allows 10% plus 50 tokens and records shrinkage; ratchet typo writes nothing; lanes run the worktree's own fm [tree db50e146559e] (2026-10-22T19:54:01Z)
- (audit maintainer) `one fm-reviewer pass: approve with nits; 3 MEDIUM + 5 LOW fixed in 120b0beb, merged with main twice (76 playbooks, 0 problems)` → test_playbook_check red first; the duplicate test_docs index test removed [tree db50e146559e] (2026-10-22T19:54:01Z)
## Log
- 2026-10-22T17:36:16Z created
- 2026-10-22T17:58:59Z set scope=['plugin/lib/fmplaybooks.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_playbook_check.py', 'plugin/skills/playbooks', 'CHANGELOG.md']
- 2026-10-22T18:12:30Z steer: fm check playbooks also runs each playbook's embedded python blocks marked runnable (game-feel's juice.py, type-and-colour's contrast proof) so an edit can't silently break them
- 2026-10-22T18:42:43Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1505.builder.md
- 2026-10-22T18:43:02Z focused
- 2026-10-22T18:54:35Z set scope=['plugin/lib/fmplaybooks.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_playbook_check.py', 'plugin/skills/playbooks', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-22T18:54:36Z scope: MASTER.md's plugin/skills row documents fm check playbooks (docs impact)
- 2026-10-22T19:20:34Z set scope=['plugin/lib/fmplaybooks.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_playbook_check.py', 'plugin/skills/playbooks', 'CHANGELOG.md', 'MASTER.md', 'plugin/tests/test_docs.py']
- 2026-10-22T19:20:34Z steer: review nits — limits, ratchet slack, merge foreman/build, test_docs index rule folded into fmplaybooks, CLI tests, output cap, lane note
- 2026-10-22T19:25:18Z merged worktree-agent-a21d484c289ccfc47 (25 file(s))
- 2026-10-22T19:25:18Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a21d484c289ccfc47
- 2026-10-22T19:53:28Z focused
- 2026-10-22T19:53:51Z scope: 18 playbooks edited for the new lint (Use-when lines, numbered lists, no-run marks), MASTER.md, test_docs.py (duplicate index test removed), ratchet.json; other files from other tasks' merges
- 2026-10-22T19:55:14Z done
- 2026-10-22T19:55:17Z committed dea1e054 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0783 [PERFORMANCE M, done, 3 steps] Big Bash outputs reach the model as head, tail and failure lines, with the full text in a file (opt-in) — lesson: measure a lossy c…
- research wave1-plan-a2475fc5d2263de06: === T-1049 [stale: plugin/lib/fmcli.py, plugin/lib/fmdeps.py, plugin/lib/fmhooks.py changed since it was written]
- research T-1503-review: Verdict:** approve with nits. I found no destructive command and no outright false SQL, Unicode, time zone or money claim, but a few steps give w…
- decision 2026-10-20: [cites: research/brainstorm-20261020] Round 1 of the 2026-10-20 brainstorm builds T-1254 (cost per fully-correct session on the page), T-1255 (Claud…
- the similar finished task took 3 steps
- likely tests for the scope: plugin/tests/test_cli.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmplaybooks.py, plugin/skills/playbooks/SKILL.md, plugin/skills/playbooks/ratchet.json, plugin/skills/playbooks/references/build/INDEX.md, plu…; re-ground the plan against them before editing
## Why not caught
nothing checked playbooks before
## Lessons
- A lint that writes its own baseline (ratchet.json) needs a root override for tests, or a CLI test rewrites the real file
## Plan gaps
- failed first: step 1 failing tests
## Files touched
- plugin/tests/test_playbook_check.py
- plugin/lib/fmplaybooks.py
- plugin/skills/playbooks/references/clean/code-simplifier.md
- plugin/skills/playbooks/references/clean/repo-sweep.md
- plugin/skills/playbooks/references/ground/code-architect.md
- plugin/skills/playbooks/references/ground/code-explorer.md
- plugin/skills/playbooks/references/ground/search-first.md
- plugin/skills/playbooks/references/reflect/architecture-decision-records.md
- plugin/skills/playbooks/references/review/silent-failures.md
- plugin/skills/playbooks/references/review/type-design.md
- plugin/skills/playbooks/references/review/test-coverage.md
- plugin/skills/playbooks/references/security/cloud-infrastructure.md
- plugin/skills/playbooks/references/context/context-budget.md
- plugin/skills/playbooks/references/lang/python-patterns.md
- plugin/skills/playbooks/references/lang/rust-patterns.md
- plugin/skills/playbooks/references/security/security-review.md
- plugin/skills/playbooks/references/ui/game-feel.md
- plugin/skills/playbooks/references/verify/verification-loop.md
- plugin/skills/playbooks/references/lang/python-testing.md
- plugin/skills/playbooks/references/ui/type-and-colour.md
- MASTER.md
- plugin/lib/fmcli.py
- plugin/skills/playbooks/ratchet.json
- plugin/skills/playbooks/references/ui/sound-design.md
- plugin/tests/test_docs.py
- README.md
- plugin/README.md
- plugin/agents/fm-reviewer.md
- plugin/lib/fmauditrun.py
- plugin/lib/fmcore.py
