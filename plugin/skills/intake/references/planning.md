# Planning: passes, tiers, brief, rubric (reference)

## Passes
- **R1 Expand:** interpretation, assumptions with confidence, testable acceptance criteria, scope paths, non-goals. M/L: flip the two assumptions the plan leans on most (what if each were false?) and note what would change; a flip that changes the approach is a question or a probe before building (T-0627).
- **R2 Ground:** read the real code, run the real commands, correct R1 against reality. M/L: list every approach worth weighing (three or more, including reuse of an existing tool and one unconventional), choose one, say why. A FEATURE M/L also gets a **capability sweep**: what a complete, best-in-class version in this space does (name the comparable tools); the expected ones go in scope, the rest are captured (`fm capture --source followup`) so the user doesn't have to ask for them one by one. Broad or exhaustive requests: `fm ideas --pack <file> --lens 'capability map' --lens approaches` for the sweep.
- **R3 Anticipate:** "If I ship this and the user reviews it, what are the three most likely follow-ups or complaints?" Each is either an implied requirement the user would obviously expect (in scope) or an adjacent idea (`fm capture --source followup`, not built). Implied requirements stay within what matters: validation at trust boundaries, data-loss handling, security, accessibility, explicit requests, tests and evidence.
- **R4 Compile:** the brief's Execution prompt, executable by a fresh session with no history. Regenerate it at every re-plan checkpoint.

## Tiers
| Tier | Signal | Depth |
|---|---|---|
| S | ~≤30 lines, 1–2 files, obvious approach, low risk | brief ≤ 10 content lines: R1 + light R2 + R4; still logged and verified |
| M | several files or a real design choice | full R1–R4, three or more approaches, capability sweep for a FEATURE |
| L | cross-cutting, schema/API/security-sensitive, large or uncertain | R1–R4 + adversarial self-critique + staged sub-tasks, each independently verifiable; `fm second plan ID` (another model reads the plan; its Plan review section is read before approving); optional `foreman:fm-reviewer` |
A request about a whole repo or "all …" (clean up everything, all docs) is never S. When unsure, go one tier up; tiers may change after R2 (`fm task set ID tier=M`, and say so).

## Brief (created by fm from templates/brief.md)
Frontmatter: id, type, tier, status (captured|planned|active|verifying|done|blocked|deferred|dropped), priority, scope, depends_on, source, allow (guard authorizations), approved, explore, created, updated.
Sections: Raw request · Interpretation · Assumptions (confidence) · Acceptance criteria · Non-goals · Approach (options → choice → why) · Risks and rollback · Execution prompt · Steps · Resume here · Verification evidence · Log · Follow-ups captured.
Confidence: M/L, state how likely the task holds on its first finish, `fm task set ID confidence=N` (0–100); `fm digest` scores it against what happened, and `fm focus` shows the track record and any caution for the scope first (T-0619). Assumptions: one bullet per fact, `fm task assume ID add "<fact>"` (`[assumed]`) and `fm task assume ID verify N` once checked (`[verified: how]` / `[false: how]`). Edit sections with `fm task set ID --section "<Name>" --text "…"` (or `--file`). Steps with `fm task step`, criteria with `fm task ac`, evidence with `fm task evidence`.

## Rubric (self-critique before executing M/L and before any gate; at most two revisions)
- Every acceptance criterion has a verification command?
- Could a fresh session execute the Execution prompt without asking anything?
- Anything in scope the user didn't ask for and wouldn't expect? Move it to INBOX.
- Anything the user would obviously expect missing? Add it.
- Simplest adequate approach? What would make it fail?
- Is rollback clear?

## Questions
Batch them into one message, each with your default. Ask only what would make the work wrong or irreversible if guessed; otherwise proceed on the default and record the assumption in the brief.
