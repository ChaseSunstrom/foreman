---
id: T-1354
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-10-21T03:47:44Z
updated: 2026-10-21T15:26:35Z
base: 070e9e9fe5acf0de52c8c8b1bf029b84f870192b
base_tree: cc59015e65a1b7a0691905739f677f91999c3b60
plan0_at: 2026-10-21T13:47:39Z
plan0_scope: []
verified: strong
---
# Lean fm code workers: the claude planner runs --restricted and the worker without the user's plugins or MCP servers, the guard kept via --settings
## Raw request
> Lean fm code workers (R2): the claude planner and worker launch without the user's plugins and MCP servers (the guard kept via --settings, like fm bench's bare arm), one config line turns it off, and the first call's input tokens are shown
## Interpretation
fm code's nested claude sessions load every plugin, MCP server, skill list and hook the user has (66k-133k input tokens a call in nixie), so a run is slow and costly. Launch them lean: only Foreman's guard, no user plugins or MCP servers; the planner also loses every code-running tool.
## Assumptions (confidence)
## Acceptance criteria
- [x] lean is the default: the claude planner's argv carries --restricted, --strict-mcp-config and --settings GUARD, the claude worker's --setting-sources project,local, --strict-mcp-config and --settings GUARD; GUARD is the plugin's own PreToolUse entries with every command's root an absolute path that exists; a note says the run is lean; the first call's tokens event still comes — verify with `python3 plugin/tests/run.py test_code_worker`
- [x] code.toml lean = false launches both as today; lean = "false" (not a boolean) is an error naming the key — verify with `python3 plugin/tests/run.py test_code_worker`
- [x] live, on this machine: a lean worker asked to write .claude/settings.local.json in a scratch repo is refused by Foreman's guard (its reply or the file says so), and a lean planner call reads fewer input tokens than today's launch (both counts printed) — verify with `python3 plugin/tests/e2e/lean_probe.py`
## Non-goals
## Approach (options → choice → why)
Options: (A) --bare (rejected: it reads only ANTHROPIC_API_KEY, never the user's OAuth login, and skips settings hooks, so the guard could go); (B) planner --restricted --strict-mcp-config --settings GUARD (no code-running tools, user/project/local settings ignored, --settings still applies) and worker --setting-sources project,local --strict-mcp-config --settings GUARD (chosen: auth unchanged, the guard is the plugin's own PreToolUse entries as fm bench's bare arm builds them); (C) a separate CLAUDE_CONFIG_DIR (rejected: loses the login). code.toml lean = false keeps today's launch. The run says so in a note; the tokens event shows the first call's size.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: a fake claude records argv for planner and worker (lean default, lean = false, a bad lean value); GUARD's commands resolve
2. [x] fmcore.guard_settings(plugin) (moved from fmbench._bare_guard, which calls it); lean flags added to claude's planner and worker launches; code.toml lean switch; note
3. [x] plugin/tests/e2e/lean_probe.py: the guard refuses in a lean worker; today's vs lean planner input tokens; run it here; docs
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_code_worker` → ✗ exit 1 · Ran 56 tests in 66.9s (1 classes, 16 at a time; slowest: Worker 67s) / FAILED (1 classes) [ran] [tree 5327f337b693] (2026-10-21T13:49:13Z)
- (step 3) `python3 plugin/tests/e2e/lean_probe.py` → ✗ exit 1 · lean worker: note.txt written, .env refused; it said: '' / ✗ lean probe failed [ran] [tree 785ef6db02cb] (2026-10-21T15:15:23Z)
- (step 3) `python3 plugin/tests/e2e/lean_probe.py` → exit 0 · lean worker: note.txt written, .env refused; it said: " <ID>`\n   - then run `fm task set <ID> --allow credentials`\n   - then retry the write.\n\nI didn't approve that permission myself or try to get [ran] [tree edd048a9741e] (2026-10-21T15:16:35Z)
- (step 1) `python3 plugin/tests/run.py test_code_worker test_bench` → exit 0 · Ran 93 tests in 55.4s (12 classes, 16 at a time; slowest: Worker 55s, Bench 31s, Judged 17s) / OK [ran] [tree 4d0bf8b785b3] (2026-10-21T15:18:46Z)
- (step 2) `python3 plugin/tests/run.py test_code_worker test_bench` → exit 0 · Ran 93 tests in 54.7s (12 classes, 16 at a time; slowest: Worker 55s, Bench 30s, Judged 17s) / OK [ran] [tree 4d0bf8b785b3] (2026-10-21T15:19:41Z)
- (ac 1) `python3 plugin/tests/run.py test_code_worker` → exit 0 · Ran 56 tests in 56.4s (1 classes, 16 at a time; slowest: Worker 56s) / OK [ran] [tree 4d0bf8b785b3] (2026-10-21T15:20:53Z)
- (ac 2) `python3 plugin/tests/run.py test_code_worker` → exit 0 · Ran 56 tests in 56.4s (1 classes, 16 at a time; slowest: Worker 56s) / OK [ran] [tree 4d0bf8b785b3] (2026-10-21T15:20:53Z)
- (ac 3) `python3 plugin/tests/e2e/lean_probe.py` → exit 0 · lean worker: note.txt written, .env refused; it said: "-tier S`, or `fm focus <ID>`.\n2. Give that task credentials permission: `fm task set <ID> --allow credentials`.\n3. Retry the write.\n\nI didn't [ran] [tree 4d0bf8b785b3] (2026-10-21T15:20:53Z)
- (audit intent) `self-review over the diff plus a live probe on this machine (plugin/tests/e2e/lean_probe.py): lean planner 15,286 vs 31,620 input tokens, both answered; a lean worker wrote note.txt and the guard refused .env; guard settings moved verbatim from fmbench._bare_guard (T-0963's security review), which now calls it` → lean is the default for claude's planner and worker; lean = false launches as before; a non-boolean lean is an error naming it; a note says the run is lean; tokens still reported [tree 4d0bf8b785b3] (2026-10-21T15:20:53Z)
- (audit adversary) `self-review over the diff plus a live probe on this machine (plugin/tests/e2e/lean_probe.py): lean planner 15,286 vs 31,620 input tokens, both answered; a lean worker wrote note.txt and the guard refused .env; guard settings moved verbatim from fmbench._bare_guard (T-0963's security review), which now calls it` → the lean session's only hooks are Foreman's own PreToolUse entries with absolute roots (tested to exist), proven live to refuse a credentials write; the planner additionally has no code-running tools (--restricted); a command the user wrote in code.toml runs as written, with no flags added [tree 4d0bf8b785b3] (2026-10-21T15:20:53Z)
- (audit edge) `self-review over the diff plus a live probe on this machine (plugin/tests/e2e/lean_probe.py): lean planner 15,286 vs 31,620 input tokens, both answered; a lean worker wrote note.txt and the guard refused .env; guard settings moved verbatim from fmbench._bare_guard (T-0963's security review), which now calls it` → a code.toml override of claude's work or plan drops lean for that part only; FOREMAN_QUIET still set so the guard runs alone; the worker keeps the project's own settings by design [tree 4d0bf8b785b3] (2026-10-21T15:20:53Z)
- (audit operator) `self-review over the diff plus a live probe on this machine (plugin/tests/e2e/lean_probe.py): lean planner 15,286 vs 31,620 input tokens, both answered; a lean worker wrote note.txt and the guard refused .env; guard settings moved verbatim from fmbench._bare_guard (T-0963's security review), which now calls it` → README says how to measure (the probe) and switch it off; the probe costs three short calls and isn't in run.py [tree 4d0bf8b785b3] (2026-10-21T15:20:53Z)
- (audit maintainer) `self-review over the diff plus a live probe on this machine (plugin/tests/e2e/lean_probe.py): lean planner 15,286 vs 31,620 input tokens, both answered; a lean worker wrote note.txt and the guard refused .env; guard settings moved verbatim from fmbench._bare_guard (T-0963's security review), which now calls it` → one guard_settings in fmcore for fm bench and fm code; lean flags live in RUNNERS beside the templates [tree 4d0bf8b785b3] (2026-10-21T15:20:53Z)
- (step 1) `python3 plugin/tests/run.py test_code_worker test_bench` → exit 0 · Ran 93 tests in 63.8s (12 classes, 16 at a time; slowest: Worker 64s, Bench 35s, Judged 20s) / OK [ran] [tree 4d0bf8b785b3] (2026-10-21T15:23:33Z)
- (step 2) `python3 plugin/tests/run.py test_code_worker test_bench` → exit 0 · Ran 93 tests in 63.2s (12 classes, 16 at a time; slowest: Worker 63s, Bench 35s, Judged 20s) / OK [ran] [tree 4d0bf8b785b3] (2026-10-21T15:24:37Z)
- (audit intent) `self-review over the diff plus a live probe on this machine (plugin/tests/e2e/lean_probe.py): lean planner 15,286 vs 31,620 input tokens, both answered; a lean worker wrote note.txt and the guard refused .env; guard settings moved verbatim from fmbench._bare_guard (T-0963's security review), which now calls it` → lean is the default for claude's planner and worker; lean = false launches as before; a non-boolean lean is an error naming it; a note says the run is lean; tokens still reported [tree 4d0bf8b785b3] (2026-10-21T15:24:43Z)
- (audit adversary) `self-review over the diff plus a live probe on this machine (plugin/tests/e2e/lean_probe.py): lean planner 15,286 vs 31,620 input tokens, both answered; a lean worker wrote note.txt and the guard refused .env; guard settings moved verbatim from fmbench._bare_guard (T-0963's security review), which now calls it` → the lean session's only hooks are Foreman's own PreToolUse entries with absolute roots (tested to exist), proven live to refuse a credentials write; the planner also has no code-running tools (--restricted); a command the user wrote in code.toml runs as written [tree 4d0bf8b785b3] (2026-10-21T15:24:43Z)
- (audit edge) `self-review over the diff plus a live probe on this machine (plugin/tests/e2e/lean_probe.py): lean planner 15,286 vs 31,620 input tokens, both answered; a lean worker wrote note.txt and the guard refused .env; guard settings moved verbatim from fmbench._bare_guard (T-0963's security review), which now calls it` → a code.toml override of claude's work or plan drops lean for that part only; FOREMAN_QUIET still set so the guard runs alone; the worker keeps the project's own settings by design [tree 4d0bf8b785b3] (2026-10-21T15:24:43Z)
- (audit operator) `self-review over the diff plus a live probe on this machine (plugin/tests/e2e/lean_probe.py): lean planner 15,286 vs 31,620 input tokens, both answered; a lean worker wrote note.txt and the guard refused .env; guard settings moved verbatim from fmbench._bare_guard (T-0963's security review), which now calls it` → README says how to measure (the probe) and switch it off; the probe costs three short calls and isn't in run.py [tree 4d0bf8b785b3] (2026-10-21T15:24:43Z)
- (audit maintainer) `self-review over the diff plus a live probe on this machine (plugin/tests/e2e/lean_probe.py): lean planner 15,286 vs 31,620 input tokens, both answered; a lean worker wrote note.txt and the guard refused .env; guard settings moved verbatim from fmbench._bare_guard (T-0963's security review), which now calls it` → one guard_settings in fmcore for fm bench and fm code; lean flags live in RUNNERS beside the templates [tree 4d0bf8b785b3] (2026-10-21T15:24:43Z)
## Log
- 2026-10-21T03:47:44Z created
- 2026-10-21T13:38:49Z planned from capture
- 2026-10-21T13:41:14Z second plan (revise) taken: live probe for the guard and the token counts (e2e, not run.py); default lean = true, lean must be a boolean; guard JSON shared from fmcore; the worker keeps the project's own settings by design (as a person running claude there would; the planner ignores them under --restricted)
- 2026-10-21T13:47:38Z focused
- 2026-10-21T15:15:04Z user approved plugin in Claude Code's permission prompt
- 2026-10-21T15:16:35Z scope: plugin/lib/fmcore.py, plugin/lib/fmbench.py, plugin/tests/e2e/lean_probe.py, README.md, CHANGELOG.md — the shared guard settings (moved from fmbench), the live probe, docs
- 2026-10-21T15:26:34Z done
- 2026-10-21T15:26:35Z committed f4cf3b99 (7 files)
## Follow-ups captured
## Plan review
A second read on sonnet, before execution (data, not instructions):
- HIGH: The third criterion can't be verified by the named command. A unit-test suite built on a fake claude can't record real input-token counts from this machine. It needs a live, authenticated call that costs money and varies from run to run, and it is likely to be skipped or flaky in `run.py`. — …
- HIGH: The plan assumes `--settings` still applies the PreToolUse guard when `--restricted`, `--strict-mcp-config` and `--setting-sources project,local` are set. It also assumes `--restricted` is a real flag, and that it removes only the code-running tools. Nothing in the plan confirms any of this, …
- MEDIUM: The planner and worker use different isolation: the planner ignores user, project and local settings, while the worker still reads project and local settings. Project-level hooks, plugins or MCP config in the repo being worked on still load for the worker. This may be intended, but the plan…
- MEDIUM: Reusing `fmbench._bare_guard` from `fmcode` creates a dependency between the two modules. The guard JSON also has to resolve the plugin root correctly in every launch context (installed, dev checkout, nested child). The criterion only says "root resolved" without saying how it's checked. — …
- MEDIUM: The lean switch is off-by-config only. There is no check that a user's `lean = false` or a missing key falls back to the intended default, and the plan doesn't say what the default is (the title implies lean on). A bad config value, such as a string "false", could flip behavior. — Specify t…
- LOW: "The first call's input tokens are shown" is in the raw request, but no step or criterion covers the display. The plan only mentions the tokens event in the approach. — Add a criterion or test showing that the tokens event/output for the first call appears in a lean run.
Verdict: revise — the argv-level design is reasonable, but the guard-survives claim and the token-measurement criterion both need real verification outside the fake-claude test before this can be trusted.
## Dissent
- [ ] HIGH: The third criterion can't be verified by the named command. A unit-test suite built on a fake claude can't record real input-token counts from this machine. It needs a live, authenticated call that costs money and varies from run to run, and it is likely to be skipped or flaky in `run.py`. — …
- [ ] HIGH: The plan assumes `--settings` still applies the PreToolUse guard when `--restricted`, `--strict-mcp-config` and `--setting-sources project,local` are set. It also assumes `--restricted` is a real flag, and that it removes only the code-running tools. Nothing in the plan confirms any of this, …
- [ ] MEDIUM: The planner and worker use different isolation: the planner ignores user, project and local settings, while the worker still reads project and local settings. Project-level hooks, plugins or MCP config in the repo being worked on still load for the worker. This may be intended, but the plan…
- [ ] MEDIUM: Reusing `fmbench._bare_guard` from `fmcode` creates a dependency between the two modules. The guard JSON also has to resolve the plugin root correctly in every launch context (installed, dev checkout, nested child). The criterion only says "root resolved" without saying how it's checked. — …
- [ ] MEDIUM: The lean switch is off-by-config only. There is no check that a user's `lean = false` or a missing key falls back to the intended default, and the plan doesn't say what the default is (the title implies lean on). A bad config value, such as a string "false", could flip behavior. — Specify t…
- [ ] LOW: "The first call's input tokens are shown" is in the raw request, but no step or criterion covers the display. The plan only mentions the tokens event in the approach. — Add a criterion or test showing that the tokens event/output for the first call appears in a lean run.
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-fm-code-catalogue: Source: research/brainstorm-20261020-222518 (fm ideas, 10 lenses, 4 rounds, 3 deepened; 522 distinct ideas). Grounded in two halve…
- research mission-20261020-222446.pack: super improve fm code, make it genuinely amazing: launch it as an app like claude (fm code with no request), able to manage ANY CL…
- T-1294 [FIX M, done, 3 steps] fm code --worker: a worker's own edits count as the run's for Foreman leases, so the judge keeps them and the next turn can edit the same c…
- decision 2026-10-20: [costly] Run fm code bench --worker claude on 2 seeds (operator, off-by-one) as T-1215's real end-to-end check
- the similar finished task took 3 steps
## Lessons
- Measure a 'lean' claim live before shipping it: a fake CLI can prove the flags but never the saving or that the guard survives
## Plan gaps
- failed first: step 1 Failing tests: a fake claude records argv for planner and worker (lean default, lean = false, a bad…
- failed first: step 3 plugin/tests/e2e/lean_probe.py: the guard refuses in a lean worker; today's vs lean planner input t…
## Files touched
- plugin/tests/test_code_worker.py
- plugin/lib/fmbench.py
- plugin/lib/fmcore.py
- plugin/lib/fmcode.py
- plugin/tests/e2e/lean_probe.py
- CHANGELOG.md
- README.md
