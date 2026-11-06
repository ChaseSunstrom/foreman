---
id: T-0428
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-09T14:05:43Z
updated: 2026-10-09T14:12:02Z
base: df9d352930915cf2cdde0429368def670e699d6e
base_tree: c91ec4130a62a0b43431262f5d8b02ea743c0e49
verified: strong
---
# Builders leave CHANGELOG.md to the main thread
## Raw request
> FIX: a builder's CHANGELOG line can land in a released section: with merge=union (T-0427) the T-0414 lane's 'Unreleased' line merged under '## 1.2.14' because the main line released between the lane's start and its merge. Builders shouldn't edit CHANGELOG.md: the lane CONTRACT (fmlanes.py) should say to put the changelog line in the final report, and the main thread adds it at finish
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the lane brief's contract says not to edit CHANGELOG.md and to give the line in the final report — verify with `python3 plugin/tests/run.py -k test_brief_leaves_the_changelog_to_the_main_thread`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first, then one CONTRACT line in fmlanes.py
## Resume here
## Docs impact
CHANGELOG entry
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_brief_leaves_the_changelog_to_the_main_thread` → ✗ exit 1 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: Brief 0s) / FAILED (1 classes) [ran] [tree 4995c9df8b34] (2026-10-09T14:08:16Z)
- (step 1) `python3 plugin/tests/run.py -k test_brief_leaves_the_changelog_to_the_main_thread` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Brief 0s) / OK [ran] [tree b874a63879b7] (2026-10-09T14:08:22Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (29 pass, 3 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                54.0    81.0     150  [0] / SessionEnd                  49.1    71.6     150  [0] (slower: 19.1 s vs a usual 11.5 s); claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 13:13 UTC; python3 plugin/tests [ran] [tree b874a63879b7] (2026-10-09T14:11:24Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed on this tree (run at 14:11 UTC) [ran] [tree b874a63879b7] (2026-10-09T14:11:30Z)
- (ac 1) `python3 plugin/tests/run.py -k test_brief_leaves_the_changelog_to_the_main_thread` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Brief 0s) / OK [ran] [tree e0ea593c021e] (2026-10-09T14:11:54Z)
- (audit edge) `builder branch read (one CONTRACT line + its test); red→green recorded by the builder; merged; criterion rerun OK` → a builder that still edits CHANGELOG merges as a union; the main thread checks placement at finish [tree e0ea593c021e] (2026-10-09T14:11:54Z)
- (audit self) `builder branch read (one CONTRACT line + its test); red→green recorded by the builder; merged; criterion rerun OK` → no findings [tree e0ea593c021e] (2026-10-09T14:11:54Z)
- (audit adversary) `builder branch read (one CONTRACT line + its test); red→green recorded by the builder; merged; criterion rerun OK` → one instruction line in the lane brief; the guard files in its diff range are T-0414/T-0421/T-0422's, adversary-reviewed there [tree e0ea593c021e] (2026-10-09T14:12:02Z)
- (audit edge) `builder branch read (one CONTRACT line + its test); red→green recorded by the builder; merged; criterion rerun OK` → a builder that still edits CHANGELOG merges as a union; the main thread checks placement at finish [tree e0ea593c021e] (2026-10-09T14:12:02Z)
- (audit self) `builder branch read (one CONTRACT line + its test); red→green recorded by the builder; merged; criterion rerun OK` → no findings [tree e0ea593c021e] (2026-10-09T14:12:02Z)
## Log
- 2026-10-09T14:05:43Z created
- 2026-10-09T14:06:05Z planned from capture
- 2026-10-09T14:06:46Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0428.builder.md
- 2026-10-09T14:08:08Z focused
- 2026-10-09T14:11:44Z merged worktree-agent-a5e2d037438f8745c (2 file(s))
- 2026-10-09T14:11:44Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a5e2d037438f8745c
- 2026-10-09T14:11:54Z focused
- 2026-10-09T14:12:01Z paused: focus moved to T-0423
- 2026-10-09T14:12:01Z focused
- 2026-10-09T14:12:02Z done
- 2026-10-09T14:12:02Z committed b58bad0 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0234-review-1: Verdict: changes needed.** One MEDIUM that can delete a branch `remove()` shouldn't, and one MEDIUM where the contract's "never close" is prose…
- T-0379 [FIX S, done, 1 steps] Builder brief: start from the main checkout's commit; isolation refusals are reported for the main thread, not retried — lesson: Watch the …
- T-0234 [FEATURE L, done, 4 steps] Implementation subagents in lane worktrees — a foreman:fm-builder agent (Edit/Write/Bash) — lesson: A contract a subagent must keep nee…
- decision 2026-09-26: Released: fast-forwarded main 924fe06 → bd86fd6 (43 commits: T-0018 rounds 1-10, T-0036, T-0038, T-0039) and pushed main + foreman/build to origin
## Lessons
- Shared files that every task touches belong to the integrator, not the lanes.
## Files touched
- .claude/worktrees/agent-a5e2d037438f8745c/plugin/tests/test_builder.py
- .claude/worktrees/agent-a5e2d037438f8745c/plugin/lib/fmlanes.py
- .claude-plugin/marketplace.json
- CHANGELOG.md
- plugin/.claude-plugin/plugin.json
- plugin/lib/fmguard.py
- plugin/lib/fmhooks.py
- plugin/lib/fmlanes.py
- plugin/tests/test_builder.py
- plugin/tests/test_guard.py
- plugin/tests/test_guard_diff.py
- plugin/tests/test_guard_pipes.py
- plugin/tests/test_hooks.py
