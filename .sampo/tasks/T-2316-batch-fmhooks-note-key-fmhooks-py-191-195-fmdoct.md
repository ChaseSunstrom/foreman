---
id: T-2316
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-31T10:46:05Z
updated: 2026-10-31T11:39:30Z
batch: [T-2313, T-2314, T-2315]
builder_model: sonnet
base: ca9a7811d086cd41987bbefb9935344d54de898d
base_tree: f134bbf4009e35f440f6c975a450cd041ec69f4d
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-10-31T10:46:50Z
plan0_scope: []
verified: strong
---
# Batch: fmhooks._note_key (fmhooks.py:191-195) …; fmdoctor._cached's key (fmdoctor.py ~36…; fm-builder.md:26 forbids onl…
## Raw request
> T-2313: fmhooks._note_key (fmhooks.py:191-195) replaces an apostrophe with a space, so "T-0877's lesson for this file" keys as "s lesson for this file" in the friction digest and can merge unrelated notes: strip 's before the punctuation pass; test _note_key on that note
> T-2314: fmdoctor._cached's key (fmdoctor.py ~369) holds the inputs' stats and the day but not the check's own code, so an edited check returns its stale cached result until tomorrow (someone tried rm state/doctor-cache.json): add fmdoctor's file mtime_ns to the key; test a patched stamp recomputes
> T-2315: fm-builder.md:26 forbids only 'cd DIR &&' chains, but builders hit 6 refusals on 'cd plugin/tests; for ...' and passed Grep a path missing foreman/: say never cd (not &&, not ;) and 'Grep/Glob: omit path, they search your worktree'; extend test_lanes.py:556's brief assertion
## Interpretation
Do T-2313, T-2314, T-2315 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-2316. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-2313: _note_key drops 's before the punctuation pass, so "T-0877's lesson for this file: x" keys as "lesson for this file x" — verify with `python3 plugin/tests/run.py test_friction test_hooks`
- [x] T-2314: fmdoctor._cached's key includes fmdoctor.py's mtime_ns, so an edited check recomputes the same day — verify with `python3 plugin/tests/run.py test_doctor`
- [x] T-2315: fm-builder.md says never cd (not with &&, not with ;) and that Grep/Glob omit path (they search the worktree); the brief test asserts both phrases — verify with `python3 plugin/tests/run.py test_lanes test_builder`
## Non-goals
## Approach (options → choice → why)
Options: 1) three one-place fixes (regex in _note_key, a code stamp in the cache key, two sentences in the builder contract) each with its test; 2) rewrite _note_key with a tokenizer; 3) clear the doctor cache on every plugin update. Choice 1: smallest diffs at the cause; 3 misses a hand edit of a check.
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-2313: fmhooks._note_key (fmhooks.py:191-195) replaces an apostrophe with a space, so "T-0877's…
2. [x] T-2314: fmdoctor._cached's key (fmdoctor.py ~369) holds the inputs' stats and the day but not…
3. [x] T-2315: fm-builder.md:26 forbids only 'cd DIR &&' chains, but builders hit 6 refusals on 'cd…
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_agents test_audit test_away test_builder test_claude test_compact test_core test_crash_hygiene test_debug test_diagnosis test_docs test_doctor test_drive_side test_export test_foresight test_genesis test_guard_evasions test_handoff test_hooks test_judgment test_lanes test_lib_hostile test_memory test_onwrite test_roles test_session test_session_fixes test_supply_delta test_tool_taint && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 985 tests in 483.6s (227 classes, 16 at a time; slowest: Stop 480s, PreToolUse 260s, NoTaskGate 239s) / FAILED (1 classes) [ran] [tree 2980d798681b] (2026-10-31T10:58:06Z)
- (step 3) `python3 plugin/tests/run.py test_agents test_docs test_claude test_core test_roles test_judgment 2>&1 | grep -v "^\s*$" | tail -30` → exit 0 · Ran 237 tests in 31.9s (75 classes, 16 at a time; slowest: Hook 29s, Fences 25s, Followups 20s) / OK [ran] [tree 2980d798681b] (2026-10-31T11:00:34Z)
- (step 1) `python3 plugin/tests/run.py test_audit test_away test_compact test_crash_hygiene test_debug test_diagnosis test_drive_side test_export test_foresight test_genesis test_guard_evasions test_handoff test_lib_hostile test_memory test_onwrite test_session test_session_fixes test_supply_delta test_tool_taint 2>&1 | grep -v "^\s*$" | tail -30` → exit 0 · Ran 437 tests in 83.9s (99 classes, 16 at a time; slowest: GenesisCheck 63s, GenesisRead 62s, Memory 54s) / OK [ran] [tree 2980d798681b] (2026-10-31T11:02:05Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_agents test_audit test_away test_builder test_claude test_compact test_core test_crash_hygiene test_debug test_diagnosis test_docs test_doctor test_drive_side test_export test_foresight test_genesis test_guard_evasions test_handoff test_hooks test_judgment test_lanes test_lib_hostile test_memory test_onwrite test_roles test_session test_session_fixes test_supply_delta test_tool_taint && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [12.20s] [ran] [tree 2980d798681b] (2026-10-31T11:06:30Z)
- (step 1) `python3 plugin/tests/run.py test_friction test_hooks` → exit 0 · Ran 244 tests in 134.0s (34 classes, 16 at a time; slowest: Stop 133s, NoTaskGate 80s, PreToolUse 75s) / OK [ran] [tree e145b4b1415b] (2026-10-31T11:33:36Z)
- (step 2) `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 91 tests in 12.7s (30 classes, 16 at a time; slowest: ViewsRepair 11s, LockProbe 9s, Command 6s) / OK [ran] [tree e145b4b1415b] (2026-10-31T11:33:50Z)
- (step 3) `python3 plugin/tests/run.py test_lanes test_builder` → exit 0 · Ran 72 tests in 59.5s (13 classes, 16 at a time; slowest: Lanes 59s, Contract 29s, Brief 10s) / OK [ran] [tree e145b4b1415b] (2026-10-31T11:34:51Z)
- (ac 1) `python3 plugin/tests/run.py test_friction test_hooks` → exit 0 · Ran 244 tests in 103.5s (34 classes, 16 at a time; slowest: Stop 103s, NoTaskGate 79s, PreToolUse 75s) / OK [ran] [tree 0da44ea59356] (2026-10-31T11:37:25Z)
- (ac 2) `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 91 tests in 7.5s (30 classes, 16 at a time; slowest: ViewsRepair 7s, LockProbe 6s, Command 3s) / OK [ran] [tree 0da44ea59356] (2026-10-31T11:37:25Z)
- (ac 3) `python3 plugin/tests/run.py test_lanes test_builder` → exit 0 · Ran 72 tests in 27.2s (13 classes, 16 at a time; slowest: Lanes 27s, Contract 13s, Brief 5s) / OK [ran] [tree 0da44ea59356] (2026-10-31T11:37:25Z)
- (audit intent) `self-review of the merged diff: _note_key strips straight and curly 's before the punctuation pass; _cached's key gains fmdoctor.py's st_mtime_ns (0 if stat fails); fm-builder.md gains the two sentences and test_lanes asserts them in the brief; each member's failing test was written first per the builder` → digest labels read right, an edited doctor check isn't served stale, builders are told not to cd with ; and not to pass Grep a path [tree 0da44ea59356] (2026-10-31T11:37:25Z)
- (audit edge) `self-review of the merged diff: _note_key strips straight and curly 's before the punctuation pass; _cached's key gains fmdoctor.py's st_mtime_ns (0 if stat fails); fm-builder.md gains the two sentences and test_lanes asserts them in the brief; each member's failing test was written first per the builder` → 'Foreman's' also loses its 's (harmless for a key); old doctor cache entries miss once and rewrite; a stat failure keys as 0 and still caches [tree 0da44ea59356] (2026-10-31T11:37:25Z)
## Log
- 2026-10-31T10:46:05Z created
- 2026-10-31T10:46:18Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_friction test_hooks`
- 2026-10-31T10:46:18Z criterion 1 text: T-2313: fmhooks._note_key (fmhooks.py:191-195) replaces an apostrophe with a space, so "T-0877's… works → T-2313: _note_key drops 's before the punctuation pass, so "T-0877's lesson for this file: x" keys as "lesson for this file x"
- 2026-10-31T10:46:20Z criterion 2 verify: `` → `python3 plugin/tests/run.py test_doctor`
- 2026-10-31T10:46:20Z criterion 2 text: T-2314: fmdoctor._cached's key (fmdoctor.py ~369) holds the inputs' stats and the day but not… works → T-2314: fmdoctor._cached's key includes fmdoctor.py's mtime_ns, so an edited check recomputes the same day
- 2026-10-31T10:46:21Z criterion 3 verify: `` → `python3 plugin/tests/run.py test_lanes test_builder`
- 2026-10-31T10:46:21Z criterion 3 text: T-2315: fm-builder.md:26 forbids only 'cd DIR &&' chains, but builders hit 6 refusals on 'cd… works → T-2315: fm-builder.md says never cd (not with &&, not with ;) and that Grep/Glob omit path (they search the worktree); the brief test asserts both phrases
- 2026-10-31T10:46:24Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2316.builder.md
- 2026-10-31T10:46:47Z focused
- 2026-10-31T10:46:50Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-10-31T11:31:18Z merged worktree-agent-ada89abbc3c7b6b33 (6 file(s))
- 2026-10-31T11:31:18Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ada89abbc3c7b6b33
- 2026-10-31T11:31:19Z focused
- 2026-10-31T11:35:03Z scope: plugin/lib/fmhooks.py (_note_key), plugin/lib/fmdoctor.py (_code_stamp, _cached key), plugin/agents/fm-builder.md, plugin/tests/test_hooks.py, plugin/tests/test_doctor.py, plugin/tests/test_lanes.py, CHANGELOG.md
- 2026-10-31T11:39:27Z done
- 2026-10-31T11:39:30Z committed d818eeff (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1866 [FEATURE M, done, 7 steps] Backlog swipe everywhere: app view, terminal loop, pick explores, prefer --reset — lesson: A loop that applies one verdict at a time mu…
- T-2296 [FEATURE M, done, 2 steps] Batch: The friction digest's guard example is …; Fmfriction give-up lines name task ids … — lesson: A test must log through the same fu…
- T-1731 [FIX M, done, 4 steps] Lane and close friction: finish --commit and shared files, CLEAN behaviour-lock in builder briefs, check --affected ski… — lesson: Skip a t…
- decision 2026-10-30: [cites: user: read SEED_PROMPT.md] Genesis setup: autonomy full, drive on, loop on, contract off, lane max 6, mandate until 2026-11-13; T-2077 is th…
## Lessons
- A cache key must include the code that computes the value, not only its inputs
## Files touched
- plugin/tests/test_hooks.py
- plugin/tests/test_doctor.py
- plugin/tests/test_lanes.py
- plugin/lib/fmhooks.py
- plugin/lib/fmdoctor.py
- plugin/agents/fm-builder.md
- CHANGELOG.md
