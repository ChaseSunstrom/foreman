Ground truth for the whole batch, from the repo.

- **Playbooks:** the repo has 48 playbooks and only one is UI (`terminal-ui.md`).
- **`fm check`:** it runs gates the user adds. It has no design, UI or slop gate.
- **`fm` verbs:** there is no `fm shot`, `fm fsck`, `fm design` or `fm codemod`. Verbs that do exist are `fm page` (`plugin/lib/fmpage.py:133`), `fm taste` (`fmideas.py:536`), `fm repeats`, `fm backtest` and `fm lib`.
- **`fm code` TUI config:** it is file-only. `load_config` is at `plugin/lib/fmcodetui.py:1906` and `print_config` at `:1989`. There is no in-app settings screen.
- **Screenshots:** `mods/foreman-ui/tools/shot.py` takes tmux-to-PNG snapshots of the Claude Code UI.
- **Cards:** the 3D, motion and shader cards exist (`web/three-js`, `web/react-three-fiber`, `web/postprocessing`, `games/glsl`, `frontend/animation`, `frontend/accessibility`).
- **Site:** I found no WebGL on the site. A combined search returned 1 hit each in `site.js`, `pages.py` and `style.css`, but a follow-up search for `canvas|webgl` returned nothing, so treat this as medium confidence.
- **Near-task labels:** every "near T-xxxx (done)" label I checked was a false match on shared words, not a real overlap.

### Design-direction and taste playbook family
ids: a001, a028, a041, a051, a077, a101, a105, a040, a163, a133, a179, a182
ground: new. Only `ui/terminal-ui.md` exists under `plugin/skills/playbooks/references/ui/`.
score: value 5 · effort M · risk low · mark build
brief: write a `ui/` playbook family (direction, type and colour, accessibility with flair, before/after exemplars) and point it at the upstream frontend-design skill instead of rivalling it (a179).

### Motion choreography playbook and tokens
ids: a005, a032, a090, a102, a027, a012, a084, a061, a158
ground: new. The motion cards exist, and the TUI has a motion setting (T-1300, T-0912).
score: value 4 · effort M · risk low · mark build for a005, a032, a090, a102, a027 and a012; skip a084, a061 and a158 (they need a player or lab page, low value).
brief: write `ui/motion.md` with a timing vocabulary, a state-to-motion table and storyboard-first steps.

### 3D scene playbook and recipes
ids: a003, a017, a031, a044, a056, a091, a103, a155, a181, a074, a167
ground: partial. The three.js, R3F and glsl cards exist, but there is no playbook.
score: value 5 · effort M · risk low · mark build for a003, a017, a031, a044, a056, a091 and a103; skip a155, a181, a074 and a167 (three renderers, GPU soak tests and offline asset validators are heavy).
brief: write `ui/scene-3d.md` with a perf budget and a zero-dependency single-file template.

### Playbook gaps beyond UI (data-viz, ops, codemod)
ids: a007, a046, a096, a107, a173, a171
ground: new. None of these stages has a playbook.
score: value 4 · effort M · risk low · mark build for a007, a046, a107 and a173; skip a171 (a codemod verb) and a096 (animated SVG charts generator).
brief: add data-viz, incident/ops and observability playbooks.

### Playbook evals and A/B lift
ids: a008, a019, a055, a067, a081, a178, a082, a110, a026
ground: partial. Evals exist (`plugin/evals/`), and T-0752 added evals on block and a bench holdout. `fm repeats` drafts skills, as in T-1070.
score: value 3 · effort M · risk low · mark build for a008 and a067 (a test that each new playbook has an eval case); skip the rest (they duplicate T-0752/T-1070 or add heavy infrastructure).
brief: add a docs test requiring an eval case per playbook file.

### Slop and anti-generic detector
ids: a002, a015, a029, a042, a106, a153, a066
ground: new. Nothing like it exists in the `fm check` code (`fmcli.py:3542-3640`).
score: value 4 · effort M · risk low · mark build
brief: add a stdlib `fm check design` that scans CSS and HTML for generic tells (default font stacks, purple gradients, uniform radius and so on), with its rules listed in the playbook.

### UI gates and contracts
ids: a014, a052, a039, a087, a131, a148, a180
ground: new. The guard and hook layer has no UI gate.
score: value 3 · effort M · risk med · mark build for a014 and a052 as soft prompts only; skip hard blocking and the rest.
brief: add a hook nudge to name a design direction before editing UI files.

### Static lints (accessibility, flash safety, compositor safety, browser baselines)
ids: a021, a108, a140, a165, a166, a169, a174, a175
ground: new
score: value 3 · effort M · risk low · mark build for a021, a108, a140 and a166, folded into the `fm check design` rules; skip a165, a169, a174 and a175.
brief: the lint rules cover contrast, missing alt text, `prefers-reduced-motion`, flash rate and animation of non-compositor properties.

