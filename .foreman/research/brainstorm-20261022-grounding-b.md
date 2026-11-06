### Design-craft playbooks (web, type, material, motion, landing, forms, mobile, email, CLI/TUI)
ids: b032, b034, b035, b036, b037, b038, b072, b073, b074, b075, b077, b121, b162, b177
ground: partial. Only `plugin/skills/playbooks/references/ui/terminal-ui.md` exists for UI (48 reference files in all). The web and 3D craft cards live in the library, not in playbooks. Medium confidence.
score: value 5 · effort M · risk low · mark build
brief: Add `references/ui/` playbooks (composition, type, material, interaction feel, depth without WebGL, backdrops, native-first motion, landing, forms, mobile, email/print, microcopy, CLI/TUI product design), each with a checkable rule list and a link to the matching library cards.

### 3D recipes, fallbacks and templates
ids: b009, b019, b031, b122, b144, b159, b160, b161
ground: partial. The library has three-js, react-three-fiber, postprocessing and glsl cards. No playbook or template covers the WebGL survival contract, baked fallback or accessibility.
score: value 4 · effort M · risk low · mark build (b019 is a stretch; fold it into a one-spec recipe)
brief: Write a 3D playbook with a survival contract (context loss, no GPU, reduced motion, aria), plus tested shader and procedural-mesh recipes and a CI compile check for the shaders.

### Motion tooling
ids: b008, b033, b042, b101, b148, b158
ground: new. No motion linter or filmstrip tool found. `fm smoke` (`plugin/lib/fmcli.py:5826`) only checks desktop and phone width. T-1306 covers TUI golden frames only. Medium confidence.
score: value 3 · effort M · risk low · mark build for b042, b148 and b008 (a freeze-time flag on the smoke screenshot). Mark skip for b033 (a new file format), b101 and b158 (low value, large effort).
brief: Add a motion budget check (long tasks, non-compositor properties) and sampled-frame assertions to the smoke screenshot path.

### Design tokens and palettes
ids: b015, b026, b043, b071, b076, b120, b153, b164
ground: new. The only `DESIGN.md` mention is in `fmideas.py` and `fmtidy.py`. Nothing handles OKLCH or DTCG. Medium confidence.
score: value 4 · effort M · risk low · mark build for b043, b076, b120 and b026. Mark skip for b153 and b164 (b164 needs a dev server; b153 is speculative) and b015, b071 (low value).
brief: A playbook plus a stdlib script that derives a light/dark pair from an OKLCH seed with contrast proofs, and exports the tokens as DTCG, CSS variables or Tailwind.

### Design gates (slop and distance checks)
ids: b002, b010, b129, b147, b163
ground: new. No slop detector exists. T-1159 only prints what was not verified.
score: value 3 · effort M · risk med · mark build for b002 and b010 (slop and crafted example pairs, plus a precision corpus). Mark skip for b129, b147 and b163 (a numeric fingerprint is fragile).
brief: Each design rule ships a slop/crafted pair, and a small regex slop detector is gated by a corpus.

### Visual verification and hostile conditions
ids: b007, b013, b018, b022, b027, b124, b127, b130, b157, b165
ground: partial and a false premise. `fm shot` does not exist, and `fm smoke` is the nearest (`fmcli.py:5826`; `smoke_web.cjs`, `fmsmoke.py`). The ideas that name `fm shot` mean `fm smoke`.
score: value 4 · effort M · risk med · mark build for b007, b127, b165 and b018 (content-torture, bad-screen and vision-simulation profiles in smoke). Mark skip for b027 (a local vision model adds a dependency) and b130, b157. Fold b013 and b124 into b018 (b124 is sandboxing, which T-0975 half covers).
brief: Extend `fm smoke web` with torture content, offline, slow network and colour-vision profiles.

### Taste and creative direction
ids: b003, b004, b005, b029, b040, b081, b082, b095, b096
ground: partial. `fm taste` (`fmcli.py:5908`) learns from kept and dropped work. No style or direction generator exists.
score: value 3 · effort S · risk low · mark build for b040, b095 and b096 (a style direction pick that writes `DESIGN.md`, a constraint card, an audacity dial). Mark skip for b003, b004, b005, b029, b081 and b082 (wild, or reads private files).
brief: A "directions" skill that offers six one-screen styles from a sentence and saves the chosen one as `DESIGN.md`, with an audacity level.

### Playful and wild extras
ids: b028, b053, b055, b100, b102, b104, b105, b118, b154, b167, b168, b169
ground: new. Nothing found.
score: value 1 · effort M · risk low · mark skip (low value, or off-request). Possible exception: b118, a dojo built on `fm guard try`, if wanted later.
brief: none.

### Site and release showpieces
ids: b030, b041, b080, b156, b166
ground: partial. The site build is in `site/` (build.py, pages.py).
score: value 3 · effort M · risk low · mark build for b156 and b041 (a 3D or animated hero from the task ledger) and b166. Mark skip for b030 and b080.
brief: Add an animated proof-chain hero to the site, built from `stats.json`.

### Playbook infrastructure and evals
ids: b011, b012, b014, b021, b025, b044, b045, b046, b049, b051, b056, b113, b123, b136, b137, b146, b151, b152, b171, b172, b176, b182
ground: partial. `fm cost` reports unused playbooks (`fmcost.py:1141`). `fm why` is for file history (`fmcli.py:5349`). `fm backtest` and `fm evolve` exist. T-0977 added zero-token skill triggering.
score: value 4 · effort M · risk low · mark build for b011 and b051 (a lint for contradictions and duplicates), b012, b045, b025 and b014 (route and reach evals with variance), b056 and b123 (a token ratchet), b151 and b182 (a "why not used" report), b171 (rationalisation table). Mark skip for b021, b046, b152 (costly) and b146. Fold b044, b049, b113, b136, b137, b172 and b176 into those builds; b137 is an atomic edit and probably built already.
brief: Add `fm check playbooks` with a lint, a token ratchet and a reach report.

