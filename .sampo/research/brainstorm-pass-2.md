# Brainstorm pass 2 (2026-10-04) — grounded slate

Source: research/brainstorm-20261004-020314 (4 lenses × 2 rounds, past pass 1 and three earlier lists; 82 new titles). Pack: pass 1's results and its friction (review passes kept finding real issues; a guard test passed for the wrong reason).

## Grounded and kept (the slate)
1. Hunk mutation proof — "mutation testing for the evidence", "detect vacuous verify commands by mutating the target", "make verification adversarial to itself". Today a guard test passed because a word scan caught a quoted path, not because the channel was handled; fm task prove only checks red→green for the whole diff (fmcli task_prove). New: revert each hunk of the task's diff alone in a scratch worktree and run the criteria's checks; a hunk whose removal fails nothing is unproven. FEATURE M.
2. Flake ledger in fm check — "make gate flakes observable before they are quarantined". One test class failed once under load today and nothing recorded which; fm check keeps only exit codes. Record the failing test names per run; a name that fails and then passes on the same tree is listed as flaky (never hidden: the failing run still fails). FEATURE M.
3. Typo help for fm — "suggest the nearest command on any fm typo or wrong flag". Steers today corrected wrong flags (run.py -k, fm research has no list verb); argparse prints only "invalid choice". difflib suggestions for subcommands and flags. FEATURE S.

## Grounded and dropped
- Post-crash reconciliation at session start — fm doctor integrity (T-0268) runs at every gate.
- Lint verify commands at write time — exists (T-0066); vacuous ones are what the mutation proof catches.
- fm since, calm/needs-you light, status-line progress — exist (T-0117, pane, statusline).
- Reviewer findings as a checklist — audit prep already lists earlier findings per lens.
- Pass-over-pass dedup of brainstorms — fm ideas --seen and "near T-… (done)" already do it.
- Negative-space check — the pre-audit co-change map already names files that usually change together.
- Process-group kill for children — run_command already starts a new session and kills the group on timeout.

## Merged into inbox pipelines (decision recorded)
- Review family: plan-time red team / opposing counsel → T-0233 (shadow plan review); with T-0230, T-0232, T-0235.
- Research family: T-0229, T-0239, T-0237, T-0238 build together.
- Bench family (decided in pass 1): T-0231, T-0240, T-0241, T-0242, T-0243 (+ the shadow-user soak idea here).

## Kept for later passes
- Guard tests with a parse-only twin (word scan off) — the payload rule from T-0270's lesson covers most of it.
- Learn standing answers from repeated replies; a taste file the user can edit; stall-based drive stop.
