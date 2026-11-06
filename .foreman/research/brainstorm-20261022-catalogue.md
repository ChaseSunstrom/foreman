# Brainstorm 2026-10-22 (T-1479): catalogue

Request: "super recursive brainstorm and improve foreman, way more skills/playbooks/way better more capable code, config in the tui, … way better/way more UI design skills with 3d, good animations, non generic stuff, styles".
Run: research/brainstorm-20261022-120901 (10 lenses × 4 rounds + 3 deepen rounds, --seen the three previous brainstorms), 548 distinct ideas. Every idea was grounded by one of three fm-recon passes (batch files t1479-ideas-a/b/c: ids a001–a183, b001–b183, c001–c182). Every id is in exactly one cluster below. Clusters were merged across the batches into 26 capabilities.

Ground truth: 48 playbooks, one of them UI (ui/terminal-ui.md). Cards for three.js, R3F, postprocessing, GLSL and animation exist, but no playbook teaches taste, motion or 3D. The fm code app is configured only by hand-edited tui.toml (load_config fmcodetui.py:1906). No design or slop gate exists. fm smoke (not "fm shot") is the screenshot path. The site has no WebGL. Most "near T-…" matches were word overlap only.

Score key: value 1–5 · effort S/M/L · risk.

## Build: round 1
1. **UI design-direction playbook family** (value 5 · M · low). ids a001 a028 a041 a051 a077 a101 a105 a040 a163 a133 a179 a182 a006 a129 a142 a162 b032 b034 b035 b036 b037 b038 b072 b073 b074 b075 b077 b121 b162 b177 c040 c065 c066 c078 c105 c119 c121 c122 c146 c163.
   - Ground: new; only ui/terminal-ui.md exists.
   - Tasks: direction (point of view first, look bank, taste-word→knob table, three-question interview, audacity dial, defaults to avoid, DESIGN.md out); type and colour; composition, depth and states; interaction, forms and microcopy.
2. **Motion playbook family** (5 · M · low). ids a005 a032 a090 a102 a027 a012 c018 c042 c043 c127 c175 c181.
   - Ground: new; cards only.
   - Tasks: motion choreography (timing vocabulary, state→motion table, storyboard first, reduced motion, loading choreography that never blocks LCP); game feel (juice with intensity caps).
3. **3D playbook family and zero-dependency template** (5 · M · low). ids a003 a017 a031 a044 a056 a091 a103 b009 b019 b031 b122 b144 b159 b160 b161 c107 c120 c166 c167.
   - Ground: partial; cards exist, no playbook.
   - Tasks: scene composition (camera, light and material, perf budget, survival contract: context loss, no GPU, reduced motion, aria); single-file scene template; black-screen triage.
4. **fm check design: a stdlib generic-tell and craft lint** (4 · M · low). ids a002 a015 a029 a042 a106 a153 a066 a021 a108 a140 a166 b002 b010 b042 c049 c147 c056 c089 c075 c173.
   - Ground: new.
   - Rules: default font stacks, the purple gradient, one radius everywhere, missing alt, contrast, no prefers-reduced-motion, animation of non-compositor properties, flash rate, unseeded randomness, motion tokens.
   - Each rule has a slop/crafted fixture pair.
5. **TUI settings: schema, comment-preserving writer, dry render** (5 · M · med). ids a064 a116 a119 b058 b059 b063 b133 c002 c007 c071.
   - Ground: new.
6. **TUI settings screen** (5 · L · med). ids a057 a080 a114 a123 a154 a168 a115 a135 a164 b001 b126 b183 c001 c003 c004 c005 c006 c008 c045 c116 c133 c134 c142 c144 c176.
   - An overlay with search, groups, a takes-effect badge, a modified-only view, live preview, revert in 10 s, and a :set line.
7. **Style shelf: original style and shader-look cards** (4 · M · low). ids a033 a078 a111 a092 c106 c108 c125 c165.
   - About 12 named looks and about 8 shader looks, plus light-and-material recipes and an SVG icon system.
8. **Visual QA playbook** (4 · M · low). ids a004 a016 a030 a043 a053 a093 a104 a130 a150 a156 a170 a183 c150.
   - Three viewports through fm smoke, an eyeball card, receipts.
9. **Design critic lens with three personas** (4 · S · low). ids a011 a020 a036 a037 a047 a062 a094 a113.
10. **Non-UI playbooks** (5 · M · low). ids a007 a046 a107 a173 b047 b048 b052 b170 b173 b174 b175 b178 b179 b180 b181 c015 c020 c021 c058 c060 c094 c098 c102 c118 c123 c124 c126 c061 c130.
    - Data-viz, incident/ops, observability; Go/JVM/Swift/C#/shell build; test craft; SQL; migration; text/time/bytes; dependency admission; characterisation; deprecation; decision memos; docs; decks and reports; scrollytelling; stdlib Python; demo production; sound (off by default).
11. **fm check playbooks** (4 · M · low). ids a008 a067 b011 b051 b012 b045 b025 b014 b056 b123 b151 b182 b171 b044 b049 b113 b136 b137 b172 b176 c148 c151 c158.
    - A lint for contradictions and duplicates, a token ratchet, an eval case per playbook, a "why not used" reach report, and a playbook for writing playbooks.

## Build: round 2
12. **Design tokens: extract and OKLCH palettes** (4 · M · low). ids a010 a025 a035 a045 a058 a083 a088 a097 a109 a141 b043 b076 b120 b026.
    - A DESIGN.md from CSS custom properties, a light/dark pair from a seed with contrast proofs, DTCG/CSS/Tailwind export.
13. **Directions skill** (3 · S · low). ids b040 b095 b096.
    - Six one-screen styles from a sentence; the pick is saved as DESIGN.md with an audacity level.
