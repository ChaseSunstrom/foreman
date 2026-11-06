Not directly related. I have sufficient evidence now. Let me finalize.

## Verdict: changes needed

## Findings

**MEDIUM** — `~/.claude/foreman/plugin/lib/fmdoctor.py:111-131` (`check_footprint`) and `~/.claude/foreman/plugin/rules/foreman.md:16,42,46,57` — The always-on rules-file budget (`RULES_MAX=80`) and MASTER.md's "cheap" claim (`~62 always-on instruction lines... it's cheap`, MASTER.md:31) are gated purely on **line count**, never on characters/tokens. Over T-0018's 10 rounds, several existing bullets in this same file were rewritten to be substantially denser rather than adding new lines: the evidence-and-state bullet (line 42) grew from `` `fm task evidence ID --step N "<cmd>" "<real result>"`. fm refuses done steps... `` (~140 chars) to a ~430-char multi-clause sentence covering `--run`, `fm check`, and the failed-run block; the "Plain words" bullet (line 16) gained two more mapped phrases (`fm sync on`, `fm repeats`) inline. Total line count is unchanged (still 60 lines, matching the "~62" figure), so `fm doctor`'s footprint check will keep reporting PASS/"cheap" even though the real per-session token cost of this always-on file has grown by roughly 20-30%+. Round 7 recognized character-based budgeting is the right tool for this exact problem and added `DESCRIPTIONS_MAX` (chars) for skill/agent/command descriptions (fmdoctor.py:127-128), but didn't extend the same treatment to `RULES_MAX`/`ALWAYS_ON_MAX`, leaving a real blind spot for exactly the kind of unnoticed growth this lens is asked to check. Fix: add a character/token budget alongside the line-count one in `check_footprint` for `rules_path` and the CLAUDE.md block. Confidence: high (verified by reading current file plus diff hunks for the before/after text).

**LOW** — `~/.claude/foreman/plugin/.claude-plugin/plugin.json:3` — still `1.1.0` after 10 feature rounds (fm sync, fm repeats, fm run --wait, audit-prep research seeding, folder-write guard category, doctor core-integrity check). Not gated by any doc or test found, so likely intentional (CHANGELOG's "Unreleased" section holds all of it), but worth confirming release process bumps this before the next tag. Confidence: low (no evidence this is expected to change per-round).

**Other observations** (not pursued further, out of this lens's core scope): `fm sync`'s per-repo `.foreman/` mirror is outside `~/.claude/foreman/state`, so `plugin/uninstall.sh`'s state-archive/removal never touches it — but this is explicitly handled by `fm sync off --remove` and documented (MASTER.md §9), so not a defect, just worth the user knowing uninstalling Foreman does not clean up `.foreman/` in any project repos.

## Acceptance criteria
No separate acceptance-criteria list was included in this brief beyond the lens's own check items; each was evaluated above:
- Install/uninstall round-trip for new state: met (uninstall archives/removes `state/` wholesale, covering audits/, research/, run.lock, sync-conflicts/; `.foreman/` mirror has its own explicit `sync off --remove`).
- Defaults match docs: met (`fm run --wait` default 6h at fmcli.py:724 matches CHANGELOG/MASTER; `fm check --timeout` default 600s; audit-prep lens-per-tier matches `references/audit.md`).
- Always-on context/startup cost don't grow unnoticed: not met — see MEDIUM finding above.
- Nothing installed/enabled without approval: met (plugin-folder guard extension, sync auto-enable-on-clone are both documented and gated as designed).
- Git operations land on intended branch: met (install.sh's main-branch/clean-tree pull guard untouched and still correct on this machine's `foreman/build` checkout; `fmguard.py`/`hook`'s committed-library fallback uses `HEAD` of Foreman's own repo, ignoring `GIT_*`).
- Versions/file maps/docs match code: met except the MEDIUM above; MASTER.md's file-map table row for `plugin/lib/` correctly lists new `fmrepeats`/`fmsync` modules.

## Not checked
Line-by-line correctness of the guard's shell-parsing/security logic (`fmguard.py`, `_tree_targets`, `_check_system`) beyond skimming — that's the security/adversary lens's job. `fmrepeats.py`, `fmwatch.py`, `fmdocs.py`, and the full test suites were not read in detail. Did not execute any commands (read-only review). `install.sh`, `setup-plugins.sh`, `reset-claude.sh`, `plugin/lib/fmsetup.py` were confirmed unmodified by this diff and read only enough to verify the round-trip/branch claims above, not audited in full.
