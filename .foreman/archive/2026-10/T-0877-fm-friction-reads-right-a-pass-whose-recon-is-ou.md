---
id: T-0877
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-15T14:43:12Z
updated: 2026-10-15T14:46:32Z
batch: [T-0858, T-0860]
base: eff4058813c4860444246a8d23feade0c274607d
base_tree: 2e663aba1f3ca1cdac25d2735ec0a9098ee1380c
verified: strong
---
# fm friction reads right: a pass whose recon is out isn't 'due' again, and once-per-file tripwire notes aren't 'repeated…
## Raw request
> T-0858: Stop-hook drive repeats 'self-improvement pass due' while the pass's recon subagent is still running: a pass whose brief was written and whose recon is out counts as in progress
> T-0860: fm friction counts once-per-file tripwire notes (each a different task's lesson) as 'repeated notes': count distinct notes, not the note kind
## Interpretation
Do T-0858, T-0860 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-0877. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-0858: Stop-hook drive repeats 'self-improvement pass due' while the pass's recon subagent is sti works — verify with `python3 plugin/tests/run.py test_friction`
- [x] T-0860: Fm friction counts once-per-file tripwire notes (each a different task's lesson) as 'repea works — verify with `python3 plugin/tests/run.py test_friction`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-0858: Stop-hook drive repeats 'self-improvement pass due' while the pass's recon subagent is sti
2. [x] T-0860: Fm friction counts once-per-file tripwire notes (each a different task's lesson) as 'repea
## Resume here
## Docs impact
none: internal
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_friction` → exit 0 · Ran 11 tests in 4.4s (2 classes, 16 at a time; slowest: Friction 4s, Mining 0s) / OK [ran] [tree d0dfb2c55506] (2026-10-15T14:44:20Z)
- (step 2) `python3 plugin/tests/run.py test_friction` → exit 0 · Ran 11 tests in 4.6s (2 classes, 16 at a time; slowest: Friction 4s, Mining 0s) / OK [ran] [tree d0dfb2c55506] (2026-10-15T14:44:25Z)
- `python3 plugin/tests/run.py test_friction` → ✗ exit 1 · Ran 11 tests in 4.6s (2 classes, 16 at a time; slowest: Friction 4s, Mining 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree d0dfb2c55506] (2026-10-15T14:44:34Z)
- `python3 plugin/tests/run.py test_friction` → exit 0 · Ran 11 tests in 4.4s (2 classes, 16 at a time; slowest: Friction 4s, Mining 0s) / OK [ran] [tree d0dfb2c55506] (2026-10-15T14:44:34Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmfriction.py, plugin/lib/fmhooks.py — commit it through a task, or git checkout it back / fm doctor: OK (35 pass, 4 ; python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                33.4    34.3     150  [0] / SessionEnd                  30.6    33.8     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under [ran] [tree d0dfb2c55506] (2026-10-15T14:46:12Z)
- (ac 1) `python3 plugin/tests/run.py test_friction` → exit 0 · Ran 11 tests in 4.3s (2 classes, 16 at a time; slowest: Friction 4s, Mining 0s) / OK [ran] [tree d0dfb2c55506] (2026-10-15T14:46:26Z)
- (ac 2) `python3 plugin/tests/run.py test_friction` → exit 0 · Ran 11 tests in 4.3s (2 classes, 16 at a time; slowest: Friction 4s, Mining 0s) / OK [ran] [tree d0dfb2c55506] (2026-10-15T14:46:26Z)
- (audit edge) `self: --brief records rsi_brief_at, and due() stays quiet while that brief is newer than the last --mark and under the 2-hour gap (the recon is out); inject events carry a short hash of the note, and 'repeated 3+' counts the same note word for word, so a kind of note about many files (tripwires) no longer reads as one repeated note; old events without the hash count as before` → a brief never followed by --mark stops blocking after 2 hours, so a forgotten pass comes due again; hashing adds one sha1 per injected note (only when a note is shown), bench within SLO [tree d0dfb2c55506] (2026-10-15T14:46:26Z)
- (audit self) `self: --brief records rsi_brief_at, and due() stays quiet while that brief is newer than the last --mark and under the 2-hour gap (the recon is out); inject events carry a short hash of the note, and 'repeated 3+' counts the same note word for word, so a kind of note about many files (tripwires) no longer reads as one repeated note; old events without the hash count as before` → no findings [tree d0dfb2c55506] (2026-10-15T14:46:26Z)
- (audit edge) `self: --brief records rsi_brief_at, and due() stays quiet while that brief is newer than the last --mark and under the 2-hour gap (the recon is out); inject events carry a short hash of the note, and 'repeated 3+' counts the same note word for word; old events without the hash count as before` → a brief never followed by --mark stops blocking after 2 hours, so a forgotten pass comes due again; one sha1 per injected note, bench within SLO [tree d0dfb2c55506] (2026-10-15T14:46:32Z)
- (audit adversary) `self: --brief records rsi_brief_at, and due() stays quiet while that brief is newer than the last --mark and under the 2-hour gap (the recon is out); inject events carry a short hash of the note, and 'repeated 3+' counts the same note word for word; old events without the hash count as before` → the sha1 is a 10-hex fingerprint of note text Foreman itself wrote, used only to group identical notes in a local digest; no secret is hashed for protection and nothing trusts it for integrity, so collisions only merge two notes' counts [tree d0dfb2c55506] (2026-10-15T14:46:32Z)
- (audit self) `self: --brief records rsi_brief_at, and due() stays quiet while that brief is newer than the last --mark and under the 2-hour gap (the recon is out); inject events carry a short hash of the note, and 'repeated 3+' counts the same note word for word; old events without the hash count as before` → no findings [tree d0dfb2c55506] (2026-10-15T14:46:32Z)
## Log
- 2026-10-15T14:43:12Z created
- 2026-10-15T14:43:35Z focused
- 2026-10-15T14:44:15Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_friction`
- 2026-10-15T14:44:20Z criterion 2 verify: `` → `python3 plugin/tests/run.py test_friction`
- 2026-10-15T14:46:32Z done
- 2026-10-15T14:46:32Z committed cdde03b (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0676 [FEATURE M, done, 7 steps] Milestone: Features — Performance and cost — lesson: A 'degrade when over pace' rule must name what is optional: side offers and self-i…
- T-0674 [FEATURE M, done, 3 steps] Milestone: Features — Observability, replay and trust — lesson: Check where secrets enter before adding redaction: every write path her…
- T-0671 [FEATURE M, done, 3 steps] Milestone: Features — Autonomy and the user — lesson: A guard-word filter on free text needs the verbs people actually use (push, delet…
- decision 2026-10-03: Self-improvement passes need N closed tasks AND 2 h since the last pass
- similar past tasks were M: consider --tier M
- similar finished tasks took 3–7 steps
## Why not caught
none: found by the friction pass itself and by the drive looping on it
## Lessons
- A 'due' signal must know about work already in flight, or it nags the agent doing it
## Files touched
- plugin/tests/test_friction.py
- plugin/lib/fmfriction.py
- plugin/lib/fmhooks.py
