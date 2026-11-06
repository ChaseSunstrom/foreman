---
id: T-1396
type: SECURITY
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-21T17:28:43Z
updated: 2026-10-21T19:16:16Z
base: c5543f01eb96bd4805932ea3db154d03a3eb6134
base_tree: c91e26bd60c098f031fd6e5a0f7e9f58b865abbc
plan0_at: 2026-10-21T17:33:20Z
plan0_scope: []
verified: strong
---
# Hostile skills and plugins can't get past the indexer: a 25+ item corpus quarantined with reasons, the Agent Skills spec checked, over-broad descriptions held out of search, and a marketplace read that survives bad entries and treats a rename as new
## Raw request
> SECURITY: Hostile-asset corpus and lints: 25+ bad skills and plugins through the indexer, each quarantined with a reason; SKILL.md frontmatter checked to the Agent Skills spec (name pattern and length, description length); over-broad descriptions held out of search; fm plugins reads a marketplace with a bad entry, and a renamed or re-sourced plugin reads as new (S9, A6 A4 B7)
> CONTEXT: round 2 of the fm/fm code brainstorm (T-1382): research/brainstorm-fm-anthropic-catalogue.md, grounding with file:line in research/brainstorm-fm-anthropic-half-a.md (A*) and half-b.md (B*)
> DONE-WHEN: the corpus test quarantines every item with a reason; a marketplace fixture with one non-dict entry loads the rest; a renamed plugin shows untrusted; fm doctor fails a skill whose name breaks the spec
## Interpretation
Round 2 brings six third-party repos into fm lib and fm plugins. Their files are data, but the indexer, the doctor's skill check and the marketplace reader must hold against hostile or malformed ones: a non-dict marketplace entry crashes fmplugins.index today (fmplugins.py:113-126) and renames are never read.
## Assumptions (confidence)
## Acceptance criteria
- [x] every corpus item is quarantined or marked with a reason and nothing crashes; a marketplace with one non-dict entry loads the rest; a renamed or re-sourced plugin reads as untrusted; fm doctor fails a skill whose name breaks the spec and passes Foreman's own — verify with `python3 plugin/tests/run.py test_lib_hostile test_doctor`
- [x] every finding in research T-1396-review except old-index re-marking has a test that fails before its fix and passes after — verify with `python3 plugin/tests/run.py test_lib_hostile test_doctor`
## Non-goals
## Approach (options → choice → why)
Options: (A) a checked-in corpus of bad assets (symlink escapes, oversized and control-character frontmatter, name/folder mismatch, 'use for every task' descriptions, YAML bombs, non-dict marketplace entries, a renamed or re-sourced plugin) run through fmlib's indexer, fmplugins.index and the doctor, each expected outcome named (chosen: one test file, every rule pinned); (B) fuzz only (finds crashes, not policy); (C) trust the source's reputation (no). The spec check (name pattern ^[a-z0-9]+(-[a-z0-9]+)*$ up to 64 and matching its folder, description 1-1024) is shared by the doctor and the indexer; an over-broad description is indexed but marked and left out of fm lib search.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: the corpus, the bad marketplace entry, the rename, the spec check
2. [x] Shared spec check; tolerant marketplace read keyed on name+source+sha; over-broad mark; docs
3. [x] fix the review's findings test-first (research T-1396-review): record_trust only on a fresh install or when the ledger has no entry or the same identity; NUL source and RecursionError skip the entry with a reason; _marketplaces validates like index(); duplicate-name pass counts only unquarantined rows as first; root SKILL.md uses the source name; the 1,024-char cap for skills only; ls-tree -z; symlink rows only for SKILL.md and agents/*.md; CRLF frontmatter normalised. BROAD: NFKC-fold before matching and widen the phrases a little, keeping the ponytail ceiling note
## Resume here
## Docs impact
CHANGELOG line (T-1396 entry); README's fm lib source line: none, the CHANGELOG names quarantine
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_lib_hostile test_doctor` → ✗ exit 1 · Ran 58 tests in 57.1s (20 classes, 16 at a time; slowest: Command 56s, ViewsRepair 36s, Checks 2s) / FAILED (3 classes) [ran] [tree a8b2dd785b47] (2026-10-21T17:41:31Z)
- (step 2) `python3 plugin/tests/run.py test_lib_hostile test_doctor` → ✗ exit 1 · Ran 58 tests in 91.2s (20 classes, 16 at a time; slowest: Command 91s, ViewsRepair 32s, HostileCorpus 10s) / FAILED (2 classes) [ran] [tree e0bfcb705f6c] (2026-10-21T17:53:10Z)
- (step 3) `python3 plugin/tests/run.py test_lib_hostile test_doctor` → ✗ exit 1 · Ran 61 tests in 89.3s (20 classes, 16 at a time; slowest: Command 89s, ViewsRepair 32s, HostileCorpus 12s) / FAILED (3 classes) [ran] [tree a99f8f8b3eea] (2026-10-21T18:47:29Z)
- (step 3) `python3 plugin/tests/run.py test_lib_hostile test_library test_plugins` → exit 0 · Ran 50 tests in 4.9s (13 classes, 16 at a time; slowest: LibraryAdmit 5s, HostileCorpus 4s, Install 4s) / OK [ran] [tree 429184b6c61d] (2026-10-21T19:12:09Z)
- (audit adversary) `fm-reviewer` → 4 MEDIUM found (enable re-trusted a re-sourced plugin; NUL source and RecursionError crashed index; _marketplaces crashed on odd names; BROAD phrase bypasses) plus LOW ls-tree quoting; all fixed test-first in step 3 (test_lib_hostile), BROAD now folds Unicode before matching (ceiling kept as a ponytail note) [tree 429184b6c61d] (2026-10-21T19:13:09Z)
- (step 1) `python3 plugin/tests/run.py test_lib_hostile test_doctor` → exit 0 · Ran 61 tests in 50.2s (20 classes, 16 at a time; slowest: Command 50s, ViewsRepair 37s, HostileCorpus 4s) / OK [ran] [tree 429184b6c61d] (2026-10-21T19:14:04Z)
- (step 2) `python3 plugin/tests/run.py test_lib_hostile test_doctor` → exit 0 · Ran 61 tests in 45.2s (20 classes, 16 at a time; slowest: Command 45s, ViewsRepair 31s, HostileCorpus 5s) / OK [ran] [tree 429184b6c61d] (2026-10-21T19:14:50Z)
- (ac 1) `python3 plugin/tests/run.py test_lib_hostile test_doctor` → exit 0 · Ran 61 tests in 52.4s (20 classes, 16 at a time; slowest: Command 52s, ViewsRepair 38s, HostileCorpus 5s) / OK [ran] [tree 429184b6c61d] (2026-10-21T19:15:51Z)
- (ac 2) `python3 plugin/tests/run.py test_lib_hostile test_doctor` → exit 0 · Ran 61 tests in 52.4s (20 classes, 16 at a time; slowest: Command 52s, ViewsRepair 38s, HostileCorpus 5s) / OK [ran] [tree 429184b6c61d] (2026-10-21T19:15:51Z)
- (audit intent) `fm-reviewer (research T-1396-review): 11 findings, 10 fixed with failing-first tests; CRLF did not reproduce (text mode normalises) and stays pinned; old indexes captured as T-1415` → every corpus item quarantined with a reason, a marketplace with bad entries loads the rest, renamed/re-sourced plugins read untrusted, fm doctor fails a spec-breaking skill and passes Foreman's own (test_lib_hostile, test_doctor green on the merged tree) [tree 429184b6c61d] (2026-10-21T19:15:51Z)
- (audit edge) `fm-reviewer (research T-1396-review): 11 findings, 10 fixed with failing-first tests; CRLF did not reproduce (text mode normalises) and stays pinned; old indexes captured as T-1415` → root SKILL.md checked against the source name; agents keep long descriptions; a clean skill isn't squatted by a quarantined one; symlink rows only for SKILL.md, skills/<x>, agents/*.md [tree 429184b6c61d] (2026-10-21T19:15:51Z)
## Log
- 2026-10-21T17:28:43Z created
- 2026-10-21T17:32:47Z planned from capture
- 2026-10-21T17:32:51Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1396.builder.md
- 2026-10-21T17:33:18Z focused
- 2026-10-21T18:19:15Z merged worktree-agent-ade0228ed0d3f469e (9 file(s))
- 2026-10-21T18:24:19Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ade0228ed0d3f469e
- 2026-10-21T18:35:27Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1396.builder.md
- 2026-10-21T18:35:45Z focused
- 2026-10-21T19:11:56Z merged worktree-agent-aafafb0d45957304d (5 file(s))
- 2026-10-21T19:11:57Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aafafb0d45957304d
- 2026-10-21T19:12:02Z focused
- 2026-10-21T19:16:16Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-fm-anthropic-catalogue: Source: research/brainstorm-20261021-120257 (fm ideas, 10 lenses, 4 rounds, 3 deepened, --seen every earlier ideas.md: 520 ne…
- research brainstorm-fm-anthropic-half-a: Grounded against `plugin/lib` at HEAD (branch foreman/build; fmcli.py and test_cli.py have uncommitted edits).
- research brainstorm-fm-anthropic-half-b: Reading used.** I took all 250 bullets of rounds 1 to 4 in lenses 01, 02, 03, 08 and 09. Four titles occur twice (themes, ETA, g…
- decision 2026-10-20: T-1300 slate: round 1 = C1 renderer, C2 motion engine, C3 live track, C4 gradients/contrast/focal line, C5 event flashes, C7 odometer/sparklines, C2…
## Why not caught
the first build tested hostile content but not malformed shapes; the reviewer's adversary lens found them
## Lessons
- A quarantine check must survive its own bad inputs: each validator gets the malformed-shape corpus (NUL, deep nesting, wrong types) not just the hostile-content one
## Plan gaps
- added late: fix the review's findings test-first (research T-1396-review): record_trust only on a fresh install or when the ledger …
- failed first: step 1 Failing tests: the corpus, the bad marketplace entry, the rename, the spec check
- failed first: step 2 Shared spec check; tolerant marketplace read keyed on name+source+sha; over-broad mark; docs
- failed first: step 3 fix the review's findings test-first (research T-1396-review): record_trust only on a fresh install…
## Files touched
- plugin/tests/fixtures/hostile/corpus.json
- plugin/tests/fixtures/hostile/marketplace.json
- plugin/tests/test_lib_hostile.py
- plugin/tests/test_doctor.py
- plugin/tests/test_library.py
- plugin/lib/fmplugins.py
- plugin/lib/fmlib.py
- plugin/lib/fmdoctor.py
- MASTER.md
