---
id: T-1187
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-16T12:38:39Z
updated: 2026-10-16T13:36:06Z
base: 900890767a7e72d68f22f83b40bdd65e84d018d2
base_tree: 47811081b0e669f671d883b80b5a449d97e774a2
plan0_at: 2026-10-16T13:08:00Z
plan0_scope: []
verified: strong
---
# `fm guard mine` lists the last N days of guard refusals with their full command, today's r
## Raw request
> FEATURE: `fm guard mine` lists the last N days of guard refusals with their full command, today's replay verdict, and a label (rewritten and passed, retried unchanged, or abandoned) taken from the next events of the same session.
> DONE-WHEN: a new test in plugin/tests/test_guard_cases.py seeds guard_block events plus follow-up events and sees `fm guard mine --json` return each refusal with the right label.
## Interpretation
Grounding guard friction needed a hand-written transcript miner. fm guard mine [--days N] [--json] lists the real guard refusals from this machine's Claude Code transcripts (~/.claude/projects/<this project>/*.jsonl): each with its full command (redacted), the rule message, today's verdict for the same command (fm guard try's decision path, or replay's default when no session context), and a label from what the session did next: rewritten and passed, retried unchanged, or abandoned. Grouped by rule with counts, so a friction pass sees the real commands.
## Assumptions (confidence)
## Acceptance criteria
- [x] with seeded transcript files, fm guard mine --json returns each refusal with its command, rule, today's verdict and the right label (rewritten-passed, retried-unchanged, abandoned), and ignores outputs that merely quote the refusal text — verify with `python3 plugin/tests/run.py test_guard_mine`
## Non-goals
## Approach (options → choice → why)
Options: (a) a reader over transcripts pairing Bash tool_use with tool_result whose text starts with the guard's refusal prefix (is_error), classifying the next Bash call in the same file; today's verdict from fmreplay's default-verdict function; output capped (top rules, 5 examples each) with --json for everything; (b) log full commands in guard_block ledger events (privacy cost on every refusal; rejected); (c) leave it to recon agents (today's manual way). Choice: (a). Read-only; transcripts are local data, treated as untrusted text (redacted, cut to 400 chars per command in text output).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests (test_guard_mine.py) with seeded jsonl transcripts
2. [x] fm guard mine in fmreplay (or a new module), registered beside guard try/wrong
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_guard_mine` → ✗ exit 1 · Ran 2 tests in 4.6s (1 classes, 16 at a time; slowest: GuardMine 2s) / FAILED (1 classes) [ran] [tree d947878cbc36] (2026-10-16T13:09:00Z)
- (step 2) `python3 plugin/tests/run.py test_guard_mine` → exit 0 · Ran 2 tests in 1.9s (1 classes, 16 at a time; slowest: GuardMine 1s) / OK [ran] [tree 9d4901c5c627] (2026-10-16T13:09:46Z)
- (step 2) `python3 plugin/tests/run.py test_guard_mine test_replay` → exit 0 · Ran 14 tests in 4.2s (4 classes, 16 at a time; slowest: Replay 4s, GuardMine 2s, GuardCases 1s) / OK [ran] [tree 82ec2e995d92] (2026-10-16T13:24:00Z)
- (ac 1) `python3 plugin/tests/run.py test_guard_mine test_replay` → exit 0 · Ran 14 tests in 3.5s (4 classes, 16 at a time; slowest: Replay 3s, GuardMine 1s, GuardCases 0s) / OK [ran] [tree 4185a5c9978d] (2026-10-16T13:28:51Z)
- (ac 1) `python3 plugin/tests/run.py test_guard_mine test_replay` → exit 0 · Ran 14 tests in 3.0s (4 classes, 16 at a time; slowest: Replay 3s, GuardMine 1s, GuardCases 0s) / OK [ran] [tree b21f699424f8] (2026-10-16T13:29:14Z)
- (ac 1) `python3 plugin/tests/run.py test_guard_mine` → exit 0 · Ran 5 tests in 1.8s (1 classes, 16 at a time; slowest: GuardMine 2s) / OK [ran] [tree 1ef4afce4155] (2026-10-16T13:29:31Z)
- (audit intent) `reviewer: one fm-reviewer pass found escape characters printed, a crash from the home folder, sessions in subdirectories/worktrees missed, the next-call heuristic and parse cost; builder fixed all; I ran it on real data, found it matched nothing because real results carry a hook-error prefix, fixed the regex and the fixture, and it now lists 48 refusals in 2 days` → the real refusals, with commands, in one place [tree 1ef4afce4155] (2026-10-16T13:29:31Z)
- (audit adversary) `reviewer: one fm-reviewer pass found escape characters printed, a crash from the home folder, sessions in subdirectories/worktrees missed, the next-call heuristic and parse cost; builder fixed all; I ran it on real data, found it matched nothing because real results carry a hook-error prefix, fixed the regex and the fixture, and it now lists 48 refusals in 2 days` → transcript text untrusted: redacted, control characters stripped, sizes capped; replay only parses [tree 1ef4afce4155] (2026-10-16T13:29:31Z)
- (audit edge) `reviewer: one fm-reviewer pass found escape characters printed, a crash from the home folder, sessions in subdirectories/worktrees missed, the next-call heuristic and parse cost; builder fixed all; I ran it on real data, found it matched nothing because real results carry a hook-error prefix, fixed the regex and the fixture, and it now lists 48 refusals in 2 days` → home-folder cwd, malformed lines, worktree sessions, --days clamped [tree 1ef4afce4155] (2026-10-16T13:29:31Z)
- (audit operator) `reviewer: one fm-reviewer pass found escape characters printed, a crash from the home folder, sessions in subdirectories/worktrees missed, the next-call heuristic and parse cost; builder fixed all; I ran it on real data, found it matched nothing because real results carry a hook-error prefix, fixed the regex and the fixture, and it now lists 48 refusals in 2 days` → grouped by rule, 5 examples each, --json for all [tree 1ef4afce4155] (2026-10-16T13:29:31Z)
- (audit maintainer) `reviewer: one fm-reviewer pass found escape characters printed, a crash from the home folder, sessions in subdirectories/worktrees missed, the next-call heuristic and parse cost; builder fixed all; I ran it on real data, found it matched nothing because real results carry a hook-error prefix, fixed the regex and the fixture, and it now lists 48 refusals in 2 days` → lives beside replay, reusing its verdict function [tree 1ef4afce4155] (2026-10-16T13:29:31Z)
- (ac 1) `python3 plugin/tests/run.py test_guard_cases test_guard_mine test_replay` → exit 0 · Ran 24 tests in 2.9s (4 classes, 16 at a time; slowest: Replay 3s, GuardCases 2s, GuardMine 1s) / OK [ran] [tree 5081d10ba123] (2026-10-16T13:34:28Z)
- `python3 plugin/tests/run.py test_guard_mine` → exit 0 · Ran 5 tests in 0.7s (1 classes, 16 at a time; slowest: GuardMine 1s) / OK [ran] [tree 5081d10ba123] (2026-10-16T13:34:36Z)
- (audit intent) `reviewer: one fm-reviewer pass found escape characters printed, a crash from the home folder, sessions in subdirectories/worktrees missed, the next-call heuristic and parse cost; builder fixed all; I ran it on real data, found it matched nothing because real results carry a hook-error prefix, fixed the regex and the fixture, and it now lists 48 refusals in 2 days; replay's transcript dir now follows CLAUDE_CONFIG_DIR and the replay-gate test no longer reads real transcripts` → the real refusals, with commands, in one place [tree 5081d10ba123] (2026-10-16T13:34:36Z)
- (audit adversary) `reviewer: one fm-reviewer pass found escape characters printed, a crash from the home folder, sessions in subdirectories/worktrees missed, the next-call heuristic and parse cost; builder fixed all; I ran it on real data, found it matched nothing because real results carry a hook-error prefix, fixed the regex and the fixture, and it now lists 48 refusals in 2 days; replay's transcript dir now follows CLAUDE_CONFIG_DIR and the replay-gate test no longer reads real transcripts` → transcript text untrusted: redacted, control characters stripped, sizes capped; replay only parses [tree 5081d10ba123] (2026-10-16T13:34:36Z)
- (audit edge) `reviewer: one fm-reviewer pass found escape characters printed, a crash from the home folder, sessions in subdirectories/worktrees missed, the next-call heuristic and parse cost; builder fixed all; I ran it on real data, found it matched nothing because real results carry a hook-error prefix, fixed the regex and the fixture, and it now lists 48 refusals in 2 days; replay's transcript dir now follows CLAUDE_CONFIG_DIR and the replay-gate test no longer reads real transcripts` → home-folder cwd, malformed lines, worktree sessions, --days clamped [tree 5081d10ba123] (2026-10-16T13:34:36Z)
- (audit operator) `reviewer: one fm-reviewer pass found escape characters printed, a crash from the home folder, sessions in subdirectories/worktrees missed, the next-call heuristic and parse cost; builder fixed all; I ran it on real data, found it matched nothing because real results carry a hook-error prefix, fixed the regex and the fixture, and it now lists 48 refusals in 2 days; replay's transcript dir now follows CLAUDE_CONFIG_DIR and the replay-gate test no longer reads real transcripts` → grouped by rule, 5 examples each, --json for all [tree 5081d10ba123] (2026-10-16T13:34:36Z)
- (audit maintainer) `reviewer: one fm-reviewer pass found escape characters printed, a crash from the home folder, sessions in subdirectories/worktrees missed, the next-call heuristic and parse cost; builder fixed all; I ran it on real data, found it matched nothing because real results carry a hook-error prefix, fixed the regex and the fixture, and it now lists 48 refusals in 2 days; replay's transcript dir now follows CLAUDE_CONFIG_DIR and the replay-gate test no longer reads real transcripts` → lives beside replay, reusing its verdict function [tree 5081d10ba123] (2026-10-16T13:34:36Z)
## Log
- 2026-10-16T12:38:39Z created
- 2026-10-16T13:07:49Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1187.builder.md
- 2026-10-16T13:08:00Z focused
- 2026-10-16T13:28:42Z merged worktree-agent-a21f175fdcd5fc2c9 (4 file(s))
- 2026-10-16T13:28:46Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a21f175fdcd5fc2c9
- 2026-10-16T13:28:47Z focused
- 2026-10-16T13:29:28Z scope: refusal regex accepts the '<Event> hook error: ' prefix real transcripts carry (found by running it on real data); MASTER.md and CHANGELOG.md
- 2026-10-16T13:34:35Z scope: replay's _logs honours CLAUDE_CONFIG_DIR (reviewer note); test_guard_cases points it at an empty folder (the replay gate test read this machine's 5,000 real commands: 20 s and load-flaky)
- 2026-10-16T13:36:05Z done
- 2026-10-16T13:36:06Z committed a7c61eff (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0783 [PERFORMANCE M, done, 3 steps] Big Bash outputs reach the model as head, tail and failure lines, with the full text in a file (opt-in) — lesson: measure a lossy c…
- research brainstorm-20261016-round4: 195 ideas, 46 clusters, each grounded against plugin/lib, hooks, skills, workflows, mods/foreman-ui and CHANGELOG.md. Paths are rela…
- T-1171 [FIX M, done, 2 steps] Guard: _drives_fm (fmguard.py:1364) treats any heredoc that doesn't parse, and fm-import t — lesson: mine full commands before relaxing a g…
- decision 2026-10-15: Round 4 slate: 6 builds from 31 grounded clusters (437 ideas): install asks before bypass, INSTALL.md for agents, fm demo (no-model), marketplace in…
## Lessons
- seed fixtures from a captured real record, not from the format you expect: the fixture lacked the hook-error prefix and the tool matched nothing real
## Plan gaps
- failed first: step 1 Failing tests (test_guard_mine.py) with seeded jsonl transcripts
## Files touched
- plugin/tests/test_guard_mine.py
- plugin/lib/fmcli.py
- plugin/lib/fmhooks.py
- plugin/lib/fmreplay.py
- MASTER.md
- CHANGELOG.md
- plugin/tests/test_guard_cases.py
