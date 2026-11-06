---
id: T-2555
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmrelease.py, plugin/tests/test_ship.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-11-02T06:23:34Z
updated: 2026-11-02T06:54:49Z
base: d9c20ac20e45beccdbc6b877f2479e755d950058
base_tree: e57180086acc3b14d2b780e119f9f8f4e9f69166
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-02T06:34:23Z
plan0_scope: [plugin/lib/fmrelease.py, plugin/tests/test_ship.py, CHANGELOG.md]
verified: strong
---
# fm ship retries its push when main moved between the last check and the push, through the same re-pick check, up to 3 tries
## Raw request
> fm ship: a push rejected because main moved during the test (cannot lock ref; here fm genesis live's tower publish, files the picks never touch) costs a full rerun; when the move touches none of the shipped files (T-2511's rule), re-pick onto the new main and push again without rerunning the suite (ship141 → ship142)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a push rejected because the remote's main moved in files the picks don't touch is re-picked onto the new main and pushed without rerunning the test; a move in a shipped file still refuses; three rejected pushes stop with the grant kept — verify with `python3 plugin/tests/run.py test_ship`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test in test_ship: a pre-push hook that moves origin's main (an unrelated file) once makes the first push fail; the ship re-picks and lands, the test runs once
2. [x] fmrelease.ship: the fetch → re-pick check → _push_main block loops up to 3 times on a rejected push (cannot lock ref, fetch first, non-fast-forward), re-fetching each time
## Resume here
## Docs impact
CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_ship.Ship.test_main_moving_between_the_last_check_and_the_push_is_re_picked_without_a_retest` → ✗ exit 1 · Ran 1 tests in 1.0s (1 classes, 16 at a time; slowest: Ship 1s) / FAILED (1 classes: test_ship.Ship) [ran] [tree d97f152d556f] [world 2f1906870a] (2026-11-02T06:34:51Z)
- (step 2) `python3 plugin/tests/run.py test_ship` → exit 0 · Ran 32 tests in 26.4s (1 classes, 16 at a time; slowest: Ship 26s) / OK [ran] [tree cff8d14f48f9] [world 2f1906870a] (2026-11-02T06:35:46Z)
- (ac 1) `python3 plugin/tests/run.py test_ship` → exit 0 · Ran 32 tests in 26.5s (1 classes, 16 at a time; slowest: Ship 26s) / OK [ran] [tree 9581b1432c10] [world 2f1906870a] (2026-11-02T06:42:58Z)
- (step 1) `python3 plugin/tests/run.py test_ship.Ship.test_main_moving_between_the_last_check_and_the_push_is_re_picked_without_a_retest` → exit 0 · Ran 1 tests in 1.0s (1 classes, 16 at a time; slowest: Ship 1s) / OK [ran] [tree 9581b1432c10] [world 2f1906870a] (2026-11-02T06:42:58Z)
- (audit edge) `self-review: the fetch, re-pick check and push loop up to 3 times only when the push error says main moved; the shared-file refusal and the cherry-pick conflict refusal stay inside the loop; the grant comes back on each failed push` → a rejection for any other reason raises at once (the grant kept, as before); three moved-main rejections in a row stop with the grant kept; a move that touches a shipped file refuses on the retry like the first check; the test's pre-receive hook moves main once [tree 9581b1432c10] (2026-11-02T06:42:58Z)
- (audit self) `self-review: the fetch, re-pick check and push loop up to 3 times only when the push error says main moved; the shared-file refusal and the cherry-pick conflict refusal stay inside the loop; the grant comes back on each failed push` → no findings [tree 9581b1432c10] (2026-11-02T06:42:58Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a file; a run of a documented command proves it (--yes-run) / Does not prove: that the prose is right: only that each documented co [ran] [tree 9581b1432c10] [world 2f1906870a] (2026-11-02T06:48:38Z)
## Log
- 2026-11-02T06:23:34Z created
- 2026-11-02T06:24:15Z planned from capture
- 2026-11-02T06:34:22Z focused
- 2026-11-02T06:34:23Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-02T06:35:57Z scope: fmrelease.ship's fetch → re-pick check → push is a 3-try loop on a rejected push whose error says main moved (_MOVED); test_ship gains a pre-receive hook that moves main once; CHANGELOG
- 2026-11-02T06:43:38Z done
- 2026-11-02T06:43:41Z committed ec276a78 (3 files)
- 2026-11-02T06:48:38Z guard authorization added: publish
- 2026-11-02T06:54:47Z publish grant used by fm ship
- 2026-11-02T06:54:49Z publish grant given back: fm ship's push failed
- 2026-11-02T06:54:49Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2511 [FIX M, done, 2 steps] fm ship re-picks onto a main that moved only in files the shipped commits never touch — lesson: A ship race with an automated publisher is …
- T-1943 [FEATURE M, done, 2 steps] Fm ship lands finished commits on the remote's main: fetch, scratch worktree at the fetche — lesson: git cherry matches by patch, so co…
- T-2527 [FEATURE M, done, 2 steps] fm ci-watch --last-ship watches the main commit the newest fm ship pushed — lesson: a falsy test on an optional CLI value turns a faile…
- decision 2026-10-30: [cites: user steer 2026-10-29: push to main without asking] Push grant (the user's own words, after gen-0): "feel free to push to main at any time w…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_release.py
## Lessons
- a check-then-act against a shared ref leaves a window; loop the check and the act together on the specific rejection, bounded
## Plan gaps
- failed first: step 1 red test in test_ship: a pre-push hook that moves origin's main (an unrelated file) once makes the …
## Files touched
- plugin/tests/test_ship.py
- plugin/lib/fmrelease.py
- CHANGELOG.md
