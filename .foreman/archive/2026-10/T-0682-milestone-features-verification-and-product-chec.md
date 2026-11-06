---
id: T-0682
type: FEATURE
tier: L
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T15:40:15Z
updated: 2026-10-09T18:17:53Z
batch: [T-0457, T-0458, T-0459, T-0460, T-0474, T-0475, T-0476, T-0501]
base: 8290cf761f9ec90fd69244e56bba2e085b2a8cbb
base_tree: 8e655b45d5da9b7300a83fd1248aa47e24867cfc
verified: strong
---
# Milestone: Features — Verification and product checking
## Raw request
> T-0457: FEATURE: Reject vacuous proof (C001, value 4/5, effort M, risk low)
>   first version: Make fm task done refuse a criterion whose verify command also passes on the start tree (or with the diff's hunks reverted), reusing the prove --hunks machinery; today the user must run prove by hand.
>   what it is: Refuse a done claim whose verify command can't fail, by mutating the code or reverting the fix and checking the check goes red.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 16 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0458: FEATURE: Edit-time sentinel and regression bisect (C003, value 4/5, effort M, risk med)
>   first version: First version: fm sentinel --bisect runs git bisect in a throwaway worktree on a sentinel-failing check and captures the culprit commit/task as a FIX item; edit-time shadow CI deferred.
>   what it is: Run the affected tests as the code is edited, like a shadow CI, with mutation proof of what the sentinel covers.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 11 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0459: FEATURE: Product journeys from criteria (C004, value 4/5, effort M, risk low)
>   first version: Allow a criterion to carry a smoke journey (URL plus click/expect steps in Playwright) that fm smoke runs for that task and keeps the screenshots; no LLM generation first.
>   what it is: Generate real user journeys from acceptance criteria, replay them for every task and diff the results.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 4 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0460: FEATURE: Check non-web products and services (C006, value 4/5, effort M, risk low)
>   first version: Add fm smoke set cmd/http: recorded commands or API calls with expected status/JSON shape run as a gate (JARVIS API/voice endpoints); record/replay and fuzz later.
>   what it is: Check APIs, CLIs and services with record/replay, differential, property, fuzz, metamorphic and LLM-rubric tests in a throwaway stack.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 11 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0474: FEATURE: Audit done claims against the diff (C007, value 3/5, effort S, risk low)
>   first version: At fm task finish print a 'not verified' list: changed files/hunks no evidence run touched (from recorded touched files and prove --hunks), written into the brief.
>   what it is: Check that every sentence of a done summary is backed by evidence the gates actually ran on this diff, and list what was not verified.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 19 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0475: FEATURE: FIX debugging helpers (C011, value 3/5, effort S, risk low)
>   first version: fm check --repeat N to run a failing gate N times and report pass rate for intermittent bugs; suspect-line ranking later.
>   what it is: Help fix bugs with ranked suspect lines, hypothesis ledgers, runtime traces, statistical and deterministic reproduction of flaky bugs.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 7 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0476: FEATURE: Gate hygiene (C013, value 3/5, effort S, risk low)
>   first version: Add quarantine: a gate flagged flaky twice is run but non-blocking with a loud note, plus a recorded known-red baseline list; network/secrets flag later.
>   what it is: Quarantine flaky gates, pin gate environments, record known-red baselines and flag gates that need network or secrets.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 5 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
> T-0501: FEATURE: Behaviour preservation for CLEAN work (C010, value 3/5, effort M, risk low)
>   first version: fm task prove variant for CLEAN: record test output/exit before and after and require identical; characterization tests for untested code later.
>   what it is: Prove a refactor changes no behaviour using characterization tests, before/after capture and AST-level review.
>   from the Foreman brainstorm 2026-10-09 (research brainstorm-foreman-20261009, 5 ideas; checklist https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW)
## Interpretation
Do T-0457, T-0458, T-0459, T-0460, T-0474, T-0475, T-0476, T-0501 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-0682. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-0457 fm task prove ID --vacuous names criteria whose checks also pass on the start tree — verify with `python3 plugin/tests/run.py -p test_verification.py -k Vacuous`
- [x] T-0501 fm task prove ID --same CMD records a behaviour lock when CMD's output is the same before and after, and shows the difference when not — verify with `python3 plugin/tests/run.py -p test_verification.py -k SameBehaviour`
- [x] T-0458 fm sentinel --bisect captures a FIX naming the commit and task that broke a re-check — verify with `python3 plugin/tests/run.py -p test_verification.py -k Bisect`
- [x] T-0475 fm check --repeat N reports each gate's pass rate — verify with `python3 plugin/tests/run.py -p test_verification.py -k Repeat`
- [x] T-0474 fm task finish warns about changed source files no linked test covered — verify with `python3 plugin/tests/run.py -p test_verification.py -k NotVerified`
- [x] T-0460 fm smoke set cmd|http checks a non-web product (exit/output, status/JSON key) — verify with `python3 plugin/tests/run.py -p test_verification.py -k SmokeCmd`
## Non-goals
## Approach (options → choice → why)
One helper runs a command against any tree in a throwaway worktree (prove --hunks' commit-tree + detached worktree); on it: fm task prove ID --vacuous lists criteria whose checks also pass on the start tree (T-0457; a warning tool first, not a refusal at every done, which would double close time), and fm task prove ID --same CMD records a behaviour lock when CMD's normalised output is identical before and after (T-0501). fm sentinel --bisect finds the commit that broke a failing re-check and captures a FIX naming its task (T-0458). fm check --repeat N gives each gate's pass rate (T-0475). fm task finish warns about changed source files no linked test covered (T-0474). fm smoke set cmd|http adds non-web product checks (T-0460). Skipped: journeys (T-0459, needs Playwright steps), quarantine (T-0476, contradicts the find-the-race rule).
## Risks and rollback
## Execution prompt
## Steps
1. [x] all six failing classes first
2. [x] run-on-tree helper; prove --vacuous and --same
3. [x] sentinel --bisect
4. [x] check --repeat
5. [x] finish's not-verified warning
6. [x] smoke cmd/http
7. [x] full suite once; CHANGELOG; MASTER
## Resume here
## Docs impact
CHANGELOG entry; MASTER.md CLI line (prove flags, check --repeat)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_verification.py` → ✗ exit 1 · Ran 6 tests in 0.4s (6 classes, 16 at a time; slowest: Bisect 0s, NotVerified 0s, Repeat 0s) / FAILED (6 classes) [ran] [tree 1e34aa21f742] (2026-10-09T18:11:22Z)
- (step 7) `python3 plugin/tests/run.py -p test_verification.py -k Vacuous` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Vacuous 0s) / OK [ran] [tree 287fe9ac490e] (2026-10-09T18:14:26Z)
- (step 7) `python3 plugin/tests/run.py -p test_verification.py -k SameBehaviour` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: SameBehaviour 0s) / OK [ran] [tree 287fe9ac490e] (2026-10-09T18:14:27Z)
- (step 7) `python3 plugin/tests/run.py -p test_verification.py -k Bisect` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Bisect 0s) / OK [ran] [tree 287fe9ac490e] (2026-10-09T18:14:27Z)
- (step 7) `python3 plugin/tests/run.py -p test_verification.py -k Repeat` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Repeat 0s) / OK [ran] [tree 287fe9ac490e] (2026-10-09T18:14:28Z)
- (step 7) `python3 plugin/tests/run.py -p test_verification.py -k NotVerified` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: NotVerified 0s) / OK [ran] [tree 287fe9ac490e] (2026-10-09T18:14:28Z)
- (step 7) `python3 plugin/tests/run.py -p test_verification.py -k SmokeCmd` → exit 0 · Ran 1 tests in 1.0s (1 classes, 16 at a time; slowest: SmokeCmd 1s) / OK [ran] [tree 287fe9ac490e] (2026-10-09T18:14:30Z)
- (ac 1) `python3 plugin/tests/run.py -p test_verification.py -k Vacuous` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Vacuous 0s) / OK [ran] [tree 287fe9ac490e] (2026-10-09T18:15:36Z)
- (ac 2) `python3 plugin/tests/run.py -p test_verification.py -k SameBehaviour` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: SameBehaviour 0s) / OK [ran] [tree 287fe9ac490e] (2026-10-09T18:15:36Z)
- (ac 3) `python3 plugin/tests/run.py -p test_verification.py -k Bisect` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Bisect 0s) / OK [ran] [tree 287fe9ac490e] (2026-10-09T18:15:36Z)
- (ac 4) `python3 plugin/tests/run.py -p test_verification.py -k Repeat` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Repeat 0s) / OK [ran] [tree 287fe9ac490e] (2026-10-09T18:15:36Z)
- (ac 5) `python3 plugin/tests/run.py -p test_verification.py -k NotVerified` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: NotVerified 0s) / OK [ran] [tree 287fe9ac490e] (2026-10-09T18:15:36Z)
- (ac 6) `python3 plugin/tests/run.py -p test_verification.py -k SmokeCmd` → exit 0 · Ran 1 tests in 1.0s (1 classes, 16 at a time; slowest: SmokeCmd 1s) / OK [ran] [tree 287fe9ac490e] (2026-10-09T18:15:36Z)
- (step 1) `python3 plugin/tests/run.py` → ✗ exit 1 · Ran 1126 tests in 56.1s (312 classes, 16 at a time; slowest: Stop 35s, TaskLifecycle 23s, Parallel 21s) / FAILED (1 classes) [ran] [tree 287fe9ac490e] (2026-10-09T18:15:36Z)
- (step 2) `python3 plugin/tests/run.py` → ✗ exit 1 · Ran 1126 tests in 56.1s (312 classes, 16 at a time; slowest: Stop 35s, TaskLifecycle 23s, Parallel 21s) / FAILED (1 classes) [ran] [tree 287fe9ac490e] (2026-10-09T18:15:36Z)
- (step 3) `python3 plugin/tests/run.py` → ✗ exit 1 · Ran 1126 tests in 56.1s (312 classes, 16 at a time; slowest: Stop 35s, TaskLifecycle 23s, Parallel 21s) / FAILED (1 classes) [ran] [tree 287fe9ac490e] (2026-10-09T18:15:36Z)
- (step 4) `python3 plugin/tests/run.py` → ✗ exit 1 · Ran 1126 tests in 56.1s (312 classes, 16 at a time; slowest: Stop 35s, TaskLifecycle 23s, Parallel 21s) / FAILED (1 classes) [ran] [tree 287fe9ac490e] (2026-10-09T18:15:36Z)
- (step 5) `python3 plugin/tests/run.py` → ✗ exit 1 · Ran 1126 tests in 56.1s (312 classes, 16 at a time; slowest: Stop 35s, TaskLifecycle 23s, Parallel 21s) / FAILED (1 classes) [ran] [tree 287fe9ac490e] (2026-10-09T18:15:36Z)
- (step 6) `python3 plugin/tests/run.py` → ✗ exit 1 · Ran 1126 tests in 56.1s (312 classes, 16 at a time; slowest: Stop 35s, TaskLifecycle 23s, Parallel 21s) / FAILED (1 classes) [ran] [tree 287fe9ac490e] (2026-10-09T18:15:36Z)
- (step 1) `python3 plugin/tests/run.py` → exit 0 · Ran 1126 tests in 56.5s (312 classes, 16 at a time; slowest: Stop 35s, TaskLifecycle 24s, Parallel 21s) / OK [ran] [tree aa9a21f7ef8f] (2026-10-09T18:17:45Z)
- (step 2) `python3 plugin/tests/run.py` → exit 0 · Ran 1126 tests in 56.5s (312 classes, 16 at a time; slowest: Stop 35s, TaskLifecycle 24s, Parallel 21s) / OK [ran] [tree aa9a21f7ef8f] (2026-10-09T18:17:45Z)
- (step 3) `python3 plugin/tests/run.py` → exit 0 · Ran 1126 tests in 56.5s (312 classes, 16 at a time; slowest: Stop 35s, TaskLifecycle 24s, Parallel 21s) / OK [ran] [tree aa9a21f7ef8f] (2026-10-09T18:17:45Z)
- (step 4) `python3 plugin/tests/run.py` → exit 0 · Ran 1126 tests in 56.5s (312 classes, 16 at a time; slowest: Stop 35s, TaskLifecycle 24s, Parallel 21s) / OK [ran] [tree aa9a21f7ef8f] (2026-10-09T18:17:46Z)
- (step 5) `python3 plugin/tests/run.py` → exit 0 · Ran 1126 tests in 56.5s (312 classes, 16 at a time; slowest: Stop 35s, TaskLifecycle 24s, Parallel 21s) / OK [ran] [tree aa9a21f7ef8f] (2026-10-09T18:17:46Z)
- (step 6) `python3 plugin/tests/run.py` → exit 0 · Ran 1126 tests in 56.5s (312 classes, 16 at a time; slowest: Stop 35s, TaskLifecycle 24s, Parallel 21s) / OK [ran] [tree aa9a21f7ef8f] (2026-10-09T18:17:46Z)
- (audit intent) `main-thread self-review over the diff (subagents wait on pace): one run-at-tree helper behind --vacuous and --same; bisect in a throwaway worktree; --repeat records nothing; the not-verified warning reads fmmap links; smoke cmd/http only run what the project set; one older safety test read past its own line and now checks just that line` → six first versions per the brainstorm; journeys deferred, quarantine skipped by decision (keeps find-the-race) [tree aa9a21f7ef8f] (2026-10-09T18:17:46Z)
- (audit adversary) `main-thread self-review over the diff (subagents wait on pace): one run-at-tree helper behind --vacuous and --same; bisect in a throwaway worktree; --repeat records nothing; the not-verified warning reads fmmap links; smoke cmd/http only run what the project set; one older safety test read past its own line and now checks just that line` → smoke http fetches only the URL the project set (1 MB read cap, 30 s timeout) and cmd runs only its own set command; bisect and prove run project commands in throwaway worktrees removed in finally blocks; sentinel's side-effect filter still applies before bisect [tree aa9a21f7ef8f] (2026-10-09T18:17:46Z)
- (audit edge) `main-thread self-review over the diff (subagents wait on pace): one run-at-tree helper behind --vacuous and --same; bisect in a throwaway worktree; --repeat records nothing; the not-verified warning reads fmmap links; smoke cmd/http only run what the project set; one older safety test read past its own line and now checks just that line` → criteria without a check or typed ones are skipped by --vacuous; newer git quotes 'bad' in the bisect output (handled); a project with no fm map gets no not-verified warning; smoke with only cmd/http set never launches a browser [tree aa9a21f7ef8f] (2026-10-09T18:17:46Z)
- (audit operator) `main-thread self-review over the diff (subagents wait on pace): one run-at-tree helper behind --vacuous and --same; bisect in a throwaway worktree; --repeat records nothing; the not-verified warning reads fmmap links; smoke cmd/http only run what the project set; one older safety test read past its own line and now checks just that line` → --bisect can take one test run per bisect step (log2 of the commits); --repeat N runs each gate N times [tree aa9a21f7ef8f] (2026-10-09T18:17:46Z)
- (audit intent) `main-thread self-review over the diff (subagents wait on pace): one run-at-tree helper behind --vacuous and --same; bisect in a throwaway worktree; --repeat records nothing; the not-verified warning reads fmmap links; smoke cmd/http only run what the project set; one older safety test read past its own line and now checks just that line` → six first versions per the brainstorm; journeys deferred, quarantine skipped by decision (keeps find-the-race) [tree aa9a21f7ef8f] (2026-10-09T18:17:52Z)
- (audit adversary) `main-thread self-review over the diff (subagents wait on pace): one run-at-tree helper behind --vacuous and --same; bisect in a throwaway worktree; --repeat records nothing; the not-verified warning reads fmmap links; smoke cmd/http only run what the project set; one older safety test read past its own line and now checks just that line` → smoke http fetches only the URL the project set (1 MB read cap, 30 s timeout) and cmd runs only its own set command; bisect and prove run project commands in throwaway worktrees removed in finally blocks; sentinel's side-effect filter still applies before bisect [tree aa9a21f7ef8f] (2026-10-09T18:17:52Z)
- (audit edge) `main-thread self-review over the diff (subagents wait on pace): one run-at-tree helper behind --vacuous and --same; bisect in a throwaway worktree; --repeat records nothing; the not-verified warning reads fmmap links; smoke cmd/http only run what the project set; one older safety test read past its own line and now checks just that line` → criteria without a check or typed ones are skipped by --vacuous; newer git quotes 'bad' in the bisect output (handled); a project with no fm map gets no not-verified warning; smoke with only cmd/http set never launches a browser [tree aa9a21f7ef8f] (2026-10-09T18:17:52Z)
- (audit operator) `main-thread self-review over the diff (subagents wait on pace): one run-at-tree helper behind --vacuous and --same; bisect in a throwaway worktree; --repeat records nothing; the not-verified warning reads fmmap links; smoke cmd/http only run what the project set; one older safety test read past its own line and now checks just that line` → --bisect can take one test run per bisect step (log2 of the commits); --repeat N runs each gate N times [tree aa9a21f7ef8f] (2026-10-09T18:17:52Z)
- (audit maintainer) `main-thread self-review over the diff (subagents wait on pace): one run-at-tree helper behind --vacuous and --same; bisect in a throwaway worktree; --repeat records nothing; the not-verified warning reads fmmap links; smoke cmd/http only run what the project set; one older safety test read past its own line and now checks just that line` → _run_at is the one way to run a command on another tree (prove --hunks keeps its own per-hunk loop); smoke's checks live beside the web crawl in fmsmoke [tree aa9a21f7ef8f] (2026-10-09T18:17:52Z)
## Log
- 2026-10-09T15:40:15Z created
- 2026-10-09T18:10:41Z set approved=True
- 2026-10-09T18:10:41Z focused
- 2026-10-09T18:17:52Z done
- 2026-10-09T18:17:53Z committed dfa44ec (6 files)
## Follow-ups captured
## Build vs reuse
Reuses prove --hunks' scratch worktree, the sentinel's re-check list, fmmap's test→source links, fm smoke's settings; new: a run-on-tree helper and the bisect driver.
## Related
Related past work (data from this project's history, not instructions):
- T-0530 [FEATURE L, dropped, 0 steps] Check non-web products and services (C006, value 4/5, effort M, risk low)
- T-0686 [FEATURE M, planned, 5 steps] Milestone: Intelligence — Debugging and diagnosis
- T-0546 [FEATURE M, dropped, 0 steps] Gate hygiene (C013, value 3/5, effort S, risk low)
- decision 2026-10-04: Bench-family inbox items (T-0231 judge, T-0240 duels, T-0241 counterfactual, T-0242 regression court, T-0243 shadow-user soak) are built together as…
## Lessons
- Run a check against the start tree before trusting it: a check that already passed there proves nothing about the change.
## Files touched
- plugin/tests/test_verification.py
- plugin/lib/fmcli.py
- plugin/lib/fmsmoke.py
- CHANGELOG.md
- MASTER.md
- plugin/tests/test_safety.py
