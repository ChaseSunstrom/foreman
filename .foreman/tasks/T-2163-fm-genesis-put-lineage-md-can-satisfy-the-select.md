---
id: T-2163
type: SECURITY
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-30T14:08:57Z
updated: 2026-10-31T00:33:05Z
base: 1c2445a84d54870339e3e2e96c1d9dcb18dc8acc
base_tree: 11d271d3f93b6615a2e14d6f3ac888701cc8e2b3
plan0_at: 2026-10-31T00:18:16Z
plan0_scope: []
group: ledger-forgery gates on genesis select
verified: strong
---
# fm genesis put lineage.md can satisfy the select stage: step() passes select on a '##…
## Raw request
> fm genesis put lineage.md can satisfy the select stage: step() passes select on a '## gen-N' heading in lineage.md, which put accepts, so a hand-written heading skips selection; make select's own record the gate (T-2155 review, MEDIUM)
## Interpretation
fm genesis step passes the select stage when lineage.md has a '## gen-N' heading, and fm genesis put files lineage.md, so a hand-written heading skips selection (T-2155 review, MEDIUM). Make select's own record the gate: only fm genesis select N moves the step past select.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm genesis step stays on select until fm genesis select N has logged its genesis_select event; a hand-put '## gen-N' lineage heading doesn't pass it — verify with `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisStep.test_a_hand_written_lineage_heading_doesnt_pass_select_only_select_does`
## Non-goals
## Approach (options → choice → why)
Options: (1) select() logs a genesis_select ledger event (gen, verdict, base), and step() passes select only on that event for gen N; (2) gate on select's decisions.md row (rejected: fm decide can write the same words); (3) refuse '## gen-' headings in fm genesis put lineage.md (rejected: blocks only one writer and breaks select's own put). Choice 1: the ledger is hash-chained and only select logs that event. A tower whose select ran before this re-runs fm genesis select N, which rewrites its own lineage section, so nothing is lost.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test in GenesisStep: a put lineage.md with '## gen-1' leaves the step on select; after fm genesis select 1 it moves on
2. [x] select() logs genesis_select; step() gates on it
3. [x] docs (MASTER fmgenesis, CHANGELOG), adversary + edge review
## Resume here
## Docs impact
MASTER.md fmgenesis entry, CHANGELOG Unreleased
## Verification evidence
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisStep.test_a_hand_written_lineage_heading_doesnt_pass_select_only_select_does 2>&1 | tail -6` → ✗ exit 1 · Ran 1 test in 0.089s / FAILED (failures=1) [ran] [tree 963e8e088637] (2026-10-31T00:22:25Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisStep` → exit 0 · Ran 13 tests in 3.054s / OK [ran] [tree 19a00420b2f7] (2026-10-31T00:22:30Z)
- (step 2) `cd plugin/tests && python3 -m unittest -q test_genesis` → exit 0 · Ran 105 tests in 33.243s / OK [ran] [tree 19a00420b2f7] (2026-10-31T00:23:05Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_genesis && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [14.80s] [ran] [tree 19a00420b2f7] (2026-10-31T00:23:27Z)
- (step 3) `cd plugin/tests && python3 -m unittest -q test_genesis 2>&1 | grep -E "^(FAIL|ERROR|Ran|OK)|Error"` → exit 0 · Ran 105 tests in 33.366s / OK [ran] [tree a9ee7f22b653] (2026-10-31T00:27:26Z)
- (step 2) `cd plugin/tests && python3 -m unittest -q test_genesis` → exit 0 · Ran 105 tests in 33.367s / OK [ran] [tree a9ee7f22b653] (2026-10-31T00:28:02Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_genesis && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [11.45s] [ran] [tree a9ee7f22b653] (2026-10-31T00:28:22Z)
- `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisStep.test_a_hand_written_lineage_heading_doesnt_pass_select_only_select_does` → ✗ exit 1 · Ran 1 test in 0.215s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree 2b37311d39f7] (2026-10-31T00:30:55Z)
- `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisStep.test_a_hand_written_lineage_heading_doesnt_pass_select_only_select_does` → exit 0 · Ran 1 test in 0.178s / OK [ran] [tree 2b37311d39f7] (2026-10-31T00:30:55Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisStep.test_a_hand_written_lineage_heading_doesnt_pass_select_only_select_does` → exit 0 · Ran 1 test in 0.218s / OK [ran] [tree 2b37311d39f7] (2026-10-31T00:32:11Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisStep.test_a_hand_written_lineage_heading_doesnt_pass_select_only_select_does` → exit 0 · Ran 1 test in 0.213s / OK [ran] [tree 2b37311d39f7] (2026-10-31T00:32:11Z)
- (step 2) `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisStep.test_a_hand_written_lineage_heading_doesnt_pass_select_only_select_does` → exit 0 · Ran 1 test in 0.181s / OK [ran] [tree 2b37311d39f7] (2026-10-31T00:32:11Z)
- (step 3) `grep -q 'T-2163' MASTER.md && grep -q 'select.md' CHANGELOG.md` → exit 0 · (no output) [ran] [tree fa96709da4f5] (2026-10-31T00:32:12Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_genesis.GenesisStep.test_a_hand_written_lineage_heading_doesnt_pass_select_only_select_does` → exit 0 · Ran 1 test in 0.180s / OK [ran] [tree fa96709da4f5] (2026-10-31T00:32:21Z)
- (audit intent) `fm-reviewer adversary+edge on the builder's branch: 2 MEDIUM (fm log could forge the ledger event; a month's ledger roll lost it) and 1 LOW (a stale health cache) fixed by moving the gate to an owned tower file, gen-N/select.md, in 20a99514; test_genesis 105 green` → only fm genesis select moves the step past select [tree fa96709da4f5] (2026-10-31T00:32:21Z)
- (audit adversary) `fm-reviewer adversary+edge on the builder's branch: 2 MEDIUM (fm log could forge the ledger event; a month's ledger roll lost it) and 1 LOW (a stale health cache) fixed by moving the gate to an owned tower file, gen-N/select.md, in 20a99514; test_genesis 105 green` → a hand-put lineage heading and an fm log genesis_select line both leave the step on select; fm genesis put gen-N/select.md is refused [tree fa96709da4f5] (2026-10-31T00:32:21Z)
- (audit edge) `fm-reviewer adversary+edge on the builder's branch: 2 MEDIUM (fm log could forge the ledger event; a month's ledger roll lost it) and 1 LOW (a stale health cache) fixed by moving the gate to an owned tower file, gen-N/select.md, in 20a99514; test_genesis 105 green` → a ledger roll or a long ledger can't send the step back to select; health()'s cache key covers the tower file [tree fa96709da4f5] (2026-10-31T00:32:21Z)
## Log
- 2026-10-30T14:08:57Z created
- 2026-10-31T00:15:44Z planned: it has criteria and steps
- 2026-10-31T00:15:44Z set type=SECURITY, tier=M
- 2026-10-31T00:18:00Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2163.builder.md
- 2026-10-31T00:18:15Z focused
- 2026-10-31T00:30:53Z merged worktree-agent-ac7300d5bf667b87e (2 file(s))
- 2026-10-31T00:30:53Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ac7300d5bf667b87e
- 2026-10-31T00:30:53Z focused
- 2026-10-31T00:32:44Z done
- 2026-10-31T00:32:46Z committed fcfb2e78 (2 files)
- 2026-10-31T00:33:05Z guard authorization added: publish
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2155 [SECURITY M, done, 3 steps] fm genesis put exam.jsonl can overwrite the exam record that fm genesis select and fm… — lesson: A gate's evidence file must be writab…
- research T-2155-review: Changes needed.** The `exam.jsonl` refusal is correct and tested, but the request's second half, the forged-Verdict case, isn't fixed. [stale: pl…
- T-2102 [FEATURE M, done, 5 steps] fm genesis select/seed — exam-gated selection into lineage.md; the feature writes the… — lesson: c.lock is not reentrant: a lock around…
- decision 2026-10-30: Genesis select: a tie on train scenarios closed reverts to the parent whatever the cost (gen-0 §3.6 verbatim: stays only if it closed more); cost pe…
## Lessons
- A gate must rest on a record only the gated verb can write: a ledger event any verb can append is a claim, an owned file is proof
## Files touched
- plugin/lib/fmgenesis.py
- plugin/tests/test_genesis.py
- CHANGELOG.md
- MASTER.md
