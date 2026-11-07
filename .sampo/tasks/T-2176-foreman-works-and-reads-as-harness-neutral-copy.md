---
id: T-2176
type: FEATURE
tier: M
status: done
priority: urgent
scope: []
depends_on: []
source: user
created: 2026-10-30T15:32:02Z
updated: 2026-10-30T16:15:05Z
batch: [T-2173, T-2174]
base: 983813829d6ac17f4dea3e16cd1717318e6d4553
base_tree: a5a5d0b0c92d5044ebd9b29bf9b4a6465669bf23
plan0_at: 2026-10-30T15:49:03Z
plan0_scope: []
verified: strong
---
# Foreman works and reads as harness-neutral: copy says coding agents, and install/run work with no Claude Code
## Raw request
> T-2173: Foreman isn't Claude-Code-specific: README ('The discipline layer for Claude Code'), site (title 'Foreman for Claude Code', h1), plugin.json, MASTER and docs describe it as a harness-neutral discipline layer for coding agents (Claude Code, fm code, Codex, Gemini CLI, opencode), with CC as one surface (user 2026-10-30: 'foreman shouldn't be specific to CC, so change it')
> T-2174: Prove Foreman works outside Claude Code: an end-to-end test with no claude binary — fm code drives a task through brief, evidence and finish on a stub model; fm install for Codex/Gemini/opencode writes working wiring; the guard and drive work without CC hooks; fix whatever breaks (user 2026-10-30: 'make sure it does work outside of CC')
## Interpretation
Do T-2173, T-2174 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-2176. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-2173: Foreman isn't Claude-Code-specific: README ('The discipline layer for Claude Code'),… works — verify with `python3 plugin/tests/run.py test_site test_setup.InstallScript`
- [x] T-2174: Foreman works with no claude anywhere on PATH: fm init, task new, evidence --run and finish close a task, and fm code finishes on a stub model — verify with `python3 plugin/tests/run.py test_setup.NoClaude test_code`
- [x] install.sh with no claude on PATH exits 0, links fm onto PATH, wires each agent it finds (codex/gemini/opencode) with fm agents install, and skips the Claude Code plugin, settings and wiring steps — verify with `python3 plugin/tests/run.py test_setup.InstallScript`
- [x] README, the site's home page, MASTER §1 and the install requirements describe Foreman as a discipline layer for coding agents (Claude Code one surface among Codex, Gemini CLI, opencode and fm code), and no product line says it is for Claude Code — verify with `python3 plugin/tests/run.py test_site test_setup.InstallScript`
- [x] fm doctor with no claude on PATH has no Claude Code failures or wiring nags, a task closes through fm task finish, and a dangling fm link of Foreman's is repaired by the installer — verify with `python3 plugin/tests/run.py test_setup.NoClaude test_setup.InstallScript test_doctor`
## Non-goals
Moving FOREMAN_HOME's default off ~/.claude (BUILD_PROMPT, hooks and existing installs assume it; FOREMAN_HOME overrides); live runs of Codex, Gemini CLI or opencode (none is installed here, and the adapters' own note already says they're built to documented formats and need a live check).
## Approach (options → choice → why)
Complete version: the installer works with no Claude Code (fm on PATH, other agents wired, fm code pointed at); every product line (README headline, site title/h1/lede/meta, MASTER §1, requirements, fine print) names coding agents with CC as one surface; a test proves a task closes with no claude anywhere on PATH. Options: (a) copy-only rewording — rejected, the installer still dies without claude, so the copy would lie; (b) a separate install-agents.sh for non-CC users — rejected, two installers drift and the one-line curl stays CC-only; (c) make claude optional inside install.sh, skip the CC-only steps, link fm and run fm agents install for each agent found — chosen: one installer, smallest diff, reuses fm agents install; (d) move FOREMAN_HOME's default off ~/.claude — rejected for now: BUILD_PROMPT, hooks and every existing install assume it, FOREMAN_HOME already overrides it (captured if it matters).
## Risks and rollback
install.sh runs on strangers' machines: the no-claude path must not touch ~/.claude settings; existing CC installs must take the identical path (InstallScript's tests stay green). Rollback: git revert of the commit.
## Execution prompt
## Steps
1. [x] T-2173: Foreman isn't Claude-Code-specific: README ('The discipline layer for Claude Code'),…
2. [x] T-2174: Prove Foreman works outside Claude Code: an end-to-end test with no claude binary — fm…
3. [x] red tests: install.sh with a PATH that has no claude (and one with a codex stub); a copy test that the home page and README headline aren't Claude-Code-only
4. [x] install.sh: claude optional; without it skip steps 2-5, link fm into ~/.local/bin, fm agents install each found agent, point at fm code when none
5. [x] copy: README headline/Why/requirements/'Beyond Claude Code', site index title/meta/h1/lede/req/fine print, MASTER §1, CHANGELOG; rebuild the site
## Resume here
## Docs impact
README headline/Why/requirements/section heading; site home and fine print; INSTALL.md; MASTER §1 and fmdoctor row; marketplace.json; CHANGELOG
## Verification evidence
- (step 3) `python3 plugin/tests/run.py test_setup.InstallScript test_setup.NoClaude` → exit 0 · Ran 15 tests in 2.2s (2 classes, 16 at a time; slowest: NoClaude 2s, InstallScript 1s) / OK [ran] [tree 9ada7fa6bb9b] (2026-10-30T15:53:52Z)
- (step 4) `python3 plugin/tests/run.py test_setup.InstallScript` → exit 0 · Ran 13 tests in 1.5s (1 classes, 16 at a time; slowest: InstallScript 1s) / OK [ran] [tree 9ada7fa6bb9b] (2026-10-30T15:53:54Z)
- (step 5) `python3 plugin/tests/run.py test_site_build.ProductLines` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: ProductLines 0s) / OK [ran] [tree 74b2652b4bb5] (2026-10-30T15:54:36Z)
- (step 1) `python3 plugin/tests/run.py test_site_build.ProductLines` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: ProductLines 0s) / OK [ran] [tree 74b2652b4bb5] (2026-10-30T15:55:57Z)
- (step 2) `python3 plugin/tests/run.py test_setup.NoClaude test_setup.InstallScript` → exit 0 · Ran 15 tests in 1.3s (2 classes, 16 at a time; slowest: NoClaude 1s, InstallScript 1s) / OK [ran] [tree 74b2652b4bb5] (2026-10-30T15:55:58Z)
- (ac 1) `python3 plugin/tests/run.py test_site_build.ProductLines test_setup.InstallScript test_setup.NoClaude` → exit 0 · Ran 16 tests in 1.3s (3 classes, 16 at a time; slowest: NoClaude 1s, InstallScript 1s, ProductLines 0s) / OK [ran] [tree 74b2652b4bb5] (2026-10-30T15:56:00Z)
- (ac 2) `python3 plugin/tests/run.py test_site_build.ProductLines test_setup.InstallScript test_setup.NoClaude` → exit 0 · Ran 16 tests in 1.3s (3 classes, 16 at a time; slowest: NoClaude 1s, InstallScript 1s, ProductLines 0s) / OK [ran] [tree 74b2652b4bb5] (2026-10-30T15:56:01Z)
- (ac 3) `python3 plugin/tests/run.py test_site_build.ProductLines test_setup.InstallScript test_setup.NoClaude` → exit 0 · Ran 16 tests in 1.3s (3 classes, 16 at a time; slowest: NoClaude 1s, InstallScript 1s, ProductLines 0s) / OK [ran] [tree 74b2652b4bb5] (2026-10-30T15:56:03Z)
- (ac 4) `python3 plugin/tests/run.py test_site_build.ProductLines test_setup.InstallScript test_setup.NoClaude` → exit 0 · Ran 16 tests in 1.3s (3 classes, 16 at a time; slowest: NoClaude 1s, InstallScript 1s, ProductLines 0s) / OK [ran] [tree 74b2652b4bb5] (2026-10-30T15:56:04Z)
- (ac 2) `python3 plugin/tests/run.py test_setup.NoClaude test_code` → exit 0 · Ran 448 tests in 62.9s (95 classes, 16 at a time; slowest: Worker 63s, Fakes 40s, Bench 17s) / OK [ran] [tree 74b2652b4bb5] (2026-10-30T15:57:12Z)
- (step 5) `fm shot /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/site/index.html --out /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/shots --reduced-motion` → exit 0 · frame-00.png … frame-04.png (5 frames 250 ms apart, real time) / no poster: the page held still [ran] [tree 74b2652b4bb5] (2026-10-30T15:58:11Z)
- (ac 1) `python3 plugin/tests/run.py test_site_build.ProductLines test_setup.InstallScript test_setup.NoClaude` → exit 0 · Ran 18 tests in 1.6s (3 classes, 16 at a time; slowest: NoClaude 1s, InstallScript 1s, ProductLines 0s) / OK [ran] [tree 920ad3284acf] (2026-10-30T16:02:26Z)
- (ac 3) `python3 plugin/tests/run.py test_site_build.ProductLines test_setup.InstallScript test_setup.NoClaude` → exit 0 · Ran 18 tests in 1.6s (3 classes, 16 at a time; slowest: NoClaude 1s, InstallScript 1s, ProductLines 0s) / OK [ran] [tree 920ad3284acf] (2026-10-30T16:02:28Z)
- (ac 4) `python3 plugin/tests/run.py test_site_build.ProductLines test_setup.InstallScript test_setup.NoClaude` → exit 0 · Ran 18 tests in 1.6s (3 classes, 16 at a time; slowest: NoClaude 1s, InstallScript 1s, ProductLines 0s) / OK [ran] [tree 920ad3284acf] (2026-10-30T16:02:29Z)
- (ac 5) `python3 plugin/tests/run.py test_setup.NoClaude test_setup.InstallScript test_doctor` → exit 0 · Ran 88 tests in 5.6s (27 classes, 16 at a time; slowest: ViewsRepair 5s, LockProbe 3s, NoClaude 2s) / OK [ran] [tree 920ad3284acf] (2026-10-30T16:02:35Z)
- (ac 2) `python3 plugin/tests/run.py test_setup.NoClaude test_code` → exit 0 · Ran 449 tests in 63.1s (95 classes, 16 at a time; slowest: Worker 63s, Fakes 40s, Bench 17s) / OK [ran] [tree 920ad3284acf] (2026-10-30T16:03:38Z)
- (step 1) `python3 plugin/tests/run.py test_site_build.ProductLines test_setup.InstallScript test_setup.NoClaude test_doctor` → exit 0 · Ran 89 tests in 5.6s (28 classes, 16 at a time; slowest: ViewsRepair 5s, LockProbe 3s, Command 2s) / OK [ran] [tree 920ad3284acf] (2026-10-30T16:03:47Z)
- (step 2) `python3 plugin/tests/run.py test_site_build.ProductLines test_setup.InstallScript test_setup.NoClaude test_doctor` → exit 0 · Ran 89 tests in 5.6s (28 classes, 16 at a time; slowest: ViewsRepair 5s, LockProbe 3s, NoClaude 2s) / OK [ran] [tree 920ad3284acf] (2026-10-30T16:03:53Z)
- (step 3) `python3 plugin/tests/run.py test_site_build.ProductLines test_setup.InstallScript test_setup.NoClaude test_doctor` → exit 0 · Ran 89 tests in 5.6s (28 classes, 16 at a time; slowest: ViewsRepair 5s, LockProbe 3s, NoClaude 2s) / OK [ran] [tree 920ad3284acf] (2026-10-30T16:03:58Z)
- (step 4) `python3 plugin/tests/run.py test_site_build.ProductLines test_setup.InstallScript test_setup.NoClaude test_doctor` → exit 0 · Ran 89 tests in 5.6s (28 classes, 16 at a time; slowest: ViewsRepair 5s, LockProbe 3s, NoClaude 2s) / OK [ran] [tree 920ad3284acf] (2026-10-30T16:04:04Z)
- (step 5) `python3 plugin/tests/run.py test_site_build.ProductLines test_setup.InstallScript test_setup.NoClaude test_doctor` → exit 0 · Ran 89 tests in 5.6s (28 classes, 16 at a time; slowest: ViewsRepair 5s, LockProbe 3s, NoClaude 2s) / OK [ran] [tree 920ad3284acf] (2026-10-30T16:04:10Z)
- (audit intent) `fm-reviewer` → met after fixes: install works with no claude (fm linked via ensure_fm_link, agents wired, CC steps skipped), doctor has no CC failures, a task closes through fm task finish, copy is harness-neutral across README/site/INSTALL/MASTER/marketplace; fm code's stub-model run is covered by test_code with only the exit-97 lockout as claude [tree 920ad3284acf] (2026-10-30T16:04:28Z)
- (audit edge) `fm-reviewer` → dangling fm link repaired, not fatal (tested); real agent CLIs and local model servers can't leak into the tests; --build without claude dies with why; ignored plugin flags are named [tree 920ad3284acf] (2026-10-30T16:04:28Z)
- (audit maintainer) `fm-reviewer` → installer reuses fmsetup.ensure_fm_link instead of a second link rule; ProductLines above the main guard; NO_CC one constant for the four doctor checks [tree 920ad3284acf] (2026-10-30T16:04:28Z)
- (audit adversary) `fm-reviewer` → no new untrusted input; quoting intact; the link is only made under $HOME and never over someone else's fm [tree 920ad3284acf] (2026-10-30T16:04:28Z)
- (audit design) `fm-reviewer + fm shot` → home page at 1280: new h1 and lede wrap cleanly, fm code chip added; site tests pass [tree 920ad3284acf] (2026-10-30T16:04:29Z)
- (ac 1) `python3 plugin/tests/run.py test_site test_setup.InstallScript` → exit 0 · Ran 41 tests in 4.7s (12 classes, 16 at a time; slowest: Header 4s, Landing 2s, Session 1s) / OK [ran] [tree 920ad3284acf] (2026-10-30T16:06:00Z)
- (ac 2) `python3 plugin/tests/run.py test_setup.NoClaude test_code` → exit 0 · Ran 449 tests in 63.6s (95 classes, 16 at a time; slowest: Worker 63s, Fakes 40s, Bench 17s) / OK [ran] [tree 920ad3284acf] (2026-10-30T16:06:00Z)
- (ac 3) `python3 plugin/tests/run.py test_setup.InstallScript` → exit 0 · Ran 14 tests in 1.0s (1 classes, 16 at a time; slowest: InstallScript 1s) / OK [ran] [tree 920ad3284acf] (2026-10-30T16:06:00Z)
- (ac 4) `python3 plugin/tests/run.py test_site test_setup.InstallScript` → exit 0 · Ran 41 tests in 4.7s (12 classes, 16 at a time; slowest: Header 4s, Landing 2s, Session 1s) / OK [ran] [tree 920ad3284acf] (2026-10-30T16:06:00Z)
- (ac 5) `python3 plugin/tests/run.py test_setup.NoClaude test_setup.InstallScript test_doctor` → exit 0 · Ran 88 tests in 5.6s (27 classes, 16 at a time; slowest: ViewsRepair 5s, LockProbe 3s, NoClaude 2s) / OK [ran] [tree 920ad3284acf] (2026-10-30T16:06:00Z)
- (audit intent) `one fm-reviewer pass (6 lenses) plus a doctor run with no claude on PATH; 7 findings fixed test-first` → installs and runs with no Claude Code (fm linked, Codex/Gemini/opencode wired, CC steps skipped), doctor clean of CC-only failures, task closes via fm task finish; product copy says coding agents [tree 920ad3284acf] (2026-10-30T16:06:00Z)
- (audit edge) `one fm-reviewer pass (6 lenses) plus a doctor run with no claude on PATH; 7 findings fixed test-first` → dangling fm link repaired; tests hermetic against real agent CLIs and local model servers; --build without claude explains [tree 920ad3284acf] (2026-10-30T16:06:00Z)
- (step 5) `python3 plugin/tests/run.py test_docs test_site_build.ProductLines` → exit 0 · Ran 81 tests in 8.3s (22 classes, 16 at a time; slowest: Fences 8s, TaskLifecycle 1s, Site 1s) / OK [ran] [tree a4a4de22e8dc] (2026-10-30T16:09:09Z)
- (audit maintainer) `self` → after the README split (ReadmeShape's 300-char rule): installer reuses ensure_fm_link, ProductLines above the main guard, NO_CC one constant; test_docs green [tree a4a4de22e8dc] (2026-10-30T16:09:09Z)
- (audit intent) `self` → unchanged by the README split: copy says coding agents, installs and runs with no Claude Code, doctor clean of CC-only failures [tree a4a4de22e8dc] (2026-10-30T16:09:09Z)
- (audit intent) `one fm-reviewer pass (6 lenses) plus a doctor run with no claude on PATH; 7 findings fixed test-first; README paragraph split for ReadmeShape` → installs and runs with no Claude Code (fm linked, Codex/Gemini/opencode wired, CC steps skipped), doctor clean of CC-only failures, task closes via fm task finish; product copy says coding agents [tree a4a4de22e8dc] (2026-10-30T16:09:38Z)
- (audit edge) `one fm-reviewer pass (6 lenses) plus a doctor run with no claude on PATH; 7 findings fixed test-first; README paragraph split for ReadmeShape` → dangling fm link repaired; tests hermetic against real agent CLIs and local model servers; --build without claude explains [tree a4a4de22e8dc] (2026-10-30T16:09:38Z)
- (audit adversary) `one fm-reviewer pass (6 lenses) plus a doctor run with no claude on PATH; 7 findings fixed test-first; README paragraph split for ReadmeShape` → install.sh takes no new untrusted input; every expansion quoted; the fm link goes only under $HOME through ensure_fm_link, which never replaces anyone else's fm or a working link; agent names come from a fixed list, not PATH contents; the README split changed no code [tree a4a4de22e8dc] (2026-10-30T16:09:38Z)
## Log
- 2026-10-30T15:32:02Z created
- 2026-10-30T15:34:31Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_site test_setup.InstallScript`
- 2026-10-30T15:34:32Z criterion 2 verify: `` → `python3 plugin/tests/run.py test_setup.NoClaude test_code`
- 2026-10-30T15:34:32Z criterion 2 text: T-2174: Prove Foreman works outside Claude Code: an end-to-end test with no claude binary — fm… works → T-2174: Foreman works with no claude anywhere on PATH: fm init, task new, evidence --run and finish close a task, and fm code finishes on a stub model
- 2026-10-30T15:35:06Z more product lines: site/genesis/index.html:106 and site/build.py:329 fine print, .claude-plugin/marketplace.json description, fmevolve.SYSTEM's 'discipline layer for Claude Code'; ECC playbook quotes stay (sourced text)
- 2026-10-30T15:47:06Z set priority=urgent
- 2026-10-30T15:49:03Z focused
- 2026-10-30T15:53:49Z red seen: before the install.sh change all 3 no-claude install tests failed with "foreman: 'claude' is required but not on PATH"
- 2026-10-30T16:02:21Z review fixes: installer uses fmsetup.ensure_fm_link (dangling link repaired, PATH hint), closing line and flags note depend on claude; tests drop real agent CLIs from the PATH and skip fm code's no-model case when a local model server answers; NoClaude closes via fm task finish; ProductLines moved above the main guard; site copy says 'your agent'; INSTALL.md steps 2 and 5; doctor's CC-only checks pass with NO_CC (found running doctor without claude). AC2's 'finishes on a stub model' is covered by test_code passing with only the exit-97 lockout as claude
- 2026-10-30T16:04:34Z scope: install.sh, INSTALL.md, README, site copy, MASTER, CHANGELOG, marketplace.json, fmdoctor's CC-only checks and their tests; all part of 'not CC-specific and works outside CC'
- 2026-10-30T16:11:06Z done
- 2026-10-30T16:11:08Z committed f50cd7a6 (12 files)
- 2026-10-30T16:12:33Z guard authorization added: publish
- 2026-10-30T16:15:05Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1866 [FEATURE M, done, 7 steps] Backlog swipe everywhere: app view, terminal loop, pick explores, prefer --reset — lesson: A loop that applies one verdict at a time mu…
- T-1760 [FEATURE M, done, 3 steps] fm code diagnostics: fm code why explains a run, piped stdin is the request's context, and the start event and the app … — lesson: Read…
- T-1905 [FIX M, done, 5 steps] CLI parsing: --section forms, a lone-word step, a capture's leading tag — lesson: When a parser accepts a shorthand, test the typo next to …
- decision 2026-10-30: [cites: user steer 2026-10-29: COVERAGE BY GRID, NOT BY LUCK] Genesis standing rule: coverage by grid — coverage.md (fm genesis put): rows = the 13 …
## Lessons
- Test 'works without X' by removing X from PATH entirely (a symlink farm of every tool but X), not by stubbing it; then run doctor too, since health checks are where hidden dependencies on X hide
## Files touched
- plugin/tests/test_setup.py
- install.sh
- plugin/tests/test_site_build.py
- .claude-plugin/marketplace.json
- INSTALL.md
- MASTER.md
- README.md
- site/build.py
- site/genesis/index.html
- site/index.html
- CHANGELOG.md
- plugin/lib/fmdoctor.py
