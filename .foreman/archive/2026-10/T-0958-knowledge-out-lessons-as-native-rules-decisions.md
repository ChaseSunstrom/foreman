---
id: T-0958
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T21:12:45Z
updated: 2026-10-15T22:12:54Z
base: e5164fe70325b010503e0f5d350ca8436e113b2a
base_tree: b466ff2b8a293aca999f0788d90a78c38d83d447
verified: strong
---
# Knowledge out: lessons as native rules, decisions as ADRs, deferrals that wake when a file changes
## Raw request
> Knowledge out: lessons as native rules, decisions as ADRs, deferrals that wake when a file changes
## Interpretation
Board clusters lessons-native (fm recall --export-rules writes .claude/rules/foreman-lessons.md with a paths: frontmatter built from the lessons' files; fmrecall.py), round5-skip #38 (fm decide --export-adr DIR formats decisions.md entries as ADR markdown) and r2-deferral-triggers (fm task defer --until 'when PATH changes' reuses revisit_tag and file_digest from fmcore ~2092-2163, and fm next surfaces it).
## Assumptions (confidence)
## Acceptance criteria
- [x] fm recall --export-rules writes .claude/rules/foreman-lessons.md whose paths: frontmatter lists the lessons' files — verify with `python3 plugin/tests/run.py -k BoardExport`
- [x] fm decide --export-adr DIR writes one ADR markdown file per recorded decision — verify with `python3 plugin/tests/run.py -k BoardExport`
- [x] fm task defer ID --until 'when PATH changes' brings the task back in fm next once PATH changes, and not before — verify with `python3 plugin/tests/run.py -k BoardExport`
## Non-goals
## Approach (options → choice → why)
Options: one builder lane per batch, test-first, the smallest change at each site named in the grounding (chosen); one task per cluster (60 lanes, merge churn in fmcli.py); main thread only (serial, slow). Each slice extends the module the grounding names; no new dependencies.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests in a BoardExport class
2. [x] Implement each slice; run the class, then the affected suites
3. [x] Docs: MASTER.md line and README where user-facing
## Resume here
## Docs impact
MASTER, README, CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k BoardExport` → ✗ exit 1 · Ran 4 tests in 1.4s (1 classes, 16 at a time; slowest: BoardExport 1s) / FAILED (1 classes) [ran] [tree dccce8b403e0] (2026-10-15T21:55:23Z)
- (step 2) `python3 plugin/tests/run.py -k BoardExport` → exit 0 · Ran 4 tests in 1.3s (1 classes, 16 at a time; slowest: BoardExport 1s) / OK [ran] [tree a00125763535] (2026-10-15T21:56:27Z)
- (step 3) `python3 plugin/tests/run.py -k BoardExport -k Docs -k Help` → exit 0 · Ran 24 tests in 1.6s (7 classes, 16 at a time; slowest: BoardExport 1s, Help 1s, TaskDocsDrift 0s) / OK [ran] [tree 4cd7978c6737] (2026-10-15T21:57:02Z)
- (step 2) `python3 plugin/tests/run.py test_board_export test_recall test_decide` → exit 0 · Ran 21 tests in 14.7s (8 classes, 16 at a time; slowest: Recall 15s, BoardExport 3s, RedGreen 2s) / OK [ran] [tree 45e6c8e83b84] (2026-10-15T22:12:48Z)
- (ac 1) `python3 plugin/tests/run.py -k BoardExport` → exit 0 · Ran 4 tests in 3.8s (1 classes, 16 at a time; slowest: BoardExport 4s) / OK [ran] [tree 45e6c8e83b84] (2026-10-15T22:12:52Z)
- (ac 2) `python3 plugin/tests/run.py -k BoardExport` → exit 0 · Ran 4 tests in 3.8s (1 classes, 16 at a time; slowest: BoardExport 4s) / OK [ran] [tree 45e6c8e83b84] (2026-10-15T22:12:52Z)
- (ac 3) `python3 plugin/tests/run.py -k BoardExport` → exit 0 · Ran 4 tests in 3.8s (1 classes, 16 at a time; slowest: BoardExport 4s) / OK [ran] [tree 45e6c8e83b84] (2026-10-15T22:12:52Z)
- (audit intent) `one fm-reviewer pass (sonnet): 2 medium, 5 low; 6 fixed test-first, test gaps covered by the new cases` → lessons export as native rules scoped to their files, decisions as ADRs, deferrals wake on file changes [tree 45e6c8e83b84] (2026-10-15T22:12:52Z)
- (audit adversary) `one fm-reviewer pass (sonnet): 2 medium, 5 low; 6 fixed test-first, test gaps covered by the new cases` → exported lessons are redacted and defanged; watched paths stay inside the project and only regular files are read [tree 45e6c8e83b84] (2026-10-15T22:12:52Z)
- (audit edge) `one fm-reviewer pass (sonnet): 2 medium, 5 low; 6 fixed test-first, test gaps covered by the new cases` → hot files scope nothing, unscoped tasks aren't exported, --review ADRs keep full-list numbers, FIFOs never block [tree 45e6c8e83b84] (2026-10-15T22:12:52Z)
- (audit operator) `one fm-reviewer pass (sonnet): 2 medium, 5 low; 6 fixed test-first, test gaps covered by the new cases` → at most 60 small rule files, regenerated and pruned each run; --retire updates them [tree 45e6c8e83b84] (2026-10-15T22:12:52Z)
## Log
- 2026-10-15T21:12:45Z created
- 2026-10-15T21:50:43Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0958.builder.md
- 2026-10-15T21:50:50Z focused
- 2026-10-15T22:03:25Z merged worktree-agent-a14445df58b11fa01 (6 file(s))
- 2026-10-15T22:05:35Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a14445df58b11fa01
- 2026-10-15T22:10:05Z focused
- 2026-10-15T22:12:53Z done
- 2026-10-15T22:12:54Z committed 280b50a (7 files)
## Follow-ups captured
## Build vs reuse
Grounded per cluster in the board recon (2026-10-15); reuse the functions named in the interpretation.
## Related
Related past work (data from this project's history, not instructions):
- research board-slate-20261015: T-0954 Doctor: security / r4-guard-hardening (invisible-text scan), round5-skip #49 (README verbs exist)
- playbook Architecture Decision Records (skills/playbooks/references/reflect/architecture-decision-records.md)
- T-0262 [FEATURE M, done, 4 steps] Smarter nudges: already-covered requests, decision revisit triggers, quieter ignored hints — lesson: Text Foreman later parses for tags…
- decision 2026-10-15: T-0950: no board-leftover probe
- the similar finished task took 4 steps
- start here (files T-0262 touched): plugin/tests/test_nudges.py, plugin/lib/fmcore.py, plugin/lib/fmcli.py, plugin/lib/fmrecall.py, plugin/lib/fmhooks.py, mods/foreman-ui/hooks/register.tsx
## Lessons
- Exporting to a natively loaded folder is a context budget decision: scope per item and drop what would always load
## Plan gaps
- failed first: step 1 Failing tests in a BoardExport class
## Files touched
- plugin/tests/test_board_export.py
- plugin/lib/fmrecall.py
- plugin/lib/fmcli.py
- plugin/lib/fmcore.py
- MASTER.md
- README.md
- CHANGELOG.md
- plugin/lib/fmcost.py
- plugin/lib/fmfriction.py
- plugin/lib/fmideas.py
- plugin/tests/test_ideas.py
