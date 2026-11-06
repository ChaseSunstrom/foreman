---
id: T-2186
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T16:40:20Z
updated: 2026-10-30T17:55:48Z
base: 90ebd1cd52fe2b2d1a4540a6672f6175c4148d08
base_tree: 76ab05df3f56edecfc859d94f474cea80b040be9
plan0_at: 2026-10-30T17:39:33Z
plan0_scope: []
verified: strong
---
# Wire the four verbs gen-1's missions name that no session path calls (fm genesis check's…
## Raw request
> FIX: wire the four verbs gen-1's missions name that no session path calls (fm genesis check's reach: fm mandate, fm outcomes, fm docs, fm adopt) into the rules, a skill or a hook note, or drop them from the missions; note the check reads text, so a verb a hook runs as Python (fmfind.precision calls fmoutcomes) still needs its name on the path (steer 2026-10-30 #3)
## Interpretation
fm genesis check's reach names fm mandate, fm outcomes, fm docs and fm adopt as named by gen-1's missions with no session path. Two are false gaps: fm find (on the rules and the session-start leads) runs fmoutcomes and fmdocs, but reach only reads text, so it measures wording, not use. Two are true gaps: fm adopt (map, gates with a flake rerun, secrets, hot untested files, queued) is what a session should run first in a repo Foreman hasn't worked in, and nothing says so; fm mandate (a sweeping request kept standing, read by scout and night) is never shown to a session or named where sweeping requests are handled.
## Assumptions (confidence)
## Acceptance criteria
- [x] reach counts a verb whose module a reached verb's module imports; fm adopt and fm mandate are named on session paths; fm genesis check's reach is clean on the live tower — verify with `python3 plugin/tests/run.py test_genesis test_hooks test_core`
- [x] live: fm genesis check's reach line is ✓ (its exit stays 1 until gen-1's Missions fill the 1247 empty coverage cells) — verify with `sh -c 'fm genesis check | grep -F "✓ reach"'`
## Non-goals
## Approach (options → choice → why)
Options: (a) reach counts a verb reached when a session path names it or the module of a reached verb imports its module (one level, read with ast), and the two true gaps are wired: fm adopt into fm next's not-worked-in line and the leads pointer, the mandate shown at session start while it stands and named in the brainstorm skill for sweeping requests (chosen); (b) tag session-facing verbs in the missions (rejected: a format check); (c) drop the verbs from the missions (rejected: the frame never shrinks); (d) a full call graph (rejected: one import level covers the cases and stays readable).
## Risks and rollback
One import level can count a verb reached that a session only reaches through a rarely-taken branch; the reach line still names it when nothing imports it. Rollback: revert the commit.
## Execution prompt
## Steps
1. [x] red tests: import-level reach, fm next names fm adopt in a new repo, session start shows a standing mandate
2. [x] implement reach imports, fm next/leads pointer, session-start mandate line, brainstorm skill line
3. [x] live fm genesis check, fm check, docs, audit, finish
## Resume here
## Docs impact
~/.claude/foreman/MASTER.md ~/.claude/foreman/CHANGELOG.md ~/.claude/foreman/plugin/skills/brainstorm/SKILL.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_genesis test_hooks` → ✗ exit 1 · Ran 302 tests in 62.6s (41 classes, 16 at a time; slowest: Stop 62s, NoTaskGate 44s, PreToolUse 39s) / FAILED (2 classes) [ran] [tree 54e33eb0be15] (2026-10-30T17:41:44Z)
- (step 2) `python3 plugin/tests/run.py test_genesis test_hooks test_core` → ✗ exit 1 · Ran 393 tests in 35.1s (63 classes, 16 at a time; slowest: Stop 35s, NoTaskGate 26s, PreToolUse 21s) / FAILED (1 classes) [ran] [tree 9321091c9207] (2026-10-30T17:43:35Z)
- (step 2) `python3 plugin/tests/run.py test_genesis test_hooks test_core` → exit 0 · Ran 393 tests in 35.2s (63 classes, 16 at a time; slowest: Stop 35s, NoTaskGate 26s, PreToolUse 21s) / OK [ran] [tree 5401851e483b] (2026-10-30T17:44:35Z)
- (step 3) `fm genesis check` → ✗ exit 1 · ✓ not-yet: 0 items / ✓ reach: 27 fm verb(s) the missions name, each on a session path [ran] [tree 5401851e483b] (2026-10-30T17:44:42Z)
- (ac 2) `sh -c 'fm genesis check | grep -F "✓ reach"'` → exit 0 · ✓ reach: 27 fm verb(s) the missions name, each on a session path [ran] [tree 5401851e483b] (2026-10-30T17:45:01Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmgenesis.py, plugin/lib/fmhooks.py — commit it through a task, or git che; python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                29.0    30.3     150  [0] / SessionEnd                  23.8    24.6     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under [ran] [tree 2fe3b39e7f38] (2026-10-30T17:49:02Z)
- (step 2) `python3 plugin/tests/run.py test_genesis test_hooks test_core` → exit 0 · Ran 393 tests in 35.1s (63 classes, 16 at a time; slowest: Stop 35s, NoTaskGate 25s, PreToolUse 21s) / OK [ran] [tree 681c30d2b114] (2026-10-30T17:49:46Z)
- `python3 plugin/tests/run.py test_genesis test_hooks` → ✗ exit 1 · Ran 302 tests in 35.6s (41 classes, 16 at a time; slowest: Stop 35s, NoTaskGate 25s, PreToolUse 20s) / FAILED (2 classes) (start tree + this task's tests) [ran] [tree e595737ad29e] (2026-10-30T17:51:04Z)
- `python3 plugin/tests/run.py test_genesis test_hooks` → exit 0 · Ran 302 tests in 34.8s (41 classes, 16 at a time; slowest: Stop 35s, NoTaskGate 25s, PreToolUse 20s) / OK [ran] [tree e595737ad29e] (2026-10-30T17:51:04Z)
- (audit intent) `foreman:fm-reviewer` → changes needed -> fixed: mandate end only as the user named it; import-as-use kept with a ponytail ceiling comment [tree e595737ad29e] (2026-10-30T17:51:20Z)
- (audit edge) `foreman:fm-reviewer` → fm adopt hint only in a repo new to Foreman, tested both ways [tree e595737ad29e] (2026-10-30T17:51:20Z)
- (audit adversary) `foreman:fm-reviewer` → an ended mandate is the user's call to renew, never the session's; mandate text labelled recorded data [tree e595737ad29e] (2026-10-30T17:51:20Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis test_hooks test_core` → exit 0 · Ran 393 tests in 35.5s (63 classes, 16 at a time; slowest: Stop 35s, NoTaskGate 26s, PreToolUse 21s) / OK [ran] [tree e595737ad29e] (2026-10-30T17:52:06Z)
- (ac 2) `sh -c 'fm genesis check | grep -F "✓ reach"'` → exit 0 · ✓ reach: 27 fm verb(s) the missions name, each on a session path [ran] [tree e595737ad29e] (2026-10-30T17:52:06Z)
- (audit intent) `one foreman:fm-reviewer pass (five lenses); 3 MEDIUM + 4 LOW: 5 fixed test-first, import-as-use kept with a ponytail ceiling` → reach measures use one import level deep; fm adopt and fm mandate are on session paths; live reach ✓ 27/27 [tree e595737ad29e] (2026-10-30T17:52:06Z)
- (audit edge) `one foreman:fm-reviewer pass (five lenses); 3 MEDIUM + 4 LOW: 5 fixed test-first, import-as-use kept with a ponytail ceiling` → the adopt hint only where Foreman hasn't worked; unreadable or missing modules import nothing [tree e595737ad29e] (2026-10-30T17:52:06Z)
- (audit adversary) `one foreman:fm-reviewer pass (five lenses); 3 MEDIUM + 4 LOW: 5 fixed test-first, import-as-use kept with a ponytail ceiling` → a session never renews an ended mandate; mandate text is quoted recorded data [tree e595737ad29e] (2026-10-30T17:52:06Z)
## Log
- 2026-10-30T16:40:20Z created
- 2026-10-30T17:08:53Z planned: it has criteria and steps
- 2026-10-30T17:39:32Z focused
- 2026-10-30T17:45:00Z criterion 2 verify: `fm genesis check` → `sh -c 'fm genesis check | grep -F "✓ reach"'`
- 2026-10-30T17:45:00Z criterion 2 text: live: fm genesis check shows ✓ reach → live: fm genesis check's reach line is ✓ (its exit stays 1 until gen-1's Missions fill the 1247 empty coverage cells)
- 2026-10-30T17:53:01Z done
- 2026-10-30T17:53:03Z committed 9d2f5423 (9 files)
- 2026-10-30T17:53:12Z guard authorization added: publish
- 2026-10-30T17:55:48Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-2184-review: Verdict: changes needed.** Two MEDIUM defects, plus acceptance criteria 4 and 5 still open. [stale: plugin/lib/fmgenesis.py, plugin/lib/fmhooks.p…
- T-2184 [FEATURE M, done, 5 steps] Foreman sessions use fm find by default (steer 2026-10-30 #3): the exam shows a Foreman… — lesson: a capability the session never hears…
- T-2124 [FEATURE M, done, 2 steps] Scout project probes: fm find + prove on the user's own project, at most 3 a day, proven only, refutation ledger, doctor faults to the …
- decision 2026-10-30: [revisited: every capability genesis builds must be called] [cites: the user's steer 2026-10-30 (third): fm find unused by sessions] [check: python3…
## Why not caught
T-2184's reach test only checked a named verb against session text; no case had a verb run through another verb's module
## Lessons
- A reach check that reads words fails both ways: it flags capabilities a session runs through another verb's code and passes ones only named; measure what runs (imports one level), and wire the true gaps where the session already looks (fm next, session start)
## Plan gaps
- failed first: step 1 red tests: import-level reach, fm next names fm adopt in a new repo, session start shows a standing…
- failed first: step 2 implement reach imports, fm next/leads pointer, session-start mandate line, brainstorm skill line
- failed first: step 3 live fm genesis check, fm check, docs, audit, finish
## Files touched
- plugin/tests/test_genesis.py
- plugin/tests/test_hooks.py
- plugin/lib/fmcli.py
- plugin/lib/fmcore.py
- plugin/lib/fmgenesis.py
- plugin/lib/fmhooks.py
- plugin/skills/brainstorm/SKILL.md
- CHANGELOG.md
- MASTER.md
