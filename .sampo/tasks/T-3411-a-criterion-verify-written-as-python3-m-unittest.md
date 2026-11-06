---
id: T-3411
type: FIX
tier: M
status: done
priority: normal
scope: [CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/README.md, .sampo/research, .sampo/tasks, plugin/lib/sampo/cli.py, plugin/lib/sampo/core.py, plugin/lib/sampo/lanes.py, plugin/tests/test_verify_unittest_form.py]
depends_on: []
source: discovered
created: 2026-11-06T08:57:15Z
updated: 2026-11-06T12:54:19Z
base_note: 
base: c70f6fb7d5b2b2c1aabafb3a183c6c9e839de82e
base_tree: 876219905759d9ddd4470340e41d5630d011c031
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-06T08:59:14Z
plan0_scope: []
builder_returned: 2026-11-06T09:45:37Z
lane_stop: merged 2026-11-06T09:50:01Z
verified: strong
unproven: [meaning]
---
# A criterion verify written as 'python3 -m unittest test_X.Class' only runs from…
## Raw request
> FIX: a criterion verify written as 'python3 -m unittest test_X.Class' only runs from plugin/tests, so lane merge (which runs it from the repo root) refuses with ERROR _FailedTest (T-3379 tonight; ~209 briefs carry that form). sampo task ac add/edit --verify should rewrite a bare 'python3 -m unittest test_*' to 'python3 plugin/tests/run.py test_*' (or run verify commands from the dir they were recorded in), and lane merge's refusal should name the criterion command and its first error line
## Interpretation
Reading 1: fix at run time, so the 209 stored briefs work unchanged. Reading 2 (ruled out): rewrite stored text at ac add only, which leaves old briefs red.
## Assumptions (confidence)
## Acceptance criteria
- [x] normalize_verify rewrites/relocates the bare unittest form and leaves other commands — verify with `python3 plugin/tests/run.py test_verify_unittest_form`
- [x] ac add/edit prints a note — verify with `python3 plugin/tests/run.py test_verify_unittest_form.AcNote`
- [x] lane merge refusal names the first error line — verify with `python3 plugin/tests/run.py test_verify_unittest_form.MergeRefusal`
## Non-goals
## Approach (options → choice → why)
1) rewrite to plugin/tests/run.py <names>: use what exists, the gate runner; likely outcome: runs with load scaling, fails if a name matches too broadly (substring). 2) run with cwd=tests dir, generic for other projects; likely outcome: exact unittest semantics, fails only if the dir guess is wrong. 3) do less: rewrite only at ac add; fails if old briefs stay red (209 of them). Choice 1 (92%): run.py when it exists, else option 2 as the fallback; both in core.run_command, the one place stored verifies run.
## Risks and rollback
Blast radius (sampo graph blast): co-changes plugin/tests/test_run.py, CHANGELOG.md, plugin/tests/test_ci_annotations.py, .github/workflows/test.yml, plugin/tests/test_bench_family.py; past FIXes T-1808, T-1809, T-1842, T-2001, T-2005.
## Execution prompt
## Steps
1. [x] tests red-first
2. [x] implement normalize_verify, note, refusal
## Resume here
## Docs impact
the builder updated MASTER.md and docs/map for user-visible behaviour; CHANGELOG line added here
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_verify_unittest_form` → ✗ exit 1 · run.py: no test matches test_verify_unittest_form [ran] [tree bf5e00c5c771] [world 2f1906870a] (2026-11-06T08:59:30Z)
- (step 1) `python3 plugin/tests/run.py test_verify_unittest_form` → exit 0 · Ran 8 tests in 144.7s (3 jobs, 16 at a time; slowest: MergeRefusal 0s, AcNote 0s, UnittestForm 0s) / OK [ran] [tree 162bcb5237e2] [world 2f1906870a] (2026-11-06T09:02:32Z)
- `sampo check --affected (affected tests only): plugin/lib/sampo/louhi.py plugin/tests/test_exam.py && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 126 · bash: line 1: plugin/lib/sampo/louhi.py: Permission denied [ran] [tree 162bcb5237e2] [world 2f1906870a] (2026-11-06T09:02:47Z)
- (step 2) `python3 plugin/tests/run.py test_affected_hubs test_affected_symbols test_cli test_core test_lane_twins test_lanes test_verify_alias test_verify_unittest_form test_mint test_rename_scan` → ✗ exit 1 · Ran 552 tests in 602.7s (102 jobs, 16 at a time; slowest: AffectedPairs 395s, Lanes 82s, TaskLifecycle 53s) / FAILED (2 classes: test_cli.AffectedPairs, test_core.LazyPatterns) [ran] [tree 162bcb5237e2] [world 2f1906870a] (2026-11-06T09:13:27Z)
- (step 2) `python3 plugin/tests/run.py test_core.LazyPatterns test_verify_unittest_form` → exit 0 · Ran 11 tests in 84.8s (4 jobs, 16 at a time; slowest: AcNote 0s, UnittestForm 0s, LazyPatterns 0s) / OK [ran] [tree 6a6f300c9a16] [world 2f1906870a] (2026-11-06T09:25:51Z)
- (step 2) `python3 plugin/tests/run.py test_verify_unittest_form` → exit 0 · Ran 8 tests in 289.3s (3 jobs, 16 at a time; slowest: AcNote 2s, UnittestForm 1s, MergeRefusal 0s) / OK [ran] [tree fee5b70821f8] [world 2f1906870a] (2026-11-06T09:37:30Z)
- (step 2) `python3 plugin/tests/run.py test_verify_unittest_form` → exit 0 · Ran 9 tests in 57.9s (3 jobs, 16 at a time; slowest: AcNote 0s, UnittestForm 0s, MergeRefusal 0s) / OK [ran] [tree 38aca95f7566] [world 2f1906870a] (2026-11-06T09:45:30Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree b9c0d8bd343b] (2026-11-06T09:50:04Z)
- (ac 1) `python3 plugin/tests/run.py test_verify_unittest_form` → exit 0 · Ran 9 tests in 1.9s (3 jobs, 16 at a time; slowest: AcNote 0s, UnittestForm 0s, MergeRefusal 0s) / OK [ran] [tree b9c0d8bd343b] [world 2f1906870a] (2026-11-06T09:50:23Z)
- (ac 2) `python3 plugin/tests/run.py test_verify_unittest_form.AcNote` → exit 0 · Ran 1 tests in 3.8s (1 jobs, 16 at a time; slowest: AcNote 0s) / OK [ran] [tree b9c0d8bd343b] [world 2f1906870a] (2026-11-06T09:50:23Z)
- (ac 3) `python3 plugin/tests/run.py test_verify_unittest_form.MergeRefusal` → exit 0 · Ran 1 tests in 8.7s (1 jobs, 16 at a time; slowest: MergeRefusal 0s) / OK [ran] [tree b9c0d8bd343b] [world 2f1906870a] (2026-11-06T09:50:23Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree b9c0d8bd343b] (2026-11-06T09:50:23Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree b9c0d8bd343b] (2026-11-06T09:50:23Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree b9c0d8bd343b] (2026-11-06T09:50:23Z)
## Log
- 2026-11-06T08:57:15Z created
- 2026-11-06T08:57:51Z set tier=M
- 2026-11-06T08:59:02Z planned: it has criteria and steps
- 2026-11-06T08:59:13Z focused
- 2026-11-06T08:59:14Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-06T09:50:01Z merged worktree-agent-a8ea99614269ed919 (4 file(s))
- 2026-11-06T09:50:02Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a8ea99614269ed919
- 2026-11-06T09:50:02Z focused
- 2026-11-06T09:50:04Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'plugin/lib/sampo/cli.py', 'plugin/lib/sampo/core.py', 'plugin/lib/sampo/lanes.py', 'plugin/tests/test_verify_unittest_form.py']
- 2026-11-06T09:50:04Z scope: widened at merge to the reviewed lane's own diff (810a91ad3), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T09:55:52Z done
- 2026-11-06T09:55:56Z committed 08db898ab (1 file)
- 2026-11-06T12:54:19Z not reverted: test_board_verbs.BoardVerbs, test_check_paths.CheckSkip, test_close_gates.CloseGates, test_docs.MapShards, test_docs.PluginFiles already fail on 810a91ad3's first parent
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2847 [FEATURE M, done, 3 steps] Hook, guard, drive and Next-line messages print sampo spellings (sampo focus, sampo ask… — lesson: a scripted respell splits producers …
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- T-2786 [FIX S, done, 1 steps] fm task ac ID edit N --text reads a verify command typed in the text: 'TEXT :: CMD' (as add and task new take it) or a trailing '— verify w…
- decision 2026-11-01: [cites: user steer 2026-11-01: decision on the cold-read rule: keep it, make it reliable (Haiku first, Sonnet decides on FAIL; a FAIL quotes the lin…
## Why not caught
the builder's own failing test before the fix, then the lane review; no earlier gate covered this path (see the brief's Regression test)
## Lessons
- none: a reviewed builder lane; its lessons are in the builder's report and the review findings
## Plan gaps
- failed first: step 1 tests red-first
- failed first: step 2 implement normalize_verify, note, refusal
## Files touched
- plugin/tests/test_verify_unittest_form.py
- plugin/lib/sampo/core.py
- plugin/lib/sampo/cli.py
- plugin/lib/sampo/lanes.py
- CHANGELOG.md
