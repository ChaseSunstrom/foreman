---
id: T-0003
type: FEATURE
tier: L
status: done
priority: normal
scope: [plugin/**, install.sh, setup-plugins.sh, README.md, configure-repo.sh]
depends_on: [T-0001, T-0002]
source: user
created: 2026-09-26T05:02:11Z
updated: 2026-09-26T05:35:08Z
---
# Phase 5: integration — install-user wiring, plugin decisions, CLAUDE.md, rules symlink, deny rules
## Raw request
> BUILD_PROMPT.md §3 Phase 5, §4.6, §4.7, §10, PLAN.md §8 §9
## Interpretation
Wire Foreman into ~/.claude reversibly and apply the approved plugin decisions: fm install-user / uninstall-user (statusLine wrapper with original saved, deny rules, CLAUDE_CODE_STOP_HOOK_BLOCK_CAP env for drive, CLAUDE.md marked block, ~/.claude/rules/foreman.md symlink, manifest of originals), install.sh step + original permission mode recording, plugin/uninstall.sh, configure-repo.sh ChaseSunstrom, README fixes (per-repo opt-out = default), setup-plugins.sh figures, disable superpowers/pyright-lsp/typescript-lsp/playwright/chrome-devtools-mcp/design/figma (ECC already off; plugin-dev after Phase 8).
## Assumptions (confidence)
## Acceptance criteria
- [x] install-user merges settings, CLAUDE.md block, rules symlink and manifest; second run is a no-op; uninstall-user restores the originals exactly; --dry-run changes nothing — verify with `python3 -m unittest test_setup`
- [x] real ~/.claude wired: statusLine wrapper renders original + hud + Foreman line; rules symlink loads; deny rules present — verify with `fm doctor (later) / manual checks`
- [x] approved plugin decisions applied and recorded — verify with `claude plugin list`
- [x] install.sh and setup-plugins.sh still run cleanly; uninstall.sh exists — verify with `bash -n install.sh setup-plugins.sh plugin/uninstall.sh; ./setup-plugins.sh --dry-run`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
Settings corruption: merge-only writes via atomic replace, backup before every change, manifest-driven exact reversal; tests on a fake HOME prove install→install (idempotent) and install→uninstall (original restored). Deny rules can't be live-tested destructively: only harmless matching commands are exercised; rm rules rely on documented syntax + guard. Rollback: fm uninstall-user, or tar -C ~ -xzf backups/claude-20260925-233203.tgz; claude plugin enable <id> for disabled plugins.
## Execution prompt
## Steps
1. [x] fmsetup install/uninstall (TDD on fake HOME)
2. [x] install.sh wiring + original mode recording, plugin/uninstall.sh, setup-plugins.sh figures, README fixes, configure-repo.sh
3. [x] Apply to the real ~/.claude (backup first) and verify statusline/rules/deny
4. [x] Apply plugin decisions (disable) and record
5. [x] Commit phase 5
## Resume here
## Verification evidence
- (step 1) `python3 -W error::ResourceWarning -m unittest discover -s plugin/tests -t plugin/tests` → 156 tests OK, no warnings; test_setup 9/9 (merge, idempotent, dry-run, foreign file refused, exact round trip, user changes kept, mode restore) (2026-09-26T05:33:16Z)
- (ac 1) `python3 -m unittest test_setup` → 9 tests OK (2026-09-26T05:33:16Z)
- (step 2) `bash -n install.sh setup-plugins.sh plugin/uninstall.sh; ./install.sh --help; plugin/uninstall.sh --help; ./setup-plugins.sh --dry-run` → all parse and run; commit 7a2715c (2026-09-26T05:34:06Z)
- (step 3) `fm install-user; plugin/hooks/statusline < sample.json; ls -l ~/.claude/rules/foreman.md; settings.json` → wired: statusline renders original + claude-hud (2 lines) + 'foreman · T-0003 FEATURE 3/5 · q3 · in0 · guard on · bypass'; symlink OK; 20 deny rules; env cap 60; CLAUDE.md block (2026-09-26T05:34:22Z)
- (ac 2) `statusline render + symlink + settings inspection` → all present and rendering (2026-09-26T05:34:22Z)
- (step 4) `claude plugin disable x7; fm install-user --record-disabled; claude plugin list` → superpowers, pyright-lsp, typescript-lsp, playwright, chrome-devtools-mcp, design, figma disabled (ecc earlier); 8 recorded in manifest; plugin-dev kept until Phase 8 (2026-09-26T05:35:08Z)
- (ac 3) `claude plugin list | grep disabled` → 8 plugins disabled and recorded (2026-09-26T05:35:08Z)
- (ac 4) `bash -n install.sh setup-plugins.sh plugin/uninstall.sh; ./setup-plugins.sh --dry-run` → parse OK; dry-run clean (2026-09-26T05:35:08Z)
- (step 5) `git log --oneline -2` → 95e4b59 feat(setup): record plugins Foreman disabled via fm install-user --record-disabled 7a2715c feat(setup): reversible ~/.claude wiring, uninstall.sh, install.sh wiring step (2026-09-26T05:35:08Z)
## Log
- 2026-09-26T05:02:11Z created
- 2026-09-26T05:02:11Z guard authorization added: core
- 2026-09-26T05:18:58Z set approved=True
- 2026-09-26T05:28:55Z focused
- 2026-09-26T05:34:06Z guard authorization added: core
- 2026-09-26T05:35:08Z done
## Follow-ups captured
