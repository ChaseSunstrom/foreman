---
id: T-1289
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-20T20:56:58Z
updated: 2026-10-20T21:55:23Z
base: dfa7cbc86d61c816074c9758bcf8f1a293e84dc4
base_tree: 650956b5b855654ff347ef42d8aad7a99def801a
plan0_at: 2026-10-20T21:41:33Z
plan0_scope: []
verified: strong
---
# The guard's refusal of a script written and run in one command says how to go on: write it in one command (cat > f <<'EOF' or the Write tool), run it in the next
## Raw request
> Guard hint for 'is written earlier in this command and run here' (fmguard.py:2634): _hint (fmguard.py:145-168) has no case, so the refusal gives no way forward; add one: write the script in one command (cat > f <<'EOF' or the Write tool), run it in the next
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a command that writes a script and runs it (printf > s.sh && bash s.sh, cat <<EOF > s.sh … sh s.sh, tee s.sh … bash s.sh) is still refused, and the refusal now ends with the way forward; the guard's verdicts are otherwise unchanged — verify with `python3 plugin/tests/run.py test_guard_diff test_guard`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test: the three forms' refusal text carries the hint; verdicts unchanged
2. [x] A _hint case in fmguard.py for 'is written earlier in this command'
## Resume here
## Docs impact
CHANGELOG
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_guard_diff test_guard 2>&1 | tail -15` → ✗ exit 1 · Ran 194 tests in 29.1s (60 classes, 16 at a time; slowest: GuardAgainstBash 26s, GuardCases 10s, Hook 8s) / FAILED (1 classes) [ran] [tree 2dad0a1a7e72] (2026-10-20T21:42:29Z)
- (ac 1) `python3 plugin/tests/run.py test_guard_diff test_guard 2>&1 | tail -12` → ✗ exit 1 · Ran 194 tests in 26.9s (60 classes, 16 at a time; slowest: GuardAgainstBash 25s, GuardCases 12s, Hook 10s) / FAILED (1 classes) [ran] [tree 773bfa3f03e9] (2026-10-20T21:43:10Z)
- (ac 1) `python3 plugin/tests/run.py test_guard_diff test_guard 2>&1 | tail -12` → exit 0 · Ran 194 tests in 36.8s (60 classes, 16 at a time; slowest: GuardAgainstBash 35s, GuardCases 15s, Hook 13s) / OK [ran] [tree 8ebefffcf34c] (2026-10-20T21:44:27Z)
- (step 2) `python3 plugin/tests/run.py test_guard_diff test_guard 2>&1 | tail -12` → exit 0 · Ran 194 tests in 36.8s (60 classes, 16 at a time; slowest: GuardAgainstBash 35s, GuardCases 15s, Hook 13s) / OK [ran] [tree 8ebefffcf34c] (2026-10-20T21:44:27Z)
- (step 1) `python3 plugin/tests/run.py test_guard_diff test_guard` → exit 0 · Ran 194 tests in 38.3s (60 classes, 16 at a time; slowest: GuardAgainstBash 36s, GuardCases 15s, Hook 13s) / OK [ran] [tree 8ebefffcf34c] (2026-10-20T21:45:09Z)
- (step 2) `python3 plugin/tests/run.py test_guard_diff test_guard` → exit 0 · Ran 194 tests in 29.4s (60 classes, 16 at a time; slowest: GuardAgainstBash 28s, GuardCases 14s, Hook 12s) / OK [ran] [tree 8ebefffcf34c] (2026-10-20T21:45:41Z)
- (step 1) `python3 plugin/tests/run.py test_guard_diff test_guard` → exit 0 · Ran 194 tests in 10.2s (60 classes, 16 at a time; slowest: GuardAgainstBash 10s, GuardCases 5s, Hook 4s) / OK [ran] [tree b7222a43a421] (2026-10-20T21:53:24Z)
- (step 2) `python3 plugin/tests/run.py test_guard_diff test_guard` → exit 0 · Ran 194 tests in 10.1s (60 classes, 16 at a time; slowest: GuardAgainstBash 9s, GuardCases 5s, Hook 4s) / OK [ran] [tree b7222a43a421] (2026-10-20T21:53:34Z)
- (ac 1) `python3 plugin/tests/run.py test_guard_diff test_guard` → exit 0 · Ran 194 tests in 9.8s (60 classes, 16 at a time; slowest: GuardAgainstBash 9s, GuardCases 5s, Hook 4s) / OK [ran] [tree b7222a43a421] (2026-10-20T21:53:45Z)
- (ac 1) `python3 plugin/tests/run.py test_guard_diff test_guard` → exit 0 · Ran 194 tests in 10.2s (60 classes, 16 at a time; slowest: GuardAgainstBash 10s, GuardCases 5s, Hook 4s) / OK [ran] [tree b7222a43a421] (2026-10-20T21:54:03Z)
- (audit intent) `self review: one _hint case keyed on the refusal's detail text; the test checks category and hint for printf/cp/tee forms; guard verdicts unchanged (194 tests, replay 0 drift)` → the refusal says to write the script in one command and run it in the next [tree b7222a43a421] (2026-10-20T21:54:03Z)
- (audit adversary) `self review: one _hint case keyed on the refusal's detail text; the test checks category and hint for printf/cp/tee forms; guard verdicts unchanged (194 tests, replay 0 drift)` → a fixed string; no verdict changes [tree b7222a43a421] (2026-10-20T21:54:03Z)
- (audit edge) `self review: one _hint case keyed on the refusal's detail text; the test checks category and hint for printf/cp/tee forms; guard verdicts unchanged (194 tests, replay 0 drift)` → the heredoc form stays allowed (its body is read), as before [tree b7222a43a421] (2026-10-20T21:54:03Z)
- (audit operator) `self review: one _hint case keyed on the refusal's detail text; the test checks category and hint for printf/cp/tee forms; guard verdicts unchanged (194 tests, replay 0 drift)` → an agent refused this way now knows the next step instead of trying --allow [tree b7222a43a421] (2026-10-20T21:54:03Z)
- (audit maintainer) `self review: one _hint case keyed on the refusal's detail text; the test checks category and hint for printf/cp/tee forms; guard verdicts unchanged (194 tests, replay 0 drift)` → the hint keys on the detail text; the test fails if that text is reworded [tree b7222a43a421] (2026-10-20T21:54:03Z)
- (audit self) `self review: one _hint case keyed on the refusal's detail text; the test checks category and hint for printf/cp/tee forms; guard verdicts unchanged (194 tests, replay 0 drift)` → no findings [tree b7222a43a421] (2026-10-20T21:54:03Z)
## Log
- 2026-10-20T20:56:58Z created
- 2026-10-20T21:41:15Z planned from capture
- 2026-10-20T21:41:22Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1289.builder.md
- 2026-10-20T21:41:32Z focused
- 2026-10-20T21:50:54Z merged worktree-agent-ad2bc23ce0920e19c (2 file(s))
- 2026-10-20T21:50:54Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ad2bc23ce0920e19c
- 2026-10-20T21:53:07Z focused
- 2026-10-20T21:53:52Z steer: the heredoc form (cat <<EOF > s.sh … sh s.sh) named in criterion 1 is allowed by design (the guard reads the heredoc body); the builder kept that verdict, as the criterion's 'verdicts unchanged' requires, and tested cp a.sh s.sh && sh s.sh as the third refused form
- 2026-10-20T21:55:23Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0774 [FIX S, done, 2 steps] Guard: heredoc python started by 'cd DIR && python3 -' resolves its relative open() targets in DIR only — lesson: a guard relaxation that t…
- T-0369 [FIX M, done, 2 steps] Guard: pin the pipe proof's strictness (premise of a self-improvement finding was false) — lesson: Before widening a guard from a friction …
- T-1171 [FIX M, done, 2 steps] Guard: _drives_fm (fmguard.py:1364) treats any heredoc that doesn't parse, and fm-import t — lesson: mine full commands before relaxing a g…
- decision 2026-10-04: Friction pass 2026-10-04: drop recon findings 1-3 (guard)
- similar finished tasks took 2–2 steps
- start here (files T-0774 touched): plugin/tests/test_guard.py, plugin/lib/fmguard.py
## Behaviour lock
only the refusal text changes: test_guard_diff's corpus of command forms keeps every verdict and category (194 guard tests green), and fm replay over the labelled cases shows 0 drift
## Lessons
- Every refusal category needs its own way forward; a generic 'to authorize: --allow' sends agents down a path that can't work
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- CHANGELOG.md
