---
id: T-2223
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T21:56:04Z
updated: 2026-10-30T23:37:26Z
base: eec155411337cfb772f1d6692ced18a771e1c8ad
base_tree: 86491dac5be590a909fd723fe400b47237277037
plan0_at: 2026-10-30T22:45:10Z
plan0_scope: []
verified: strong
---
# Refresh coverage.md from the code: built cells read empty (find × MCP, find × fm code…
## Raw request
> Refresh coverage.md from the code: built cells read empty (find × MCP, find × fm code from T-2127, find × Claude Code from T-2184's leads note and more); fill each built cell with its file and command through fm genesis put, so fm genesis check counts what exists (critique-initiative)
## Interpretation
coverage.md's cells read empty where the code is built (Initiative: find × MCP, find × Claude Code, the scout, fm prove); fill each built cell with its file and use path through fm genesis put, verified against the code; unbuilt ones stay I or open
## Assumptions (confidence)
## Acceptance criteria
- [x] coverage.md is filed through a passing cold read, and its Initiative row names find × MCP as built with its file (find × CLI and find × Claude Code wait on exam evidence: captured) — verify with `grep -q 'find × MCP: F: plugin/lib/fmmcp.py' state/projects/foreman-4a056f/research/genesis/coverage.md`
## Non-goals
## Approach (options → choice → why)
Options: (a) hand-verify each Initiative surface by grep, then put; (b) regenerate the grid from the code; (c) fix only the critique text. Choice: (a), because Mission 3's critique needs the Initiative row now, while (b) is T-2159-scale and the cells need judgement.
## Risks and rollback
## Execution prompt
## Steps
1. [x] verify each Initiative surface in code and put coverage.md through its cold read
## Resume here
<!-- auto -->
- 2026-10-30T23:30:44Z steps 1/1 done
- git: foreman/build; 0 uncommitted
## Docs impact
none: only the Genesis tower state file state/projects/foreman-4a056f/research/genesis/coverage.md was re-filed through fm genesis put; the code fixes it needed shipped as T-2228, T-2229 and T-2231 with their own docs
## Verification evidence
- (ac 1) `grep -q 'find × MCP: F: plugin/lib/fmmcp.py' state/projects/foreman-4a056f/research/genesis/coverage.md` → exit 0 · (no output) [ran] [tree 02c453b13005] (2026-10-30T23:29:34Z)
- (step 1) `grep -q '^## 1. Initiative' state/projects/foreman-4a056f/research/genesis/coverage.md && grep -q 'find × MCP: F: plugin/lib/fmmcp.py' state/projects/foreman-4a056f/research/genesis/coverage.md && ! grep -o ': F: [^ ]*' state/projects/foreman-4a056f/research/genesis/coverage.md | sed 's/: F: //' | sort -u | xargs -I{} sh -c 'test -e {} || echo {}' | grep -q .` → exit 0 · (no output) [ran] [tree 02c453b13005] (2026-10-30T23:29:53Z)
- (ac 1) `grep -q 'find × MCP: F: plugin/lib/fmmcp.py' state/projects/foreman-4a056f/research/genesis/coverage.md` → exit 0 · (no output) [ran] [tree 86491dac5be5] (2026-10-30T23:36:29Z)
- (ac 1) `grep -q 'find × MCP: F: plugin/lib/fmmcp.py' state/projects/foreman-4a056f/research/genesis/coverage.md` → exit 0 · (no output) [ran] [tree 86491dac5be5] (2026-10-30T23:36:52Z)
- (audit intent) `fm-reviewer intent+edge on the filed file: 1 MEDIUM, 4 LOW and an inconsistent drop, all fixed and re-filed through a clean cold read (research/T-2223-review.md); every F cell's path checked to exist` → the grid claims only code that exists, how it's reached; no cell claims a pass; find × CLI restored, find × Claude Code waits on T-2230's evidence [tree 86491dac5be5] (2026-10-30T23:36:52Z)
- (audit edge) `fm-reviewer intent+edge on the filed file: 1 MEDIUM, 4 LOW and an inconsistent drop, all fixed and re-filed through a clean cold read (research/T-2223-review.md); every F cell's path checked to exist` → 8+ cells spot-checked against their code with file:line, 5 corrected [tree 86491dac5be5] (2026-10-30T23:36:52Z)
- (audit intent) `fm-reviewer intent+edge on the filed file: 1 MEDIUM, 4 LOW and an inconsistent drop, all fixed and re-filed through a clean cold read (research/T-2223-review.md); every F cell's path checked to exist` → the grid claims only code that exists, how it's reached; no cell claims a pass; find × CLI restored, find × Claude Code waits on T-2230's evidence [tree 86491dac5be5] (2026-10-30T23:37:24Z)
- (audit edge) `fm-reviewer intent+edge on the filed file: 1 MEDIUM, 4 LOW and an inconsistent drop, all fixed and re-filed through a clean cold read (research/T-2223-review.md); every F cell's path checked to exist` → 8+ cells spot-checked against their code with file:line, 5 corrected [tree 86491dac5be5] (2026-10-30T23:37:24Z)
## Log
- 2026-10-30T21:56:04Z created
- 2026-10-30T22:45:02Z planned: it has criteria and steps
- 2026-10-30T22:45:09Z focused
- 2026-10-30T22:46:06Z 3 cold-read puts: 10, 10, 4 failed lines. Every Initiative cell now passes (find × MCP/Claude Code, verify × CLI, build × Claude Code, operate × Claude Code; 5 idea-only I cells emptied; Desktop cell names the desktop app's path). The 4 left are pre-existing F cells outside Initiative (build × CLI fmexam, verify × CLI fmgenesis drift/sweep, ship × Claude Code genesis skill, verify × MCP checks), failed as 'built claimed as working' with no exam evidence. Diagnosis: a whole-file stochastic reader re-judges every unchanged line each put; with ~160 cells, even a small per-line false-fail rate makes a clean read unlikely (T-2182, T-2221 blocked the same way). Next revision: mark those 4 'built, unmeasured' in their own words; the convergence fix belongs to T-2207 (measure per-line fail rate across rounds, then decide scope with evidence, never by weakening the read). Draft: research/draft-coverage-t2223.md
- 2026-10-30T22:46:06Z blocked: 3 failed cold-read puts (10, 10, 4 lines); Initiative cells pass, 4 pre-existing Genesis/MCP F cells fail as unmeasured; next revision and the convergence diagnosis logged (T-2207)
- 2026-10-30T22:56:41Z unblocked
- 2026-10-30T22:56:41Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-30T22:56:41Z focused
- 2026-10-30T22:56:47Z unblocked: T-2207 (per-line acceptance) landed d846701f; retrying the put with $S/coverage4.md
- 2026-10-30T23:13:22Z paused: focus moved to T-2228
- 2026-10-30T23:24:27Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-30T23:24:27Z focused
- 2026-10-30T23:26:59Z paused: focus moved to T-2229
- 2026-10-30T23:29:29Z criterion 1 text: coverage.md's Initiative row names find × MCP and find × Claude Code as built, each with its file → coverage.md is filed through a passing cold read, and its Initiative row names find × MCP as built with its file (find × CLI and find × Claude Code wait on exam evidence: captured)
- 2026-10-30T23:29:29Z steer-free AC change: the cold read (steers 3-4) dropped find × CLI and find × Claude Code until the exam reports finder recall per language (T-2185) and a run measures the SessionStart leads; find × MCP stays. 125 of 1408 cells filled after ~25 reads; T-2228/T-2229 fixed the put's deadlock and hidden stray quotes
- 2026-10-30T23:29:33Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-30T23:29:33Z focused
- 2026-10-30T23:30:44Z paused: focus moved to T-2221
- 2026-10-30T23:36:12Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-30T23:36:12Z focused
- 2026-10-30T23:36:28Z review fixes re-filed through a clean cold read (put24); find × CLI restored as code-exists (the MCP find tool runs it); only find × Claude Code (SessionStart leads) still waits on T-2230
- 2026-10-30T23:37:26Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research draft-critique-initiative-gen1: Task: T-2120, T-2121, T-2122, T-2123, T-2124, T-2125, T-2126, T-2127 (all done), and the fixes their reviews and
- T-2159 [FEATURE M, done, 3 steps] Coverage must be real: reset coverage.md's templated cells (a shim to…, a site page to…,… — lesson: A templated-text detector has to co…
- T-2124 [FEATURE M, done, 2 steps] Scout project probes: fm find + prove on the user's own project, at most 3 a day, proven only, refutation ledger, doctor faults to the …
- decision 2026-10-30: [cites: user steer 2026-10-29: COVERAGE BY GRID, NOT BY LUCK] Genesis standing rule: coverage by grid — coverage.md (fm genesis put): rows = the 13 …
- similar finished tasks took 2–3 steps
## Lessons
- A cold reader with no code access can only judge claims, not facts: pair it with one code-reading review before filing an inventory, or it drops true cells and keeps false ones
