---
id: T-2756
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/sampo/cli.py, plugin/lib/sampo/rune.py, plugin/lib/sampo/core.py, plugin/tests/test_genesis.py]
depends_on: []
source: discovered
created: 2026-11-03T02:46:37Z
updated: 2026-11-03T05:34:17Z
base: b7cbaa5c89a56df52a40447777a2a041074e5e15
base_tree: 255e2fab14f19678c4dc36df17b3dceced56057b
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-03T03:07:47Z
plan0_scope: []
builder_model: sonnet
lane_stop: merged 2026-11-03T04:49:26Z
verified: strong
unproven: [docs, meaning, ui-unshot]
---
# fm doctor's steer-check hint says 'fm decide … --check CMD --revisited WORDS', but a row…
## Raw request
> FIX: fm doctor's steer-check hint says 'fm decide … --check CMD --revisited WORDS', but a row settles a steer rule only when it also --cites the user's steer; following the hint as printed leaves the FAIL (cost a retry on 2026-11-03). The hint should name --cites
## Interpretation
Reading 1 (chosen): a user steer is scored against gen-N's sealed prediction once per cited message, not once per decision. Today plugin/lib/sampo/cli.py:4323 calls rune.score_steer(p, f'{decision} {cites}') on every fm decide whose --cites reads as a steer. score_steer (plugin/lib/sampo/rune.py:3688) keys the gap on sha1 of that text. So re-recording a rule (with --check and --revisited, as the doctor asks) or deriving a second rule from the same steer files another anticipation gap and another prediction-score row. This happened three times this session (T-2754, T-2755, T-2761, all dropped). Fix: score_steer takes the cite. It writes it in the row, and skips (returns None) when the newest gen's prediction-score.jsonl already holds a row with that cite. The gap is keyed on the cite. Also, core.steer_checks' hint (plugin/lib/sampo/core.py:~3728) names --cites, since only a row that cites a user steer settles a steer rule. Reading 2 (ruled out): skip scoring only when --revisited is given. The derived-rule case (a new decision citing the same steer) would still file a gap.
## Assumptions (confidence)
## Acceptance criteria
- [x] a row that --revisited an earlier steer files no new anticipation gap and no prediction-score row, and the doctor's hint for an unchecked steer names --cites — verify with `python3 plugin/tests/run.py test_genesis.SealedPrediction.test_restating_a_steer_files_no_gap_and_the_hint_names_cites`
## Non-goals
## Approach (options → choice → why)
1. Use what exists: a cite= keyword on rune.score_steer, read against the jsonl it already writes; one argument from cli; the hint string. Likely outcome: about 12 lines plus the drafted test. Fails if: two different steers share identical cite text; then they are the same message.
2. Dedupe in eco.capture_once by a normalized key. Fails if: the prediction-score row still double-counts the hit rate.
3. Do less: leave it and drop the duplicate gaps by hand. Fails if: every steer re-record files one; it already happened three times.
Choice 1 (90%).
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test, then fmcli's decide skips score_steer when --revisited is given, and fmcore.steer_checks' hint names --cites (after T-2748 merges: both files move)
## Resume here
<!-- auto -->
- 2026-11-03T04:59:00Z steps 1/1 done
- git: foreman/build; 0 uncommitted
- touched since last checkpoint: /tmp/claude-1000/-home-<user>--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/directions-v2/3-copper-mountain/_build/gen_logo.py, /tmp/claude-1000/-home-<user>--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/directions-v2/2-forge/logo.svg, /tmp/claude-1000/-home-<user>--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/directions-v2/2-forge/icon-16.svg, /tmp/claude-1000/-home-<user>--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/directions-v2/2-forge/_tools/sheet.html, /tmp/claude-1000/-home-<user>--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/directions-v2/1-kirjokansi/_src/gen.py, /tmp/claude-1000/-home-<user>--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/directions-v2/3-copper-mountain/_build/build_page.py
- failures met: origin git@github.com:sampo.git (fetch)
## Docs impact
none: internal scoring; the doctor's hint text is the doc
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_genesis.SealedPrediction.test_restating_a_steer_files_no_gap_and_the_hint_names_cites 2>&1 | grep -E "AssertionError|^OK|FAILED|Error" | head -5` → ✗ exit 1 · FAILED (failures=1) / FAILED (1 classes: test_genesis.SealedPrediction) [ran] [tree 798540ac69f3] [world 2f1906870a] (2026-11-03T03:07:58Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis.SealedPrediction.test_restating_a_steer_files_no_gap_and_the_hint_names_cites 2>&1 | tail -8` → ✗ exit 1 · Ran 1 tests in 6.3s (1 classes, 16 at a time; slowest: SealedPrediction 1s) / FAILED (1 classes: test_genesis.SealedPrediction) [ran] [tree fd53951a9f5d] [world 2f1906870a] (2026-11-03T04:36:54Z)
- (step 1) `python3 plugin/tests/run.py test_genesis.SealedPrediction.test_restating_a_steer_files_no_gap_and_the_hint_names_cites` → exit 0 · Ran 1 tests in 2.1s (1 classes, 16 at a time; slowest: SealedPrediction 1s) / OK [ran] [tree 0a945a8c2cbc] [world 2f1906870a] (2026-11-03T04:38:17Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_core test_genesis && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [58.19s] [ran] [tree 0a945a8c2cbc] [world 2f1906870a] (2026-11-03T04:40:48Z)
- `python3 plugin/tests/run.py test_genesis.SealedPrediction.test_restating_a_steer_files_no_gap_and_the_hint_names_cites` → ✗ exit 1 · Ran 1 tests in 1.6s (1 classes, 16 at a time; slowest: SealedPrediction 0s) / FAILED (1 classes: test_genesis.SealedPrediction) (start tree + this task's tests) [ran] [tree 0a945a8c2cbc] [world 2f1906870a] (2026-11-03T04:50:14Z)
- `python3 plugin/tests/run.py test_genesis.SealedPrediction.test_restating_a_steer_files_no_gap_and_the_hint_names_cites` → exit 0 · Ran 1 tests in 1.1s (1 classes, 16 at a time; slowest: SealedPrediction 1s) / OK [ran] [tree 0a945a8c2cbc] [world 2f1906870a] (2026-11-03T04:50:14Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis.SealedPrediction.test_restating_a_steer_files_no_gap_and_the_hint_names_cites` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T04:50:14Z [ran] [tree 0a945a8c2cbc] [world 2f1906870a] (2026-11-03T04:50:38Z)
- (audit intent) `self: read the merged diff; the cite is normalised the same way it is stored, the gap key hashes the cite so a restated steer can't file a second gap, and decide passes the cites text through` → a steer cited by several decisions is scored once per gen; the doctor's hint now names --cites, the flag that makes a row a steer [tree 0a945a8c2cbc] (2026-11-03T04:50:38Z)
- (audit edge) `self: read the merged diff; the cite is normalised the same way it is stored, the gap key hashes the cite so a restated steer can't file a second gap, and decide passes the cites text through` → the cite check runs outside the lock, so two decides at the same instant could both score; harmless (one extra row, capture_once dedupes the gap). A row without cite (older rows) reads as None and never matches [tree 0a945a8c2cbc] (2026-11-03T04:50:38Z)
- (audit adversary) `self: read the merged diff; the cite is normalised the same way it is stored, the gap key hashes the cite so a restated steer can't file a second gap, and decide passes the cites text through` → sha1 is a dedupe key, not a security boundary; a crafted cite can only suppress its own gen's gap for that same cite text, which the user wrote; a malformed jsonl row is skipped, not raised [tree 0a945a8c2cbc] (2026-11-03T04:50:38Z)
- (audit self) `self: read the merged diff; the cite is normalised the same way it is stored, the gap key hashes the cite so a restated steer can't file a second gap, and decide passes the cites text through` → no findings [tree 0a945a8c2cbc] (2026-11-03T04:50:38Z)
- `python3 plugin/tests/run.py test_genesis.SealedPrediction.test_restating_a_steer_files_no_gap_and_the_hint_names_cites` → exit 0 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: SealedPrediction 0s) / OK [ran] [tree b3eb410e32c8] [world 2f1906870a] (2026-11-03T04:51:38Z)
- (audit intent) `self: read the merged diff; the cite is normalised the same way it is stored, the gap key hashes the cite so a restated steer can't file a second gap, and decide passes the cites text through` → a steer cited by several decisions is scored once per gen; the doctor's hint now names --cites, the flag that makes a row a steer [tree b3eb410e32c8] (2026-11-03T04:51:38Z)
- (audit edge) `self: read the merged diff; the cite is normalised the same way it is stored, the gap key hashes the cite so a restated steer can't file a second gap, and decide passes the cites text through` → the cite check runs outside the lock, so two decides at the same instant could both score; harmless (one extra row, capture_once dedupes the gap). A row without cite (older rows) reads as None and never matches [tree b3eb410e32c8] (2026-11-03T04:51:38Z)
- (audit adversary) `self: read the merged diff; the cite is normalised the same way it is stored, the gap key hashes the cite so a restated steer can't file a second gap, and decide passes the cites text through` → sha1 is a dedupe key, not a security boundary; a crafted cite can only suppress its own gen's gap for that same cite text, which the user wrote; a malformed jsonl row is skipped, not raised [tree b3eb410e32c8] (2026-11-03T04:51:38Z)
- (audit self) `self: read the merged diff; the cite is normalised the same way it is stored, the gap key hashes the cite so a restated steer can't file a second gap, and decide passes the cites text through` → no findings [tree b3eb410e32c8] (2026-11-03T04:51:38Z)
- `python3 plugin/tests/run.py test_genesis.SealedPrediction` → exit 0 · Ran 6 tests in 1.1s (1 classes, 16 at a time; slowest: SealedPrediction 1s) / OK [ran] [tree f49132869b08] [world 2f1906870a] (2026-11-03T05:25:59Z)
- (audit intent) `self: read the merged diff; the cite is normalised the same way it is stored, the gap key hashes the cite so a restated steer can't file a second gap, and decide passes the cites text through` → a steer cited by several decisions is scored once per gen; the doctor's hint now names --cites, the flag that makes a row a steer [tree f49132869b08] (2026-11-03T05:25:59Z)
- (audit edge) `self: read the merged diff; the cite is normalised the same way it is stored, the gap key hashes the cite so a restated steer can't file a second gap, and decide passes the cites text through` → the cite check runs outside the lock, so two decides at the same instant could both score; harmless (one extra row, capture_once dedupes the gap). A row without cite (older rows) reads as None and never matches [tree f49132869b08] (2026-11-03T05:25:59Z)
- (audit adversary) `self: read the merged diff; the cite is normalised the same way it is stored, the gap key hashes the cite so a restated steer can't file a second gap, and decide passes the cites text through` → sha1 is a dedupe key, not a security boundary; a crafted cite can only suppress its own gen's gap for that same cite text, which the user wrote; a malformed jsonl row is skipped, not raised [tree f49132869b08] (2026-11-03T05:25:59Z)
- (audit self) `self: read the merged diff; the cite is normalised the same way it is stored, the gap key hashes the cite so a restated steer can't file a second gap, and decide passes the cites text through` → no findings [tree f49132869b08] (2026-11-03T05:25:59Z)
## Log
- 2026-11-03T02:46:37Z created
- 2026-11-03T03:07:20Z scope (found 2026-11-03): re-recording a steer row with --revisited to add its check also filed two new anticipation gaps (T-2754, T-2755, dropped as duplicates of T-2744): a row that --revisited an earlier steer row restates it and files no gap
- 2026-11-03T03:07:44Z set tier=S
- 2026-11-03T03:07:44Z planned: it has criteria and steps
- 2026-11-03T03:07:46Z focused
- 2026-11-03T03:07:47Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-03T03:07:50Z criterion 1 verify: `python3 plugin/tests/run.py test_genesis.Genesis.test_restating_a_steer_files_no_gap_and_the_hint_names_cites` → `python3 plugin/tests/run.py test_genesis.SealedPrediction.test_restating_a_steer_files_no_gap_and_the_hint_names_cites`
- 2026-11-03T03:24:47Z paused: focus moved to T-2753
- 2026-11-03T03:40:56Z scope: a decision that --cites a user steer already scored (same cite text) also files a gap (T-2761-style duplicates on 2026-11-03): score a steer once per cited message, not per decision row
- 2026-11-03T03:42:07Z plan: the test lives in the scratchpad (t2756-test.py) until T-2748 merges; fix = decide scores a steer only when no prediction-score row of the newest gen already holds the same cite text (covers --revisited restatements and derived decisions), and steer_checks' hint names --cites
- 2026-11-03T04:36:10Z set scope=['plugin/lib/sampo/cli.py', 'plugin/lib/sampo/rune.py', 'plugin/lib/sampo/core.py', 'plugin/tests/test_genesis.py']
- 2026-11-03T04:36:12Z set approved=True
- 2026-11-03T04:36:13Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2756.builder.md
- 2026-11-03T04:36:26Z focused
- 2026-11-03T04:49:26Z merged worktree-agent-a3d3f10f7c4a48c5d (4 file(s))
- 2026-11-03T04:50:01Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a3d3f10f7c4a48c5d
- 2026-11-03T04:50:01Z focused
- 2026-11-03T04:51:31Z scope: test_rename_env.py arrived with the T-2766 lane merge, and .fm-scratch/e.json is a test run's scratch; neither is T-2756's edit
- 2026-11-03T05:25:57Z scope: every file outside the scope since focus arrived in other lanes' merge commits (T-2766, T-2764, T-2765, T-2767, T-2768, T-2774, T-2775, T-2777, T-2781, T-2782) or a test run's .fm-scratch; T-2756's own edits are the four scope files
- 2026-11-03T05:34:17Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-2167-review: Verdict:** changes needed. There are no blockers. The doctor behaviour doesn't match what the user asked for, and one enforcement hole could leav…
- T-2465 [FIX S, done, 1 steps] fm decide refuses a row that cites a user steer without --check, naming --check and --revisited
- T-2493 [FIX S, done, 2 steps] Two fm CLI fixes: fm decide refuses a user-steer row without --check; a mistyped flag's hint names only the typed comma… — lesson: Say a ga…
- decision 2026-10-30: [revisited: every user steer becomes a standing rule] [cites: the user's steer 2026-10-30 (second): standing rule] [check: python3 plugin/tests/run.…
- similar finished tasks took 1–2 steps
## Preflight
Changed in scope since this was planned (2026-11-03): plugin/lib/sampo/cli.py, plugin/lib/sampo/core.py, plugin/lib/sampo/rune.py, plugin/tests/test_genesis.py; re-ground the plan against them before editing
## Lessons
- Key a dedupe on the stable identifier (the cite), not the free text around it
## Files touched
- plugin/tests/test_genesis.py
- plugin/tests/test_rename_env.py
- .fm-scratch/e.json
- plugin/lib/sampo/cli.py
- plugin/lib/sampo/core.py
- plugin/lib/sampo/rune.py
- MASTER.md
- plugin/bin/sampo
- plugin/commands/backlog.md
- plugin/commands/build.md
- plugin/commands/looks.md
- plugin/commands/settings.md
- plugin/hooks/hook
- plugin/lib/sampo/doctor.py
- plugin/lib/sampo/graph.py
- plugin/lib/sampo/hooks.py
- plugin/lib/sampo/ideas.py
- plugin/lib/sampo/outcomes.py
- plugin/lib/sampo/py.py
- plugin/lib/sampo/release.py
- plugin/lib/sampo/reverify.py
- plugin/lib/sampo/split.py
- plugin/lib/sampo/stack.py
- plugin/output-styles/foreman.md
- plugin/skills/brainstorm/SKILL.md
- plugin/skills/brainstorm/references/ideas-prompt.md
- plugin/skills/capture/SKILL.md
- plugin/skills/debug-test/SKILL.md
- plugin/skills/design-extract/SKILL.md
- plugin/skills/directions/SKILL.md
