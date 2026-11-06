---
id: T-1076
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmdoctor.py, plugin/lib/upstream-issues.json, plugin/tests/test_doctor.py]
depends_on: []
source: user
created: 2026-10-16T04:03:35Z
updated: 2026-10-16T05:10:25Z
base: 38a3610010553f59668035608f8b4ae1711f4cf2
base_tree: 0d15b7dc5789d678712cba8f373f0ba6041575d9
verified: strong
---
# Upstream watch: fm doctor matches recurring Claude Code errors to known upstream issues an
## Raw request
> FEATURE: Upstream watch: fm doctor matches recurring Claude Code errors to known upstream issues and says which version fixes them (wild C20)
> CONTEXT: T-1054, the user: "do everything in that brainstorm, and even more for stuff that ISNT done, and even wilder ideas, these seem very simple" + "maybe a way to forever loop a brainstorm/yourself". Wild round: research brainstorm-20261016-wild-clusters (24 clusters). Earlier catalogue: research brainstorm-20261016-catalogue (its skip marks are now build marks too).
## Interpretation
`fm doctor` gets an "upstream" check. It matches errors seen repeatedly (2 or more in 7 days) against a bundled list of known Claude Code issues. When a match is fixed in a newer version, it says so, for example "upgrade to 2.1.X". Nothing like it exists: `check_cc_features` (fmdoctor.py:515) only compares versions for features Foreman uses, and `check_hook_errors` (fmdoctor.py:619) only counts errors.
## Assumptions (confidence)
## Acceptance criteria
- [x] Repeated matching errors give WARN naming the issue and fix version; no match or a single occurrence gives PASS — verify with `python3 plugin/tests/run.py test_doctor`
- [x] The shipped JSON parses and every entry has all five keys — verify with `python3 plugin/tests/run.py test_doctor`
## Non-goals
## Approach (options → choice → why)
(a) fetch the GitHub issues live; (b) a bundled JSON of patterns; (c) both. Choose (b): doctor must work offline, and the data is checkable. Entries in `plugin/lib/upstream-issues.json` are `{id, pattern, issue_url, fixed_in, note}`. - Add `check_upstream(errors=None, version=None, issues=None)` in fmdoctor. - Error sources are `hooks.log` entries via `recent_hook_errors` (fmdoctor.py:601), widened to a `days=7` parameter, plus failure signatures in `failures.jsonl`. - Compare against `fmhooks._cc_version()`. A match whose `fixed_in` is above the installed version gives WARN "matches <issue> (seen N×); fixed in X: claude update". A match already fixed in the installed version gives WARN "should be fixed in X yet recurs". Otherwise PASS. - Register it in `run_all` after `check_cc_features` (fmdoctor.py:1142). - Seed entries must be real. The implementer should confirm each against github.com/anthropics/claude-code issues, and drop any entry that can't be verified.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: call `d.check_upstream` with stub errors, version tuples and issue lists (the same style as test_doctor.py:35). Cases: older version, so WARN with the fix version; newer version, so the "recurs" WARN; single occurrence; empty list. Plus a schema test of the bundled file.
2. [x] Implement the check, the data file and the `run_all` registration.
## Resume here
## Docs impact
CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_doctor` → ✗ exit 1 · Ran 45 tests in 43.4s (17 classes, 16 at a time; slowest: Command 42s, ViewsRepair 29s, Checks 2s) / FAILED (2 classes) [ran] [tree ff1cc998562f] (2026-10-16T04:58:54Z)
- (step 2) `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 45 tests in 36.9s (17 classes, 16 at a time; slowest: Command 37s, ViewsRepair 22s, Checks 1s) / OK [ran] [tree cc0128462763] (2026-10-16T05:00:16Z)
- (step 1) `python3 plugin/tests/run.py test_doctor` → ✗ exit 1 · Ran 46 tests in 30.7s (17 classes, 16 at a time; slowest: Command 31s, ViewsRepair 20s, Checks 1s) / FAILED (2 classes) [ran] [tree feee64158bf8] (2026-10-16T05:06:01Z)
- (step 2) `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 46 tests in 32.5s (17 classes, 16 at a time; slowest: Command 32s, ViewsRepair 23s, Checks 1s) / OK [ran] [tree 78c6ad4dbc49] (2026-10-16T05:07:14Z)
- (ac 1) `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 46 tests in 37.3s (17 classes, 16 at a time; slowest: Command 37s, ViewsRepair 20s, Checks 1s) / OK [ran] [tree c6997e464740] (2026-10-16T05:10:22Z)
- (ac 2) `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 46 tests in 37.3s (17 classes, 16 at a time; slowest: Command 37s, ViewsRepair 20s, Checks 1s) / OK [ran] [tree c6997e464740] (2026-10-16T05:10:22Z)
- (audit intent) `builder lane, then fm-reviewer five-lens pass (research T-1076-review): approve with nits; 2 MEDIUM + 3 LOW fixed by the builder test-first; verification of each seed entry logged; merged --no-ff and criteria re-run here` → a recurring error that matches a known upstream issue names it and the fixing version [tree c6997e464740] (2026-10-16T05:10:22Z)
- (audit adversary) `builder lane, then fm-reviewer five-lens pass (research T-1076-review): approve with nits; 2 MEDIUM + 3 LOW fixed by the builder test-first; verification of each seed entry logged; merged --no-ff and criteria re-run here` → patterns come only from the bundled, schema-tested file; literals behind fixed prefixes (no catastrophic backtracking) [tree c6997e464740] (2026-10-16T05:10:22Z)
- (audit edge) `builder lane, then fm-reviewer five-lens pass (research T-1076-review): approve with nits; 2 MEDIUM + 3 LOW fixed by the builder test-first; verification of each seed entry logged; merged --no-ff and criteria re-run here` → errors before an update don't count; unknown version gets its own message; a bad entry is a WARN, never a crashed doctor; hinted duplicates skipped [tree c6997e464740] (2026-10-16T05:10:22Z)
- (audit operator) `builder lane, then fm-reviewer five-lens pass (research T-1076-review): approve with nits; 2 MEDIUM + 3 LOW fixed by the builder test-first; verification of each seed entry logged; merged --no-ff and criteria re-run here` → PASS on this machine; WARN text says what to run [tree c6997e464740] (2026-10-16T05:10:22Z)
- (audit maintainer) `builder lane, then fm-reviewer five-lens pass (research T-1076-review): approve with nits; 2 MEDIUM + 3 LOW fixed by the builder test-first; verification of each seed entry logged; merged --no-ff and criteria re-run here` → check_upstream and one data file; recent_hook_errors keeps its default for other callers [tree c6997e464740] (2026-10-16T05:10:22Z)
## Log
- 2026-10-16T04:03:35Z created
- 2026-10-16T04:22:41Z set scope=['plugin/lib/fmdoctor.py', 'plugin/lib/upstream-issues.json', 'plugin/tests/test_doctor.py']
- 2026-10-16T04:22:41Z set tier=M
- 2026-10-16T04:55:03Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1076.builder.md
- 2026-10-16T04:55:16Z focused
- 2026-10-16T05:08:38Z seed verification (2026-10-16, builder): each issue fetched from the GitHub issues API, exists, closed, body quotes the error; each fixed_in from a 'Fixed' line citing it in the upstream CHANGELOG: #25990 (zsh heredoc read-only fs) 2.1.47; #21654 (macOS sandbox cwd temp file) 2.1.45; #22087 (classifyHandoffIfNeeded is not defined) 2.1.45; #28334 (bad option: --sdk-url) 2.1.69; #97352 dropped (also matches genuine 403s)
- 2026-10-16T05:09:34Z merged worktree-agent-a707fb51956b840e0 (3 file(s))
- 2026-10-16T05:09:42Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a707fb51956b840e0
- 2026-10-16T05:09:43Z focused
- 2026-10-16T05:09:44Z scope: CHANGELOG.md (its line)
- 2026-10-16T05:10:25Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1065 [SECURITY M, done, 2 steps] Tamper-evident ledger: each ledger line carries the hash of the one before; fm verify-ledg — lesson: A hot-path write that gains a loc…
- T-1057 [FEATURE M, done, 3 steps] Forever loop: fm loop on makes Foreman improve itself without end: when the queue and inbo — lesson: An invariant that ends a loop must…
- T-0785 [FEATURE S, done, 2 steps] fm doctor names the Foreman features the installed Claude Code is too old for — lesson: a probe for a setting must look where Foreman w…
- decision 2026-10-16: T-1054: every wild cluster (23) plus the earlier catalogue's skips became briefs T-1057..T-1087; the forever loop (T-1057) goes first after the demo…
- likely tests for the scope: plugin/tests/test_doctor.py
## Preflight
Changed in scope since this was planned (2026-10-16): plugin/lib/fmdoctor.py, plugin/lib/upstream-issues.json, plugin/tests/test_doctor.py; re-ground the plan against them before editing
## Lessons
- A bundled list of upstream facts needs its provenance logged per entry, or reviewers can't trust it
## Plan gaps
- failed first: step 1 Failing tests: call `d.check_upstream` with stub errors, version tuples and issue lists (the same s…
## Files touched
- plugin/tests/test_doctor.py
- plugin/lib/upstream-issues.json
- plugin/lib/fmdoctor.py
- CHANGELOG.md
