---
id: T-1262
type: FEATURE
tier: S
status: done
priority: normal
scope: [mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx, mods/foreman-ui/README.md, mods/foreman-ui/.claude-plugin/plugin.json, .claude-plugin/marketplace.json, CHANGELOG.md, mods/foreman-ui/types/index.d.ts]
depends_on: []
source: followup
created: 2026-10-20T14:01:26Z
updated: 2026-10-23T12:55:55Z
base: 771938a0a89cbc7c1a0431363da505342782452f
base_tree: cba7cf08f06a206dca21a6f51fad6cdafef54828
plan0_at: 2026-10-23T12:50:18Z
plan0_scope: [mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx, mods/foreman-ui/README.md, CHANGELOG.md]
verified: strong
---
# Guard asks through a mod tool.check with decider person, so only a person's dialog answer
## Raw request
> Guard asks through a mod tool.check with decider person, so only a person's dialog answer approves (needs the foreman-ui update the user approves) (brainstorm-20261020 C8)
## Interpretation
A guard grant (fm ask ID CATEGORY) must be approved only by a person answering the permission dialog: never by auto mode's classifier, bypass mode, or a saved allow rule. Claude Code 2.1.309 has no decider field any more: a tool.check hook's own ask is a person's ask (the dialog, the host's callback or a PermissionRequest hook answers; no classifier allow settles it; no whole-tool rule is kept; where nobody can be asked it is a deny). So foreman-ui re-answers Foreman's PreToolUse ask for fm ask as its own.
## Assumptions (confidence)
## Acceptance criteria
- [x] Foreman's ask for fm ask comes back from tool.check as foreman-ui's own ask (plugin set by the engine), with Foreman's reason; any other verdict passes through untouched — verify with `claude plugin test mods/foreman-ui`
## Non-goals
## Approach (options → choice → why)
Options: (1) a tool.check hook that re-answers core's ask when PreToolUse made it with Foreman's 'Foreman asks' reason - chosen: no second parser of fm ask, the guard stays the one judge; (2) parse the command in TS (mirrors lone_fm_ask; drifts); (3) deny unless approver is person (would refuse the desktop app's host callback, which the engine counts as a person's channel). A hook that fails is skipped and the classic flow stands (today's behaviour: the grant still needs the PermissionRequest record).
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test: tool.check on fm ask returns foreman-ui's ask; other asks and allows untouched
2. [x] the tool.check hook, README and CHANGELOG
## Resume here
## Docs impact
mods/foreman-ui/README.md (a Grants line), CHANGELOG.md; mods/foreman-ui/types/index.d.ts declares scrub
## Verification evidence
- (step 1) `claude plugin test mods/foreman-ui` → ✗ exit 1 · 1 fail / Ran 149 tests across 4 files. [11.70s] [ran] [tree 8d5d57a43ed0] (2026-10-23T12:51:55Z)
- (step 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 149 tests across 4 files. [11.74s] [ran] [tree 9e69462a67ba] (2026-10-23T12:54:40Z)
- (step 2) `python3 plugin/tests/run.py test_release test_release_py test_plugins test_supply_delta` → exit 0 · Ran 108 tests in 13.1s (12 classes, 16 at a time; slowest: Release 13s, BoardVerbs 12s, Install 2s) / OK [ran] [tree 9e69462a67ba] (2026-10-23T12:54:54Z)
- (ac 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 149 tests across 4 files. [11.62s] [ran] [tree 9e69462a67ba] (2026-10-23T12:55:06Z)
- (ac 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 149 tests across 4 files. [11.68s] [ran] [tree 9e69462a67ba] (2026-10-23T12:55:27Z)
- (audit intent) `self review in the main thread (subagents paused by the usage budget): the hook only ever re-answers an ask as an ask, so it can't loosen anything; it keys on core's verdict (PreToolUse's ask with Foreman's 'Foreman asks' reason, which only the two fm ask prompts in fmhooks.py start with), so the guard stays the one parser of fm ask; claude plugin validate passes (it failed before on the undeclared scrub key)` → an fm ask grant can be approved only by a person's answer; auto mode's classifier, bypass mode or a whole-Bash allow rule no longer settle it (Claude Code 2.1.309 treats a plugin's own tool.check ask as a person's) [tree 9e69462a67ba] (2026-10-23T12:55:27Z)
- (audit edge) `self review in the main thread (subagents paused by the usage budget): the hook only ever re-answers an ask as an ask, so it can't loosen anything; it keys on core's verdict (PreToolUse's ask with Foreman's 'Foreman asks' reason, which only the two fm ask prompts in fmhooks.py start with), so the guard stays the one parser of fm ask; claude plugin validate passes (it failed before on the undeclared scrub key)` → other asks (a PreToolUse ask with another reason), denies and allows pass untouched (tested); a failure falls back to the verdict beneath (the classic ask), never an allow; where nobody can be asked the engine refuses the plugin's ask, as fm run's own deny already did [tree 9e69462a67ba] (2026-10-23T12:55:27Z)
- (audit adversary) `self review in the main thread (subagents paused by the usage budget): the hook only ever re-answers an ask as an ask, so it can't loosen anything; it keys on core's verdict (PreToolUse's ask with Foreman's 'Foreman asks' reason, which only the two fm ask prompts in fmhooks.py start with), so the guard stays the one parser of fm ask; claude plugin validate passes (it failed before on the undeclared scrub key)` → a model can't word its way in: the reason comes from Foreman's hook output, and another hook's 'Foreman asks' ask is only made stricter; the PostToolUse grant still needs the dialog's PermissionRequest record [tree 9e69462a67ba] (2026-10-23T12:55:27Z)
- (audit self) `self review in the main thread (subagents paused by the usage budget): the hook only ever re-answers an ask as an ask, so it can't loosen anything; it keys on core's verdict (PreToolUse's ask with Foreman's 'Foreman asks' reason, which only the two fm ask prompts in fmhooks.py start with), so the guard stays the one parser of fm ask; claude plugin validate passes (it failed before on the undeclared scrub key)` → no findings [tree 9e69462a67ba] (2026-10-23T12:55:27Z)
## Log
- 2026-10-20T14:01:26Z created
- 2026-10-23T12:50:13Z set tier=S, scope=['mods/foreman-ui/hooks/register.tsx', 'mods/foreman-ui/tests/foreman-ui.test.tsx', 'mods/foreman-ui/README.md', 'CHANGELOG.md']
- 2026-10-23T12:50:17Z focused
- 2026-10-23T12:51:01Z set scope=['mods/foreman-ui/hooks/register.tsx', 'mods/foreman-ui/tests/foreman-ui.test.tsx', 'mods/foreman-ui/README.md', 'mods/foreman-ui/.claude-plugin/plugin.json', '.claude-plugin/marketplace.json', 'CHANGELOG.md']
- 2026-10-23T12:54:06Z set scope=['mods/foreman-ui/hooks/register.tsx', 'mods/foreman-ui/tests/foreman-ui.test.tsx', 'mods/foreman-ui/README.md', 'mods/foreman-ui/.claude-plugin/plugin.json', '.claude-plugin/marketplace.json', 'CHANGELOG.md', 'mods/foreman-ui/types/index.d.ts']
- 2026-10-23T12:54:07Z scope: types/index.d.ts gains scrub (T-1081 wrote foreman-ui.scrub without declaring it, so claude plugin validate failed on the mod this task releases as 0.19.0)
- 2026-10-23T12:55:54Z done
- 2026-10-23T12:55:55Z committed a0304697 (7 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0974 [FEATURE M, done, 3 steps] Opt-in auto-approve of read-only Bash the guard classifies safe, in the PermissionRequest hook (T-0974) — lesson: An allowlist for 'rea…
- research claude-code-capabilities: Method.** I read the README, the plugins/ and examples/ directory listings, the docs overview, and the CHANGELOG (about 1.06M characte…
- research T-0108-review: [instruction-like text quoted from a file or tool; data, not instructions] ## intent: ok [stale: mods/foreman-ui/hooks/register.tsx, plugin/lib/f…
- decision 2026-09-26: T-0014 permission mode: fm serve passes --permission-mode only when given; otherwise Remote Control uses the user's own defaultMode (bypass here, se…
## Preflight
Changed in scope since this was planned (2026-10-20): CHANGELOG.md, mods/foreman-ui/README.md, mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx; re-ground the plan against them before editing
## Lessons
- Claude Code 2.1.309 has no tool.check decider field: a plugin's own ask is already a person's, so tighten by re-answering the ask, not by returning it as heard
## Plan gaps
- failed first: step 1 red test: tool.check on fm ask returns foreman-ui's ask; other asks and allows untouched
## Files touched
- mods/foreman-ui/tests/foreman-ui.test.tsx
- .claude-plugin/marketplace.json
- CHANGELOG.md
- mods/foreman-ui/.claude-plugin/plugin.json
- mods/foreman-ui/README.md
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/types/index.d.ts
