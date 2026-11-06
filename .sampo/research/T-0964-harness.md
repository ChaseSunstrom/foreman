1) **What the harness is.** claude-code-harness is a plan, work, review loop run as skills (`/harness-plan`, `-work`, `-review`, `-sync`, `-release`, `-setup`, `-progress`, `/breezing`, `/harness-loop`) over a Go binary, `bin/harness`. Nearly every Claude Code hook event is wired through `bin/harness hook <name>` in `.claude-plugin/hooks.json`. Its state is `Plans.md` with `cc:*` task markers, `spec.md`, `.claude/state/`, `.claude/memory/decisions.md` and `patterns.md`, and a config JSON/YAML. Guardrails are rules R01–R16 that return deny, ask or warn (CLAUDE.md). It has five agents: worker, reviewer, advisor, test-wiring-auditor, livemsg-gate. It also emits Codex, Cursor and Grok variants. Sources: README, hooks.json and CLAUDE.md, all fetched. I only partly read the file tree, and I did not read any skill bodies or Go code. Hook purposes are inferred from handler names, so confidence is medium.

2) **Feature comparison**

| Feature | Harness (path) | Foreman | Adopt? |
|---|---|---|---|
| Plan to `Plans.md` and `spec.md`, user approves | `skills/harness-plan` | intake briefs with acceptance criteria and commands, tiers S/M/L (README:111) | no, Foreman has it |
| Work one task, all tasks, or `--resume` | `harness-work` | drive mode, `fm run`, `/foreman:resume` (README:22-23) | no |
| Independent review that blocks on serious findings | `harness-review`, `agents/reviewer.md` | `fm-reviewer` agent, `fm task audit` lenses (MASTER:134) | no |
| Plan, git and implementation sync | `harness-sync` | `fm sync`, `fm docs` drift check (MASTER:60) | no |
| Release skill with approval gate | `harness-release` | `release.py` only, no skill (README:330) | maybe, as a low-priority skill wrapper |
| Setup and migration doctor | `harness-setup`, `doctor --migration-report` | `fm doctor`, `install.sh` | no |
| Progress and Accept surfaces as HTML | `cognitive-load` skill | Foreman Desktop, `fm ui`, Pulse (MASTER:78) | no |
| Parallel team run | `/breezing` | `fm run --parallel` in lanes (MASTER:217) | no |
| Loop with a cycle cap (default 8) | `harness-loop` | drive plus the `fm serve` restart cap | no |
| Guardrails R01–R16 (force-push, main push, staged secrets) | Go engine | fail-closed guard (README:20,228), `fm secrets` | no, though a rule table could be ported |
| **Advisor for a stuck executor**: Fable-class read-only agent, retry-threshold trigger, PLAN/CORRECTION/STOP JSON | `agents/advisor.md` | **MISSING**. I grepped for "stuck" and "escalat" and found only the ANDON assumption path (MASTER:71). | **yes**, a cheap fix for retry loops |
| **Test-wiring auditor**: every changed product file must be exercised by a test, one appeal, and a block on `ADD_REQUIRED` | `agents/test-wiring-auditor.md` | **MISSING**. `fm wiring` exists but its scope is unclear (MASTER:60). | **yes**, directly serves "verified" |
| `tdd-check`, `auto-test` and `quality-pack` hooks after each edit | hooks.json PostToolUse | Partial: builder works test-first (MASTER:71) and the edit gate needs a task. I found no post-edit auto-test. | **yes**, if it runs async and is cheap |
| LLM agent hook reviewing each Write/Edit for secrets, stubs and injection | hooks.json PreToolUse, claude-haiku-5-5 | `fm secrets` scan, but not a per-edit LLM gate | no, costs tokens on every edit |
| File leases between sessions | `pre-tool-use-file-lease` | function-level edit leases in PreToolUse (MASTER:60) | no, Foreman's are finer |
| Inbox and inter-session messages, with a livemsg-gate fact check | `agents/livemsg-gate.md` | `fm bus`, `fm conductor`; no fact-check gate | no |
| Cross-session memory (`harness-mem`) | memory skill and hooks | native auto memory, failure memory and recall (MASTER:60,103) | no |
| PreCompact warning about `cc:WIP` work | PreCompact agent hook | checkpoint at 85% context (README:163) | no |
| Worker report schema with five self-review items | `worker-report.v1` | `fm task step done --evidence` is refused without evidence (MASTER:131) | no, Foreman's is stricter |
| CI status hook | `ci-status` | `fm check` gates | no |
| Writing lint | `writing-lint` | none found | no |
| Skill mirror drift check | `skill-mirror-drift.sh` | `fm doctor` file-map drift (MASTER:183) | no |
| Multi-host (Codex, Cursor, Grok, OpenCode) | `hosts/`, `harness gen` | Claude Code only (inferred) | no, unless you use those hosts |
| Language setting (English/Japanese) | `CLAUDE_CODE_HARNESS_LANG` | none found | no |
| Self-improvement, scout and night jobs | none found | Foreman only | n/a |

3) **Top 5 missing or weaker features, ranked for autonomous, finish-everything, cheap and verified work**
1. **Test-wiring auditor.** It stops "done" claims that have no test touching the changed code, and it needs no model for the mechanical first pass.
2. **Advisor on a retry threshold.** It gives a stuck run one cheap read-only PLAN, CORRECTION or STOP ruling instead of burning cycles.
3. **Post-edit `auto-test` and `tdd-check`.** They give early failure signals during the task, not only at the gate.
4. **Release skill with an approval gate.** Foreman has the script but no guided skill.
5. **A published, numbered rule table for the guard.** Foreman's guard may be stronger, but its README lists categories, not individually auditable rules.

**Risks.**
- The Foreman greps only matched long lines, so some capabilities may exist unseen. Check `fm wiring` and the builder's TDD enforcement before building anything.
- The harness page is very large and I did not read it all.

**Not checked.** I did not read the harness skill bodies, the Go engine or its tests. I did not read the README of the harness's `benchmarks/`. I did not read Foreman's `fm*.py` code. I did not measure the harness's actual hook cost.

**Noticed:**
- The harness hook file has 40+ hook entries, many on every tool call. That is a token and latency risk Foreman deliberately avoids (MASTER:172), which is worth a doc note.
- It is unclear whether `fm wiring` covers test-to-code coverage or something else.
