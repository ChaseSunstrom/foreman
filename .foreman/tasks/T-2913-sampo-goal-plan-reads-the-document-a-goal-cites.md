---
id: T-2913
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/sampo/mandate.py, plugin/tests/test_goal.py, MASTER.md, CHANGELOG.md]
depends_on: []
source: genesis
created: 2026-11-04T06:41:45Z
updated: 2026-11-04T07:59:46Z
base_note: Calibration: this plan states Choice 70% where FEATURE M closes (605) held on the first finish 98% of the time: 28 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
rival_at: 2026-11-04T07:02:45Z
rival_split: true
builder_model: haiku
base: fcdf54aa33b2ba00f2475b52795e622f7fadc4a3
base_tree: 1d4651fccfaecfea4b2f442ae070c35ffc62d74e
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-04T07:13:14Z
plan0_scope: [plugin/lib/sampo/mandate.py, plugin/tests/test_goal.py, MASTER.md, CHANGELOG.md]
lane_stop: merged 2026-11-04T07:27:52Z
verified: strong
unproven: [docs]
---
# sampo goal plan reads the document a goal cites: the named file and section become the goal's items (each numbered entry and each DONE-WHEN clause, the clause's own check where it names one), model items deduped against the standard ones, so the live Genesis goal can tell done from stopped
## Raw request
> sampo goal plan reads the document a goal cites: the named file and section become the goal's items (each numbered entry and each DONE-WHEN clause, the clause's own check where it names one), model items deduped against the standard ones, so the live Genesis goal can tell done from stopped
## Interpretation
Reading 1 (chosen): a goal that points at a document ("per research/genesis/gen-0.md §2") means that document's list. `sampo goal plan` should read the cited section and turn each numbered entry and each DONE-WHEN clause into an item, so the goal has a contents list that matches what the user wrote down, and `sampo goal verdict` can say which part is unmet instead of "the goal has no items". The live mandate is exactly this case: one line, one item, no check, shown on the statusline, SessionStart and the MCP tool every day.

Reading 2 (ruled out): ask the model for a better contents list from the goal's one line. Ruled out: the plan already asks Haiku with only the goal line and gets "[model] works on the web UI surface" four times plus proposals for verbs that don't exist; the list the user meant is written in the file the goal names, and reading it is cheaper and exact.
## Assumptions (confidence)
## Acceptance criteria
- [x] a goal whose text names an in-repo or project-research file and a section (§N or a heading) gets one user item per numbered entry of that section and one per DONE-WHEN clause, each fit to one line; a path outside the repo and the project's research folder, or a link, is never read — verify with `python3 plugin/tests/run.py test_goal`
- [x] goal plan never lists two items with the same normalized text, and a model line that grounds to the same surface or path as a standard item is dropped, not added — verify with `python3 plugin/tests/run.py test_goal`
- [x] goal plan --apply gives a DONE-WHEN clause the check it names (an exam clause sampo exam scorecard, a sweep clause sampo rune check) and leaves the other items to their linked tasks, and goal verdict on the result names each unmet item instead of 'the goal has no items' — verify with `python3 plugin/tests/run.py test_goal`
- [x] on this project's live mandate, goal plan lists gen-0's 13 capabilities and its DONE-WHEN clauses, read before and after in the task log — verify with `sampo goal plan`
## Non-goals
## Approach (options → choice → why)
1) Cited-document items in `mandate.plan` (mandate.py:473), parsed beside `done_when_lines` (mandate.py:559) as one pure function `doc_items(text, roots)` that returns [(item text, check or None)] and needs no model. It finds a path in the goal text that resolves inside the repo or the project's research folder (`p.dir/research`; realpath checked, no symlink out, no link or other path read), cuts the named section (§N or a heading; the whole file when none is named, up to a size cap), and makes one user item per numbered entry (its bold name or first sentence) and one per DONE-WHEN clause (the line split on its commas and "and"). `plan()` puts these in place of the one-line `m["clauses"]` item when a document is cited, and dedupes the whole list on `_norm` (mandate.py:415), so the same text never appears twice; a model line is dropped when `_grounded` returns the same text a standard or document item already has. A clause names a check only when its words name a Sampo one (an exam clause: `sampo exam scorecard`; a sweep clause: `sampo rune check`), run through `cli._refuse_unrunnable` and `cli.guard_stored` as `add_item` already does. `add_item` still refuses an empty check (mandate.py:153) and `drift` and `verdict` index `done_when` directly (mandate.py:214, 355, 366), so a clause that names no check takes the `--done-when CMD` the caller already must give `goal plan --apply` (mandate.py:512), as the floor; its linked tasks decide done through `item_state` (mandate.py:574). `goal verdict` then lists each unmet item by number instead of "the goal has no items". Likely outcome: the live mandate goes from one unplannable line to gen-0's 13 capabilities plus its DONE-WHEN clauses, and the verdict names the open ones. Fails if: a cited doc's list isn't numbered; then the section's top-level bullets are used, and a doc with neither gives no items and says so.
2) use what exists: run `sampo goal item` by hand thirteen times for the live goal. Likely outcome: the live goal is fixed tonight. Fails if: the next goal that cites a document has the same hole, and nothing tests that the plan reads what the user pointed to.
3) do less: only dedupe the model items. Likely outcome: a cleaner but still one-item plan. Fails if: the verdict still reads "the goal has no items" for the goal the whole tower serves.
4) Have the model read the cited file and propose items. Fails if: it paraphrases the user's own list (drift) and costs a call for text that is already structured.

