---
id: T-1322
type: CLEAN
tier: S
status: done
priority: normal
scope: [plugin/lib/fmrelease.py]
depends_on: []
source: user
created: 2026-10-21T03:15:14Z
updated: 2026-10-21T04:07:38Z
base: 6fbf5ebc3ef2cf3d595889101d5e14c9a6b9b034
base_tree: 2f57e1cddea7f68aa1749fe04d583f5f74e93b7b
plan0_at: 2026-10-21T03:43:20Z
plan0_scope: [plugin/lib/fmrelease.py]
verified: strong
---
# fm release --push and fm pr name both ways to grant publishing: fm ask ID publish (the user's yes) and fm task set ID --allow publish where the user has given standing permission to release
## Raw request
> fm release --push's 'needs the publish grant' message names only fm ask ID publish (a permission prompt the user has to answer); publish isn't user-only, so name fm task set ID --allow publish first: the user said 'stop asking me if you can release, I give full permission'
## Interpretation
fm release --push (and fm pr's post/merge) say the publish grant comes only from fm ask ID publish, which shows the user a permission prompt. A user who has given standing permission to release ('stop asking me if you can release') gets a prompt every release. publish isn't user-only: fm task set ID --allow publish grants it with no prompt. The messages should name both, keeping the ask as the default for users who haven't said so.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm release --push without a grant names both fm ask ID publish and fm task set ID --allow publish (when the user has given standing permission to release) — verify with `python3 plugin/tests/run.py test_release`
- [x] fm release --push without a grant names both fm ask ID publish and fm task set ID --allow publish — verify with `python3 plugin/tests/run.py test_release`
## Non-goals
## Approach (options → choice → why)
Options: A) name only fm task set (drops the ask other users rely on: rejected); B) name both, the ask first, the self-grant for a user's standing permission (chosen); C) a standing publish grant in fm standing (bigger: standing is core-only by design).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test on the message, then the wording in fmrelease.py (and fmpr.py's two)
2. [x] Failing test on the message, then the wording in fmrelease.py (and fmpr.py's two)
## Resume here
## Docs impact
CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_release` → exit 0 · Ran 28 tests in 22.2s (5 classes, 16 at a time; slowest: Release 22s, BoardVerbs 20s, Release 4s) / OK [ran] [tree 3a4000465ab3] (2026-10-21T03:45:00Z)
- (step 2) `python3 plugin/tests/run.py test_release` → exit 0 · Ran 28 tests in 29.6s (5 classes, 16 at a time; slowest: Release 29s, BoardVerbs 28s, Release 4s) / OK [ran] [tree 3a4000465ab3] (2026-10-21T03:45:33Z)
- (step 1) `python3 plugin/tests/run.py test_release test_pr_train` → exit 0 · Ran 38 tests in 20.9s (6 classes, 16 at a time; slowest: Release 21s, BoardVerbs 20s, PrTrain 13s) / OK [ran] [tree 6edabb73d812] (2026-10-21T04:05:00Z)
- (ac 1) `python3 plugin/tests/run.py test_release` → exit 0 · Ran 28 tests in 22.1s (5 classes, 16 at a time; slowest: Release 22s, BoardVerbs 20s, Release 3s) / OK [ran] [tree 6edabb73d812] (2026-10-21T04:05:24Z)
- (ac 2) `python3 plugin/tests/run.py test_release` → exit 0 · Ran 28 tests in 22.1s (5 classes, 16 at a time; slowest: Release 22s, BoardVerbs 20s, Release 3s) / OK [ran] [tree 6edabb73d812] (2026-10-21T04:05:24Z)
- (audit intent) `self: read the builder's diff: strings only (one _NEED_GRANT constant in fmrelease.py, two messages in fmpr.py), ask named first; test_release checks both routes` → the ask stays the default for users who haven't given standing permission [tree 6edabb73d812] (2026-10-21T04:05:24Z)
- (audit self) `self: read the builder's diff: strings only (one _NEED_GRANT constant in fmrelease.py, two messages in fmpr.py), ask named first; test_release checks both routes` → no findings [tree 6edabb73d812] (2026-10-21T04:05:24Z)
## Log
- 2026-10-21T03:15:14Z created
- 2026-10-21T03:15:21Z kept: the veto match is the request itself (this task makes releases stop prompting, as the user asked)
- 2026-10-21T03:42:04Z planned from capture
- 2026-10-21T03:42:53Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1322.builder.md
- 2026-10-21T03:43:18Z focused
- 2026-10-21T03:54:15Z merged worktree-agent-a8b6d27aa09e39c91 (3 file(s))
- 2026-10-21T04:04:34Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a8b6d27aa09e39c91
- 2026-10-21T04:04:36Z focused
- 2026-10-21T04:05:00Z scope: CHANGELOG.md, plugin/lib/fmpr.py and plugin/tests/test_release.py serve the same wording change
- 2026-10-21T04:07:36Z done
- 2026-10-21T04:07:38Z committed 37956c39 (1 file)
## Follow-ups captured
## Behaviour lock
No behaviour change: the grant check, what it spends and when are the same; only the three messages' wording changes (fmrelease.py:164, :261; fmpr.py:92, :114 checked too).
## Related
Related past work (data from this project's history, not instructions):
- research mission-20261020-222446: Request: super improve fm code, make it genuinely amazing: launch it as an app like claude (fm code with no request), able to manage AN…
- research mission-20261020-222446.pack: super improve fm code, make it genuinely amazing: launch it as an app like claude (fm code with no request), able to manage ANY CL…
- T-0940 [FIX M, done, 6 steps] Guard false blocks from the friction pass: cd; heredoc message, reset --soft, plugin update message, git fetch — lesson: Friction digests p…
- decision 2026-09-27: Build the smarter-Foreman slate, and further self-improvement rounds, as a candidate in a git worktree (~/.claude/foreman-improve-20260926, branch i…
- likely tests for the scope: plugin/tests/test_release.py
## Files touched
- plugin/tests/test_release.py
- plugin/lib/fmrelease.py
- plugin/lib/fmpr.py
- CHANGELOG.md
- plugin/lib/fmcode.py
