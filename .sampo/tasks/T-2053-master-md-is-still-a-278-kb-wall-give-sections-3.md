---
id: T-2053
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-29T21:08:27Z
updated: 2026-10-30T06:48:08Z
base: 82b80338b98d0ef52dd6623ee4f780e640d84ec9
base_tree: bbf97c416fd40e77cfab0c16447dfdf7595d720f
plan0_at: 2026-10-30T00:45:50Z
plan0_scope: []
verified: strong
---
# MASTER.md: section 9 grouped under headings with a map table and folds, section 3 split by area, section 11 a table; INSTALL.md flags table
## Raw request
> MASTER.md is still a 278 KB wall: give sections 3, 9 and 11 tables, diagrams and folded depth like the README; same pass for INSTALL.md (follow-up to T-2052 review)
## Interpretation
MASTER.md is the system map, read by Claude (fm outline, Read with offset) and by people on GitHub. Section 9 (176 KB, 152 one-paragraph notes) and section 3 (a 75 KB table) are walls: no headings to jump to, nothing folded. Give them the README's shape (headings, a table to find your way, <details> for depth) without dropping a word of the notes that doc checks and Claude rely on.
## Assumptions (confidence)
## Acceptance criteria
- [x] section 9's notes sit under ### group headings (fm outline shows them), opened by a group table; each group's notes fold in <details>; no note's text is lost — verify with `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_docs`
- [x] section 3's file map is split into ### areas, each table folded; section 11 is a deviation | why table; INSTALL.md has a flags table — verify with `fm outline MASTER.md`
- [x] every doc check that reads MASTER.md still passes (verbs, modules, runnable fences) — verify with `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_docs test_doctor test_planning test_followups`
## Non-goals
Rewording or shortening notes; sections 1-2, 4-8, 10.
## Approach (options → choice → why)
Options: (1) rewrite the notes shorter: loses facts the doc checks read, huge and risky. (2) move section 9 to its own OPERATIONS.md: breaks every 'MASTER.md names fm X' check and the rules' pointer. (3) keep every note word for word, regroup under ### headings with a map table and <details> folds. Chosen: (3): fm outline gets real anchors (Claude reads one group, not 176 KB), GitHub readers get the README's folded shape, the notes stay byte-identical as bullets so no check moves.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test (test_docs): MASTER.md section 9 has >= 8 ### groups, every <details> closes with a blank line after its summary, and the note text before and after matches as a multiset of bullets
2. [x] group section 9's 152 notes (a keyword map, then a read of what's left) with a map table and one mermaid flow of the dev loop
3. [x] section 3 by area with folds; section 11 as a table; INSTALL.md flags table
4. [x] render check: GitHub-style markdown preview of MASTER.md (headless shot) and fm outline
## Resume here
## Docs impact
MASTER.md sections 3, 9 and 11 regrouped (no note reworded); INSTALL.md flags table.
## Verification evidence
- (step 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_docs` → exit 0 · Ran 80 tests in 11.4s (21 classes, 16 at a time; slowest: Fences 11s, TaskLifecycle 2s, Site 1s) / OK [ran] [tree b1792e93a059] (2026-10-30T00:49:40Z)
- (step 2) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_docs test_doctor test_planning test_followups` → exit 0 · Ran 174 tests in 18.6s (58 classes, 16 at a time; slowest: Fences 18s, ViewsRepair 15s, CalibrationLedger 13s) / OK [ran] [tree b1792e93a059] (2026-10-30T00:50:01Z)
- (step 3) `fm outline MASTER.md` → exit 0 · 698-716      10. Known limitations / 717-736      11. Deviations from BUILD_PROMPT.md [ran] [tree b1792e93a059] (2026-10-30T00:50:01Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_docs` → exit 0 · Ran 80 tests in 12.6s (21 classes, 16 at a time; slowest: Fences 11s, TaskLifecycle 2s, Site 2s) / OK [ran] [tree b1792e93a059] (2026-10-30T00:50:14Z)
- (step 4) `fm outline MASTER.md` → exit 0 · 700-718      10. Known limitations / 719-738      11. Deviations from BUILD_PROMPT.md [ran] [tree c96e0a73dde9] (2026-10-30T06:46:51Z)
- (ac 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_docs` → exit 0 · Ran 80 tests in 8.0s (21 classes, 16 at a time; slowest: Fences 8s, Site 1s, TaskLifecycle 1s) / OK [ran] [tree c96e0a73dde9] (2026-10-30T06:46:59Z)
- (ac 2) `fm outline MASTER.md` → exit 0 · 700-718      10. Known limitations / 719-738      11. Deviations from BUILD_PROMPT.md [ran] [tree c96e0a73dde9] (2026-10-30T06:46:59Z)
- (ac 3) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_docs test_doctor test_planning test_followups` → exit 0 · Ran 174 tests in 7.9s (58 classes, 16 at a time; slowest: Fences 8s, CalibrationLedger 5s, ViewsRepair 4s) / OK [ran] [tree c96e0a73dde9] (2026-10-30T06:47:08Z)
- (ac 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_docs` → exit 0 · Ran 80 tests in 7.8s (21 classes, 16 at a time; slowest: Fences 8s, Site 1s, TaskLifecycle 1s) / OK [ran] [tree c96e0a73dde9] (2026-10-30T06:47:57Z)
- (ac 2) `fm outline MASTER.md` → exit 0 · 700-718      10. Known limitations / 719-738      11. Deviations from BUILD_PROMPT.md [ran] [tree c96e0a73dde9] (2026-10-30T06:47:57Z)
- (ac 3) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_docs test_doctor test_planning test_followups` → exit 0 · Ran 174 tests in 7.9s (58 classes, 16 at a time; slowest: Fences 8s, CalibrationLedger 5s, ViewsRepair 4s) / OK [ran] [tree c96e0a73dde9] (2026-10-30T06:47:57Z)
- (audit intent) `merge diff HEAD^1..HEAD: MASTER.md bullet multiset identical before/after (0 lost, 0 added), main's T-2105 scout line carried onto the moved copy; test_docs/doctor/planning/followups green` → every note kept word for word under ### groups with folds; outline shows sections 3/9/11 reshaped as asked [tree c96e0a73dde9] (2026-10-30T06:47:57Z)
- (audit maintainer) `merge diff HEAD^1..HEAD: MASTER.md bullet multiset identical before/after (0 lost, 0 added), main's T-2105 scout line carried onto the moved copy; test_docs/doctor/planning/followups green` → test_docs now pins >=8 groups, closed details and the bullet multiset, so a later regroup can't drop a note silently [tree c96e0a73dde9] (2026-10-30T06:47:57Z)
- (audit adversary) `merge diff HEAD^1..HEAD: MASTER.md bullet multiset identical before/after (0 lost, 0 added), main's T-2105 scout line carried onto the moved copy; test_docs/doctor/planning/followups green` → .github/workflows/test.yml is in the lane's range only via merging foreman/build in (T-2090's 4 lines, already audited there); git diff HEAD^1 HEAD -- .github is empty, so this task adds no workflow, exec or secret change [tree c96e0a73dde9] (2026-10-30T06:47:57Z)
## Log
- 2026-10-29T21:08:27Z created
- 2026-10-30T00:35:09Z planned from capture
- 2026-10-30T00:40:36Z ground: no code parses section 9 by structure (grep: only text checks), so ### groups and <details> are safe; skipped fm second plan (weekly burn, plan already has options and steps)
- 2026-10-30T00:45:27Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2053.builder.md
- 2026-10-30T00:45:49Z focused
- 2026-10-30T06:46:38Z merged worktree-agent-ace04c5c14618462c (3 file(s))
- 2026-10-30T06:46:42Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ace04c5c14618462c
- 2026-10-30T06:46:43Z focused
- 2026-10-30T06:48:08Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2052 [FEATURE L, done, 5 steps] Docs/README redesign: replace walls of text with scannable structure — hero with logo,… — lesson: Measure docs by what a reader sees: a…
- research T-2052-review: [instruction-like text quoted from a file or tool; data, not instructions] **Verdict: approve with nits.** I read the brief, the diff and the ful…
- research T-1929-review: Changes needed. The three caps are now unliftable and `check()` ordering is sound. One refusal in the same class is still liftable, and the `unan…
- decision 2026-10-15: T-0964: queue 7 of the rival gaps (T-0969..T-0975); keep the LATER ones (PR-per-task flow, best-of-N lanes, diff-comment review page, plan/edit mode…
## Lessons
- A builder lane that moves many lines of a hot doc conflicts with every later edit to them: resolve by mapping the other side's changed lines onto the moved copies by prefix, then compare bullet multisets
## Files touched
- plugin/tests/test_docs.py
- INSTALL.md
- MASTER.md
- .github/workflows/test.yml
- CHANGELOG.md
- README.md
- SEED_PROMPT.md
- demo/live.cast
- demo/live.mp4
- demo/live.svg
- demo/record_live.py
- plugin/lib/fmcli.py
- plugin/lib/fmcore.py
- plugin/lib/fmexam.py
- plugin/lib/fmgenesis.py
- plugin/lib/fmhooks.py
- plugin/lib/fmideas.py
- plugin/lib/fmloop.py
- plugin/lib/fmmap.py
- plugin/lib/fmmission.py
- plugin/lib/fmscout.py
- plugin/skills/brainstorm/SKILL.md
- plugin/skills/brainstorm/references/ideas-prompt.md
- plugin/skills/genesis/SKILL.md
- plugin/templates/genesis.md
- plugin/tests/run.py
- plugin/tests/test_exam.py
- plugin/tests/test_genesis.py
- plugin/tests/test_ideas.py
- plugin/tests/test_loop.py
