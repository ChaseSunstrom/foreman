---
id: T-2138
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-30T10:37:52Z
updated: 2026-10-30T10:48:52Z
base: 89e07defcf02ab3e0e822f6b10a14755afdca000
base_tree: ec6493cd3d8ae78567ff4b0750323fa90a0b0686
plan0_at: 2026-10-30T10:41:00Z
plan0_scope: []
verified: strong
---
# Stop wiring: a done claim while the last request has unaccounted clauses blocks once with them (Mission 4 brief 4)
## Raw request
> Stop wiring: a done claim while the last request has unaccounted clauses blocks once with them (Mission 4 brief 4)
## Interpretation
When the reply claims done (claims_done) while the last request still has clauses fm clauses could not map to a task, Stop blocks once and names them, so a sweeping request is not called done with parts silently dropped. Never a trap: no block on a stop_hook_active stop, once per set of open clauses per session, and a list older than a day is ignored.
## Assumptions (confidence)
## Acceptance criteria
- [x] a done claim while fm clauses' open list is non-empty is blocked once, naming them; the same set never blocks twice, and a stop_hook_active stop ends the turn — verify with `python3 plugin/tests/run.py test_hooks test_request`
## Non-goals
## Approach (options → choice → why)
Options: (a) a new _clauses_gate in the stop() nudge chain after _evidence_gate; (b) fold it into _claims_gate; (c) only extend the drive message. Chosen (a): the same shape as _evidence_gate (keyed once in the gate file, logs a stop_gate event), one function, and the chain keeps the evidence gate first. (b) mixes two keys; (c) never blocks a done claim.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first: clauses.open + claims_done → one block naming them; no-progress and DRIVE_MAX still end it
2. [x] docs (MASTER Stop, CHANGELOG)
## Resume here
<!-- auto -->
- 2026-10-30T10:44:08Z steps 2/2 done
- git: foreman/build; 4 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmhooks.py, plugin/tests/test_hooks.py
- touched since last checkpoint: /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/t2138-test.edit, plugin/tests/test_hooks.py, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/t2138-impl.edit, plugin/lib/fmhooks.py, CHANGELOG.md, MASTER.md
## Docs impact
MASTER.md: Stop hook section gains 'Unaccounted clauses (T-2138)'. CHANGELOG.md: one Unreleased line. No README or site change: an internal Stop guard.
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_hooks test_request` → exit 0 · Ran 212 tests in 31.0s (32 classes, 16 at a time; slowest: Stop 31s, NoTaskGate 23s, PreToolUse 18s) / OK [ran] [tree 5b54d503403a] (2026-10-30T10:42:22Z)
- (step 2) `fm docs` → exit 0 · No doc drift in ~/.claude/foreman. [ran] [tree 3b2ffae07f8b] (2026-10-30T10:42:31Z)
- (step 1) `python3 plugin/tests/run.py test_hooks test_request` → exit 0 · Ran 213 tests in 31.4s (32 classes, 16 at a time; slowest: Stop 31s, NoTaskGate 23s, PreToolUse 18s) / OK [ran] [tree f93796b54107] (2026-10-30T10:47:32Z)
- (step 2) `fm docs` → exit 0 · No doc drift in ~/.claude/foreman. [ran] [tree f93796b54107] (2026-10-30T10:47:32Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks test_request` → exit 0 · Ran 213 tests in 31.3s (32 classes, 16 at a time; slowest: Stop 31s, NoTaskGate 23s, PreToolUse 18s) / OK [ran] [tree f93796b54107] (2026-10-30T10:48:15Z)
- (audit intent) `one fm-reviewer pass over the diff (five lenses), 5 findings verified: 4 fixed test-first, 1 decided (day window kept)` → fires only after fm clauses; day window decided over turn start; CHANGELOG reworded; auto-run captured T-2146 [tree f93796b54107] (2026-10-30T10:48:15Z)
- (audit adversary) `one fm-reviewer pass over the diff (five lenses), 5 findings verified: 4 fixed test-first, 1 decided (day window kept)` → sha1 is a dedupe key only, clause text c.plain'd and fit to 80; no exec, no secrets [tree f93796b54107] (2026-10-30T10:48:15Z)
- (audit edge) `one fm-reviewer pass over the diff (five lenses), 5 findings verified: 4 fixed test-first, 1 decided (day window kept)` → undated/corrupt at counts as stale; same set never holds twice across sessions; 6 clauses name 5; tested [tree f93796b54107] (2026-10-30T10:48:15Z)
- (audit maintainer) `one fm-reviewer pass over the diff (five lenses), 5 findings verified: 4 fixed test-first, 1 decided (day window kept)` → one test covers stale, undated, cap and other session [tree f93796b54107] (2026-10-30T10:48:15Z)
- (audit operator) `one fm-reviewer pass over the diff (five lenses), 5 findings verified: 4 fixed test-first, 1 decided (day window kept)` → runs after the evidence gate, never on stop_hook_active, logs stop_gate; held sets capped at 50 [tree f93796b54107] (2026-10-30T10:48:15Z)
## Log
- 2026-10-30T10:37:52Z created
- 2026-10-30T10:40:55Z criterion 1 verify: `python3 plugin/tests/run.py test_hooks_stop test_clauses` → `python3 plugin/tests/run.py test_hooks test_request`
- 2026-10-30T10:40:55Z criterion 1 text: a done claim with fm clauses' open list non-empty is blocked once naming them; a second stop with no progress ends the turn → a done claim while fm clauses' open list is non-empty is blocked once, naming them; the same set never blocks twice, and a stop_hook_active stop ends the turn
- 2026-10-30T10:40:59Z focused
- 2026-10-30T10:47:01Z scope: MASTER.md and CHANGELOG.md for the docs; plugin/tests/test_hooks.py for the Stop tests
- 2026-10-30T10:48:51Z done
- 2026-10-30T10:48:52Z committed 70cdbe01 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-2104-review: Verdict: changes needed.** One HIGH finding makes sweep red for good once its Mission tasks are archived. A MEDIUM finding makes a cold read that…
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- T-1810 [FEATURE M, done, 4 steps] Session start sweeps for problems nobody raised: CI on main, a changed model/window/CC (cost math redone), a stale blocked pile, overdu…
- decision 2026-10-30: [revisit: when plugin/lib/fmmandate.py changes @468614546a50] Mission 4: the goal ledger grows fm mandate (one standing goal per project: text, clau…
## Lessons
- A freshness check on a stored timestamp must treat a missing or unparsable stamp as stale; 'or 0' quietly fails open.
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
- MASTER.md
