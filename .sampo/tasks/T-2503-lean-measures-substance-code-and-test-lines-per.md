---
id: T-2503
type: FEATURE
tier: M
status: done
priority: urgent
scope: []
depends_on: []
source: user
created: 2026-11-01T19:16:31Z
updated: 2026-11-01T20:44:43Z
base: fbb6e81d8eade085e2d513e1d3abc414fb7bc15c
base_tree: fded83ca6f4681847d62991f8fab6659ee5e2aac
predict_minutes: 10
predict_attempts: 1
plan0_at: 2026-11-01T20:24:58Z
plan0_scope: []
verified: strong
---
# Lean measures substance: code and test lines per module, hook p95, injected context,…
## Raw request
> FEATURE!: lean measures substance: code and test lines per module, hook p95, injected context, verb count and dependency count, each against the previous generation; net growth needs a per-capability exam or outcome gain or it files a subtraction task; a lean check that only counts rules or skill text fails
> DONE-WHEN: the sweep's lean row reads those five measures against the previous generation's record and files a subtraction task for unearned growth
## Interpretation
Readings: (a) likeliest: the sweep's lean row measures substance beside the always-on footprint: code lines and test lines per module, hook p95, injected context (SessionStart and UserPromptSubmit chars), verb count and dependency count, each against the previous generation's record; net code growth is judged per capability from its Mission's commits: with an exam or outcome gain it passes, unmeasured it waits (pending, no task: the user's answer of 2026-11-01), measured with no gain it files a subtraction task. (b) Replace the rules/skill metrics with substance ones: rejected, the user called a rules-only check a bug, not the rules metrics wrong; both stay. Fails if: a Mission's commits don't name its task ids (then its growth is unattributed and reported as such).
## Assumptions (confidence)
## Acceptance criteria
- [x] the lean row reports code lines, test lines, dependencies, hook p95, injected chars and verbs against the previous generation; a Mission's growth with an exam or outcome gain passes, unmeasured growth is listed as pending with no task, measured growth with no gain turns the row red and files one subtraction task; a check counting only rules or skill text is gone — verify with `python3 plugin/tests/run.py test_genesis.LeanSubstance`
## Non-goals
## Approach (options → choice → why)
1) _lean() adds code lines, test lines, dependencies (non-stdlib top-level imports in plugin/lib) and keeps per-module lines in the record; record_lean stores injected chars when the doctor's bench ran; _growth(p, n) attributes numstat line deltas to each Mission by its T-ids' commits and reads the capability's gain from the scorecard against the previous generation and its tasks' survival; the lean row reports gains, pending growth, and files one CLEAN capture per measured no-gain capability. Fails if: the scorecard is all 'too few' (then all growth is pending, as the user chose). 2) Judge total growth only. Fails if: the user asked per capability. 3) use what exists: fmdoctor.check_footprint's ratchet for substance too. Fails if: a strict ratchet forbids all growth, which the user's rule allows when earned. 4) do less: report the numbers with no judgment. Fails if: growth with no gain never becomes a subtraction task. Choice 1 (80%): every measure the user named, judged by the rule they gave, with the waiting case recorded.
## Risks and rollback
Line counts are cheap (a few hundred files). Attribution by commit subject 'T-NNNN:' misses squashed or unlabeled commits: reported as unattributed growth, never silently dropped. Rollback: revert; older lean records lack the new metrics and are read as not judged for them.
## Execution prompt
## Steps
1. [x] red tests: LeanSubstance (metrics, attribution, gain/pending/no-gain, subtraction task once)
2. [x] _lean metrics + record + _growth + lean row
3. [x] docs: genesis skill, MASTER, CHANGELOG
## Resume here
## Docs impact
plugin/skills/genesis/SKILL.md, MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_genesis.LeanSubstance` → ✗ exit 1 · Ran 3 tests in 1.0s (1 classes, 16 at a time; slowest: LeanSubstance 1s) / FAILED (1 classes: test_genesis.LeanSubstance) [ran] [tree 8f0e51887f95] (2026-11-01T20:26:01Z)
- (step 1) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 197 tests in 22.5s (21 classes, 16 at a time; slowest: GenesisRead 22s, GenerationReview 20s, GenesisCheck 17s) / OK [ran] [tree b1cc49087b3f] (2026-11-01T20:29:02Z)
- (step 2) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 197 tests in 24.0s (21 classes, 16 at a time; slowest: GenesisRead 24s, GenerationReview 20s, GenesisCheck 19s) / OK [ran] [tree b1cc49087b3f] (2026-11-01T20:29:27Z)
- (step 3) `python3 plugin/tests/run.py test_genesis` → exit 0 · Ran 197 tests in 23.2s (21 classes, 16 at a time; slowest: GenesisRead 23s, GenerationReview 20s, GenesisCheck 17s) / OK [ran] [tree b1cc49087b3f] (2026-11-01T20:29:51Z)
- `python3 plugin/tests/run.py test_genesis.LeanSubstance` → ✗ exit 1 · Ran 3 tests in 2.5s (1 classes, 16 at a time; slowest: LeanSubstance 1s) / FAILED (1 classes: test_genesis.LeanSubstance) (start tree + this task's tests) [ran] [tree b1cc49087b3f] (2026-11-01T20:29:55Z)
- `python3 plugin/tests/run.py test_genesis.LeanSubstance` → exit 0 · Ran 3 tests in 1.0s (1 classes, 16 at a time; slowest: LeanSubstance 1s) / OK [ran] [tree b1cc49087b3f] (2026-11-01T20:29:55Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis.LeanSubstance` → exit 0 · Ran 3 tests in 0.6s (1 classes, 16 at a time; slowest: LeanSubstance 0s) / OK [ran] [tree b1cc49087b3f] (2026-11-01T20:36:44Z)
- (audit intent) `main-thread review of the diff: growth comes from git numstat over the generation's commits (no snapshot needed, so gen 2 is judged though its lean record predates these measures); attribution by commit subject T-id to each Mission; unmeasured growth waits per the user's answer; the strict ratchet for always-on text and hook p95 is unchanged` → the user's part 3 with their answer: code and test lines per module and dependencies against the generation's start, growth judged per capability by gain, unmeasured growth pending with no task, measured no-gain red with one subtraction task [tree b1cc49087b3f] (2026-11-01T20:36:44Z)
- (audit edge) `main-thread review of the diff: growth comes from git numstat over the generation's commits (no snapshot needed, so gen 2 is judged though its lean record predates these measures); attribution by commit subject T-id to each Mission; unmeasured growth waits per the user's answer; the strict ratchet for always-on text and hook p95 is unchanged` → no start commit leaves growth not judged (said); unlabeled commits are reported as unattributed lines, never dropped; a new dependency follows the generation's verdict; capture_once's key now sits on its own line so a rerun files nothing twice (the same latent miss in T-2501's review_fixes is fixed too) [tree b1cc49087b3f] (2026-11-01T20:36:44Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm ask: text in a file; a run of a documented command proves it (--yes-run) / · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a f [ran] [tree b1cc49087b3f] (2026-11-01T20:38:51Z)
## Log
- 2026-11-01T19:16:31Z created
- 2026-11-01T19:18:58Z steer: unmeasured growth waits (pending on the lean row, no task); only measured growth with no gain files a subtraction task
- 2026-11-01T20:16:43Z planned: it has criteria and steps
- 2026-11-01T20:24:57Z set approved=True
- 2026-11-01T20:24:57Z focused
- 2026-11-01T20:24:58Z predicted from its closes: 10 min, 1 attempt(s)
- 2026-11-01T20:29:55Z scope: fmgenesis _growth/_gain/_deps/_substance_row + sweep row + glob import + capture_once key lines (also review_fixes), test_genesis LeanSubstance, genesis SKILL.md, MASTER, CHANGELOG
- 2026-11-01T20:38:21Z done
- 2026-11-01T20:38:24Z committed 90673f93 (5 files)
- 2026-11-01T20:38:51Z guard authorization added: publish
- 2026-11-01T20:44:43Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2359 [FEATURE M, done, 3 steps] Each generation's sweep fails on net growth: footprint, hook p95 and verbs at the seed vs at the sweep (Mission 8, #12) — lesson: A no-…
- decision 2026-11-01: [costly] [cites: user steer 2026-11-01: cross-cutting review, gap map redraw, lean substance, proof before presentation, sealed prediction and blind…
- decision 2026-11-01: [cites: user steer 2026-11-01: unmeasured growth waits instead of filing a subtraction task] [check: python3 plugin/tests/run.py test_genesis.LeanSu…
- T-2358 [FEATURE M, done, 3 steps] The lean ratchet measures what gen-0 names: hook p95 and injected context, and only a cut pays for growth (Mission 8, #12) — lesson: Ne…
## Lessons
- capture_once's key dedupes only on a raw-request line that starts with it: a caller that passes key= must also put the key on its own line in the text
## Plan gaps
- failed first: step 1 red tests: LeanSubstance (metrics, attribution, gain/pending/no-gain, subtraction task once)
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
- CHANGELOG.md
- MASTER.md
- plugin/skills/genesis/SKILL.md
