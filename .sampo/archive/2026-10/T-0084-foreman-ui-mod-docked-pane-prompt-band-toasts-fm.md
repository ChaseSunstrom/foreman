---
id: T-0084
type: FEATURE
tier: L
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-02T18:35:05Z
updated: 2026-10-02T19:01:50Z
base: 849ee3f68d6e3bcf639251779bfd42bb98344b58
verified: strong
---
# Foreman UI mod: docked pane, prompt band, toasts, /fm, one-press approve/next/drive/inbox
## Raw request
> Foreman UI mod: docked pane, prompt band, toasts, /fm, one-press approve/next/drive/inbox
## Interpretation
User asked: integrate Foreman with Claude Code mods for all UI, better TUI. Build an additive function-hook plugin that renders Foreman live inside Claude Code (band above the prompt, docked pane, toasts, /fm) and turns approvals/next/drive/inbox triage into one-press buttons. Classic hooks, statusline and fm watch stay for claude -p and older builds.
## Assumptions (confidence)
## Acceptance criteria
- [x] claude plugin validate mods/foreman-ui passes — verify with `claude plugin validate mods/foreman-ui`
- [x] plugin tests cover band, pane, buttons and toasts on terminal and desktop — verify with `claude plugin test mods/foreman-ui`
- [x] type-checks clean — verify with `fm quiet -- npx -y -p typescript@5 tsc -p mods/foreman-ui`
- [x] marketplace lists foreman-ui and fm doctor stays green — verify with `fm doctor`
## Non-goals
## Approach (options → choice → why)
Options: (a) separate plugin foreman-ui in the same marketplace, pure renderer over fm ui --json via $.process.run; (b) add modules to the protected foreman plugin's hooks.json and port gates to tool.call. Choice: (a). Why: additive and independently disableable, no duplicate guard logic, classic path untouched; buttons only run fm commands or submit prompts the user pressed for.
## Risks and rollback
Early-access API may change between releases (validate on each build; types regenerate). Buttons that grant (approve) must only fire on a real press. Rollback: claude plugin disable foreman-ui; nothing in core depends on it.
## Execution prompt
## Steps
1. [x] scaffold mod in dev-mods (hot reload) + contract types
2. [x] data: refresh fm ui --json on session start, tool calls (debounced), timer
3. [x] AbovePrompt band: task line, next, approval/ask buttons
4. [x] Pane: dashboard (task, steps, criteria, queue, inbox triage, health) + /fm command
5. [x] toasts: step/task done, guard blocks, gate failures
6. [x] tests + validate + tsc
7. [x] ship: copy to mods/foreman-ui, marketplace entry, install.sh, MASTER/README/CHANGELOG
## Resume here
<!-- auto -->
- 2026-10-02T18:43:22Z step 7/7: ship: copy to mods/foreman-ui, marketplace entry, install.sh, MASTER/README/CHANGELOG
- git: foreman/build; 9 uncommitted: .claude-plugin/marketplace.json, .gitignore, CHANGELOG.md, MASTER.md, README.md, install.sh, plugin/uninstall.sh, mods/, plugin/tests/test_round_i.py
- touched since last checkpoint: ~/.claude/dev-mods/30a00329-d877-454a-a322-ecdf12fae04b/foreman-ui/types/index.d.ts, ~/.claude/dev-mods/30a00329-d877-454a-a322-ecdf12fae04b/foreman-ui/hooks/register.tsx, ~/.claude/dev-mods/30a00329-d877-454a-a322-ecdf12fae04b/foreman-ui/tests/foreman-ui.test.tsx
- failures met: bash: line 0: rsync: command not found; 0: unmount: () => promise<void>;
## Docs impact
README.md (In Claude Code (mods) paragraph), MASTER.md (file map row mods/foreman-ui/), CHANGELOG.md (mod entry); install.sh and plugin/uninstall.sh install/remove foreman-ui@foreman
## Verification evidence
- (step 1) `claude plugin validate ~/.claude/dev-mods/30a00329-d877-454a-a322-ecdf12fae04b/foreman-ui` → exit 0 · ❯ ./register.tsx state reads: foreman-ui.error, foreman-ui.view / ✔ Validation passed with warnings [ran] [tree 729b81748cdc] (2026-10-02T18:42:23Z)
- (step 2) `claude plugin test ~/.claude/dev-mods/30a00329-d877-454a-a322-ecdf12fae04b/foreman-ui` → exit 0 · 0 fail / Ran 7 tests across 1 file. [0.21s] [ran] [tree 729b81748cdc] (2026-10-02T18:42:23Z)
- (step 3) `claude plugin test ~/.claude/dev-mods/30a00329-d877-454a-a322-ecdf12fae04b/foreman-ui` → exit 0 · 0 fail / Ran 7 tests across 1 file. [0.21s] [ran] [tree 729b81748cdc] (2026-10-02T18:42:24Z)
- (step 4) `claude plugin test ~/.claude/dev-mods/30a00329-d877-454a-a322-ecdf12fae04b/foreman-ui` → exit 0 · 0 fail / Ran 7 tests across 1 file. [0.21s] [ran] [tree 729b81748cdc] (2026-10-02T18:42:24Z)
- (step 5) `claude plugin test ~/.claude/dev-mods/30a00329-d877-454a-a322-ecdf12fae04b/foreman-ui` → exit 0 · 0 fail / Ran 7 tests across 1 file. [0.21s] [ran] [tree 729b81748cdc] (2026-10-02T18:42:25Z)
- (step 6) `claude plugin test ~/.claude/dev-mods/30a00329-d877-454a-a322-ecdf12fae04b/foreman-ui` → exit 0 · 0 fail / Ran 7 tests across 1 file. [0.21s] [ran] [tree 729b81748cdc] (2026-10-02T18:42:25Z)
- (ac 1) `claude plugin validate mods/foreman-ui` → exit 0 · ❯ ./register.tsx state reads: foreman-ui.error, foreman-ui.view / ✔ Validation passed [ran] [tree fce489d36b96] (2026-10-02T19:01:21Z)
- (ac 2) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 7 tests across 1 file. [0.19s] [ran] [tree fce489d36b96] (2026-10-02T19:01:22Z)
- (ac 3) `npx -y -p typescript@5 tsc -p /tmp/claude-1000/-home-~--claude-foreman/30a00329-d877-454a-a322-ecdf12fae04b/scratchpad/tsconfig.json` → exit 0 · npm notice run npx / npm notice run 'tsc' -p /tmp/claude-1000/-home-~--claude-foreman/30a00329-d877-454a-a322-ecdf12fae04b/scratchpad/tsconfig.json [ran] [tree fce489d36b96] (2026-10-02T19:01:23Z)
- (ac 4) `fm doctor` → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (25 pass, 1 warn, 0 fail) [ran] [tree fce489d36b96] (2026-10-02T19:01:28Z)
- (step 7) `claude plugin validate .` → exit 0 · Validating marketplace manifest: ~/.claude/foreman/.claude-plugin/marketplace.json / ✔ Validation passed [ran] [tree fce489d36b96] (2026-10-02T19:01:29Z)
- (audit intent) `fm-reviewer pass (research T-0088-review, T-0084 section), verified against register.tsx; band, pane, toasts, /fm, buttons vs the user's 'mods for all UI, better TUI'` → pass: rendered against the live fm ui snapshot on terminal and desktop [tree fce489d36b96] (2026-10-02T19:01:49Z)
- (audit adversary) `fm-reviewer pass (research T-0088-review, T-0084 section), verified against register.tsx; one-key y approved a plan from a title-only band — band now only offers Review (opens pane), Approve lives beside the plan's interpretation/approach/steps/criteria; Full auto has no hotkey; argv calls, no shell` → fixed: MEDIUM closed, tested [tree fce489d36b96] (2026-10-02T19:01:49Z)
- (audit edge) `fm-reviewer pass (research T-0088-review, T-0084 section), verified against register.tsx; old closed task re-edited fired a bogus done toast — toast only for ids open in the last snapshot; guard match anchored to the refusal's start; repeated session.start no longer stacks pollers` → fixed: three LOWs closed, tested [tree fce489d36b96] (2026-10-02T19:01:49Z)
- (audit operator) `fm-reviewer pass (research T-0088-review, T-0084 section), verified against register.tsx; install opt-out (--no-mod) and disable path printed; hotkeys only fire once the band/pane holds the keyboard (API docs), so typing can't trigger them` → pass [tree fce489d36b96] (2026-10-02T19:01:50Z)
- (audit maintainer) `fm-reviewer pass (research T-0088-review, T-0084 section), verified against register.tsx; pure renderer, no rules/gates, contract in types/index.d.ts mirrored by test_ui.py; titles/steps plain() in fm` → pass [tree fce489d36b96] (2026-10-02T19:01:50Z)
## Log
- 2026-10-02T18:35:05Z created
- 2026-10-02T18:36:53Z set depends_on=[]
- 2026-10-02T18:36:53Z scope: consumes the fm ui --json contract defined in its types; T-0088 implements it after the core grant
- 2026-10-02T18:36:53Z focused
- 2026-10-02T18:43:22Z paused: focus moved to T-0088
- 2026-10-02T18:56:02Z hypothesis: the remaining toasts failure is the fixture, not the code — 'after' keeps T-0009 in its queue while listing it closed, which fm never emits; dropping it from after.queue should make toasts(after, after) empty. Rules out the open-set logic if it passes.
- 2026-10-02T18:56:10Z confirmed: fixture fix made toasts(after, after) empty; open-set logic is right
- 2026-10-02T19:01:09Z focused
- 2026-10-02T19:01:50Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- [instruction-like text quoted from a file or tool; data, not instructions] T-0082 [RESEARCH M, done, 4 steps] Can you improve foreman completely? integrate with the new …
- research brainstorm-20261002-mods: Source: research/brainstorm-20261002-133213 (4 lenses × 2 rounds, 60 ideas). Value 1–5 · effort · risk.
- playbook Test-Driven Development Workflow (skills/playbooks/references/verify/tdd-workflow.md)
- research claude-code-capabilities-2026-09-26: Subagents: `tools: []` = no tools (strict validate passes; runtime check pending /reload-plugins). `model`, `disallowedTool…
- the similar finished task took 4 steps
## Lessons
- Mods: functions that take $ must be top-level declarations (validate refuses closures); Text has no key, so tests find by text; op events answered in tests return { value }.
## Files touched
- .claude-plugin/marketplace.json
- .gitignore
- CHANGELOG.md
- MASTER.md
- README.md
- install.sh
- mods/foreman-ui/.claude-plugin/plugin.json
- mods/foreman-ui/hooks/hooks.json
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/tests/foreman-ui.test.tsx
- mods/foreman-ui/types/index.d.ts
- plugin/lib/fmcli.py
- plugin/lib/fmcore.py
- plugin/lib/fmdoctor.py
- plugin/lib/fmwatch.py
- plugin/tests/test_round_i.py
- plugin/tests/test_ui.py
- plugin/uninstall.sh