### Non-UI playbook families
ids: b047, b048, b050, b052, b054, b170, b173, b174, b175, b178, b179, b180, b181
ground: new, partial for security. Only the review/security/release/perf/fix sets exist.
score: value 5 · effort M · risk low · mark build (skip b050 and b054, which need repo history)
brief: Write playbooks for debug and incident, migration, SQL, text/time/bytes, security, dependency admission, characterisation, deprecation, devices and decision memos.

### Config in the TUI (settings screen, profiles, live preview)
ids: b001, b016, b058, b059, b060, b061, b062, b063, b064, b065, b066, b067, b068, b069, b115, b126, b133, b142, b143, b149, b183
ground: partial. `load_config` and `print_config` read `tui.toml` (`fmcodetui.py:1906`, `1989`). There is no in-TUI settings screen, `:set`, or comment-preserving write.
score: value 5 · effort L · risk med · mark build for b126 (a `:set` line), b133 and b058 (dry-render before write), b183, b061 and b115 (auto profiles), b063 and b059. Mark skip for b016, b066, b067, b068, b069, b142, b143, b149 (the Control Room web app is a stretch) and b062, b064, b065 (premature).
brief: Add a settings screen and `:set` to `fmcodetui.py` that edits `tui.toml` in place and tries a render before it writes.

### TUI visuals and 3D
ids: b017, b039, b099, b103, b131, b132
ground: partial. T-1300 covers the truecolor renderer, and T-1311 the theme gallery.
score: value 3 · effort M · risk low · mark build for b039, b103 and b132 (half-block 3D track, riso theme, keymap poster). Mark skip for b017, b099 and b131.
brief: Add a half-block raymarched 3D station track and a riso theme to `fmcodetui.py`.

### TUI test net
ids: b134, b135, b139, b141
ground: partial. T-1306 and T-1050 already add golden frames, a fuzz, and a width sweep.
score: value 3 · effort S · risk low · mark build for b135 and b134. Mark skip for b139 and b141.
brief: A width oracle sweep over hostile strings, and crashes saved as fixtures.

### Guard and safety
ids: b020, b083, b084, b085, b087, b089, b090, b106, b107, b108
ground: partial and built. b108 is built (`fm guard try`, `fmcli.py:5387`). b084 is built (`fm bench guard`, `fmcli.py:5664`). b106 and b083 are built or partly built (`fmsecrets.py:53` `scan_diff`, `staged_leaks`). b085 is built (T-1472). b107 is built (`fm rule`, `fmcli.py:5416`).
score: value 2 · effort S · risk high · mark skip (built, or it risks weakening the guard). Possible exception: b089 (`fm doctor --wrong`), which can be checked on its own.
brief: none.

### Evidence, calibration and exports
ids: b023, b024, b057, b091, b140
ground: partial. T-1061 added a calibration ledger, and `fm backtest` exists. No noise-aware perf evidence or trace export found.
score: value 2 · effort M · risk low · mark skip for b024, b057 and b091 (built or low value). Mark build for b023 (a noise-aware perf evidence kind) and b140 (a canary that spots load flaps).
brief: Add a perf evidence kind that compares repeated runs; teach the canary to spot load flaps.

### Run records and review aids
ids: b006, b079, b086, b097, b098, b110, b111, b117
ground: partial. `fm export`, `fm pr` and T-0885 (rank changes by review risk) exist.
score: value 2 · effort M · risk low · mark skip, except b098 (a before/after wipe) and b110 (a reading path). Both can build on T-0885.
brief: A before/after view and a reading order for a UI task's receipt.

### Backlog and process
ids: b078, b092, b093, b109, b119, b138
ground: partial. T-1077 (stale plan sweep) and `fm digest` exist. T-1331 and T-1382, the earlier brainstorm tasks, are blocked.
score: value 3 · effort S · risk low · mark build for b138 (a round-convergence stop for brainstorms) and b078. Mark skip for the rest.
brief: Stop a brainstorm round when it adds no new idea.

### Scaffolds and dev loop
ids: b070, b114, b125, b128
ground: new. `fm` has `mcp new` (`fmmcp.py:292`) and no `fm new` or `fm dev`.
score: value 3 · effort M · risk low · mark build for b125 (strict templates) and b128. Mark skip for b070 and b114.
brief: Strict-by-default templates for web, 3D and TUI panels.

### Docs truth and discoverability
ids: b088, b112, b145
ground: partial. `fm help` and `fm check` (`fmcli.py:5528`) exist.
score: value 3 · effort S · risk low · mark build for b145 (a release check that documented commands still run) and b112 (answer "can Foreman do X?" from `fm help`). Mark skip for b088.
brief: A check that runs the documented command fences.

### Integrations and exports
ids: b094, b116, b150, b155
ground: new, and partial for MCP (`fm mcp`, `fmmcp.py`).
score: value 1 · effort M · risk med · mark skip
brief: none.

Unclustered: none

Risks:
- Several "near T-xxxx (done)" tags are false matches. I treated them as noise.
- "`fm shot`" is a false premise: the command does not exist and the nearest is `fm smoke`.
- I did not open the lens files. The cluster verdicts rest on the titles, a grep of `plugin/`, and task titles.

Not checked: the cards library for existing 3D, motion and token cards; the lens files; whether any open task covers b138 or b149; `mods/foreman-ui` and the `site/` internals.

Noticed: none
