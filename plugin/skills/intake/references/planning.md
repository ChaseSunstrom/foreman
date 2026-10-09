# Planning: passes, tiers, brief, rubric (reference)

## Passes
- **R1 Expand:** interpretation, assumptions with confidence, testable acceptance criteria, scope paths, non-goals. M/L: flip the two assumptions the plan leans on most (what if each were false?) and note what would change; a flip that changes the approach is a question or a probe before building (T-0627).
- **R2 Ground:** read the real code, run the real commands, correct R1 against reality. Before trusting a library's docs, probe the installed version (`fm deps --calls` lists versions and import sites; its source or `--help` beats a web page about another version). For prior art, `fm recall --repos <identifiers>` searches other opted-in projects, and `fm recall --explain "<question>"` cites where its names are defined (T-0594, T-0618, T-0659). M/L: list every approach worth weighing (three or more, including reuse of an existing tool and one unconventional), choose one, say why. A FEATURE M/L also gets a **capability sweep**: what a complete, best-in-class version in this space does (name the comparable tools); the expected ones go in scope, the rest are captured (`fm capture --source followup`) so the user doesn't have to ask for them one by one. Broad or exhaustive requests: `fm ideas --pack <file> --lens 'capability map' --lens approaches` for the sweep.
- **Steps (R2):** order by risk and information. Spikes and unknowns go first: a `Spike:` step is throwaway, and its result is a note or a verified assumption, never shipped code. Ask a person as early as you can. Reversible work comes before irreversible work (deploy, migrate, delete, release); `fm focus` flags the reverse order. A FEATURE L's first step is a walking skeleton: the thinnest end-to-end path, behind a failing acceptance test. Each step ends in one observable result. Obligations: every FIX has contain, cure and inoculate steps; every migration or data change has a cleanup step and a rollback step; an L names its rollback in Risks and rollback (finish warns without one). A step can say what its check should print, `(expect: TEXT)`; `fm task evidence --step N --run CMD` marks the run ✓ or missed (T-0596). A step can name its contract, `(produces: PATH, …)` and `(requires: PATH, …)`; `fm focus` flags products that already exist and requirements nothing makes (T-0666). Steps that similar past plans had to add late come back in Related at focus (T-0645). A step can cite the assumption it rests on as `(A2)`. An assumption can carry its kill criterion, `fm task assume ID add "<fact>" --kill "<what would show it false>"`; `fm next` lists open ones. In Approach, each option says what would change your mind about it. When the choice was close, `fm second plan ID --role devil` argues for the option you rejected (T-0631, T-0609). If A2 turns out false, `fm next` names those steps for a replan, and so does `fm surprise` on an active M/L task (`fm task log ID "replan: …"` answers it). Recipes: `decomposition.md` (T-0623–T-0626, T-0603, T-0643).
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
