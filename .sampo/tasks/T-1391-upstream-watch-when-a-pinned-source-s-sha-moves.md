---
id: T-1391
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmscout.py, plugin/tests/test_scout.py, MASTER.md, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-21T17:28:43Z
updated: 2026-10-23T10:01:29Z
inferred_deps: [T-1382]
inferred_why: T-1382: named in its request
base: 381a2cce68ca2d2d419a68f6eff0b7fef28dbe37
base_tree: 0099da113f3fcb6ad62594584542affba34251e2
plan0_at: 2026-10-23T09:59:47Z
plan0_scope: [plugin/lib/fmscout.py, plugin/tests/test_scout.py, MASTER.md, CHANGELOG.md]
verified: strong
---
# Upstream watch: when a pinned source's sha moves, one finding lists added, removed and ren
## Raw request
> FEATURE: Upstream watch: when a pinned source's sha moves, one finding lists added, removed and renamed items with the licence class (nothing installs); git ls-remote skips unchanged sources; Claude Code CHANGELOG lines with no Foreman match become captures (S4, A14 A34 B2)
> CONTEXT: round 2 of the fm/fm code brainstorm (T-1382): research/brainstorm-fm-anthropic-catalogue.md, grounding with file:line in research/brainstorm-fm-anthropic-half-a.md (A*) and half-b.md (B*)
> DONE-WHEN: a fixture source whose sha moved yields exactly one capture and an unchanged sha makes no fetch; a fixture changelog yields one capture per unmatched feature
## Interpretation
fm scout's slow sources probe: a stale source whose remote HEAD (git ls-remote, no fetch) equals its pinned commit is skipped; one that moved is refreshed, and when its items changed it is one RESEARCH finding listing added, removed and renamed skills (a rename keeps its path) with the licence class. Nothing installs. New probe: each bullet of Claude Code's CHANGELOG (the indexed anthropic-claude-code checkout, data only) past CC_TESTED whose backticked names appear nowhere in Foreman's own text becomes a finding. Capture bounds (3 a run, 5 open) still apply.
## Assumptions (confidence)
## Acceptance criteria
- [x] a fixture source whose sha moved yields exactly one finding and an unchanged sha makes no fetch; a fixture changelog yields one finding per unmatched feature — verify with `python3 plugin/tests/run.py test_scout`
## Non-goals
## Approach (options → choice → why)
Options: fetch every source weekly and diff (network and disk for nothing when unchanged); poll GitHub's API (needs a token, GitHub only); ls-remote then refresh only on a move, diffing the two indexes by path. Choice: the last. Changelog matching by backticked names (flags, commands, settings) against Foreman's README, MASTER, CHANGELOG, rules, skills and lib: prose-only bullets are skipped rather than guessed.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests, then ls-remote skip, index_delta finding and probe_cc_changelog
## Resume here
## Docs impact
CHANGELOG.md, MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_scout.ScoutProbes` → ✗ exit 1 · Ran 10 tests in 1.2s (1 classes, 16 at a time; slowest: ScoutProbes 1s) / FAILED (1 classes) [ran] [tree 34afe088a5ee] (2026-10-23T09:59:54Z)
- (step 1) `python3 plugin/tests/run.py test_scout` → exit 0 · Ran 19 tests in 11.4s (3 classes, 16 at a time; slowest: Scout 11s, ScoutDrive 2s, ScoutProbes 1s) / OK [ran] [tree 57d1a0c579aa] (2026-10-23T10:00:56Z)
- (ac 1) `python3 plugin/tests/run.py test_scout` → exit 0 · Ran 19 tests in 11.4s (3 classes, 16 at a time; slowest: Scout 11s, ScoutDrive 2s, ScoutProbes 1s) / OK [ran] [tree 57d1a0c579aa] (2026-10-23T10:01:08Z)
- (audit intent) `self review; test_scout green; a dry scout run on this machine reports no probe errors` → a source whose remote HEAD is its pin isn't fetched; one that moved is one finding with added, removed and renamed items and its licence class; each changelog bullet past CC_TESTED naming something Foreman never mentions is a finding (tests) [tree 57d1a0c579aa] (2026-10-23T10:01:08Z)
- (audit adversary) `self review; test_scout green; a dry scout run on this machine reports no probe errors` → upstream text is data: names and bullets go through c.plain and fit before they reach a title, ls-remote runs with the source's safe git config and '--' before the URL, nothing from a source is run or installed, and captures stay bounded (3 a run, 5 open) [tree 57d1a0c579aa] (2026-10-23T10:01:08Z)
## Log
- 2026-10-21T17:28:43Z created
- 2026-10-23T09:45:51Z set tier=M, scope=['plugin/lib/fmscout.py', 'plugin/tests/test_scout.py', 'MASTER.md', 'CHANGELOG.md']
- 2026-10-23T09:59:46Z focused
- 2026-10-23T10:01:27Z done
- 2026-10-23T10:01:29Z committed 35a9f342 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1397 [FEATURE M, done, 1 steps] Intake offer: fm code prints one line when an indexed skill matches the request (name, lic — lesson: Stack cards name tools (cargo) mor…
- research brainstorm-fm-anthropic-catalogue: Source: research/brainstorm-20261021-120257 (fm ideas, 10 lenses, 4 rounds, 3 deepened, --seen every earlier ideas.md: 520 ne…
- T-1405 [FIX M, done, 4 steps] Crash hygiene: stack dumps for hung verbs, safe stale index.lock removal, a lock probe in doctor — lesson: A safety rule written as 'unknow…
- decision 2026-10-20: The recursive brainstorm loop is dry after round 1: a two-lens probe past the 368 earlier ideas gave 51 titles, 2 of real value after grounding (rep…
- likely tests for the scope: plugin/tests/test_scout.py
## Preflight
Changed in scope since this was planned (2026-10-21): CHANGELOG.md, MASTER.md, plugin/lib/fmscout.py, plugin/tests/test_scout.py; re-ground the plan against them before editing
## Lessons
- Ask the remote before fetching it: git ls-remote names the head in one round trip, so a weekly refresh of an unchanged source costs nothing
## Plan gaps
- failed first: step 1 failing tests, then ls-remote skip, index_delta finding and probe_cc_changelog
## Files touched
- plugin/tests/test_scout.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmscout.py
