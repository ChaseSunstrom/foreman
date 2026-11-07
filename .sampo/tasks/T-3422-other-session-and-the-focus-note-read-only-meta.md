---
id: T-3422
type: FIX
tier: M
status: active
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T09:57:38Z
updated: 2026-11-06T17:30:33Z
lane: ~/.claude/foreman/.claude/worktrees/agent-a41db42a89f4bd91c
lane_branch: worktree-agent-a41db42a89f4bd91c
base: 4c069af1c7d1f231ec01b2048dce639b8bfc6981
base_tree: e3fd233cc915e43bc2963bd5b874cf7515fb8992
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-11-06T09:58:49Z
plan0_scope: []
builder_returned: 2026-11-06T10:44:48Z
lane_passed: {"tree": "645fb508ad4e36a845e2361fbaad789b5e568207", "cmds": ["python3 plugin/tests/run.py test_hooks.OtherSessionMarkers"]}
inferred_deps: [T-3389]
inferred_why: T-3389: named in its request
group: fleet claims and session liveness
---
# _other_session and the focus note read only meta.json's one session slot, so a second…
## Raw request
> FIX: _other_session and the focus note read only meta.json's one session slot, so a second session working autonomously still looks idle; read the per-session sessions/<sid>.seen markers T-3389 adds (T-3389 review)
## Interpretation
Reading 1: scan markers for any non-self fresh one (chosen). Reading 2: make every session write its own stamp into meta.json; ruled out, needs lock and parse per tool call, which T-3389 avoided.
## Assumptions (confidence)
## Acceptance criteria
- [ ] non-owner fresh marker counts live, stale does not, own ignored — verify with `python3 plugin/tests/run.py test_hooks.OtherSessionMarkers`
## Non-goals
## Approach (options → choice → why)
1) Helper in core.py scanning sessions/*.seen, used by both readers; likely outcome: cheap, correct. 2) use what exists: the meta.json session slot, extended to a per-session map; fails if: a lock and parse per tool call, which T-3389 avoided. 3) do less: leave the slot only; fails if: the second session still looks idle. Choice 1 (80%): stat only, no lock.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test then helper + wire both readers
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_hooks.OtherSessionMarkers` → exit 0 · Ran 1 tests in 97.1s (1 jobs, 16 at a time; slowest: OtherSessionMarkers 0s) / OK [ran] [tree 607ad70d6834] [world 2f1906870a] (2026-11-06T10:01:09Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_affected_hubs test_affected_symbols test_cli test_compact test_core test_doctor test_hooks test_kalevala test_left_out test_louhi_models test_mint test_models test_rename_scan test_verify_alias test_verify_unittest_form && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [19.83s] [ran] [tree 607ad70d6834] [world 2f1906870a] (2026-11-06T10:04:38Z)
- (step 1) `python3 plugin/tests/run.py test_hooks.OtherSessionMarkers` → ✗ exit 1 · Ran 4 tests in 7.3s (1 jobs, 16 at a time; slowest: OtherSessionMarkers 1s) / FAILED (1 classes: test_hooks.OtherSessionMarkers) [ran] [tree 92074f72af87] [world 2f1906870a] (2026-11-06T10:06:18Z)
- (step 1) `python3 plugin/tests/run.py test_hooks.OtherSessionMarkers` → exit 0 · Ran 4 tests in 23.1s (1 jobs, 16 at a time; slowest: OtherSessionMarkers 1s) / OK [ran] [tree 1d692da99cf6] [world 2f1906870a] (2026-11-06T10:06:54Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_affected_hubs test_affected_symbols test_cli test_compact test_core test_doctor test_hooks test_kalevala test_left_out test_louhi_models test_mint test_models test_rename_scan test_verify_alias test_verify_unittest_form && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 944 tests in 130.4s (458 jobs, 16 at a time; slowest: AffectedPairs.test_an_affected_run_with_evidence_records_it 58s, AffectedPairs.test_only_the_red_first_file_itself_is_left_out 52s, AffectedPa [ran] [tree 1d692da99cf6] [world 2f1906870a] (2026-11-06T10:09:12Z)
- (step 1) `python3 plugin/tests/run.py test_hooks.OtherSessionMarkers test_hooks.PostToolUse` → exit 0 · Ran 12 tests in 1.7s (2 jobs, 16 at a time; slowest: PostToolUse 1s, OtherSessionMarkers 1s) / OK [ran] [tree 645fb508ad4e] [world 2f1906870a] (2026-11-06T10:43:45Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_affected_hubs test_affected_symbols test_cli test_compact test_core test_doctor test_hooks test_kalevala test_left_out test_louhi_models test_mint test_models test_rename_scan test_verify_alias test_verify_unittest_form && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 174 tests across 6 files. [13.49s] [ran] [tree 645fb508ad4e] [world 2f1906870a] (2026-11-06T10:44:38Z)
## Log
- 2026-11-06T09:57:38Z created
- 2026-11-06T09:58:29Z planned: it has criteria and steps
- 2026-11-06T09:58:48Z focused
- 2026-11-06T09:58:49Z predicted from its closes: 6 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3389 [FIX M, active, 1 steps] Session liveness ('seen') refreshes only on prompts, so a holder doing 15+ min of…
- T-2847 [FEATURE M, done, 3 steps] Hook, guard, drive and Next-line messages print sampo spellings (sampo focus, sampo ask… — lesson: a scripted respell splits producers …
- T-2915 [FEATURE M, done, 4 steps] MASTER.md opens whole in one Read: each over-long section moves to docs/map shards, MASTER.md keeps a one-line-per-entry index with lin…
- decision 2026-10-16: T-1069 self-approved under full autonomy: a race clones the brief as a 'b' task so each builder works under its own id; pick merges the winner throu…
- similar finished tasks took 3–4 steps
