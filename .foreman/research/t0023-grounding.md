# T-0023 grounding: project-specific skills/tools for repetitive work (2026-09-26)

## What Foreman already records
- Ledger events (this project, ~700 events): step_done 66, step_add 64, task_set 61, ac_check 58, audit 37, subagent 35,
  touched 33 (edits only). Bash commands are NOT recorded in the ledger; evidence commands in briefs are the only
  record of what was run, with real results.
- Evidence commands repeat heavily: `python3 -m unittest <module>` (dozens of variants), the full suite with
  -W error::ResourceWarning (4), `plugin/tests/e2e/roundtrip.py` (4), `bench_hooks.py --runs N` (5), `fm doctor` (4),
  `bash -n install.sh … ; ./setup-plugins.sh --dry-run` (2), fm-reviewer lens runs (many).
- Related self-inbox items: T-0024 `fm task evidence --run` (run + record real output), T-0025 `fm check` (the
  project's gate commands in one call), T-0026 `fm audit prep` (diff + reviewer briefs).

## Claude Code mechanisms
- Project skills: `<repo>/.claude/skills/<name>/SKILL.md` (frontmatter name + description; description is always-on
  context in every session in that repo, ~20-60 tokens each). Project commands: `.claude/commands/*.md`.
  Agents: `.claude/agents/*.md`. Scripts: plain files in the repo (no always-on cost).

## Options
A. `fm repeats`: mine evidence commands (normalized: T-ids, paths, numbers) across briefs+archive; report shapes
   seen >= 3 times in >= 2 tasks; the reflect stage / `fm next` suggests one conversion per task: a project check
   (`fm check` config, T-0025) for gate commands, a script for multi-command sequences, a project skill for
   procedures (steps + judgement). Creation is a normal task (S), skills need the user's yes only if always-on.
B. Record every Bash command in PostToolUse (async) and mine those. More signal, but writes on every tool call and
   stores command text (secrets risk; redaction needed). Rejected for now.
C. LLM-only: at reflect, ask Claude "what did you repeat?". Cheap, but not evidence-based; keep as a prompt line in
   the reflect procedure alongside A.

## Recommendation
A + C, built on T-0025 (`fm check`) and T-0024 (`--run`): most repetition here is "run the gates", which `fm check`
solves directly; `fm repeats` finds the rest and proposes skills/scripts with counts as evidence.
