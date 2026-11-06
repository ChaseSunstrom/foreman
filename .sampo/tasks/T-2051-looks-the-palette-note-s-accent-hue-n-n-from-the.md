---
id: T-2051
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-29T20:28:48Z
updated: 2026-10-29T23:32:26Z
base: ac5d856541fe796b980a12986310fb44db28db20
base_tree: f98ed591e075f1d16c253221376d6e140c73dbf8
plan0_at: 2026-10-29T23:26:11Z
plan0_scope: []
verified: strong
---
# Looks: the Palette note's 'Accent hue N, N° from the nearest status hue' is meaningless…
## Raw request
> Looks: the Palette note's 'Accent hue N, N° from the nearest status hue' is meaningless for a near-neutral accent (chroma < 0.03, e.g. darkroom); gen.py should skip it
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] no look card with accent chroma under 0.03 carries a hue-distance note — verify with `cd plugin/tests && python3 -m unittest test_library.LibraryCards.test_a_near_neutral_accent_has_no_hue_note`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] drop the note from darkroom and glacier
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_library.LibraryCards.test_a_near_neutral_accent_has_no_hue_note` → ✗ exit 1 · Ran 1 test in 0.008s / FAILED (failures=1) [ran] [tree f7aa110192db] (2026-10-29T23:26:24Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_library` → exit 0 · Ran 43 tests in 9.574s / OK [ran] [tree 6767e46b7c83] (2026-10-29T23:26:48Z)
- `cd plugin/tests && python3 -m unittest test_library.LibraryCards.test_a_near_neutral_accent_has_no_hue_note` → ✗ exit 1 · Ran 1 test in 0.008s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree 6767e46b7c83] (2026-10-29T23:26:49Z)
- `cd plugin/tests && python3 -m unittest test_library.LibraryCards.test_a_near_neutral_accent_has_no_hue_note` → exit 0 · Ran 1 test in 0.007s / OK [ran] [tree 6767e46b7c83] (2026-10-29T23:26:49Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  version skew         uidemo-982f4c ran 1.2.29, lacks 317 (T-0275, T-0705, T-0787, T-0933 …) — restart their sessions on the new Foreman / fm doctor: OK (49 pass, 5 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · skipped: nothing under plugin/lib/**, plugin/hooks/**, plugin/bin/**, plugin/tests/bench_hooks.py, plugin/tests/fixtures/** changed since its pass at 23:20 UTC; claude plugin test mods/foreman-ui → [ran] [tree 6767e46b7c83] (2026-10-29T23:29:53Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_library.LibraryCards.test_a_near_neutral_accent_has_no_hue_note` → exit 0 · Ran 1 test in 0.008s / OK [ran] [tree 6767e46b7c83] (2026-10-29T23:30:04Z)
- (audit intent) `self-review: two card sentences removed; a test over every look card pins the rule (accent chroma under 0.03 carries no hue-distance note); nothing in lib or site parses the sentence` → darkroom (0.024) and glacier (0.015) no longer claim a hue distance for an accent that reads as no colour [tree 6767e46b7c83] (2026-10-29T23:30:04Z)
- (audit adversary) `self-review: two card sentences removed; a test over every look card pins the rule (accent chroma under 0.03 carries no hue-distance note); nothing in lib or site parses the sentence` → card text only; no code path or input changed [tree 6767e46b7c83] (2026-10-29T23:30:04Z)
- (audit edge) `self-review: two card sentences removed; a test over every look card pins the rule (accent chroma under 0.03 carries no hue-distance note); nothing in lib or site parses the sentence` → the test skips cards with no --accent row; shipping-manifest (0.014) never had the note and still passes [tree 6767e46b7c83] (2026-10-29T23:30:04Z)
- (audit operator) `self-review: two card sentences removed; a test over every look card pins the rule (accent chroma under 0.03 carries no hue-distance note); nothing in lib or site parses the sentence` → fm lib lint and test_library 43/43 pass; the cards still explain the near-neutral accent in words [tree 6767e46b7c83] (2026-10-29T23:30:04Z)
- (audit maintainer) `self-review: two card sentences removed; a test over every look card pins the rule (accent chroma under 0.03 carries no hue-distance note); nothing in lib or site parses the sentence` → a new look card generated with the note at low chroma fails the test with its file name [tree 6767e46b7c83] (2026-10-29T23:30:04Z)
- (audit self) `self-review: two card sentences removed; a test over every look card pins the rule (accent chroma under 0.03 carries no hue-distance note); nothing in lib or site parses the sentence` → no findings [tree 6767e46b7c83] (2026-10-29T23:30:04Z)
## Log
- 2026-10-29T20:28:48Z created
- 2026-10-29T23:26:06Z set type=FIX, tier=S
- 2026-10-29T23:26:06Z planned: it has criteria and steps
- 2026-10-29T23:26:11Z focused
- 2026-10-29T23:30:11Z done
- 2026-10-29T23:30:13Z committed 70e924b9 (4 files)
- 2026-10-29T23:30:18Z guard authorization added: publish
- 2026-10-29T23:32:26Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- playbook Type and colour that read as chosen (fm playbooks show ui/type-and-colour)
- T-2045 [FEATURE M, done, 3 steps] Eight more named looks on the style shelf (12 to 20) — lesson: A look's accent rule (30° from status hues) rules out the obvious brand …
- research T-1512-review: Verdict:** approve with nits. I found no defect in the probe, the hush write or the escaping. I could not run the tests (read-only), so every poi…
- decision 2026-10-15: Round 4 slate: 6 builds from 31 grounded clusters (437 ideas): install asks before bypass, INSTALL.md for agents, fm demo (no-model), marketplace in…
- similar past tasks were M: consider --tier M
- the similar finished task took 3 steps
## Why not caught
the look cards were written by a one-off scratchpad generator that printed the hue note for every accent; no test read the note against the chroma
## Lessons
- A generated card sentence needs the same guard as the generator's numbers: a hue distance is noise below a chroma floor
## Plan gaps
- failed first: step 1 failing test
## Files touched
- plugin/tests/test_library.py
- plugin/skills/library/cards/looks/look-darkroom.md
- plugin/skills/library/cards/looks/look-glacier.md
- CHANGELOG.md
