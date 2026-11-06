---
id: T-2243
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-31T00:26:08Z
updated: 2026-10-31T00:45:52Z
base: fcfb2e78586fba67e25e7bee4548611b1d1fc732
base_tree: fa96709da4f5d7b33564826f81709bc3342fc7ce
plan0_at: 2026-10-31T00:27:12Z
plan0_scope: []
verified: strong
---
# fm genesis put: judge a long narrative tower file section by section (one cold read per…
## Raw request
> fm genesis put: judge a long narrative tower file section by section (one cold read per ## section, each with its own acceptance and previous reads, the file filed when every section passes), so objections can't rotate across the whole file; evidence: Mission 3's critique failed 13 puts (1-6 new flags each, some reversing earlier ones) after T-2207/T-2228/T-2231/T-2236
## Interpretation
fm genesis put reads a whole tower file in one cold read. On long narrative files (critiques, missions) each read rotates 1-6 new objections across lines earlier reads passed, so Mission 3's critique failed 13 puts even after per-line acceptance (T-2207), re-keyed findings (T-2228), paragraph joins (T-2231) and multi-line quotes (T-2236). Judge such files one ## section at a time, each with its own acceptance and previous reads, filing the file when every section's read passes.
## Assumptions (confidence)
## Acceptance criteria
- [x] a long narrative tower file is read one ## section at a time: an unchanged section that passed isn't re-read, a changed or failing one is, and the file is filed only when every section passes — verify with `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisRead.test_a_long_file_is_read_by_section_and_a_passed_unchanged_section_isnt_read_again`
## Non-goals
## Approach (options → choice → why)
Options: (1) one cold read per ## section, each section's text plus a one-line outline of the others for context, keyed in genesis-reads.json and genesis-accepted.json as 'name#heading'; an unchanged section that passed keeps its pass and isn't re-read, so a put re-reads only changed or failing sections; (2) majority of 2 whole-file reads (decided against on 2026-10-30, keeps rotation); (3) a fixed checklist per tower kind (loses the open read for gaming). Choice 1: rotation can only touch the sections that changed, and a passed section stays passed while its text, the charter and the exam tail are unchanged. Files under a size floor (coverage.md's bullets, seed tables) keep the whole-file read.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test in GenesisRead with a stub reader counting reads per section
2. [x] _read splits on ## sections past a size floor, keys reads and acceptance by name#heading, skips unchanged passed sections
3. [x] docs (MASTER fmgenesis, CHANGELOG), adversary + edge review
## Resume here
## Docs impact
MASTER.md fmgenesis entry, CHANGELOG Unreleased
## Verification evidence
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisRead.test_a_long_file_is_read_by_section_and_a_passed_unchanged_section_isnt_read_again 2>&1 | tail -8` → ✗ exit 1 · Ran 1 test in 0.271s / FAILED (failures=1) [ran] [tree 8789892c84aa] (2026-10-31T00:27:42Z)
- (step 2) `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisRead` → exit 0 · Ran 12 tests in 4.370s / OK [ran] [tree 43434c84669c] (2026-10-31T00:30:43Z)
- (step 3) `cd plugin/tests && python3 -m unittest -q test_genesis 2>&1 | grep -vE "Warning|cur = open|^$" | tail -30` → exit 0 · Ran 110 tests in 65.995s / OK [ran] [tree ff68edf4b8bd] (2026-10-31T00:37:23Z)
- `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisRead.test_a_long_file_is_read_by_section_and_a_passed_unchanged_section_isnt_read_again` → ✗ exit 1 · Ran 1 test in 0.270s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree ff1de891febb] (2026-10-31T00:41:17Z)
- `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisRead.test_a_long_file_is_read_by_section_and_a_passed_unchanged_section_isnt_read_again` → exit 0 · Ran 1 test in 0.419s / OK [ran] [tree ff1de891febb] (2026-10-31T00:41:17Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisRead.test_a_long_file_is_read_by_section_and_a_passed_unchanged_section_isnt_read_again` → exit 0 · Ran 1 test in 0.422s / OK [ran] [tree ff1de891febb] (2026-10-31T00:41:44Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisRead` → exit 0 · Ran 15 tests in 5.489s / OK [ran] [tree ff1de891febb] (2026-10-31T00:41:49Z)
- (step 2) `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisRead` → exit 0 · Ran 15 tests in 5.463s / OK [ran] [tree ff1de891febb] (2026-10-31T00:41:55Z)
- (step 3) `grep -q 'T-2243' MASTER.md && grep -q 'one section at a time' CHANGELOG.md` → exit 0 · (no output) [ran] [tree 5f7018374dd7] (2026-10-31T00:41:55Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisRead.test_a_long_file_is_read_by_section_and_a_passed_unchanged_section_isnt_read_again` → exit 0 · Ran 1 test in 0.429s / OK [ran] [tree 5f7018374dd7] (2026-10-31T00:41:57Z)
- (audit intent) `fm-reviewer adversary+edge on the builder's branch: 1 HIGH (a heading in the prompt's file-name attribute could close the data fence) and 6 MEDIUM/LOW (headings-only skip, renames dropping findings, cross-section contradictions, advisory passes stored, unbounded cost, duplicate keys) fixed in 369af8cc; HIGH verified here (keys are hashes); test_genesis 110 green` → a long narrative tower file is judged section by section and converges, the rest of the cold read unchanged [tree 5f7018374dd7] (2026-10-31T00:41:57Z)
- (audit adversary) `fm-reviewer adversary+edge on the builder's branch: 1 HIGH (a heading in the prompt's file-name attribute could close the data fence) and 6 MEDIUM/LOW (headings-only skip, renames dropping findings, cross-section contradictions, advisory passes stored, unbounded cost, duplicate keys) fixed in 369af8cc; HIGH verified here (keys are hashes); test_genesis 110 green` → no heading text reaches the prompt's attribute; renames keep earlier findings; a cross-section claim is visible through the outline's first lines [tree 5f7018374dd7] (2026-10-31T00:41:57Z)
- (audit edge) `fm-reviewer adversary+edge on the builder's branch: 1 HIGH (a heading in the prompt's file-name attribute could close the data fence) and 6 MEDIUM/LOW (headings-only skip, renames dropping findings, cross-section contradictions, advisory passes stored, unbounded cost, duplicate keys) fixed in 369af8cc; HIGH verified here (keys are hashes); test_genesis 110 green` → short sections merge, at most 12 reads a put, an advisory pass is re-read, orphan keys pruned on a pass [tree 5f7018374dd7] (2026-10-31T00:41:57Z)
## Log
- 2026-10-31T00:26:08Z created
- 2026-10-31T00:26:55Z planned: it has criteria and steps
- 2026-10-31T00:26:55Z set tier=M, approved=True
- 2026-10-31T00:26:55Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2243.builder.md
- 2026-10-31T00:27:11Z focused
- 2026-10-31T00:41:15Z merged worktree-agent-a2148037eb654f563 (2 file(s))
- 2026-10-31T00:41:15Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a2148037eb654f563
- 2026-10-31T00:41:15Z focused
- 2026-10-31T00:42:17Z done
- 2026-10-31T00:43:00Z guard authorization added: publish
- 2026-10-31T00:45:52Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2205 [FIX M, done, 2 steps] fm genesis put's cold read doesn't converge on long tower files: 13 rounds to file… — lesson: A model judge read from scratch every round d…
- T-2104 [FEATURE M, done, 5 steps] fm genesis drift/sweep — gen-0 MUST/NEVER drift check with a cold read, the §7 sweep in… — lesson: Never write a literal triple backtic…
- T-2166 [FEATURE M, done, 4 steps] Cold read on every tower write: fm genesis put (and the tower's own writers: exam_line,… — lesson: A nondeterministic cold reader finds…
- decision 2026-10-30: Cold reads converge by per-line acceptance (keyed on line text + charter hash), not by majority reads or diff-only reads: every line still gets a wh…
## Lessons
- Splitting a check into parts must keep every part's input fenced and its memory keyed by something the writer can't type
## Files touched
- plugin/tests/test_genesis.py
- plugin/lib/fmgenesis.py
