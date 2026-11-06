1. **Answer**

I read the repo for only some of the 182 ideas. I checked the TUI config code, the playbook and card inventory, the open task titles, the sandbox code, and whether `fm shot`, `fm scene`, `fm img`, `fm look` and `fm flow` exist. Everything else is marked by title alone, so treat those marks as medium or low confidence.

Almost everything is new. `fm code tui` has no in-app settings screen. Config lives only in tui.toml, loaded at `~/.claude/foreman/plugin/lib/fmcodetui.py:1906` and printed by `--print-config` at `:1989`. Motion modes `full`, `reduced` and `off` already exist (`:97`). Only one UI playbook exists (`ui/terminal-ui.md`). The cards `three-js`, `react-three-fiber`, `postprocessing`, `framer-motion`, `animation`, `glsl` and `shader-performance` exist. No `fm shot`, `scene`, `img`, `look`, `flow`, `stories`, `view`, `home` or `drill` verb turned up in `fmcli.py`. Sandboxing is bwrap/sandbox-exec probing (`~/.claude/foreman/plugin/lib/fmserve.py:399`) with no Landlock. No task I scanned (T-1400 to T-1485) covers these ideas. I did not check the done tasks named in the "near" notes, so treat those matches as false until someone checks.

2. **Findings**

### Settings screen core
ids: c001, c003, c004, c005, c006, c008, c045, c116, c133, c134, c142, c144, c176
ground: new — no in-app screen; `fmcodetui.py:76` DEFAULTS and `:1906` load_config are file-only
score: value 5 · effort L · risk med · mark build
brief: Add a `fm code tui` settings overlay (search, goal groups, live preview, motion preview, detented dials, runner test) that writes tui.toml.

### Config history, diff, share, scripting
ids: c002, c007, c010, c011, c012, c013, c071, c131, c132, c135, c136, c139, c143
ground: partial — `print_config` and the `_style_error`/`_layout_error` validators exist (`:1989`); nothing else does
score: value 4 · effort M · risk low · mark build (c136 and c143 are skip: low value)
brief: Add `fm code config` get/set/diff/export/undo that writes only changed keys, flags dead settings, and gives a pasteable code.

### Config adaptive and wild
ids: c009, c023, c070, c083, c137, c138, c140, c141
ground: new
score: value 2 · effort L · risk med · mark skip (speculative; c083 glyph-width probe is the one cheap build)
brief: Build only c083, a cursor-position glyph width probe.

### Motion playbooks and cards
ids: c018, c042, c043, c127, c175, c181
ground: partial — `animation.md` and `framer-motion.md` cards exist; no motion playbook
score: value 5 · effort M · risk low · mark build
brief: Write motion-choreography, game-feel and 3D camera/easing playbooks with intensity caps.

### Motion verification gates
ids: c075, c100, c113, c117, c172, c173, c174, c178, c179, c182
ground: new — no `fm shot` and no motion lint found
score: value 3 · effort L · risk med · mark build only c075 and c173 (token lint, reduced-motion check); the rest skip (they need a browser or video stack)
brief: Add a stdlib lint for motion tokens and reduced-motion parity in generated CSS.

### TUI motion behaviour
ids: c050, c177, c180
ground: partial — `MOTIONS` (`:97`) already covers a hush; a state tempo is new
score: value 3 · effort S · risk low · mark build c177 and c180; c050 skip
brief: Bind a hush key to cycle motion and slow the spinner tempo by agent state.

### 3D playbooks and lints
ids: c017, c046, c107, c120, c160, c164, c166, c167
ground: partial — `three-js`, `react-three-fiber` and `postprocessing` cards exist; no playbook
score: value 4 · effort M · risk low · mark build c120, c166, c167, c107 (playbook plus static lint); skip c017, c046, c160, c164 (need a headless GPU)
brief: Write a WebGL black-screen triage playbook and a static lint for scene.json (poster fallback, reduced-motion, camera blocking data).

### 3D scene tooling
ids: c031, c063, c074, c095, c110, c111, c159, c162, c171
ground: new
score: value 3 · effort L · risk med · mark build c110 and c159 (half-block rasteriser, `fm scene` JSON); the rest skip (c031 is a large PNG codec for little gain)
brief: Add a stdlib half-block solid rasteriser for the station track, and a scene.json spec verb.