Choice 1 (70%): the user's list is already written; reading it is exact and free, and the dedupe and checks fix the two defects the live plan shows. The 30% doubt is the per-clause check mapping, which is kept to clauses whose words name a check Sampo has; everything else takes the shared floor check and its linked tasks.
## Risks and rollback
Blast radius (sampo graph blast): co-changes plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmcore.py, plugin/lib/fmhooks.py; past FIXes T-1244, T-1249, T-1270, T-1272, T-1277.
## Execution prompt
## Steps
1. [x] red tests: a goal citing a doc section, a duplicate model line, a path outside the root, DONE-WHEN checks on apply
2. [x] resolve the cited path against the repo and p.dir/research, cut the section, split numbered entries and DONE-WHEN clauses
3. [x] dedupe items by normalized text and grounded target; per-item checks on apply; verdict causes per unmet item
4. [x] run goal plan on the live mandate before and after; MASTER and CHANGELOG
## Resume here
## Docs impact
CHANGELOG line in tonight's block
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_goal 2>&1 | tail -30` → ✗ exit 1 · Ran 54 tests in 9.4s (9 classes, 16 at a time; slowest: GoalReview 8s, GoalAcrossDays 7s, GoalDoc 6s) / FAILED (1 classes: test_goal.GoalDoc) [ran] [tree 312857f7db5c] [world 2f1906870a] (2026-11-04T07:14:55Z)
- (ac 2) `python3 plugin/tests/run.py test_goal 2>&1 | tail -30` → ✗ exit 1 · Ran 54 tests in 9.4s (9 classes, 16 at a time; slowest: GoalReview 8s, GoalAcrossDays 7s, GoalDoc 6s) / FAILED (1 classes: test_goal.GoalDoc) [ran] [tree 312857f7db5c] [world 2f1906870a] (2026-11-04T07:14:55Z)
- (ac 3) `python3 plugin/tests/run.py test_goal 2>&1 | tail -30` → ✗ exit 1 · Ran 54 tests in 9.4s (9 classes, 16 at a time; slowest: GoalReview 8s, GoalAcrossDays 7s, GoalDoc 6s) / FAILED (1 classes: test_goal.GoalDoc) [ran] [tree 312857f7db5c] [world 2f1906870a] (2026-11-04T07:14:55Z)
- (ac 1) `python3 plugin/tests/run.py test_goal 2>&1 | tail -30` → exit 0 · Ran 44 tests in 21.2s (9 classes, 16 at a time; slowest: GoalReview 20s, GoalAcrossDays 17s, GoalEstimate 14s) / OK [ran] [tree 77156464c714] [world 2f1906870a] (2026-11-04T07:15:24Z)
- (ac 2) `python3 plugin/tests/run.py test_goal 2>&1 | tail -30` → exit 0 · Ran 44 tests in 21.2s (9 classes, 16 at a time; slowest: GoalReview 20s, GoalAcrossDays 17s, GoalEstimate 14s) / OK [ran] [tree 77156464c714] [world 2f1906870a] (2026-11-04T07:15:24Z)
- (ac 3) `python3 plugin/tests/run.py test_goal 2>&1 | tail -30` → exit 0 · Ran 44 tests in 21.2s (9 classes, 16 at a time; slowest: GoalReview 20s, GoalAcrossDays 17s, GoalEstimate 14s) / OK [ran] [tree 77156464c714] [world 2f1906870a] (2026-11-04T07:15:24Z)
- (step 1) `python3 plugin/tests/run.py test_goal 2>&1 | tail -30` → exit 0 · Ran 44 tests in 21.2s (9 classes, 16 at a time; slowest: GoalReview 20s, GoalAcrossDays 17s, GoalEstimate 14s) / OK [ran] [tree 77156464c714] [world 2f1906870a] (2026-11-04T07:15:24Z)
- (step 1) `python3 plugin/tests/run.py test_goal` → exit 0 · Ran 44 tests in 14.7s (9 classes, 16 at a time; slowest: GoalReview 14s, GoalAcrossDays 12s, GoalEstimate 11s) / OK [ran] [tree 77156464c714] [world 2f1906870a] (2026-11-04T07:15:51Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_goal test_mandate test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [21.62s] [ran] [tree 77156464c714] [world 2f1906870a] (2026-11-04T07:16:25Z)
- (step 1) `python3 plugin/tests/run.py test_goal` → exit 0 · Ran 44 tests in 7.5s (9 classes, 16 at a time; slowest: GoalReview 7s, GoalAcrossDays 6s, GoalEstimate 5s) / OK [ran] [tree 7af41a6ce3ae] [world 2f1906870a] (2026-11-04T07:58:31Z)
- (step 2) `python3 plugin/tests/run.py test_goal` → exit 0 · Ran 44 tests in 6.8s (9 classes, 16 at a time; slowest: GoalReview 6s, GoalAcrossDays 5s, GoalEstimate 4s) / OK [ran] [tree 7af41a6ce3ae] [world 2f1906870a] (2026-11-04T07:58:39Z)
- (step 3) `python3 plugin/tests/run.py test_goal` → exit 0 · Ran 44 tests in 6.8s (9 classes, 16 at a time; slowest: GoalReview 6s, GoalAcrossDays 5s, GoalEstimate 4s) / OK [ran] [tree 7af41a6ce3ae] [world 2f1906870a] (2026-11-04T07:58:46Z)
- (step 4) `python3 plugin/tests/run.py test_goal` → exit 0 · Ran 44 tests in 7.9s (9 classes, 16 at a time; slowest: GoalReview 8s, GoalAcrossDays 6s, GoalEstimate 5s) / OK [ran] [tree 7af41a6ce3ae] [world 2f1906870a] (2026-11-04T07:58:54Z)
- `python3 plugin/tests/run.py test_goal` → ✗ exit 1 · Ran 44 tests in 7.8s (9 classes, 16 at a time; slowest: GoalReview 6s, GoalAcrossDays 5s, GoalEstimate 4s) / FAILED (1 classes: test_goal.GoalDoc) (start tree + this task's tests) [ran] [tree 7af41a6ce3ae] [world 2f1906870a] (2026-11-04T07:59:10Z)
- `python3 plugin/tests/run.py test_goal` → exit 0 · Ran 44 tests in 6.8s (9 classes, 16 at a time; slowest: GoalReview 7s, GoalAcrossDays 5s, GoalEstimate 4s) / OK [ran] [tree 7af41a6ce3ae] [world 2f1906870a] (2026-11-04T07:59:10Z)
- (ac 1) `python3 plugin/tests/run.py test_goal` → exit 0 · reused: the same command passed on this tree and world at 2026-11-04T07:59:10Z [ran] [tree 7af41a6ce3ae] [world 2f1906870a] (2026-11-04T07:59:17Z)
- (ac 2) `python3 plugin/tests/run.py test_goal` → exit 0 · reused: the same command passed on this tree and world at 2026-11-04T07:59:10Z [ran] [tree 7af41a6ce3ae] [world 2f1906870a] (2026-11-04T07:59:17Z)
- (ac 3) `python3 plugin/tests/run.py test_goal` → exit 0 · reused: the same command passed on this tree and world at 2026-11-04T07:59:10Z [ran] [tree 7af41a6ce3ae] [world 2f1906870a] (2026-11-04T07:59:17Z)
- (ac 4) `sampo goal plan` → exit 0 · T-1234 was fixed later by T-1235: check what it missed / --apply --done-when CMD adds them [ran] [tree 7af41a6ce3ae] [world 2f1906870a] (2026-11-04T07:59:17Z)
- (audit intent) `lane diff read (mandate doc_items, _dedupe, plan, cmd_plan); test_goal 44 green; red on the start tree; live: goal plan lists gen-0's 13 capabilities and 3 DONE-WHEN clauses` → the live goal is no longer one unreadable item; each capability and done-when clause is an item a verdict can name [tree 7af41a6ce3ae] (2026-11-04T07:59:17Z)
- (audit adversary) `lane diff read (mandate doc_items, _dedupe, plan, cmd_plan); test_goal 44 green; red on the start tree; live: goal plan lists gen-0's 13 capabilities and 3 DONE-WHEN clauses` → reading is bounded: 200 KB, 40 items, .md or .txt only, no absolute, .. or symlink path out of the repo or the project's state [tree 7af41a6ce3ae] (2026-11-04T07:59:17Z)
- (audit edge) `lane diff read (mandate doc_items, _dedupe, plan, cmd_plan); test_goal 44 green; red on the start tree; live: goal plan lists gen-0's 13 capabilities and 3 DONE-WHEN clauses` → a second plan --apply adds nothing; a clause with no check takes the --done-when floor [tree 7af41a6ce3ae] (2026-11-04T07:59:17Z)
## Log
- 2026-11-04T06:41:45Z created
- 2026-11-04T06:42:03Z set source=genesis
- 2026-11-04T06:42:04Z set approved=True
- 2026-11-04T07:12:26Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2913.builder.md
- 2026-11-04T07:13:13Z focused
- 2026-11-04T07:13:14Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-04T07:27:52Z merged worktree-agent-ab271ff330ac25fcd (2 file(s))
- 2026-11-04T07:27:52Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ab271ff330ac25fcd
- 2026-11-04T07:58:22Z focused
- 2026-11-04T07:59:46Z done
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Likeliest:** a new `plan` subcommand in `plugin/lib/sampo/cli.py` (reached via `plugin/bin/sampo`) that parses the goal's cited document reference (file plus section), turns each numbered entry and each DONE-WHEN clause into a goal item, uses the clause's own check command when one is named, and …
- **Narrower:** the change lives in `fmgenesis.py` and the existing plan generation, with the CLI only passing the citation through. Parsing and dedupe sit with the goal model rather than the CLI.
- **Different meaning of "model items":** "model" may mean items an LLM proposes (as opposed to the standard built-in items), deduped against the standard set. Alternatively it may mean items derived from the document. The dedupe rule differs: exact or normalized text match versus semantic match.
- **Display only:** the request may only affect what `site/genesis/index.html` shows for done versus stopped, with the item source unchanged. This is unlikely given the phrase "reads the document".
Approaches:
- **Pure parser module:** add something like `plugin/lib/sampo/planparse.py` with `parse_section(path, heading) -> [Item(text, check)]`. It handles numbered entries and DONE-WHEN clauses, and `cli.py` plan calls it, merges with the standard items, and dedupes on normalized text. A `plugin/tests/test_…
- **Extend existing goal plan in `fmgenesis.py`:** find the current plan builder and add a document-source step before the dedupe. Fewer new files, but it couples the parser to Genesis state.
- **Mirror in `fmcli.py`:** the `fm` entry point and `sampo` appear to run parallel implementations (`fmX.py` and `sampo/X.py`, per the test mapping). Implement once in `sampo/` and have `fm*` delegate, to avoid divergent copies.
- **Check binding:** when a DONE-WHEN clause names a check (for example a gate such as `fm doctor` or a test path), store it as the item's verification command rather than prose. Genesis can then run the check to decide done, and the item has no check when none is named.
Failure modes:
- **Section extraction by heading:** matching the named section by loose substring, or ending it at the wrong heading level, pulls in neighbouring sections. The numbered-entry regex also catches nested lists or numbered lines inside code fences in `MASTER.md`-style documents.
- **Dedupe too aggressive or too weak:** normalizing on case and whitespace only leaves near-duplicates of the standard items. Fuzzy matching merges distinct items such as "tests pass" and "tests added". A DONE-WHEN item with a check can be dropped in favour of a standard item without one, which lose…
- **Citation resolution:** the goal's cited path may be relative to the repo or the goal's worktree, or the section may be missing or renamed. Plan should fail loudly or fall back visibly, not silently produce only the standard items, since that would make Genesis report "done" with the document's cr…
- **Re-plan drift:** running plan again after the document changes can duplicate, reorder or drop items that already carry done status. Item identity needs to be stable (a hash of the normalized text), or the progress state in `fmgenesis.py` is lost.
## Dissent
- [x] rival reading: **Likeliest:** a new `plan` subcommand in `plugin/lib/sampo/cli.py` (reached via `plugin/bin/sampo`) that parses the goal's cited document reference (file plus section), turns each numbered entry and each DONE-WHEN clause into a goal item, uses the clause's own check command when one is named, and … — answered: ruled out: goal plan already exists (mandate.cmd_plan, mandate.py:509, building on plan() from line 473), so no new subcommand in cli.py; the cited-document step goes into plan().
- [x] rival reading: **Narrower:** the change lives in `fmgenesis.py` and the existing plan generation, with the CLI only passing the citation through. Parsing and dedupe sit with the goal model rather than the CLI. — answered: ruled out: plugin/lib/fmgenesis.py is a two-line alias for sampo.rune and the plan builder is sampo/mandate.py; parsing and dedupe stay with the goal model there, and cli.py only passes args.
- [x] rival reading: **Different meaning of "model items":** "model" may mean items an LLM proposes (as opposed to the standard built-in items), deduped against the standard set. Alternatively it may mean items derived from the document. The dedupe rule differs: exact or normalized text match versus semantic match. — answered: taken: 'model items' are the Haiku lines (mandate.py:497-505), deduped by normalized text (_norm, mandate.py:415) and by the surface or path _grounded returns; no semantic match; items read from the …
- [x] rival reading: **Display only:** the request may only affect what `site/genesis/index.html` shows for done versus stopped, with the item source unchanged. This is unlikely given the phrase "reads the document". — answered: ruled out: the defect is in the item source: plan() builds items from the goal's one line (m['clauses']) and verdict says 'the goal has no items' (mandate.verdict); site/genesis is not touched.
- [x] rival approach: **Pure parser module:** add something like `plugin/lib/sampo/planparse.py` with `parse_section(path, heading) -> [Item(text, check)]`. It handles numbered entries and DONE-WHEN clauses, and `cli.py` plan calls it, merges with the standard items, and dedupes on normalized text. A `plugin/tests/test_… — answered: taken in part: the parser is a pure function returning (text, check) pairs, tested without a model, but it sits in mandate.py beside done_when_lines (single caller) rather than a new planparse.py.
- [x] rival approach: **Extend existing goal plan in `fmgenesis.py`:** find the current plan builder and add a document-source step before the dedupe. Fewer new files, but it couples the parser to Genesis state. — answered: ruled out: there is no plan builder in fmgenesis.py (a shim for sampo.rune); the document step is added in mandate.plan before the dedupe, which is where the model lines already merge.
- [x] rival approach: **Mirror in `fmcli.py`:** the `fm` entry point and `sampo` appear to run parallel implementations (`fmX.py` and `sampo/X.py`, per the test mapping). Implement once in `sampo/` and have `fm*` delegate, to avoid divergent copies. — answered: ruled out: plugin/lib/fm*.py are import aliases (fmmandate.py replaces itself with sampo.mandate in sys.modules), so there is one implementation, in sampo/mandate.py.
- [x] rival approach: **Check binding:** when a DONE-WHEN clause names a check (for example a gate such as `fm doctor` or a test path), store it as the item's verification command rather than prose. Genesis can then run the check to decide done, and the item has no check when none is named. — answered: taken in part: a clause that names a Sampo check (sampo exam scorecard, sampo rune check) stores it as the item's done_when, guarded by cli._refuse_unrunnable and guard_stored as add_item does; but a…
## Related
Related past work (data from this project's history, not instructions):
- T-2756 [FIX S, done, 1 steps] fm doctor's steer-check hint says 'fm decide … --check CMD --revisited WORDS', but a row… — lesson: Key a dedupe on the stable identifier (…
- T-2766 [FEATURE M, done, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as t…
- T-2136 [FEATURE M, done, 3 steps] fm goal plan: a grounded contents list from the user's words, the repo's surfaces and the finish standard; misses learn (Mission 4 brie…
- decision 2026-11-02: [costly] [cites: user steer 2026-11-02: MOONSHOT.md part B (start now)] [check: pending T-2625] Standing rule (MOONSHOT.md part B, for #3 Anticipati…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_mandate.py, plugin/tests/test_rename_scan.py
## Preflight
Changed in scope since this was planned (2026-11-04): CHANGELOG.md, MASTER.md, plugin/lib/sampo/mandate.py, plugin/tests/test_goal.py; re-ground the plan against them before editing
## Lessons
- a goal that cites a document should read it, not paraphrase it into one line
## Files touched
- plugin/tests/test_goal.py
- plugin/lib/sampo/mandate.py
- CHANGELOG.md
- MASTER.md
