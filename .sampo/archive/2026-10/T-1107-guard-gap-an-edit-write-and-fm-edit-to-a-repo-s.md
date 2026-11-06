---
id: T-1107
type: SECURITY
tier: S
status: done
priority: normal
scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py]
depends_on: []
source: discovered
created: 2026-10-16T05:05:43Z
updated: 2026-10-16T05:20:57Z
base: fe7d349803187932f731eddddca13e2c1b7d9b79
base_tree: 64c98aae3663882f9a951efae231feab7c66dd30
verified: strong
---
# Guard gap: an Edit/Write (and fm edit) to a repo's .git/config or .git/hooks/* is allowed;
## Raw request
> Guard gap: an Edit/Write (and fm edit) to a repo's .git/config or .git/hooks/* is allowed; core.hooksPath or a hook file runs code on the next git command. Treat writes under .git/ as a guarded category (ask), as the guard does for Claude Code settings
## Interpretation
Edit/Write/redirect to a git config file isn't guarded, though the same key set through `git config` is (_git_config_code): core.hooksPath, alias.!, filter drivers, includes. Classify writes to a repo's .git/config, .git/config.worktree, .git/worktrees/*/config and the user-wide ~/.gitconfig and ~/.config/git/config as 'system' (code that runs later), as .git/hooks/ already is.
## Assumptions (confidence)
## Acceptance criteria
- [x] A write to .git/config, .git/config.worktree, .git/worktrees/x/config, ~/.gitconfig or ~/.config/git/config is classified system; look-alike files are not — verify with `python3 plugin/tests/run.py test_guard`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test: each config path → system; a look-alike file → nothing
2. [x] Add the config paths to _runs_later
## Resume here
## Docs impact
CHANGELOG line; guard behaviour, no user doc
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_guard` → ✗ exit 1 · Ran 106 tests in 6.4s (45 classes, 16 at a time; slowest: GuardAgainstBash 6s, Hook 3s, PluginChanges 1s) / FAILED (1 classes) [ran] [tree b527a3a61e0c] (2026-10-16T05:20:01Z)
- (step 2) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 106 tests in 6.4s (45 classes, 16 at a time; slowest: GuardAgainstBash 6s, Hook 2s, InterpreterWrites 1s) / OK [ran] [tree 91063e061952] (2026-10-16T05:20:16Z)
- (ac 1) `python3 plugin/tests/run.py test_guard` → exit 0 · Ran 106 tests in 13.2s (45 classes, 16 at a time; slowest: GuardAgainstBash 13s, Hook 5s, RuleIds 2s) / OK [ran] [tree bb6e722e1e1c] (2026-10-16T05:20:55Z)
- (audit adversary) `self: table test of every config path plus look-alikes and git's own config-writing commands` → symlinked targets resolve through _variants; case-folded .GIT/CONFIG matched (re.I); git's own config writes (config user.name, remote add, branch -u) stay unguarded; a redirect append to .git/config is system; not covered: a custom GIT_DIR or a rewritten .git gitdir file pointing elsewhere [tree bb6e722e1e1c] (2026-10-16T05:20:55Z)
- (audit self) `self: table test of every config path plus look-alikes and git's own config-writing commands` → no findings [tree bb6e722e1e1c] (2026-10-16T05:20:55Z)
## Log
- 2026-10-16T05:05:43Z created
- 2026-10-16T05:19:30Z set scope=['plugin/lib/fmguard.py', 'plugin/tests/test_guard.py']
- 2026-10-16T05:19:47Z focused
- 2026-10-16T05:20:41Z scope: CHANGELOG.md — the release note for the guard change
- 2026-10-16T05:20:56Z done
- 2026-10-16T05:20:57Z committed 79017f8 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0269-review-2: Verdict:** changes needed. I read the code only and ran nothing, so each "not blocked" below comes from tracing the code and is unexecuted.
- research T-0291-review-1: Changes needed. Fix 2 (the `confirm` flag) can be bypassed by the working session itself, and fix 3 has one gap that runs a planted driver. [st…
- research t0018-r5-maintainer: HIGH — plugin/lib/fmguard.py:188-198 (`_protected_roots`) vs plugin/lib/fmguard.py:165-171 (`_is_core`) — tree-write guard misses project-l…
- decision 2026-10-04: Friction pass 2026-10-04: drop recon findings 1-3 (guard)
- likely tests for the scope: plugin/tests/test_guard.py
## Lessons
- When a guard covers a command that changes a setting, check the file the setting lives in too
## Plan gaps
- failed first: step 1 Failing test: each config path → system; a look-alike file → nothing
## Files touched
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- CHANGELOG.md