### 3D showpieces
ids: c022, c047, c059, c104, c114, c168, c169, c170
ground: new
score: value 2 · effort L · risk med · mark skip (c114, the site hero, is the one on-request build and fits `site/`)
brief: c114 only: a canvas subway-map hero on the site fed by the task ledger.

### Visual QA and screenshots
ids: c032, c041, c052, c053, c054, c055, c056, c062, c067, c068, c069, c084, c085, c089, c090, c092, c097, c150, c161
ground: new — no `fm shot`, `fm flow` or `fm stories` verb found; site self-hosts fonts (T-1411, done)
score: value 3 · effort L · risk med · mark build c150 (visual-proof playbook), c056 (CSS lint), c089 (seeded-random lint); skip the rest (browser dependency)
brief: Write a visual-proof playbook with receipts, a stdlib CSS architecture lint, and an unseeded-randomness lint.

### Design craft: brief, slop, de-default
ids: c040, c049, c065, c066, c072, c078, c096, c105, c109, c119, c121, c122, c146, c147, c163
ground: partial — one UI playbook only
score: value 5 · effort M · risk low · mark build (c049 and c147 as a stdlib generic-tell lint; skip c072, c096, c109)
brief: Write the Look Grammar, taste (look, motion, light), de-default, layout-rhythm and state-atlas playbooks, plus a brief-first UI chain.

### Design recipes and specimens
ids: c016, c057, c064, c106, c108, c112, c125, c165
ground: new
score: value 4 · effort M · risk low · mark build c106, c108, c125, c165 (text recipes and cards); skip c016, c057, c064, c112
brief: Add a light-and-material recipe shelf, a typography-as-texture playbook, an SVG icon system playbook and shader look cards.

### Taste and wild style ideas
ids: c024, c037, c044, c051, c077, c079, c115, c155
ground: new
score: value 2 · effort M · risk med · mark skip (c079 five-idiom layouts could be a playbook section)
brief: none.

### Language, domain and sound playbooks
ids: c015, c020, c021, c025, c058, c060, c061, c094, c098, c102, c118, c123, c124, c126, c130
ground: partial — build playbooks exist only for cpp, rust and typescript, and lang only for cpp, rust and python
score: value 5 · effort M · risk low · mark build (c025 skip as a runtime feature; c061 and c130 merge into one sound playbook, off by default)
brief: Write the Go/JVM/Swift/C#/shell build, test-craft, deck/report, docs, scrollytelling, loading-choreography, stdlib-Python, demo-production and sound playbooks.

### Playbook machinery
ids: c073, c093, c099, c128, c129, c145, c148, c149, c151, c152, c153, c154, c156, c157, c158
ground: new — no router, overlay or blame code found
score: value 3 · effort M · risk low · mark build c148, c151, c153, c158 (eval pair, playbook-writing playbook, `fm code` one-line intake, contradiction check); skip the rest
brief: Add a playbook linter for contradiction and token budget, and a one-line costed playbook intake in `fm code`.

### Safety, ratchet and gate hygiene
ids: c027, c028, c033, c080, c081, c082, c086, c087, c088, c091
ground: partial — an evasion corpus exists (T-1263, T-1482, T-1483); no allow-corpus or Landlock found
score: value 4 · effort M · risk med · mark build c028, c033, c080, c081, c087; skip c027 (ctypes Landlock), c086, c088, c091
brief: Add an allow-corpus of harmless commands the guard must pass, lock the guard files against `fm evolve`, and add a pass/fail/unable result to checks.

### Workflow, state and misc
ids: c014, c019, c026, c029, c030, c034, c035, c036, c038, c039, c048, c076, c101, c103
ground: new, unchecked against the done tasks they resemble
score: value 2 · effort M · risk low · mark skip (c029 premise probe, c101 spike rule and c034 `fm home` are the cheapest builds; c076 Figma MCP is unsafe)
brief: none.

Unclustered: none

3. **Risks / surprises**
- I did not open any lens file. All "wild" ideas are judged by title.
- Most "near T-xxxx" notes looked false (word overlap only), but I verified none.
- Counts per cluster sum to 182, but I did not machine-check that the ids are unique.

4. **Not checked**
- Lens-file details.
- The `fmcli.py` verb table beyond a few greps.
- The `mods/foreman-ui` and `site/` code.
- The evals directory.
- The remaining 15 frontend/web/games cards.

**Noticed:** none
