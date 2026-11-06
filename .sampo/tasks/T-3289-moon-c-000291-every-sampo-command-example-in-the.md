---
id: T-3289
type: FEATURE
tier: M
status: active
priority: normal
scope: [plugin/tests/test_docexamples.py, README.md, MASTER.md, INSTALL.md, plugin/skills, plugin/commands, plugin/rules/foreman.md, CHANGELOG.md]
depends_on: []
source: user
created: 2026-11-06T02:34:52Z
updated: 2026-11-06T02:53:19Z
builder: 2026-11-06T02:35:13Z
builder_model: haiku
builder_proc: archbox-hardened|pid:[4026531836]|2060851|807411
lane: ~/.claude/foreman/.claude/worktrees/agent-ab43d7562ecb71710
lane_branch: worktree-agent-ab43d7562ecb71710
base: 5c403348c1dfe9523985c9f84cf7db536080f17f
base_tree: 9eb33fa93e768f0136959dc9b365e08cdaa741eb
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T02:36:02Z
plan0_scope: [plugin/tests/test_docexamples.py, README.md, MASTER.md, INSTALL.md, plugin/skills, plugin/commands, plugin/rules/foreman.md, CHANGELOG.md]
builder_returned: 2026-11-06T02:53:19Z
---
# Moon C-000291: every sampo command example in the docs parses against the real CLI (unknown verb/flag fails)
## Raw request
> Moon C-000291: every sampo command example in the docs parses against the real CLI (unknown verb/flag fails)
## Interpretation
Reading 1 (chosen): a new static test that parses every documented sampo command example with the real argparse parser, failing on unknown verb or flag. Reading 2 (ruled out): running each example against a scratch project, because most examples are destructive or need real task ids, and parse-only is what the brief allows. Existing coverage: test_docs.py sampo_mention_problems checks only the verb and first subcommand word in README/INSTALL, and the Smith section of README gets a full parse; flags elsewhere (MASTER, skills, commands, rules) are unchecked. A probe found 798 examples, 198 failing to parse, mostly missing-required-argument noise to be filtered.
## Assumptions (confidence)
## Acceptance criteria
- [ ] a new test module extracts backticked/fenced sampo and fm examples from README, MASTER, INSTALL, skills/*/SKILL.md, commands/*.md and rules/foreman.md, fills placeholders, parses each with cli.build_parser and fails on unknown verb, invalid choice or unrecognized flag, ignoring missing-required-argument errors — verify with `python3 plugin/tests/run.py test_docexamples`
- [ ] the checker itself is pinned: a planted example with a made-up flag and one with a made-up verb are reported, a bare 'sampo task done' and a '[--lens ...]' placeholder form are not — verify with `python3 plugin/tests/run.py test_docexamples`
- [ ] every real doc example passes (stale ones fixed in the docs, or listed with a reason in an explicit allowlist) — verify with `python3 plugin/tests/run.py test_docexamples`
## Non-goals
## Approach (options → choice → why)
1. New test module test_docexamples.py that regex-extracts examples, normalizes placeholders, parses with cli.build_parser, and keeps only unrecognized-argument and invalid-choice errors. Likely outcome: catches renamed flags in every doc, small and isolated, no collision with big files.
2. Extend sampo_mention_problems in test_docs.py to check flags. Likely outcome: works, but edits a shared test file other lanes touch.
3. Run examples against a scratch project. fails if: examples need real ids or are destructive, flaky and slow.
4. Do less: only add MASTER.md to the existing verb check. Likely outcome: misses flag drift, which is the actual silent breakage.

Choice 1 (85%): isolated new module, flag-level coverage, cheap. Captured: none.
## Risks and rollback
Blast radius (sampo graph blast): co-changes plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmcore.py, plugin/lib/fmhooks.py; past FIXes T-1303, T-1468, T-1473, T-1485, T-1521.
## Execution prompt
## Steps
1. [ ] write failing test_docexamples with the planted-example pins, using argparse error text to separate unknown flag/verb from missing-required
2. [x] run it over the real docs, fix each stale example in the doc (or allowlist with reason); renamed verbs go through cli.RENAMES like sampo_mention_problems
3. [ ] CHANGELOG line  <- CURRENT
## Resume here
<!-- auto -->
- 2026-11-06T02:42:39Z step 1/3: write failing test_docexamples with the planted-example pins, using argparse error text to separate unknown flag/verb from missing-required
- git: worktree-agent-ab43d7562ecb71710; 1 uncommitted: plugin/tests/test_docexamples.py
- touched since last checkpoint: plugin/tests/test_docexamples.py
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_docexamples` → ✗ exit 1 · Ran 3 tests in 9.7s (1 jobs, 16 at a time; slowest: DocExamples 0s) / FAILED (1 classes: test_docexamples.DocExamples) [ran] [tree a3ab2262a0b9] [world 2f1906870a] (2026-11-06T02:39:48Z)
- (step 2) `python3 plugin/tests/run.py test_docexamples` → exit 0 · Ran 3 tests in 2.3s (1 jobs, 16 at a time; slowest: DocExamples 1s) / OK [ran] [tree abd33fdfc8cb] [world 2f1906870a] (2026-11-06T02:46:29Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_docexamples test_docs test_doctor test_left_out test_models test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [80.86s] [ran] [tree abd33fdfc8cb] [world 2f1906870a] (2026-11-06T02:48:25Z)
- (step 2) `python3 plugin/tests/run.py test_docexamples` → exit 0 · Ran 3 tests in 5.5s (1 jobs, 16 at a time; slowest: DocExamples 3s) / OK [ran] [tree b0cf39039960] [world 2f1906870a] (2026-11-06T02:49:53Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_docexamples test_docs test_doctor test_left_out test_models test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [84.00s] [ran] [tree b0cf39039960] [world 2f1906870a] (2026-11-06T02:52:22Z)
## Log
- 2026-11-06T02:34:52Z created
- 2026-11-06T02:35:01Z set scope=['plugin/tests/test_docexamples.py', 'README.md', 'MASTER.md', 'INSTALL.md', 'plugin/skills', 'plugin/commands', 'plugin/rules/foreman.md', 'CHANGELOG.md']
- 2026-11-06T02:35:13Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3289.builder.md
- 2026-11-06T02:35:58Z focused
- 2026-11-06T02:36:02Z predicted from its closes: 4 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2768 [CLEAN M, done, 3 steps] The skills, commands and output style say Sampo (T-2742 step 5b): every prose Foreman in plugin/skills, plugin/commands and plugin/output…
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- T-2808 [CLEAN M, done, 3 steps] Agents, plugin and marketplace descriptions, install.sh's messages and the last skill, command and README lines say Sampo (T-2742 step 5)…
- decision 2026-11-03: [outward] [cites: user steer: read SAMPO.md (plugin foreman@foreman becomes sampo@sampo; nothing a user already has may break)] [check: pending T-27…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_audit.py, plugin/tests/test_backlog.py, plugin/tests/test_board_export.py, plugin/tests/test_board_surfaces.py, plugin/tests/test_brainsto…
