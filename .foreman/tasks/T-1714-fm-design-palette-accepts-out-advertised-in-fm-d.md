---
id: T-1714
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmdesign.py, plugin/lib/fmcli.py, plugin/tests/test_design_tokens.py, plugin/tests/test_docs.py, plugin/skills/ui-design/SKILL.md, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-23T01:27:51Z
updated: 2026-10-23T02:29:46Z
base: d7e6b5537792a4b2340f8d639c0ac789a1d3aaf4
base_tree: 46a9a0b16098842c92f4fda231f36bb8faf238b4
plan0_at: 2026-10-23T02:21:58Z
plan0_scope: [plugin/lib/fmdesign.py, plugin/lib/fmcli.py, plugin/tests/test_design_tokens.py, plugin/skills/ui-design/SKILL.md, CHANGELOG.md]
verified: strong
---
# fm design palette writes --out (it was advertised and ignored)
## Raw request
> fm design palette accepts --out (advertised in fm design --help) and silently ignores it: write the file or refuse the flag
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm design palette SEED --out FILE writes the export to FILE (refusing a symlink) and prints the proofs; without --out it prints as before — verify with `python3 plugin/tests/run.py test_design_tokens.Palette`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] write --out
## Resume here
<!-- auto -->
- 2026-10-23T02:23:22Z step 2/2: write --out
- git: foreman/build; 2 uncommitted: plugin/lib/fmdesign.py, plugin/tests/test_design_tokens.py
- touched since last checkpoint: plugin/tests/test_design_tokens.py, plugin/lib/fmdesign.py
## Docs impact
plugin/skills/ui-design/SKILL.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_design_tokens.Palette` → red as expected (exit 1) · Ran 13 tests in 2.5s (1 classes, 16 at a time; slowest: Palette 2s) / FAILED (1 classes) [ran] [tree f0bba5069a02] (2026-10-23T02:22:13Z)
- (step 2) `python3 plugin/tests/run.py test_design_tokens test_docs` → exit 0 · Ran 101 tests in 11.4s (18 classes, 16 at a time; slowest: Fences 11s, Extract 6s, TaskLifecycle 2s) / OK [ran] [tree 4de28ddbc604] (2026-10-23T02:27:13Z)
- (ac 1) `python3 plugin/tests/run.py test_design_tokens.Palette` → exit 0 · Ran 13 tests in 3.6s (1 classes, 16 at a time; slowest: Palette 3s) / OK [ran] [tree 4de28ddbc604] (2026-10-23T02:27:18Z)
- `python3 plugin/tests/run.py test_design_tokens.Palette` → ✗ exit 1 · Ran 13 tests in 4.7s (1 classes, 16 at a time; slowest: Palette 3s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 4de28ddbc604] (2026-10-23T02:27:27Z)
- `python3 plugin/tests/run.py test_design_tokens.Palette` → exit 0 · Ran 13 tests in 3.2s (1 classes, 16 at a time; slowest: Palette 3s) / OK [ran] [tree 4de28ddbc604] (2026-10-23T02:27:27Z)
- (ac 1) `python3 plugin/tests/run.py test_design_tokens.Palette` → exit 0 · Ran 13 tests in 5.9s (1 classes, 16 at a time; slowest: Palette 5s) / OK [ran] [tree 4de28ddbc604] (2026-10-23T02:27:48Z)
- (audit intent) `self-review: --out writes through fmcore.write_atomic after refusing a symlink (tested: nothing created at the link target), '-' prints, proofs still go to stderr, JSON unchanged; the ui-design skill and its doc test now name --out` → fm design palette --out FILE writes the export where it says [tree 4de28ddbc604] (2026-10-23T02:27:48Z)
- (audit edge) `self-review: --out writes through fmcore.write_atomic after refusing a symlink (tested: nothing created at the link target), '-' prints, proofs still go to stderr, JSON unchanged; the ui-design skill and its doc test now name --out` → a symlinked --out exits 2 with nothing written; --out - prints as before [tree 4de28ddbc604] (2026-10-23T02:27:48Z)
- (audit self) `self-review: --out writes through fmcore.write_atomic after refusing a symlink (tested: nothing created at the link target), '-' prints, proofs still go to stderr, JSON unchanged; the ui-design skill and its doc test now name --out` → no findings [tree 4de28ddbc604] (2026-10-23T02:27:48Z)
- (audit intent) `self-review: --out writes through fmcore.write_atomic after refusing a symlink (tested: nothing created at the link target), '-' prints, proofs still go to stderr, JSON unchanged; the ui-design skill and its doc test now name --out` → fm design palette --out FILE writes the export where it says [tree 4de28ddbc604] (2026-10-23T02:29:00Z)
- (audit adversary) `self-review: --out writes through fmcore.write_atomic after refusing a symlink (tested: nothing created at the link target), '-' prints, proofs still go to stderr, JSON unchanged; the ui-design skill and its doc test now name --out` → a planted symlink at --out is refused before any write (tested), and write_atomic's mkstemp temp file can't be redirected; the path is the user's own argument [tree 4de28ddbc604] (2026-10-23T02:29:00Z)
- (audit edge) `self-review: --out writes through fmcore.write_atomic after refusing a symlink (tested: nothing created at the link target), '-' prints, proofs still go to stderr, JSON unchanged; the ui-design skill and its doc test now name --out` → a symlinked --out exits 2 with nothing written; --out - prints as before [tree 4de28ddbc604] (2026-10-23T02:29:00Z)
- (audit self) `self-review: --out writes through fmcore.write_atomic after refusing a symlink (tested: nothing created at the link target), '-' prints, proofs still go to stderr, JSON unchanged; the ui-design skill and its doc test now name --out` → no findings [tree 4de28ddbc604] (2026-10-23T02:29:00Z)
## Log
- 2026-10-23T01:27:51Z created
- 2026-10-23T02:21:55Z planned from capture
- 2026-10-23T02:21:56Z set scope=['plugin/lib/fmdesign.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_design_tokens.py', 'plugin/skills/ui-design/SKILL.md', 'CHANGELOG.md']
- 2026-10-23T02:21:57Z focused
- 2026-10-23T02:23:23Z paused: focus moved to T-1637
- 2026-10-23T02:26:12Z focused
- 2026-10-23T02:27:01Z set scope=['plugin/lib/fmdesign.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_design_tokens.py', 'plugin/tests/test_docs.py', 'plugin/skills/ui-design/SKILL.md', 'CHANGELOG.md']
- 2026-10-23T02:27:38Z scope: test_docs.py pinned the old '>' redirect wording for the ui-design skill; now pins --out
- 2026-10-23T02:29:43Z done
- 2026-10-23T02:29:46Z committed 4306a430 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1507-review: Verdict: changes needed.** The maths is sound. The problems are in extract's file handling, its speed on hostile input, and how a Tokens-only DES…
- research T-1506-review: Verdict:** changes needed. I could only read the code, not run it, so every finding below is a code trace and none was executed. Four fixes shoul…
- T-1648 [FEATURE M, active, 3 steps] fm design roll: a seeded, coherent pick from the look cards, applied as one reversible patch
- decision 2026-10-22: [costly] Accepted the plugin supply baseline on 2026-10-22: code-review, context7, frontend-design, security-guidance, skill-creator (claude-plugins…
- likely tests for the scope: plugin/tests/test_cli.py
## Why not caught
no test ran palette with --out; T-1700's review spotted it from the code
## Lessons
- A flag the parser accepts must do something or be refused; a doc test pinned the workaround, so fix the test with the flag
## Files touched
- plugin/tests/test_design_tokens.py
- plugin/lib/fmdesign.py
- CHANGELOG.md
- plugin/lib/fmcli.py
- plugin/skills/ui-design/SKILL.md
- plugin/tests/test_docs.py
- MASTER.md
- plugin/lib/fmshot.py
- plugin/tests/test_fmshot.py
