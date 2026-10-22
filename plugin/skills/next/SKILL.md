---
name: next
description: Use whenever you have finished, blocked or dropped a task, or the user says next or continue: closes it and starts the next queued one.
---

# Foreman: next

1. Close out the current task in one call: `fm task finish ID --audit "<how>" [--lens "<lens>: <result>" …] [--docs …] [--lesson …] [--commit "<message>"]` (or `fm task block` / `fm task drop ID "<why>"`). fm lists anything still missing — fix it or record evidence first. `--commit` commits only this task's files and only after the close succeeds: never chain `finish | tail … && git commit` (a pipe hides the refusal).
2. Triage the inbox (`fm state`): expand each captured item into a planned brief (`/foreman:intake` §2) or leave it captured with a note if it needs the user.
3. Re-plan checkpoint after a phase group or a structural change: re-read the remaining briefs, update scope, approach and Execution prompts to the new reality, `fm queue --replan`, and log what changed in each brief (`fm task set ID --section Log …` is automatic for field changes).
4. Show the queue in ≤ 10 lines (`fm queue`).
5. Next task = the first runnable item (`fm next` names it and its stage). If it needs approval (L tier, `?`, destructive) and isn't `approved`: standard autonomy → present the plan and stop; full autonomy → self-approve after the self-critique (`fm decide`, `fm task set ID approved=true`) and continue. Then `fm focus ID` and follow its Execution prompt.
6. Queue empty:
   - **FINAL VERIFY:** run the project's full verification (build, all tests, lint) fresh; `fm log final_verify '{"cmd":"…","result":"…"}'`. Then the session audit (`operator` + `adversary` over the whole session diff, `../intake/references/audit.md`); fix or capture what it finds.
   - **REFLECT:** `/foreman:reflect`.
   - Suggest `/foreman:tidy` if STATE says tidy is overdue.
   - Report what was done with evidence, in a few lines.
