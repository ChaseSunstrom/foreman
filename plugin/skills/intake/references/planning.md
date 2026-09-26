# Planning: passes, tiers, brief, rubric (reference)

## Passes
- **R1 Expand:** interpretation, assumptions with confidence, testable acceptance criteria, scope paths, non-goals.
- **R2 Ground:** read the real code, run the real commands, correct R1 against reality. M/L: at least two approaches, choose one, say why.
- **R3 Anticipate:** "If I ship this and the user reviews it, what are the three most likely follow-ups or complaints?" Each is either an implied requirement the user would obviously expect (in scope) or an adjacent idea (`fm capture --source followup`, not built). Implied requirements stay within what matters: validation at trust boundaries, data-loss handling, security, accessibility, explicit requests, tests and evidence.
- **R4 Compile:** the brief's Execution prompt, executable by a fresh session with no history. Regenerate it at every re-plan checkpoint.

## Tiers
| Tier | Signal | Depth |
|---|---|---|
| S | ~≤30 lines, 1–2 files, obvious approach, low risk | brief ≤ 10 content lines: R1 + light R2 + R4; still logged and verified |
| M | several files or a real design choice | full R1–R4, two approaches |
| L | cross-cutting, schema/API/security-sensitive, large or uncertain | R1–R4 + adversarial self-critique + staged sub-tasks, each independently verifiable; optional `foreman:fm-reviewer` |
When unsure, go one tier up; tiers may change after R2 (`fm task set ID tier=M`, and say so).

## Brief (created by fm from templates/brief.md)
Frontmatter: id, type, tier, status (captured|planned|active|verifying|done|blocked|deferred|dropped), priority, scope, depends_on, source, allow (guard authorizations), approved, explore, created, updated.
Sections: Raw request · Interpretation · Assumptions (confidence) · Acceptance criteria · Non-goals · Approach (options → choice → why) · Risks and rollback · Execution prompt · Steps · Resume here · Verification evidence · Log · Follow-ups captured.
Edit sections with `fm task set ID --section "<Name>" --text "…"` (or `--file`). Steps with `fm task step`, criteria with `fm task ac`, evidence with `fm task evidence`.

## Rubric (self-critique before executing M/L and before any gate; at most two revisions)
- Every acceptance criterion has a verification command?
- Could a fresh session execute the Execution prompt without asking anything?
- Anything in scope the user didn't ask for and wouldn't expect? Move it to INBOX.
- Anything the user would obviously expect missing? Add it.
- Simplest adequate approach? What would make it fail?
- Is rollback clear?

## Questions
Batch them into one message, each with your default. Ask only what would make the work wrong or irreversible if guessed; otherwise proceed on the default and record the assumption in the brief.
