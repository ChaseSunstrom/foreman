---
name: resume
description: Use after /compact, /clear, a crash, a new session, a preemption, or when the user says RESUME or "where were we" — restores the exact Foreman resume point (active task, current step, Resume here notes, Execution prompt) and continues from it.
---

# Foreman: resume

1. `fm resume` — active task, current step, the "Resume here" notes and the brief path. (SessionStart already injected a summary; this gives the full picture.)
2. Read the brief's Execution prompt and the current step. Compare "Resume here" with reality: `git status`, `git log --oneline -5`, the files it names.
3. State the resume point in one line: "Resuming T-0012 [FIX] at step 3/5: <step>."
4. If reality disagrees with the brief (uncommitted work missing, files changed), record what you found (`fm checkpoint --note …`) before continuing.
5. Continue with what `fm next` names (the harness derives it from the brief). If there is no active task, run `/foreman:next`.
