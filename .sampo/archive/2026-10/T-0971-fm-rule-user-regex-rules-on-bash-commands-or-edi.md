---
id: T-0971
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-10-15T22:08:00Z
updated: 2026-10-15T23:05:11Z
base: 28189021aecf0dcb1a3526677c67d9beb69859f5
base_tree: 65a96d36ccb49e80b6bf06f0c0d35241380d5671
verified: strong
---
# Fm rule: user regex rules on Bash commands or edited paths that warn or block, enforced by
## Raw request
> fm rule: user regex rules on Bash commands or edited paths that warn or block, enforced by the guard hook, addable from a correction, from hookify (research/T-0964-catalogue.md)
## Interpretation
User-authored rules, like hookify: a regex on Bash commands or on edited paths that warns or blocks, enforced by the guard hook, addable from a correction (a veto) so 'never do X again' becomes a real stop. Removing a rule is the user's call.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm rule add 'git push.*main' --on bash --block --why 'release.py pushes' makes the guard deny a matching Bash command with that why; --warn adds a note and lets it run; --on path matches an Edit/Write file path; a bad regex is refused at add time; fm rule rm from Claude is refused as self-authorize; fm rule add --from-veto N turns a recorded veto into a rule — verify with `python3 plugin/tests/run.py -k UserRules`
## Non-goals
## Approach (options → choice → why)
Options: fm rule add PATTERN --on bash|path --warn|--block --why TEXT, stored in the project's meta, checked in PreToolUse after the guard (a block denies with the why; a warn is a note), fm rule list, fm rule rm N refused from Claude as self-authorize, fm rule add --from-veto N (chosen: reuses the guard hook, no new hook); markdown rule files like hookify (another format to parse and keep safe); rules as vetoes only (they never block).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing UserRules tests
2. [x] fm rule verb, the PreToolUse check, the self-authorize rm, --from-veto; docs
## Resume here
<!-- auto -->
- 2026-10-15T23:02:34Z step 1/2: Failing UserRules tests
- git: foreman/build; 4 uncommitted: plugin/lib/fmcore.py, plugin/lib/fmguard.py, plugin/lib/fmhooks.py, plugin/tests/test_user_rules.py
- touched since last checkpoint: .claude/worktrees/agent-a714812d19c0f3e45/plugin/tests/test_user_rules.py, .claude/worktrees/agent-a714812d19c0f3e45/plugin/lib/fmcore.py, .claude/worktrees/agent-a714812d19c0f3e45/plugin/lib/fmhooks.py, .claude/worktrees/agent-a714812d19c0f3e45/plugin/lib/fmguard.py, .claude/worktrees/agent-a714812d19c0f3e45/plugin/lib/fmcli.py, .claude/worktrees/agent-a714812d19c0f3e45/MASTER.md, plugin/tests/test_user_rules.py, /tmp/claude-1000/-home-<user>--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/rulesfix.py, plugin/lib/fmcore.py, plugin/lib/fmguard.py, plugin/lib/fmhooks.py
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k UserRules` → ✗ exit 1 · Ran 7 tests in 6.2s (1 classes, 16 at a time; slowest: UserRules 5s) / FAILED (1 classes) [ran] [tree 79853841d0f4] (2026-10-15T22:52:47Z)
- (step 2) `python3 plugin/tests/run.py -k UserRules` → exit 0 · Ran 7 tests in 3.2s (1 classes, 16 at a time; slowest: UserRules 3s) / OK [ran] [tree 020fedfa3ae5] (2026-10-15T22:54:31Z)
- (step 1) `python3 plugin/tests/run.py -k UserRules` → exit 0 · Ran 9 tests in 5.4s (1 classes, 16 at a time; slowest: UserRules 5s) / OK [ran] [tree c864863b937c] (2026-10-15T23:05:04Z)
- (ac 1) `python3 plugin/tests/run.py -k UserRules` → exit 0 · Ran 9 tests in 5.2s (1 classes, 16 at a time; slowest: UserRules 5s) / OK [ran] [tree c864863b937c] (2026-10-15T23:05:10Z)
- (audit intent) `security-guidance review: 3 findings (Bash writes and symlinks skipped path rules; padding past the 4000-char scan hid a block match; python could call drop_rule/drop_veto) fixed test-first; test_user_rules/test_guard/test_hooks 266 OK` → block/warn rules on commands and paths, rm is the user's, veto→rule; matches the brief [tree c864863b937c] (2026-10-15T23:05:10Z)
- (audit adversary) `security-guidance review: 3 findings (Bash writes and symlinks skipped path rules; padding past the 4000-char scan hid a block match; python could call drop_rule/drop_veto) fixed test-first; test_user_rules/test_guard/test_hooks 266 OK` → a Bash write, a redirect, a symlink alias, 5000-char padding and a python heredoc calling the rule store are all refused in tests; past RULE_SCAN (or 4000 with no alarm) block rules fail closed [tree c864863b937c] (2026-10-15T23:05:10Z)
- (audit edge) `security-guidance review: 3 findings (Bash writes and symlinks skipped path rules; padding past the 4000-char scan hid a block match; python could call drop_rule/drop_veto) fixed test-first; test_user_rules/test_guard/test_hooks 266 OK` → an empty, unclosed or overlong regex is refused at add time; a catastrophic pattern is time-boxed and a block fails closed [tree c864863b937c] (2026-10-15T23:05:10Z)
## Log
- 2026-10-15T22:08:00Z created
- 2026-10-15T22:50:07Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0971.builder.md
- 2026-10-15T22:50:19Z focused
- 2026-10-15T22:58:20Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a714812d19c0f3e45 (branch worktree-agent-a714812d19c0f3e45 kept: not merged)
- 2026-10-15T22:59:42Z focused
- 2026-10-15T23:01:06Z merged foreman/T-0971 (6 file(s))
- 2026-10-15T23:05:10Z done
- 2026-10-15T23:05:11Z committed 9a87d19 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0433 [SECURITY M, done, 3 steps] Guard fuzzer: mutated real-bash forms never run a dangerous call unblocked — lesson: A guard's own tests find what its authors imagine…
- research T-0964-catalogue: Sources: research/T-0964-harness.md (claude-code-harness, feature by feature), research/T-0964-workflow.md (ECC,
- T-0786 [FEATURE M, done, 3 steps] fm page: the queue (and optionally a brainstorm catalogue) as one self-contained HTML page for a claude.ai Artifact, with Build/Veto pi…
- decision 2026-10-03: Self-approve T-0175 (L, guard): approach A
- similar finished tasks took 3–3 steps
## Lessons
- A rule on a path is only as strong as every way the path gets written: check Bash write targets and the realpath, and fail closed past the scan cap instead of reading a prefix.
## Plan gaps
- failed first: step 1 Failing UserRules tests
## Files touched
- plugin/tests/test_user_rules.py
- plugin/lib/fmcore.py
- plugin/lib/fmhooks.py
- plugin/lib/fmguard.py
- plugin/lib/fmcli.py
- MASTER.md
- CHANGELOG.md
