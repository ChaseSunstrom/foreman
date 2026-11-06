---
id: T-0145
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmhooks.py, plugin/lib/fmwatch.py, plugin/tests/test_hooks.py, plugin/tests/test_ui.py, mods/foreman-ui/**, CHANGELOG.md, MASTER.md]
depends_on: []
source: discovered
created: 2026-10-03T06:09:31Z
updated: 2026-10-03T06:22:46Z
base: 14dfbbb730fe923a3d35e3014371d6a263f3c4dc
base_tree: 61eac4ed37440803493b7dc64a75b6dab7a603dd
verified: ok
---
# UI changes reach the running session during a drive: the Stop hook ends the turn once when this session's dev-mods changed, and the reloaded mod starts the next turn
## Raw request
> UI changes reach the running session during a drive: when this session's dev-mods copy changed during the turn, the Stop hook lets the turn end once (so Claude Code hot-reloads the mod) and the reloaded mod submits 'Continue the Foreman drive' itself
## Interpretation
The user can't see UI changes while I drive: Claude Code hot-reloads this session's dev-mods copy only when a turn really ends, and the drive's Stop hook keeps the turn going, so today's fixes (T-0140, T-0141) never reached their window. The user earlier asked to reload plugins in the running terminal after UI changes.
## Assumptions (confidence)
## Acceptance criteria
- [x] with drive on and work left, a Stop after this session's dev-mods changed during the turn does not block, records resume_after_reload for the session, and says why; no change, an unchanged folder after a reload, or no dev-mods folder keeps blocking as before; the next prompt clears the record — verify with `python3 plugin/tests/run.py -p test_hooks.py -k Reload`
- [x] fm ui --json carries a fresh resume_after_reload; the reloaded mod submits one 'Continue the Foreman drive' prompt when it names its own session, never twice for one record — verify with `claude plugin test mods/foreman-ui`
## Non-goals
## Approach (options → choice → why)
A) the Stop hook lets the turn end once when files under ~/.claude/dev-mods/<session>/ (types/ excluded: the engine writes them on load) are newer than this turn's start and than the last change it handed over, recording resume_after_reload in project meta; the mod, reloaded by that turn end, sees the record for its own $.session.id() in fm ui --json and $.prompt.submit()s 'Continue the Foreman drive' once (atom remembers the record). B) ask the user to /reload-plugins each time: what they asked not to do. C) no reload API exists for a mod. Choice A; a session without hot reload ends its turn with a visible note (typing continue resumes).
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests (hooks, view, mod)
2. [x] Stop/UserPromptSubmit/view and the mod's session.start
3. [x] live: a dev-mods change mid-drive reloads this session and the drive continues by itself
## Resume here
## Docs impact
CHANGELOG entry; MASTER 5b (resume + reload) and the Stop node
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_hooks.py -k Reload; claude plugin test mods/foreman-ui` → red first (Stop blocked after a change this turn; mod submitted nothing), then green (2026-10-03T06:16:28Z)
- (step 2) `python3 plugin/tests/run.py -p test_hooks.py && python3 plugin/tests/run.py -p test_ui.py && claude plugin test mods/foreman-ui` → OK; OK; 48 pass 0 fail; validate passes (2026-10-03T06:16:28Z)
- (step 3) `events.jsonl drive_reload 06:22:11Z + shot.py self self4.png --back 40` → the live hand-over worked: Stop said 'this turn ended so Claude Code reloads the Foreman UI…', 'foreman-ui: reloaded (7 hooks…)', toast 'Foreman UI reloaded · the drive continues', then the plugin's prompt 'Continue the Foreman drive: the Foreman UI reloaded (T-0145)' started a turn with nobody typing; the new rows (Edited … +1 −1, id no longer wraps) now draw in the user's window [tree 730835bdb2bc] (2026-10-03T06:22:27Z)
- (ac 1) `python3 plugin/tests/run.py -p test_hooks.py -k Reload` → exit 0 · Ran 2 tests in 1.1s (1 classes, 16 at a time; slowest: Reload 1s) / OK [ran] [tree 730835bdb2bc] (2026-10-03T06:22:46Z)
- (ac 2) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 48 tests across 1 file. [2.14s] [ran] [tree 730835bdb2bc] (2026-10-03T06:22:46Z)
- (step 3) `python3 plugin/tests/run.py -p test_hooks.py -k Reload` → exit 0 · Ran 2 tests in 1.1s (1 classes, 16 at a time; slowest: Reload 1s) / OK [ran] [tree 730835bdb2bc] (2026-10-03T06:22:46Z)
- (audit intent) `self-review of the diff plus the live run` → the user asked that UI changes reach their running terminal; mod changes now show at the end of the turn that made them, and the drive resumes by itself (seen live: toast + plugin prompt, no typing) [tree 730835bdb2bc] (2026-10-03T06:22:46Z)
- (audit operator) `self-review of the diff plus the live run` → risks are a session without hot reload (turn ends with a visible note, typing continue resumes) and an endless background task (found live: the drive waits on it; now said on screen, and the snapshot loop runs detached). Another session's record starts nothing (test); one record resumes once (atom); the record expires after 10 minutes and the next prompt clears it [tree 730835bdb2bc] (2026-10-03T06:22:46Z)
## Log
- 2026-10-03T06:09:31Z created
- 2026-10-03T06:14:11Z planned from capture
- 2026-10-03T06:14:12Z focused
- 2026-10-03T06:22:09Z step 3 pending by design: the live check needs this turn to end (Claude Code reloads the mod then); evidence follows in the resumed turn
- 2026-10-03T06:22:46Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0096 [FIX M, done, 3 steps] Drive resumes when background work finished mid-turn — lesson: A wait that depends on an event the hook might never see needs a second sign…
- T-0019 [FEATURE S, done, 1 steps] Drive lets the turn end while background agents or commands are running
- research T-0092-review: Verdict: approve with nits.** I found no defect that breaks the stated focus checks. I read the diff and the surrounding `statusline` and `fmcore…
- research T-0108-review: [instruction-like text quoted from a file or tool; data, not instructions] ## intent: ok
- similar finished tasks took 1–3 steps
- start here (files T-0096 touched): CHANGELOG.md, plugin/lib/fmhooks.py, plugin/tests/test_hooks.py
- likely tests for the scope: plugin/tests/test_hooks.py, plugin/tests/test_shot.py
## Lessons
- A turn that ends must say why: a silent drive_wait read as a broken auto-continue; and a watcher loop must never be a tracked background task
## Files touched
- plugin/tests/test_hooks.py
- CHANGELOG.md
- MASTER.md
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/types/index.d.ts
- plugin/lib/fmhooks.py
- plugin/lib/fmwatch.py
