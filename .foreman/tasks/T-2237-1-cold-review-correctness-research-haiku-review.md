---
id: T-2237
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T23:58:47Z
updated: 2026-10-31T00:40:52Z
base: 0bab91a7754fd2b3d886dd2db37708c0a5c0ad58
base_tree: 1f80a981fc1c9214569ff5ac1df4d9b037b17d73
plan0_at: 2026-10-31T00:18:41Z
plan0_scope: []
inferred_deps: [T-2185]
inferred_why: T-2185: fixes the ladder's cold-review correctness
paused_tree: 2b37311d39f7d5bf762d9f516ddb1da9a4ce485f
verified: strong
---
# #1 cold-review correctness (research/haiku-review-initiative.md): COLD re-finds (docs,…
## Raw request
> FIX: #1 cold-review correctness (research/haiku-review-initiative.md): COLD re-finds (docs, dep, secret) are labelled proven though they re-run the same finder, and dep reads the host interpreter; fm prove's deadline isn't checked inside _pick's two 300 s suite runs; fmfind's triple-quote tracking can flip on '"""' strings or # """ comments and hide later defs from the untested finder
## Interpretation
Three correctness defects from the cold Haiku review of #1, each grounded: (1) the dep finder maps import names to distributions through the host's installed packages (fmfind._dists, importlib.metadata), so its result depends on the machine, while fm prove's cold re-find calls it 'the tree itself holds it'; (2) fm prove checks its deadline only between candidates, and _pick can run two 300 s suites past it; (3) the Python triple-quote tracker in fmfind.Src flips on a '"""' inside a string or a # """ comment, hiding later defs from the untested finder.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm find's dep result doesn't change with the host's installed packages; prove never runs a suite past its deadline; a '"""' inside a string or comment doesn't hide later defs from the untested finder — verify with `cd plugin/tests && python3 -m unittest -q test_find.FindReview`
## Non-goals
## Approach (options → choice → why)
(1) Options: a static import→distribution table (PY_ALIAS grown) with no host lookup; keep the host lookup but mark such dep findings unprovable; resolve against the tree's lockfile. Choice: drop _dists() and grow PY_ALIAS with the common mismatches (yaml→pyyaml, dateutil→python-dateutil, google.protobuf→protobuf, …) so fm find gives the same answer on every machine; the cold re-find's evidence then holds, and its wording says it's a re-find by the same check, not an outside proof. (2) pass the remaining budget into _pick so each suite's timeout is min(300, left), and stop when it runs out. (3) for .py files, take string spans from tokenize (stdlib, parses without running anything) instead of counting quote marks; a tokenize error falls back to today's tracker.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests (class FindReview in test_find): dep with a mocked empty and full host metadata gives the same findings; a suite that would pass the deadline is cut at it; a quote mark in a string or comment leaves the later def visible
2. [x] drop _dists, grow PY_ALIAS; reword the cold re-find's evidence
3. [x] remaining budget into _pick; tokenize string spans with the tracker as fallback
4. [x] docs, adversary + edge review
## Resume here
<!-- auto -->
- 2026-10-31T00:30:53Z step 4/4: docs, adversary + edge review
- git: foreman/build; 2 uncommitted: CHANGELOG.md, MASTER.md
- touched since last checkpoint: .claude/worktrees/agent-a51556a8cb86a00a4/plugin/tests/test_find.py, .claude/worktrees/agent-a51556a8cb86a00a4/plugin/lib/fmfind.py, .claude/worktrees/agent-a51556a8cb86a00a4/plugin/lib/fmprove.py, CHANGELOG.md, MASTER.md
## Docs impact
MASTER.md fmfind and fmprove entries, CHANGELOG Unreleased
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest -q test_find.FindReview` → exit 0 · Ran 3 tests in 2.160s / OK [ran] [tree 3e627695dfa8] (2026-10-31T00:20:17Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_find && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [21.86s] [ran] [tree 3e627695dfa8] (2026-10-31T00:20:54Z)
- `cd plugin/tests && python3 -m unittest -q test_find.FindReview` → ✗ exit 1 · Ran 3 tests in 120.081s / FAILED (failures=3) (start tree + this task's tests) [ran] [tree 4551b489d993] (2026-10-31T00:29:26Z)
- `cd plugin/tests && python3 -m unittest -q test_find.FindReview` → exit 0 · Ran 3 tests in 1.083s / OK [ran] [tree 4551b489d993] (2026-10-31T00:29:26Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_find.FindReview` → exit 0 · Ran 3 tests in 1.076s / OK [ran] [tree 4551b489d993] (2026-10-31T00:30:14Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_find.FindReview` → exit 0 · Ran 3 tests in 1.076s / OK [ran] [tree 4551b489d993] (2026-10-31T00:30:15Z)
- (step 2) `cd plugin/tests && python3 -m unittest -q test_find.FindReview` → exit 0 · Ran 3 tests in 1.080s / OK [ran] [tree 4551b489d993] (2026-10-31T00:30:16Z)
- (step 3) `cd plugin/tests && python3 -m unittest -q test_find.FindReview` → exit 0 · Ran 3 tests in 1.078s / OK [ran] [tree 4551b489d993] (2026-10-31T00:30:18Z)
- (step 4) `grep -q 'T-2237' MASTER.md && grep -q 're-find by the same check' MASTER.md` → exit 0 · (no output) [ran] [tree 2b37311d39f7] (2026-10-31T00:31:15Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_find.FindReview` → exit 0 · Ran 3 tests in 1.076s / OK [ran] [tree 2b37311d39f7] (2026-10-31T00:31:16Z)
- (audit intent) `fm-reviewer adversary+edge on the builder's branch: 1 MEDIUM (multi-line f-strings unmarked under 3.12+ tokenize) and 3 LOW (a dep test that couldn't fail, deadline rounding and docstring, tokenize cost on minified lines) fixed test-first in e254f2f4; test_find + test_scout 65 green` → the three defects the cold review found are fixed, each red then green, and nothing else in fm find's output changed [tree 2b37311d39f7] (2026-10-31T00:31:16Z)
- (audit adversary) `fm-reviewer adversary+edge on the builder's branch: 1 MEDIUM (multi-line f-strings unmarked under 3.12+ tokenize) and 3 LOW (a dep test that couldn't fail, deadline rounding and docstring, tokenize cost on minified lines) fixed test-first in e254f2f4; test_find + test_scout 65 green` → f-string and t-string spans now mark data lines, so a planted multi-line f-string can't add fake defs or imports; tokenize only parses, with every error falling back [tree 2b37311d39f7] (2026-10-31T00:31:16Z)
- (audit edge) `fm-reviewer adversary+edge on the builder's branch: 1 MEDIUM (multi-line f-strings unmarked under 3.12+ tokenize) and 3 LOW (a dep test that couldn't fail, deadline rounding and docstring, tokenize cost on minified lines) fixed test-first in e254f2f4; test_find + test_scout 65 green` → the dep result is the same with an empty or full host mapping; the deadline cuts a sleeping suite; files with lines over 2000 characters skip tokenize [tree 2b37311d39f7] (2026-10-31T00:31:16Z)
## Log
- 2026-10-30T23:58:47Z created
- 2026-10-31T00:17:36Z planned: it has criteria and steps
- 2026-10-31T00:18:21Z set approved=True
- 2026-10-31T00:18:22Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2237.builder.md
- 2026-10-31T00:18:40Z focused
- 2026-10-31T00:27:19Z merged worktree-agent-a51556a8cb86a00a4 (3 file(s))
- 2026-10-31T00:27:19Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a51556a8cb86a00a4
- 2026-10-31T00:27:24Z focused
- 2026-10-31T00:30:53Z paused: focus moved to T-2163
- 2026-10-31T00:31:40Z done
- 2026-10-31T00:31:42Z committed 800af4e4 (2 files)
- 2026-10-31T00:33:04Z guard authorization added: publish
- 2026-10-31T00:40:52Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research haiku-review-initiative: Scope: fmfind.py, fmprove.py, fmscout.py, fmhooks._leads_note. Adversary + edge. Two claims spot-checked and confirmed (marked ✓); the …
- T-2234 [FEATURE M, dropped, 0 steps] fmprove.py:289-291 records --yes-run consent before argument validation; fmfind.py:74-79…
- T-2235 [SECURITY L, done, 4 steps] #1 cold-review fixes (research/haiku-review-initiative.md): fm find scans tracked… — lesson: A review by a smaller model of the same f…
- decision 2026-10-30: Proven kinds (dep, docs, secret) file without a cold re-run; scout never refiles a regression
- similar past tasks were L: consider --tier L
- the similar finished task took 4 steps
## Why not caught
Each finder was tested against renders Foreman writes itself, on one machine: no test varied the host's installed packages, put a quote mark in a string or comment above a def, or ran a suite slower than the deadline. A cold review by a different model (research/haiku-review-initiative.md) found them; a planted-case test per finder input class would have.
## Lessons
- Replacing a hand counter with the stdlib tokenizer needs the tokenizer's version differences: 3.12 split f-strings into their own tokens
## Files touched
- plugin/tests/test_find.py
- plugin/lib/fmfind.py
- plugin/lib/fmprove.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmgenesis.py
- plugin/tests/test_genesis.py
