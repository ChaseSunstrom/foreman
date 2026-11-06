---
id: T-3021
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T21:05:23Z
updated: 2026-11-04T21:10:27Z
base: 881e863554f21fa00e09e35fddfdf98b181d47f6
base_tree: bcbb2655254d98f9246b6558cccdb39e6459238f
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-04T21:05:25Z
plan0_scope: []
verified: strong
unproven: [meaning]
---
# The live page keeps its session across server restarts: a restart (a deploy, the systemd unit) no longer 403s an open tab; the session secret persists 0600 in the project's state and the 403 page names sampo watch --web --url
## Raw request
> The live page keeps its session across server restarts: a restart (a deploy, the systemd unit) no longer 403s an open tab; the session secret persists 0600 in the project's state and the 403 page names sampo watch --web --url
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a second server on the same project accepts the first one's cookie; the 403 body names sampo watch --web --url; the secret file is 0600 — verify with `python3 plugin/tests/run.py test_live`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] persist the session; a 403 that says how to get in
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_live` → exit 0 · Ran 36 tests in 15.1s (9 classes, 16 at a time; slowest: Page 14s, Serve 6s, Snapshot 3s) / OK [ran] [tree 431801393f3d] [world 2f1906870a] (2026-11-04T21:09:01Z)
- `python3 plugin/tests/run.py test_live` → ✗ exit 1 · Ran 36 tests in 16.0s (9 classes, 16 at a time; slowest: Page 14s, Serve 7s, Snapshot 3s) / FAILED (1 classes: test_live.Serve) (start tree + this task's tests) [ran] [tree 431801393f3d] [world 2f1906870a] (2026-11-04T21:09:33Z)
- `python3 plugin/tests/run.py test_live` → exit 0 · Ran 36 tests in 14.8s (9 classes, 16 at a time; slowest: Page 14s, Serve 7s, Snapshot 3s) / OK [ran] [tree 431801393f3d] [world 2f1906870a] (2026-11-04T21:09:33Z)
- (ac 1) `python3 plugin/tests/run.py test_live` → exit 0 · reused: the same command passed on this tree and world at 2026-11-04T21:09:33Z [ran] [tree 431801393f3d] [world 2f1906870a] (2026-11-04T21:09:54Z)
- (audit intent) `self review of a 25-line change: the secret is 32 random bytes in the project's state, 0600 (re-chmodded if loosened), compared in constant time as before; the URL token stays one-time per start` → a restart keeps an open tab signed in (tested: a second server accepts the first one's cookie); the 403 names sampo watch --web --url [tree 431801393f3d] (2026-11-04T21:09:54Z)
- (audit adversary) `self review of a 25-line change: the secret is 32 random bytes in the project's state, 0600 (re-chmodded if loosened), compared in constant time as before; the URL token stays one-time per start` → the secret never leaves the state dir; a world-readable file is tightened on read; another local user still needs the cookie or the token [tree 431801393f3d] (2026-11-04T21:09:54Z)
- (audit edge) `self review of a 25-line change: the secret is 32 random bytes in the project's state, 0600 (re-chmodded if loosened), compared in constant time as before; the URL token stays one-time per start` → a short or missing file mints a new secret; an unreadable file falls back to a fresh one for this start [tree 431801393f3d] (2026-11-04T21:09:54Z)
- (audit self) `self review of a 25-line change: the secret is 32 random bytes in the project's state, 0600 (re-chmodded if loosened), compared in constant time as before; the URL token stays one-time per start` → no findings [tree 431801393f3d] (2026-11-04T21:09:54Z)
## Log
- 2026-11-04T21:05:23Z created
- 2026-11-04T21:05:24Z focused
- 2026-11-04T21:05:25Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-04T21:09:54Z scope: plugin/lib/sampo/live.py and plugin/tests/test_live.py only
- 2026-11-04T21:10:25Z done
- 2026-11-04T21:10:27Z committed e8370360 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3020 [FEATURE S, done, 1 steps] Run the live page always on: a systemd user unit for sampo watch --web on 127.0.0.1:46459, restarted on failure and at login (T-2997 st…
- research live-schema: Server: `sampo live [--port N]`
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- decision 2026-09-26: T-0014 supervisor: systemd user unit only (no tmux-only fallback); the unit runs tmux on a private socket (foreman-<slug>) for the TTY Remote Contro…
- similar finished tasks took 1–9 steps
## Why not caught
no test restarted the server against a signed-in browser; test_live now does
## Lessons
- A server that restarts on deploys must keep its session, or every deploy silently locks the user out; and a restart that changes access owes the user a fresh link
## Files touched
- plugin/lib/sampo/live.py
- plugin/tests/test_live.py
