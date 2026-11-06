---
id: T-2504
type: FEATURE
tier: M
status: done
priority: urgent
scope: []
depends_on: []
source: user
created: 2026-11-01T19:16:31Z
updated: 2026-11-01T20:59:01Z
base: 90673f93f9280d284360ffee873a56c1466344cb
base_tree: b1cc49087b3f434d6518f6d83c85494116536f41
predict_minutes: 10
predict_attempts: 1
plan0_at: 2026-11-01T20:38:33Z
plan0_scope: []
verified: strong
---
# Proof before presentation: the sweep compares the site's and README's public claims…
## Raw request
> FEATURE!: proof before presentation: the sweep compares the site's and README's public claims (numbers, "passes", capability statements) to the exam lines and fm outcomes, and goes red on a claim that runs ahead of them
> DONE-WHEN: a README or site claim with no exam or outcome line behind it turns the sweep row red, naming the claim and file
## Interpretation
Readings: (a) likeliest: a sweep row 'proof before presentation' that reads the public prose (README.md, site/index.html, the string constants of site/pages.py) for result claims (a count 'N of M' or 'N/M', a percentage, a ratio 'Nx', or a comparison: beats, outperforms, better/faster/cheaper than) and requires each to name its proof: an exam run id that exam.jsonl holds, a task whose brief recorded the measurement (T-NNNN with an evidence row), or live data (fm outcomes, fm exam scorecard, a chart drawn from site/stats.json); it also refuses a line saying a gen-0 capability passes while the scorecard doesn't. Today's site has static results with no source (44 of 105 hidden tests; 0 of 6 vs 1 of 6, 33% more). (b) Judge claims with a model: rejected, the user asked the sweep to compare claims with exam lines, which a mechanical match does and a model opinion doesn't.
## Assumptions (confidence)
## Acceptance criteria
- [x] a README or site result claim with no exam run, measured task or live source turns the sweep's 'proof before presentation' row red naming file:line; with a resolvable source it passes; a capability-pass claim the scorecard doesn't show is red; the site's static results today carry their sources — verify with `python3 plugin/tests/run.py test_genesis.ProofBeforePresentation`
## Non-goals
## Approach (options → choice → why)
1) _claims(root) extracts result-shaped sentences from the three sources (pages.py by ast string constants with 5+ words, so SVG and code strings stay out); _claim_row(p) checks each for a resolvable proof and checks capability-pass lines against scorecard(); red lines name file:line and the claim; then the two site lines found today get their sources. Fails if: a mechanism statement trips the regex (it then needs its source or a rewording, which is cheap). 2) use what exists: fm prove --docs, which checks documented commands run. Fails if: it proves commands, not result numbers. 3) do less: forbid numbers in prose entirely. Fails if: honest reported results (including losses) would vanish instead of being tied to their record. Choice 1 (80%): every number a reader sees is tied to a record a sweep can resolve.
## Risks and rollback
False positives on mechanism lines (thresholds like 'at 85%' in the README): the regex excludes a percentage after 'at' or 'over' that names a threshold, and such lines can name their source. Rollback: revert; the sources added to the site prose stay as plain text.
Blast radius (fm graph blast): co-changes CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/tests/test_docs.py, plugin/lib/fmcode.py; past FIXes T-1117, T-1209, T-1239, T-2060, T-2061.
## Execution prompt
## Steps
1. [x] red tests: ProofBeforePresentation (extraction, sources, capability claims, sweep row)
2. [x] _claims + _claim_row + sweep row; source the two site lines
3. [x] docs: genesis skill, MASTER, CHANGELOG
## Resume here
## Docs impact
plugin/skills/genesis/SKILL.md, MASTER.md, CHANGELOG.md, README.md, site/pages.py
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_genesis.ProofBeforePresentation` → ✗ exit 1 · Ran 3 tests in 14.7s (1 classes, 16 at a time; slowest: ProofBeforePresentation 14s) / FAILED (1 classes: test_genesis.ProofBeforePresentation) [ran] [tree 6a4a2decab59] (2026-11-01T20:39:37Z)
- (step 1) `python3 plugin/tests/run.py test_genesis.ProofBeforePresentation test_site test_docs` → exit 0 · Ran 143 tests in 17.9s (46 classes, 16 at a time; slowest: ProofBeforePresentation 17s, Fences 11s, DocsProof 6s) / OK [ran] [tree 5acd793e0be4] (2026-11-01T20:42:16Z)
- (step 2) `python3 plugin/tests/run.py test_genesis.ProofBeforePresentation test_site test_docs` → exit 0 · Ran 143 tests in 16.4s (46 classes, 16 at a time; slowest: ProofBeforePresentation 16s, Fences 10s, Header 6s) / OK [ran] [tree 5acd793e0be4] (2026-11-01T20:42:33Z)
- (step 3) `python3 plugin/tests/run.py test_genesis.ProofBeforePresentation test_site test_docs` → exit 0 · Ran 143 tests in 16.2s (46 classes, 16 at a time; slowest: ProofBeforePresentation 16s, Fences 11s, Header 6s) / OK [ran] [tree 5acd793e0be4] (2026-11-01T20:42:50Z)
- `python3 plugin/tests/run.py test_genesis.ProofBeforePresentation` → ✗ exit 1 · Ran 3 tests in 16.1s (1 classes, 16 at a time; slowest: ProofBeforePresentation 14s) / FAILED (1 classes: test_genesis.ProofBeforePresentation) (start tree + this task's tests) [ran] [tree 5acd793e0be4] (2026-11-01T20:43:22Z)
- `python3 plugin/tests/run.py test_genesis.ProofBeforePresentation` → exit 0 · Ran 3 tests in 15.4s (1 classes, 16 at a time; slowest: ProofBeforePresentation 15s) / OK [ran] [tree 5acd793e0be4] (2026-11-01T20:43:22Z)
- (ac 1) `python3 plugin/tests/run.py test_genesis.ProofBeforePresentation` → exit 0 · Ran 3 tests in 9.0s (1 classes, 16 at a time; slowest: ProofBeforePresentation 9s) / OK [ran] [tree 5acd793e0be4] (2026-11-01T20:50:12Z)
- (audit intent) `main-thread review of the diff: claims come from three public sources (README, site/index.html, site/pages.py constants by ast); a source on the claim's line or constant counts; code spans and SVG strings are skipped; the real repo's 9 hits were triaged: two historical results now cite T-1242 and T-1231 (both briefs hold evidence), two data-rendered sentences cite stats.json, three rule or sample lines carry the rule mark, one mechanism desc was reworded` → the user's part 4: the sweep compares public claims with the record, red on a result with no exam run, measured task or live source, and on a capability said to pass while the scorecard doesn't [tree 5acd793e0be4] (2026-11-01T20:50:12Z)
- (audit edge) `main-thread review of the diff: claims come from three public sources (README, site/index.html, site/pages.py constants by ast); a source on the claim's line or constant counts; code spans and SVG strings are skipped; the real repo's 9 hits were triaged: two historical results now cite T-1242 and T-1231 (both briefs hold evidence), two data-rendered sentences cite stats.json, three rule or sample lines carry the rule mark, one mechanism desc was reworded` → a threshold after at/over/above/under isn't a result; a marked rule line is exempt by an explicit, reviewable marker; a T-id source must be a brief with recorded evidence, not just any id [tree 5acd793e0be4] (2026-11-01T20:50:12Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm ask: text in a file; a run of a documented command proves it (--yes-run) / · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a f [ran] [tree 5acd793e0be4] (2026-11-01T20:52:28Z)
## Log
- 2026-11-01T19:16:31Z created
- 2026-11-01T20:31:21Z planned: it has criteria and steps
- 2026-11-01T20:32:11Z sources found for today's static site results: '44 of 105 hidden tests' was introduced by T-1242 (da7e4e23, the long session and marathon), '0 of 6 for Foreman, 1 of 6 for Claude Code, 33% more' by T-1231 (f72c440f, the first duel's history): cite each task id in the prose, and the check confirms each brief recorded evidence
- 2026-11-01T20:38:32Z set approved=True
- 2026-11-01T20:38:32Z focused
- 2026-11-01T20:38:33Z predicted from its closes: 10 min, 1 attempt(s)
- 2026-11-01T20:43:23Z scope: fmgenesis _prose/_claim_row/RESULT/SOURCE/RULE_MARK + sweep row, site/pages.py (two sources, two stats.json sources, one rule mark, one reworded desc), README.md (one rule mark), test_genesis ProofBeforePresentation, genesis SKILL.md, MASTER, CHANGELOG
- 2026-11-01T20:51:59Z done
- 2026-11-01T20:52:01Z committed ec8f2f2d (7 files)
- 2026-11-01T20:52:28Z guard authorization added: publish
- 2026-11-01T20:59:01Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2489 [FEATURE M, done, 3 steps] Model layer surfaces: MCP decide tool, fm doctor backend health, the site's Model layer… — lesson: README has a 2000-word visible budge…
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- T-2501 [FEATURE L, done, 4 steps] Generation cross-cutting review: after the Mission critiques, one cold reviewer on a… — lesson: a new genesis stage needs the shared te…
- decision 2026-11-01: [costly] [cites: user steer 2026-11-01: cross-cutting review, gap map redraw, lean substance, proof before presentation, sealed prediction and blind…
## Lessons
- a claims check needs an explicit way to say 'this is a rule, not a result' (an invisible marker), or every threshold in a mechanism description reads as an unproven number
## Plan gaps
- failed first: step 1 red tests: ProofBeforePresentation (extraction, sources, capability claims, sweep row)
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
- README.md
- site/pages.py
- CHANGELOG.md
- MASTER.md
- plugin/skills/genesis/SKILL.md
