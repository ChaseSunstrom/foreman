# Rival plugins: every gap, grounded and marked (T-0964, 2026-10-15)

Sources: research/T-0964-harness.md (claude-code-harness, feature by feature), research/T-0964-workflow.md (ECC,
superpowers, OpenSpec, spec-kit, BMAD, SuperClaude, task-master, ccpm, Auto-Claude, cc-sessions, spec-workflow,
TDD Guard, hookify, official plugins, awesome-claude-code index), research/T-0964-orchestration.md (claude-flow,
oh-my-claudecode, Claude Squad, vibe-kanban, Crystal, Conductor, claude-code-router, ccusage, Usage Monitor, opcode,
tweakcc, continuous-claude, claude-code-action, Aider, OpenHands, Roo, Cline, Kiro, Devin). Grounding: grep of
MASTER.md, README.md and plugin/lib by the main thread; "present" means the code does it today.

Marks: BUILD (queued now) · LATER (inbox, with why) · DONE (Foreman has it) · SKIP (with why).

## Verification
| Gap | From | Grounding | Value | Mark |
|---|---|---|---|---|
| Test-first at edit time: product code edited before the task's failing test exists | TDD Guard, superpowers, harness tdd-check | No edit-time nudge in fmhooks (grep test-first: none); close-time T-0474 "not verified" and fm task prove exist | 4 | BUILD (zero-token, no LLM judge) |
| Affected tests run in the background after edits, failures surfaced next turn | harness auto-test | `fm check --affected` is manual; the claims gate only notes "no test ran after the last edit" | 4 | BUILD |
| Test-wiring audit: changed files with no test exercising them | harness test-wiring-auditor | DONE: T-0474 close warning "not verified: … no linked test changed or ran" (fmcli ~1747), red→green for FIX | 5 | DONE (warns; a block would fail legit refactors) |
| Confidence-scored review findings | official code-review | reviewer returns verified findings only; ReportFindings carries a verdict | 2 | SKIP: verdict already filters |
| Reviewer on another provider in the loop | continuous-claude, /ask | `fm second` (other model) exists after the fact | 2 | SKIP: fm second covers it |

## Safety
| Gap | From | Grounding | Value | Mark |
|---|---|---|---|---|
| User-authored rule files: regex → warn or block, from corrections | hookify | vetoes.json only adds a note (MASTER: vetoes); no block | 4 | BUILD (`fm rule`) |
| Instruction-like text in fetched/tool output flagged | Parry-guard, AgentShield | untrusted issue text is marked; nothing scans WebFetch/MCP/curl output | 3 | BUILD (zero-token note) |
| Auto-approve read-only commands by parsing | Dippy | PermissionRequest only records fm ask (fmhooks.permission_request) | 3 | BUILD, opt-in (helps default-mode users; off by default) |
| Container or sandbox per headless run | OpenHands | README: the guard is a speed bump, not a sandbox; no sandbox flag on fm run | 4 | BUILD after confirming Claude Code's sandbox settings key in its docs |
| Numbered guard rule table | harness R01–R16 | categories documented, no numbered table | 2 | LATER: docs only, low value |
| Per-edit LLM gate for secrets/stubs | harness PreToolUse agent hook | fm secrets scans commits | 2 | SKIP: tokens on every edit |

## Cost and pace
| Gap | From | Grounding | Value | Mark |
|---|---|---|---|---|
| Limit forecast: when the 5-hour/weekly window fills at this pace | Usage Monitor, ccusage | fmbudget reads used_percentage/resets_at and pace; no forecast line | 3 | BUILD (`fm cost --forecast`) |
| Plan-strong / edit-cheap model split | Aider architect, opusplan | `fm run --models` per tier; no per-phase split | 3 | LATER: measure with fm bench first |
| Per-task complexity → model routing | oh-my-claudecode | tiers map to models in fm run | 2 | DONE (per tier) |
| Provider fallback on a limit | claude-code-router | `fm run --failover AGENT` | 2 | DONE |
| Gateway with traces and key pools | claude-code-router | none | 1 | SKIP: out of scope |

## Orchestration and integrations
| Gap | From | Grounding | Value | Mark |
|---|---|---|---|---|
| PR per task: push, open PR, wait for CI, merge on green | continuous-claude, ccpm | no gh pr path (grep: none); lanes merge locally | 4 | LATER (inbox `?`): outward; needs the user's yes for pushes |
| GitHub @claude bot | claude-code-action | official action exists | 3 | SKIP: use the official action |
| Dependency-graph waves in parallel | Kiro | `#T-…` depends-on + fm run --parallel batches independent tasks | 3 | DONE |
| Best-of-N: two lanes try competing approaches, keep the better | Crystal, Fusion Harness | fm ideas fans out ideas, not implementations | 3 | LATER: costly; worth a bench first |
| Inline diff comments sent back to the agent | vibe-kanban, Conductor, Plannotator | approve-plan, fm page picks; no diff comments | 3 | LATER: an Artifact review page whose comments become steers |
| Chat notifications | oh-my-claudecode | fm notify CMD + PushNotification | 2 | DONE |
| PRD → epic → issues write-back | ccpm | fm inbox gh reads issues | 3 | LATER: outward, same blocker as forge sync |
| Shareable read-only dashboard | spec-workflow | fm ui / pane; Artifacts could host one | 2 | LATER |
| Scheduled/webhook triggers | OpenHands | fm night, fm scout, fm serve | 2 | DONE |
| Release skill with an approval gate | harness-release | release.py | 2 | SKIP: the release script is the gate |

## Memory, planning, UX
| Gap | From | Grounding | Value | Mark |
|---|---|---|---|---|
| Vector/semantic recall | claude-flow, Continuous-Claude, ECC | fm recall (lexical) + lessons | 2 | SKIP: a vector store adds a dependency for little |
| Repo/symbol map | Aider | fm map, fm sym, fm outline | 3 | DONE |
| Checkpoint rewind and fork | opcode | Claude Code /rewind + refs/foreman/snapshots; fm oops (T-0960) | 3 | DONE |
| Constitution + clarify gate | spec-kit | CLAUDE.md + intake Interpretation/Assumptions | 2 | SKIP |
| Living spec deltas | OpenSpec | briefs per task | 2 | SKIP |
| Complexity scoring + subtask expansion | task-master | tiers; `fm task split` | 2 | DONE |
| Scored "instincts" | ECC | lessons + tripwires injected | 2 | SKIP |
| Kanban board | vibe-kanban, Auto-Claude | pane + Desktop | 2 | SKIP |
| TTS announcements | hooks-mastery | chimes + notify | 1 | SKIP |
| Advisor for a stuck executor | harness advisor | 3-failures block + "edited 6 times without a check" hypothesis nudge + fm-debugger agent | 3 | DONE (nudge names debugging.md; fm-debugger exists) |
| PreCompact warning | harness | checkpoint at 85% context | 2 | DONE |
| Multi-host emitters | harness, wshobson | fm agents install codex/gemini/opencode | 2 | DONE |
| Ralph loop | ralph-wiggum | the drive | 2 | DONE |

## Slate (queued as briefs, value for effort)
1. Test-first nudge at edit time (S/M)
2. Background affected tests after edits, failures surfaced next turn (M)
3. `fm rule`: user regex rules that warn or block, enforced by the guard hook (M)
4. Instruction-like text in tool output flagged (S)
5. `fm cost --forecast` (S)
6. Opt-in read-only auto-approve in PermissionRequest (S/M)
7. `fm run --sandbox` with Claude Code's native sandbox (S, docs check first)
