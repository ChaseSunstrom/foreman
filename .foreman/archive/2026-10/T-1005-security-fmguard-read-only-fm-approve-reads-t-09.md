---
id: T-1005
type: SECURITY
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-16T00:55:19Z
updated: 2026-10-16T01:02:04Z
base: 5596cf950afda1eb9fcfc0b586739e0fd8dfdbfc
base_tree: 309363f79c2b333e869ca15577404be6c0e703df
verified: strong
---
# fm approve-reads: exec-capable and abbreviated flags are not reads
## Raw request
> SECURITY: fmguard.read_only (fm approve-reads, T-0974) passes exec-capable flags: git grep -O<cmd>/--open-files-in-pager, sort --compress-program, rg --hostname-bin/-z/--pre-glob; make each program's flags fail closed (unknown long options are not reads) and add these to the refusal fixtures
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] read_only refuses git grep -O<cmd>/--open-files-in-pager, git --ext-diff/--textconv, sort --compress-program and its GNU abbreviation (--comp=), sort -uo clustered/attached -oFILE, rg --hostname-bin/--pre-glob/-z, tree -oFILE; every READS case still passes — verify with `python3 plugin/tests/run.py test_approve_reads`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test: the bypass commands in NOT_READS
2. [x] read_only: a bad short flag in any single-dash cluster, a long option that abbreviates a bad one, per-program exec flags; git's exec flags
3. [x] docs: CHANGELOG line
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_approve_reads` → exit 0 · Ran 3 tests in 1.3s (1 classes, 16 at a time; slowest: ApproveReads 1s) / OK [ran] [tree 79aea3937a2a] (2026-10-16T00:56:49Z)
- (step 2) `python3 plugin/tests/run.py test_approve_reads` → exit 0 · Ran 3 tests in 1.3s (1 classes, 16 at a time; slowest: ApproveReads 1s) / OK [ran] [tree 79aea3937a2a] (2026-10-16T00:56:51Z)
- (step 1) `python3 plugin/tests/run.py test_approve_reads` → ✗ exit 1 · Ran 3 tests in 0.8s (1 classes, 16 at a time; slowest: ApproveReads 1s) / FAILED (1 classes) [ran] [tree 03294d08d0ad] (2026-10-16T01:00:49Z)
- (step 2) `python3 plugin/tests/run.py test_approve_reads` → ✗ exit 1 · Ran 3 tests in 0.8s (1 classes, 16 at a time; slowest: ApproveReads 1s) / FAILED (1 classes) [ran] [tree d68fa81495a8] (2026-10-16T01:01:02Z)
- (step 2) `python3 plugin/tests/run.py test_approve_reads` → exit 0 · Ran 3 tests in 0.8s (1 classes, 16 at a time; slowest: ApproveReads 1s) / OK [ran] [tree f68f3bb58079] (2026-10-16T01:01:12Z)
- (ac 1) `python3 plugin/tests/run.py test_approve_reads` → exit 0 · Ran 3 tests in 0.8s (1 classes, 16 at a time; slowest: ApproveReads 1s) / OK [ran] [tree f68f3bb58079] (2026-10-16T01:01:13Z)
- (step 3) `grep -q 'T-1005' CHANGELOG.md` → exit 0 · (no output) [ran] [tree 758fb56f326e] (2026-10-16T01:01:57Z)
- (audit adversary) `self` → probed: GNU abbreviations (--comp=, --out=, --se=), clusters (-uo, -oFILE, -nOcat, -qf), '--' before find's actions, uniq IN OUT, file -C, tree -R -H, git -c/--no-pager/GIT_PAGER= (refused as sub or assignment), --output-indicator-new (harmless, passes): all refused or harmless; git's default textconv in a hostile repo stays the accepted risk from T-0974 [tree 758fb56f326e] (2026-10-16T01:01:57Z)
- (audit intent) `self` → the criterion's bypasses plus the reviewer's (find --) and three write paths found in grounding; READS all pass [tree 758fb56f326e] (2026-10-16T01:01:57Z)
- (ac 1) `python3 plugin/tests/run.py test_approve_reads` → exit 0 · Ran 3 tests in 0.8s (1 classes, 16 at a time; slowest: ApproveReads 1s) / OK [ran] [tree 758fb56f326e] (2026-10-16T01:02:03Z)
- (audit adversary) `builder branch reviewed line by line; merged; reviewer's find -- bypass and three write paths closed test-first; guard suites green` → abbreviations, clusters, '--', uniq IN OUT, file -C, tree -R refused; textconv in a hostile repo remains the accepted T-0974 risk [tree 758fb56f326e] (2026-10-16T01:02:03Z)
- (audit edge) `builder branch reviewed line by line; merged; reviewer's find -- bypass and three write paths closed test-first; guard suites green` → fail-closed false positives (git status -uno, date -Iseconds, uniq -f 1 a) get Claude Code's own dialog [tree 758fb56f326e] (2026-10-16T01:02:03Z)
- (audit self) `builder branch reviewed line by line; merged; reviewer's find -- bypass and three write paths closed test-first; guard suites green` → no findings [tree 758fb56f326e] (2026-10-16T01:02:03Z)
## Log
- 2026-10-16T00:55:19Z created
- 2026-10-16T00:55:41Z planned from capture
- 2026-10-16T00:55:41Z plan: GNU getopt takes unambiguous long-option abbreviations (sort --out=x is --output) and clustered/attached short options (sort -uoFILE); check a bad short flag anywhere in a single-dash cluster, and a long option any bad long option starts with (len>=4); git: -O*/--open-files-in-pager*, --ext-diff, --textconv; rg: --pre* (covers --pre-glob), --hostname-bin*, -z/--search-zip
- 2026-10-16T00:55:46Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1005.builder.md
- 2026-10-16T00:55:53Z focused
- 2026-10-16T01:00:40Z merged worktree-agent-aaf69eb5167130fac (2 file(s))
- 2026-10-16T01:00:40Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aaf69eb5167130fac
- 2026-10-16T01:00:40Z focused
- 2026-10-16T01:02:03Z done
- 2026-10-16T01:02:04Z committed e62fc86 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0269-review-2: Verdict:** changes needed. I read the code only and ran nothing, so each "not blocked" below comes from tracing the code and is unexecuted.
- T-0668 [SECURITY S, done, 2 steps] Guard: computed-name rm reading accepts rm's abbreviated long options and stops at the first operand — lesson: getopt_long takes uniqu…
- research T-0270-review-1: Verdict: changes needed.** The new code has one regression and several ways around it. I read the code only. I could not run commands, so every…
- decision 2026-10-03: Self-approve T-0175 (L, guard): approach A
- the similar finished task took 2 steps
- start here (files T-0668 touched): plugin/tests/test_guard_pipes.py, plugin/lib/fmguard.py, CHANGELOG.md
## Files touched
- plugin/tests/test_approve_reads.py
- plugin/lib/fmguard.py
- CHANGELOG.md
