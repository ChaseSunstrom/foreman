---
id: T-3320
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-06T04:26:29Z
updated: 2026-11-06T04:26:29Z
steer_method_rate: 0.218
---
# Sampo must support any number of concurrent sessions on one repo, including recursive…
## Raw request
> And also the ability to have multiple sessions running in parallel on the same repo/recursive tower improvement like I was talking about, and even on different machines via git/changes/whatever, while still being managed entirely without duplications/drift, etc.
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- Sampo must support any number of concurrent sessions on one repo, including recursive tower-improvement runs where one level improves the level below. Sessions on other machines must also be supported, with changes moving over git, patches or bundles. All of them are managed as one coherent system …
- Keep one canonical source of truth for coordination state: a work ledger of tasks, claims, status, owner session or machine, base commit and results. It lives in the repo or a repo-synced location and is not in any session's memory. Every session reads it before starting work and updates it as work…
- Make claims explicit and expiring. A session claims a task or tower level with a lease (owner ID, machine ID, timestamp, heartbeat). A live lease blocks others from taking the same work. A stale lease can be reclaimed safely and the reclaim is recorded. Two sessions can never both hold the same cla…
- Prevent duplication at the source. Before starting work, a session checks the ledger and the current tree for the same or equivalent task, and merges or defers to existing work instead of redoing it. Every piece of work has a stable identity (a task ID or content-derived key), so replays and retrie…
- Isolate each session's working changes in its own branch, worktree or equivalent, with the base commit recorded. Integrate through a defined, ordered path: rebase or merge, re-run verification on the result, then land. Never edit another session's in-flight files directly.
- Detect and resolve drift. When sessions or machines diverge (different base, conflicting edits, a ledger that disagrees with the tree, a tower level built on a superseded lower level), the system detects it, reports it, and reconciles it by a documented rule. It never silently overwrites either sid…
- For recursive tower improvement, make each level's inputs, outputs and dependencies explicit. When a lower level changes, the levels above it are marked stale and re-validated. Concurrent improvement passes on different levels must not clobber each other, and the tower's state must be reproducible …
- Make cross-machine sync work with only git or a plain transferable artifact (patch or bundle). It must tolerate offline periods and out-of-order arrival, and it must converge to the same state on every machine once synced. No shared filesystem or live connection is required.
- Prove it with tests. Cover at least: two sessions racing for one claim, a session crashing mid-task and its lease expiring, duplicate task submission, divergent bases from two machines converging, and a lower tower level changing under an upper one. Run them as part of the normal verification, and …
- Give the user visibility and control: a status command or view showing all active sessions, machines, claims, stale leases, detected drift and the integration queue, plus a way to release, reassign or cancel a claim.
- Update every surface this touches: the ledger and claim implementation, the session start and finish hooks, the docs and runbook for multi-session and multi-machine use, and the config and defaults. Add measures such as duplicate-work rate, drift events, reclaim count and time to converge.
- Act on this by building and wiring it in. Don't just advise or describe it. Anything outward-facing or irreversible still needs the user's grant. That covers pushing to or pulling from remotes, connecting to other machines, force-pushing, rewriting history, deleting branches or worktrees, and overr…
## Assumptions (confidence)
## Acceptance criteria
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-06T04:26:29Z created
## Follow-ups captured
