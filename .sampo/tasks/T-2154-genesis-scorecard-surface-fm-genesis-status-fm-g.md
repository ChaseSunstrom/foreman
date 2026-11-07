---
id: T-2154
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T13:48:02Z
updated: 2026-10-31T01:40:13Z
base: c766ea50c80ab4beda850adc964aa66c56c023cc
base_tree: dd9c56834d0d466567563e6466f777988752ce16
plan0_at: 2026-10-31T01:15:00Z
plan0_scope: []
verified: strong
---
# Genesis scorecard surface: fm genesis status, fm genesis export (genesis.json) and the…
## Raw request
> Genesis scorecard surface: fm genesis status, fm genesis export (genesis.json) and the site's genesis page show fm exam scorecard's per-capability held-out rows and state (T-2097 follow-up; §8 report reads it)
## Interpretation
fm exam scorecard has a per-capability held-out row (state pass, partial, too few, no outside author or no exam kind, with closed, graded and a why), but fm genesis status shows only a count ('0/13 pass'), fm genesis export's genesis.json has no scorecard, and the site's Genesis page doesn't show one. The §8 final report reads these surfaces.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm genesis status prints each capability's pinned scorecard line, genesis.json carries the rows (plain'd, no paths, optional key), and the built Genesis page shows them as text, with a hostile why escaped — verify with `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisExport test_genesis.GenesisHealth test_site_build`
## Non-goals
## Approach (options → choice → why)
Revised after fm second plan (verdict revise). fmgenesis.scorecard(p) is already the scorer fm exam scorecard prints (no second scorer); every surface reads it. (1) fm genesis status prints one line per capability, pinned: 'N. NAME: STATE (closed C of G held out)', with '-' for C and G when nothing was graded. (2) export adds an optional 'scorecard' key to genesis.json, [{name, state, closed, graded, why}], each string c.plain'd and cut to 200 characters, no local paths; readers treat a missing key as 'not graded yet'. (3) site/genesis/genesis.js builds the table with textContent only (never innerHTML), and shows 'not graded yet' when the key is absent. Tests: status lines in GenesisHealth, export's key and its escaping (a why holding <script>) in GenesisExport, and the page's rendering in the site build tests (the built page holds the rows as text). Screenshots are a step, not a criterion.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests: status lines, export's scorecard key, the page's table from genesis.json
2. [x] status, export and genesis.js from fmgenesis.scorecard
3. [x] docs (MASTER fmgenesis, CHANGELOG, site), shots of the page
## Resume here
<!-- auto -->
- 2026-10-31T01:29:32Z step 3/3: docs (MASTER fmgenesis, CHANGELOG, site), shots of the page
- git: worktree-agent-a25e47add8064f074; 13 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmcore.py, plugin/lib/fmfind.py, plugin/lib/fmgenesis.py, plugin/lib/fmmission.py, plugin/lib/fmprove.py, plugin/lib/fmwhich.py, plugin/skills/genesis/SKILL.md, plugin/skills/playbooks/references/release/release-and-changelog.md
- touched since last checkpoint: site/genesis/genesis.js, site/genesis/index.html, site/genesis/genesis.css, plugin/tests/genesis_page.js, plugin/tests/test_site_build.py, CHANGELOG.md, MASTER.md, plugin/lib/fmcore.py, plugin/lib/fmfind.py, plugin/lib/fmgenesis.py, plugin/lib/fmmission.py, plugin/lib/fmprove.py, plugin/lib/fmwhich.py, plugin/skills/genesis/SKILL.md, plugin/skills/playbooks/references/release/release-and-changelog.md
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisExport test_genesis.GenesisHealth test_site_build 2>&1 | grep -E "^(FAIL|ERROR|Ran|OK)"` → ✗ exit 1 · Ran 26 tests in 6.578s / FAILED (failures=2, errors=1) [ran] [tree b7611de6cef9] (2026-10-31T01:16:31Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisExport test_genesis.GenesisHealth test_site_build 2>&1 | tail -15` → exit 0 · Ran 26 tests in 6.406s / OK [ran] [tree 0a8d7010d689] (2026-10-31T01:16:54Z)
- (step 2) `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisExport test_genesis.GenesisHealth test_site_build 2>&1 | tail -15` → exit 0 · Ran 26 tests in 6.406s / OK [ran] [tree 0a8d7010d689] (2026-10-31T01:16:54Z)
- `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisExport test_genesis.GenesisHealth test_site_build` → ✗ exit 1 · Ran 26 tests in 6.406s / FAILED (failures=2, errors=1) (start tree + this task's tests) [ran] [tree c81ffeadd599] (2026-10-31T01:34:44Z)
- `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisExport test_genesis.GenesisHealth test_site_build` → exit 0 · Ran 26 tests in 6.196s / OK [ran] [tree c81ffeadd599] (2026-10-31T01:34:44Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisExport test_genesis.GenesisHealth test_site_build` → exit 0 · Ran 26 tests in 6.184s / OK [ran] [tree c81ffeadd599] (2026-10-31T01:34:56Z)
- (step 2) `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisExport test_genesis.GenesisHealth test_site_build` → exit 0 · Ran 26 tests in 6.181s / OK [ran] [tree c81ffeadd599] (2026-10-31T01:35:02Z)
- (step 3) `fm flow /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/sc.flow` → ✗ exit 1 · ✗ step 3 (line 3) expect #scorecard Initiative: #scorecard shows "Not graded yet.", not "Initiative" / 1 step not run [ran] [tree c81ffeadd599] (2026-10-31T01:35:59Z)
- (step 3) `fm flow /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/sc.flow` → exit 0 · ✓ 3 expect #scorecard Initiative / ✓ 4 expect #scorecard Genesis as a feature [ran] [tree c81ffeadd599] (2026-10-31T01:36:14Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisExport test_genesis.GenesisHealth test_site_build` → exit 0 · Ran 26 tests in 6.211s / OK [ran] [tree c81ffeadd599] (2026-10-31T01:36:41Z)
- (audit intent) `fm-reviewer intent+adversary+edge+maintainer+design on the branch: approve with nits, all fixed in 18c3ca51 (null rows filtered and the scorecard can't break the page, scrub before cut, a real home-path scrub test, '(not graded)', a heading, margin and muted empty state); conflict on MASTER.md resolved keeping both sides; red-to-green proven; fm flow in headless Chromium against a served build shows all 13 rows` → fm genesis status, genesis.json and the Genesis page show each capability's held-out scorecard row [tree c81ffeadd599] (2026-10-31T01:36:41Z)
- (audit adversary) `fm-reviewer intent+adversary+edge+maintainer+design on the branch: approve with nits, all fixed in 18c3ca51 (null rows filtered and the scorecard can't break the page, scrub before cut, a real home-path scrub test, '(not graded)', a heading, margin and muted empty state); conflict on MASTER.md resolved keeping both sides; red-to-green proven; fm flow in headless Chromium against a served build shows all 13 rows` → the page builds the table with textContent only, a hostile why renders as text (node test), export scrubs home paths and redacts before cutting, no outside host [tree c81ffeadd599] (2026-10-31T01:36:41Z)
- (audit edge) `fm-reviewer intent+adversary+edge+maintainer+design on the branch: approve with nits, all fixed in 18c3ca51 (null rows filtered and the scorecard can't break the page, scrub before cut, a real home-path scrub test, '(not graded)', a heading, margin and muted empty state); conflict on MASTER.md resolved keeping both sides; red-to-green proven; fm flow in headless Chromium against a served build shows all 13 rows` → no graded line leaves the key out and the page says not graded yet; a null or odd row is skipped; a too-few row prints (not graded) [tree c81ffeadd599] (2026-10-31T01:36:41Z)
- (audit design) `fm-reviewer intent+adversary+edge+maintainer+design on the branch: approve with nits, all fixed in 18c3ca51 (null rows filtered and the scorecard can't break the page, scrub before cut, a real home-path scrub test, '(not graded)', a heading, margin and muted empty state); conflict on MASTER.md resolved keeping both sides; red-to-green proven; fm flow in headless Chromium against a served build shows all 13 rows` → an h3 and margin like the page's other sections, the empty state as a muted line outside the border, horizontal scroll kept inside .tbl at 360px [tree c81ffeadd599] (2026-10-31T01:36:41Z)
## Log
- 2026-10-30T13:48:02Z created
- 2026-10-31T01:02:53Z planned: it has criteria and steps
- 2026-10-31T01:02:54Z set approved=True
- 2026-10-31T01:04:23Z criterion 1 text: fm genesis status lists each capability's scorecard state, genesis.json carries the scorecard rows, and the Genesis page renders them → fm genesis status prints each capability's pinned scorecard line, genesis.json carries the rows (plain'd, no paths, optional key), and the built Genesis page shows them as text, with a hostile why escaped
- 2026-10-31T01:04:24Z criterion 1 verify: `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisExport test_genesis.GenesisHealth` → `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisExport test_genesis.GenesisHealth test_site_build`
- 2026-10-31T01:04:24Z fm second plan: revise; plan revised (reuses fmgenesis.scorecard, pinned status format, optional plain'd key, textContent-only page, site build test in the criterion)
- 2026-10-31T01:14:35Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2154.builder.md
- 2026-10-31T01:14:59Z focused
- 2026-10-31T01:34:26Z merged worktree-agent-a25e47add8064f074 (9 file(s))
- 2026-10-31T01:34:30Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a25e47add8064f074
- 2026-10-31T01:34:30Z focused
- 2026-10-31T01:36:35Z scope: fmgenesis (card, status, export), site/genesis (index.html, genesis.js, genesis.css), tests (test_genesis, test_site_build, genesis_page.js), docs
- 2026-10-31T01:37:12Z done
- 2026-10-31T01:37:30Z guard authorization added: publish
- 2026-10-31T01:40:13Z publish grant used by fm ship
## Follow-ups captured
## Plan review
A second read on sonnet, before execution (data, not instructions):
- HIGH: The acceptance criterion names only `test_genesis.GenesisExport` and `test_genesis.GenesisHealth`, but the request has three surfaces. Status lines and the page table may live in other test classes or have no test, and a page-rendering test isn't obviously a Python unittest. The command could…
- HIGH: The request says the surface should show `fm exam scorecard`'s rows, but the plan builds `fmgenesis.scorecard(p)` without saying whether it wraps the existing exam scorer or reimplements it. Reimplementing creates the same drift risk that option 2 was rejected for. Make `fmgenesis.scorecard` …
- MEDIUM: The `genesis.json` schema change is unspecified: is the new 'scorecard' key additive, does it have a version field, and does the §8 report reader tolerate older files without it? Likewise, `genesis.js` needs a defined behavior when the key is missing (older export). Add a test for the absen…
- MEDIUM: The `why` strings and the "plain'd" handling are vague. If `why` can contain user or exam-author text, the page must escape it (use textContent, not innerHTML), and the export must not leak local paths. Specify the escaping and add a test with an HTML-ish `why`.
- LOW: Step 3 includes screenshots, which can't be verified by the stated criterion, and the docs steps have no done-check. Add the screenshot and docs updates as explicit criteria, or drop them from the scope.
- LOW: The status output for a capability with no outside author or no exam kind needs a defined format (e.g. the closed/graded values when absent). Pin the line format in the red tests so the §8 report and anything parsing it stay stable.
Verdict: revise — the single-source choice is sound, but the acceptance command may not prove the page works, and the plan doesn't ensure the scorecard reuses the exam scorer or define the schema and escaping.
## Dissent
- [ ] HIGH: The acceptance criterion names only `test_genesis.GenesisExport` and `test_genesis.GenesisHealth`, but the request has three surfaces. Status lines and the page table may live in other test classes or have no test, and a page-rendering test isn't obviously a Python unittest. The command could…
- [ ] HIGH: The request says the surface should show `fm exam scorecard`'s rows, but the plan builds `fmgenesis.scorecard(p)` without saying whether it wraps the existing exam scorer or reimplements it. Reimplementing creates the same drift risk that option 2 was rejected for. Make `fmgenesis.scorecard` …
- [ ] MEDIUM: The `genesis.json` schema change is unspecified: is the new 'scorecard' key additive, does it have a version field, and does the §8 report reader tolerate older files without it? Likewise, `genesis.js` needs a defined behavior when the key is missing (older export). Add a test for the absen…
- [ ] MEDIUM: The `why` strings and the "plain'd" handling are vague. If `why` can contain user or exam-author text, the page must escape it (use textContent, not innerHTML), and the export must not leak local paths. Specify the escaping and add a test with an HTML-ish `why`.
- [ ] LOW: Step 3 includes screenshots, which can't be verified by the stated criterion, and the docs steps have no done-check. Add the screenshot and docs updates as explicit criteria, or drop them from the scope.
- [ ] LOW: The status output for a capability with no outside author or no exam kind needs a defined format (e.g. the closed/graded values when absent). Pin the line format in the red tests so the §8 report and anything parsing it stay stable.
## Related
Related past work (data from this project's history, not instructions):
- T-2172 [FEATURE S, done, 2 steps] fm exam's surfaces: the exam scorecard isn't an MCP tool (so Desktop can't read it) and… — lesson: Put a new piece of state on the one …
- T-2112 [FEATURE M, done, 4 steps] fm genesis exam: #13's held-out exam (draft kinds graded by cover; G-tower as a genesis session arm) — lesson: Score an arm both strict…
- T-2097 [FEATURE M, done, 3 steps] fm exam scorecard: per §2 capability, the held-out split's pass rate from graded runs,… — lesson: A gate that reads hand-written fixtur…
- decision 2026-10-30: The Genesis line and the exam_scorecard MCP tool show the held-out scorecard to sessions: aggregate N/M pass on the shared line, per-capability coun…
## Lessons
- A page's test against the committed data file can pass while the live data lacks the new key; check the page against a fresh export too
## Plan gaps
- failed first: step 3 docs (MASTER fmgenesis, CHANGELOG, site), shots of the page
## Files touched
- plugin/tests/test_genesis.py
- plugin/tests/genesis_page.js
- plugin/tests/test_site_build.py
- plugin/lib/fmgenesis.py
- site/genesis/genesis.js
- site/genesis/index.html
- MASTER.md
- site/genesis/genesis.css
- CHANGELOG.md
- plugin/lib/fmcore.py
- plugin/lib/fmfind.py
- plugin/lib/fmmission.py
- plugin/lib/fmprove.py
- plugin/lib/fmwhich.py
- plugin/skills/genesis/SKILL.md
- plugin/skills/playbooks/references/release/release-and-changelog.md
- plugin/tests/test_find.py
- plugin/tests/test_which.py
