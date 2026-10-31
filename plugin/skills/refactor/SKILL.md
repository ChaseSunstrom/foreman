---
name: refactor
description: Use whenever you refactor, simplify or delete dead code: pin behaviour first, then change in small steps.
---

# Foreman: refactor and clean up

A refactor changes structure, never behaviour. It is a CLEAN task: no brief yet → `/foreman:intake` first (the hooks refuse edits without one).

1. **Scope it with data.** `fm map` for the layout and hot files, `fm graph blast PATH` for what a change would touch, `fm sym PATH:NAME` for a definition and its callers. A repo-wide sweep → `../playbooks/references/clean/repo-sweep.md`.
2. **Pin what the code does today** when tests are thin: `../playbooks/references/clean/characterisation-tests.md`. The pins are committed before the first refactor commit and a refactor commit never edits them.
3. **Remove or simplify** with `../playbooks/references/clean/refactor-cleaner.md` (dead code, duplicates, unused exports: prove each is unused before deleting) and `../playbooks/references/clean/code-simplifier.md` (the smallest shape that does the same thing). A public name going away → `../playbooks/references/clean/deprecation.md`.
4. **One small step, one run.** `fm task evidence ID --step N --run "<the pins or the suite>"` after each; red → undo that step, don't patch forward.
5. **Bugs found on the way** are captured (`fm capture --source discovered`), not fixed inside the refactor.
6. **Close:** `fm check --affected --evidence ID`, then `fm audit prep ID` for one `foreman:fm-reviewer` pass. The diff should shrink or stay flat; a refactor that adds lines says why.
