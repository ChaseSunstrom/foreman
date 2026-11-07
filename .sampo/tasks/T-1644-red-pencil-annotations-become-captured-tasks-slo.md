---
id: T-1644
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcritique.py, plugin/lib/fmcli.py, plugin/tests/test_critique.py, plugin/skills/ui-design/SKILL.md, MASTER.md, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T20:58:10Z
updated: 2026-10-28T20:24:18Z
group: design critique gates
base: 3e98fe17775acafe5dc33c67d653200d30063910
base_tree: 2cf379d318441377fbb354bb564a449f431fe91e
plan0_at: 2026-10-28T20:10:36Z
plan0_scope: []
verified: strong
---
# fm critique --bingo, --marks, --brief: slop bingo, red-pencil marks as tasks, brief-vs-built
## Raw request
> Red-pencil annotations become captured tasks; slop bingo; brief-vs-built check (from T-1533; waits: after fm critique; local vision models optional only)
## Interpretation
Three fm critique modes. --bingo: nine measurable tells of a templated look (generic font, violet accent, stock greys, one radius, same shadow, one gap, flat type scale, size sprawl, near-duplicate drift) on a 3x3 card; a full line exits 1. --marks: the user circles things in pencil red on a screenshot (or lists boxes in JSON); each mark becomes one captured FIX task naming the element under it (selector + text), scoped to the local file. --brief: the phrases the brief quotes must appear in the page's text. No vision model: pixel diff against a fresh shot and the census only.
## Assumptions (confidence)
## Acceptance criteria
- [x] --bingo scores nine template tells on a 3x3 card and exits 1 on a line, census or page — verify with `python3 plugin/tests/run.py test_critique`
- [x] --marks FILE.png|.json turns each red-pencil mark into one captured FIX task naming the element under it, deduped on rerun — verify with `python3 plugin/tests/run.py test_critique`
- [x] --brief [ID] looks for the brief's quoted phrases in the page text and exits 1 naming the missing ones — verify with `python3 plugin/tests/run.py test_critique`
- [x] bad input (marks file, mode mix, census with a page mode, brief without quotes) exits 2 before any browser — verify with `python3 plugin/tests/run.py test_critique`
## Non-goals
## Approach (options → choice → why)
Options: (a) a vision model reads marks: rejected, optional only and costly; (b) pixel diff of marked vs fresh shot at the same size, red-only, 16px cells joined 8-connected: chosen, deterministic and dependency-free; (c) JSON boxes only: kept as the second input. Bingo reuses the census keys and critique's near_total; brief reuses fmcore briefs and one innerText read. All three refuse bad input before a browser starts and share _open (frozen page).
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests first (red)
2. [x] fmcritique: bingo, marks, brief + cmd wiring + parser
3. [x] docs: ui-design skill, MASTER, CHANGELOG
## Resume here
<!-- auto -->
- 2026-10-28T20:17:16Z step 1/3: tests first (red)
- git: foreman/build; 6 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmcritique.py, plugin/skills/ui-design/SKILL.md, plugin/tests/test_critique.py
- touched since last checkpoint: /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/t1644-lib.py, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/t1644-edit.txt, plugin/lib/fmcli.py, plugin/lib/fmcritique.py, plugin/tests/test_critique.py, CHANGELOG.md, MASTER.md, plugin/skills/ui-design/SKILL.md
## Docs impact
ui-design skill, MASTER fmcritique bullet, CHANGELOG
## Verification evidence
- (audit intent) `fm-reviewer intent pass vs the brief's 4 ACs` → bingo, marks, brief and pre-browser refusals all shipped as asked [tree 168b2178479e] (2026-10-28T20:19:21Z)
- (audit adversary) `page/file text paths read` → all page text via plain_lines+defang+redact, backticks to ', file name now safe(); huge PNG refused from header [tree 168b2178479e] (2026-10-28T20:19:22Z)
- (audit edge) `caps, empty, mode mixes` → over-cap marks/phrases now noted not silent; [] and bad JSON exit 2; one mode at a time [tree 168b2178479e] (2026-10-28T20:19:22Z)
- (audit operator) `help and errors read` → --brief help names the page-first order; every refusal names its flag [tree 168b2178479e] (2026-10-28T20:19:22Z)
- (audit maintainer) `_open factored out of take, one lib section` → no duplication of the frozen-page setup [tree 168b2178479e] (2026-10-28T20:19:23Z)
- (step 1) `python3 plugin/tests/run.py test_critique` → exit 0 · Ran 27 tests in 7.1s (8 classes, 16 at a time; slowest: InABrowser 7s, Census 2s, Marks 1s) / OK [ran] [tree 168b2178479e] (2026-10-28T20:19:30Z)
- (step 2) `python3 plugin/tests/run.py test_critique` → exit 0 · Ran 27 tests in 7.1s (8 classes, 16 at a time; slowest: InABrowser 7s, Census 2s, Marks 1s) / OK [ran] [tree 168b2178479e] (2026-10-28T20:19:38Z)
- (step 3) `python3 plugin/tests/run.py test_critique` → exit 0 · Ran 27 tests in 7.1s (8 classes, 16 at a time; slowest: InABrowser 7s, Census 2s, Marks 1s) / OK [ran] [tree 168b2178479e] (2026-10-28T20:19:45Z)
- (ac 1) `python3 plugin/tests/run.py test_critique` → exit 0 · Ran 27 tests in 7.0s (8 classes, 16 at a time; slowest: InABrowser 7s, Census 2s, Marks 1s) / OK [ran] [tree 168b2178479e] (2026-10-28T20:23:50Z)
- (ac 2) `python3 plugin/tests/run.py test_critique` → exit 0 · Ran 27 tests in 7.0s (8 classes, 16 at a time; slowest: InABrowser 7s, Census 2s, Marks 1s) / OK [ran] [tree 168b2178479e] (2026-10-28T20:23:50Z)
- (ac 3) `python3 plugin/tests/run.py test_critique` → exit 0 · Ran 27 tests in 7.0s (8 classes, 16 at a time; slowest: InABrowser 7s, Census 2s, Marks 1s) / OK [ran] [tree 168b2178479e] (2026-10-28T20:23:50Z)
- (ac 4) `python3 plugin/tests/run.py test_critique` → exit 0 · Ran 27 tests in 7.0s (8 classes, 16 at a time; slowest: InABrowser 7s, Census 2s, Marks 1s) / OK [ran] [tree 168b2178479e] (2026-10-28T20:23:50Z)
- (audit edge) `one fm-reviewer pass (approve with nits); six nits fixed: cap notes, newline-kept element text, safe file name, header size check, --brief help order, page-bingo exit` → over-cap marks and phrases now noted; [] and bad JSON exit 2 before a browser [tree 168b2178479e] (2026-10-28T20:23:50Z)
## Log
- 2026-10-22T20:58:10Z created
- 2026-10-28T20:09:45Z planned from capture
- 2026-10-28T20:10:34Z set status=captured
- 2026-10-28T20:10:34Z planned from capture
- 2026-10-28T20:10:35Z focused
- 2026-10-28T20:10:42Z set scope=['plugin/lib/fmcritique.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_critique.py', 'plugin/skills/ui-design/SKILL.md', 'MASTER.md', 'CHANGELOG.md']
- 2026-10-28T20:14:14Z set scope=['plugin/lib/fmcritique.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_critique.py', 'plugin/skills/ui-design/SKILL.md', 'MASTER.md', 'CHANGELOG.md']
- 2026-10-28T20:24:16Z done
- 2026-10-28T20:24:18Z committed 17149151 (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1533 [FEATURE L, dropped, 4 steps] Round 3 (T-1520): Design critique tools: a computed-style census critique, 'why does this
- playbook Type and colour that read as chosen (fm playbooks show ui/type-and-colour)
- T-1642 [FEATURE M, done, 3 steps] fm critique: a computed-style census critiqued against DESIGN.md, and why-does-this-look-like-this for a selector — lesson: Strip by Un…
- decision 2026-10-22: T-1479 brainstorm: 548 ideas grounded into 26 capabilities; round 1 (19 tasks: UI design, motion and 3D playbooks and template, fm design lint, TUI …
- the similar finished task took 3 steps
## Lessons
- a cap that truncates must say what it dropped, and pair per-item notes after the cap, not before
## Files touched
- plugin/tests/test_critique.py
- plugin/lib/fmcli.py
- plugin/lib/fmcritique.py
- CHANGELOG.md
- MASTER.md
- plugin/skills/ui-design/SKILL.md
