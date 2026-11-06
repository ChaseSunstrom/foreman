---
id: T-1273
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-20T14:29:02Z
updated: 2026-10-20T18:37:53Z
base: e058bf9633418a758a46748dcf44ae01c41ab03e
base_tree: 521079caa73c0fbbb708b5f5fba36aff88c18c4d
plan0_at: 2026-10-20T18:18:37Z
plan0_scope: []
verified: strong
---
# One placeholder rule for secrets: the close warning and the commit refusal agree on what a fake value is
## Raw request
> One placeholder filter for secrets: the close warning (fmcli _close_warnings_of) and the commit refusal (fmsecrets.scan_text) disagree on placeholder tokens, so a fake sk- fixture passes one and is refused by the other
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fmsecrets owns one is_placeholder(line or value) that both scan_text (fmsecrets.py:38) and the close warning (fmcli.py:1778) use, so a fixture line is either warned and refused, or neither; a real-looking token still is both — verify with `python3 plugin/tests/run.py test_secrets`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test: a line with a fake sk- token gives the same verdict from the close warning and from scan_text
2. [x] One helper in fmsecrets, used by both; changelog
## Resume here
## Docs impact
CHANGELOG
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_secrets 2>&1 | tail -8` → ✗ exit 1 · Ran 10 tests in 8.2s (4 classes, 16 at a time; slowest: Secrets 7s, Session 1s, KnownFixes 1s) / FAILED (1 classes) [ran] [tree 8ae9fab374f4] (2026-10-20T18:19:05Z)
- (step 2) `python3 plugin/tests/run.py test_secrets` → exit 0 · Ran 10 tests in 8.6s (4 classes, 16 at a time; slowest: Secrets 8s, KnownFixes 1s, Session 1s) / OK [ran] [tree bc7965e73a25] (2026-10-20T18:21:07Z)
- (ac 1) `python3 plugin/tests/run.py test_secrets 2>&1 | grep -E "^(FAIL|OK|AssertionError)"` → ✗ exit 1 · FAILED (failures=1) / FAILED (1 classes) [ran] [tree c6ec4d2d101e] (2026-10-20T18:24:26Z)
- (step 2) `python3 plugin/tests/run.py test_secrets test_safety` → exit 0 · Ran 23 tests in 3.2s (10 classes, 16 at a time; slowest: Secrets 3s, CleanupGate 1s, SecretsGate 1s) / OK [ran] [tree 2cdc88765bee] (2026-10-20T18:24:43Z)
- `python3 plugin/tests/run.py test_secrets test_safety` → ✗ exit 1 · Ran 23 tests in 3.6s (10 classes, 16 at a time; slowest: Secrets 3s, CleanupGate 1s, SecretsGate 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree a79995174c3e] (2026-10-20T18:33:03Z)
- `python3 plugin/tests/run.py test_secrets test_safety` → exit 0 · Ran 23 tests in 3.2s (10 classes, 16 at a time; slowest: Secrets 3s, CleanupGate 1s, SecretsGate 1s) / OK [ran] [tree a79995174c3e] (2026-10-20T18:33:03Z)
- (step 1) `python3 plugin/tests/run.py test_secrets test_safety` → exit 0 · Ran 23 tests in 3.2s (10 classes, 16 at a time; slowest: Secrets 3s, CleanupGate 1s, SecretsGate 1s) / OK [ran] [tree a79995174c3e] (2026-10-20T18:33:14Z)
- (ac 1) `python3 plugin/tests/run.py test_secrets` → exit 0 · Ran 10 tests in 3.1s (4 classes, 16 at a time; slowest: Secrets 3s, Session 0s, KnownFixes 0s) / OK [ran] [tree a79995174c3e] (2026-10-20T18:36:53Z)
- (audit intent) `one fm-reviewer pass over the branch (five lenses): the adversary finding (an unanchored placeholder match let a real token containing 'your' or 'fake' pass) sent back and fixed test-first with a token-only rule; gates green` → one is_placeholder(value, token=) that scan_text, the Claude-config scan and (through scan_text) the close warning all use; both now agree [tree a79995174c3e] (2026-10-20T18:36:53Z)
- (audit adversary) `one fm-reviewer pass over the branch (five lenses): the adversary finding (an unanchored placeholder match let a real token containing 'your' or 'fake' pass) sent back and fixed test-first with a token-only rule; gates green` → for sk-/ghp_/AKIA tokens only a whole placeholder word (example, placeholder, changeme, dummy, redacted, your-/your_/yourkey) or 6+ x's excuses it; a real-shaped sk-ant key with 'your' or 'fake' inside is still refused (test); a key with -example appended is excused, accepted as the documented-example convention [tree a79995174c3e] (2026-10-20T18:36:53Z)
- (audit edge) `one fm-reviewer pass over the branch (five lenses): the adversary finding (an unanchored placeholder match let a real token containing 'your' or 'fake' pass) sent back and fixed test-first with a token-only rule; gates green` → [REDACTED] and sk-ant-EXAMPLE are no longer reported by fm secrets either, consistent with one rule; a second real token on the same line is still found [tree a79995174c3e] (2026-10-20T18:36:53Z)
- (audit operator) `one fm-reviewer pass over the branch (five lenses): the adversary finding (an unanchored placeholder match let a real token containing 'your' or 'fake' pass) sent back and fixed test-first with a token-only rule; gates green` → warning and refusal text unchanged; the old line-wide filter that hid real findings next to an unrelated 'example' host name is gone [tree a79995174c3e] (2026-10-20T18:36:53Z)
- (audit maintainer) `one fm-reviewer pass over the branch (five lenses): the adversary finding (an unanchored placeholder match let a real token containing 'your' or 'fake' pass) sent back and fixed test-first with a token-only rule; gates green` → the regexes live in fmsecrets beside PLACEHOLDER; the fake fixture word changed from 'fake' to 'dummy' to match the stricter rule [tree a79995174c3e] (2026-10-20T18:36:53Z)
- (audit self) `one fm-reviewer pass over the branch (five lenses): the adversary finding (an unanchored placeholder match let a real token containing 'your' or 'fake' pass) sent back and fixed test-first with a token-only rule; gates green` → no findings [tree a79995174c3e] (2026-10-20T18:36:53Z)
## Log
- 2026-10-20T14:29:02Z created
- 2026-10-20T17:26:11Z planned from capture
- 2026-10-20T18:18:27Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1273.builder.md
- 2026-10-20T18:18:36Z focused
- 2026-10-20T18:29:12Z merged worktree-agent-a4b77167a97ad1df1 (3 file(s))
- 2026-10-20T18:29:15Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a4b77167a97ad1df1
- 2026-10-20T18:32:55Z focused
- 2026-10-20T18:37:53Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0956 [FEATURE M, done, 3 steps] Closing: one verdict line for close warnings, a Landed line, and a leftovers scan — lesson: A status line that recomputes what a siblin…
- research T-0132-review: Verdict: changes needed.** I could only read files, so I traced everything by reading the code and ran nothing. [stale: plugin/lib/fmcli.py, plug…
- T-0870 [FEATURE M, done, 2 steps] fm demo: see Foreman work in a minute without model calls (a temp repo with a seeded bug: brief, guard block, red test, fix, evidence, …
- decision 2026-10-04: The recursive brainstorm loop is dry: pass 5 kept 2 small ideas (built as T-0287) and pass 6 (fresh lenses: performance, unspoken needs; 43 titles) …
## Lessons
- A placeholder test for credentials must match whole placeholder words, not substrings: random key bodies contain short words like 'your' often enough (about 1 in 3,000) to leak real keys
## Files touched
- plugin/tests/test_secrets.py
- plugin/lib/fmsecrets.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- plugin/tests/test_bookkeeping.py
