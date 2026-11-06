---
id: T-0375
type: FEATURE
tier: L
status: done
priority: normal
scope: [plugin/lib/fmmission.py, plugin/lib/fmcli.py, plugin/lib/fmideas.py, plugin/lib/fmhooks.py, plugin/skills/brainstorm/**, plugin/tests/**, MASTER.md, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-09T00:10:52Z
updated: 2026-10-09T01:02:21Z
base: c60ba31655d1b1c47d062c82029ecfcfb83586f7
base_tree: 542addaa429b05790789b9599a36879570642f8b
verified: strong
---
# fm mission: Foreman composes the full mission and brainstorm seeds itself for open-ended and exhaustive requests
## Raw request
> what other prompt can I give to jarvis to give full functionality/UI/motion/beautiful UI/features/capabilities, seeds for brainstorm prompts and orchestration agents of agents, etc. ? and whatever you give me, and what I am asking for, allow foreman to do automatically, so i don't have to manually ask you for a prompt again, etc.
## Interpretation
The user had to ask me twice for a JARVIS prompt that says: finish the queue in parallel, super brainstorm with capability map, UI/motion/beauty per surface, orchestration (agents of agents), verify on the real path, repo sweep, recurse until dry. They want Foreman to compose that itself every time a request is open-ended, for any project (not hardcoded to JARVIS).
## Assumptions (confidence)
## Acceptance criteria
- [x] fm mission writes a pack + mission (the user's own words, open queue/inbox, surfaces found, pillars: capability map, UI and motion per surface, real-path verification, parallel lanes, repo sweep, recursion until dry) and the fm ideas command with lenses chosen for the project's surfaces — verify with `python3 plugin/tests/run.py -k test_mission_composes_pack_pillars_and_lenses`
- [x] an open-ended or exhaustive prompt's note names fm mission first — verify with `python3 plugin/tests/run.py -k test_open_ended_request_points_at_mission`
## Non-goals
## Approach (options → choice → why)
(a) a fixed prompt template in the skill — the model fills it by hand each time, the step it skipped before; (b) fm mission: one command builds the pack from the project's facts (README head, fm map, git log), the user's own words (fmideas.user_voice), open queue/inbox, and detected surfaces (web UI, mobile, desktop, server, CLI, LLM/agent code), writes the mission with pillars and the exact fm ideas line with surface-chosen lenses; the prompt note and brainstorm skill call it; (c) run fm ideas automatically from the hook — too costly and invisible. Choice (b).
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first: fm mission (pack, surfaces → lenses, pillars, saved under research/)
2. [x] new lenses: beautiful UI and motion, every device and surface, agents of agents; prompt hook note; brainstorm skill uses it
3. [x] gate, docs
## Resume here
<!-- auto -->
- 2026-10-09T00:48:56Z step 1/3: test-first: fm mission (pack, surfaces → lenses, pillars, saved under research/)
- git: foreman/build; 4 uncommitted: plugin/lib/fmcli.py, plugin/tests/test_hooks.py, plugin/lib/fmmission.py, plugin/tests/test_mission.py
- touched since last checkpoint: plugin/tests/test_mission.py, plugin/tests/test_hooks.py, plugin/lib/fmmission.py, plugin/lib/fmcli.py
## Docs impact
CHANGELOG Unreleased, MASTER file map (fmmission), brainstorm SKILL step 2, ideas-prompt lens descriptions, fm help tier
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_mission_composes_pack_pillars_and_lenses` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Mission 0s) / OK [ran] [tree 5a447bbe5515] (2026-10-09T00:51:04Z)
- (step 2) `python3 plugin/tests/run.py -k test_open_ended_request_points_at_mission` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: UserPromptSubmit 0s) / OK [ran] [tree 41c291a64da2] (2026-10-09T00:51:32Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 1 of 6 failed: python3 plugin/tests/run.py → ✗ exit 1 · Ran 905 tests in 37.0s (222 classes, 16 at a time; slowest: Stop 24s, TaskLifecycle 21s, Bench 19s) / FAILED (2 classes) [ran] [tree d0d1bc0312f8] (2026-10-09T00:54:51Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (26 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                32.7    34.3     150  [0] / SessionEnd                  30.0    32.2     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 00:30 UTC; python3 plugin/tests/run.py → exit 0 · Ran 905 tests in [ran] [tree bbacc29da6ef] (2026-10-09T00:58:14Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (26 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                32.1    34.5     150  [0] / SessionEnd                  29.9    31.5     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 00:30 UTC; python3 plugin/tests/run.py → exit 0 · Ran 905 tests in [ran] [tree ddf47d8f9411] (2026-10-09T01:02:11Z)
- (ac 1) `python3 plugin/tests/run.py -k test_mission_composes_pack_pillars_and_lenses` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Mission 0s) / OK [ran] [tree ddf47d8f9411] (2026-10-09T01:02:21Z)
- (ac 2) `python3 plugin/tests/run.py -k test_open_ended_request_points_at_mission` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: UserPromptSubmit 0s) / OK [ran] [tree ddf47d8f9411] (2026-10-09T01:02:21Z)
- (audit intent) `one foreman:fm-reviewer pass (Sonnet), five lenses; findings verified against the code and fixed; gate green after the fixes` → ok — hook names fm mission for exhaustive and open-ended prompts; note now uses double quotes like SKILL.md [tree ddf47d8f9411] (2026-10-09T01:02:21Z)
- (audit adversary) `one foreman:fm-reviewer pass (Sonnet), five lenses; findings verified against the code and fixed; gate green after the fixes` → ok — printed and --json mission are now the redacted text, same as saved; pack path shlex-quoted in the fm ideas line [tree ddf47d8f9411] (2026-10-09T01:02:21Z)
- (audit edge) `one foreman:fm-reviewer pass (Sonnet), five lenses; findings verified against the code and fixed; gate green after the fixes` → ok — CLI project with docs/index.html and server Kotlin gets no UI or mobile surface (test); git via c._git with timeouts; 12-lens super run is still capped by fm budget, which refuses explicitly [tree ddf47d8f9411] (2026-10-09T01:02:21Z)
- (audit operator) `one foreman:fm-reviewer pass (Sonnet), five lenses; findings verified against the code and fixed; gate green after the fixes` → ok — MASTER, CHANGELOG, help tiers updated; rules file untouched; prompt note within budget (test) [tree ddf47d8f9411] (2026-10-09T01:02:21Z)
- (audit maintainer) `one foreman:fm-reviewer pass (Sonnet), five lenses; findings verified against the code and fixed; gate green after the fixes` → ok — reuses c._git, fmideas.user_voice, DEFAULT_LENSES; mission embeds the pack on purpose so it stands alone [tree ddf47d8f9411] (2026-10-09T01:02:21Z)
## Log
- 2026-10-09T00:10:52Z created
- 2026-10-09T00:20:46Z planned from capture
- 2026-10-09T00:20:46Z set approved=True
- 2026-10-09T00:48:08Z focused
- 2026-10-09T01:02:21Z done
- 2026-10-09T01:02:21Z committed 9956efc (10 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0364 [FIX L, done, 5 steps] Foreman keeps working while background jobs run, plans and brainstorms wider, uses subagents — lesson: Read the user's transcripts before t…
- research landscape-20261004: Asked 2026-10-04 · 3 sub-question(s) · 21 claims: 12 quote found, 7 quote not found, 2 unchecked. ✓ means the quoted words are on the cited …
- T-0125 [FEATURE M, done, 4 steps] Recursive self-improvement loop: fm friction digests Foreman's own friction since the last pass, fm next calls for a pass every N close…
- decision 2026-09-27: Build the smarter-Foreman slate, and further self-improvement rounds, as a candidate in a git worktree (~/.claude/foreman-improve-20260926, branch i…
- likely tests for the scope: plugin/tests/test_hooks.py, plugin/tests/test_ideas.py
## Lessons
- When the user asks for a prompt twice, make Foreman compose it from the project; keep surface detection on directory/manifest signals, not file extensions alone
## Files touched
- plugin/tests/test_mission.py
- plugin/tests/test_hooks.py
- plugin/lib/fmmission.py
- plugin/lib/fmcli.py
- plugin/lib/fmhooks.py
- plugin/lib/fmideas.py
- plugin/skills/brainstorm/SKILL.md
- plugin/skills/brainstorm/references/ideas-prompt.md
- CHANGELOG.md
- MASTER.md
