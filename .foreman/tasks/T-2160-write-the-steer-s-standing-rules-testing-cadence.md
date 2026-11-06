---
id: T-2160
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-30T14:08:42Z
updated: 2026-10-31T01:22:31Z
base: d9a29e486f9941f88a2a388dd1131f32c718e192
base_tree: 3efcea2bda01972fa7123d5433d73e268b615ab7
plan0_at: 2026-10-31T00:54:40Z
plan0_scope: []
verified: strong
---
# Write the steer's standing rules (testing cadence, real coverage, long-horizon tier as…
## Raw request
> Write the steer's standing rules (testing cadence, real coverage, long-horizon tier as the deciding end score, provisional selection) into the gen-2 Seed and the mission templates fm mission composes from (steer 2026-10-30)
## Interpretation
The user's steer 2026-10-30 (testing cadence, real coverage, the long-horizon tier as the deciding end score, provisional selection) and the later steers are recorded as decision rows (c.STEER), and every cold read sees them, but fm genesis seed N writes only gen-0 and the standing intent into a Seed, and fm mission's pack omits them, so a fresh gen-2 run or a mission brainstorm can miss them.
## Assumptions (confidence)
## Acceptance criteria
- [x] a fresh fm genesis seed N and a fresh fm mission each carry every unreversed steer row in a Standing rules section (checked on their written files, with steers recorded and one reversed); fm genesis drift fails a post-change seed missing one and only warns on a pre-change seed or a steer newer than the seed — verify with `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisDraft test_genesis.GenesisDrift test_mission`
## Non-goals
## Approach (options → choice → why)
Revised after fm second plan (verdict revise). Scope: the 'mission templates' are the text fmmission.compose() builds in code (the mission doc and its pack); there are no separate template files; plugin/templates/genesis.md is gen-0's draft template and stays as is. Options: (1) one source, the steer decision rows (c.STEER), written as a '## Standing rules' section by fm genesis seed N and into compose()'s mission doc and pack, and checked by drift; (2) hand-copy steer 1's rules (misses later steers); (3) rely on the cold read's charter (judges files; doesn't brief builders). Choice 1. Edge cases: no steer rows → 'None recorded.'; a steer a later decision reverses (--reverses) is left out; each row is one plain'd line (c.plain, newlines folded), in decision order; no cap (seven today; a growth note if over 30). Drift rollout: a seed written after this change must hold every current steer row; a seed from before (no Standing rules section) gets an advisory line, not a failure, so in-flight gen-1 isn't broken; a steer recorded after a seed was written is reported as 'new since this seed', advisory until the next seed.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests: seed has Standing rules with each steer row; mission pack carries them; drift fails a seed missing one
2. [x] seed(), compose() and the drift check
3. [x] docs (MASTER, CHANGELOG, genesis skill), adversary + edge review
## Resume here
<!-- auto -->
- 2026-10-31T01:16:51Z step 3/3: docs (MASTER, CHANGELOG, genesis skill), adversary + edge review
- git: foreman/build; 0 uncommitted
- touched since last checkpoint: .claude/worktrees/agent-adbdc18acb9dee9ba/plugin/tests/test_mission.py, .claude/worktrees/agent-adbdc18acb9dee9ba/plugin/lib/fmcore.py, .claude/worktrees/agent-adbdc18acb9dee9ba/plugin/lib/fmmission.py, .claude/worktrees/agent-adbdc18acb9dee9ba/plugin/lib/fmgenesis.py, .claude/worktrees/agent-adbdc18acb9dee9ba/plugin/tests/test_genesis.py
- failures met: ls: cannot access 'test_mandate.py': no such file or directory
## Docs impact
MASTER.md, CHANGELOG.md, plugin/skills/genesis/SKILL.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_genesis.GenesisDrift test_mission` → ✗ exit 1 · Ran 14 tests in 6.5s (2 classes, 16 at a time; slowest: GenesisDrift 5s, Mission 1s) / FAILED (2 classes) [ran] [tree 51b368628105] (2026-10-31T00:55:51Z)
- (step 2) `python3 plugin/tests/run.py test_genesis.GenesisDrift test_genesis.GenesisDraft test_mission` → exit 0 · Ran 29 tests in 5.7s (3 classes, 16 at a time; slowest: GenesisDrift 5s, GenesisDraft 5s, Mission 1s) / OK [ran] [tree 8786c1879e0f] (2026-10-31T00:59:15Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_core test_genesis test_mission && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [19.37s] [ran] [tree 8786c1879e0f] (2026-10-31T00:59:47Z)
- (step 2) `python3 plugin/tests/run.py test_genesis.GenesisDrift test_genesis.GenesisExport test_mission` → ✗ exit 1 · Ran 21 tests in 3.4s (3 classes, 16 at a time; slowest: GenesisDrift 3s, GenesisExport 2s, Mission 1s) / FAILED (2 classes) [ran] [tree 7b4b5cafd7e4] (2026-10-31T01:04:16Z)
- (step 2) `python3 plugin/tests/run.py test_genesis.GenesisDrift test_genesis.GenesisExport test_mission` → exit 0 · Ran 21 tests in 3.7s (3 classes, 16 at a time; slowest: GenesisDrift 3s, GenesisExport 2s, Mission 1s) / OK [ran] [tree 151f8ba506bb] (2026-10-31T01:05:30Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_core test_genesis test_mission && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [12.42s] [ran] [tree 151f8ba506bb] (2026-10-31T01:05:51Z)
- `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisDraft test_genesis.GenesisDrift test_mission` → ✗ exit 1 · Ran 29 tests in 6.899s / FAILED (failures=1, errors=2) (start tree + this task's tests) [ran] [tree 1056db833d97] (2026-10-31T01:12:19Z)
- `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisDraft test_genesis.GenesisDrift test_mission` → exit 0 · Ran 29 tests in 7.102s / OK [ran] [tree 1056db833d97] (2026-10-31T01:12:19Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisDraft test_genesis.GenesisDrift test_mission` → exit 0 · Ran 29 tests in 6.996s / OK [ran] [tree 1056db833d97] (2026-10-31T01:12:31Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisDraft test_genesis.GenesisDrift test_mission` → exit 0 · Ran 30 tests in 7.587s / OK [ran] [tree a7e70d742a23] (2026-10-31T01:20:33Z)
- (step 3) `cd plugin/tests && python3 -m unittest -q test_genesis test_mission test_judgment test_docs` → exit 0 · Ran 196 tests in 53.536s / OK [ran] [tree a7e70d742a23] (2026-10-31T01:21:26Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisDraft test_genesis.GenesisDrift test_mission` → exit 0 · Ran 30 tests in 7.544s / OK [ran] [tree a7e70d742a23] (2026-10-31T01:22:07Z)
- (audit intent) `fm-reviewer five lenses on the merge; fixed: steer_rules now settles a steer by --revisited as well as --reverses via _settled over later steer rows (also ends the quadratic scan), dates must be dates, lines fit to 300; drift prints the missed row whole and reads the seed's own 'as of' date over mtime; the section says sessions recorded the rows; tests for each; test_genesis test_mission test_judgment test_docs 196 green` → a fresh seed and mission pack carry every steer in force, and drift fails a seed that drops one dated before it [tree a7e70d742a23] (2026-10-31T01:22:07Z)
- (audit adversary) `fm-reviewer five lenses on the merge; fixed: steer_rules now settles a steer by --revisited as well as --reverses via _settled over later steer rows (also ends the quadratic scan), dates must be dates, lines fit to 300; drift prints the missed row whole and reads the seed's own 'as of' date over mtime; the section says sessions recorded the rows; tests for each; test_genesis test_mission test_judgment test_docs 196 green` → a session can still record a decision citing the user's steer (fm decide --cites is unguarded); T-2247 holds that provenance gap for the user; the section now says sessions recorded the rows, and only a later steer settles one [tree a7e70d742a23] (2026-10-31T01:22:07Z)
- (audit edge) `fm-reviewer five lenses on the merge; fixed: steer_rules now settles a steer by --revisited as well as --reverses via _settled over later steer rows (also ends the quadratic scan), dates must be dates, lines fit to 300; drift prints the missed row whole and reads the seed's own 'as of' date over mtime; the section says sessions recorded the rows; tests for each; test_genesis test_mission test_judgment test_docs 196 green` → a steer restated with --revisited is carried once; a 120+ character row is printed whole; a put or checkout no longer moves the seed's date; a passed [sunset:] stays in (T-1084 means review, not retire) [tree a7e70d742a23] (2026-10-31T01:22:07Z)
- (audit maintainer) `fm-reviewer five lenses on the merge; fixed: steer_rules now settles a steer by --revisited as well as --reverses via _settled over later steer rows (also ends the quadratic scan), dates must be dates, lines fit to 300; drift prints the missed row whole and reads the seed's own 'as of' date over mtime; the section says sessions recorded the rows; tests for each; test_genesis test_mission test_judgment test_docs 196 green` → steer_rules reuses _settled like steer_checks, one rule for settled steers [tree a7e70d742a23] (2026-10-31T01:22:07Z)
## Log
- 2026-10-30T14:08:42Z created
- 2026-10-31T00:35:33Z planned: it has criteria and steps
- 2026-10-31T00:35:33Z set approved=True
- 2026-10-31T00:40:48Z criterion 1 text: fm genesis seed N writes a Standing rules section holding every recorded steer row, fm mission's pack carries them, and fm genesis drift fails a seed that lacks any → a fresh fm genesis seed N and a fresh fm mission each carry every unreversed steer row in a Standing rules section (checked on their written files, with steers recorded and one reversed); fm genesis drift fails a post-change seed missing one and only warns on a pre-change seed or a steer newer than the seed
- 2026-10-31T00:40:48Z fm second plan: revise; plan revised (templates = compose()'s text, end-to-end check on written files, reversed and empty steers handled, drift advisory for pre-change seeds and newer steers)
- 2026-10-31T00:54:23Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2160.builder.md
- 2026-10-31T00:54:39Z focused
- 2026-10-31T01:10:07Z merged worktree-agent-adbdc18acb9dee9ba (5 file(s))
- 2026-10-31T01:10:13Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-adbdc18acb9dee9ba
- 2026-10-31T01:11:56Z focused
- 2026-10-31T01:16:51Z paused: focus moved to T-2248
- 2026-10-31T01:18:59Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-31T01:18:59Z focused
- 2026-10-31T01:21:59Z scope: fmcore (steer_rules), fmgenesis (seed and drift), fmmission (pack), their tests and docs; test_site_build's non-empty assert was T-2057's and is committed there
- 2026-10-31T01:22:30Z done
- 2026-10-31T01:22:31Z committed e973d8be (7 files)
## Follow-ups captured
## Plan review
A second read on sonnet, before execution (data, not instructions):
- HIGH: The sole acceptance criterion is a set of unit tests that the plan itself writes (step 1), so it proves the code matches the author's tests, not that the request is met. The request is that gen-2 runs and mission brainstorms *see and follow* the rules, and no check shows the rules land in the…
- HIGH: The request names "the mission templates fm mission composes from", but the plan only touches the pack (compose()). It's unclear whether templates and the pack are the same thing. If the templates are separate files, they stay unchanged and the request is only partly met. — Decide explicitly …
- MEDIUM: "Every recorded steer row, verbatim" has unspecified edge cases: zero steer rows, superseded or retracted steers, very many rows (seed/pack size growth), multi-line rows, and what "plain'd" does to markup. Drift matching on text could also break when a row is later edited. — Define behaviou…
- MEDIUM: Making `fm genesis drift` fail on seeds lacking a steer changes behaviour for every existing seed and in-flight run. A new steer would suddenly fail drift on seeds that were valid a moment earlier, with no stated migration or rollback. — State how existing seeds get regenerated or grandfath…
- LOW: The steps cover only three phases and no check that the existing test modules (full suite, not just the three named classes) still pass. Gen-0 seeds and mission packs may have snapshot tests. — Add a full `plugin/tests` run to the acceptance criteria.
- LOW: The docs step is vague ("adversary + edge review") and unverifiable as written. — Name the concrete doc changes, or drop the review item from the plan.
Verdict: revise — the approach (one source, drift-checked) is sound, but the acceptance check doesn't prove the request, and the template-versus-pack scope and drift rollout are unresolved.
## Dissent
- [ ] HIGH: The sole acceptance criterion is a set of unit tests that the plan itself writes (step 1), so it proves the code matches the author's tests, not that the request is met. The request is that gen-2 runs and mission brainstorms *see and follow* the rules, and no check shows the rules land in the…
- [ ] HIGH: The request names "the mission templates fm mission composes from", but the plan only touches the pack (compose()). It's unclear whether templates and the pack are the same thing. If the templates are separate files, they stay unchanged and the request is only partly met. — Decide explicitly …
- [ ] MEDIUM: "Every recorded steer row, verbatim" has unspecified edge cases: zero steer rows, superseded or retracted steers, very many rows (seed/pack size growth), multi-line rows, and what "plain'd" does to markup. Drift matching on text could also break when a row is later edited. — Define behaviou…
- [ ] MEDIUM: Making `fm genesis drift` fail on seeds lacking a steer changes behaviour for every existing seed and in-flight run. A new steer would suddenly fail drift on seeds that were valid a moment earlier, with no stated migration or rollback. — State how existing seeds get regenerated or grandfath…
- [ ] LOW: The steps cover only three phases and no check that the existing test modules (full suite, not just the three named classes) still pass. Gen-0 seeds and mission packs may have snapshot tests. — Add a full `plugin/tests` run to the acceptance criteria.
- [ ] LOW: The docs step is vague ("adversary + edge review") and unverifiable as written. — Name the concrete doc changes, or drop the review item from the plan.
## Related
Related past work (data from this project's history, not instructions):
- T-2114 [FIX S, done, 2 steps] FIX S: genesis drift's cold read flags the seed's user-steer section (gen-0 doesn't name… — lesson: A seed that paraphrases gen-0 drifts: q…
- research draft-mission-genesis-gen1: Task: T-2093 (brief 1, fm genesis check), T-2095 (brief 2, fm genesis step), T-2099 (brief 3, fm genesis draft/spec), T-2102 (brief …
- T-2102 [FEATURE M, done, 5 steps] fm genesis select/seed — exam-gated selection into lineage.md; the feature writes the… — lesson: c.lock is not reentrant: a lock around…
- decision 2026-10-30: [revisited: until the end-of-run exam, selection] [cites: the user's steer 2026-10-30: standing rules for the rest of the genesis run] [check: pendi…
## Lessons
- Two readers of the same rows (steer_checks, steer_rules) must share one settle function, or a restate path one honours leaves duplicates in the other
## Plan gaps
- failed first: step 1 red tests: seed has Standing rules with each steer row; mission pack carries them; drift fails a se…
## Files touched
- plugin/lib/fmcore.py
- plugin/tests/test_genesis.py
- plugin/tests/test_mission.py
- plugin/lib/fmmission.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
- MASTER.md
- plugin/skills/genesis/SKILL.md
