---
id: T-2799
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: scout
created: 2026-11-03T08:30:32Z
updated: 2026-11-03T21:27:29Z
builder_model: sonnet
base: d8f0a58e2e3f7f4c893af3a23700a0cc4cfdda11
base_tree: 11852b1e229250bf7a75820ebf191f86a9489f80
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-03T21:11:43Z
plan0_scope: []
lane_stop: merged 2026-11-03T21:24:02Z
verified: strong
unproven: [docs]
---
# Write stack cards for junit:junit, knip, mime-guess, org.jetbrains.kotlin.android, org.json:json, 3 left out
## Raw request
> Found by fm scout: dependencies in your projects with no stack card: junit:junit, knip, mime-guess, org.jetbrains.kotlin.android, org.json:json, org.junit.platform:junit-platform-launcher, org.robolectric:robolectric, psutil. Write one card each to the spec in plugin/skills/library/SKILL.md (a writer subagent per batch), then fm lib check (found under the standing mandate: Genesis: build Foreman into a self-directing harness per research/genesis/gen-0…)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a stack card for each of junit:junit, knip, mime-guess, org.jetbrains.kotlin.android, org.json:json, org.junit.platform:junit-platform-launcher, org.robolectric:robolectric and psutil, to plugin/skills/library/SKILL.md's spec, and fm lib check passes — verify with `fm lib check`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] write the eight cards (one writer per batch, per the library skill)
2. [x] fm lib check
## Resume here
## Docs impact
none: the cards are docs
## Verification evidence
- (step 1) `python3 plugin/bin/fm lib gaps` → exit 0 · 1  zstandard / 48 uncovered dependencies (fm lib draft NAME --area AREA stages a card) [ran] [tree 909a3a9aced9] [world 2f1906870a] (2026-11-03T21:15:09Z)
- (step 2) `python3 plugin/bin/fm lib check` → exit 0 · 1227 cards, all well-formed, 2 with a verified: date (27 related names have no card yet). [ran] [tree 909a3a9aced9] [world 2f1906870a] (2026-11-03T21:15:10Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_audit test_board_surfaces test_brainstorm_skill test_cli test_core test_cost test_design_surfaces test_design_tokens test_docs test_doctor test_edit_cards test_extras test_followups test_guard test_guard_cases test_hooks test_ideation test_incident test_judgment test_lib_hostile test_lib_source_kill test_library test_nudges test_onwrite test_playbook_use test_plugin_parity test_plugins test_release test_replan test_scaffold test_scene test_scout test_second test_shade test_showpieces test_site_gallery test_skillroute test_smoke_profiles test_speed test_steering test_supply_delta test_taste_ledger test_tidy test_tool_queue test_ui test_verifying test_which && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.75s] [ran] [tree 909a3a9aced9] [world 2f1906870a] (2026-11-03T21:17:19Z)
- (ac 1) `fm lib check` → exit 0 · 1227 cards, all well-formed, 2 with a verified: date (27 related names have no card yet). [ran] [tree de40f8b1fdca] [world 2f1906870a] (2026-11-03T21:24:12Z)
- (audit intent) `self: eight new markdown cards, nothing else; fm lib check passes on the merged tree; mime_guess and psutil grounded against installed versions, the JVM and knip cards kept to well-known facts` → the user's projects' uncovered deps now have cards [tree de40f8b1fdca] (2026-11-03T21:24:12Z)
- (audit edge) `self: eight new markdown cards, nothing else; fm lib check passes on the merged tree; mime_guess and psutil grounded against installed versions, the JVM and knip cards kept to well-known facts` → commands in the JVM cards' Verify sections were not run here (no Gradle/Maven) [tree de40f8b1fdca] (2026-11-03T21:24:12Z)
- (audit adversary) `self: eight new markdown cards, nothing else; fm lib check passes on the merged tree; mime_guess and psutil grounded against installed versions, the JVM and knip cards kept to well-known facts` → static text; lint's untrusted-instruction and npx checks pass; knip runs via ./node_modules/.bin, not npx [tree de40f8b1fdca] (2026-11-03T21:24:12Z)
- (audit self) `self: eight new markdown cards, nothing else; fm lib check passes on the merged tree; mime_guess and psutil grounded against installed versions, the JVM and knip cards kept to well-known facts` → no findings [tree de40f8b1fdca] (2026-11-03T21:24:12Z)
## Log
- 2026-11-03T08:30:32Z created
- 2026-11-03T21:11:31Z planned: it has criteria and steps
- 2026-11-03T21:11:33Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2799.builder.md
- 2026-11-03T21:11:42Z focused
- 2026-11-03T21:11:43Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-03T21:24:02Z merged worktree-agent-ae27ce08511c94587 (8 file(s))
- 2026-11-03T21:24:07Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ae27ce08511c94587
- 2026-11-03T21:24:08Z focused
- 2026-11-03T21:27:29Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2301 [FEATURE S, deferred, 0 steps] Write stack cards for androidx.webkit:webkit, base64, catboost, chacha20poly1305, com.alphacephei:vosk
- T-2531 [FEATURE S, dropped, 0 steps] Write stack cards for com.microsoft.onnxruntime:onnxruntime-android, com.squareup.okhttp3:mockwebserver, com.squareup.o…
- T-2599 [FEATURE S, deferred, 0 steps] Write stack cards for hmac, hmmlearn, http-body-util, import-linter, io.github.takahirom.roborazzi:roborazzi
- decision 2026-10-31: [cites: T-2178; gen-0 §2 #13; decisions 2026-10-30 T-2105] Genesis self-start (gen-0 #13, reconciling T-2105): under full autonomy, a drained queue …
## Files touched
- plugin/skills/library/cards/jvm/junit4.md
- plugin/skills/library/cards/node/knip.md
- plugin/skills/library/cards/rust/mime-guess.md
- plugin/skills/library/cards/jvm/kotlin-android.md
- plugin/skills/library/cards/jvm/org-json.md
- plugin/skills/library/cards/jvm/junit-platform-launcher.md
- plugin/skills/library/cards/jvm/robolectric.md
- plugin/skills/library/cards/python/psutil.md