14. **fm smoke hostile profiles** (4 · M · med). ids b007 b013 b018 b124 b127 b165 b008 b148.
    - Torture content, offline, slow network, colour-vision simulation, freeze time, sampled frames.
15. **fm code config CLI** (4 · M · low). ids c010 c011 c012 c013 c131 c132 c135 c139.
    - get/set/diff/export/undo, writes only changed keys, flags dead settings, pasteable share code.
16. **Key, layout and runner editors in the app** (3 · M · low). ids a118 a120 a121 a124 a125. After 6.
17. **TUI motion and visuals** (3 · S–M · low). ids c177 c180 c083 c110 b039 b103 b132.
    - A hush key cycles motion; spinner tempo by state; a glyph-width probe; a half-block 3D station track; a riso theme; a keymap poster.
18. **Site proof-chain hero** (3 · L · med). ids a013 a095 c114 b156 b041 b166.
    - A single-file WebGL or canvas hero fed by stats.json, with a static fallback and reduced motion.
19. **UI direction nudge** (3 · S · med). ids a014 a052.
    - A soft hook note asking for a design direction before UI files are edited. It never blocks.
20. **Terminal-UI playbook expansion** (3 · S · low). ids a009.
    - Display width, resize, motion, and CLI product design (b177 is folded into 1).
21. **TUI test net** (3 · S · low). ids b134 b135.
    - A width-oracle sweep over hostile strings; crashes are saved as fixtures.
22. **Safety ratchet** (4 · M · med). ids c028 c033 c080 c081 c087.
    - An allow-corpus of harmless commands the guard must pass, guard files locked against fm evolve, a pass/fail/unable check result.
23. **Evidence and review aids** (3 · M · low). ids b023 b140 b098 b110.
    - A noise-aware perf evidence kind; the canary spots load flaps; a before/after wipe and a reading order for UI receipts.
24. **Scaffolds and docs truth** (3 · M · low). ids b125 b128 b145 b112 a068.
    - Strict templates for web, 3D and TUI panels; a release check that runs documented command fences; "can Foreman do X?" answered from fm help; a verified: field on cards.

## Skipped, each with its reason
25. **Built already, or would weaken the guard.** ids b020 b083 b084 b085 b087 b089 b090 b106 b107 b108 b138.
    - fm guard try, fm bench guard, fmsecrets scan_diff, T-1472 and fm rule exist; fm ideas --dry already stops a dry round.
26. **Heavy, off-request or speculative.** Each needs a browser or GPU stack, a new dependency or a live server, or is wild with low value:
    - a019 a026 a055 a081 a082 a110 a178 (evals: duplicate T-0752/T-1070)
    - a061 a084 a158 (motion player/lab pages)
    - a074 a155 a167 a181 (three renderers, GPU soak tests, asset validators)
    - a096 a171 (animated-chart generator, codemod verb)
    - a039 a087 a131 a148 a180 (hard UI blocks)
    - a165 a169 a174 a175 (browser-baseline lints)
    - a079 a147 a149 a151 a176 (fm shot, which needs a browser dependency)
    - a054 a086 a098 a159 a177 a137 a048 (tournaments)
    - a023 a024 a038 a050 a100 a112 a139 a152 a157 a161 (galleries, live servers, thumbnails)
    - a022 a059 a089 a132 (separate packaging)
    - a128 a134 a136 a144 a146 (taste extras)
    - a034 a049 a076 a085 a138 a160 (showcase extras)
    - a018 a060 a099 (terminal rasterizer novelty; a cheaper one is c110 in 17)
    - a063 a075 a117 a122 a126 a127 (settings macros)
    - a065 a070 a071 a072 a073 a145 (repo infrastructure)
    - a143 a172 (font-binary shelf)
    - b003 b004 b005 b029 b081 b082 (wild, or read private files)
    - b015 b071 b153 b164 (token extras)
    - b016 b062 b064 b065 b066 b067 b068 b069 b142 b143 b149 (a web control room, premature)
    - b017 b099 b131 b139 b141
    - b021 b046 b146 b152 (costly evals)
    - b024 b057 b091 (calibration: built in T-1061)
    - b027 b130 b157 (a local vision model)
    - b028 b053 b055 b100 b102 b104 b105 b118 b154 b167 b168 b169 (playful extras)
    - b030 b080 b033 b101 b158 b129 b147 b163 b050 b054 b070 b114 b088 b006 b079 b086 b097 b111 b117 b078 b092 b093 b109 b119 b094 b116 b150 b155 b060 b061 b115 b126
    - c009 c023 c070 c137 c138 c140 c141 (adaptive config)
    - c016 c057 c064 c112 (recipes needing assets)
    - c017 c046 c160 c164 (need a headless GPU)
    - c022 c047 c059 c104 c168 c169 c170 (3D showpieces)
    - c024 c037 c044 c051 c077 c079 c115 c155 (wild taste; c079 becomes a section of 1)
    - c025 (runtime sound)
    - c027 (ctypes Landlock) c086 c088 c091
    - c031 c063 c074 c095 c111 c162 c171 (3D tooling)
    - c050 c072 c096 c109
    - c032 c041 c052 c053 c054 c055 c062 c067 c068 c069 c084 c085 c090 c092 c097 c161 (browser stack)
    - c100 c113 c117 c172 c174 c178 c179 c182 (video stack)
    - c073 c093 c099 c128 c129 c145 c149 c152 c153 c154 c156 c157 (playbook machinery extras)
    - c014 c019 c026 c029 c030 c034 c035 c036 c038 c039 c048 c076 c101 c103 (workflow; c076, a Figma MCP, is unsafe)
    - c136 c143

Note: b061 and b115 (automatic profiles) and b126 (:set) are in 6. c049 and c147 are in 4. b177 is in 1.
