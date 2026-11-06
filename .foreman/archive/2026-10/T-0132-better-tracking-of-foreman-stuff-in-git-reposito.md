---
id: T-0132
type: SECURITY
tier: M
status: done
priority: normal
scope: [plugin/lib/fmsecrets.py, plugin/lib/fmcli.py, plugin/tests/test_secrets.py, CHANGELOG.md, MASTER.md, plugin/rules/foreman.md, plugin/tests/e2e/**]
depends_on: []
source: user
created: 2026-10-03T04:52:05Z
updated: 2026-10-03T07:49:44Z
base: ebfbbb7b6b6fea636e03a239e9e0fbe2a43e530a
base_tree: 57bf178d031511b3881a81a5a64d1602d8faa8c3
verified: strong
---
# Credential audit (fm secrets) and task-tagged commits
## Raw request
> better tracking of foreman stuff in git repositories, credential finding/auditing in repositories/claude stuff, etc.
## Interpretation
Two parts. (1) fm secrets: find credentials without printing them, in the working tree (tracked and untracked, not ignored), in git history on request (--history), and in Claude Code config (~/.claude.json, user and project settings, .mcp.json: literal keys in env/headers, secret formats, credential files readable by others, project config with a secret that git tracks). Exit 1 on any finding so it can gate. (2) Foreman's own commits (fm task finish --commit) carry a Foreman-Task trailer, are logged in the brief, and are refused when the lines they add look like a secret.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm secrets finds a planted key in the tree, one only in history (--history), and a literal key in a project .mcp.json, names where and what kind without printing the value, skips allowlisted lines, and exits 1 — verify with `python3 plugin/tests/run.py -k test_secrets`
- [x] fm task finish --commit adds a Foreman-Task trailer, logs the commit in the brief, and refuses (unstaged) when an added line looks like a secret — verify with `python3 plugin/tests/run.py -k test_secrets`
- [x] All gates pass — verify with `fm check`
## Non-goals
## Approach (options → choice → why)
Options: (a) extend fm doctor's git-hygiene check; (b) a separate fm secrets command in its own module that reuses fmcore's secret patterns, with the commit path calling the same line scanner on its staged diff. Choice: (b): doctor is a quick health check and history scans can be slow; one scanner for tree, history and commits keeps the patterns in one place. Lines marked 'pragma: allowlist secret' (the detect-secrets convention) are skipped so test fixtures can opt out.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red tests for the tree, history, Claude config and commit paths
2. [x] fmsecrets module and fm secrets command
3. [x] Commit trailer, brief log line and secret refusal in _commit_task
4. [x] Run it on this repo and ~/.claude; fix or allowlist what it finds
5. [x] Docs: MASTER, CHANGELOG, a plain-words rules line
## Resume here
## Docs impact
MASTER (file map, a 'Credentials and commits' paragraph), CHANGELOG; rules unchanged (the rules file is at its 6000-character budget; fm secrets is in fm help and MASTER).
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_secrets` → exit 0 · Ran 4 tests in 0.7s (2 classes, 16 at a time; slowest: Secrets 1s, MessageDisplay 0s) / OK [ran] [tree 55ffa5e3e895] (2026-10-03T07:45:19Z)
- (step 2) `python3 plugin/tests/run.py -k test_secrets` → exit 0 · Ran 4 tests in 0.7s (2 classes, 16 at a time; slowest: Secrets 1s, MessageDisplay 0s) / OK [ran] [tree 55ffa5e3e895] (2026-10-03T07:45:20Z)
- (step 3) `python3 plugin/tests/run.py -k test_secrets` → exit 0 · Ran 4 tests in 0.7s (2 classes, 16 at a time; slowest: Secrets 1s, MessageDisplay 0s) / OK [ran] [tree 55ffa5e3e895] (2026-10-03T07:45:21Z)
- (step 4) `fm secrets` → exit 0 · No credentials found (the working tree and Claude config; --history adds git history). [ran] [tree 55ffa5e3e895] (2026-10-03T07:45:21Z)
- (step 5) `python3 plugin/tests/run.py -k test_self_docs_match_the_code` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Checks 0s) / OK [ran] [tree 55ffa5e3e895] (2026-10-03T07:45:21Z)
- (step 1) `python3 plugin/tests/run.py -k test_secrets` → exit 0 · Ran 5 tests in 0.9s (2 classes, 16 at a time; slowest: Secrets 1s, MessageDisplay 0s) / OK [ran] [tree 31bf7e876ce5] (2026-10-03T07:49:32Z)
- (step 2) `python3 plugin/tests/run.py -k test_secrets` → exit 0 · Ran 5 tests in 0.9s (2 classes, 16 at a time; slowest: Secrets 1s, MessageDisplay 0s) / OK [ran] [tree 31bf7e876ce5] (2026-10-03T07:49:33Z)
- (step 3) `python3 plugin/tests/run.py -k test_secrets` → exit 0 · Ran 5 tests in 0.9s (2 classes, 16 at a time; slowest: Secrets 1s, MessageDisplay 0s) / OK [ran] [tree 31bf7e876ce5] (2026-10-03T07:49:34Z)
- (step 4) `fm secrets` → exit 0 · No credentials found (the working tree and Claude config; --history adds git history). [ran] [tree 31bf7e876ce5] (2026-10-03T07:49:34Z)
- (step 5) `python3 plugin/tests/run.py -k test_self_docs_match_the_code` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: Checks 0s) / OK [ran] [tree 31bf7e876ce5] (2026-10-03T07:49:34Z)
- (ac 1) `python3 plugin/tests/run.py -k test_secrets` → exit 0 · Ran 5 tests in 0.9s (2 classes, 16 at a time; slowest: Secrets 1s, MessageDisplay 0s) / OK [ran] [tree 31bf7e876ce5] (2026-10-03T07:49:44Z)
- (ac 2) `python3 plugin/tests/run.py -k test_secrets` → exit 0 · Ran 5 tests in 0.9s (2 classes, 16 at a time; slowest: Secrets 1s, MessageDisplay 0s) / OK [ran] [tree 31bf7e876ce5] (2026-10-03T07:49:44Z)
- (ac 3) `fm check` → exit 0 · ✓ all 5 gates passed on this exact tree already (run at 07:49 UTC); cached (fm check --fresh reruns) [ran] [tree 31bf7e876ce5] (2026-10-03T07:49:44Z)
- (audit intent) `One fm-reviewer pass (intent + adversary) found 8: four commit-check bypasses (diff.noprefix/mnemonicPrefix headers, -diff/binary files, the whole index committed but only task files scanned, a failed git diff read as clean), three detection gaps (DB_PASSWORD-style names, unquoted .env/YAML values, unparseable JSON config) and FIFO/symlink config reads. All fixed with tests for each; no path prints a value (reviewer traced output, --json, the refusal and the brief log).` → fm secrets audits the tree, history and Claude config as asked, and Foreman's commits are tagged, logged and checked; permission findings count as findings (the header says 'finding(s)', not credentials) [tree 31bf7e876ce5] (2026-10-03T07:49:44Z)
- (audit adversary) `One fm-reviewer pass (intent + adversary) found 8: four commit-check bypasses (diff.noprefix/mnemonicPrefix headers, -diff/binary files, the whole index committed but only task files scanned, a failed git diff read as clean), three detection gaps (DB_PASSWORD-style names, unquoted .env/YAML values, unparseable JSON config) and FIFO/symlink config reads. All fixed with tests for each; no path prints a value (reviewer traced output, --json, the refusal and the brief log).` → the commit check now reads git's diff with prefix/binary/textconv config overridden, commits only the scanned files (git commit -- files), refuses when git can't show them; detection covers prefixed names, bare config values and non-JSON config; no value reaches output [tree 31bf7e876ce5] (2026-10-03T07:49:44Z)
## Log
- 2026-10-03T04:52:05Z created
- 2026-10-03T07:33:39Z planned from capture
- 2026-10-03T07:40:37Z focused
- 2026-10-03T07:40:44Z criteria run through plugin/tests/run.py: unittest from the repo root can't import the tests' helpers
- 2026-10-03T07:43:09Z scope: allowlist markers on the fake credentials in test_core, test_doctor, test_hooks and test_sync (fm secrets now runs clean on this repo)
- 2026-10-03T07:49:44Z done
- 2026-10-03T07:49:44Z committed 410af46 (9 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research rsi-20261003-pass1: 1. **Answer** — Two causes are grounded in code. The first is the 32 evidence nudges: automatic evidence is tagged `(ac N)`, but the Stop ga…
- research t0018-r5-adversary: HIGH — `~/.claude/foreman/plugin/lib/fmguard.py:188-198` (`_protected_roots`) and `:146-147` (`_CRED_DIRS`/`_CRED_FILES`) — tree-w…
- research t0018-r5-maintainer: HIGH — plugin/lib/fmguard.py:188-198 (`_protected_roots`) vs plugin/lib/fmguard.py:165-171 (`_is_core`) — tree-write guard misses project-l…
- research T-0078-review: Verdict: changes needed (one MEDIUM, fail-open, plus a LOW).** `~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0078.diff` is …
## Preflight
Changed in scope since this was planned (2026-10-03): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/rules/foreman.md; re-ground the plan against them before editing
## Lessons
- A scanner that gates a commit must read exactly what the commit will take, through git invocations immune to the user's git config; scanning a pathspec while committing the index, or trusting a/b prefixes, are both silent bypasses.
## Files touched
- plugin/lib/fmsecrets.py
- plugin/lib/fmcli.py
- plugin/tests/test_secrets.py
- CHANGELOG.md
- MASTER.md
- plugin/tests/test_core.py
- plugin/tests/test_doctor.py
- plugin/tests/test_hooks.py
- plugin/tests/test_sync.py
