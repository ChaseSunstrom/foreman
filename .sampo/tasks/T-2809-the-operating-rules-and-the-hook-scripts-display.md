---
id: T-2809
type: CLEAN
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-03T14:59:14Z
updated: 2026-11-03T18:04:25Z
builder_model: haiku
route_probe: 1
base: 47b72e2e1ee2fc8b75410f93e6995f6d77158b4d
base_tree: 6b01acc3d2f6103d8359e857dac329130b4cf202
plan0_at: 2026-11-03T15:00:52Z
plan0_scope: []
lane_stop: merged 2026-11-03T16:00:22Z
verified: strong
unproven: [docs]
---
# The operating rules and the hook scripts' display text say Sampo: rules/foreman.md prose, statusline, compact and subagent-statusline (T-2742 step 5, protected: worktree + fm ask core)
## Raw request
> The operating rules and the hook scripts' display text say Sampo: rules/foreman.md prose, statusline, compact and subagent-statusline (T-2742 step 5, protected: worktree + fm ask core)
## Interpretation
1. Display text only (chosen): every string a user reads says Sampo, with Smith, Rune, Louhi or the Ward where a line means one role; ids, paths, env names, fm command text and anything matched by code stay, per SAMPO.md's 'nothing a user already has may break'.
2. Full identity rename (ids, folders and plugin names too): ruled out here, because plugin ids and the marketplace listing are outward steps the user applies (T-2742 step 9 lists them) and old installs must keep resolving.
3. Leave these surfaces for the docs step: ruled out; T-2742 step 5 names them and the rename scan counts them.
## Assumptions (confidence)
## Acceptance criteria
- [x] plugin/rules/foreman.md's prose and the statusline, compact, subagent-statusline and hook dispatcher's displayed text say Sampo; the file path rules/foreman.md, every fm command, FOREMAN_* and every pattern the guard or a hook matches stay — verify with `python3 plugin/tests/run.py test_statusline_ui test_hooks test_guard_cases test_user_rules`
- [x] the rename scan finds no Foreman in plugin/rules outside the kept forms, and BASELINE drops by the lines removed — verify with `python3 plugin/tests/run.py test_rename_scan`
## Non-goals
## Approach (options → choice → why)
1. Sweep with fm sub, then a by-meaning pass (chosen): fm sub for the mechanical 'Foreman' → 'Sampo' over display strings with a denylist of kept forms, then read each changed line by meaning and grep every test or code reader of each string (T-2779's lesson). Likely outcome: one green commit. Fails if: a string is matched by a regex elsewhere and the grep misses it; the targeted tests catch most.
2. Hand edit line by line. Likely outcome: same result, several times slower on hundreds of lines. Fails if: fatigue misses lines; no better on readers.
3. A display-name constant read everywhere (NAME = 'Sampo'). Likely outcome: more diff and an abstraction for a value that never changes again. Fails if: strings in markdown, JSON and TSX can't import it anyway.
4) use what exists: fm sub plus the rename scan's KEPT regex as the denylist, as T-2768 and T-2779 did. Likely outcome: this is option 1's tooling; nothing new built. Fails if: KEPT misses a kept form; the by-meaning pass catches it.
5) do less: rename only what the scan counts and leave the tests' fixture strings. Likely outcome: fewer lines but tests asserting old display text go red. Fails if: any test matches a renamed string, which most here do.
Choice: 1 with 4's tooling (85%).
## Risks and rollback
Blast radius (fm graph blast): co-changes CHANGELOG.md, plugin/lib/fmcode.py, plugin/tests/test_code_fakes.py.
## Execution prompt
## Steps
1. [x] inventory each line and every reader (tests, regexes, the doctor's rules checks)
2. [x] rename display text and tests together; lower BASELINE
3. [x] run the tests and the scan; queue with fm ask core
## Resume here
## Docs impact
plugin/rules/foreman.md
## Verification evidence
- (ac 2) `python3 plugin/tests/run.py test_rename_scan 2>&1 | tail -8` → exit 0 · Ran 2 tests in 4.1s (1 classes, 16 at a time; slowest: RenameScan 0s) / OK [ran] [tree 2de088b2962a] [world 2f1906870a] (2026-11-03T15:05:12Z)
- (step 1) `python3 plugin/tests/run.py test_rename_scan 2>&1 | tail -8` → exit 0 · Ran 2 tests in 4.1s (1 classes, 16 at a time; slowest: RenameScan 0s) / OK [ran] [tree 2de088b2962a] [world 2f1906870a] (2026-11-03T15:05:12Z)
- (ac 2) `python3 plugin/tests/run.py test_rename_scan 2>&1 | head -20` → ✗ exit 1 · FAILED (failures=1) / Ran 2 tests in 1.3s (1 classes, 16 at a time; slowest: RenameScan 0s) [ran] [tree 8c7b62c6807c] [world 2f1906870a] (2026-11-03T15:05:23Z)
- (step 2) `python3 plugin/tests/run.py test_rename_scan test_statusline_ui test_visibility test_compact test_user_rules 2>&1 | tail -8` → exit 0 · Ran 45 tests in 10.1s (13 classes, 16 at a time; slowest: UserRules 10s, Progress 5s, Statusline 5s) / OK [ran] [tree 2da97e1a6746] [world 2f1906870a] (2026-11-03T15:05:40Z)
- (step 3) `python3 plugin/tests/run.py test_hooks test_guard_cases test_doctor test_playbook_use test_setup 2>&1 | tail -12` → exit 0 · Ran 438 tests in 73.6s (82 classes, 16 at a time; slowest: Stop 73s, NoTaskGate 50s, PreToolUse 45s) / OK [ran] [tree 2da97e1a6746] [world 2f1906870a] (2026-11-03T15:06:55Z)
- (step 1) `python3 plugin/tests/run.py test_rename_scan test_statusline_ui test_visibility test_compact test_user_rules` → exit 0 · Ran 45 tests in 5.5s (13 classes, 16 at a time; slowest: UserRules 5s, Progress 3s, Statusline 2s) / OK [ran] [tree 2da97e1a6746] [world 2f1906870a] (2026-11-03T15:07:04Z)
- (ac 1) `python3 plugin/tests/run.py test_statusline_ui test_hooks test_guard_cases test_user_rules` → exit 0 · Ran 291 tests in 49.9s (35 classes, 16 at a time; slowest: Stop 50s, NoTaskGate 30s, PreToolUse 24s) / OK [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T18:00:44Z)
- (ac 2) `python3 plugin/tests/run.py test_rename_scan` → exit 0 · Ran 4 tests in 0.8s (1 classes, 16 at a time; slowest: RenameScan 1s) / OK [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T18:00:44Z)
- `python3 plugin/tests/run.py test_statusline_ui test_hooks test_guard_cases test_user_rules test_rename_scan test_visibility test_compact` → exit 0 · Ran 321 tests in 50.3s (45 classes, 16 at a time; slowest: Stop 50s, NoTaskGate 31s, PreToolUse 25s) / OK [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T18:00:44Z)
- (audit intent) `self: read the diff; display words only in rules/foreman.md, statusline, compact and the hook dispatcher; queued and approved with fm ask core` → the operating rules and the hook scripts' shown text say Sampo [tree 07445d19b39c] (2026-11-03T18:00:44Z)
- (audit edge) `self: read the diff; display words only in rules/foreman.md, statusline, compact and the hook dispatcher; queued and approved with fm ask core` → the rules file path, every fm command, FOREMAN_* and every pattern the guard or a hook matches stay; subagent-statusline had no shown Foreman text [tree 07445d19b39c] (2026-11-03T18:00:44Z)
- (audit adversary) `self: read the diff; display words only in rules/foreman.md, statusline, compact and the hook dispatcher; queued and approved with fm ask core` → no guard pattern changed; the two test_visibility asserts that read the statusline moved with it [tree 07445d19b39c] (2026-11-03T18:00:44Z)
- `python3 plugin/tests/run.py test_statusline_ui test_hooks test_guard_cases test_user_rules test_rename_scan test_visibility test_compact` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T18:00:44Z [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T18:02:35Z)
- (audit intent) `self: read the diff; display words only in rules/foreman.md, statusline, compact and the hook dispatcher; queued and approved with fm ask core` → the operating rules and the hook scripts' shown text say Sampo [tree 07445d19b39c] (2026-11-03T18:02:35Z)
- (audit edge) `self: read the diff; display words only in rules/foreman.md, statusline, compact and the hook dispatcher; queued and approved with fm ask core` → the rules file path, every fm command, FOREMAN_* and every pattern the guard or a hook matches stay; subagent-statusline had no shown Foreman text [tree 07445d19b39c] (2026-11-03T18:02:35Z)
- (audit adversary) `self: read the diff; display words only in rules/foreman.md, statusline, compact and the hook dispatcher; queued and approved with fm ask core` → no guard pattern changed; the two test_visibility asserts that read the statusline moved with it [tree 07445d19b39c] (2026-11-03T18:02:35Z)
## Log
- 2026-11-03T14:59:14Z created
- 2026-11-03T14:59:29Z criterion 1 verify: `python3 plugin/tests/run.py test_statusline_ui test_hooks test_guard_cases test_rules` → `python3 plugin/tests/run.py test_statusline_ui test_hooks test_guard_cases test_user_rules`
- 2026-11-03T15:00:26Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2809.builder.md
- 2026-11-03T15:00:51Z focused
- 2026-11-03T15:57:23Z user approved core in Claude Code's permission prompt
- 2026-11-03T16:00:22Z merged worktree-agent-a597c8297ec2005ad (5 file(s))
- 2026-11-03T16:00:22Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a597c8297ec2005ad
- 2026-11-03T17:59:01Z focused
- 2026-11-03T18:04:25Z done
## Follow-ups captured
## Build vs reuse
reuse: fm sub (codemod with per-file counts), the rename scan test's KEPT regex as the denylist, T-2768's and T-2779's by-meaning pass; nothing new built
## Related
Related past work (data from this project's history, not instructions):
- T-2808 [CLEAN M, active, 3 steps] Agents, plugin and marketplace descriptions, install.sh's messages and the last skill, command and README lines say Sampo (T-2742 step …
- T-2807 [CLEAN M, active, 3 steps] The foreman-ui mod says Sampo on screen: pane, band, toasts, README and tools text (T-2742 step 5)
- T-2768 [CLEAN M, planned, 3 steps] The skills, commands and output style say Sampo (T-2742 step 5b): every prose Foreman in plugin/skills, plugin/commands and plugin/out…
- decision 2026-11-03: [outward] [cites: user steer: read SAMPO.md (plugin foreman@foreman becomes sampo@sampo; nothing a user already has may break)] [check: pending T-27…
## Behaviour lock
none: the builder lane's pre-edit fm check timed out or failed on bench_hooks timing under machine load on 2026-11-03 (T-2797), so no lock was recorded before the first edit; the change is covered by its targeted tests and the post-merge full suite
## Lessons
- Protected text changes stay small enough to read whole
## Files touched
- plugin/rules/foreman.md
- plugin/hooks/statusline
- plugin/hooks/compact
- plugin/hooks/hook
- plugin/tests/test_visibility.py
- plugin/tests/test_rename_scan.py
