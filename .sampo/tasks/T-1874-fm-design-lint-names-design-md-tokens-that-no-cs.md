---
id: T-1874
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-28T23:04:55Z
updated: 2026-10-29T01:04:49Z
base: ac71d5a14bf95f9fdeb19f43df53e60553ffcd75
base_tree: d1cf3f5d17df9f09770b598c5556886bf5bd7fbf
plan0_at: 2026-10-29T00:56:35Z
plan0_scope: []
verified: strong
---
# Fm design lint names DESIGN.md tokens that no CSS in the project uses
## Raw request
> FEATURE: fm design lint names DESIGN.md tokens that no CSS in the project uses
> CONTEXT: forever loop round 5 ("Unused-token report for DESIGN.md"); report only, never delete.
## Interpretation
fm design lint also reads the project's DESIGN.md ## Tokens (the git root's, or docs/DESIGN.md) and names every token that none of the files it linted uses, one line, report only: it never deletes, and the lint's exit code is unchanged.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm design lint names DESIGN.md tokens no linted file uses, report only, exit unchanged — verify with `python3 plugin/tests/run.py test_design_lint`
## Non-goals
Deleting tokens; a gate or exit code for unused tokens; reading JS theme objects.
## Approach (options → choice → why)
unused_tokens(tokens, texts): a token is used when a linted file mentions --name anywhere but its own definition (var(--name), getPropertyValue('--name')), or, for a Tailwind theme name --{color,font,text,spacing,radius,shadow,…}-X, a class word ending -X. cmd_design's lint branch reads DESIGN.md via _default_out() when it exists and read_design accepts it; prints 'DESIGN.md: N token(s) unused in the M file(s) linted: --a, --b' and adds unused_tokens to the JSON. No DESIGN.md or no Tokens section: nothing said.
## Risks and rollback
False 'unused' when tokens are used only from a file the lint doesn't read (JS, a template): the line says it counts only the files linted. Rollback: git revert.
## Execution prompt
## Steps
1. [x] Tests first in test_design_lint.py, red
2. [x] unused_tokens and the lint line; green
3. [x] Docs: CHANGELOG, MASTER; test_docs
## Resume here
<!-- auto -->
- 2026-10-29T01:02:59Z steps 3/3 done
- git: foreman/build; 6 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmdesign.py, plugin/skills/ui-design/SKILL.md, plugin/tests/test_design_lint.py
- touched since last checkpoint: plugin/lib/fmcli.py, CHANGELOG.md, MASTER.md, plugin/skills/ui-design/SKILL.md, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/e1874r.txt, plugin/lib/fmdesign.py, plugin/tests/test_design_lint.py, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/e1886t.txt, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/e1886i.txt, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/e1886d.txt, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/e1887t.txt, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/e1887i.txt
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_design_lint.UnusedTokens` → red as expected (exit 1) · Ran 2 tests in 0.7s (1 classes, 16 at a time; slowest: UnusedTokens 0s) / FAILED (1 classes) [ran] [tree 4d297f1605ed] (2026-10-29T00:56:42Z)
- (step 2) `python3 plugin/tests/run.py test_design_lint` → exit 0 · Ran 33 tests in 1.9s (6 classes, 16 at a time; slowest: Allow 1s, Rules 1s, UnusedTokens 1s) / OK [ran] [tree aa73b57ea1e7] (2026-10-29T00:56:51Z)
- (step 3) `grep -c T-1874 CHANGELOG.md MASTER.md` → exit 0 · CHANGELOG.md:1 / MASTER.md:1 [ran] [tree 62ef8f16d38c] (2026-10-29T00:56:56Z)
- `python3 plugin/tests/run.py test_design_lint.UnusedTokens` → ✗ exit 1 · Ran 2 tests in 2.0s (1 classes, 16 at a time; slowest: UnusedTokens 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 62ef8f16d38c] (2026-10-29T00:57:00Z)
- `python3 plugin/tests/run.py test_design_lint.UnusedTokens` → exit 0 · Ran 2 tests in 1.4s (1 classes, 16 at a time; slowest: UnusedTokens 1s) / OK [ran] [tree 62ef8f16d38c] (2026-10-29T00:57:00Z)
- (step 2) `python3 plugin/tests/run.py test_design_lint test_design` → exit 0 · Ran 120 tests in 4.0s (24 classes, 16 at a time; slowest: Extract 4s, Tokens 3s, Xray 3s) / OK [ran] [tree 6c86fb3ee6bf] (2026-10-29T00:59:46Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcli.py, plugin/lib/fmdesign.py — commit it through a task, or git checkout it back / fm doctor: OK (49 pass, 5 warn; python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                42.3    50.2     150  [0] / SessionEnd                  36.6    41.7     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under [ran] [tree 6c86fb3ee6bf] (2026-10-29T01:04:13Z)
- (ac 1) `python3 plugin/tests/run.py test_design_lint` → exit 0 · Ran 33 tests in 0.9s (6 classes, 16 at a time; slowest: UnusedTokens 1s, Allow 1s, Rules 1s) / OK [ran] [tree 6c86fb3ee6bf] (2026-10-29T01:04:23Z)
- (audit intent) `one fm-reviewer pass: 2 MEDIUM (tailwind config uses, bad --tokens validated first) and 3 LOW (max-md:, root from linted path, single findall) all fixed test-first` → lint names DESIGN.md tokens no linted CSS/class/config uses; exit code unchanged (advice only) [tree 6c86fb3ee6bf] (2026-10-29T01:04:23Z)
- (audit adversary) `one fm-reviewer pass: 2 MEDIUM (tailwind config uses, bad --tokens validated first) and 3 LOW (max-md:, root from linted path, single findall) all fixed test-first` → none — reads local files only, names are printed through the existing finding path [tree 6c86fb3ee6bf] (2026-10-29T01:04:23Z)
- (audit edge) `one fm-reviewer pass: 2 MEDIUM (tailwind config uses, bad --tokens validated first) and 3 LOW (max-md:, root from linted path, single findall) all fixed test-first` → bad --tokens errors before linting; max-md:/md: breakpoints and tailwind.config hsl(var(--x)) count as uses; no DESIGN.md → silent [tree 6c86fb3ee6bf] (2026-10-29T01:04:23Z)
## Log
- 2026-10-28T23:04:55Z created
- 2026-10-29T00:53:50Z set status=planned
- 2026-10-29T00:56:34Z focused
- 2026-10-29T01:04:48Z done
- 2026-10-29T01:04:49Z committed 53c50108 (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1873 [FEATURE M, done, 3 steps] Fm scene gallery: every built-in scene on one contact sheet, each with a one-line caption — lesson: A playbook has a token ceiling (tes…
- research T-1506-review: Verdict:** changes needed. I could only read the code, not run it, so every finding below is a code trace and none was executed. Four fixes shoul…
- T-1397 [FEATURE M, done, 1 steps] Intake offer: fm code prints one line when an indexed skill matches the request (name, lic — lesson: Stack cards name tools (cargo) mor…
- decision 2026-10-23: Cause: hooks handed Claude the exact fm command each turn, so it never loaded the skill describing the step; descriptions used Foreman jargon or use…
## Lessons
- an unused-token check must count every place a token can be consumed (config files, variant prefixes), or it cries wolf
## Files touched
- plugin/tests/test_design_lint.py
- plugin/lib/fmcli.py
- plugin/lib/fmdesign.py
- CHANGELOG.md
- MASTER.md
- plugin/skills/ui-design/SKILL.md
