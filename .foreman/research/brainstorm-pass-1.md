# Brainstorm pass 1 (2026-10-04) — grounded slate

Source: research/brainstorm-20261004-013651 (4 lenses × 3 rounds, past the four earlier idea lists; 132 new titles). Pack: the user's words, what was built today, the open inbox, fm friction since the last pass.

## Grounded and kept (the slate)
1. Guard: `git stash list` / `git stash show` are read-only — fmguard.py:1350 puts every `stash` in _GIT_WORKTREE_WRITES, so a read-only listing is blocked as a tree write over core (2 blocks in today's friction). FIX S.
2. Repo integrity in fm doctor — a machine crash today left four zero-byte loose objects in .git/objects; `git diff` failed until they were moved aside and fm doctor passed throughout (no check looks at objects or truncated state files). Doctor check + `fm doctor --repair` that quarantines empty loose objects. FEATURE M.
3. S tasks that outgrow S — nothing notices an S task touching many files, so it skips M's plan gate and lens audits (fmcore next_action has no tier check). fm next tripwire. FEATURE S.
4. Shared-prefix child prompts — fmideas.child_prompt starts with "Lens: …", so sibling and later-round prompts share no prefix for prompt caching; put the pack first. PERFORMANCE S.

## Grounded and dropped
- Gate result cache by input hash / affected tests — exist (fm check reuses a pass on the same tree; --affected).
- Reviewer memory — exists (audit prep lists earlier findings per lens).
- Atomic state writes — write_atomic everywhere; the crash hit git objects, not state.
- "What changed since you left", hook watchdog, guard replay corpus — exist (T-0117, T-0087, T-0189).
- Drive waits without ending the turn — the harness re-invokes on a background notification; ending the turn is the cheapest wait.
- Token-free read-only answers — exist for status words (UserPromptSubmit answers from state).

## Kept for later passes (value, unclear premise or larger)
- Flake ledger / load-aware rerun for gates (one class failed once under load 27; cause unproven).
- Per-task token and wall-clock bill at close.
- Reviewer findings bound to regression seeds before close (done by hand in every batch today).
- Merge the bench-family inbox items (bench judge, skill duels, counterfactual ledger, regression court, shadow-user soak) into one pipeline batch.
