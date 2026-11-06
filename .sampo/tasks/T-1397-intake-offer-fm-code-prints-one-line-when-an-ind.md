---
id: T-1397
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcode.py, plugin/lib/fmplugins.py, plugin/lib/fmcli.py, plugin/tests/test_code.py, plugin/tests/test_plugins.py, MASTER.md, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-21T17:28:43Z
updated: 2026-10-23T09:59:34Z
inferred_deps: [T-1382]
inferred_why: T-1382: named in its request
group: skills and routing
base: 54ea925237dbce22b763fa4e44fad3b1788388a9
base_tree: c99fbb825cdcc6e7b122282edaa3fbeb7fabb6c3
plan0_at: 2026-10-23T09:55:41Z
plan0_scope: [plugin/lib/fmcode.py, plugin/lib/fmplugins.py, plugin/lib/fmcli.py, plugin/tests/test_code.py, plugin/tests/test_plugins.py, MASTER.md, CHANGELOG.md]
verified: strong
---
# Intake offer: fm code prints one line when an indexed skill matches the request (name, lic
## Raw request
> FEATURE: Intake offer: fm code prints one line when an indexed skill matches the request (name, licence class, token cost), never installing; fm plugins suggest lists three with reasons from the project's own stack (S10, A18)
> CONTEXT: round 2 of the fm/fm code brainstorm (T-1382): research/brainstorm-fm-anthropic-catalogue.md, grounding with file:line in research/brainstorm-fm-anthropic-half-a.md (A*) and half-b.md (B*)
> DONE-WHEN: 'extract tables from this pdf' prints exactly one offer and a request with no match prints none; fm plugins suggest --json gives at most three with a reason each
## Interpretation
Two offers, neither installs anything. (1) At a new fm code run's start, one note when an indexed skill from fm lib's sources clearly matches the request: its name, licence class and token cost, and that fm lib show reads it as data. Clear means a word of the skill's own name, four points in all and a lead over the next skill; otherwise nothing. (2) fm plugins suggest [--json]: up to three marketplace plugins not installed that fit the project's stack (the best find() hit for each card fm lib detects), each with the card and its evidence as the reason.
## Assumptions (confidence)
## Acceptance criteria
- [x] 'extract tables from this pdf' prints exactly one offer and a request with no match prints none; fm plugins suggest --json gives at most three with a reason each — verify with `python3 plugin/tests/run.py test_code.SkillOffer test_plugins.Suggest`
## Non-goals
## Approach (options → choice → why)
Options: embed and rank every skill per request (a model call or vectors: cost and a dependency); keyword scoring over the existing index with a strict threshold (fm lib search's scoring, tightened); always show the top three (noise on every run). Choice: the threshold scorer, one line or none; suggest reuses fm lib suggest's stack detection and fm plugins find.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests, then skill_offer at run start and fmplugins.suggest with the verb
## Resume here
## Docs impact
CHANGELOG.md, MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_code.SkillOffer test_plugins.Suggest` → ✗ exit 1 · Ran 2 tests in 0.5s (2 classes, 16 at a time; slowest: SkillOffer 0s, Suggest 0s) / FAILED (2 classes) [ran] [tree bf09b4afc9dd] (2026-10-23T09:55:48Z)
- (step 1) `python3 plugin/tests/run.py test_code.SkillOffer test_plugins.Suggest` → exit 0 · Ran 2 tests in 0.6s (2 classes, 16 at a time; slowest: SkillOffer 0s, Suggest 0s) / OK [ran] [tree 0099da113f3f] (2026-10-23T09:57:24Z)
- (ac 1) `python3 plugin/tests/run.py test_code.SkillOffer test_plugins.Suggest` → exit 0 · Ran 2 tests in 0.6s (2 classes, 16 at a time; slowest: SkillOffer 0s, Suggest 0s) / OK [ran] [tree 0099da113f3f] (2026-10-23T09:57:31Z)
- (audit intent) `self review; test_code.SkillOffer, test_plugins and test_cli green; fm plugins suggest tried on a Cargo project` → 'extract tables from this pdf' gets exactly one offer (kit:pdf, open, ~N tokens) and 'fix add' none; suggest gives at most three not-installed plugins, each with its card and evidence (tests) [tree 0099da113f3f] (2026-10-23T09:57:31Z)
- (audit edge) `self review; test_code.SkillOffer, test_plugins and test_cli green; fm plugins suggest tried on a Cargo project` → a tie between two skills offers none; a damaged index never stops a run; a card's area joins the search (cargo → rust) except the generic lang; remote entries say their size is known once installed [tree 0099da113f3f] (2026-10-23T09:57:31Z)
## Log
- 2026-10-21T17:28:43Z created
- 2026-10-23T09:43:21Z set tier=M, scope=['plugin/lib/fmcode.py', 'plugin/lib/fmplugins.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_code.py', 'plugin/tests/test_plugins.py', 'MASTER.md', 'CHANGELOG.md']
- 2026-10-23T09:55:41Z focused
- 2026-10-23T09:59:32Z done
- 2026-10-23T09:59:34Z committed 381a2cce (7 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-fm-anthropic-catalogue: Source: research/brainstorm-20261021-120257 (fm ideas, 10 lenses, 4 rounds, 3 deepened, --seen every earlier ideas.md: 520 ne…
- T-1405 [FIX M, done, 4 steps] Crash hygiene: stack dumps for hung verbs, safe stale index.lock removal, a lock probe in doctor — lesson: A safety rule written as 'unknow…
- T-1410 [FEATURE S, done, 2 steps] fm vetoes prints the command that retracts each veto, and that command removes exactly it — lesson: A record the user can create should…
- decision 2026-10-15: Recommendation: build T-0969..T-0975 (edit-time test-first note, background affected tests, fm rule, tool-output injection flag, fm cost --forecast,…
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_code.py, plugin/tests/test_plugins.py
## Preflight
Changed in scope since this was planned (2026-10-21): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmcode.py, plugin/lib/fmplugins.py, plugin/tests/test_code.py; re-ground the plan against them before editing
## Lessons
- Stack cards name tools (cargo) more often than languages; search plugins by the card and its area, or the language the tool implies is never matched
## Plan gaps
- failed first: step 1 failing tests, then skill_offer at run start and fmplugins.suggest with the verb
## Files touched
- plugin/tests/test_code.py
- plugin/tests/test_plugins.py
- plugin/lib/fmplugins.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmcli.py
- plugin/lib/fmcode.py