### Screenshot and visual proof loop
ids: a004, a016, a030, a043, a053, a079, a093, a104, a130, a150, a156, a170, a183, a147, a149, a151, a176
ground: partial. `mods/foreman-ui/tools/shot.py` and `plugin/lib/fmsmoke.py` with `smoke_web.cjs` do headless web capture.
score: value 4 · effort L · risk med · mark build for a104, a016 and a130 as a playbook (screenshots at three viewports from a seeded fixture, plus an eyeball card). Skip a079 `fm shot` as a new verb because it needs a browser dependency. Skip the others.
brief: write `ui/visual-qa.md` reusing the smoke harness.

### Design critic and style tournament
ids: a011, a020, a036, a037, a047, a062, a094, a113, a054, a086, a098, a159, a177, a137, a048
ground: partial. `plugin/agents/fm-reviewer.md` exists, and T-1069 is racing builders.
score: value 4 · effort S · risk low · mark build for a094, a113, a020 and a047 (a design-critic lens with three personas, added to the playbook and the reviewer); skip the rest.
brief: add a design-critic lens to the reviewer agent.

### Style shelf and lookbook
ids: a033, a078, a112, a152, a038, a023, a100, a111, a161, a024, a092, a050, a157, a139
ground: new
score: value 4 · effort M · risk low · mark build for a033, a078 (named styles as library cards) and a111 and a092 (original shader looks as cards); skip the galleries, live server and thumbnails.
brief: add about 12 original style cards and about 8 shader-look cards under `library/cards/frontend`.

### Design tokens and reference extraction
ids: a010, a025, a035, a045, a058, a083, a088, a097, a109, a141, a022, a089, a132, a059
ground: partial. T-0378 only exempts the guard for token files. There is no extractor.
score: value 3 · effort M · risk low · mark build for a045, a058 and a109 (a DESIGN.md from the repo's own CSS, plus a reference teardown skill); skip the rest. a059 is skipped because a separate plugin splits packaging.
brief: add a `design-extract` skill that derives a DESIGN.md from CSS custom properties.

### Taste interview and vague-word translation
ids: a006, a128, a129, a142, a144, a146, a162, a134, a136
ground: partial. `fm taste` exists (T-0112, T-0655) and `fm ideas` expands requests.
score: value 3 · effort S · risk low · mark build for a129 and a142 (a taste-word-to-knob table in the playbook) and a006 and a162 (an interview step); skip the rest.
brief: add the taste-word table and a three-question interview to the design playbook.

### Site and showcase
ids: a013, a034, a049, a095, a085, a138, a160, a076
ground: new. The site has no WebGL.
score: value 3 · effort L · risk med · mark build for a013 and a095 (a hand-written WebGL hero for the site); skip the others.
brief: add a single-file WebGL hero to `site/` with a static fallback and reduced-motion support.

### Terminal 3D rasterizer and terminal-UI playbook
ids: a009, a018, a060, a099
ground: partial. `ui/terminal-ui.md` exists, and the TUI has a truecolor renderer (T-1300).
score: value 3 · effort M · risk low · mark build for a009 (expand the playbook); skip the rasterizer ideas, which are novelty.
brief: expand `terminal-ui.md` with display-width, resize and motion notes.

### In-app settings screen
ids: a057, a080, a114, a116, a123, a154, a168, a064, a122, a119, a117
ground: new. Config is file-only (`fmcodetui.py:1906-2000`).
score: value 5 · effort L · risk med · mark build for a080, a116, a119 and a123 (a schema-driven settings screen with a takes-effect badge, a modified-only view and a dead-setting check). Build a064 as a standalone fix (preserve comments on save). Skip the rest.
brief: add a settings panel to `fmcodetui` generated from one schema list.

### Settings safety and macros
ids: a063, a115, a135, a127, a126, a164, a075
ground: partial. Motion off exists as a setting; hush is one key.
score: value 3 · effort S · risk low · mark build for a115, a135 and a164, as a revert-in-10-seconds prompt; skip the rest.
brief: after a setting changes, show a preview and revert after 10 seconds without a keypress.

### Key, layout and runner editors
ids: a118, a120, a121, a124, a125
ground: partial. `[keys]` config exists (`fmcodetui.py:1960`).
score: value 2 · effort M · risk low · mark skip (low value before the settings screen exists)

### Repo hygiene and infrastructure
ids: a065, a068, a070, a071, a072, a073, a145
ground: partial. The guard corpus exists (T-1263).
score: value 2 · effort M · risk low · mark skip (off-request for this brainstorm), except a068, build (a verified-at line on cards)
brief: add a `verified:` field to card frontmatter.

### Fonts
ids: a143, a172
ground: partial. The site self-hosts fonts (T-1411).
score: value 2 · effort M · risk low · mark skip (needs a font-binary shelf)

Unclustered: none

**Risks / surprises:** I searched the repo for gaps, not for every duplicate. Cluster membership for a164 and a145 is a judgement call. The site WebGL finding is medium confidence. I did not run anything or read any lens files.

**Not checked:** the lens files, `fmideas` deduplication, byte-reproducible builds, `fm doctor` rendering checks.

**Noticed:** none
