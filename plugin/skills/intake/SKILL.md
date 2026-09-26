---
name: intake
description: Use for any new work request before editing anything — tagged lines (FIX:, FEATURE:, CLEAN:, PERF:, SECURITY:, RESEARCH:, with CONTEXT/CONSTRAINT/DONE-WHEN/SKIP) or a plain one-line request. Turns it into Foreman briefs, expands (R1), grounds in the real code (R2), anticipates follow-ups (R3), compiles a self-contained Execution prompt (R4), orders the queue canonically and starts per autonomy. Also covers the execute loop, evidence, debugging, regression tests and delegation.
---

# Foreman intake

Run this for every new request, tagged or plain. A typo gets a three-line brief, never zero thought. State changes go through `fm`.

## 1. Capture
- Tagged block → `fm intake <<'EOF'` … `EOF` (stdin). It creates one **captured** brief per item, attaches the block's CONTEXT/CONSTRAINT/DONE-WHEN/SKIP lines, and prints the canonical order. Language details: `references/language.md`.
- Plain request → classify it (type + tier) and state that in one line, then `fm capture "<verbatim request>" --type T --tier X`.
- While another task is active, a new request is only captured (focus lock in the rules): reply with its id and continue the active task.

## 2. Expand, ground, anticipate, compile (per item, in canonical order)
Promote each captured item: `fm task new "<imperative title>" --type T --tier X --from T-NNNN --scope <glob>...`.
Then fill the brief with `fm task set ID --section "<Name>" --text "…"` and `fm task ac` / `fm task step`:
1. **R1 Expand:** Interpretation, Assumptions (with confidence), testable acceptance criteria (`fm task ac ID add "<criterion>" --verify "<cmd>"`), scope paths, Non-goals.
2. **R2 Ground:** read the real code, run the real commands, correct R1 against reality. For M/L, compare at least two approaches in "Approach (options → choice → why)". Library/API questions: context7. Large unfamiliar areas: `foreman:fm-recon` (`references/delegate.md`).
3. **R3 Anticipate:** pre-mortem — "if I ship this, what are the three most likely follow-ups or complaints?" Implied requirements (error handling, edge cases, tests, docs/config, migration notes) go in scope. Adjacent ideas are captured (`fm capture --source followup`), not built.
4. **R4 Compile:** write the **Execution prompt** section: a block a fresh session with zero history could execute (goal, context, files, steps, acceptance checks, verification commands, constraints). Add steps with `fm task step ID add "…"`.
Tier depth, the brief layout and the rubric: `references/planning.md`.

## 3. Self-critique (M/L, and before any approval gate)
Every criterion has a verification command? Could a fresh session run the Execution prompt without asking? Anything in scope the user didn't ask for and wouldn't expect → INBOX. Anything obviously expected missing → add. Simplest adequate approach? Rollback clear? Revise at most twice.

## 4. Autonomy gate
- L tier, `?` items, and anything destructive or irreversible (data deletion, force-push, migrations on real data, major dependency bumps, public API changes): present a ≤ 15-line plan summary plus batched questions, each with your default, then stop. After approval: `fm task set ID approved=true`.
- S/M: proceed after self-review.

## 5. Baseline (once per queue)
Confirm the build and tests run; record baseline metrics for PERF items; note git state. `fm log baseline '{"tests":"<result>","commit":"<sha>"}'`. A FIX that breaks the baseline is hoisted first.

## 6. Execute
`fm focus ID`, then follow `references/execute.md` — one step at a time, fresh evidence per step, checkpoints, commits, the 3-attempt loop cap and end-of-task triage. Stage procedures: `/foreman:playbooks`. FIX work: `references/debugging.md` then `references/regression-test.md`. Before any completion claim: `references/verification.md`.
