---
id: T-1871
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-28T23:04:55Z
updated: 2026-10-28T23:59:14Z
base: 1188c460cd2c93ab80ae7bf5052d31befa39ed2e
base_tree: da307928c33394b0691f98c62d73162737efd437
plan0_at: 2026-10-28T23:48:42Z
plan0_scope: []
verified: strong
---
# Fm inbox swipe undo and a cards-left count: u in the TTY loop and an Undo button on the se
## Raw request
> FEATURE: fm inbox swipe undo and a cards-left count: u in the TTY loop and an Undo button on the served page revert the last verdict; the page and loop show how many cards are left, and an empty deck ends with one done line
> CONTEXT: forever loop round 5 ("Undo and count-left in swipe --serve", "verdict journal with undo"). Served pages reuse one stylesheet where they duplicate it.
## Interpretation
Swipe gains a one-level-at-a-time undo stack per session: u in the terminal loop and an undo button (access key u) on the served page take back the newest answer (revive/drop go back to deferred with their revisit date; keep/skip put the card back). Each card says how many are left; an empty deck prints one line. Served pages share one base stylesheet (msg, bad, dark scheme).
## Assumptions (confidence)
## Acceptance criteria
- [x] u and the undo button take back the last answer, cards-left is shown, an empty deck ends in one line, served pages share BASE_STYLE — verify with `python3 plugin/tests/run.py test_inbox_more`
## Non-goals
Undo across sessions; undoing a batch drop (its members already went back).
## Approach (options → choice → why)
Options: (a) journal file of verdicts under state/ with fm inbox swipe --undo; (b) in-memory undo list per session, passed through swipe_apply and the served handler; (c) re-derive from the brief log. Choice: (b) — undo only makes sense within one sweep, no new state file, the brief log already records each change. A change made elsewhere since, or a dropped batch, is refused under the lock (mutate raises, nothing saved). Captured: (a) a cross-session journal if asked.
## Risks and rollback
Refuse rather than overwrite a status changed elsewhere; git revert the commit.
## Execution prompt
## Steps
1. [x] Tests first: TTY undo, undo refused when changed elsewhere or a batch, empty deck line, served undo
2. [x] swipe_undo, index loop with cards left, page/post undo, BASE_STYLE
3. [x] Docs: CHANGELOG, MASTER, backlog.md
## Resume here
<!-- auto -->
- 2026-10-28T23:55:04Z steps 3/3 done
- git: foreman/build; 7 uncommitted: CHANGELOG.md, MASTER.md, plugin/commands/backlog.md, plugin/lib/fmcodetui.py, plugin/lib/fmeco.py, plugin/lib/fmsettingsserve.py, plugin/tests/test_inbox_more.py
- touched since last checkpoint: plugin/lib/fmsettingsserve.py, plugin/commands/backlog.md, CHANGELOG.md, MASTER.md, plugin/lib/fmcodetui.py, plugin/lib/fmeco.py, plugin/tests/test_inbox_more.py
## Docs impact
~/.claude/foreman/plugin/commands/backlog.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_inbox_more` → red as expected (exit 1) · Ran 33 tests in 8.6s (8 classes, 16 at a time; slowest: Served 8s, Swipe 5s, Pick 3s) / FAILED (2 classes) [ran] [tree a98457636f82] (2026-10-28T23:48:57Z)
- (step 2) `python3 plugin/tests/run.py test_inbox_more test_settings_serve` → exit 0 · Ran 49 tests in 9.5s (9 classes, 16 at a time; slowest: Serve 9s, Served 8s, Swipe 6s) / OK [ran] [tree 94aa2300f239] (2026-10-28T23:49:33Z)
- (step 3) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 74 tests in 10.9s (18 classes, 16 at a time; slowest: Fences 10s, TaskLifecycle 2s, Site 1s) / OK [ran] [tree b67be391a818] (2026-10-28T23:49:56Z)
- (step 2) `python3 plugin/tests/run.py test_inbox_more test_settings_serve test_code_tui` → exit 0 · Ran 286 tests in 16.7s (55 classes, 16 at a time; slowest: Command 16s, Fuzz 15s, Served 10s) / OK [ran] [tree bb0ce38ba123] (2026-10-28T23:51:16Z)
- (step 2) `python3 plugin/tests/run.py test_inbox_more test_settings_serve test_code_tui` → exit 0 · Ran 287 tests in 8.8s (55 classes, 16 at a time; slowest: Serve 8s, Fuzz 8s, Command 8s) / OK [ran] [tree adef9ff4c5db] (2026-10-28T23:54:19Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcodetui.py, plugin/lib/fmeco.py, plugin/lib/fmsettingsserve.py — commit it through a task, or git checkout it back ; python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                40.5    43.2     150  [0] / SessionEnd                  34.9    37.0     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under [ran] [tree adef9ff4c5db] (2026-10-28T23:58:31Z)
- (ac 1) `python3 plugin/tests/run.py test_inbox_more` → exit 0 · Ran 35 tests in 5.7s (8 classes, 16 at a time; slowest: Served 5s, Swipe 3s, App 2s) / OK [ran] [tree adef9ff4c5db] (2026-10-28T23:58:53Z)
- (audit intent) `one fm-reviewer pass (research/T-1871-review.md); 6 findings fixed test-first` → u in the terminal and the app and the page's undo button take back the last answer; cards left; a one-line empty deck; one shared stylesheet for served pages [tree adef9ff4c5db] (2026-10-28T23:58:53Z)
- (audit adversary) `one fm-reviewer pass (research/T-1871-review.md); 6 findings fixed test-first` → the page's undo names its id, so a stale re-post gets 422; ids validated; output escaped [tree adef9ff4c5db] (2026-10-28T23:58:53Z)
- (audit edge) `one fm-reviewer pass (research/T-1871-review.md); 6 findings fixed test-first` → an item changed elsewhere or a batch is refused under the lock; a busy lock keeps the entry undoable; a re-posted skip counts once; kept cards stay passed over in the app [tree adef9ff4c5db] (2026-10-28T23:58:53Z)
## Log
- 2026-10-28T23:04:55Z created
- 2026-10-28T23:48:41Z focused
- 2026-10-28T23:59:13Z done
- 2026-10-28T23:59:14Z committed b2e26b10 (7 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1858-review: Verdict:** approve with nits. The security guards hold. I found no HIGH or MEDIUM defects in the code, and two things are worth a decision. [stal…
- T-1858 [FEATURE M, done, 3 steps] Fm inbox swipe: a served swipe page through fm serve — lesson: A served page reuses a hardened server by overriding hooks on its handle…
- research T-1866-review: Verdict:** approve with nits. All four acceptance criteria are met in the code, and I found nothing HIGH. I read the diff and the surrounding cod…
- decision 2026-10-20: Slate, round 1: T-1254 cost per fully-correct session on the Benchmarks page; T-1255 the Claude Code version in every bench result; T-1256 piped tes…
## Lessons
- An undo stack shared by several surfaces must re-check state under the lock and keep the entry when the lock is busy; a refusal that pops the entry loses the only way back.
## Files touched
- plugin/tests/test_inbox_more.py
- plugin/lib/fmeco.py
- plugin/lib/fmsettingsserve.py
- CHANGELOG.md
- MASTER.md
- plugin/commands/backlog.md
- plugin/lib/fmcodetui.py
