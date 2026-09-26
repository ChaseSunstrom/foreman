---
description: Build Foreman (or resume building it) from ~/.claude/foreman/BUILD_PROMPT.md
argument-hint: "[optional extra instructions for this run]"
---
Build Foreman.

1. Read `~/.claude/foreman/BUILD_PROMPT.md` in full. It is the spec: follow it exactly, including its settings block and Appendix A.
2. If `~/.claude/foreman/local/PLAN.md` exists, this is a resume. Read `local/PLAN.md` and `local/recon.md`; if Phase 2 is finished, run `fm state` for the `foreman` project. State the resume point in one line, then continue from there.
3. Otherwise, start at Phase 0.

Extra instructions for this run (may be empty): $ARGUMENTS
