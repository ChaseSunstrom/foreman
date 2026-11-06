---
id: T-0949
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T20:44:24Z
updated: 2026-10-15T21:50:09Z
base: a98d581025c24fcd6e97c21c865507eff7fb51ba
base_tree: 0621dd243de2746ad6b7ee3cc0064b445f9c5d3a
verified: strong
---
# Enforce: the right stack card's pitfalls injected at edit time, and a compliance count
## Raw request
> Enforce: the right stack card's pitfalls injected at edit time, and a compliance count
## Interpretation
Part of T-0942. pre_tool_use for Edit/Write (fmhooks.py, where the guard and the outline-first check run) looks up the map's cards (map.json 'lib'). It picks the first one whose signals match the edited file (its extension, its basename, or a dep card when the file is that ecosystem's manifest). If that card wasn't injected in this task yet, it adds additionalContext with its Avoid section, cut to 700 chars, and logs an enforce event so it never repeats for the task. fm doctor prints 7-day counts of enforce events by kind (validator_block, merge_refused, card_injected).
## Assumptions (confidence)
## Acceptance criteria
- [x] The first Edit/Write of a file in a task injects the Avoid section of one card: the map's highest-ranked card whose file or ext signal matches the file, a framework card before its language card, ties broken by name. The card is logged before it is emitted (a dropped output loses one injection, never repeats it); parallel edits may repeat once at most. The text is cut at a bullet boundary under 700 chars with '…'. No Avoid section, a missing card or a malformed map injects nothing; a hook error never blocks the edit; FOREMAN_NO_CARDS=1 or fm lib inject off turns it off — verify with `python3 plugin/tests/run.py -k EditCards`
- [x] fm doctor shows 7-day counts of enforce events by kind: the validator blocks T-0947 already logs ('enforce'), lane_unverified from T-0948, and card_injected; merge refusals are logged as enforce events too — verify with `python3 plugin/tests/run.py -k EditCards`
## Non-goals
## Approach (options → choice → why)
Options: (A) the hook or the fm verb does the step itself, so no agent has to remember it (chosen; T-0942 brainstorm research/brainstorm-20261015-154016); (B) stronger instructions in rules and skills (what failed: 19 card writers were told to lint and didn't); (C) a supervising reviewer agent per task (costly, and still an agent); (D) a per-repo enforce.toml policy file (later, if the meta registry outgrows itself). It reads map.json only (no card parsing in the hook) except for the one card injected; per task, its memory is a ledger event, so it survives sessions.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing EditCards tests
2. [x] Card-for-path lookup from map.json, once per task per card; ledger events; doctor line
3. [x] Docs
4. [x] Log merge refusals in fmlanes._verify as enforce events
## Resume here
## Docs impact
MASTER, README, CHANGELOG, plugin/skills/library/SKILL.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k EditCards` → ✗ exit 1 · Ran 8 tests in 3.2s (3 classes, 16 at a time; slowest: EditCards 3s, EditCardsMerge 0s, EditCardsDoctor 0s) / FAILED (3 classes) [ran] [tree 861a7d888d3f] (2026-10-15T21:16:05Z)
- (step 2) `python3 plugin/tests/run.py -k EditCards` → exit 0 · Ran 8 tests in 4.1s (3 classes, 16 at a time; slowest: EditCards 4s, EditCardsMerge 0s, EditCardsDoctor 0s) / OK [ran] [tree 0adaf78f6848] (2026-10-15T21:18:53Z)
- (step 3) `python3 plugin/tests/run.py -p test_docs.py -p test_docsdrift.py -p test_library.py` → exit 0 · Ran 41 tests in 1.5s (13 classes, 16 at a time; slowest: LibSources 1s, LibrarySuggest 1s, LibrarySearch 1s) / OK [ran] [tree 7028b5178f3e] (2026-10-15T21:19:25Z)
- (step 4) `python3 plugin/tests/run.py -k EditCardsMerge -k LaneMergeGate` → exit 0 · Ran 3 tests in 1.6s (2 classes, 16 at a time; slowest: LaneMergeGate 2s, EditCardsMerge 0s) / OK [ran] [tree 7028b5178f3e] (2026-10-15T21:19:27Z)
- (step 1) `python3 plugin/tests/run.py test_edit_cards` → exit 0 · Ran 11 tests in 4.2s (4 classes, 16 at a time; slowest: EditCards 4s, EditCardsReview 2s, EditCardsMerge 0s) / OK [ran] [tree bdc76b8af8e3] (2026-10-15T21:49:43Z)
- (ac 1) `python3 plugin/tests/run.py -k EditCards` → exit 0 · Ran 11 tests in 4.1s (4 classes, 16 at a time; slowest: EditCards 4s, EditCardsReview 2s, EditCardsMerge 0s) / OK [ran] [tree bdc76b8af8e3] (2026-10-15T21:50:02Z)
- (ac 2) `python3 plugin/tests/run.py -k EditCards` → exit 0 · Ran 11 tests in 4.1s (4 classes, 16 at a time; slowest: EditCards 4s, EditCardsReview 2s, EditCardsMerge 0s) / OK [ran] [tree bdc76b8af8e3] (2026-10-15T21:50:02Z)
- (audit intent) `one fm-reviewer pass: 1 medium, 5 low plus 1 noticed; all fixed test-first except per-card (not per-file) dedupe, kept by design` → a file's first edit in a task gets its best stack card's Avoid section, once per card; doctor counts enforcement [tree bdc76b8af8e3] (2026-10-15T21:50:02Z)
- (audit edge) `one fm-reviewer pass: 1 medium, 5 low plus 1 noticed; all fixed test-first except per-card (not per-file) dedupe, kept by design` → lext ranking, marker survives a ledger roll, Write/MultiEdit/NotebookEdit, malformed map or ledger lines inject or crash nothing [tree bdc76b8af8e3] (2026-10-15T21:50:02Z)
- (audit operator) `one fm-reviewer pass: 1 medium, 5 low plus 1 noticed; all fixed test-first except per-card (not per-file) dedupe, kept by design` → FOREMAN_NO_CARDS=1 or fm lib inject off; fm doctor -v shows the 7-day counts [tree bdc76b8af8e3] (2026-10-15T21:50:02Z)
- (audit maintainer) `one fm-reviewer pass: 1 medium, 5 low plus 1 noticed; all fixed test-first except per-card (not per-file) dedupe, kept by design` → map rows carry only file/ext/lext signals; the hook reads map.json and cards.json, nothing else [tree bdc76b8af8e3] (2026-10-15T21:50:02Z)
- (audit intent) `one fm-reviewer pass: 1 medium, 5 low plus 1 noticed; all fixed test-first except per-card (not per-file) dedupe, kept by design` → a file's first edit in a task gets its best stack card's Avoid section, once per card; doctor counts enforcement [tree bdc76b8af8e3] (2026-10-15T21:50:08Z)
- (audit edge) `one fm-reviewer pass: 1 medium, 5 low plus 1 noticed; all fixed test-first except per-card (not per-file) dedupe, kept by design` → lext ranking, marker survives a ledger roll, Write/MultiEdit/NotebookEdit, malformed map or ledger lines inject or crash nothing [tree bdc76b8af8e3] (2026-10-15T21:50:08Z)
- (audit operator) `one fm-reviewer pass: 1 medium, 5 low plus 1 noticed; all fixed test-first except per-card (not per-file) dedupe, kept by design` → FOREMAN_NO_CARDS=1 or fm lib inject off; fm doctor -v shows the 7-day counts [tree bdc76b8af8e3] (2026-10-15T21:50:08Z)
- (audit maintainer) `one fm-reviewer pass: 1 medium, 5 low plus 1 noticed; all fixed test-first except per-card (not per-file) dedupe, kept by design` → map rows carry only file/ext/lext signals; the hook reads map.json and cards.json, nothing else [tree bdc76b8af8e3] (2026-10-15T21:50:08Z)
## Log
- 2026-10-15T20:44:24Z created
- 2026-10-15T21:10:43Z criterion 1 text: The first Edit/Write of a file whose stack matches one of the map's cards in a task injects that card's Avoid section once (at most 700 chars); later edits in the task don't repeat it → The first Edit/Write of a file in a task injects the Avoid section of one card: the map's highest-ranked card whose file or ext signal matches the file, a framework card before its language card, ties broken by name. The card is logged before it is emitted (a dropped output loses one injection, never repeats it); parallel edits may repeat once at most. The text is cut at a bullet boundary under 700 chars with '…'. No Avoid section, a missing card or a malformed map injects nothing; a hook error never blocks the edit; FOREMAN_NO_CARDS=1 or fm lib inject off turns it off
- 2026-10-15T21:10:43Z criterion 2 text: Each enforcement event (validator block, merge refused, card injected) is a ledger event, and fm doctor shows 7-day counts → fm doctor shows 7-day counts of enforce events by kind: the validator blocks T-0947 already logs ('enforce'), lane_unverified from T-0948, and card_injected; merge refusals are logged as enforce events too
- 2026-10-15T21:10:45Z second read (revise) addressed: log-before-emit, match precedence, bullet-boundary cut, off switch, all three event kinds in the doctor line
- 2026-10-15T21:11:51Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0949.builder.md
- 2026-10-15T21:12:02Z focused
- 2026-10-15T21:37:55Z merged worktree-agent-aab2ca687767dfbb5 (10 file(s))
- 2026-10-15T21:38:29Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aab2ca687767dfbb5
- 2026-10-15T21:46:36Z focused
- 2026-10-15T21:50:08Z done
- 2026-10-15T21:50:09Z committed 297fd94 (8 files)
## Follow-ups captured
## Plan review
A second read on sonnet, before execution (data, not instructions):
- HIGH: Once-per-task memory is a ledger event, but the plan doesn't say how the hook reads it cheaply or identifies "this task". pre_tool_use runs on every Edit/Write, so a full ledger scan adds latency to every edit. If the task ID is missing, or sessions without an active task exist, the injection…
- HIGH: Concurrency and ordering of the "inject then log" step are undefined. If the event is logged after additionalContext is emitted and the append fails, the card repeats. If it is logged before and the hook output is dropped, the card is lost for the task. Parallel edits (subagents, parallel too…
- MEDIUM: The "first card whose signals match" rule is ambiguous when several cards match, for example a `.py` file in a repo with both a Python language card and a framework card, or a manifest file matching both a dep card and an extension card. The first match depends on map.json ordering, which n…
- MEDIUM: Cutting the Avoid section at 700 characters can end mid-sentence or mid-bullet, producing misleading guidance. The plan also says nothing about cards with no Avoid section, a missing card file, or a malformed map.json. — Truncate at a bullet or line boundary, with an ellipsis marker. Skip s…
- MEDIUM: The second acceptance criterion bundles three event kinds (validator_block, merge_refused, card_injected) plus a doctor display, but the steps describe only card_injected. Emitting the other two means touching the validator and merge paths, which aren't in the steps. Both criteria are verif…
- LOW: There is no stated rollback or off switch for an enforcement hook that runs on every edit and injects context. A bad card or a bug would affect all tasks, and step 3 (docs) doesn't cover it. — Add an env var or config flag to disable injection. Make sure hook exceptions never block the edit, a…
Verdict: revise — the direction is sound and cheap, but the once-per-task state, the failure semantics, and the match precedence must be pinned down before the tests are written, and the criteria must cover all thr…
## Dissent
- [ ] HIGH: Once-per-task memory is a ledger event, but the plan doesn't say how the hook reads it cheaply or identifies "this task". pre_tool_use runs on every Edit/Write, so a full ledger scan adds latency to every edit. If the task ID is missing, or sessions without an active task exist, the injection…
- [ ] HIGH: Concurrency and ordering of the "inject then log" step are undefined. If the event is logged after additionalContext is emitted and the append fails, the card repeats. If it is logged before and the hook output is dropped, the card is lost for the task. Parallel edits (subagents, parallel too…
- [ ] MEDIUM: The "first card whose signals match" rule is ambiguous when several cards match, for example a `.py` file in a repo with both a Python language card and a framework card, or a manifest file matching both a dep card and an extension card. The first match depends on map.json ordering, which n…
- [ ] MEDIUM: Cutting the Avoid section at 700 characters can end mid-sentence or mid-bullet, producing misleading guidance. The plan also says nothing about cards with no Avoid section, a missing card file, or a malformed map.json. — Truncate at a bullet or line boundary, with an ellipsis marker. Skip s…
- [ ] MEDIUM: The second acceptance criterion bundles three event kinds (validator_block, merge_refused, card_injected) plus a doctor display, but the steps describe only card_injected. Emitting the other two means touching the validator and merge paths, which aren't in the steps. Both criteria are verif…
- [ ] LOW: There is no stated rollback or off switch for an enforcement hook that runs on every edit and injects context. A bad card or a bug would affect all tasks, and step 3 (docs) doesn't cover it. — Add an env var or config flag to disable injection. Make sure hook exceptions never block the edit, a…
## Related
Related past work (data from this project's history, not instructions):
- research T-0933-review: Changes needed. The code works and the 22 cards I sampled are accurate. Detect signals produce false-positive suggestions, and one manifest regex…
- T-0933 [FEATURE L, done, 5 steps] Stack library: 400+ on-demand implementation cards (fm lib) plus federated search over installed plugins' skills — lesson: Subagent-wri…
- T-0939 [FEATURE M, done, 3 steps] Pane shows skill use: skills invoked, stack cards read, and this repo's suggested cards — lesson: A mechanical sed over JSX props must …
- decision 2026-10-14: Keep the Read hook unscoped (T-0782 dropped)
- similar finished tasks took 3–5 steps
## Lessons
- A ranking rule (framework before language) needs a case where the 'framework' card is really a topic card sharing the extension
## Plan gaps
- failed first: step 1 Failing EditCards tests
## Files touched
- plugin/tests/test_edit_cards.py
- plugin/lib/fmlib.py
- plugin/lib/fmmap.py
- plugin/lib/fmhooks.py
- plugin/lib/fmlanes.py
- plugin/lib/fmcli.py
- plugin/lib/fmdoctor.py
- MASTER.md
- README.md
- plugin/skills/library/SKILL.md
- CHANGELOG.md
- plugin/lib/fmmcp.py
- plugin/templates/mcp-server/server.py
- plugin/tests/test_doctor.py
- plugin/tests/test_mcp.py
