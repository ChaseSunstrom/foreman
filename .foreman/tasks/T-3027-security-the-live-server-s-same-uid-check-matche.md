---
id: T-3027
type: SECURITY
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T21:44:23Z
updated: 2026-11-04T21:49:40Z
base: d8b618840c0a4bf32b2663acee0b0c927fbc90fd
base_tree: ce69163b3cc8e5488847e2beb8f6243965b2e3ac
plan0_at: 2026-11-04T21:44:25Z
plan0_scope: []
verified: strong
---
# SECURITY: the live server's same-uid check matches the client's socket row by address as well as ports: a request from 127.0.0.2:P (another uid) must not inherit the uid of the user's 127.0.0.1:P connection; exactly one matching row, else the cookie path
## Raw request
> SECURITY: the live server's same-uid check matches the client's socket row by address as well as ports: a request from 127.0.0.2:P (another uid) must not inherit the uid of the user's 127.0.0.1:P connection; exactly one matching row, else the cookie path
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] peer_uid only matches a row whose local address is the request's client address and whose remote address and port are the server's; a 127.0.0.2 client with the user's port number gets None; two matching rows give None — verify with `python3 plugin/tests/run.py test_live`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test with a fake /proc; the address match; restart the service
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_live && curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:46459/` → exit 0 · OK / 200 [ran] [tree 4d99dfb9d0d4] [world 2f1906870a] (2026-11-04T21:47:42Z)
- `python3 plugin/tests/run.py test_live` → ✗ exit 1 · Ran 43 tests in 17.0s (10 classes, 16 at a time; slowest: Page 15s, Serve 13s, Snapshot 5s) / FAILED (1 classes: test_live.PeerUid) (start tree + this task's tests) [ran] [tree 4d99dfb9d0d4] [world 2f1906870a] (2026-11-04T21:48:22Z)
- `python3 plugin/tests/run.py test_live` → exit 0 · Ran 43 tests in 17.2s (10 classes, 16 at a time; slowest: Serve 16s, Page 16s, Snapshot 8s) / OK [ran] [tree 4d99dfb9d0d4] [world 2f1906870a] (2026-11-04T21:48:22Z)
- (ac 1) `python3 plugin/tests/run.py test_live` → exit 0 · reused: the same command passed on this tree and world at 2026-11-04T21:48:22Z [ran] [tree 4d99dfb9d0d4] [world 2f1906870a] (2026-11-04T21:48:32Z)
- (audit intent) `found by the adversarial fm-reviewer pass on T-3026 (it traced the code path); fixed test-first with a fake /proc holding the attacker's 127.0.0.2 row; the service was stopped while the hole was open and restarted with the fix` → only the client's own socket row (its address and port, the server's address and port) decides the uid; one row exactly [tree 4d99dfb9d0d4] (2026-11-04T21:48:32Z)
- (audit adversary) `found by the adversarial fm-reviewer pass on T-3026 (it traced the code path); fixed test-first with a fake /proc holding the attacker's 127.0.0.2 row; the service was stopped while the hole was open and restarted with the fix` → another uid binding 127.0.0.2 with the user's port number now gets None and falls to the cookie; a second matching row makes it ambiguous and None; a non-loopback client address is None before any read [tree 4d99dfb9d0d4] (2026-11-04T21:48:32Z)
- (audit edge) `found by the adversarial fm-reviewer pass on T-3026 (it traced the code path); fixed test-first with a fake /proc holding the attacker's 127.0.0.2 row; the service was stopped while the hole was open and restarted with the fix` → IPv4-mapped rows still count for 127.0.0.1; ::1 maps to its own form; a socket from the user to another server is not a match [tree 4d99dfb9d0d4] (2026-11-04T21:48:32Z)
- (audit self) `found by the adversarial fm-reviewer pass on T-3026 (it traced the code path); fixed test-first with a fake /proc holding the attacker's 127.0.0.2 row; the service was stopped while the hole was open and restarted with the fix` → no findings [tree 4d99dfb9d0d4] (2026-11-04T21:48:32Z)
## Log
- 2026-11-04T21:44:23Z created
- 2026-11-04T21:44:24Z focused
- 2026-11-04T21:48:31Z scope: live.py peer_uid and its caller, test_live.py PeerUid
- 2026-11-04T21:49:37Z done
- 2026-11-04T21:49:40Z committed b75abe96 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3023 [FEATURE M, done, 3 steps] Machine-wide live server with same-user access: /api/machine lists every project and live session; /api/state and /api/stream take ?pro…
- playbook Security Review Skill (fm playbooks show security/security-review)
- T-2159 [FEATURE M, done, 3 steps] Coverage must be real: reset coverage.md's templated cells (a shim to…, a site page to…,… — lesson: A templated-text detector has to co…
- decision 2026-09-26: T-0014 supervisor: systemd user unit only (no tmux-only fallback); the unit runs tmux on a private socket (foreman-<slug>) for the TTY Remote Contro…
- similar past tasks were M: consider --tier M
- similar finished tasks took 3–3 steps
## Why not caught
T-3023's tests faked only rows of the honest client; no test planted a second row with the same port on another address
## Lessons
- A peer lookup in /proc must match the whole 4-tuple, never ports alone: ports are per-address, and another user can bind the same port on another loopback address
## Files touched
- plugin/lib/sampo/live.py
- plugin/tests/test_live.py
