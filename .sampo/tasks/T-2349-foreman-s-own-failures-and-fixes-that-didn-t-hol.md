---
id: T-2349
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmrecall.py, plugin/lib/fmdoctor.py, plugin/lib/fmeco.py, plugin/tests/test_recall.py, plugin/tests/test_doctor.py, MASTER.md]
depends_on: []
source: user
created: 2026-10-31T14:00:55Z
updated: 2026-10-31T14:43:20Z
builder_model: sonnet
base: d9573a1782eb87207d614b3e16d26580e1871b50
base_tree: fd0fb757b0697cc3eaee7b3cbadb68db7bf1025b
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-10-31T14:14:24Z
plan0_scope: [plugin/lib/fmrecall.py, plugin/lib/fmdoctor.py, plugin/lib/fmhooks.py]
verified: strong
---
# Foreman's own failures, and fixes that didn't hold, enter the signal-to-fix loop (Mission 8, #7)
## Raw request
> Foreman's own failures, and fixes that didn't hold, enter the signal-to-fix loop (Mission 8, #7)
## Interpretation
Gap map #7 signal->fix. T-2272 files one FIX when a failure signature hits 3+ tasks, keyed once ever, so a signature that comes back after its FIX closed is never seen again (the fix didn't hold and nobody knows). It also skips Foreman's own failures: an 'fm doctor: failed' line hit 9 tasks and a PostToolUseFailure over-budget line hit 6 in failures.jsonl, and neither became a fix (the first is excluded by the ^fm rule meant for refusals; the second predates T-2272, which only looks at new rows). 494 rows, 0 captured.
## Assumptions (confidence)
## Acceptance criteria
- [x] A recurring-failure signature that hits a new task after its captured FIX closed captures one FIX 'Fix did not hold: T-X' bound to T-X (from:), once per signature and closed fix; a second hit after that adds no task — verify with `python3 plugin/tests/run.py test_recall test_outcomes`
- [x] Foreman's own failures count: an fm doctor FAIL line, a hook traceback logged to hooks.log and a hook over its latency budget, recurring across 3+ tasks or sessions, capture one FIX (trigger self-failure); 'fm: refused' lines and runner tallies still never capture — verify with `python3 plugin/tests/run.py test_recall test_doctor`
- [x] The first note_failure after the change replays failures.jsonl once, so a signature that crossed 3 tasks before T-2272 shipped is captured once; a second run replays nothing — verify with `python3 plugin/tests/run.py test_recall`
## Non-goals
## Approach (options → choice → why)
1) in fmrecall._recurring: when the signature's capture is closed and a new task hits it after the close, capture 'Fix did not hold: <id>' keyed on (signature, closed id), bound to it (from:), trigger did-not-hold; count Foreman's own failures (an fm doctor FAIL line, a hook traceback in hooks.log, a hook over its latency budget) as signatures while refusals ('fm: refused') and tallies stay out; one replay of failures.jsonl on the first run after the change. 2) a separate incident store every signal feeds - rejected now: a second store beside failures.jsonl and capture events for what one key does. 3) reopen the closed task in place - rejected: closed tasks are archived and their evidence is history; a bound new FIX keeps both. Choice 1.
## Risks and rollback
Blast radius (fm graph blast): co-changes CHANGELOG.md, plugin/tests/test_hooks.py, plugin/lib/fmcli.py, MASTER.md, plugin/tests/test_doctor.py; past FIXes T-0877, T-0907, T-0908, T-0928, T-0951.
## Execution prompt
## Steps
1. [x] red tests: did-not-hold after close; doctor FAIL, hooks.log and over-budget signatures; refusals and tallies stay out; one-time replay
2. [x] did-not-hold capture and own-failure signatures in fmrecall; the feeds from fmdoctor and the hook error log
3. [x] docs: MASTER failure memory line, CHANGELOG
## Resume here
<!-- auto -->
- 2026-10-31T14:23:33Z step 2/3: did-not-hold capture and own-failure signatures in fmrecall; the feeds from fmdoctor and the hook error log
- git: worktree-agent-aa3fa3fe724a4fd21; 5 uncommitted: plugin/lib/fmdoctor.py, plugin/lib/fmeco.py, plugin/lib/fmrecall.py, plugin/tests/test_doctor.py, plugin/tests/test_recall.py
- touched since last checkpoint: plugin/lib/fmeco.py, plugin/lib/fmrecall.py, plugin/lib/fmdoctor.py, plugin/tests/test_doctor.py, plugin/tests/test_recall.py
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_recall test_doctor` → ✗ exit 1 · Ran 122 tests in 75.1s (40 classes, 16 at a time; slowest: Recall 67s, OtherProjects 24s, LockProbe 16s) / FAILED (2 classes: test_recall.Recurring, test_doctor.HookErrors) [ran] [tree 715e115e75b3] (2026-10-31T14:18:42Z)
- (step 2) `python3 plugin/tests/run.py test_recall test_doctor test_outcomes` → ✗ exit 1 · Ran 145 tests in 67.1s (51 classes, 16 at a time; slowest: Recall 66s, Survival 62s, ModelRouter 43s) / FAILED (2 classes: test_recall.Recurring, test_doctor.HookErrors) [ran] [tree e96d58ddb031] (2026-10-31T14:21:48Z)
- (ac 3) `python3 plugin/tests/run.py test_recall 2>&1 | grep -v "^$" | head -40` → ✗ exit 1 · Ran 30 tests in 37.6s (10 classes, 16 at a time; slowest: Recall 37s, OtherProjects 14s, Consolidate 10s) / FAILED (1 classes: test_recall.Recurring) [ran] [tree 848169913cb1] (2026-10-31T14:22:36Z)
- (step 2) `python3 plugin/tests/run.py test_recall test_doctor test_outcomes` → exit 0 · Ran 145 tests in 24.2s (51 classes, 16 at a time; slowest: Recall 23s, Survival 22s, ModelRouter 17s) / OK [ran] [tree 387b23da3f64] (2026-10-31T14:24:44Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_crash_hygiene test_doctor test_ecosystem test_memory test_recall test_supply_delta test_trust && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [18.70s] [ran] [tree 387b23da3f64] (2026-10-31T14:25:35Z)
- (ac 2) `python3 plugin/tests/run.py test_recall test_doctor 2>&1 | grep -E "^(ERROR|FAIL|OK|Ran)" | head -20` → ✗ exit 1 · Ran 126 tests in 40.9s (40 classes, 16 at a time; slowest: Recall 40s, OtherProjects 21s, ViewsRepair 15s) / FAILED (2 classes: test_recall.Recurring, test_doctor.HookErrors) [ran] [tree bd090538b8b6] (2026-10-31T14:34:42Z)
- (step 2) `python3 plugin/tests/run.py test_recall test_doctor test_outcomes` → exit 0 · Ran 149 tests in 35.6s (51 classes, 16 at a time; slowest: Recall 35s, Survival 34s, ModelRouter 23s) / OK [ran] [tree 6f3a7b880016] (2026-10-31T14:36:37Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_crash_hygiene test_doctor test_ecosystem test_memory test_recall test_supply_delta test_trust && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [18.78s] [ran] [tree 6f3a7b880016] (2026-10-31T14:37:53Z)
- (step 2) `python3 plugin/tests/run.py test_recall test_doctor test_outcomes` → exit 0 · Ran 149 tests in 36.7s (51 classes, 16 at a time; slowest: Recall 36s, Survival 34s, ModelRouter 23s) / OK [ran] [tree cb0a31a737f7] (2026-10-31T14:40:39Z)
- (step 3) `grep -q 'T-2349' MASTER.md && grep -q 'T-2349' CHANGELOG.md` → exit 0 · (no output) [ran] [tree 2f3e60a6c609] (2026-10-31T14:41:12Z)
- (ac 1) `python3 plugin/tests/run.py test_recall test_outcomes` → exit 0 · Ran 56 tests in 23.5s (21 classes, 16 at a time; slowest: Recall 23s, Survival 22s, ModelRouter 14s) / OK [ran] [tree 2f3e60a6c609] (2026-10-31T14:42:22Z)
- (ac 2) `python3 plugin/tests/run.py test_recall test_doctor` → exit 0 · Ran 126 tests in 22.8s (40 classes, 16 at a time; slowest: Recall 22s, OtherProjects 9s, ViewsRepair 7s) / OK [ran] [tree 2f3e60a6c609] (2026-10-31T14:42:22Z)
- (ac 3) `python3 plugin/tests/run.py test_recall` → exit 0 · Ran 33 tests in 21.7s (10 classes, 16 at a time; slowest: Recall 21s, OtherProjects 8s, Consolidate 5s) / OK [ran] [tree 2f3e60a6c609] (2026-10-31T14:42:22Z)
- (step 1) `python3 plugin/tests/run.py test_recall test_doctor` → exit 0 · Ran 126 tests in 22.8s (40 classes, 16 at a time; slowest: Recall 22s, OtherProjects 9s, ViewsRepair 7s) / OK [ran] [tree 2f3e60a6c609] (2026-10-31T14:42:22Z)
- (audit intent) `one fm-reviewer pass (all five lenses): approve with nits; both MEDIUMs fixed on the branch (replay capped at 5 and moved out of the hook into fm doctor; a did-not-hold needs a hit later than the fix's close), the LOWs fixed (hourly traceback unit, marker only on a clean finish, per-feed isolation); 149 tests OK after merge` → a fix that didn't hold and Foreman's own recurring failures each file one FIX; old failures replay once (tested) [tree 2f3e60a6c609] (2026-10-31T14:42:22Z)
- (audit adversary) `one fm-reviewer pass (all five lenses): approve with nits; both MEDIUMs fixed on the branch (replay capped at 5 and moved out of the hook into fm doctor; a did-not-hold needs a hit later than the fix's close), the LOWs fixed (hourly traceback unit, marker only on a clean finish, per-feed isolation); 149 tests OK after merge` → doctor and hook text pass failure_signature (redact) then defang(plain) before a brief; keys are hashed and escaped [tree 2f3e60a6c609] (2026-10-31T14:42:22Z)
- (audit operator) `one fm-reviewer pass (all five lenses): approve with nits; both MEDIUMs fixed on the branch (replay capped at 5 and moved out of the hook into fm doctor; a did-not-hold needs a hit later than the fix's close), the LOWs fixed (hourly traceback unit, marker only on a clean finish, per-feed isolation); 149 tests OK after merge` → no hook holds the project lock for the replay any more; doctor's feed is bounded (5 replays, ~30 note_own calls) [tree 2f3e60a6c609] (2026-10-31T14:42:22Z)
- (audit edge) `one fm-reviewer pass (all five lenses): approve with nits; both MEDIUMs fixed on the branch (replay capped at 5 and moved out of the hook into fm doctor; a did-not-hold needs a hit later than the fix's close), the LOWs fixed (hourly traceback unit, marker only on a clean finish, per-feed isolation); 149 tests OK after merge` → a traceback before the fix's close never files a false did-not-hold; five tracebacks in an hour count once [tree 2f3e60a6c609] (2026-10-31T14:42:22Z)
## Log
- 2026-10-31T14:00:55Z created
- 2026-10-31T14:14:10Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2349.builder.md
- 2026-10-31T14:14:23Z focused
- 2026-10-31T14:14:24Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-10-31T14:17:00Z set scope=['plugin/lib/fmrecall.py', 'plugin/lib/fmdoctor.py', 'plugin/lib/fmeco.py', 'plugin/tests/test_recall.py', 'plugin/tests/test_doctor.py', 'MASTER.md']
- 2026-10-31T14:17:01Z scope widened: tests, fmeco.capture_once (bound=), MASTER; fmhooks left out (held by T-2369): the hooks.log feed runs from fm doctor
- 2026-10-31T14:39:57Z merged worktree-agent-aa3fa3fe724a4fd21 (5 file(s))
- 2026-10-31T14:39:58Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aa3fa3fe724a4fd21
- 2026-10-31T14:39:59Z focused
- 2026-10-31T14:40:58Z scope: plugin/lib/fmrecall.py, plugin/lib/fmdoctor.py, plugin/lib/fmeco.py, plugin/tests/test_recall.py, plugin/tests/test_doctor.py, plugin/tests/test_outcomes.py, MASTER.md, CHANGELOG.md
- 2026-10-31T14:43:17Z done
- 2026-10-31T14:43:20Z committed 6a000b62 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1076-review: Verdict: approve with nits.** The code is correct on the paths I traced. None of these findings is HIGH. I did not run the tests, and I could not…
- research T-1875-review: Approve with nits. The feature meets the acceptance criterion in code. I did not run the tests, because I only had read tools. There are no HIGH …
- research mission-20261029-104513: Request: keep super ultimate recursive brainstorming, and implementing all ideas, super ultimate improve foreman in all ways [stale: de…
- decision 2026-10-30: [revisited: weakness-finding uses signals] [cites: user steer 2026-10-30] [check: python3 plugin/tests/run.py test_exam.ExamAuthors] Standing rule: …
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_doctor.py, plugin/tests/test_hooks.py, plugin/tests/test_recall.py
## Lessons
- A one-time backfill doesn't belong in a hook: run it where a slow, bounded pass is expected
## Plan gaps
- failed first: step 1 red tests: did-not-hold after close; doctor FAIL, hooks.log and over-budget signatures; refusals an…
- failed first: step 2 did-not-hold capture and own-failure signatures in fmrecall; the feeds from fmdoctor and the hook e…
## Files touched
- plugin/tests/test_recall.py
- plugin/tests/test_doctor.py
- plugin/lib/fmeco.py
- plugin/lib/fmrecall.py
- plugin/lib/fmdoctor.py
- CHANGELOG.md
- MASTER.md
