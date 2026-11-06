---
id: T-1939
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T08:38:50Z
updated: 2026-10-29T08:53:29Z
base: a4060741de2d3347fa3fdc722e2ac1673600bbb3
base_tree: d6d428c9e8bcce82c52f0130fd28f8cb0b16bf25
plan0_at: 2026-10-29T08:38:57Z
plan0_scope: []
verified: strong
---
# fm ci-watch falls back to GitHub's public API when gh is missing or logged out
## Raw request
> fm ci-watch falls back to GitHub's public API when gh is missing or logged out
## Interpretation
gh is logged out here, so fm ci-watch can't see CI at all; a hand-rolled curl loop was the only route. When gh fails, read the same facts from GitHub's public API (public repos need no token).
## Assumptions (confidence)
## Acceptance criteria
- [x] with gh failing, ci-watch finds the commit's run and briefs failed jobs' annotations as data — verify with `python3 plugin/tests/run.py test_ci_watch`
## Non-goals
## Approach (options → choice → why)
Complete version: run lookup by head_sha, failed jobs' annotations as the brief's evidence, transient API errors keep polling, no repo/private repo keeps gh's error. Approaches: (1) catch gh's UsageError in _latest/_brief and use urllib on api.github.com (chosen: smallest, reuses fmforesight.github_repo); (2) a separate fm ci-watch --public flag (rejected: the user shouldn't need to know gh's state); (3) shell out to curl (rejected: not everywhere, harder to test). No token is sent, so the host is fixed and nothing leaks; annotation text goes through plain/defang/redact.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: gh fails, public API faked, run found and annotations briefed
2. [x] fallback in _latest and _brief via fmforesight.github_repo, fixed host, no token
3. [x] docs: changelog, ship-to-main playbook names fm ci-watch --commit
## Resume here
## Docs impact
CHANGELOG, MASTER, fm help, ship-to-main playbook step 6
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_ci_watch 2>&1 | grep -E "^(FAIL|ERROR|AssertionError|UsageError|Ran|OK|FAILED)|Error:" | head` → ✗ exit 1 · Ran 5 tests in 1.6s (1 classes, 16 at a time; slowest: CiWatch 1s) / FAILED (1 classes) [ran] [tree 47569237c35e] (2026-10-29T08:39:38Z)
- (ac 1) `python3 plugin/tests/run.py test_ci_watch 2>&1 | grep -E "^(FAIL|ERROR|AssertionError|UsageError|Ran|OK|FAILED)|Error:" | head` → exit 0 · Ran 5 tests in 1.6s (1 classes, 16 at a time; slowest: CiWatch 1s) / OK [ran] [tree 82e11bd06b69] (2026-10-29T08:39:55Z)
- (step 1) `python3 plugin/tests/run.py test_ci_watch 2>&1 | grep -E "^(FAIL|ERROR|AssertionError|UsageError|Ran|OK|FAILED)|Error:" | head` → exit 0 · Ran 5 tests in 1.6s (1 classes, 16 at a time; slowest: CiWatch 1s) / OK [ran] [tree 82e11bd06b69] (2026-10-29T08:39:55Z)
- `python3 plugin/tests/run.py test_ci_watch` → ✗ exit 1 · Ran 5 tests in 2.4s (1 classes, 16 at a time; slowest: CiWatch 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree ab46a1958e42] (2026-10-29T08:40:41Z)
- `python3 plugin/tests/run.py test_ci_watch` → exit 0 · Ran 5 tests in 1.6s (1 classes, 16 at a time; slowest: CiWatch 1s) / OK [ran] [tree ab46a1958e42] (2026-10-29T08:40:41Z)
- (step 1) `python3 plugin/tests/run.py test_ci_watch` → exit 0 · Ran 5 tests in 1.6s (1 classes, 16 at a time; slowest: CiWatch 1s) / OK [ran] [tree ab46a1958e42] (2026-10-29T08:40:43Z)
- (step 2) `python3 plugin/tests/run.py test_ci_watch` → exit 0 · Ran 5 tests in 1.6s (1 classes, 16 at a time; slowest: CiWatch 1s) / OK [ran] [tree ab46a1958e42] (2026-10-29T08:40:45Z)
- (step 3) `grep -c 'fm ci-watch --commit' plugin/skills/playbooks/references/release/ship-to-main.md` → exit 0 · 1 [ran] [tree ab46a1958e42] (2026-10-29T08:40:46Z)
- (step 1) `python3 plugin/tests/run.py test_ci_watch` → exit 0 · Ran 5 tests in 1.7s (1 classes, 16 at a time; slowest: CiWatch 1s) / OK [ran] [tree e42cfad1b4c5] (2026-10-29T08:48:41Z)
- (step 2) `python3 plugin/tests/run.py test_ci_watch` → exit 0 · Ran 5 tests in 1.7s (1 classes, 16 at a time; slowest: CiWatch 1s) / OK [ran] [tree e42cfad1b4c5] (2026-10-29T08:48:43Z)
- (step 3) `grep -c 'fm ci-watch --commit' plugin/skills/playbooks/references/release/ship-to-main.md` → exit 0 · 1 [ran] [tree e42cfad1b4c5] (2026-10-29T08:48:43Z)
- (ac 1) `python3 plugin/tests/run.py test_ci_watch` → exit 0 · Ran 5 tests in 1.7s (1 classes, 16 at a time; slowest: CiWatch 1s) / OK [ran] [tree e42cfad1b4c5] (2026-10-29T08:53:02Z)
- (audit intent) `one fm-reviewer pass (research T-1939-review): 1 medium + 2 low fixed test-first` → medium fixed - 401/403/404 now end the watch with gh's error and the code instead of an hour of silent polls; empty annotations say to open the run; help and MASTER no longer say gh only [tree e42cfad1b4c5] (2026-10-29T08:53:02Z)
- (audit adversary) `one fm-reviewer pass (research T-1939-review): 1 medium + 2 low fixed test-first` → ok - fixed host api.github.com, no token sent (asserted), repo from the origin regex, sha 40 hex, run and job ids must be ints, annotation text plain/redact/defang, FOREMAN_NO_NET and sensitive keep gh's error (tested) [tree e42cfad1b4c5] (2026-10-29T08:53:02Z)
- (audit edge) `one fm-reviewer pass (research T-1939-review): 1 medium + 2 low fixed test-first` → public polls spaced at least 75 s for the 60-an-hour limit (tested with fmci's own clock); transient errors keep polling; >30 jobs not paginated, capped at 20 [tree e42cfad1b4c5] (2026-10-29T08:53:02Z)
- (audit maintainer) `one fm-reviewer pass (research T-1939-review): 1 medium + 2 low fixed test-first` → tests cover 404, NO_NET, sensitive, empty annotations, pacing; the time patch is scoped to fmci because test threads share the time module [tree e42cfad1b4c5] (2026-10-29T08:53:02Z)
## Log
- 2026-10-29T08:38:50Z created
- 2026-10-29T08:38:56Z focused
- 2026-10-29T08:53:27Z done
- 2026-10-29T08:53:29Z committed b0ee2923 (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- playbook Loop Design + Review (fm playbooks show evals/loop-design-check)
- T-1227 [FIX S, done, 1 steps] CI: the fm run --sandbox test needs no real bubblewrap
- T-1669 [FEATURE M, done, 4 steps] Fm drill: compound fault days in a temp home, promotion by false-positive rate (from T-155 — lesson: A corrupt meta.json hides its proj…
- decision 2026-10-28: T-1803 step 3: the next-step hint does not name the top routed book
- similar finished tasks took 1–4 steps
- start here (files T-1227 touched): plugin/tests/test_unattended.py, CHANGELOG.md
## Lessons
- A fallback to an unauthenticated API must turn its auth/limit answers into the original error and pace itself under the anonymous limit, or it trades a clear failure for a silent hour
## Files touched
- plugin/tests/test_ci_watch.py
- plugin/lib/fmci.py
- CHANGELOG.md
- plugin/skills/playbooks/references/release/ship-to-main.md
- MASTER.md
- plugin/lib/fmcli.py
