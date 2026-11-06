---
id: T-2199
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T19:14:57Z
updated: 2026-10-31T01:06:10Z
base: 9c73f4c332619688b3c3e68d340ffc4b1b741711
base_tree: d9e65fa0a3157be70b40c03dbd03b9608be16bdb
plan0_at: 2026-10-31T00:32:54Z
plan0_scope: []
verified: strong
---
# fm prove: model-written failing tests prove vuln, bug, slow and flaky candidates (red…
## Raw request
> fm prove: model-written failing tests prove vuln, bug, slow and flaky candidates (red 3/3 for an assertion on a throwaway copy, failure changes when the candidate is stubbed; a test failing for its own reason stays a lead); T-2122 shipped the deterministic proofs (untested by stub-and-suite with a control, docs/dep/secret re-found cold)
## Interpretation
fm find emits vuln (SQL from a parameter), slow (quadratic membership/scan) and flaky (unseeded randomness in a test) candidates that fm prove leaves as leads (fmprove.prove: 'needs a failing test'). Prove them on the throwaway copy, only in a tree the user said yes to (fmprove.trusted), so the find → prove → fix loop covers every kind #1 names. No 'bug' finder exists; a bug kind is out of scope until one does.
## Assumptions (confidence)
## Acceptance criteria
- [x] flaky: fm prove reruns the flagged test K times on the throwaway copy of a trusted tree and proves it only when it both passes and fails — verify with `cd plugin/tests && python3 -m unittest -q test_find.FindProveKinds.test_flaky_is_proven_only_when_reruns_both_pass_and_fail`
- [x] vuln, slow and bug candidates: a tool-less child writes one failing test; proven only when it's red 3 of 3 on an assertion and the failure changes when the candidate's body is stubbed to raise a sentinel, else a lead; the test runs with credential env vars stripped, only in a trusted tree or exam sandbox — verify with `cd plugin/tests && python3 -m unittest -q test_find.FindProveKinds`
## Non-goals
## Approach (options → choice → why)
Options: (a) flaky deterministically: rerun the flagged test K times on the copy; proven when it both passes and fails (no model); (b) per-kind deterministic probes (call the SQL builder with a quote; time n vs 8n inputs), language-specific harnesses; (c) a tool-less child writes one failing test per candidate from its source; proven when red 3/3 on an assertion and the failure changes when the candidate's body is stubbed to raise a sentinel (the test exercises it), else a lead; (d) leave them leads and rank lower. Choice: (a) for flaky plus (c) for vuln and slow: every language, one shape, the stub control keeps a test failing for its own reason a lead; model-written test code runs with fmbench.CREDENTIALS stripped, like exam code.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests (class FindProveKinds) with a stub claude for the child and planted flaky, vuln and slow repos
2. [x] flaky by reruns
3. [x] child-written failing test with the stub control for vuln, slow and bug
4. [x] docs (MASTER, CHANGELOG), adversary + edge review
## Resume here
## Docs impact
MASTER.md fmprove entry, CHANGELOG Unreleased
## Verification evidence
- (ac 2) `cd plugin/tests && python3 -m unittest -q test_find.FindProveKinds 2>&1 | tail -25` → ✗ exit 1 · Ran 4 tests in 2.540s / FAILED (failures=2) [ran] [tree 1e039d7275f3] (2026-10-31T00:35:06Z)
- (ac 2) `cd plugin/tests && python3 -m unittest -q test_find.FindProveKinds 2>&1 | tail -25` → exit 0 · Ran 4 tests in 2.427s / OK [ran] [tree 544216909d7c] (2026-10-31T00:35:19Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_find.FindProveKinds 2>&1 | tail -25` → exit 0 · Ran 4 tests in 2.427s / OK [ran] [tree 544216909d7c] (2026-10-31T00:35:19Z)
- (step 2) `cd plugin/tests && python3 -m unittest -q test_find test_scout 2>&1 | tail -4` → exit 0 · Ran 69 tests in 62.678s / OK [ran] [tree 170297c45e89] (2026-10-31T00:38:10Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_find.FindProveKinds` → exit 0 · Ran 4 tests in 2.536s / OK [ran] [tree 170297c45e89] (2026-10-31T00:38:17Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_find && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [21.57s] [ran] [tree 170297c45e89] (2026-10-31T00:38:51Z)
- (step 2) `cd plugin/tests && python3 -m unittest -q test_find.FindProveKinds.test_flaky_is_proven_only_when_reruns_both_pass_and_fail` → exit 0 · Ran 1 test in 1.478s / OK [ran] [tree 170297c45e89] (2026-10-31T00:38:56Z)
- (ac 2) `cd plugin/tests && python3 -m unittest -q test_find.FindProveKinds 2>&1 | grep -E "^(FAIL|ERROR|Ran|OK)"` → ✗ exit 1 · Ran 8 tests in 2.935s / FAILED (failures=3) [ran] [tree daf2126362e4] (2026-10-31T00:43:25Z)
- (step 3) `cd plugin/tests && python3 -m unittest -q test_find.FindProveKinds` → exit 0 · Ran 8 tests in 3.489s / OK [ran] [tree 6d889b9ebba6] (2026-10-31T00:44:57Z)
- `cd plugin/tests && python3 -m unittest -q test_find.FindProveKinds` → ✗ exit 1 · Ran 8 tests in 0.693s / FAILED (failures=7, errors=1) (start tree + this task's tests) [ran] [tree 54b2ff2dd7eb] (2026-10-31T01:04:39Z)
- `cd plugin/tests && python3 -m unittest -q test_find.FindProveKinds` → exit 0 · Ran 8 tests in 2.106s / OK [ran] [tree 54b2ff2dd7eb] (2026-10-31T01:04:39Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_find.FindProveKinds.test_flaky_is_proven_only_when_reruns_both_pass_and_fail` → exit 0 · Ran 1 test in 0.921s / OK [ran] [tree 54b2ff2dd7eb] (2026-10-31T01:05:34Z)
- (ac 2) `cd plugin/tests && python3 -m unittest -q test_find.FindProveKinds` → exit 0 · Ran 8 tests in 2.384s / OK [ran] [tree 54b2ff2dd7eb] (2026-10-31T01:05:36Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_find.FindProveKinds` → exit 0 · Ran 8 tests in 2.157s / OK [ran] [tree 54b2ff2dd7eb] (2026-10-31T01:05:39Z)
- (step 2) `cd plugin/tests && python3 -m unittest -q test_find.FindProveKinds` → exit 0 · Ran 8 tests in 2.235s / OK [ran] [tree 54b2ff2dd7eb] (2026-10-31T01:05:41Z)
- (step 3) `cd plugin/tests && python3 -m unittest -q test_find.FindProveKinds` → exit 0 · Ran 8 tests in 2.167s / OK [ran] [tree 54b2ff2dd7eb] (2026-10-31T01:05:43Z)
- (step 4) `grep -q 'T-2199' MASTER.md && grep -q 'proves more kinds' CHANGELOG.md` → exit 0 · (no output) [ran] [tree d19f6c4d4cfd] (2026-10-31T01:05:44Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_find.FindProveKinds.test_flaky_is_proven_only_when_reruns_both_pass_and_fail` → exit 0 · Ran 1 test in 0.618s / OK [ran] [tree d19f6c4d4cfd] (2026-10-31T01:05:48Z)
- (ac 2) `cd plugin/tests && python3 -m unittest -q test_find.FindProveKinds` → exit 0 · Ran 8 tests in 2.157s / OK [ran] [tree d19f6c4d4cfd] (2026-10-31T01:05:48Z)
- (audit intent) `fm-reviewer adversary+edge+intent on the builder's branch: gates, env stripping, path and shell injection, and the cap all held; 1 HIGH (a stub's syntax error echoing the sentinel read as proof), 2 MEDIUM (an unconditional FM_RED proven; flaky matched a passing test's name) and 4 LOW fixed test-first in 794c2a3b, plus the sensitive-project refusal; test_find + test_scout 73 green` → flaky by reruns, vuln/slow/bug by a model-written failing test with two stub controls, each lead explained [tree d19f6c4d4cfd] (2026-10-31T01:05:48Z)
- (audit adversary) `fm-reviewer adversary+edge+intent on the builder's branch: gates, env stripping, path and shell injection, and the cap all held; 1 HIGH (a stub's syntax error echoing the sentinel read as proof), 2 MEDIUM (an unconditional FM_RED proven; flaky matched a passing test's name) and 4 LOW fixed test-first in 794c2a3b, plus the sensitive-project refusal; test_find + test_scout 73 green` → the sentinel is built at runtime, a stubbed file must parse, a benign-return stub must change the red, the child writes only into the copy with credentials stripped, and only in a trusted tree; a sensitive project gets no child test [tree d19f6c4d4cfd] (2026-10-31T01:05:48Z)
- (audit edge) `fm-reviewer adversary+edge+intent on the builder's branch: gates, env stripping, path and shell injection, and the cap all held; 1 HIGH (a stub's syntax error echoing the sentinel read as proof), 2 MEDIUM (an unconditional FM_RED proven; flaky matched a passing test's name) and 4 LOW fixed test-first in 794c2a3b, plus the sensitive-project refusal; test_find + test_scout 73 green` → per-run timeouts against the deadline, a fresh copy per rerun, a missing folder is a lead, ts/rs/c say no test can run [tree d19f6c4d4cfd] (2026-10-31T01:05:48Z)
## Log
- 2026-10-30T19:14:57Z created
- 2026-10-31T00:32:00Z planned: it has criteria and steps
- 2026-10-31T00:32:00Z set approved=True
- 2026-10-31T00:32:38Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2199.builder.md
- 2026-10-31T00:32:54Z focused
- 2026-10-31T01:04:34Z merged worktree-agent-acd43fb2c16f79ddd (2 file(s))
- 2026-10-31T01:04:35Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-acd43fb2c16f79ddd
- 2026-10-31T01:04:35Z focused
- 2026-10-31T01:06:08Z done
- 2026-10-31T01:06:10Z committed db375799 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2121 [FEATURE L, done, 2 steps] fm find: deterministic language-agnostic finders (untested, docs, deps, sql, slow, flaky, secrets, gates), zero on every clean render (…
- T-2124 [FEATURE M, done, 2 steps] Scout project probes: fm find + prove on the user's own project, at most 3 a day, proven only, refutation ledger, doctor faults to the …
- T-2122 [FEATURE L, done, 2 steps] fm find prove: proof tickets, red 3/3 for an assertion and mutate-to-confirm; unproven candidates become leads (Mission 3 brief 3) — le…
- decision 2026-10-30: Proven kinds (dep, docs, secret) file without a cold re-run; scout never refiles a regression
- similar finished tasks took 2–2 steps
## Lessons
- A proof that a model-written test exercises the code needs two controls (raise and benign return) and a sentinel that can't appear in the source; one control proves only that the function is called
## Files touched
- plugin/tests/test_find.py
- plugin/lib/fmprove.py
- CHANGELOG.md
