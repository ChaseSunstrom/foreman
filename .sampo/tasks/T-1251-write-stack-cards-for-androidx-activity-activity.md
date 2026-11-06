---
id: T-1251
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: scout
created: 2026-10-20T13:44:43Z
updated: 2026-10-20T21:02:17Z
base: 9934ffedcd4b428fd0dc025bead0b6ed47dd6e78
base_tree: 32fa5bf492b266f6e4602f1fad03a3cd57df777a
plan0_at: 2026-10-20T20:55:26Z
plan0_scope: []
verified: strong
---
# Stack cards cover the 8 androidx dependencies fm scout found: new cards for DataStore, Macrobenchmark and the Car App Library; Compose and Android cards detect the rest
## Raw request
> Found by fm scout: dependencies in your projects with no stack card: androidx.activity:activity-ktx, androidx.benchmark:benchmark-macro-junit4, androidx.car.app:app, androidx.car.app:app-projected, androidx.compose.foundation:foundation, androidx.compose.ui:ui-test-junit4, androidx.compose.ui:ui-test-manifest, androidx.datastore:datastore-preferences. Write one card each to the spec in plugin/skills/library/SKILL.md (a writer subagent per batch), then fm lib check
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm lib gaps no longer lists androidx.activity:activity-ktx, androidx.benchmark:benchmark-macro-junit4, androidx.car.app:app, androidx.car.app:app-projected, androidx.compose.foundation:foundation, androidx.compose.ui:ui-test-junit4, androidx.compose.ui:ui-test-manifest or androidx.datastore:datastore-preferences, and every card passes the lint — verify with `fm lib check && fm lib gaps`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Detect lines: compose foundation and ui-test-* on jetpack-compose, activity-ktx on android
2. [x] Three new cards to the spec in plugin/skills/library/SKILL.md (jvm area): androidx-datastore, android-macrobenchmark, android-car-app; verify commands that run on a plain Gradle project; fm lib check
## Resume here
## Docs impact
CHANGELOG
## Verification evidence
- (step 1) `plugin/bin/fm lib gaps` → exit 0 · 1  win10toast / 49 uncovered dependencies (fm lib draft NAME --area AREA stages a card) [ran] [tree f175593039c8] (2026-10-20T20:56:28Z)
- (step 2) `plugin/bin/fm lib check` → exit 0 · 1087 cards, all well-formed (27 related names have no card yet). [ran] [tree f175593039c8] (2026-10-20T20:56:29Z)
- (step 1) `fm lib check` → exit 0 · 1087 cards, all well-formed (27 related names have no card yet). [ran] [tree a127e5e3e55b] (2026-10-20T21:01:10Z)
- (step 2) `fm lib check` → exit 0 · 1087 cards, all well-formed (27 related names have no card yet). [ran] [tree a127e5e3e55b] (2026-10-20T21:01:11Z)
- (ac 1) `fm lib check` → exit 0 · 1087 cards, all well-formed (27 related names have no card yet). [ran] [tree a127e5e3e55b] (2026-10-20T21:01:17Z)
- (ac 1) `fm lib check && fm lib gaps` → exit 0 · 1  win10toast / 49 uncovered dependencies (fm lib draft NAME --area AREA stages a card) [ran] [tree a127e5e3e55b] (2026-10-20T21:01:18Z)
- (audit intent) `self review of the three new cards' API examples (PreferenceDataStoreFactory.create with backgroundScope, TestCarContext.createCarContext, MacrobenchmarkRule) and the detect lines; fm lib check 1087 well-formed; fm lib gaps lists none of the 8` → all 8 dependencies map to a card (gaps re-checked on main: 0 of the 8 listed) [tree a127e5e3e55b] (2026-10-20T21:01:18Z)
- (audit adversary) `self review of the three new cards' API examples (PreferenceDataStoreFactory.create with backgroundScope, TestCarContext.createCarContext, MacrobenchmarkRule) and the detect lines; fm lib check 1087 well-formed; fm lib gaps lists none of the 8` → cards are text the library injects as guidance; no commands run from them [tree a127e5e3e55b] (2026-10-20T21:01:18Z)
- (audit edge) `self review of the three new cards' API examples (PreferenceDataStoreFactory.create with backgroundScope, TestCarContext.createCarContext, MacrobenchmarkRule) and the detect lines; fm lib check 1087 well-formed; fm lib gaps lists none of the 8` → app-automotive and app-testing detected too, so the car card matches either form factor [tree a127e5e3e55b] (2026-10-20T21:01:18Z)
- (audit operator) `self review of the three new cards' API examples (PreferenceDataStoreFactory.create with backgroundScope, TestCarContext.createCarContext, MacrobenchmarkRule) and the detect lines; fm lib check 1087 well-formed; fm lib gaps lists none of the 8` → verify commands are plain Gradle tasks every Android project has [tree a127e5e3e55b] (2026-10-20T21:01:18Z)
- (audit maintainer) `self review of the three new cards' API examples (PreferenceDataStoreFactory.create with backgroundScope, TestCarContext.createCarContext, MacrobenchmarkRule) and the detect lines; fm lib check 1087 well-formed; fm lib gaps lists none of the 8` → same spec as the other jvm cards; related names point at existing cards [tree a127e5e3e55b] (2026-10-20T21:01:18Z)
- (audit self) `self review of the three new cards' API examples (PreferenceDataStoreFactory.create with backgroundScope, TestCarContext.createCarContext, MacrobenchmarkRule) and the detect lines; fm lib check 1087 well-formed; fm lib gaps lists none of the 8` → no findings [tree a127e5e3e55b] (2026-10-20T21:01:18Z)
## Log
- 2026-10-20T13:44:43Z created
- 2026-10-20T20:53:53Z planned from capture
- 2026-10-20T20:55:13Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1251.builder.md
- 2026-10-20T20:55:26Z focused
- 2026-10-20T21:00:53Z merged worktree-agent-af4db9010003e8a84 (5 file(s))
- 2026-10-20T21:00:54Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-af4db9010003e8a84
- 2026-10-20T21:01:06Z focused
- 2026-10-20T21:02:17Z done
- 2026-10-20T21:02:17Z committed 136df68a (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1016 [FEATURE S, done, 2 steps] Stack cards for the deps scout found: scipy, python-audio (librosa, soundfile, demucs), postprocessing; detect lines for playwright-cor…
- T-1020 [FEATURE S, done, 1 steps] Stack cards: SvelteKit adapters, Vite plugins, VS Code extension tooling and xterm.js detected
- T-1018 [FEATURE S, done, 2 steps] Stack cards: CodeMirror 6 card; tauri-build and tauri-plugin-* on the tauri card; troika-three-text on three-js
- decision 2026-10-15: Build T-0933 (stack library) before the board waves: the user's latest ask, and its card writing runs in parallel subagents while the main thread bu…
- similar finished tasks took 1–2 steps
## Lessons
- fm lib gaps from the main checkout reads the main library, so a worktree's new cards show up only via its own plugin/bin/fm
## Files touched
- plugin/skills/library/cards/jvm/jetpack-compose.md
- plugin/skills/library/cards/jvm/android.md
- plugin/skills/library/cards/jvm/androidx-datastore.md
- plugin/skills/library/cards/jvm/android-macrobenchmark.md
- plugin/skills/library/cards/jvm/android-car-app.md
- CHANGELOG.md
