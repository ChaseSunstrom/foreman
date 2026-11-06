---
id: T-1762
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcodetui.py, plugin/tests/test_code_tui.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: followup
created: 2026-10-23T07:54:56Z
updated: 2026-10-23T08:01:15Z
batch: [T-1755, T-1756, T-1761]
base: 64f9412a0b65d764e6022b35a87a3d74969d396d
base_tree: 14aa1da7400d91bb9a5ad91230cb7104472f1fc0
plan0_at: 2026-10-23T07:58:04Z
plan0_scope: [plugin/lib/fmcodetui.py, plugin/tests/test_code_tui.py, CHANGELOG.md, MASTER.md]
verified: strong
---
# fm code app action cards: a failure or a stall shows a card with what happened and one-key next steps, the app sweeps r…
## Raw request
> T-1755: fm code app: an error as a three-row card (what happened / what Foreman did / next) with its Next: command one key away; a request piped on stdin read as context (rest of T-1334)
> T-1756: fm code app: opening the app sweeps runners a killed run left (stop_survivors), quitting mid-run shows 'stopping <runner> (pid N)… stopped' per child, and the header says when the worker runs guard-only (rest of T-1337)
> T-1761: fm code app: a stalled run shows a card with w wait, k kill, m switch runner (rest of T-1373)
## Interpretation
Do T-1755, T-1756, T-1761 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-1762. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-1755: a failure shows a card (what happened, what Foreman did, the next command); Enter resumes, opens a read-only fm command's output, or names any other for the user's shell; Esc hides it — verify with `python3 plugin/tests/run.py test_code_tui.Cards`
- [x] T-1756: the app stops runners a killed run left when it opens, and quitting mid-run prints 'stopping NAME (pid N)… stopped' for each runner the run had — verify with `python3 plugin/tests/run.py test_code_tui.Cards`
- [x] T-1761: a live stall shows a card: w waits, k stops the run, m stops it and picks another runner to resume with; any sign of life ends it — verify with `python3 plugin/tests/run.py test_code_tui.Cards`
## Non-goals
## Approach (options → choice → why)
Cards are drawn over the run view from State (status, error, next, and a stall kept until the next non-heartbeat event), not a new mode, so the panels stay live behind them; Esc hides the one on screen (keyed by its kind and first line). Enter on a failure only runs what is safe without the user: a resume, or an allowlisted read-only fm command whose output opens in the existing text view; anything else (fm ask, fm replay) is named for their shell. The open-time sweep reuses fmcode.stop_survivors; the per-runner quit lines read fmcode's code-procs entries owned by the app's child, printed after the screen closes, killing any group still there after 3 s. Options considered: a modal card view (hides the run), running any next command (some need the user's answer), a sweep only in fm code (the app's first run would do it, but opening the app is when a leftover shows).
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-1755: Fm code app: an error as a three-row card (what happened / what Foreman did / next) with i
2. [x] T-1756: Fm code app: opening the app sweeps runners a killed run left (stop_survivors), quitting m
3. [x] T-1761: Fm code app: a stalled run shows a card with w wait, k kill, m switch runner (rest of T-13
## Resume here
## Docs impact
CHANGELOG, MASTER
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 205 tests in 8.3s (35 classes, 16 at a time; slowest: Fuzz 8s, Command 8s, Events 3s) / OK [ran] [tree 1b0563631863] (2026-10-23T08:00:26Z)
- (step 2) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 205 tests in 8.4s (35 classes, 16 at a time; slowest: Fuzz 8s, Command 8s, Events 3s) / OK [ran] [tree 1b0563631863] (2026-10-23T08:00:35Z)
- (step 3) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 205 tests in 8.3s (35 classes, 16 at a time; slowest: Fuzz 8s, Command 8s, Events 3s) / OK [ran] [tree 1b0563631863] (2026-10-23T08:00:44Z)
- (audit intent) `self: members re-read` → pass: failure and stall cards with one-key next steps, the open-time sweep, per-runner stop lines on quit [tree db500c7a3aa9] (2026-10-23T08:00:45Z)
- (ac 1) `python3 plugin/tests/run.py test_code_tui.Cards` → exit 0 · Ran 5 tests in 0.6s (1 classes, 16 at a time; slowest: Cards 0s) / OK [ran] [tree db500c7a3aa9] (2026-10-23T08:00:52Z)
- (ac 2) `python3 plugin/tests/run.py test_code_tui.Cards` → exit 0 · Ran 5 tests in 0.6s (1 classes, 16 at a time; slowest: Cards 0s) / OK [ran] [tree db500c7a3aa9] (2026-10-23T08:00:52Z)
- (ac 3) `python3 plugin/tests/run.py test_code_tui.Cards` → exit 0 · Ran 5 tests in 0.6s (1 classes, 16 at a time; slowest: Cards 0s) / OK [ran] [tree db500c7a3aa9] (2026-10-23T08:00:52Z)
- (audit intent) `self review (subagents paused at 77% weekly usage): intent, adversary, edge` → all three criteria met [tree db500c7a3aa9] (2026-10-23T08:00:52Z)
- (audit adversary) `self review (subagents paused at 77% weekly usage): intent, adversary, edge` → Enter runs only a resume or an allowlisted read-only fm command (full-match regex, argv split, fm's own script, 30 s); fm ask, fm replay and anything else are named, never run; the quit report kills only groups registered as this app's child's runners, after checking they're alive [tree db500c7a3aa9] (2026-10-23T08:00:52Z)
- (audit edge) `self review (subagents paused at 77% weekly usage): intent, adversary, edge` → a card hidden with Esc returns only for a new failure or stall; the stall card goes on any sign of life; Enter with no next command does nothing; a runner whose name /proc can't read is skipped [tree db500c7a3aa9] (2026-10-23T08:00:52Z)
## Log
- 2026-10-23T07:54:56Z created
- 2026-10-23T07:57:50Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_code_tui.Cards`
- 2026-10-23T07:57:50Z criterion 1 text: T-1755: Fm code app: an error as a three-row card (what happened / what Foreman did / next) with i works → T-1755: a failure shows a card (what happened, what Foreman did, the next command); Enter resumes, opens a read-only fm command's output, or names any other for the user's shell; Esc hides it
- 2026-10-23T07:57:51Z criterion 2 verify: `` → `python3 plugin/tests/run.py test_code_tui.Cards`
- 2026-10-23T07:57:51Z criterion 2 text: T-1756: Fm code app: opening the app sweeps runners a killed run left (stop_survivors), quitting m works → T-1756: the app stops runners a killed run left when it opens, and quitting mid-run prints 'stopping NAME (pid N)… stopped' for each runner the run had
- 2026-10-23T07:57:51Z criterion 3 verify: `` → `python3 plugin/tests/run.py test_code_tui.Cards`
- 2026-10-23T07:57:51Z criterion 3 text: T-1761: Fm code app: a stalled run shows a card with w wait, k kill, m switch runner (rest of T-13 works → T-1761: a live stall shows a card: w waits, k stops the run, m stops it and picks another runner to resume with; any sign of life ends it
- 2026-10-23T07:57:52Z set scope=['plugin/lib/fmcodetui.py', 'plugin/tests/test_code_tui.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-23T07:58:02Z focused
- 2026-10-23T08:01:13Z done
- 2026-10-23T08:01:15Z committed 3c5ae76a (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1754 [FEATURE M, done, 3 steps] fm code: a Next: line on every failure, the start event names the Foreman running it, and a registry that stops runners… — lesson: A re…
- T-1760 [FEATURE M, done, 3 steps] fm code diagnostics: fm code why explains a run, piped stdin is the request's context, and the start event and the app … — lesson: Read…
- T-1741 [FEATURE M, done, 2 steps] fm code TUI: navigation (/ search, context key hints, Tab focus ring) and a real request line editor (history, Ctrl key… — lesson: Put …
- decision 2026-10-20: Slate, round 1: T-1254 cost per fully-correct session on the Benchmarks page; T-1255 the Claude Code version in every bench result; T-1256 piped tes…
## Lessons
- A process's /proc name right after Popen can still be the parent's: wait for the exec before reading it in a test
## Files touched
- plugin/tests/test_code_tui.py
- plugin/lib/fmcodetui.py
- CHANGELOG.md
- MASTER.md
