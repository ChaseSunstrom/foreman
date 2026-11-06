---
id: T-3198
type: SECURITY
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-05T11:33:21Z
updated: 2026-11-05T18:06:36Z
base: 397e14bea9c20443e1f4c429d37afd82edd860af
base_tree: 4446da47039ea64b66863151d45085fa0c271eef
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-05T17:36:02Z
plan0_scope: []
verified: strong
unproven: [docs, red]
---
# Works check: the use copy cap counts direct use fan-out only; nested pattern/marker…
## Raw request
> works check: the use copy cap counts direct use fan-out only; nested pattern/marker references escape it
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] nested fan-out through url(#id) references (pattern fills, markers, clip-path, mask, filter, style) counts toward MAX_USES like <use>, and a cycle through them fails xml — verify with `python3 plugin/tests/run.py test_design_works`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests: a pattern bomb and a url() cycle fail xml
2. [x] url(#id) edges in works._uses
## Resume here
## Docs impact
docs/map/files-lib-3.md fmworks row; CHANGELOG line
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_design_works.StaticGates` → ✗ exit 1 · Ran 16 tests in 2.1s (1 jobs, 16 at a time; slowest: StaticGates 1s) / FAILED (1 classes: test_design_works.StaticGates) [ran] [tree cc7eded9fe32] [world 2f1906870a] (2026-11-05T17:55:20Z)
- (step 2) `python3 plugin/tests/run.py test_design_works test_works_cli` → ✗ exit 1 · run.py: no test matches test_works_cli [ran] [tree 8ea762388ca2] [world 2f1906870a] (2026-11-05T17:58:05Z)
- (step 2) `python3 plugin/tests/run.py test_design_works test_map` → exit 0 · Ran 38 tests in 10.5s (12 jobs, 16 at a time; slowest: Map 10s, StaticGates 5s, Rendered.test_icons_blank_clipped_still_and_duplicate_fail_their_gates 4s) / OK [ran] [tree fc83a2f8bd16] [world 2f1906870a] (2026-11-05T17:58:37Z)
- `python3 plugin/tests/run.py test_design_works.StaticGates` → ✗ exit 1 · Ran 17 tests in 5.8s (1 jobs, 16 at a time; slowest: StaticGates 1s) / FAILED (1 classes: test_design_works.StaticGates) (start tree + this task's tests) [ran] [tree fc83a2f8bd16] [world 2f1906870a] (2026-11-05T17:58:52Z)
- `python3 plugin/tests/run.py test_design_works.StaticGates` → exit 0 · Ran 17 tests in 6.8s (17 jobs, 16 at a time; slowest: StaticGates.test_stylesheet_rules_naming_a_url_are_capped_and_the_worst_allowed_stays_fast 6s, StaticGates.test_a_hostile_megabyte_is_checked_in_s [ran] [tree fc83a2f8bd16] [world 2f1906870a] (2026-11-05T17:58:52Z)
- (ac 1) `python3 plugin/tests/run.py test_design_works` → exit 0 · Ran 27 tests in 10.9s (25 jobs, 16 at a time; slowest: Rendered.test_icons_blank_clipped_still_and_duplicate_fail_their_gates 9s, Rendered.test_cards_low_contrast_and_scripted_fail_their_gates 7s, Ren [ran] [tree fc83a2f8bd16] [world 2f1906870a] (2026-11-05T17:59:39Z)
- (audit adversary) `self: re-read _refs/_sheet/_uses against the bypasses: quoted and spaced url(), uppercase URL(, fallbacks after url(), xlink:href, pattern/filter/gradient href inheritance, feImage/textPath/mpath hrefs, SMIL to/values carrying url(), CSS custom properties, :root and attribute selectors (match-all), @media-nested rules; escapes and @import stay refused by _bad_css` → pattern, marker (vertex-weighted), stylesheet-class and quoted-url cycle bombs all fail xml; 65 url rules fail; 64 match-all rules on 19,000 elements finish under 10 s [tree fc83a2f8bd16] (2026-11-05T17:59:39Z)
- (audit edge) `self: re-read _refs/_sheet/_uses against the bypasses: quoted and spaced url(), uppercase URL(, fallbacks after url(), xlink:href, pattern/filter/gradient href inheritance, feImage/textPath/mpath hrefs, SMIL to/values carrying url(), CSS custom properties, :root and attribute selectors (match-all), @media-nested rules; escapes and @import stay refused by _bad_css` → gradients cost no copy and their stops ignore stylesheet refs, so a *{fill:url(#g)} rule isn't a false cycle; a hatch pattern by class, 40 gradient fills and 30 marker-end arrows pass [tree fc83a2f8bd16] (2026-11-05T17:59:39Z)
- (audit intent) `self: re-read _refs/_sheet/_uses against the bypasses: quoted and spaced url(), uppercase URL(, fallbacks after url(), xlink:href, pattern/filter/gradient href inheritance, feImage/textPath/mpath hrefs, SMIL to/values carrying url(), CSS custom properties, :root and attribute selectors (match-all), @media-nested rules; escapes and @import stay refused by _bad_css` → nested paint/marker/mask/clip/filter fan-out counts toward MAX_USES like <use> [tree fc83a2f8bd16] (2026-11-05T17:59:39Z)
- (audit self) `self: re-read _refs/_sheet/_uses against the bypasses: quoted and spaced url(), uppercase URL(, fallbacks after url(), xlink:href, pattern/filter/gradient href inheritance, feImage/textPath/mpath hrefs, SMIL to/values carrying url(), CSS custom properties, :root and attribute selectors (match-all), @media-nested rules; escapes and @import stay refused by _bad_css` → no findings [tree fc83a2f8bd16] (2026-11-05T17:59:39Z)
## Log
- 2026-11-05T11:33:21Z created
- 2026-11-05T17:34:33Z set status=planned
- 2026-11-05T17:36:01Z focused
- 2026-11-05T17:36:02Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-05T17:36:10Z paused: focus moved to T-2261
- 2026-11-05T17:52:28Z re-based: what other work changed while it was paused isn't its own change
- 2026-11-05T17:52:28Z focused
- 2026-11-05T17:59:22Z scope: works.py and its test, the docs map row for fmworks and the CHANGELOG line
- 2026-11-05T18:06:30Z done
- 2026-11-05T18:06:36Z committed 6efa000d (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2052 [FEATURE L, done, 5 steps] Docs/README redesign: replace walls of text with scannable structure — hero with logo,… — lesson: Measure docs by what a reader sees: a…
- research T-2349-review: Verdict: approve with nits.** I found no HIGH or CRITICAL defects. The untrusted-text and keying requirements hold. The replay is unbounded and r…
- research T-2343-review: T-2343 review (coordinator, main thread: the pace gate held fm-reviewer subagents).
- decision 2026-11-03: [outward] [cites: user steer: read SAMPO.md (plugin foreman@foreman becomes sampo@sampo; nothing a user already has may break)] [check: pending T-27…
- similar past tasks were L: consider --tier L
- the similar finished task took 5 steps
## Why not caught
the use-bomb test only built <use> chains; the new test builds one bomb per reference kind
## Lessons
- a copy cap must count every reference kind the renderer expands (href, url() in attributes, styles and stylesheets), weighted by how many times it draws
## Plan gaps
- failed first: step 1 failing tests: a pattern bomb and a url() cycle fail xml
- failed first: step 2 url(#id) edges in works._uses
## Files touched
- plugin/tests/test_design_works.py
- plugin/lib/sampo/works.py
- CHANGELOG.md
- docs/map/files-lib-3.md
