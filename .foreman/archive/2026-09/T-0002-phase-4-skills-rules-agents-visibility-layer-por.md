---
id: T-0002
type: FEATURE
tier: L
status: done
priority: normal
scope: [plugin/**]
depends_on: [T-0001]
source: user
created: 2026-09-26T05:02:11Z
updated: 2026-09-26T05:28:55Z
---
# Phase 4: skills, rules, agents, visibility layer, ported playbooks
## Raw request
> BUILD_PROMPT.md §3 Phase 4, §4.5, §4.8, §8, PLAN.md D21
## Interpretation
Everything the model and user interact with: rules/foreman.md (always-on, ≤80 lines), skills (intake, next, resume, status, capture, tidy, doctor, reflect, improve, playbooks) with ported superpowers + ECC references, read-only agents fm-recon / fm-reviewer, and the visibility layer (statusline wrapper + session snapshots, subagent statusline, fm watch, theme, observability snippet). Small fm additions the skills need: fm decide, fm research add, fm capture --self.
## Assumptions (confidence)
## Acceptance criteria
- [x] rules ≤80 lines; every SKILL.md has name+description and <500 lines; agents have no Write/Edit/Bash; ported files carry attribution — verify with `python3 -m unittest test_docs`
- [x] statusline composes original + hud + Foreman line and writes a session snapshot; subagent rows render; fm watch --once shows a new tool event — verify with `python3 -m unittest test_visibility`
- [x] fm decide / research add / capture --self behave and log — verify with `python3 -m unittest test_cli`
- [x] plugin validates strictly and Foreman's always-on cost stays small — verify with `claude plugin validate --strict plugin; claude plugin details foreman@foreman`
## Non-goals
## Approach (options → choice → why)
Ported procedures live as references behind two skills (intake, playbooks) so always-on cost stays ~2 descriptions; user-only skills set disable-model-invocation. Statusline: Python wrapper runs the saved original command and claude-hud in parallel, then prints one Foreman line from cached state.line; snapshots the statusline JSON to state/sessions for fm watch. fm watch: stdlib curses with a plain --once renderer sharing one data function.
## Risks and rollback
## Execution prompt
Goal: Phase 4 of BUILD_PROMPT (§4.5, §4.8, §8) per local/PLAN.md D7, D8, D18, D21. Code in plugin/lib (fmcore, fmcli, fmhooks), tests in plugin/tests (unittest; ForemanTestCase). 1) Tests first in test_cli.py for fm decide 'X' --why --rejected (appends a row to decisions.md via fm), fm research add NAME [--file F|stdin] (writes research/NAME.md), fm capture --self (targets the project registered for FOREMAN_HOME). 2) test_visibility.py: hooks/statusline reads stdin JSON, runs state/install-manifest.json statusLine_original.command and claude-hud (if enabled) in parallel, drops blank lines, prints Foreman line, writes state/sessions/<id>.json; hooks/subagent-statusline prints {id,content} JSON lines; fm watch --once renders sections incl. a just-appended tool event. 3) Write plugin/rules/foreman.md (≤80 lines), skills/*/SKILL.md (+ intake references language/planning/execute/delegate), agents/fm-recon.md + fm-reviewer.md (tools allowlist, read-only), themes/foreman.json, observability/*, THIRD_PARTY_LICENSES.md, settings.json (subagentStatusLine); test_docs.py enforces budgets and attribution. 4) claude plugin validate --strict plugin; measure claude plugin details foreman@foreman. 5) Commit.
## Steps
1. [x] fm decide / research add / capture --self (TDD)
2. [x] Visibility: statusline wrapper, subagent statusline, fm watch (TDD)
3. [x] Rules, skills, agents, theme, observability, licenses (+ doc tests)
4. [x] Strict validation + footprint measurement
5. [x] Commit phase 4
## Resume here
T-0002 step 2 in progress: test_visibility.py written (RED next); then implement hooks/statusline, hooks/subagent-statusline, lib/fmwatch.py. Porting of superpowers (intake/references) and ECC (playbooks/references, 40 files) already generated via scratchpad/port.py, uncommitted.
<!-- auto -->
- 2026-09-26T05:23:28Z step 2/5: Visibility: statusline wrapper, subagent statusline, fm watch (TDD)
- git: main; 4 uncommitted: plugin/lib/fmcli.py, plugin/tests/test_cli.py, plugin/skills/, plugin/tests/test_visibility.py
## Verification evidence
- (step 1) `python3 -m unittest test_cli` → 29 tests OK incl. decide/research/capture --self (2026-09-26T05:22:50Z)
- (ac 3) `python3 -m unittest test_cli.DecisionsResearchSelf` → 5 tests OK (row format, pipe escaping, stdin/file + redaction, unsafe name refused, --self routing) (2026-09-26T05:22:50Z)
- (step 2) `python3 -m unittest test_visibility` → 9 tests OK: statusline composition/snapshot/fallback, subagent rows, fm watch --once < 2 s with new tool event (2026-09-26T05:25:02Z)
- (ac 2) `python3 -m unittest test_visibility` → 9 tests OK (2026-09-26T05:25:02Z)
- (step 3) `python3 -m unittest test_docs` → 12 tests OK: rules 51 lines, 10 skills valid, 47 ported refs attributed, playbook index complete, agents read-only, settings/theme/hooks.json valid (2026-09-26T05:28:55Z)
- (ac 1) `python3 -m unittest test_docs` → 12 tests OK (2026-09-26T05:28:55Z)
- (step 4) `claude plugin validate --strict plugin; claude plugin details foreman@foreman; unittest discover` → validation passed; always-on ~1,346 tok (11 skills incl. build, 2 agents, 13 hooks); 147 tests OK (2026-09-26T05:28:55Z)
- (ac 4) `claude plugin details foreman@foreman` → ~1,346 always-on tokens vs 51.8k baseline (2026-09-26T05:28:55Z)
- (step 5) `git log --oneline -1` → 5b0589e feat(plugin): rules, skills, read-only agents, visibility layer, ported playbooks (2026-09-26T05:28:55Z)
## Log
- 2026-09-26T05:02:11Z created
- 2026-09-26T05:02:11Z guard authorization added: core
- 2026-09-26T05:18:58Z focused
- 2026-09-26T05:18:58Z set approved=True
- 2026-09-26T05:28:55Z done
## Follow-ups captured
