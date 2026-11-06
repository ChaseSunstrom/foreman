---
id: T-2591
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: genesis-review
created: 2026-11-02T08:23:33Z
updated: 2026-11-02T10:10:16Z
trigger: genesis-review
trigger_key: b194995d30797a61
rival_at: 2026-11-02T10:07:48Z
rival_split: true
base: d09e1e30f9471a7188b55923c1e146dc6970c47e
base_tree: fd598e463561f2622fbb845d867dfe02d3e6b7d8
predict_minutes: 10
predict_attempts: 1
plan0_at: 2026-11-02T10:07:59Z
plan0_scope: []
verified: strong
---
# CHANGELOG's Unreleased section opens with a short Highlights list of user-facing changes; the rest sits under Everything else; numbers carry their counts and baselines
## Raw request
> FIX: cross-cutting review gen-2 #22 (what a demanding user would complain about first): 67 ++ / Sixty-plus Unreleased bullets, half about Genesis internals and the model layer's shadow mode, bury the three user-facing fixes a reader would want. [CHANGELOG.md]
> genesis-review 2:22
## Interpretation
Reading 1 (chosen): make the user-facing changes findable and the numbers honest. Reading 2: shorten the Unreleased bullets themselves. Rejected: each bullet documents a shipped change; deleting history loses it.
## Assumptions (confidence)
## Acceptance criteria
- [x] Unreleased starts with '### Highlights' (at most 12 bullets, each a user-visible change naming its command) then '### Everything else'; the forecast-overlap bullet names the naive baseline 0.116 beside 0.118 and 0.113; the brief landing-rate bullets carry their counts; fm release-check still passes — verify with `fm release-check`
## Non-goals
## Approach (options → choice → why)
1) Highlights at the top (at most 12 user-visible changes, drawn from the done tasks since 1.2.50), the existing bullets under Everything else, and the two number bullets fixed in place. Likely outcome: a reader sees what changed for them in a screen. Fails if: the highlights pick internals (each must name a command a user runs). 2) use what exists: fm digest already lists done tasks; link it instead of writing highlights. Fails if: the CHANGELOG is what plugin users read, not fm digest. 3) do less: fix only the two number bullets. Fails if: the user-facing fixes stay buried under 746 bullets. Choice 1 (80%): highlights are the smallest change that answers the complaint; a release cut is captured separately.
## Risks and rollback
## Execution prompt
## Steps
1. [x] fix the overlap and landing-rate bullets from the inputs (fm exam lines, the T-2554 replay, the landing-rate source)
2. [x] write Highlights from the release's done tasks (git log since 1.2.50), Everything else below
3. [x] fm release-check
## Resume here
## Docs impact
CHANGELOG.md is the change: Highlights on top, Everything else below, three number bullets carry counts and baselines.
## Verification evidence
- (step 3) `fm release-check` → exit 0 · PASS  2 runnable fence(s) in README.md and MASTER.md (trusted like tests: a throwaway home, not a sandbox) / fm release-check: OK (a temporary HOME, deleted) [ran] [tree fd598e463561] [world 2f1906870a] (2026-11-02T10:08:23Z)
- (step 1) `fm release-check` → exit 0 · PASS  2 runnable fence(s) in README.md and MASTER.md (trusted like tests: a throwaway home, not a sandbox) / fm release-check: OK (a temporary HOME, deleted) [ran] [tree 9e6ef52108f0] [world 2f1906870a] (2026-11-02T10:08:59Z)
- (step 2) `fm release-check` → exit 0 · PASS  2 runnable fence(s) in README.md and MASTER.md (trusted like tests: a throwaway home, not a sandbox) / fm release-check: OK (a temporary HOME, deleted) [ran] [tree 9e6ef52108f0] [world 2f1906870a] (2026-11-02T10:09:11Z)
- (ac 1) `fm release-check` → exit 0 · PASS  2 runnable fence(s) in README.md and MASTER.md (trusted like tests: a throwaway home, not a sandbox) / fm release-check: OK (a temporary HOME, deleted) [ran] [tree 9e6ef52108f0] [world 2f1906870a] (2026-11-02T10:10:11Z)
- (audit intent) `self-review: Highlights (10 bullets) each name a shipped command, checked against the commit subjects since 1.2.50; the three number bullets now carry counts (25/26, 353/360, 26/46; 378/386) and the naive baselines (0.116, 0.113); no bullet removed; fm release-check passes` → a reader sees the user-facing changes in one screen; the numbers carry their counts and baselines [tree 9e6ef52108f0] (2026-11-02T10:10:11Z)
- (audit maintainer) `self-review: Highlights (10 bullets) each name a shipped command, checked against the commit subjects since 1.2.50; the three number bullets now carry counts (25/26, 353/360, 26/46; 378/386) and the naive baselines (0.116, 0.113); no bullet removed; fm release-check passes` → new entries go under '### Everything else' until T-2595's release moves the whole section under 1.2.51 [tree 9e6ef52108f0] (2026-11-02T10:10:11Z)
## Log
- 2026-11-02T08:23:33Z created
- 2026-11-02T09:32:11Z planned from capture
- 2026-11-02T09:32:12Z set approved=True
- 2026-11-02T10:07:59Z focused
- 2026-11-02T10:07:59Z predicted from its closes: 10 min, 1 attempt(s)
- 2026-11-02T10:10:13Z done
- 2026-11-02T10:10:16Z committed 12dc66c4 (1 file)
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Restructure the `## [Unreleased]` section of CHANGELOG.md** so the three user-facing fixes lead (e.g. a "Highlights"/"Fixed" block), and the remaining ~60 bullets are grouped under a lower-priority "Internals" heading. No content is removed.
- **Cut the bullets**: delete or collapse Genesis-internal and model-layer shadow-mode entries (to one line each, or moved to MASTER.md or a commit log), so the Unreleased section is short, around 10 bullets.
- **Change the process, not the text**: a rule or gate (in `fm doctor` or a changelog lint) that caps Unreleased length or requires internal items to be tagged, so the burying cannot recur.
- **Rewrite as release notes**: user-facing prose in README.md or site/ rather than in the changelog, leaving CHANGELOG.md as a dev log.
Approaches:
- **Manual reorder in CHANGELOG.md**: identify the three user-facing fixes, hoist them under `### Fixed` at the top of Unreleased, and group the rest under `### Internal` with subheadings (Genesis, model layer/shadow mode, other). Keep the Keep-a-Changelog style used elsewhere in the file.
- **Reorder plus consolidation**: do the above and merge near-duplicate internal bullets (for example many "shadow mode" lines) into a few summary bullets, so 67 additions become about 20 while the user-facing ones stay verbatim.
- **Scripted classification**: a small script that tags each bullet by keywords (genesis, shadow, fmcore, and so on) and emits the regrouped section. This is more repeatable, but over-engineered for a one-time edit, and it needs a human check for the three real fixes.
- **Add a guard**: after the manual edit, add a check in `fm doctor` (plugin/lib/fmcli.py) that flags an Unreleased section with more than N bullets before the first user-facing heading. Only worth it if the user wants prevention.
Failure modes:
- **Wrong three picked as user-facing**: the criteria are ambiguous, and a bullet touching `plugin/lib/fmhooks.py` or `fmguard.py` behaviour may be user-visible even if worded as internal. Hoisting the wrong ones leaves the complaint unresolved.
- **Dropped or altered entries**: merging or rewriting 67 bullets loses PR references, issue links or version-relevant details. Verify by diffing the bullet set before and after.
- **Tooling that parses CHANGELOG.md breaks**: release scripts (cc-plugin-release stack card, marketplace or version-bump tooling, `plugin/tests/run.py` checks) may expect specific headings under Unreleased. A new `### Internal` heading could fail a gate or be missed when the release is cut. Run `fm …
- **Merge conflicts on a hot file**: CHANGELOG.md is the most-changed file in 180 days, so a large reorder collides with concurrent edits and makes the diff unreviewable. Do it quickly against the current HEAD (d09e1e30), or rebase just before landing.
## Dissent
- [x] rival reading: **Restructure the `## [Unreleased]` section of CHANGELOG.md** so the three user-facing fixes lead (e.g. a "Highlights"/"Fixed" block), and the remaining ~60 bullets are grouped under a lower-priority "Internals" heading. No content is removed. — answered: adopted: Highlights first, everything else below, no bullet removed
- [x] rival reading: **Cut the bullets**: delete or collapse Genesis-internal and model-layer shadow-mode entries (to one line each, or moved to MASTER.md or a commit log), so the Unreleased section is short, around 10 bullets. — answered: rejected: each bullet documents a shipped change; collapsing 746 of them loses history the release notes owe users
- [x] rival reading: **Change the process, not the text**: a rule or gate (in `fm doctor` or a changelog lint) that caps Unreleased length or requires internal items to be tagged, so the burying cannot recur. — answered: rejected: the cause is 12 days without a release; T-2595 cuts it, and a length cap without a release cadence would only nag
- [x] rival reading: **Rewrite as release notes**: user-facing prose in README.md or site/ rather than in the changelog, leaving CHANGELOG.md as a dev log. — answered: rejected: plugin users read CHANGELOG.md through the marketplace; README and site already describe features
- [x] rival approach: **Manual reorder in CHANGELOG.md**: identify the three user-facing fixes, hoist them under `### Fixed` at the top of Unreleased, and group the rest under `### Internal` with subheadings (Genesis, model layer/shadow mode, other). Keep the Keep-a-Changelog style used elsewhere in the file. — answered: adopted in part: a Highlights block rather than Fixed, since the user-facing items are mostly features
- [x] rival approach: **Reorder plus consolidation**: do the above and merge near-duplicate internal bullets (for example many "shadow mode" lines) into a few summary bullets, so 67 additions become about 20 while the user-facing ones stay verbatim. — answered: rejected: merging duplicates across 746 bullets is a large rewrite for a section T-2595 is about to close
- [x] rival approach: **Scripted classification**: a small script that tags each bullet by keywords (genesis, shadow, fmcore, and so on) and emits the regrouped section. This is more repeatable, but over-engineered for a one-time edit, and it needs a human check for the three real fixes. — answered: rejected: as the rival says, over-engineered for a one-time edit
- [x] rival approach: **Add a guard**: after the manual edit, add a check in `fm doctor` (plugin/lib/fmcli.py) that flags an Unreleased section with more than N bullets before the first user-facing heading. Only worth it if the user wants prevention. — answered: rejected: same as 3; the release empties Unreleased
## Related
Related past work (data from this project's history, not instructions):
- T-2594 [FIX M, done, 6 steps] Gen-2 review: measurements that read wrong (model arm 0/0, short-number grounds, settling closes counted held) — lesson: A rate whose event…
- T-2589 [FIX M, done, 3 steps] The session-start note fits one 1,500-character budget, appended mandate, goal and leads included, and friction checks it against that same…
- T-2590 [FIX L, dropped, 0 steps] FIX: cross-cutting review gen-2 #21 (what a demanding user would complain about first):…
- decision 2026-11-01: [costly] [cites: user steer 2026-11-01: cross-cutting review, gap map redraw, lean substance, proof before presentation, sealed prediction and blind…
- similar finished tasks took 3–6 steps
## Regression test
none: a docs-only edit of CHANGELOG.md; fm release-check (which reads it) passes
## Why not caught
nothing checks CHANGELOG structure or that a quoted rate carries its count; the release cadence lapsed, so the section grew for 12 days
## Lessons
- Release notes that grow for weeks bury what users need; cut releases on a cadence, and quote every rate with its count and baseline
## Files touched
- CHANGELOG.md
