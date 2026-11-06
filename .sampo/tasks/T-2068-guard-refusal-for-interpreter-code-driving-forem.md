---
id: T-2068
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: self
created: 2026-10-30T00:29:09Z
updated: 2026-11-02T18:50:33Z
base: ea67498a17b6a0304644a7183a39fde61ca667f7
base_tree: 77820b6696dc7f49f2853222198d84d99ba082e9
predict_minutes: 12
predict_attempts: 1
plan0_at: 2026-11-02T18:43:20Z
plan0_scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py, CHANGELOG.md, MASTER.md]
verified: strong
---
# The interpreter-code guard refusal names the clause that fired: Foreman's module named in shell text, python settings, code that doesn't parse, dynamic code or a non-plain import, an unknown run folder or a shadowing file, or an fm import
## Raw request
> Guard refusal for interpreter code driving Foreman names no clause that fired (7x on a python heredoc editing a test file): put the matched clause in the refusal detail (fmguard.py ~2184) so the next pass can tell an import from text in a string
## Interpretation
Reading 1 (chosen): the refusal says which of _drives_fm's six clauses fired, so the next attempt fixes that one thing (42 refusals in the week to 11-01, each a rewrite by guesswork). Reading 2 (ruled out here): relax the rule itself; that is T-2261, which needs adversarial cases first, and clause names on future refusals are the data it needs.
## Assumptions (confidence)
## Acceptance criteria
- [x] each of the six clauses of _drives_fm shows in the refusal's detail, and the rule id and hint stay the same — verify with `python3 plugin/tests/run.py test_guard.InterpreterWrites`
- [x] the guard suites still pass — verify with `python3 plugin/tests/run.py test_guard test_guard_diff test_guard_cases test_guard_evasions test_guard_exec_vectors test_guard_hardening`
## Non-goals
## Approach (options → choice → why)
1) _drives_fm returns a short reason string ('' when clean), the one caller puts it after the rule's fixed words. Likely outcome: the six return points become six named clauses, truthiness unchanged, the rule id (first words) and hint (startswith) unchanged. 2) Log the clause in the guard_block event only. Fails if: Claude reads the refusal, not the ledger, so the rewrite stays a guess. 3) A separate rule id per clause. Fails if: fm risk, friction and standing grants key on the one rule id; six ids split them. 4) Do less: name the clause only for the commonest case (cd ;). Likely outcome: the other five stay guesses. 5) Use what exists: the refusal already appends conditional hints for the cd-; and cat-heredoc shapes (fmguard._interpreter_writes); the clause is one more piece of that same detail string. Likely outcome: no new mechanism, and _hint keeps keying on the unchanged prefix. Choice: 1 built as 5 (85%).
## Risks and rollback
Truthiness must not change: an empty reason is falsy, any clause a non-empty string, so no command passes that failed before (the guard suites pin it). The reason names only the clause and at most a module name, never command text. Rollback: git revert.
Blast radius (fm graph blast): co-changes plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmhooks.py, plugin/lib/fmcore.py; past FIXes T-1056, T-1106, T-1117, T-1122, T-1124.
## Execution prompt
## Steps
1. [x] red test: one command per clause, its words in the refusal
2. [x] _drives_fm returns the reason (falsy empty string), the refusal carries it
3. [x] docs: CHANGELOG, MASTER
## Resume here
## Docs impact
CHANGELOG (Unreleased: the refusal names its clause); MASTER.md: a bullet of its own under Recall, lessons and self-improvement (map count 23).
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_guard.InterpreterWrites.test_the_refusal_names_the_clause_that_fired` → ✗ exit 1 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: InterpreterWrites 0s) / FAILED (1 classes: test_guard.InterpreterWrites) [ran] [tree 907ed065b37e] [world 2f1906870a] (2026-11-02T18:43:41Z)
- (step 2) `python3 plugin/tests/run.py test_guard test_guard_diff test_guard_cases test_guard_evasions test_guard_exec_vectors test_guard_hardening test_guard_pipes test_guard_mine test_hooks` → ✗ exit 1 · Ran 559 tests in 46.7s (121 classes, 16 at a time; slowest: Stop 46s, NoTaskGate 28s, PreToolUse 25s) / FAILED (5 classes: test_guard_hardening.Mutation, test_guard.ProtectedTouch, test_guard.PipeShel [ran] [tree ca58c6b8202a] [world 2f1906870a] (2026-11-02T18:45:21Z)
- (step 2) `python3 plugin/tests/run.py test_guard test_guard_diff test_guard_cases test_guard_evasions test_guard_exec_vectors test_guard_hardening test_guard_pipes test_guard_mine test_hooks` → exit 0 · Ran 559 tests in 46.6s (121 classes, 16 at a time; slowest: Stop 46s, NoTaskGate 28s, PreToolUse 25s) / OK [ran] [tree fd6f27b76039] [world 2f1906870a] (2026-11-02T18:46:38Z)
- (step 3) `python3 plugin/tests/run.py test_docs test_docsdrift test_redefinitions` → exit 0 · Ran 105 tests in 8.3s (25 classes, 16 at a time; slowest: Fences 8s, DocsProof 2s, TaskLifecycle 1s) / OK [ran] [tree 85fe00f4d01d] [world 2f1906870a] (2026-11-02T18:47:14Z)
- (step 3) `python3 plugin/tests/run.py test_docs test_docsdrift test_redefinitions test_guard.InterpreterWrites` → exit 0 · Ran 121 tests in 8.2s (26 classes, 16 at a time; slowest: Fences 8s, DocsProof 2s, TaskLifecycle 1s) / OK [ran] [tree 7b7e0c4e1373] [world 2f1906870a] (2026-11-02T18:49:37Z)
- (ac 1) `python3 plugin/tests/run.py test_guard.InterpreterWrites` → exit 0 · Ran 16 tests in 0.6s (1 classes, 16 at a time; slowest: InterpreterWrites 0s) / OK [ran] [tree 7b7e0c4e1373] [world 2f1906870a] (2026-11-02T18:49:57Z)
- (ac 2) `python3 plugin/tests/run.py test_guard test_guard_diff test_guard_cases test_guard_evasions test_guard_exec_vectors test_guard_hardening` → exit 0 · Ran 311 tests in 8.6s (90 classes, 16 at a time; slowest: Mutation 8s, GuardAgainstBash 5s, Trust 4s) / OK [ran] [tree 7b7e0c4e1373] [world 2f1906870a] (2026-11-02T18:49:57Z)
- (step 1) `python3 plugin/tests/run.py test_guard.InterpreterWrites.test_the_refusal_names_the_clause_that_fired` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: InterpreterWrites 0s) / OK [ran] [tree 7b7e0c4e1373] [world 2f1906870a] (2026-11-02T18:49:57Z)
- (audit intent) `one foreman:fm-reviewer pass weighted to adversary (research T-2068-review): approve; every former True is a non-empty string and every False empty, the sole caller tests truthiness, only a capped identifier from the command reaches the refusal, rule id and hint unchanged; nits taken: MASTER sentence split into its own bullet, a long line wrapped; nit rejected: the {{}} in the test is right (self.bash formats the command); the 6 guard tests broken mid-task by a shadowed _name helper were caught by the suites and fixed by renaming to _ident` → each of the six clauses names itself in the refusal, so the next rewrite fixes the clause that fired [tree 7b7e0c4e1373] (2026-11-02T18:49:57Z)
- (audit adversary) `one foreman:fm-reviewer pass weighted to adversary (research T-2068-review): approve; every former True is a non-empty string and every False empty, the sole caller tests truthiness, only a capped identifier from the command reaches the refusal, rule id and hint unchanged; nits taken: MASTER sentence split into its own bullet, a long line wrapped; nit rejected: the {{}} in the test is right (self.bash formats the command); the 6 guard tests broken mid-task by a shadowed _name helper were caught by the suites and fixed by renaming to _ident` → no command refused before passes now (truthiness kept at every return; reviewer confirmed); the refusal quotes at most a [\w.]{1,40} identifier [tree 7b7e0c4e1373] (2026-11-02T18:49:57Z)
- (audit edge) `one foreman:fm-reviewer pass weighted to adversary (research T-2068-review): approve; every former True is a non-empty string and every False empty, the sole caller tests truthiness, only a capped identifier from the command reaches the refusal, rule id and hint unchanged; nits taken: MASTER sentence split into its own bullet, a long line wrapped; nit rejected: the {{}} in the test is right (self.bash formats the command); the 6 guard tests broken mid-task by a shadowed _name helper were caught by the suites and fixed by renaming to _ident` → non-parsing code, relative imports and an unknown run folder take non-crashing paths; _ident falls back to '?' [tree 7b7e0c4e1373] (2026-11-02T18:49:57Z)
- (audit maintainer) `one foreman:fm-reviewer pass weighted to adversary (research T-2068-review): approve; every former True is a non-empty string and every False empty, the sole caller tests truthiness, only a capped identifier from the command reaches the refusal, rule id and hint unchanged; nits taken: MASTER sentence split into its own bullet, a long line wrapped; nit rejected: the {{}} in the test is right (self.bash formats the command); the 6 guard tests broken mid-task by a shadowed _name helper were caught by the suites and fixed by renaming to _ident` → the helper first named _name shadowed fmguard's argv _name (6 guard tests failed); renamed _ident; T-2630 captured for an edit-time redefinition note [tree 7b7e0c4e1373] (2026-11-02T18:49:57Z)
## Log
- 2026-10-30T00:29:09Z created
- 2026-10-31T00:13:33Z self-improvement pass 2026-10-31 (rsi-20261031-001203): recon ranked naming _drives_fm's firing clause top (7x core:interpreter-code-driving-foreman). Left alone per the standing rule that T-2068 touches the guard; it waits for the user.
- 2026-10-31T00:54:44Z blocked: touches the guard (fmguard._drives_fm): a standing rule leaves it to the user, and guard changes need the user's grant; it goes in the final report with the friction evidence (7x core:interpreter-code-driving-foreman, rsi-20261031-001203)
- 2026-11-02T18:12:50Z unblocked
- 2026-11-02T18:12:50Z unblocked: trust mode is on (Claude may edit the guard), the only blocker; still ~8 blocks/day (ledger 2026-10-28..11-01: 42)
- 2026-11-02T18:26:38Z planned from capture
- 2026-11-02T18:43:19Z focused
- 2026-11-02T18:43:20Z predicted from its closes: 12 min, 1 attempt(s)
- 2026-11-02T18:50:30Z done
- 2026-11-02T18:50:33Z committed f73d4efb (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1194 [FIX M, done, 2 steps] Guard parses python -c code like quoted heredoc bodies before calling it Foreman-driving — lesson: Loosening a guard rule needs the mined r…
- T-1171 [FIX M, done, 2 steps] Guard: _drives_fm (fmguard.py:1364) treats any heredoc that doesn't parse, and fm-import t — lesson: mine full commands before relaxing a g…
- research T-1932-review: Changes needed. The core change is correct, but the third-refusal advice still points to a grant that can't help, and one unread-program refusal …
- decision 2026-10-31: User's blanket approval (13:2xZ) applied: T-2246 (cold-read FAILs block only when they quote the clause they break), T-2247 (steer provenance) and T…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_guard.py
## Preflight
Changed in scope since this was planned (2026-10-30): CHANGELOG.md, MASTER.md, plugin/lib/fmguard.py, plugin/tests/test_guard.py; re-ground the plan against them before editing
## Lessons
- Before adding a top-level helper to a big module, grep its name: a second def silently replaces the first, and only the full suites show it (third time: _grounded, _TID, now _name)
## Plan gaps
- failed first: step 1 red test: one command per clause, its words in the refusal
- failed first: step 2 _drives_fm returns the reason (falsy empty string), the refusal carries it
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- CHANGELOG.md
- MASTER.md
