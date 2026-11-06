---
id: T-2630
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmhooks.py, plugin/lib/fmcore.py, plugin/tests/test_redefinitions.py, plugin/tests/test_hooks.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: discovered
created: 2026-11-02T18:46:57Z
updated: 2026-11-02T19:34:15Z
builder_model: sonnet
predict_minutes: 12
predict_attempts: 1
plan0_at: 2026-11-02T19:15:00Z
plan0_scope: [plugin/lib/fmhooks.py, plugin/lib/fmcore.py, plugin/tests/test_redefinitions.py, plugin/tests/test_hooks.py, CHANGELOG.md, MASTER.md]
lane_stop: merged 2026-11-02T19:30:10Z
base: b9b0f422ab014b065b755f202097dfc7f6f57ad1
base_tree: 789f470560f1405958022de9e20d7b99c22677ce
verified: strong
---
# An Edit or Write that adds a top-level def, class or assignment its Python module already defines gets a note at once, naming the name and the earlier line (third shadowed helper: _name in fmguard broke 6 guard tests until the suites ran)
## Raw request
> FEATURE: an edit that adds a top-level def, class or assignment a module already defines gets a PostToolUse note at once (the name and the earlier line), not only at full gates: test_redefinitions (T-2553) caught two shadowed helpers, and T-2068 hit a third (_name in fmguard, which broke 6 guard tests until the suites ran); reuse test_redefinitions.redefinitions on the edited file, Python only, one note per name per session
## Interpretation
Reading 1 (chosen): reuse test_redefinitions.redefinitions (T-2553) at edit time: when an Edit or Write on a .py file adds text that starts a top-level def, class or assignment, parse the file once and note any name now defined twice, with both lines. Reading 2 (ruled out): block the edit. A second def can be deliberate mid-refactor, and the full suites already fail on it; a note at the moment of the edit is what was missing.
## Assumptions (confidence)
## Acceptance criteria
- [x] an edit whose new text defines a top-level name the file already had gets a PostToolUse note naming both lines; an in-place rebinding (X = f(X)) and an edit that adds no top-level name get none — verify with `python3 plugin/tests/run.py test_redefinitions`
- [x] the hook suites pass and the prompt-to-note cost stays inside the hook budget — verify with `python3 plugin/tests/run.py test_hooks test_redefinitions test_perf_cost test_speed`
## Non-goals
## Approach (options → choice → why)
1) A PostToolUse note: prefilter the edit's own new text with a regex for a column-0 def, class or NAME =, and only then ast-parse the file. Likely outcome: no parse on most edits, one parse (tens of ms) when a top-level name is added. 2) A pre-commit lint (pyflakes F811). Fails if: it runs at commit, the same late moment as the suites. 3) Run test_redefinitions after every edit. Fails if: it parses all 120 modules each time. 4) Do less: a note in the hint text of the shadowing failure only. Likely outcome: still found only when tests fail. 5) Use what exists: test_redefinitions.redefinitions already tells a shadow from a deliberate rebinding; move it to fmcore and import it from both. Likely outcome: one function, two callers. Choice: 1 built on 5 (85%).
## Risks and rollback
Hook latency: the regex prefilter keeps the parse off ordinary edits; a parse error is silent (no note). Rollback: git revert.
Blast radius (fm graph blast): co-changes plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, README.md, plugin/lib/fmexam.py; past FIXes T-1056, T-1106, T-1117, T-1122, T-1124.
## Execution prompt
## Steps
1. [x] red test
2. [x] move redefinitions() into fmcore; the PostToolUse note, prefiltered on the edit's own text
3. [x] docs: CHANGELOG, MASTER
## Resume here
<!-- auto -->
- 2026-11-02T19:26:13Z step 1/3: red test
- git: foreman/build; 1 uncommitted: MOONSHOT.md
- touched since last checkpoint: .claude/worktrees/agent-a93cf226742c3212e/plugin/tests/test_redefinitions.py, .claude/worktrees/agent-a93cf226742c3212e/plugin/lib/fmcore.py, .claude/worktrees/agent-a93cf226742c3212e/plugin/lib/fmhooks.py
## Docs impact
CHANGELOG (Unreleased entry); MASTER.md: a Shadowed names at edit time bullet under Hooks, notes and steering (map count bumped).
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_redefinitions` → ✗ exit 1 (never ran: no tests ran) · Ran 0 tests in 0.3s (1 classes, 16 at a time; slowest: _FailedTest 0s) / FAILED (1 classes: unittest.loader._FailedTest) [ran] [tree a51ade902eb4] [world 2f1906870a] (2026-11-02T19:15:28Z)
- (step 2) `python3 plugin/tests/run.py test_hooks test_redefinitions test_onwrite` → exit 0 · Ran 264 tests in 45.3s (35 classes, 16 at a time; slowest: Stop 45s, NoTaskGate 27s, PreToolUse 23s) / OK [ran] [tree ebd1dc5ba73f] [world 2f1906870a] (2026-11-02T19:17:18Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_cards_at_prompt test_core test_drive_side test_guard_evasions test_hooks test_memory test_redefinitions test_rewind test_tool_taint && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 435 tests in 62.6s (71 classes, 16 at a time; slowest: Stop 62s, NoTaskGate 44s, PreToolUse 40s) / FAILED (1 classes: test_core.LazyPatterns) [ran] [tree ebd1dc5ba73f] [world 2f1906870a] (2026-11-02T19:18:22Z)
- (step 3) `python3 plugin/tests/run.py test_core test_redefinitions test_hooks 2>&1 | tail -4` → exit 0 · Ran 391 tests in 49.2s (61 classes, 16 at a time; slowest: Stop 49s, NoTaskGate 29s, PreToolUse 25s) / OK [ran] [tree 007e3c84d467] [world 2f1906870a] (2026-11-02T19:19:21Z)
- (step 1) `python3 plugin/tests/run.py test_redefinitions` → exit 0 · Ran 7 tests in 0.9s (2 classes, 16 at a time; slowest: RedefinitionNote 1s, Redefinitions 1s) / OK [ran] [tree 6b01269123aa] [world 2f1906870a] (2026-11-02T19:31:05Z)
- (step 2) `python3 plugin/tests/run.py test_hooks test_redefinitions test_perf_cost test_speed test_core` → exit 0 · Ran 419 tests in 46.0s (70 classes, 16 at a time; slowest: Stop 46s, NoTaskGate 28s, PreToolUse 24s) / OK [ran] [tree 6b01269123aa] [world 2f1906870a] (2026-11-02T19:31:51Z)
- (step 3) `python3 plugin/tests/run.py test_docs test_docsdrift` → exit 0 · Ran 103 tests in 8.2s (24 classes, 16 at a time; slowest: Fences 8s, DocsProof 2s, TaskLifecycle 1s) / OK [ran] [tree 6b01269123aa] [world 2f1906870a] (2026-11-02T19:32:00Z)
- (ac 1) `python3 plugin/tests/run.py test_redefinitions` → exit 0 · Ran 7 tests in 0.9s (2 classes, 16 at a time; slowest: RedefinitionNote 1s, Redefinitions 1s) / OK [ran] [tree 6b01269123aa] [world 2f1906870a] (2026-11-02T19:33:00Z)
- (ac 2) `python3 plugin/tests/run.py test_hooks test_redefinitions test_perf_cost test_speed` → exit 0 · Ran 282 tests in 45.0s (43 classes, 16 at a time; slowest: Stop 45s, NoTaskGate 26s, PreToolUse 23s) / OK [ran] [tree 6b01269123aa] [world 2f1906870a] (2026-11-02T19:33:00Z)
- (audit intent) `builder lane (sonnet) built it test-first; one foreman:fm-reviewer pass (research T-2630-review) approved with nits, all taken: decorated repeats (@overload, @f.register) skipped in the note, only the names shown marked told with the rest counted, files outside the project skipped; the criterion naming a missing test module fixed to test_perf_cost and test_speed; the lane merge landed the builder's branch without the nit commit, so the nits were applied on main through fm edit from that commit's diff` → a shadowing edit is noted with both lines at once; a rebinding X = f(X), an edit adding no top-level name, overloads and registered handlers get none (tests) [tree 6b01269123aa] (2026-11-02T19:33:00Z)
- (audit operator) `builder lane (sonnet) built it test-first; one foreman:fm-reviewer pass (research T-2630-review) approved with nits, all taken: decorated repeats (@overload, @f.register) skipped in the note, only the names shown marked told with the rest counted, files outside the project skipped; the criterion naming a missing test module fixed to test_perf_cost and test_speed; the lane merge landed the builder's branch without the nit commit, so the nits were applied on main through fm edit from that commit's diff` → the parse runs only when the edit's own text starts a column-0 name; ast is imported inside the function; the hook suites and perf tests pass [tree 6b01269123aa] (2026-11-02T19:33:00Z)
- (audit adversary) `builder lane (sonnet) built it test-first; one foreman:fm-reviewer pass (research T-2630-review) approved with nits, all taken: decorated repeats (@overload, @f.register) skipped in the note, only the names shown marked told with the rest counted, files outside the project skipped; the criterion naming a missing test module fixed to test_perf_cost and test_speed; the lane merge landed the builder's branch without the nit commit, so the nits were applied on main through fm edit from that commit's diff` → sha1 only keys the once-per-session marker (path and name), never a secret or an integrity check; a crafted file can at worst suppress or repeat a note, and a file outside the project or over 2 MB is never parsed [tree 6b01269123aa] (2026-11-02T19:33:00Z)
## Log
- 2026-11-02T18:46:57Z created
- 2026-11-02T19:13:49Z planned from capture
- 2026-11-02T19:14:51Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2630.builder.md
- 2026-11-02T19:14:59Z focused
- 2026-11-02T19:15:00Z predicted from its closes: 12 min, 1 attempt(s)
- 2026-11-02T19:23:32Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a93cf226742c3212e (branch worktree-agent-a93cf226742c3212e kept: not merged)
- 2026-11-02T19:23:32Z focused
- 2026-11-02T19:23:37Z criterion 2 verify: `python3 plugin/tests/run.py test_hooks test_redefinitions test_perf_hooks` → `python3 plugin/tests/run.py test_hooks test_redefinitions test_perf_cost test_speed`
- 2026-11-02T19:26:13Z set status=captured
- 2026-11-02T19:26:14Z lane: ~/.claude/foreman.lanes/T-2630 on foreman/T-2630
- 2026-11-02T19:30:10Z merged worktree-agent-a93cf226742c3212e (3 file(s))
- 2026-11-02T19:30:13Z lane removed: ~/.claude/foreman.lanes/T-2630 (branch foreman/T-2630 kept: not merged)
- 2026-11-02T19:30:13Z focused
- 2026-11-02T19:34:12Z done
- 2026-11-02T19:34:15Z committed 50b857d4 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2068 [FEATURE M, done, 3 steps] The interpreter-code guard refusal names the clause that fired: Foreman's module named in shell text, python settings, code that doesn'…
- T-2553 [FEATURE S, done, 2 steps] A test fails when a plugin/lib module silently redefines a top-level name — lesson: a stdlib ast test can stand in for a linter rule no…
- T-2613 [FEATURE M, done, 4 steps] fm exam long grade splits false dones into misses on names the goal never states and real misses — lesson: When an automatic rule repla…
- decision 2026-11-01: [cites: user steer 2026-11-01: decision on the cold-read rule: keep it, make it reliable (Haiku first, Sonnet decides on FAIL; a FAIL quotes the lin…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_core.py, plugin/tests/test_hooks.py
## Lessons
- fm lane merge takes the lane's recorded branch: after re-attaching a lane on a new branch, commit there and merge that branch, or the merge lands the old one
## Plan gaps
- failed first: step 1 red test
## Files touched
- plugin/tests/test_redefinitions.py
- plugin/lib/fmcore.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
- MASTER.md
