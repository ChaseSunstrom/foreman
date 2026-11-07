---
id: T-2090
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-30T03:27:43Z
updated: 2026-10-30T13:29:10Z
base: 0b64215c092c64a01c3dd4e8967be97431d183c4
base_tree: 332883794333b9d032a56c280c9cac734694be82
plan0_at: 2026-10-30T03:27:52Z
plan0_scope: []
verified: ok
---
# Genesis keeps the site live: fm genesis live on + detached publish on every tower change
## Raw request
> Genesis keeps the site live: fm genesis live on + detached publish on every tower change

Also asked (T-2088, done here):
> Genesis keeps the site live on its own: every fm genesis put/init (and exam results) re-exports site/genesis and ships it to main (standing grant), debounced so a burst of puts is one push
## Interpretation
User: 'for everything in genesis, have your stuff automatically update the site, so its constantly up to date'. Every tower change (put/init, task progress on mission tasks, exam results) should reach https://chasesunstrom.github.io/foreman/genesis/ without a manual export + ship. Main pushes are standing-approved by the user (2026-10-29); the grant-on-a-task rule stays by spending one publish grant to switch live publishing on.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm genesis live on needs and spends a publish grant; off clears it — verify with `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis`
- [x] fm genesis publish pushes site/genesis data to main only when the tower changed, skips when unchanged, never touches other paths — verify with `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis`
- [x] tower puts and the Stop hook kick a throttled detached publish only while live is on — verify with `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis test_hooks`
- [x] fm genesis status shows the site's live state and last push; docs and CI paths-ignore updated — verify with `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis test_docs`
## Non-goals
## Approach (options → choice → why)
Complete version: opt-in switch (live on/off, grant spent once, undo listed), trigger on every tower write and each turn end, throttle, single instance, change detection that ignores the per-run updated/rev fields, data-only commits (site/genesis) in a scratch worktree off fetched main, push, last-result status, CI skip for data-only pushes, docs. Approaches: A) detached fm genesis publish kicked by put/init and the Stop hook, throttled 5 min (chosen: no session tokens, works in CC via the hook, local and reversible via live off). B) Claude-driven export+ship per Stop nudge (spends tokens every turn, needs a session). C) separate data branch + scheduled pages.yml build (moves the site build off main, cron lag, more CI). D) host cron/systemd timer (invisible to the user, needs the timers category, hard to undo). No in-worktree test run: nothing on main tests genesis data (outside_hosts reads html/css/js/svg only), and the JSON is built by json.dumps.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests: live on/off grant, publish to a bare remote (change, no change, paths), kick throttle and off, status
2. [x] implement live/publish/kick in fmgenesis + CLI + Stop hook wiring
3. [x] test.yml paths-ignore for genesis data; MASTER.md, README, CHANGELOG
4. [x] turn live on for this repo, publish once, verify the Pages deploy
## Resume here
<!-- auto -->
- 2026-10-30T03:48:42Z step 1/4: failing tests: live on/off grant, publish to a bare remote (change, no change, paths), kick throttle and off, status
- git: foreman/build; 7 uncommitted: .github/workflows/test.yml, CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/lib/fmhooks.py, plugin/tests/test_genesis.py
- touched since last checkpoint: /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/t2090c.py, plugin/lib/fmgenesis.py, plugin/lib/fmcli.py, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/t2090d.py, CHANGELOG.md, MASTER.md
## Docs impact
MASTER.md fmgenesis entry, CHANGELOG Unreleased
## Verification evidence
- (ac 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis 2>&1 | grep -E "^(FAIL|ERROR)|Ran|FAILED|OK" | head -10` → ✗ exit 1 · Ran 13 tests in 1.5s (3 classes, 16 at a time; slowest: Genesis 1s, GenesisLive 1s, GenesisExport 1s) / FAILED (1 classes) [ran] [tree db2e0ab3bc1c] (2026-10-30T03:29:06Z)
- (ac 2) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis 2>&1 | grep -E "^(FAIL|ERROR)|Ran|FAILED|OK" | head -10` → ✗ exit 1 · Ran 13 tests in 1.5s (3 classes, 16 at a time; slowest: Genesis 1s, GenesisLive 1s, GenesisExport 1s) / FAILED (1 classes) [ran] [tree db2e0ab3bc1c] (2026-10-30T03:29:06Z)
- (step 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis` → ✗ exit 1 · Ran 13 tests in 1.5s (3 classes, 16 at a time; slowest: Genesis 1s, GenesisLive 1s, GenesisExport 1s) / FAILED (1 classes) [ran] [tree db2e0ab3bc1c] (2026-10-30T03:29:11Z)
- (ac 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis 2>&1 | grep -vE "^\s*$" | tail -25` → ✗ exit 1 · Ran 13 tests in 2.0s (3 classes, 16 at a time; slowest: Genesis 2s, GenesisLive 1s, GenesisExport 1s) / FAILED (1 classes) [ran] [tree 8904e4504322] (2026-10-30T03:30:27Z)
- (ac 2) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis 2>&1 | grep -vE "^\s*$" | tail -25` → ✗ exit 1 · Ran 13 tests in 2.0s (3 classes, 16 at a time; slowest: Genesis 2s, GenesisLive 1s, GenesisExport 1s) / FAILED (1 classes) [ran] [tree 8904e4504322] (2026-10-30T03:30:27Z)
- (step 2) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis` → exit 0 · Ran 13 tests in 3.3s (3 classes, 16 at a time; slowest: GenesisLive 3s, Genesis 2s, GenesisExport 1s) / OK [ran] [tree 7a58b1e2a610] (2026-10-30T03:30:43Z)
- (step 3) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis test_docs test_which` → exit 0 · Ran 107 tests in 7.9s (26 classes, 16 at a time; slowest: Fences 8s, Which 2s, GenesisLive 2s) / OK [ran] [tree fd30945095bf] (2026-10-30T03:31:29Z)
- (step 4) `fm genesis live on, then fm genesis publish pushed e6a6a181 (site/genesis/genesis.json only) to origin main; re-run says up to date` → pages run e6a6a181 success; https://chasesunstrom.github.io/foreman/genesis/genesis.json serves updated 2026-10-30T03:31:33Z [tree fd30945095bf] (2026-10-30T03:33:25Z)
- (ac 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis 2>&1 | grep -E "^(FAIL|ERROR|AssertionError|.*Error:)" | head -20` → ✗ exit 1 · FAILED (failures=3) / FAILED (1 classes) [ran] [tree 17cf5d87f6ea] (2026-10-30T03:41:57Z)
- (ac 2) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis 2>&1 | grep -E "^(FAIL|ERROR|AssertionError|.*Error:)" | head -20` → ✗ exit 1 · FAILED (failures=3) / FAILED (1 classes) [ran] [tree 17cf5d87f6ea] (2026-10-30T03:41:57Z)
- (ac 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis 2>&1 | grep -E "^(FAIL|ERROR|AssertionError|.*Error:|Ran|OK)" | head -20` → exit 0 · Ran 14 tests in 4.6s (3 classes, 16 at a time; slowest: GenesisLive 4s, Genesis 2s, GenesisExport 1s) / OK [ran] [tree b3a3fc7207ab] (2026-10-30T03:43:11Z)
- (ac 2) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis 2>&1 | grep -E "^(FAIL|ERROR|AssertionError|.*Error:|Ran|OK)" | head -20` → exit 0 · Ran 14 tests in 4.6s (3 classes, 16 at a time; slowest: GenesisLive 4s, Genesis 2s, GenesisExport 1s) / OK [ran] [tree b3a3fc7207ab] (2026-10-30T03:43:11Z)
- (ac 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis` → exit 0 · Ran 14 tests in 2.6s (3 classes, 16 at a time; slowest: GenesisLive 2s, Genesis 1s, GenesisExport 1s) / OK [ran] [tree 459fb514c032] (2026-10-30T03:49:05Z)
- (ac 2) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis` → exit 0 · Ran 14 tests in 2.6s (3 classes, 16 at a time; slowest: GenesisLive 2s, Genesis 1s, GenesisExport 1s) / OK [ran] [tree 459fb514c032] (2026-10-30T03:49:05Z)
- (ac 3) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis test_hooks` → exit 0 · Ran 220 tests in 23.2s (30 classes, 16 at a time; slowest: Stop 23s, NoTaskGate 21s, PreToolUse 14s) / OK [ran] [tree 459fb514c032] (2026-10-30T03:49:05Z)
- (ac 4) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_genesis test_docs` → exit 0 · Ran 92 tests in 7.9s (23 classes, 16 at a time; slowest: Fences 8s, GenesisLive 3s, Genesis 1s) / OK [ran] [tree 459fb514c032] (2026-10-30T03:49:05Z)
- (audit intent) `one fm-reviewer pass (5 lenses): 2 medium + 4 low, all fixed test-first; full gates green (4296 tests)` → trailing edge fixed, a change inside the window goes out when it ends (pending + --settle) [tree 459fb514c032] (2026-10-30T03:49:05Z)
- (audit adversary) `one fm-reviewer pass (5 lenses): 2 medium + 4 low, all fixed test-first; full gates green (4296 tests)` → private ref replaces FETCH_HEAD; push refused outside site/genesis; failure text redacted [tree 459fb514c032] (2026-10-30T03:49:05Z)
- (audit edge) `one fm-reviewer pass (5 lenses): 2 medium + 4 low, all fixed test-first; full gates green (4296 tests)` → live on checks origin main before spending; second live on spends nothing; stale pending ignored [tree 459fb514c032] (2026-10-30T03:49:05Z)
- (audit operator) `one fm-reviewer pass (5 lenses): 2 medium + 4 low, all fixed test-first; full gates green (4296 tests)` → open-ended grant documented in MASTER.md, fm decide --kind outward [tree 459fb514c032] (2026-10-30T03:49:05Z)
- (audit maintainer) `one fm-reviewer pass (5 lenses): 2 medium + 4 low, all fixed test-first; full gates green (4296 tests)` → failed publish shows in status and is retried (test) [tree 459fb514c032] (2026-10-30T03:49:05Z)
## Log
- 2026-10-30T03:27:43Z created
- 2026-10-30T03:27:52Z focused
- 2026-10-30T03:31:30Z guard authorization added: publish
- 2026-10-30T03:31:30Z publish grant used by fm genesis live on
- 2026-10-30T03:49:42Z done
- 2026-10-30T03:49:44Z committed b1553311 (7 files)
- 2026-10-30T03:50:35Z guard authorization added: publish
- 2026-10-30T03:52:41Z publish grant used by fm ship
- 2026-10-30T13:29:10Z includes T-2088: Genesis keeps the site live on its own: every fm genesis put/init (and exam results)…
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2080 [FEATURE M, done, 4 steps] Genesis on the site: fm genesis export + a live interactive tower graph page, shipped to main — lesson: An export that feeds a public p…
- T-2078 [FEATURE M, done, 3 steps] fm genesis: the tower's home: init saves gen-0 verbatim and read-only, put files tower docs under research/genesis, status shows the to…
- research T-2078-review: Verdict:** approve with nits. The three acceptance criteria are met, and `put` refuses gen-0 and every path outside the tower shape. I found one …
- decision 2026-10-30: T-2080: push the Genesis export to main on the user's explicit ask ('can you push what you have in the genesis stuff to main?'); grant spent on this…
## Lessons
- a leading-edge throttle on a detached job drops the last change; schedule one trailing waiter instead
## Plan gaps
- failed first: step 1 failing tests: live on/off grant, publish to a bare remote (change, no change, paths), kick throttl…
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
- plugin/lib/fmcli.py
- plugin/lib/fmhooks.py
- .github/workflows/test.yml
- CHANGELOG.md
- MASTER.md
- plugin/tests/test_exam.py
