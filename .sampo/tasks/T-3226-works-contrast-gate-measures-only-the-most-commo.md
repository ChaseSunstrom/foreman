---
id: T-3226
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/sampo/works.py, plugin/tests/test_design_works.py, plugin/lib/sampo/smallcards.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-11-05T18:13:16Z
updated: 2026-11-05T19:06:45Z
base: fc487f355d2feb8a58ca6013352d20dc0a696052
base_tree: db26c1b52bd10cc10d5a0a9d693fbdda108089fc
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-05T19:01:39Z
plan0_scope: []
verified: strong
unproven: [red]
---
# Works contrast gate measures only the most common colour pairs, so a small badge or chip…
## Raw request
> works contrast gate measures only the most common colour pairs, so a small badge or chip in a rarer colour can pass below 4.5:1: measure every text run's own pair (T-3102 noticed)
## Interpretation
works._text_ratio keeps only (text, background) pixel pairs that make at least SHARE of the text's changed pixels, to skip antialiasing; a small badge, chip or one coloured word is under SHARE, so its contrast is never measured. Plan: group the changed pixels by background colour; in each group keep the core text colours (drop a colour that lies on the segment between the background and a commoner text colour of that group: an antialiasing shade) with at least MIN_TEXT pixels; the gate is the lowest ratio over every group's cores. Bounded: the top 64 colours per group.
## Assumptions (confidence)
## Acceptance criteria
- [x] a card whose body text passes but whose small badge (own chip background) or one coloured word sits under 4.5:1 fails contrast; antialiased body text alone still passes as today — verify with `python3 plugin/tests/run.py test_design_works`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests: a low-contrast badge and a low-contrast word fail; plain antialiased text passes
2. [x] _text_ratio by background group with antialiasing shades dropped
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_design_works.Rendered` → ✗ exit 1 · Ran 6 tests in 3.8s (6 jobs, 16 at a time; slowest: Rendered.test_icons_blank_clipped_still_and_duplicate_fail_their_gates 3s, Rendered.test_the_text_report_names_each_gate_with_its_number 3s, Rendere [ran] [tree 303da50e5c38] [world 2f1906870a] (2026-11-05T19:01:58Z)
- (step 2) `python3 plugin/tests/run.py test_design_works test_small_cards test_site_build` → exit 0 · Ran 85 tests in 13.9s (51 jobs, 16 at a time; slowest: CardsPage 13s, ExamplesRendered.test_every_component_has_a_kit_demo_that_passes_in_both_themes 8s, Rendered.test_icons_blank_clipped_still_and_du [ran] [tree 04f8fd6b24d4] [world 2f1906870a] (2026-11-05T19:05:25Z)
- `python3 plugin/tests/run.py test_design_works.Rendered` → ✗ exit 1 · Ran 6 tests in 13.9s (1 jobs, 16 at a time; slowest: Rendered 10s) / FAILED (1 classes: test_design_works.Rendered) (start tree + this task's tests) [ran] [tree 04f8fd6b24d4] [world 2f1906870a] (2026-11-05T19:05:44Z)
- `python3 plugin/tests/run.py test_design_works.Rendered` → exit 0 · Ran 6 tests in 3.7s (6 jobs, 16 at a time; slowest: Rendered.test_icons_blank_clipped_still_and_duplicate_fail_their_gates 3s, Rendered.test_cards_low_contrast_and_scripted_fail_their_gates 2s, Render [ran] [tree 04f8fd6b24d4] [world 2f1906870a] (2026-11-05T19:05:44Z)
- (ac 1) `python3 plugin/tests/run.py test_design_works` → ✗ exit 1 · Ran 28 tests in 2.0s (10 jobs, 16 at a time; slowest: StaticGates 2s, Rendered.test_icons_blank_clipped_still_and_duplicate_fail_their_gates 0s, Rendered.test_a_faint_badge_or_a_faint_line_fails_besid [ran] [tree c0e453ab6471] [world 2f1906870a] (2026-11-05T19:05:56Z)
- (ac 1) `python3 plugin/tests/run.py test_design_works` → exit 0 · Ran 28 tests in 7.6s (5 jobs, 16 at a time; slowest: Rendered 7s, StaticGates 2s, WithoutBrowser 0s) / OK [ran] [tree c0e453ab6471] [world 2f1906870a] (2026-11-05T19:06:22Z)
- (audit intent) `self: _text_ratio groups changed pixels by the background they covered; a colour is dropped only when it lies on the segment between that background and another of the group's colours (antialiasing) or within NEAR of a commoner one (hinting); MIN_TEXT keeps single stray pixels out; bounded at 64 colours per group, compared pairwise; one criteria run went red under load 40 and green on rerun (render timing)` → a faint badge on its own chip and a faint line beside clear body text both fail; clear antialiased text passes [tree c0e453ab6471] (2026-11-05T19:06:22Z)
- (audit edge) `self: _text_ratio groups changed pixels by the background they covered; a colour is dropped only when it lies on the segment between that background and another of the group's colours (antialiasing) or within NEAR of a commoner one (hinting); MIN_TEXT keeps single stray pixels out; bounded at 64 colours per group, compared pairwise; one criteria run went red under load 40 and green on rerun (render timing)` → the old commonest-pair fallback remains when no colour reaches MIN_TEXT; a near-identical hinting variant at 4.47 beside a 4.56 core no longer fails the select demo [tree c0e453ab6471] (2026-11-05T19:06:22Z)
- (audit design) `self: _text_ratio groups changed pixels by the background they covered; a colour is dropped only when it lies on the segment between that background and another of the group's colours (antialiasing) or within NEAR of a commoner one (hinting); MIN_TEXT keeps single stray pixels out; bounded at 64 colours per group, compared pairwise; one criteria run went red under load 40 and green on rerun (render timing)` → the kit's controls take --surface and --line instead of the browser's dark grey [tree c0e453ab6471] (2026-11-05T19:06:22Z)
- (audit self) `self: _text_ratio groups changed pixels by the background they covered; a colour is dropped only when it lies on the segment between that background and another of the group's colours (antialiasing) or within NEAR of a commoner one (hinting); MIN_TEXT keeps single stray pixels out; bounded at 64 colours per group, compared pairwise; one criteria run went red under load 40 and green on rerun (render timing)` → no findings [tree c0e453ab6471] (2026-11-05T19:06:22Z)
## Log
- 2026-11-05T18:13:16Z created
- 2026-11-05T19:01:10Z planned: it has criteria and steps
- 2026-11-05T19:01:38Z focused
- 2026-11-05T19:01:39Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-05T19:03:51Z scope: smallcards.UI_CSS gave controls the text colour but the browser's background; the new gate measured the dark theme's default button at 4.34:1 (a real miss the old gate hid), so controls now take --surface and --line
- 2026-11-05T19:05:10Z set scope=['plugin/lib/sampo/works.py', 'plugin/tests/test_design_works.py', 'plugin/lib/sampo/smallcards.py', 'CHANGELOG.md']
- 2026-11-05T19:06:43Z done
- 2026-11-05T19:06:45Z committed 9c5aa472 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- playbook Type and colour that read as chosen (fm playbooks show ui/type-and-colour)
- research T-2876-ui-review: Verdict: approve with nits.** The forge palette, the gold titles and borders, and the steel done state read as intended. The main gaps are tha…
- T-2915 [FEATURE M, done, 4 steps] MASTER.md opens whole in one Read: each over-long section moves to docs/map shards, MASTER.md keeps a one-line-per-entry index with lin…
- decision 2026-10-23: T-1623: the five UI contract rules are written down from what the UI playbooks already require: motion (reduced motion as its own path), contrast (p…
- similar past tasks were M: consider --tier M
- the similar finished task took 4 steps
## Why not caught
the rendered tests only had one text colour per work; the new test adds a badge and a second line
## Lessons
- a contrast gate that samples only the commonest pairs passes small UI text; group by background and drop antialiasing shades instead
## Plan gaps
- failed first: step 1 failing tests: a low-contrast badge and a low-contrast word fail; plain antialiased text passes
## Files touched
- plugin/tests/test_design_works.py
- plugin/lib/sampo/works.py
- plugin/lib/sampo/smallcards.py
- CHANGELOG.md
