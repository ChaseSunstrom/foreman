---
id: T-2156
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T14:03:51Z
updated: 2026-10-31T08:46:46Z
builder_model: sonnet
base: fea468ec67279f06da534171057455b06711273d
base_tree: 7d9717ff9e895a76152acb7ef300abb06a2fe14e
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-10-31T08:22:03Z
plan0_scope: []
verified: strong
---
# fm ci-watch backs off to GitHub's rate-limit reset and holds one watch per repo
## Raw request
> fm ci-watch sat silent for over an hour on 3 watches (ci14-16) while gh run list answered HTTP 403 'API rate limit exceeded' (unauthenticated, 60/h shared): it printed only 'watching X, up to 120 polls'. It should name the limit and its reset time (gh api rate_limit), back off to the reset, and never run several watches that split one hourly budget
## Interpretation
When GitHub's unauthenticated hourly limit is spent, fm ci-watch should say so with the reset time and wait for it rather than stop or go silent, and only one watch per repo should poll so several watches don't split the 60 calls.
## Assumptions (confidence)
## Acceptance criteria
- [x] A public-API 403 whose X-RateLimit-Remaining is 0 makes the watch say the hourly limit is spent and the reset time (local HH:MM), wait until the reset and poll again, without counting the wait as a poll; a 403 with no rate-limit headers (a private repo) still stops at once — verify with `python3 plugin/tests/run.py test_ci_watch`
- [x] A second fm ci-watch on the same repo waits on a per-repo lock, saying a watch already holds this repo's poll budget, instead of polling alongside it — verify with `python3 plugin/tests/run.py test_ci_watch`
## Non-goals
## Approach (options → choice → why)
Options: 1) on a 403 read the X-RateLimit-Reset header and sleep to it; 2) call /rate_limit (free) before each poll and pace from it; 3) authenticate or switch to gh api. Choice 1: the header already arrives with the failing call, no extra request, and gh is logged out here so 3 isn't available; for parallel watches: a per-repo fcntl lock (one budget, one poller) over a shared poll cache (more state, same effect).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red tests: a rate-limited 403 with a reset header waits then continues; a headerless 403 raises; a held lock makes the second watch wait
2. [x] In _api, read X-RateLimit-Remaining/Reset on 403 and raise a RateLimited carrying the reset; watch catches it, says it, sleeps to the reset; wrap watch in an fcntl lock under the state dir keyed by the repo
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_ci_watch 2>&1 | tail -30` → ✗ exit 1 · Ran 11 tests in 38.0s (1 classes, 16 at a time; slowest: CiWatch 24s) / FAILED (1 classes) [ran] [tree 5511a3ad95b4] (2026-10-31T08:24:49Z)
- (ac 2) `python3 plugin/tests/run.py test_ci_watch 2>&1 | tail -30` → ✗ exit 1 · Ran 11 tests in 38.0s (1 classes, 16 at a time; slowest: CiWatch 24s) / FAILED (1 classes) [ran] [tree 5511a3ad95b4] (2026-10-31T08:24:49Z)
- (ac 1) `python3 plugin/tests/run.py test_ci_watch 2>&1 | tail -15` → exit 0 · Ran 11 tests in 24.4s (1 classes, 16 at a time; slowest: CiWatch 22s) / OK [ran] [tree ba8e70ceb598] (2026-10-31T08:25:30Z)
- (ac 2) `python3 plugin/tests/run.py test_ci_watch 2>&1 | tail -15` → exit 0 · Ran 11 tests in 24.4s (1 classes, 16 at a time; slowest: CiWatch 22s) / OK [ran] [tree ba8e70ceb598] (2026-10-31T08:25:30Z)
- (step 1) `python3 plugin/tests/run.py test_ci_watch 2>&1 | tail -15` → exit 0 · Ran 11 tests in 24.4s (1 classes, 16 at a time; slowest: CiWatch 22s) / OK [ran] [tree ba8e70ceb598] (2026-10-31T08:25:30Z)
- (step 1) `python3 plugin/tests/run.py test_ci_watch` → exit 0 · Ran 11 tests in 28.1s (1 classes, 16 at a time; slowest: CiWatch 25s) / OK [ran] [tree ba8e70ceb598] (2026-10-31T08:26:09Z)
- (step 2) `python3 plugin/tests/run.py test_ci_watch` → exit 0 · Ran 11 tests in 25.6s (1 classes, 16 at a time; slowest: CiWatch 23s) / OK [ran] [tree ba8e70ceb598] (2026-10-31T08:26:37Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_ci_watch && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · 5 fail / Ran 154 tests across 4 files. [129.81s] [ran] [tree ba8e70ceb598] (2026-10-31T08:29:21Z)
- (ac 1) `python3 plugin/tests/run.py test_ci_watch 2>&1 | tail -30` → exit 0 · Ran 14 tests in 9.2s (1 classes, 16 at a time; slowest: CiWatch 8s) / OK [ran] [tree 28e766230917] (2026-10-31T08:37:53Z)
- (ac 2) `python3 plugin/tests/run.py test_ci_watch 2>&1 | tail -30` → exit 0 · Ran 14 tests in 9.2s (1 classes, 16 at a time; slowest: CiWatch 8s) / OK [ran] [tree 28e766230917] (2026-10-31T08:37:53Z)
- (step 2) `python3 plugin/tests/run.py test_ci_watch` → exit 0 · Ran 14 tests in 11.0s (1 classes, 16 at a time; slowest: CiWatch 10s) / OK [ran] [tree 28e766230917] (2026-10-31T08:38:09Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_ci_watch && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [48.06s] [ran] [tree 28e766230917] (2026-10-31T08:39:14Z)
- (step 1) `python3 plugin/tests/run.py test_ci_watch` → exit 0 · Ran 14 tests in 10.2s (1 classes, 16 at a time; slowest: CiWatch 9s) / OK [ran] [tree 0f17f5cef73b] (2026-10-31T08:44:16Z)
- (step 2) `python3 plugin/tests/run.py test_ci_watch` → exit 0 · Ran 14 tests in 11.2s (1 classes, 16 at a time; slowest: CiWatch 10s) / OK [ran] [tree 0f17f5cef73b] (2026-10-31T08:44:29Z)
- (ac 1) `python3 plugin/tests/run.py test_ci_watch` → exit 0 · Ran 14 tests in 13.1s (1 classes, 16 at a time; slowest: CiWatch 12s) / OK [ran] [tree 8f7f82f6f8b3] (2026-10-31T08:45:21Z)
- (ac 2) `python3 plugin/tests/run.py test_ci_watch` → exit 0 · Ran 14 tests in 13.1s (1 classes, 16 at a time; slowest: CiWatch 12s) / OK [ran] [tree 8f7f82f6f8b3] (2026-10-31T08:45:21Z)
- (audit intent) `one fm-reviewer pass (adversary, edge, operator, maintainer) on the branch: 2 MEDIUM (bogus reset crash, endless 2 s loop on a stale reset) and 1 MEDIUM operator (lock taken when gh is authenticated, unbounded) plus LOWs, all fixed test-first by the builder; I read the fixed diff` → a spent hourly limit now says so with its reset time and waits instead of stopping or going silent, and one watch per repo spends the public budget [tree 8f7f82f6f8b3] (2026-10-31T08:45:21Z)
- (audit adversary) `one fm-reviewer pass (adversary, edge, operator, maintainer) on the branch: 2 MEDIUM (bogus reset crash, endless 2 s loop on a stale reset) and 1 MEDIUM operator (lock taken when gh is authenticated, unbounded) plus LOWs, all fixed test-first by the builder; I read the fixed diff` → the public-API request still sends no token to a fixed host; header text never reaches output (only int-derived HH:MM and minutes); a wild reset is a plain 403 [tree 8f7f82f6f8b3] (2026-10-31T08:45:21Z)
- (audit edge) `one fm-reviewer pass (adversary, edge, operator, maintainer) on the branch: 2 MEDIUM (bogus reset crash, endless 2 s loop on a stale reset) and 1 MEDIUM operator (lock taken when gh is authenticated, unbounded) plus LOWs, all fixed test-first by the builder; I read the fixed diff` → a reset far off or non-ASCII stops at once; a stale reset paces at the poll floor and gives up after 3 waits; a killed watch frees its flock [tree 8f7f82f6f8b3] (2026-10-31T08:45:21Z)
- (audit operator) `one fm-reviewer pass (adversary, edge, operator, maintainer) on the branch: 2 MEDIUM (bogus reset crash, endless 2 s loop on a stale reset) and 1 MEDIUM operator (lock taken when gh is authenticated, unbounded) plus LOWs, all fixed test-first by the builder; I read the fixed diff` → gh-authenticated watches never lock, so fm ship --watch isn't queued behind another watch unless both read the public API [tree 8f7f82f6f8b3] (2026-10-31T08:45:21Z)
- (audit maintainer) `one fm-reviewer pass (adversary, edge, operator, maintainer) on the branch: 2 MEDIUM (bogus reset crash, endless 2 s loop on a stale reset) and 1 MEDIUM operator (lock taken when gh is authenticated, unbounded) plus LOWs, all fixed test-first by the builder; I read the fixed diff` → _poll split from watch so the lock wraps it in one place; tests stub urllib and time [tree 8f7f82f6f8b3] (2026-10-31T08:45:21Z)
## Log
- 2026-10-30T14:03:51Z created
- 2026-10-31T08:21:01Z planned from capture
- 2026-10-31T08:21:30Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2156.builder.md
- 2026-10-31T08:22:00Z focused
- 2026-10-31T08:22:03Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-10-31T08:43:59Z merged worktree-agent-a99042f34998263e8 (2 file(s))
- 2026-10-31T08:44:00Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a99042f34998263e8
- 2026-10-31T08:44:01Z focused
- 2026-10-31T08:44:57Z scope: plugin/lib/fmci.py, plugin/tests/test_ci_watch.py, MASTER.md, CHANGELOG.md
- 2026-10-31T08:46:41Z done
- 2026-10-31T08:46:46Z committed fc6a417a (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1939-review: Verdict: changes needed.** The fallback does what the acceptance criterion says, but it hides gh's error on a private repo or a rate-limited IP. …
- T-1939 [FEATURE M, done, 3 steps] fm ci-watch falls back to GitHub's public API when gh is missing or logged out — lesson: A fallback to an unauthenticated API must turn…
- T-1940 [FEATURE S, done, 1 steps] Fm ci-watch has no message when the watch ends because polling saw no run at all. It could — lesson: none: a one-line follow-up to T-19…
- decision 2026-10-30: [cites: the user's steer 2026-10-30: standing rules for the rest of the genesis run] Long-horizon tier is the deciding end-of-run score for every ca…
## Lessons
- A rate-limit header is untrusted input: bound it (ASCII digits, a max wait) before sleeping on it, and cap repeated waits
## Files touched
- plugin/tests/test_ci_watch.py
- plugin/lib/fmci.py
- MASTER.md
- CHANGELOG.md
