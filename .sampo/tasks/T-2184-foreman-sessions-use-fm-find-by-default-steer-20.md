---
id: T-2184
type: FEATURE
tier: M
status: done
priority: urgent
scope: []
depends_on: []
source: user
created: 2026-10-30T16:22:42Z
updated: 2026-10-30T17:03:48Z
base: dcfcea290b45b47ea27a6e796e0439a4ce024611
base_tree: 6d0a174f0f00ad58dc26ad227e62f4a4357a537a
plan0_at: 2026-10-30T16:29:23Z
plan0_scope: []
verified: strong
---
# Foreman sessions use fm find by default (steer 2026-10-30 #3): the exam shows a Foreman…
## Raw request
> FEATURE!: Foreman sessions use fm find by default (steer 2026-10-30 #3): the exam shows a Foreman session finds 6/18 where fm find alone finds 16/18 on the same held-out scenarios. Wire fm find (and fm find prove once T-2122 lands) into what a session does in an unfamiliar repo or with no request, so the foreman arm uses it by default; re-run the Haiku smoke arms on those 9 scenarios to confirm. Standing rules with checks (fm decide --cites user steer --check): every capability Genesis builds must be called by a real session path; a capability whose free arm beats the session arm is a top gap
## Interpretation
Steer 2026-10-30 #3. On held-out run s31-006 the foreman arm found 6/18, the same as plain Claude, while fm find alone (the free finders arm) found 16/18: nothing a session reads mentions fm find (no rule, skill, hook note or fm next line), and fmscout's probe_find refuses a repo whose commits aren't the user's, so an exam repo never sees it. Wire it into the session paths an unfamiliar repo or a no-request run actually takes: session start with nothing active or queued gets fm find's ranked leads as quoted data (bounded scan), fm next with an empty queue in a repo with no task history says fm find --rank, and the operating rules say so; fm find prove joins when T-2122 lands. Then rerun the Haiku smoke foreman arm on s31-006's 9 held-out scenarios (smoke only: it confirms, never decides). The two standing rules get checks here: fm genesis check names a verb a mission's DONE-WHEN promises that no session path names; the scorecard and the next seed put a capability whose free arm beats the session arm first.
## Assumptions (confidence)
## Acceptance criteria
- [x] session start (startup or clear) with nothing active or queued puts fm find's ranked leads (at most 8, each row a JSON string of repo text, a candidate to prove red first) into the context, in an unattended run or an interactive one in a repo Foreman hasn't worked in, inside the hook's time budget (a 1.5 s scan deadline); a tree past 400 listed files gets a pointer instead of a scan — verify with `python3 plugin/tests/run.py test_hooks`
- [x] fm next with an empty queue in a repo with no closed task names fm find --rank, and the operating rules say an unfamiliar repo or no request starts there — verify with `python3 plugin/tests/run.py test_hooks test_docs`
- [x] fm genesis check (its exit code and the sweep's row) names an fm verb a mission names that no session path (rules, skills, commands, the strings hooks and fm next print) names; fm exam scorecard and the next seed put a capability whose free arm beats the session arm first — verify with `python3 plugin/tests/run.py test_genesis`
- [x] the Haiku smoke foreman arm reruns on s31-006's 9 held-out scenarios with the wiring and its line is graded (smoke only, never a decision): 10/18 found vs 6/18 before, 3 false alarms vs 7; the finders' 16/18 stays a top gap — verify with `fm exam`
- [x] both standing rules from steer 3 carry passing checks (no longer pending T-2184) — verify with `fm doctor --full -v`
## Non-goals
## Approach (options → choice → why)
Complete version: leads at session start (headless and interactive, nothing active or queued; capped scan, ≤ 8 leads, c.plain'd and fenced as data, a note that each is a candidate to prove red first), fm next's empty-queue line in a repo with no closed task, a rules line, the exam arm picking it up through session start, a reach check in fm genesis check, a free-beats-session line in fm exam scorecard and seed(), MASTER/README/CHANGELOG, the Haiku smoke rerun. Options: (a) only a rules line: rejected, a line the model may skip is how 6/18 happened; (b) the hook injects leads it computes: chosen, the session sees them without choosing to run anything; (c) fm next says run fm find: kept as the second path for interactive sessions with an empty queue; (d) make probe_find file tasks in any repo: rejected, filing work in a clone the user doesn't own breaks T-2124's consent rule. Scan cost: synchronous only up to a tracked-file cap measured on Foreman's own tree, else skipped with a pointer to fm find --rank.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests: session-start leads (headless, interactive, big tree), fm next's empty-queue line, the reach check, free-beats-session in scorecard and seed
2. [x] implement the leads note, fm next's line and the rules line
3. [x] implement the reach check and the free-beats-session ordering
4. [x] Haiku smoke rerun of the foreman arm on s31-006's held-out 9, graded
5. [x] steer 3 rules get their checks (fm decide --revisited --check); docs: MASTER, README, CHANGELOG
## Resume here
## Docs impact
MASTER.md (fmfind, fmgenesis check/scorecard/seed), README.md (finder row), CHANGELOG.md, plugin/rules/foreman.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_hooks.SessionStart test_genesis.GenesisCheck test_genesis.GenesisSelect` → red as expected (exit 1) · Ran 35 tests in 11.1s (3 classes, 16 at a time; slowest: SessionStart 11s, GenesisCheck 3s, GenesisSelect 1s) / FAILED (3 classes) [ran] [tree c9b990b4000b] (2026-10-30T16:33:15Z)
- (step 2) `python3 plugin/tests/run.py test_hooks test_loop test_cli` → exit 0 · Ran 369 tests in 36.7s (70 classes, 16 at a time; slowest: Stop 36s, NoTaskGate 27s, PreToolUse 22s) / OK [ran] [tree 125e927c6435] (2026-10-30T16:38:29Z)
- (step 3) `python3 plugin/tests/run.py test_genesis test_exam test_core test_docs` → ✗ exit 1 · Ran 284 tests in 20.0s (67 classes, 16 at a time; slowest: ExamGen 20s, ExamAuthors 13s, ExamRust 12s) / FAILED (1 classes) [ran] [tree 125e927c6435] (2026-10-30T16:38:50Z)
- (step 3) `python3 plugin/tests/run.py test_genesis test_exam test_core test_docs` → exit 0 · Ran 284 tests in 20.0s (67 classes, 16 at a time; slowest: ExamGen 20s, ExamAuthors 13s, ExamRust 12s) / OK [ran] [tree 45e72d0c866d] (2026-10-30T16:40:05Z)
- (step 3) `python3 plugin/tests/run.py test_hooks.SessionStart test_genesis.GenesisCheck test_genesis.GenesisSweep` → red as expected (exit 1) · Ran 35 tests in 11.4s (3 classes, 16 at a time; slowest: SessionStart 11s, GenesisSweep 4s, GenesisCheck 4s) / FAILED (2 classes) [ran] [tree 76c153c95eea] (2026-10-30T16:46:44Z)
- (step 3) `python3 plugin/tests/run.py test_hooks test_genesis test_exam test_core test_docs test_loop test_cli` → exit 0 · Ran 648 tests in 47.6s (131 classes, 16 at a time; slowest: Stop 47s, NoTaskGate 37s, PreToolUse 33s) / OK [ran] [tree 0d7d0b252b03] (2026-10-30T16:49:00Z)
- (audit intent) `foreman:fm-reviewer (T-2184-review)` → leads now quoted (JSON rows, shortened paths); interactive-only-when-unfamiliar and whole-mission reach are stated in the criteria; steps 4-5 close with the smoke line and the doctor run [tree dc145e06023e] (2026-10-30T16:49:47Z)
- (audit edge) `foreman:fm-reviewer (T-2184-review)` → cap now counts fm find's own listing (tracked plus untracked); a 1.5 s daemon-thread deadline returns a pointer; startup/clear only; tests cover each [tree dc145e06023e] (2026-10-30T16:49:48Z)
- (audit adversary) `foreman:fm-reviewer (T-2184-review)` → repo-controlled paths enter context only as JSON strings under a data label; the listing runs git with fsmonitor and hooks off; fm find never runs repo code [tree dc145e06023e] (2026-10-30T16:49:48Z)
- (audit operator) `foreman:fm-reviewer (T-2184-review)` → ~400 tokens once per idle startup; scan bounded at 1.5 s; fm genesis check adds a parser build (fm only, never a hook) [tree dc145e06023e] (2026-10-30T16:49:48Z)
- (audit maintainer) `foreman:fm-reviewer (T-2184-review)` → reach reads string literals only (ast, docstrings skipped); exit-code and sweep-row tests added; blank lines tidied [tree dc145e06023e] (2026-10-30T16:49:48Z)
- (step 5) `fm doctor --full -v` → ✗ exit 1 · PASS  upstream issues      no error seen twice in 7 days matches the 4 known Claude Code issue(s) / fm doctor: FAILED (47 pass, 7 warn, 1 fail) [ran] [tree dc145e06023e] (2026-10-30T16:51:03Z)
- (step 4) `fm exam` → exit 0 · finders s0-001: 90/108 found, 0 false alarms, 0/108 fixed, 0/54 test-first, 0/18 readings, 0/9 missing tools named, held out 30/36 found / foreman s31-006: 10/18 found, 3 false alarms, 17/18 fixed, 5/ [ran] [tree 056f656c5c33] (2026-10-30T16:52:39Z)
- (step 5) `fm doctor --full -v` → exit 0 · PASS  upstream issues      no error seen twice in 7 days matches the 4 known Claude Code issue(s) / fm doctor: OK (48 pass, 7 warn, 0 fail) [ran] [tree 056f656c5c33] (2026-10-30T16:54:06Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 213 tests in 32.4s (28 classes, 16 at a time; slowest: Stop 32s, NoTaskGate 23s, PreToolUse 18s) / OK [ran] [tree 056f656c5c33] (2026-10-30T16:56:12Z)
- (ac 2) `python3 plugin/tests/run.py test_hooks test_docs` → exit 0 · Ran 292 tests in 32.7s (48 classes, 16 at a time; slowest: Stop 32s, NoTaskGate 23s, PreToolUse 18s) / OK [ran] [tree 056f656c5c33] (2026-10-30T16:56:12Z)
- (ac 3) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 87 tests in 4.4s (13 classes, 16 at a time; slowest: GenesisSweep 4s, GenesisLive 4s, GenesisCheck 4s) / OK [ran] [tree 056f656c5c33] (2026-10-30T16:56:12Z)
- (ac 4) `fm exam` → exit 0 · finders s0-001: 90/108 found, 0 false alarms, 0/108 fixed, 0/54 test-first, 0/18 readings, 0/9 missing tools named, held out 30/36 found / foreman s31-006: 10/18 found, 3 false alarms, 17/18 fixed, 5/ [ran] [tree 056f656c5c33] (2026-10-30T16:56:12Z)
- (ac 5) `fm doctor --full -v` → exit 0 · PASS  upstream issues      no error seen twice in 7 days matches the 4 known Claude Code issue(s) / fm doctor: OK (48 pass, 7 warn, 0 fail) [ran] [tree 056f656c5c33] (2026-10-30T16:56:12Z)
- (audit intent) `one fm-reviewer pass over five lenses; 5 findings fixed test-first, 1 kept by decision (whole-mission reach, criterion reworded)` → a session with nothing to do now starts from fm find's leads (headless, or interactive in a new repo), fm next and the rules point there, the reach check and the free-beats-session gap are in check, scorecard and seed; Haiku smoke 6/18 → 10/18 found on s31-006 held out, finders' 16/18 still the top gap (T-2192) [tree 056f656c5c33] (2026-10-30T16:56:12Z)
- (audit edge) `one fm-reviewer pass over five lenses; 5 findings fixed test-first, 1 kept by decision (whole-mission reach, criterion reworded)` → the cap counts fm find's own listing, a 1.5 s deadline returns a pointer, startup and clear only; a big or slow tree never holds session start [tree 056f656c5c33] (2026-10-30T16:56:12Z)
- (audit adversary) `one fm-reviewer pass over five lenses; 5 findings fixed test-first, 1 kept by decision (whole-mission reach, criterion reworded)` → repo paths enter context only as JSON strings under a data label; the listing runs git with fsmonitor and hooks off; fm find never runs repo code [tree 056f656c5c33] (2026-10-30T16:56:12Z)
## Log
- 2026-10-30T16:22:42Z created
- 2026-10-30T16:24:27Z steer recorded as two standing rules (decisions.md, check pending T-2184): every Genesis capability called by a real session path; a free arm beating the session arm is a top gap
- 2026-10-30T16:27:03Z set tier=M, priority=urgent
- 2026-10-30T16:27:57Z planned: it has criteria and steps
- 2026-10-30T16:29:23Z focused
- 2026-10-30T16:35:46Z steer 4 (detection ladder for #1) captured as T-2185 with two standing rules pending on it; T-2184 keeps to wiring fm find into session paths
- 2026-10-30T16:49:41Z criterion 1 text: session start with nothing active or queued puts fm find's ranked leads (at most 8, quoted as data, each a candidate to prove red first) into the context, headless and interactive, inside the hook's time budget; a big tree gets a pointer instead of a scan → session start (startup or clear) with nothing active or queued puts fm find's ranked leads (at most 8, each row a JSON string of repo text, a candidate to prove red first) into the context, in an unattended run or an interactive one in a repo Foreman hasn't worked in, inside the hook's time budget (a 1.5 s scan deadline); a tree past 400 listed files gets a pointer instead of a scan
- 2026-10-30T16:49:41Z criterion 3 text: fm genesis check names an fm verb a mission's DONE-WHEN promises that no session path (rules, skills, commands, hook notes, fm next) names; fm genesis scorecard and the next seed put a capability whose free arm beats the session arm first → fm genesis check (its exit code and the sweep's row) names an fm verb a mission names that no session path (rules, skills, commands, the strings hooks and fm next print) names; fm exam scorecard and the next seed put a capability whose free arm beats the session arm first
- 2026-10-30T16:52:39Z criterion 4 verify: `fm exam scorecard` → `fm exam`
- 2026-10-30T16:52:39Z criterion 4 text: the Haiku smoke foreman arm reruns on s31-006's 9 held-out scenarios with the wiring and its line is graded (smoke only, never a decision) → the Haiku smoke foreman arm reruns on s31-006's 9 held-out scenarios with the wiring and its line is graded (smoke only, never a decision): 10/18 found vs 6/18 before, 3 false alarms vs 7; the finders' 16/18 stays a top gap
- 2026-10-30T16:57:11Z done
- 2026-10-30T16:57:13Z committed 46e8661e (15 files)
- 2026-10-30T16:58:41Z guard authorization added: publish
- 2026-10-30T17:03:48Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2102 [FEATURE M, done, 5 steps] fm genesis select/seed — exam-gated selection into lineage.md; the feature writes the… — lesson: c.lock is not reentrant: a lock around…
- research draft-mission-genesis-gen1: Task: T-2093 (brief 1, fm genesis check), T-2095 (brief 2, fm genesis step), T-2099 (brief 3, fm genesis draft/spec), T-2102 (brief …
- T-2112 [FEATURE M, done, 4 steps] fm genesis exam: #13's held-out exam (draft kinds graded by cover; G-tower as a genesis session arm) — lesson: Score an arm both strict…
- decision 2026-10-30: [cites: the user's steer 2026-10-30 (third): fm find unused by sessions] [check: pending T-2184] Standing rule: every capability Genesis builds must…
## Lessons
- a capability the session never hears of scores like none: wire each built verb into a session path (session start, fm next, the rules) and let a check read those paths' printable strings, not their comments
## Plan gaps
- failed first: step 3 implement the reach check and the free-beats-session ordering
- failed first: step 5 steer 3 rules get their checks (fm decide --revisited --check); docs: MASTER, README, CHANGELOG
## Files touched
- plugin/tests/test_genesis.py
- plugin/tests/test_hooks.py
- plugin/lib/fmcore.py
- plugin/lib/fmexam.py
- plugin/lib/fmgenesis.py
- plugin/lib/fmhooks.py
- plugin/rules/foreman.md
- plugin/evals/guard-force-push/prompt.md
- plugin/evals/guard-publish/prompt.md
- plugin/evals/intake-block/prompt.md
- plugin/evals/mid-task-capture/prompt.md
- plugin/evals/one-liner/prompt.md
- CHANGELOG.md
- MASTER.md
- README.md
