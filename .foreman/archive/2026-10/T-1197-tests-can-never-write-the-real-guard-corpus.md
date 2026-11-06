---
id: T-1197
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-16T13:38:34Z
updated: 2026-10-16T13:42:41Z
base: f017dfa05d8c226d5332c565200acbe6877ff195
base_tree: fd472f89aa4dac894d4ddf37f142ee831d43b1ac
plan0_at: 2026-10-16T13:38:35Z
plan0_scope: []
verified: strong
---
# Tests can never write the real guard corpus
## Raw request
> Tests can never write the real guard corpus
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm and hook calls in tests default FOREMAN_GUARD_CASES to a temp file; the real corpus stays at its 6 committed cases after the subdir matrix runs — verify with `python3 plugin/tests/run.py test_subdir_matrix test_guard_cases test_guard_wrong`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Restore the corpus and default FOREMAN_GUARD_CASES in helpers.fm/hook
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py -k test_a_test_without_the_env_never_writes_the_real_corpus` → exit 0 · Ran 1 tests in 1.2s (1 classes, 16 at a time; slowest: GuardCases 0s) / OK (start tree + this task's tests) [ran] [tree dd7cb6bb7cea] (2026-10-16T13:39:32Z)
- `python3 plugin/tests/run.py -k test_a_test_without_the_env_never_writes_the_real_corpus` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: GuardCases 0s) / OK [ran] [tree dd7cb6bb7cea] (2026-10-16T13:39:32Z)
- (step 1) `python3 plugin/tests/run.py test_subdir_matrix test_guard_cases test_guard_mine test_replay` → exit 0 · Ran 33 tests in 8.1s (5 classes, 16 at a time; slowest: SubdirMatrix 8s, Replay 3s, GuardCases 2s) / OK [ran] [tree 7877df8aa81d] (2026-10-16T13:40:11Z)
- (ac 1) `python3 plugin/tests/run.py test_subdir_matrix test_guard_cases test_guard_wrong` → exit 0 · Ran 20 tests in 15.0s (2 classes, 16 at a time; slowest: SubdirMatrix 15s, GuardCases 4s) / OK [ran] [tree 56b3ac22dc77] (2026-10-16T13:41:03Z)
- `python3 plugin/tests/run.py test_subdir_matrix test_guard_cases test_guard_mine test_replay` → exit 0 · Ran 33 tests in 12.6s (5 classes, 16 at a time; slowest: SubdirMatrix 12s, GuardCases 5s, Replay 4s) / OK [ran] [tree 56b3ac22dc77] (2026-10-16T13:41:03Z)
- (audit self) `self: setUp default is restored in tearDown with the other env keys; the one test of the T-1175 fallback opts out with an empty value, which cases_path treats as unset; grep shows no other test relies on the real corpus via fm` → no findings [tree 56b3ac22dc77] (2026-10-16T13:41:03Z)
- `python3 plugin/tests/run.py test_subdir_matrix test_guard_cases test_guard_mine test_replay` → exit 0 · Ran 33 tests in 8.1s (5 classes, 16 at a time; slowest: SubdirMatrix 8s, Replay 3s, GuardCases 2s) / OK [ran] [tree 56b3ac22dc77] (2026-10-16T13:41:58Z)
- (audit adversary) `self: setUp default is restored in tearDown with the other env keys; the one test of the T-1175 fallback opts out with an empty value, which cases_path treats as unset; grep shows no other test relies on the real corpus via fm` → test-only change; the guard and fm guard wrong are untouched; an empty FOREMAN_GUARD_CASES still falls back to the checkout corpus as before, and the new test restores the real file if a regression writes it [tree 56b3ac22dc77] (2026-10-16T13:41:58Z)
- (audit self) `self: setUp default is restored in tearDown with the other env keys; the one test of the T-1175 fallback opts out with an empty value, which cases_path treats as unset; grep shows no other test relies on the real corpus via fm` → no findings [tree 56b3ac22dc77] (2026-10-16T13:41:58Z)
## Log
- 2026-10-16T13:38:34Z created
- 2026-10-16T13:38:35Z focused
- 2026-10-16T13:40:34Z scope: CHANGELOG line
- 2026-10-16T13:42:40Z done
- 2026-10-16T13:42:41Z committed f6062ef0 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1175 [FIX S, done, 2 steps] Fm guard wrong run from a builder's worktree writes into the main checkout's corpus (PLUGI
- T-0433 [SECURITY M, done, 3 steps] Guard fuzzer: mutated real-bash forms never run a dangerous call unblocked — lesson: A guard's own tests find what its authors imagine…
- T-0783 [PERFORMANCE M, done, 3 steps] Big Bash outputs reach the model as head, tail and failure lines, with the full text in a file (opt-in) — lesson: measure a lossy c…
- decision 2026-10-04: [costly] T-0308 closed on self-audit, hunk proofs and the replay corpus
- similar finished tasks took 2–3 steps
## Regression test
test_guard_cases.test_a_test_without_the_env_never_writes_the_real_corpus: red before the helpers.py change (it wrote the real corpus; its finally restored it), green after. fm task prove can't show it because the fix itself is in a test file (helpers.py), so the start tree plus test files already holds it.
## Files touched
- plugin/tests/fixtures/guard_cases.jsonl
- plugin/tests/test_guard_cases.py
- plugin/tests/helpers.py
- CHANGELOG.md
