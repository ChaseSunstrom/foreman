---
name: reflect
description: Use after finishing a Foreman task or phase, after a block or a long back-and-forth, or when the user asks for a retro — records decisions, durable learnings (auto memory) and Foreman self-improvement ideas with evidence, without changing Foreman itself.
---

# Foreman: reflect

Short retro on the last task or phase. Evidence over opinion.
1. What happened: the brief's Log, evidence, guard blocks and stop-gate events (`fm watch --once`, the ledger via `fm resume`); across tasks, `fm friction` (the self-improvement digest since the last pass).
2. Ask: what caused back-and-forth? What did the user correct (`fm recall --corrections`; a repeated one is a durable preference: save it)? What did the guard block that the user then allowed? What took more than one verification attempt? What would a fresh session have needed to know?
3. Record, each in its own home:
   - Decisions (what, why, rejected alternatives) → `fm decide "<decision>" --why "…" --rejected "…" --task ID`.
   - Durable, project-specific learnings and gotchas → auto memory for this project (one line in MEMORY.md, detail in a topic file). No task status there.
   - Stable conventions the project should follow → propose a line for the project CLAUDE.md (≤ 150 lines; apply per autonomy).
   - Ideas to improve Foreman itself → `fm capture --self --source self --type <T> "<idea> — evidence: <what happened>"`. Never edit Foreman directly from here; `/foreman:improve` handles those.
4. Report in ≤ 8 lines.
