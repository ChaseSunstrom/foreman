---
id: T-0874
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T14:11:51Z
updated: 2026-10-15T14:42:56Z
base: 443eac5e7eef24d3cf345b3723d3afe8208c59fc
base_tree: 6bfe441055f70a6720847605b13e5d878de39b56
verified: strong
---
# Marketplace install works and is documented: /plugin marketplace add + /plugin install in a clean HOME gives a working Foreman, README shows it, and the first session says how to finish wiring when ~/.claude isn't wired
## Raw request
> Marketplace install works and is documented: /plugin marketplace add + /plugin install in a clean HOME gives a working Foreman, README shows it, and the first session says how to finish wiring when ~/.claude isn't wired
## Interpretation
Every popular rival installs with one /plugin install; Foreman's marketplace.json exists but only curl|bash is documented. A bare plugin install gets hooks and fm (plugin bin) but not the rules symlink, CLAUDE.md block or statusline; the first session should say so.
## Assumptions (confidence)
## Acceptance criteria
- [x] a SessionStart in a project whose ~/.claude isn't wired names fm install-user once; README documents the marketplace path — verify with `python3 plugin/tests/run.py test_hooks.SessionStart`
## Non-goals
## Approach (options → choice → why)
Options: (a) verify the bare path in a sandbox HOME, document it, add a one-time SessionStart note pointing at fm install-user; (b) make the plugin self-wire on first SessionStart (writes ~/.claude without consent); (c) docs only. Chose (a): honest, no silent writes.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Clean-HOME check of the bare marketplace install
2. [x] SessionStart 'finish wiring' note + README section
## Resume here
## Docs impact
README install section
## Verification evidence
- (step 1) `claude plugin list` → exit 0 · Path: ~/.claude/plugins/synced/5c6dfa37-93dd-4629-b988-4c203bfcc1c6_1c4f9a98-efaa-4a14-b5b3-7852713bd772/figma~g2 / Status: ✘ disabled [ran] [tree 2e663aba1f3c] (2026-10-15T14:40:32Z)
- (step 2) `python3 plugin/tests/run.py test_hooks.SessionStart` → exit 0 · Ran 12 tests in 9.6s (1 classes, 16 at a time; slowest: SessionStart 9s) / OK [ran] [tree 2e663aba1f3c] (2026-10-15T14:40:42Z)
- `python3 plugin/tests/run.py test_hooks.SessionStart` → ✗ exit 1 · Ran 12 tests in 9.7s (1 classes, 16 at a time; slowest: SessionStart 9s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 2e663aba1f3c] (2026-10-15T14:41:01Z)
- `python3 plugin/tests/run.py test_hooks.SessionStart` → exit 0 · Ran 12 tests in 9.5s (1 classes, 16 at a time; slowest: SessionStart 9s) / OK [ran] [tree 2e663aba1f3c] (2026-10-15T14:41:01Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmhooks.py — commit it through a task, or git checkout it back / fm doctor: OK (35 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                33.1    35.4     150  [0] / SessionEnd                  29.7    32.2     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman- [ran] [tree 2e663aba1f3c] (2026-10-15T14:42:37Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks.SessionStart` → exit 0 · Ran 12 tests in 9.6s (1 classes, 16 at a time; slowest: SessionStart 9s) / OK [ran] [tree 2e663aba1f3c] (2026-10-15T14:42:55Z)
- (audit intent) `self + live: in a throwaway HOME, claude plugin marketplace add <repo> and plugin install foreman@foreman succeeded, and the first SessionStart registered the project and ran; the rules were never loaded, which the new note fixes without writing to ~/.claude; README documents the /plugin path. Not verified: the GitHub-source form (/plugin marketplace add ChaseSunstrom/foreman), which needs the network; it uses the same .claude-plugin/marketplace.json` → a newcomer can install Foreman the way rivals install (two /plugin commands), with nothing outside the plugin changed, and the first session still follows Foreman's rules [tree 2e663aba1f3c] (2026-10-15T14:42:55Z)
- (audit edge) `self + live: in a throwaway HOME, claude plugin marketplace add <repo> and plugin install foreman@foreman succeeded, and the first SessionStart registered the project and ran; the rules were never loaded, which the new note fixes without writing to ~/.claude; README documents the /plugin path. Not verified: the GitHub-source form (/plugin marketplace add ChaseSunstrom/foreman), which needs the network; it uses the same .claude-plugin/marketplace.json` → the note appears only while ~/.claude/rules/foreman.md is missing, so wired installs see nothing new; it adds ~330 chars to SessionStart, inside the 2,000-char budget [tree 2e663aba1f3c] (2026-10-15T14:42:55Z)
## Log
- 2026-10-15T14:11:51Z created
- 2026-10-15T14:26:24Z focused
- 2026-10-15T14:35:04Z user approved plugin in Claude Code's permission prompt
- 2026-10-15T14:35:12Z plugin grant used for: claude plugin marketplace add
- 2026-10-15T14:35:26Z user approved plugin in Claude Code's permission prompt
- 2026-10-15T14:38:39Z user approved plugin in Claude Code's permission prompt
- 2026-10-15T14:38:39Z plugin grant used for: claude plugin install changes Claude Code's plugins, MCP servers or config [plugin foreman@foreman]
- 2026-10-15T14:42:55Z done
- 2026-10-15T14:42:56Z committed eff4058 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0855 [FIX M, done, 5 steps] A fresh install is clean and works from a shell: doctor passes and shows only problems, fm check finds the test runner,… — lesson: Walk thr…
- research brainstorm-round4-20261015: 437 ideas (9 lenses x 4 rounds + 3 deepen rounds, past every earlier run) from new evidence: a clean-HOME newcomer install, a survey…
- T-0854 [FIX M, done, 5 steps] A newcomer's first fm commands make sense: short --help, task new shows its values and an example, init/status say what… — lesson: The firs…
- decision 2026-10-15: Round 4 slate: 6 builds from 31 grounded clusters (437 ideas): install asks before bypass, INSTALL.md for agents, fm demo (no-model), marketplace in…
## Lessons
- Test the install path a rival's users would take; a plugin that only works after a bespoke installer loses them at step one
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/fmhooks.py
- README.md
