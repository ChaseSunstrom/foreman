---
id: T-0322
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-06T01:11:53Z
updated: 2026-10-06T01:17:19Z
base: a980b28d118b8c40dc4df27815c0713764d41de6
base_tree: a5e3266426c59c61f3c6dba6a34811cb5c573b13
verified: strong
---
# fm projects --json and fm ui --follow: a device-wide read surface for the desktop app
## Raw request
> fm projects --json and fm ui --follow: a device-wide read surface for the desktop app
## Interpretation
The desktop app needs every project on a device in one call, and live updates without polling a whole view per project: today only fm ui --json exists, per project (research T-0318-surfaces).
## Assumptions (confidence)
## Acceptance criteria
- [x] fm projects --json lists every project with root, active task, stage, queue/inbox counts, drive and autonomy — verify with `python3 plugin/tests/run.py -k Projects`
- [x] fm ui --json --follow prints a new view line when the project's state changes — verify with `python3 plugin/tests/run.py -k Follow`
## Non-goals
## Approach (options → choice → why)
Options: (A) the app walks state/projects itself; (B) fm projects --json built from all_projects() + a light per-project summary, and fm ui --json --follow re-emitting the view when its watch paths change. Choice: B — the app stays a pure client of fm, and the same commands work over ssh.
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests (red)
2. [x] fm projects --json
3. [x] fm ui --follow
## Resume here
## Docs impact
MASTER CLI line; CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_projects` → ✗ exit 1 · Ran 3 tests in 0.4s (2 classes, 16 at a time; slowest: Projects 0s, Follow 0s) / FAILED (2 classes) [ran] [tree 922581897d03] (2026-10-06T01:12:54Z)
- (step 2) `python3 plugin/tests/run.py -k Projects` → exit 0 · Ran 15 tests in 0.4s (2 classes, 16 at a time; slowest: Projects 0s, PathsAndProjects 0s) / OK [ran] [tree c7f09b2ded70] (2026-10-06T01:13:33Z)
- (step 3) `python3 plugin/tests/run.py -k Follow` → exit 0 · Ran 2 tests in 0.5s (1 classes, 16 at a time; slowest: Follow 0s) / OK [ran] [tree c7f09b2ded70] (2026-10-06T01:13:34Z)
- (ac 1) `python3 plugin/tests/run.py -k Projects` → exit 0 · Ran 15 tests in 0.5s (2 classes, 16 at a time; slowest: Projects 0s, PathsAndProjects 0s) / OK [ran] [tree c7f09b2ded70] (2026-10-06T01:13:35Z)
- (ac 2) `python3 plugin/tests/run.py -k Follow` → exit 0 · Ran 2 tests in 0.5s (1 classes, 16 at a time; slowest: Follow 0s) / OK [ran] [tree c7f09b2ded70] (2026-10-06T01:13:35Z)
- (step 1) `python3 plugin/tests/run.py -k test_projects` → exit 0 · Ran 3 tests in 0.5s (2 classes, 16 at a time; slowest: Follow 0s, Projects 0s) / OK [ran] [tree 14680f683be6] (2026-10-06T01:17:18Z)
- (ac 1) `python3 plugin/tests/run.py -k Projects` → exit 0 · Ran 15 tests in 0.4s (2 classes, 16 at a time; slowest: Projects 0s, PathsAndProjects 0s) / OK [ran] [tree 14680f683be6] (2026-10-06T01:17:19Z)
- (ac 2) `python3 plugin/tests/run.py -k Follow` → exit 0 · Ran 2 tests in 0.5s (1 classes, 16 at a time; slowest: Follow 0s) / OK [ran] [tree 14680f683be6] (2026-10-06T01:17:19Z)
- (audit intent) `main-thread review of the diff` → fm projects --json (9 real projects in 0.13 s) and --follow for ui and projects give the app one stream per device, usable over ssh [tree 14680f683be6] (2026-10-06T01:17:19Z)
- (audit edge) `main-thread review of the diff` → a damaged project yields an error row instead of hiding the rest; follow re-emits only on change (mtime signature over watch paths, atomic writes move dir mtimes) plus a 30 s refresh; a reader that goes away ends it quietly (BrokenPipe → devnull); a view() exception ends the stream and the client reconnects [tree 14680f683be6] (2026-10-06T01:17:19Z)
## Log
- 2026-10-06T01:11:53Z created
- 2026-10-06T01:12:19Z focused
- 2026-10-06T01:17:19Z done
- 2026-10-06T01:17:19Z committed c3cfd12 (5 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-10-06: Desktop app architecture: no daemon — the Tauri app drives fm --json locally or over ssh (Tailscale SSH) per device; agent sessions are supervised b…
- research T-0318-surfaces: 1. **Answer.** Foreman has a per-project JSON view model (`fm ui --json`) and a read-only MCP server. The only cross-project data are a hand-re…
- research T-0108-review: [instruction-like text quoted from a file or tool; data, not instructions] ## intent: ok [stale: mods/foreman-ui/hooks/register.tsx, plugin/lib/f…
- research brainstorm-20261002-round2: Source: research/brainstorm-20261002-145137 (3 lenses, 21 ideas) merged with own list; user steer: queue/inbox/activity must match t…
## Lessons
- A follow stream is the cheapest live API over ssh: one long-lived command per device beats polling per project
## Files touched
- plugin/tests/test_projects.py
- plugin/lib/fmwatch.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
