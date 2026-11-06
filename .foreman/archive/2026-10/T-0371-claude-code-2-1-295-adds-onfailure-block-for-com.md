---
id: T-0371
type: SECURITY
tier: S
status: done
priority: normal
scope: [plugin/hooks/hooks.json, plugin/tests/**, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-09T00:01:51Z
updated: 2026-10-09T00:42:36Z
base: 61821ef69b2da43aa6ea38a15ab1aa91e2a62785
base_tree: 3044e8450032b17894914c8737d0d0235dc23da5
verified: strong
---
# Guard hook fails closed in Claude Code itself: onFailure: "block" on the PreToolUse hook (Claude Code ≥2.1.295)
## Raw request
> Claude Code 2.1.295 adds onFailure: "block" for command hooks (a hook that can't start, times out or exits unexpectedly blocks the action): set it on Foreman's PreToolUse guard in hooks.json once the installed Claude Code is ≥2.1.295 (this machine runs 2.1.287), so a crashed or timed-out guard fails closed in Claude Code itself; fm doctor can say when the build supports it
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] hooks.json's PreToolUse hook declares onFailure: block and claude plugin validate passes — verify with `python3 plugin/tests/run.py -k test_the_guard_hook_fails_closed`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first: hooks.json onFailure, validate
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_the_guard_hook_fails_closed` → ✗ exit 1 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: PluginFiles 0s) / FAILED (1 classes) [ran] [tree c8ba56bc8857] (2026-10-09T00:21:45Z)
- (step 1) `python3 plugin/tests/run.py -k test_the_guard_hook_fails_closed` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: PluginFiles 0s) / OK [ran] [tree a83671980a70] (2026-10-09T00:21:50Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 2 of 6 failed: claude plugin test mods/foreman-ui → ✗ exit 1 · 1 fail / Ran 62 tests across 1 file. [3.06s]; fm replay → ✗ exit 1 · 0 newly allowed (possible bypasses) / 2919 new to the corpus · fm replay --accept takes these verdicts as the baseline [ran] [tree a83671980a70] (2026-10-09T00:23:17Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 2 of 6 failed: claude plugin test mods/foreman-ui → ✗ exit 1 · 1 fail / Ran 62 tests across 1 file. [2.95s]; fm replay → ✗ exit 1 · 0 newly allowed (possible bypasses) / 2919 new to the corpus · fm replay --accept takes these verdicts as the baseline [ran] [tree a83671980a70] (2026-10-09T00:23:54Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 2 of 6 failed: claude plugin test mods/foreman-ui → ✗ exit 1 · 1 fail / Ran 62 tests across 1 file. [3.02s]; fm replay → ✗ exit 1 · 0 newly allowed (possible bypasses) / 2919 new to the corpus · fm replay --accept takes these verdicts as the baseline [ran] [tree a83671980a70] (2026-10-09T00:24:43Z)
- (ac 1) `python3 plugin/tests/run.py -k test_the_guard_hook_fails_closed` → exit 0 · Ran 1 tests in 0.1s (1 classes, 16 at a time; slowest: PluginFiles 0s) / OK [ran] [tree bfed826730d6] (2026-10-09T00:42:10Z)
- (audit adversary) `main-thread review of the builder's diff (2 files, 12 lines) before fm lane merge; criteria re-run on the merged tree; claude plugin validate passes` → fail-closed only where the guard decides (PreToolUse); a timeout now blocks, which is the intent; other events stay fail-open so a broken hook can't wedge a session [tree bfed826730d6] (2026-10-09T00:42:10Z)
- (audit operator) `main-thread review of the builder's diff (2 files, 12 lines) before fm lane merge; criteria re-run on the merged tree; claude plugin validate passes` → the 5 s timeout stays; hooks measured ~30 ms here and ~65 ms on loaded JARVIS; the 'fm doctor says when the build supports it' part was left out: validate passes and older builds ignore the key [tree bfed826730d6] (2026-10-09T00:42:10Z)
- (audit self) `main-thread review of the builder's diff (2 files, 12 lines) before fm lane merge; criteria re-run on the merged tree; claude plugin validate passes` → no findings [tree bfed826730d6] (2026-10-09T00:42:10Z)
- (audit adversary) `main-thread review of the builder's diff (2 files, 12 lines) before fm lane merge; criteria re-run on the merged tree; claude plugin validate passes` → fail-closed only where the guard decides (PreToolUse); a timeout now blocks, which is the intent; other events stay fail-open so a broken hook can't wedge a session [tree bfed826730d6] (2026-10-09T00:42:35Z)
- (audit operator) `main-thread review of the builder's diff (2 files, 12 lines) before fm lane merge; criteria re-run on the merged tree; claude plugin validate passes` → the 5 s timeout stays; hooks ~30 ms here and ~65 ms on loaded JARVIS; JARVIS and this machine run 2.1.295 [tree bfed826730d6] (2026-10-09T00:42:35Z)
- (audit self) `main-thread review of the builder's diff (2 files, 12 lines) before fm lane merge; criteria re-run on the merged tree; claude plugin validate passes` → no findings [tree bfed826730d6] (2026-10-09T00:42:35Z)
## Log
- 2026-10-09T00:01:51Z created
- 2026-10-09T00:21:18Z planned from capture
- 2026-10-09T00:21:28Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0371.builder.md
- 2026-10-09T00:21:38Z focused
- 2026-10-09T00:41:48Z merged worktree-agent-a45354b9fb0dc932a (2 file(s))
- 2026-10-09T00:41:53Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a45354b9fb0dc932a
- 2026-10-09T00:41:53Z focused
- 2026-10-09T00:42:35Z scope: the other paths aren't this task's edits — Claude Code made the builder's worktree from the old local main, so its start snapshot predates the build branch's commits (README, install.sh, foreman-ui, MASTER, marketplace); the task's own diff is hooks.json + test_docs.py + CHANGELOG.md
- 2026-10-09T00:42:36Z done
- 2026-10-09T00:42:36Z committed f2c88b6 (70 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0318-surfaces: 1. **Answer.** Foreman has a per-project JSON view model (`fm ui --json`) and a read-only MCP server. The only cross-project data are a hand-re…
- research T-0087-review: Verdict:** approve with nits. PreToolUse can never be paused, and the pause cannot get stuck or flap. The findings below are all MEDIUM or LOW. […
- research T-0324-review: Verdict: changes needed.** One fail-open path and two config-clobber paths are verified. I read the code but ran nothing, so each failing input b…
- decision 2026-10-03: Round 4 slate: guard replay corpus (M) and a mod version check in fm doctor (S) first; four followups to the inbox
## Lessons
- A Sonnet builder handled a 2-file S task cleanly; landing it was the hard part until fm lane merge existed
## Files touched
- .claude/worktrees/agent-a45354b9fb0dc932a/plugin/tests/test_docs.py
- .claude/worktrees/agent-a45354b9fb0dc932a/plugin/hooks/hooks.json
- CHANGELOG.md
- .claude-plugin/marketplace.json
- MASTER.md
- README.md
- install.sh
- mods/foreman-ui/.claude-plugin/plugin.json
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/tools/shot.py
- mods/foreman-ui/types/index.d.ts
- plugin/.claude-plugin/plugin.json
- plugin/bin/fm
- plugin/evals/guard-force-push/prompt.md
- plugin/evals/guard-publish/prompt.md
- plugin/evals/intake-block/prompt.md
- plugin/evals/mid-task-capture/prompt.md
- plugin/evals/one-liner/prompt.md
- plugin/hooks/hook
- plugin/hooks/hooks.json
- plugin/hooks/statusline
- plugin/integrations/opencode/foreman.ts
- plugin/lib/fmagents.py
- plugin/lib/fmbudget.py
- plugin/lib/fmclaude.py
- plugin/lib/fmcli.py
- plugin/lib/fmcore.py
- plugin/lib/fmcost.py
- plugin/lib/fmdoctor.py
