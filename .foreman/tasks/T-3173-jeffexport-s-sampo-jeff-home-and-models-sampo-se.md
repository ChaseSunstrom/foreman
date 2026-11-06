---
id: T-3173
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-05T07:23:01Z
updated: 2026-11-05T17:30:54Z
builder_model: haiku
base: 37d09c710551e069f49477a504605c4e7bab3d63
base_tree: fbeb99c1806ab8a7abd91140363edb3e6a41c02c
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-11-05T10:16:45Z
plan0_scope: []
builder_returned: 2026-11-05T10:19:48Z
lane_stop: merged 2026-11-05T15:35:37Z
lane_verified: 4fae5ddafa18169c1d3481091b653c4a670f4338
verified: strong
unproven: [tui-unshot, ui-unshot]
---
# SAMPO_ names reach child processes: jeffexport's SAMPO_JEFF_HOME and models' SAMPO_SECRETS are moved to their FOREMAN_ names at import, so a child never sees the SAMPO_ one (the bug smallcards.home had, T-3101)
## Raw request
> jeffexport's SAMPO_JEFF_HOME and models' SAMPO_SECRETS have the same rename bug smallcards.home had (only one env name read after the Foreman to Sampo rename)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] with SAMPO_JEFF_HOME or SAMPO_SECRETS set, a child process started by jeffexport or models still sees the SAMPO_ name, and the FOREMAN_ name keeps working too — verify with `python3 plugin/tests/run.py test_jeff_export test_models`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests then the fix in both
## Resume here
## Docs impact
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_jeff_export test_models 2>&1 | tail -8` → exit 0 · Ran 111 tests in 11.9s (19 classes, 16 at a time; slowest: Wired 11s, Bench 3s, RunRoute 1s) / OK [ran] [tree b4bd326ba9e0] [world 2f1906870a] (2026-11-05T10:17:13Z)
- (step 1) `python3 plugin/tests/run.py test_jeff_export test_models 2>&1 | tail -8` → exit 0 · Ran 111 tests in 11.9s (19 classes, 16 at a time; slowest: Wired 11s, Bench 3s, RunRoute 1s) / OK [ran] [tree b4bd326ba9e0] [world 2f1906870a] (2026-11-05T10:17:13Z)
- (step 1) `python3 plugin/tests/run.py test_jeff_export test_models` → exit 0 · Ran 111 tests in 11.4s (19 classes, 16 at a time; slowest: Wired 11s, Bench 3s, RunRoute 1s) / OK [ran] [tree b4bd326ba9e0] [world 2f1906870a] (2026-11-05T10:17:30Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_code_hardening test_code_worker test_ctx_variant test_doctor test_export test_jeff_export test_left_out test_models test_moons_scale test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 164 tests across 6 files. [21.80s] [ran] [tree b4bd326ba9e0] [world 2f1906870a] (2026-11-05T10:19:41Z)
- (step 1) `python3 plugin/tests/run.py test_jeff_export test_models test_small_cards` → exit 0 · Ran 132 tests in 5.4s (29 jobs, 16 at a time; slowest: Bench 5s, Wired.test_a_rerun_gives_the_same_hash_and_the_canary_is_in_the_manifest 4s, Wired.test_authors_agent_text_off_by_default_tool_text_qua [ran] [tree ed07a638d5b3] [world 2f1906870a] (2026-11-05T17:30:07Z)
- `python3 plugin/tests/run.py test_jeff_export test_models test_small_cards` → ✗ exit 1 · Ran 132 tests in 17.1s (23 jobs, 16 at a time; slowest: Wired 15s, Bench 4s, RunRoute 2s) / FAILED (2 classes: test_models.OpenAIShape, test_jeff_export.JeffHomeEnv) (start tree + this task's tests) [ran] [tree ed07a638d5b3] [world 2f1906870a] (2026-11-05T17:30:31Z)
- `python3 plugin/tests/run.py test_jeff_export test_models test_small_cards` → exit 0 · Ran 132 tests in 5.4s (29 jobs, 16 at a time; slowest: Bench 5s, Wired.test_a_rerun_gives_the_same_hash_and_the_canary_is_in_the_manifest 4s, Wired.test_authors_agent_text_off_by_default_tool_text_qua [ran] [tree ed07a638d5b3] [world 2f1906870a] (2026-11-05T17:30:31Z)
- (ac 1) `python3 plugin/tests/run.py test_jeff_export test_models` → exit 0 · Ran 111 tests in 5.0s (25 jobs, 16 at a time; slowest: Bench 4s, Wired.test_a_rerun_gives_the_same_hash_and_the_canary_is_in_the_manifest 4s, Wired.test_optout_and_a_symlink_to_a_sensitive_root_are_le [ran] [tree f417f3c83626] [world 2f1906870a] (2026-11-05T17:30:45Z)
- (audit adversary) `re-ran test_jeff_export test_models test_small_cards on main after the merge (132 OK), proved red→green; the merge conflict with T-3101 in smallcards.home was the same code on both sides, docstring combined` → SAMPO_SECRETS names where the secrets file lives; reading it under both names changes which path is read, not who may read it: Ward still guards ~/.config/sampo as credentials, and the self-change gate's key ignores both names (T-3192) [tree f417f3c83626] (2026-11-05T17:30:45Z)
- (audit edge) `re-ran test_jeff_export test_models test_small_cards on main after the merge (132 OK), proved red→green; the merge conflict with T-3101 in smallcards.home was the same code on both sides, docstring combined` → with neither name set the default state paths hold; with both set the SAMPO_ one wins, as before [tree f417f3c83626] (2026-11-05T17:30:45Z)
- (audit self) `re-ran test_jeff_export test_models test_small_cards on main after the merge (132 OK), proved red→green; the merge conflict with T-3101 in smallcards.home was the same code on both sides, docstring combined` → no findings [tree f417f3c83626] (2026-11-05T17:30:45Z)
## Log
- 2026-11-05T07:23:01Z created
- 2026-11-05T10:16:10Z planned from capture
- 2026-11-05T10:16:10Z set approved=True
- 2026-11-05T10:16:11Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3173.builder.md
- 2026-11-05T10:16:44Z focused
- 2026-11-05T10:16:45Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-11-05T10:21:04Z steer: lead added smallcards.home (same bug, the builder's Noticed) with a red-first subprocess test; 132 tests OK
- 2026-11-05T14:56:52Z focused
- 2026-11-05T15:35:37Z merged worktree-agent-af0010fabc0874977 (6 file(s))
- 2026-11-05T15:35:37Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-af0010fabc0874977
- 2026-11-05T15:46:46Z verified: the full suite is green on 4fae5ddaf
- 2026-11-05T17:29:55Z focused
- 2026-11-05T17:30:47Z affected tests waived: names that can't match are T-3160's modules (merged and reverted inside this window, not on disk); T-3173's own tests pass (132 OK)
- 2026-11-05T17:30:49Z done
- 2026-11-05T17:30:54Z committed fbe7d2e8 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- T-2766 [FEATURE M, done, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as t…
- T-2748 [CLEAN M, done, 4 steps] Internals become Sampo (T-2742 step 4): plugin/lib/fmX.py moves to the package plugin/lib/sampo/ under the decided map, each old fmX.py s…
- decision 2026-11-03: SAMPO_X moves into FOREMAN_X when sampo.core loads and leaves the environment (SAMPO wins); FOREMAN_X is not copied back to SAMPO_X
- similar past tasks were L: consider --tier L
## Files touched
- plugin/lib/sampo/models.py
- plugin/lib/sampo/jeffexport.py
- plugin/tests/test_jeff_export.py
- plugin/tests/test_models.py
- plugin/tests/test_small_cards.py
- plugin/lib/sampo/smallcards.py
- CHANGELOG.md
- MASTER.md
- docs/map/files-lib-2.md
- mods/foreman-ui/.claude-plugin/plugin.json
- mods/foreman-ui/hooks/kit.ts
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/hooks/rows.tsx
- mods/foreman-ui/hooks/state.ts
- mods/foreman-ui/tests/fixtures/golden.ts
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/tools/shot.py
- plugin/lib/fmguard.py
- plugin/lib/sampo/cli.py
- plugin/lib/sampo/core.py
- plugin/lib/sampo/cost.py
- plugin/lib/sampo/doctor.py
- plugin/lib/sampo/hooks.py
- plugin/lib/sampo/lanes.py
- plugin/lib/sampo/live.py
- plugin/lib/sampo/louhi.py
- plugin/lib/sampo/moonscale.py
- plugin/lib/sampo/rune.py
- plugin/lib/sampo/selfgate.py
- plugin/lib/sampo/smith.py
