---
id: T-1665
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/test_portability.py, CHANGELOG.md, plugin/lib/fmhome.py, MASTER.md, plugin/lib/fmguard.py, plugin/tests/test_guard.py, plugin/lib/fmsync.py, plugin/tests/test_sync.py]
depends_on: []
source: user
created: 2026-10-22T20:59:08Z
updated: 2026-10-23T04:53:18Z
base: ed44de6d06deb221951ef28ec8580acee494bae6
base_tree: 7729aadd139a744a50775a47717c81cf379d1e5c
plan0_at: 2026-10-23T03:32:21Z
plan0_scope: [plugin/lib/fmcli.py, plugin/tests/test_portability.py, CHANGELOG.md]
verified: strong
---
# fm home export and import: a tarball of Foreman's state without secrets, checked on import into an empty home
## Raw request
> fm home export and import: a tarball of Foreman's state without secrets, checked on import into an empty home
## Interpretation
fm home export [--out FILE] writes a tarball of Foreman's home state (tasks, decisions, research, settings) without secrets (redacted text, credential-shaped files left out) plus a manifest of hashes; fm home import FILE checks the manifest, refuses absolute or .. paths and links, and imports into an empty home.
## Assumptions (confidence)
## Acceptance criteria
- [x] export then import into an empty home round-trips tasks, drops a planted secret and refuses a path-traversal member — verify with `python3 plugin/tests/run.py test_portability.Home`
## Non-goals
## Approach (options → choice → why)
Options: rsync the folder (copies secrets, no checks); a git bundle (state isn't a repo); a checked tarball. Choice: the tarball with a manifest: one file, verifiable, safe to unpack.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] tarfile writer using redact and the credential check
3. [x] import with a manifest hash check
## Resume here
## Docs impact
MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_portability.Home` → ✗ exit 1 · Ran 6 tests in 5.1s (1 classes, 16 at a time; slowest: Home 3s) / FAILED (1 classes) [ran] [tree 2f3f3680daae] (2026-10-23T03:34:56Z)
- (step 2) `python3 plugin/tests/run.py test_portability.Home` → exit 0 · Ran 6 tests in 23.9s (1 classes, 16 at a time; slowest: Home 21s) / OK [ran] [tree 1c54f73b4a90] (2026-10-23T03:40:21Z)
- (step 3) `python3 plugin/tests/run.py test_portability.Home test_help` → exit 0 · Ran 12 tests in 23.1s (4 classes, 16 at a time; slowest: Home 21s, Help 7s, PromptApprovals 6s) / OK [ran] [tree 1c54f73b4a90] (2026-10-23T03:40:48Z)
- (step 1) `python3 plugin/tests/run.py test_portability test_guard.UntestedRuleSites` → ✗ exit 1 · Ran 15 tests in 6.6s (2 classes, 16 at a time; slowest: Home 6s, UntestedRuleSites 0s) / FAILED (2 classes) [ran] [tree 830b490db91b] (2026-10-23T03:59:42Z)
- (step 2) `python3 plugin/tests/run.py test_portability test_guard` → exit 0 · Ran 282 tests in 17.5s (79 classes, 16 at a time; slowest: Mutation 17s, GuardAgainstBash 10s, Home 9s) / OK [ran] [tree c19576348107] (2026-10-23T04:02:23Z)
- (step 3) `python3 plugin/tests/run.py test_portability test_help test_sync` → exit 0 · Ran 34 tests in 33.1s (6 classes, 16 at a time; slowest: Sync 33s, Home 16s, Help 2s) / OK [ran] [tree c19576348107] (2026-10-23T04:02:58Z)
- (step 1) `python3 plugin/tests/run.py test_portability test_sync` → ✗ exit 1 · Ran 36 tests in 25.1s (3 classes, 16 at a time; slowest: Sync 24s, Home 18s, BoardSurfaces 1s) / FAILED (2 classes) [ran] [tree 53e587ee10a4] (2026-10-23T04:41:15Z)
- (step 2) `python3 plugin/tests/run.py test_portability test_guard test_sync` → exit 0 · Ran 307 tests in 39.2s (81 classes, 16 at a time; slowest: Sync 38s, Home 33s, Mutation 30s) / OK [ran] [tree d6fae4b571c3] (2026-10-23T04:44:49Z)
- (step 3) `python3 plugin/tests/run.py test_portability test_help` → ✗ exit 1 · Ran 25 tests in 13.4s (4 classes, 16 at a time; slowest: Home 13s, Help 1s, PromptApprovals 1s) / FAILED (1 classes) [ran] [tree d6fae4b571c3] (2026-10-23T04:45:03Z)
- (step 3) `python3 plugin/tests/run.py test_portability test_help` → exit 0 · Ran 25 tests in 10.8s (4 classes, 16 at a time; slowest: Home 10s, Help 1s, PromptApprovals 1s) / OK [ran] [tree 8093f0383090] (2026-10-23T04:45:43Z)
- (ac 1) `python3 plugin/tests/run.py test_portability test_sync` → exit 0 · Ran 36 tests in 23.8s (3 classes, 16 at a time; slowest: Sync 23s, Home 18s, BoardSurfaces 1s) / OK [ran] [tree fcb8e79c0585] (2026-10-23T04:51:38Z)
- (step 1) `python3 plugin/tests/run.py test_portability.Home test_guard` → exit 0 · Ran 289 tests in 24.2s (79 classes, 16 at a time; slowest: Home 24s, Mutation 23s, GuardAgainstBash 20s) / OK [ran] [tree fcb8e79c0585] (2026-10-23T04:52:13Z)
- (ac 1) `python3 plugin/tests/run.py test_portability.Home` → exit 0 · Ran 18 tests in 19.9s (1 classes, 16 at a time; slowest: Home 20s) / OK [ran] [tree fcb8e79c0585] (2026-10-23T04:52:35Z)
- (audit intent) `two fm-reviewer passes (first: 2 HIGH, 2 MEDIUM grant/agent-run/redaction/atomicity; second: 1 HIGH active-brief import, invisible-character audit forgery also in fm sync, meta types); all fixed test-first; spot-checked _brief (active→planned, lease marks dropped, confirm set) and _from_mirror (plain before the subs)` → fm home export writes Foreman's state as one redacted tarball with a hash manifest; fm home import restores it into an empty home [tree fcb8e79c0585] (2026-10-23T04:52:35Z)
- (audit adversary) `two fm-reviewer passes (first: 2 HIGH, 2 MEDIUM grant/agent-run/redaction/atomicity; second: 1 HIGH active-brief import, invisible-character audit forgery also in fm sync, meta types); all fixed test-first; spot-checked _brief (active→planned, lease marks dropped, confirm set) and _from_mirror (plain before the subs)` → import is user-only (guard); an allowlist per project; meta keeps only typed safe keys; briefs lose grants, run marks, counted audits, lease marks and focus, and open ones wait for the user's confirm; trust, plugin trust, PANIC, code.toml, asks and fixes refuse the archive; links, devices and non-regular members refused; header records over 64 KB refused before tarfile reads them, failing closed if tarfile changes; check_run/evidence events dropped [tree fcb8e79c0585] (2026-10-23T04:52:35Z)
- (audit edge) `two fm-reviewer passes (first: 2 HIGH, 2 MEDIUM grant/agent-run/redaction/atomicity; second: 1 HIGH active-brief import, invisible-character audit forgery also in fm sync, meta types); all fixed test-first; spot-checked _brief (active→planned, lease marks dropped, confirm set) and _from_mirror (plain before the subs)` → a failure after the rename rolls the import back; Infinity sizes, nested names and truncated archives are refused without a traceback; next_id moves past imported ids; a redacted ledger's broken chain is named [tree fcb8e79c0585] (2026-10-23T04:52:35Z)
- (audit operator) `two fm-reviewer passes (first: 2 HIGH, 2 MEDIUM grant/agent-run/redaction/atomicity; second: 1 HIGH active-brief import, invisible-character audit forgery also in fm sync, meta types); all fixed test-first; spot-checked _brief (active→planned, lease marks dropped, confirm set) and _from_mirror (plain before the subs)` → export names every file it left out and why [tree fcb8e79c0585] (2026-10-23T04:52:35Z)
## Log
- 2026-10-22T20:59:08Z created
- 2026-10-22T20:59:09Z set scope=['plugin/lib/fmcli.py', 'plugin/tests/test_portability.py', 'CHANGELOG.md']
- 2026-10-22T20:59:10Z split from T-1550 (L) by recon; works from Claude Code too (an fm verb, /foreman: command, skill or the foreman-ui mod)
- 2026-10-22T21:30:04Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_portability.Home`
- 2026-10-22T21:30:27Z criterion 1 text: export then import into an empty home round-trips tasks, drops a planted secret and refuses a path-traversal member — verify with python3 plugin/tests/run.py test_portability.Home → export then import into an empty home round-trips tasks, drops a planted secret and refuses a path-traversal member
- 2026-10-23T03:32:02Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1665.builder.md
- 2026-10-23T03:32:20Z focused
- 2026-10-23T03:38:39Z set scope=['plugin/lib/fmcli.py', 'plugin/tests/test_portability.py', 'CHANGELOG.md', 'plugin/lib/fmhome.py', 'MASTER.md']
- 2026-10-23T03:58:24Z set scope=['plugin/lib/fmcli.py', 'plugin/tests/test_portability.py', 'CHANGELOG.md', 'plugin/lib/fmhome.py', 'MASTER.md', 'plugin/lib/fmguard.py', 'plugin/tests/test_guard.py']
- 2026-10-23T04:40:03Z set scope=['plugin/lib/fmcli.py', 'plugin/tests/test_portability.py', 'CHANGELOG.md', 'plugin/lib/fmhome.py', 'MASTER.md', 'plugin/lib/fmguard.py', 'plugin/tests/test_guard.py', 'plugin/lib/fmsync.py', 'plugin/tests/test_sync.py']
- 2026-10-23T04:40:03Z scope: fmsync.py and test_sync.py for the plain-first order in _from_mirror (second review, item 2)
- 2026-10-23T04:51:05Z merged worktree-agent-ada1a5c7c37eda848 (9 file(s))
- 2026-10-23T04:51:06Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ada1a5c7c37eda848
- 2026-10-23T04:51:12Z focused
- 2026-10-23T04:52:13Z scope: plugin/lib/fmhome.py (new), plugin/lib/fmsync.py (plain first in _from_mirror), plugin/lib/fmguard.py (home import user-only), plugin/lib/fmcli.py (home verb), plugin/tests/test_sync.py, MASTER.md, CHANGELOG.md
- 2026-10-23T04:53:18Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0263-review-1: Findings come from reading the diff plus `fmcore.py`, `fmmap.py` and `fmrecall.py`. I did not run any tests. Line numbers for new code are diff…
- research T-1606-review: Verdict: changes needed.** The core works, but the note's "logs keep it redacted" claim is false on one path, and the report-and-file flow puts t…
- research rsi-pass-2: 1. **Answer.** Of the four guard false positives, two can be made precise without opening a bypass. These are the `secrets.txt` scratch file, and th…
- decision 2026-10-22: T-1422: dropped the plan reach lint (hosts/paths in a planner's plan → refuse). Two reviews (research T-1422-review, -review2) showed it either refu…
- likely tests for the scope: plugin/tests/test_cli.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmguard.py, plugin/lib/fmhome.py, plugin/lib/fmsync.py, plugin/tests/test_guard.py, plugin/tests/test_portability.py, plugin/tests/test_sync.py; re-ground the plan against them before editing
## Lessons
- Importing state is a trust boundary: allowlist what may come in and strip every field that grants or marks work done
## Plan gaps
- failed first: step 1 failing test
## Files touched
- plugin/tests/test_portability.py
- plugin/lib/fmhome.py
- plugin/lib/fmcli.py
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- MASTER.md
- CHANGELOG.md
- plugin/tests/test_sync.py
- plugin/lib/fmsync.py
