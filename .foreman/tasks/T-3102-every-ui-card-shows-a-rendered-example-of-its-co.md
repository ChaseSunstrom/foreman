---
id: T-3102
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/sampo/smallcards.py, plugin/lib/sampo/works.py, plugin/templates/ui-kit.html, plugin/tests/test_site_build.py, plugin/tests/test_small_cards.py, research/ui-card-examples.md, site/build.py, site/cards.js, site/sections.css, CHANGELOG.md]
depends_on: [T-3106]
source: user
created: 2026-11-05T03:05:43Z
updated: 2026-11-05T18:39:55Z
rival_at: 2026-11-05T17:32:16Z
rival_split: true
builder_model: opus
base: 98a29e7fc0cf154a29032fa8d4981e9e886c433b
base_tree: 74b4a042feb34ab79c0e007584cdf2c9253424dd
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-11-05T17:32:39Z
plan0_scope: []
base_note: Calibration: this plan states Choice 75% where FEATURE M closes (651) held on the first finish 98% of the time: 23 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
builder_returned: 2026-11-05T18:12:42Z
lane_stop: merged 2026-11-05T18:26:19Z
verified: strong
unproven: [docs, ui-unshot]
lane_verified: 4d4e2d46275cf0fb4a52dabdf1d50902169d2cec
---
# Every UI card shows a rendered example of its component: a checked card-specific one where it exists, else its component's kit demo (T-3100 part 2)
## Raw request
> Every UI card shows a rendered example of its component: a checked card-specific one where it exists, else its component's kit demo (T-3100 part 2)
## Interpretation
Reading 1 (chosen): a local model writes one static HTML and CSS snippet per UI card (the card's component, platform look and concern, from its steps and example; no script, no external URL), kept in state/cards/examples.jsonl only when a headless render passes (not blank, no sideways overflow at 390 px, body text at 4.5:1 or more in light and dark, under 12 KB), and the Cards page shows it in a sandboxed iframe (srcdoc, no allow-scripts); a card with no kept example shows a handmade kit demo of its component (16 components, both themes). Reading 2: screenshots per card; rejected, thousands of images and none follow the theme.
## Assumptions (confidence)
## Acceptance criteria
- [x] sampo playbooks small examples --grid ui writes examples with a local model, keeps one only when its render check passes (not blank, no overflow at 390 px, 4.5:1 text in both themes, under 12 KB, no script or external URL after sanitising), and records why each rejected one failed — verify with `python3 plugin/tests/run.py test_small_cards`
- [x] the Cards page shows each UI card's kept example in a sandboxed iframe without scripts, else its component's kit demo; all 16 components have a kit demo in both themes — verify with `python3 plugin/tests/run.py test_site_build`
## Non-goals
## Approach (options → choice → why)
1. Use what exists: the cards' own example text as the brief, the local writers moons and cards already use, a headless render check like the site's shot tools, a 16-component kit as the floor; likely outcome: every UI card shows something on day one and card-specific examples grow. 2. Do less: the kit demos only; fails if: a 'loading state of a Svelte table' card shows a generic table. 3. Examples written by Haiku; fails if: 3,000+ paid calls when local models write HTML well enough to pass a render check. Choice 1 (75%)
## Risks and rollback
Blast radius (sampo graph blast): unknown, no co-change history for state/cards/examples.jsonl.
## Execution prompt
## Steps
1. [x] failing tests: the sanitiser (script, on* handlers, external URLs dropped), the render check verdicts, kept and rejected rows, the kit fallback
2. [x] the examples writer and check in smallcards, the 16-component kit, the iframe on the Cards page
3. [x] a live run over the UI grid with a local model; kept and rejected counts in research
## Resume here
<!-- auto -->
- 2026-11-05T17:52:09Z step 1/3: failing tests: the sanitiser (script, on* handlers, external URLs dropped), the render check verdicts, kept and rejected rows, the kit fallback
- git: worktree-agent-a985e8bc3dc323b7c; 6 uncommitted: plugin/lib/sampo/smallcards.py, plugin/lib/sampo/works.py, plugin/tests/test_site_build.py, plugin/tests/test_small_cards.py, site/build.py, plugin/templates/ui-kit.html
- touched since last checkpoint: plugin/lib/sampo/works.py, plugin/templates/ui-kit.html, plugin/lib/sampo/smallcards.py, site/build.py
## Docs impact
CHANGELOG line; research/ui-card-examples.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_small_cards` → ✗ exit 1 · Ran 29 tests in 3.8s (6 jobs, 16 at a time; slowest: Admit 3s, Grow 3s, Examples 3s) / FAILED (2 classes: test_small_cards.Examples, test_small_cards.ExamplesRendered) [ran] [tree de8b7ea4e734] [world 2f1906870a] (2026-11-05T17:44:09Z)
- (ac 1) `python3 plugin/tests/run.py test_small_cards 2>&1 | grep -A20 "^ERROR\|^FAIL:\|^Ran .* jobs" | head -40` → exit 0 · Ran 29 tests in 11.9s (7 jobs, 16 at a time; slowest: ExamplesRendered.test_every_component_has_a_kit_demo_that_passes_in_both_themes 11s, ExamplesRendered.test_blank_overflow_and_faint_text_fail_and_ [ran] [tree fec4cf429fb2] [world 2f1906870a] (2026-11-05T17:51:46Z)
- (ac 2) `python3 plugin/tests/run.py test_site_build 2>&1 | tail -25` → exit 0 · Ran 28 tests in 15.1s (13 jobs, 16 at a time; slowest: CardsPage 14s, Landing 5s, Reproducible 3s) / OK [ran] [tree 33a761a865a1] [world 2f1906870a] (2026-11-05T17:54:01Z)
- (step 2) `python3 plugin/tests/run.py test_site_build test_small_cards test_design_works` → exit 0 · Ran 82 tests in 16.2s (34 jobs, 16 at a time; slowest: CardsPage 15s, ExamplesRendered.test_every_component_has_a_kit_demo_that_passes_in_both_themes 13s, Rendered.test_cards_low_contrast_and_scripted [ran] [tree 4703493c3700] [world 2f1906870a] (2026-11-05T17:55:37Z)
- (ac 1) `python3 plugin/tests/run.py test_small_cards 2>&1 | tail -3` → exit 0 · Ran 29 tests in 14.7s (7 jobs, 16 at a time; slowest: ExamplesRendered.test_every_component_has_a_kit_demo_that_passes_in_both_themes 14s, Admit 4s, UiGrid 4s) / OK [ran] [tree 7e00776bc776] [world 2f1906870a] (2026-11-05T18:02:43Z)
- (step 3) `python3 plugin/tests/run.py test_small_cards 2>&1 | tail -3` → exit 0 · Ran 29 tests in 14.7s (7 jobs, 16 at a time; slowest: ExamplesRendered.test_every_component_has_a_kit_demo_that_passes_in_both_themes 14s, Admit 4s, UiGrid 4s) / OK [ran] [tree 7e00776bc776] [world 2f1906870a] (2026-11-05T18:02:43Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_bench_family test_code_tui test_design_gates test_design_lint test_design_sprint test_design_works test_docs test_doctor test_fmpy test_genesis test_goal test_left_out test_library test_map test_models test_moons_scale test_moonshot test_motion_verify test_rename_scan test_replay test_sampo_design test_scene test_ship test_ship_next test_showpieces test_site test_site_build test_site_hero test_site_landing test_site_sampo test_site_sections test_small_cards test_steer test_suite_hygiene test_taste_ledger && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 173 tests across 6 files. [45.95s] [ran] [tree 7e00776bc776] [world 2f1906870a] (2026-11-05T18:02:57Z)
- (step 3) `python3 plugin/bin/sampo playbooks small examples --grid ui --max-calls 4` → exit 0 · Card examples: 4 call(s), 4 kept, 0 rejected; stopped: max_calls; jarvis-nothink 3, jarvis 1 [ran] [tree 3173f6f166f6] [world 2f1906870a] (2026-11-05T18:12:15Z)
- (step 1) `python3 plugin/tests/run.py test_small_cards test_site_build test_design_works` → ✗ exit 1 · Ran 84 tests in 36.1s (51 jobs, 16 at a time; slowest: ExamplesRendered 30s, CardsPage 20s, Rendered.test_the_text_report_names_each_gate_with_its_number 13s) / FAILED (1 classes: test_design_works.St [ran] [tree 33f919f7d662] [world 2f1906870a] (2026-11-05T18:29:34Z)
- `python3 plugin/tests/run.py test_small_cards test_site_build` → ✗ exit 1 · Ran 50 tests in 13.2s (19 jobs, 16 at a time; slowest: Landing 7s, Reproducible 4s, Admit 4s) / FAILED (4 classes: test_site_build.CardsPage, test_small_cards.Examples, test_site_build.CardsDemo, test (start tree + this task's tests) [ran] [tree 33f919f7d662] [world 2f1906870a] (2026-11-05T18:30:10Z)
- `python3 plugin/tests/run.py test_small_cards test_site_build` → exit 0 · Ran 57 tests in 18.6s (36 jobs, 16 at a time; slowest: CardsPage 17s, ExamplesRendered.test_every_component_has_a_kit_demo_that_passes_in_both_themes 17s, ExamplesRendered.test_blank_overflow_and_fain [ran] [tree 33f919f7d662] [world 2f1906870a] (2026-11-05T18:30:10Z)
- (step 1) `python3 plugin/tests/run.py test_small_cards test_site_build test_design_works` → exit 0 · Ran 84 tests in 18.9s (66 jobs, 16 at a time; slowest: ExamplesRendered.test_every_component_has_a_kit_demo_that_passes_in_both_themes 18s, CardsPage 17s, Rendered.test_the_text_report_names_each_gate [ran] [tree 33f919f7d662] [world 2f1906870a] (2026-11-05T18:31:01Z)
- (ac 1) `python3 plugin/tests/run.py test_small_cards` → exit 0 · Ran 29 tests in 15.1s (23 jobs, 16 at a time; slowest: ExamplesRendered.test_every_component_has_a_kit_demo_that_passes_in_both_themes 14s, ExamplesRendered.test_blank_overflow_and_faint_text_fail_and [ran] [tree 33f919f7d662] [world 2f1906870a] (2026-11-05T18:31:47Z)
- (ac 2) `python3 plugin/tests/run.py test_site_build` → exit 0 · Ran 28 tests in 15.7s (18 jobs, 16 at a time; slowest: CardsPage 15s, Reproducible 3s, NoBareNulls 3s) / OK [ran] [tree 33f919f7d662] [world 2f1906870a] (2026-11-05T18:31:47Z)
- (audit intent) `builder self-review plus my spot-checks before queueing: the frame is sandbox="" (no scripts, no same-origin) and the example is re-sanitised from a parse of known elements and attributes; merged by the queue; first evidence run went red once under load 60 then green twice (a render-timing flake, class not named)` → each UI card shows its own kept example, else its component's kit demo; 13 of 16 tried were kept [tree 33f919f7d662] (2026-11-05T18:31:47Z)
- (audit adversary) `builder self-review plus my spot-checks before queueing: the frame is sandbox="" (no scripts, no same-origin) and the example is re-sanitised from a parse of known elements and attributes; merged by the queue; first evidence run went red once under load 60 then green twice (a render-timing flake, class not named)` → script, on* handlers and every URL but #… and data:image are stripped and fail safe; the frame's CSP loads nothing [tree 33f919f7d662] (2026-11-05T18:31:47Z)
- (audit edge) `builder self-review plus my spot-checks before queueing: the frame is sandbox="" (no scripts, no same-origin) and the example is re-sanitised from a parse of known elements and attributes; merged by the queue; first evidence run went red once under load 60 then green twice (a render-timing flake, class not named)` → a bad kit.json or demo shows no example rather than breaking the card; reruns skip kept cards, at most 3 tries a card [tree 33f919f7d662] (2026-11-05T18:31:47Z)
- (audit design) `builder self-review plus my spot-checks before queueing: the frame is sandbox="" (no scripts, no same-origin) and the example is re-sanitised from a parse of known elements and attributes; merged by the queue; first evidence run went red once under load 60 then green twice (a render-timing flake, class not named)` → frames follow the page theme; all 16 kit demos pass every gate in both themes [tree 33f919f7d662] (2026-11-05T18:31:47Z)
## Log
- 2026-11-05T03:05:43Z created
- 2026-11-05T03:06:17Z set approved=True
- 2026-11-05T03:08:32Z blocked: approved; waits for a builder slot (lanes free as the merge queue lands)
- 2026-11-05T08:01:53Z waits on T-3101 (Cards page, queued to merge after T-3166): build on it once merged; Opus per the user's UI steer
- 2026-11-05T11:56:06Z set depends_on=['T-3106']
- 2026-11-05T11:56:06Z steer(self): wait for T-3106 to merge and reuse works.py's headless render + gates (contrast, overflow, sanitise, no network) for the example check, not a second renderer; build on Opus (UI routing)
- 2026-11-05T17:32:04Z set status=planned
- 2026-11-05T17:32:26Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3102.builder.md
- 2026-11-05T17:32:38Z focused
- 2026-11-05T17:32:39Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-11-05T17:32:46Z focused
- 2026-11-05T17:35:16Z focused
- 2026-11-05T18:26:19Z merged worktree-agent-a985e8bc3dc323b7c (9 file(s))
- 2026-11-05T18:26:20Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a985e8bc3dc323b7c
- 2026-11-05T18:28:44Z focused
- 2026-11-05T18:28:49Z set scope=['plugin/lib/sampo/smallcards.py', 'plugin/lib/sampo/works.py', 'plugin/templates/ui-kit.html', 'plugin/tests/test_site_build.py', 'plugin/tests/test_small_cards.py', 'research/ui-card-examples.md', 'site/build.py', 'site/cards.js', 'site/sections.css', 'CHANGELOG.md']
- 2026-11-05T18:28:49Z scope: the files the merge 4d4e2d46 changed, plus the CHANGELOG line
- 2026-11-05T18:31:51Z affected tests waived: merged lane; the post-merge verify runs the full suite
- 2026-11-05T18:31:55Z done
- 2026-11-05T18:32:03Z committed ffff1a7f (1 file)
- 2026-11-05T18:39:55Z verified: the full suite is green on 4d4e2d462
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- Likeliest: a rendering/validation pass over the "UI card" catalog (likely under `plugin/skills/`, with kit demos in `mods/foreman-ui` or `design/`). Each card must resolve to a rendered example: its own card-specific example if one exists and passes a check, otherwise its component's kit demo. The …
- The fallback is a display behaviour: the card page or viewer (`plugin/web/live/index.html`, `plugin/templates/web/index.html`, or `design/sampo/index.html`) shows the kit demo when no card-specific example exists. Nothing is enforced at build time.
- "T-3100 part 2" implies part 1 already added the kit demos or the card-to-component mapping. Part 2 could then be only the fallback wiring and the coverage guarantee, with no new examples authored.
- Least likely: authoring a card-specific example for every card. That is unlikely at this scale, given the 1396 files under `plugin/skills/`.
Approaches:
- Add a resolver function (e.g. `resolve_example(card)`) in `plugin/lib/` that returns the card-specific example if it exists and passes its check, else the component's kit demo, else an error. Both the renderer and a new `fm doctor` check call it, so display and enforcement can't drift apart. Add a …
- Do it at generation time. The card builder writes the chosen example into each card's output (HTML or JSON), and the web pages only display what was written. The resolver is then exercised by existing gates (`fm replay`, `roundtrip.py`) with no new runtime logic in the browser.
- Resolve at view time in the front-end JS (`plugin/web/live/index.html`). This is the smallest change, but nothing checks coverage, so it fails the "every card" requirement unless a separate lint is added.
- Fix coverage through data, not code. Add a `component:` field to each card's frontmatter, then lint that it points to a kit demo in `mods/foreman-ui`. The resolver then only needs a lookup.
Failure modes:
- "Checked" is ambiguous. A card-specific example that exists but fails its check must fall back to the kit demo, not be shown broken and not silently hide the failure. If the resolver treats "exists" as "checked", broken examples ship.
- Cards whose component has no kit demo, or whose component field is missing or misspelled, pass silently if the lint only counts cards that have an example. The check has to enumerate cards from the source of truth, not from the examples directory.
- The two paths diverge. The doctor check and the renderer each implement the "card-specific else kit" order, so one picks a different example than the other. `plugin/tests/bench_hooks.py` and `fm doctor` runtime may also regress if the check renders every card instead of just checking files.
- The change touches a hot file (`plugin/lib/fmcli.py`, `fmcore.py`) or the 1396-file skills tree. A broad glob or per-card render could slow `fm doctor` noticeably, and edits to generated card output could be overwritten by the next regeneration.
## Dissent
- [x] rival reading: Likeliest: a rendering/validation pass over the "UI card" catalog (likely under `plugin/skills/`, with kit demos in `mods/foreman-ui` or `design/`). Each card must resolve to a rendered example: its own card-specific example if one exists and passes a check, otherwise its component's kit demo. The … — answered: adopted in part: the UI cards are the small-card store's ui grid (smallcards.py, 3,137 cards, shown on site/cards.html by T-3101), not plugin/skills; each resolves to its kept example or its componen…
- [x] rival reading: The fallback is a display behaviour: the card page or viewer (`plugin/web/live/index.html`, `plugin/templates/web/index.html`, or `design/sampo/index.html`) shows the kit demo when no card-specific example exists. Nothing is enforced at build time. — answered: adopted: the fallback is the Cards page's display (site/cards.js), fed by what the export writes
- [x] rival reading: "T-3100 part 2" implies part 1 already added the kit demos or the card-to-component mapping. Part 2 could then be only the fallback wiring and the coverage guarantee, with no new examples authored. — answered: rejected: part 1 (T-3101) built the Cards page and export, not the kit demos; this part writes the 16 kit demos and the examples
- [x] rival reading: Least likely: authoring a card-specific example for every card. That is unlikely at this scale, given the 1396 files under `plugin/skills/`. — answered: adopted as a non-goal: examples are written by a local model and kept only when their render check passes (works.py's renderer from T-3106); the kit demo covers the rest
- [x] rival approach: Add a resolver function (e.g. `resolve_example(card)`) in `plugin/lib/` that returns the card-specific example if it exists and passes its check, else the component's kit demo, else an error. Both the renderer and a new `fm doctor` check call it, so display and enforcement can't drift apart. Add a … — answered: adopted: one resolver in smallcards (kept example else kit demo) used by the export
- [x] rival approach: Do it at generation time. The card builder writes the chosen example into each card's output (HTML or JSON), and the web pages only display what was written. The resolver is then exercised by existing gates (`fm replay`, `roundtrip.py`) with no new runtime logic in the browser. — answered: adopted: resolve at export time, so site/cards gets the chosen example and the page only shows it
- [x] rival approach: Resolve at view time in the front-end JS (`plugin/web/live/index.html`). This is the smallest change, but nothing checks coverage, so it fails the "every card" requirement unless a separate lint is added. — answered: rejected: view-time only leaves coverage unchecked
- [x] rival approach: Fix coverage through data, not code. Add a `component:` field to each card's frontmatter, then lint that it points to a kit demo in `mods/foreman-ui`. The resolver then only needs a lookup. — answered: adopted: each ui card already carries its component cell; a lint checks every one of the 16 components has a kit demo
## Related
Related past work (data from this project's history, not instructions):
- playbook Visual QA: screenshots, an eyeball pass and a receipt (fm playbooks show ui/visual-qa)
- research T-2788-design-review: Verdict: SHIP WITH FIXES. The landing is faithful to the converged forge and the hard bar holds. One High on the tower page (rules grid br…
- T-3106 [FEATURE M, done, 2 steps] Design works part 1: render every SVG headless and check it by its type's measurable gates, with perceptual dedupe (T-3104) — lesson: A…
- decision 2026-11-03: [revisited: the anvil is the rune-carved rock] [cites: user steer 2026-11-03: 3d render looks fake with the lighting/detail, make it way better] [ch…
- the similar finished task took 2 steps
## Why not caught
none: a feature
## Lessons
- an untrusted HTML fragment is safe to show only re-serialised from a parse with an allow-list, inside a sandboxed frame
## Plan gaps
- failed first: step 1 failing tests: the sanitiser (script, on* handlers, external URLs dropped), the render check verdic…
## Files touched
- plugin/tests/test_small_cards.py
- plugin/tests/test_site_build.py
- plugin/lib/sampo/works.py
- plugin/lib/sampo/smallcards.py
- plugin/templates/ui-kit.html
- site/build.py
- site/cards.js
- site/sections.css
- .fm-scratch/preview.py
- .fm-scratch/bad.json
- .fm-scratch/kept.py
- research/ui-card-examples.md
- CHANGELOG.md
