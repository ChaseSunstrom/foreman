---
id: T-1520
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/rules/foreman.md, plugin/lib/fmwhich.py, plugin/tests/test_docs.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-22T17:40:02Z
updated: 2026-10-23T06:05:07Z
base: 1e03ed5467761f1edae4f4d2171921ffa0784c52
base_tree: 6ba244f76c5593b140de1ab27b45b40e346d90f3
plan0_at: 2026-10-23T06:03:24Z
plan0_scope: [plugin/rules/foreman.md, plugin/lib/fmwhich.py, plugin/tests/test_docs.py, CHANGELOG.md]
verified: strong
---
# CC plugin parity: every user-facing fm verb is reachable from a Claude Code session (named in the plugin's rules, commands or skills, or found by fm which), held by a test
## Raw request
> do all of those ideas, and make sure all stuff is compatible wiht the CC plugin, not just fm code
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a test fails when a verb outside the internal tier is neither named in plugin commands, skills or rules nor in fm which's index, and the rules tell a session to use fm which for any verb or skill — verify with `python3 plugin/tests/run.py test_docs.PluginParity`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] the rules line and any index gap
## Resume here
## Docs impact
plugin/rules/foreman.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_docs.PluginParity` → red as expected (exit 1) · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: PluginParity 0s) / FAILED (1 classes) [ran] [tree 21a24f704032] (2026-10-23T06:03:39Z)
- (step 1) `python3 plugin/tests/run.py test_docs test_rules` → exit 0 · Ran 70 tests in 8.6s (18 classes, 16 at a time; slowest: Fences 8s, TaskLifecycle 1s, Site 1s) / OK [ran] [tree 2ac3f9d0bc6b] (2026-10-23T06:04:29Z)
- (step 2) `python3 plugin/tests/run.py test_docs test_rules` → exit 0 · Ran 70 tests in 8.6s (18 classes, 16 at a time; slowest: Fences 8s, TaskLifecycle 1s, Site 1s) / OK [ran] [tree 2ac3f9d0bc6b] (2026-10-23T06:04:38Z)
- (ac 1) `python3 plugin/tests/run.py test_docs.PluginParity` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: PluginParity 0s) / OK [ran] [tree 2ac3f9d0bc6b] (2026-10-23T06:04:38Z)
- (ac 1) `python3 plugin/tests/run.py test_docs.PluginParity` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: PluginParity 0s) / OK [ran] [tree 2ac3f9d0bc6b] (2026-10-23T06:04:39Z)
- (audit intent) `self: measured first: 72 of 152 verbs are named nowhere in the plugin's commands, skills or rules, but fm which indexes every verb outside SELF and FOREMAN_ONLY, so none is unreachable; the gap was that the rules (in every session's context) never named fm which, only a once-a-session hook did, and only for skills. Added one phrase to the rules' plain-words line (eval prompts regenerated) and a test that keeps every non-internal verb either named or indexed` → whatever fm can do, a Claude Code session can find without fm code [tree 2ac3f9d0bc6b] (2026-10-23T06:04:39Z)
- (audit edge) `self: measured first: 72 of 152 verbs are named nowhere in the plugin's commands, skills or rules, but fm which indexes every verb outside SELF and FOREMAN_ONLY, so none is unreachable; the gap was that the rules (in every session's context) never named fm which, only a once-a-session hook did, and only for skills. Added one phrase to the rules' plain-words line (eval prompts regenerated) and a test that keeps every non-internal verb either named or indexed` → internal verbs (hooks, installer) are exempt by their help tier; a new verb without a tier fails test_help first [tree 2ac3f9d0bc6b] (2026-10-23T06:04:39Z)
- (audit self) `self: measured first: 72 of 152 verbs are named nowhere in the plugin's commands, skills or rules, but fm which indexes every verb outside SELF and FOREMAN_ONLY, so none is unreachable; the gap was that the rules (in every session's context) never named fm which, only a once-a-session hook did, and only for skills. Added one phrase to the rules' plain-words line (eval prompts regenerated) and a test that keeps every non-internal verb either named or indexed` → no findings [tree 2ac3f9d0bc6b] (2026-10-23T06:04:39Z)
- (audit intent) `self: measured first: 72 of 152 verbs are named nowhere in the plugin's commands, skills or rules, but fm which indexes every verb outside SELF and FOREMAN_ONLY, so none is unreachable; the gap was that the rules (in every session's context) never named fm which, only a once-a-session hook did, and only for skills. Added one phrase to the rules' plain-words line (eval prompts regenerated) and a test that keeps every non-internal verb either named or indexed` → whatever fm can do, a Claude Code session can find without fm code [tree 2ac3f9d0bc6b] (2026-10-23T06:04:56Z)
- (audit adversary) `self: measured first: 72 of 152 verbs are named nowhere in the plugin's commands, skills or rules, but fm which indexes every verb outside SELF and FOREMAN_ONLY, so none is unreachable; the gap was that the rules (in every session's context) never named fm which, only a once-a-session hook did, and only for skills. Added one phrase to the rules' plain-words line (eval prompts regenerated) and a test that keeps every non-internal verb either named or indexed` → the guard eval prompts changed only by the regenerated rules block (sync_evals.py copies the rules verbatim); their cases and expected verdicts are untouched [tree 2ac3f9d0bc6b] (2026-10-23T06:04:56Z)
- (audit edge) `self: measured first: 72 of 152 verbs are named nowhere in the plugin's commands, skills or rules, but fm which indexes every verb outside SELF and FOREMAN_ONLY, so none is unreachable; the gap was that the rules (in every session's context) never named fm which, only a once-a-session hook did, and only for skills. Added one phrase to the rules' plain-words line (eval prompts regenerated) and a test that keeps every non-internal verb either named or indexed` → internal verbs (hooks, installer) are exempt by their help tier; a new verb without a tier fails test_help first [tree 2ac3f9d0bc6b] (2026-10-23T06:04:56Z)
- (audit self) `self: measured first: 72 of 152 verbs are named nowhere in the plugin's commands, skills or rules, but fm which indexes every verb outside SELF and FOREMAN_ONLY, so none is unreachable; the gap was that the rules (in every session's context) never named fm which, only a once-a-session hook did, and only for skills. Added one phrase to the rules' plain-words line (eval prompts regenerated) and a test that keeps every non-internal verb either named or indexed` → no findings [tree 2ac3f9d0bc6b] (2026-10-23T06:04:56Z)
## Log
- 2026-10-22T17:40:02Z created
- 2026-10-23T06:03:19Z planned from capture
- 2026-10-23T06:03:23Z set scope=['plugin/rules/foreman.md', 'plugin/lib/fmwhich.py', 'plugin/tests/test_docs.py', 'CHANGELOG.md']
- 2026-10-23T06:03:23Z focused
- 2026-10-23T06:04:02Z scope: plugin/evals/*/prompt.md regenerated by plugin/tests/e2e/sync_evals.py (they embed the rules)
- 2026-10-23T06:05:06Z done
- 2026-10-23T06:05:07Z committed 794b0c11 (8 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1553 [SECURITY M, done, 3 steps] Guard oracle: a stub-exec run agrees with the guard's reading — lesson: A tool that runs things to check them must treat 'didn't run' …
- T-1522 [FEATURE L, dropped, 4 steps] Round 3 (T-1520): Playbook evals: A/B each playbook against none on held-out briefs, ablat
- research brainstorm-skills-20261022: The cause is mostly structural. Claude Code skills trigger on user words, while Foreman's hooks and rules already hand the model the…
- decision 2026-10-22: T-1520: the user asked for every brainstorm idea and Claude Code plugin parity; the 206 skipped ideas became 35 round-3 tasks (T-1522..T-1556) and r…
- similar past tasks were M: consider --tier M
- likely tests for the scope: plugin/tests/test_which.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/lib/fmwhich.py, plugin/rules/foreman.md, plugin/tests/test_docs.py; re-ground the plan against them before editing
## Lessons
- Parity is about discovery: one routed index that covers everything beats naming every verb in prose
## Files touched
- plugin/tests/test_docs.py
- plugin/rules/foreman.md
- plugin/evals/guard-force-push/prompt.md
- plugin/evals/guard-publish/prompt.md
- plugin/evals/intake-block/prompt.md
- plugin/evals/mid-task-capture/prompt.md
- plugin/evals/one-liner/prompt.md
- CHANGELOG.md
