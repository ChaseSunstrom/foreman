# Round 7 brainstorm catalogue (2026-10-15)

Probe: `fm ideas` with reliability + delight, 2 rounds, past every earlier ideas.md (brainstorm-20261015-132957): 49 new titles, each grounded by three fm-recon passes (verdict, evidence, value 1–5, effort). The user then asked for a UI overhaul mid-round; that became T-0909 and a UI brainstorm of its own (brainstorm-20261015-134649, 43 ideas), whose overlap with round 7's delight ideas is noted below.

## Build (round 7 slate, value-for-effort order)
1. Bare `fm` inside a project answers "what now?": `fm next` and the status line; help outside one (PARTIAL: bare fm prints help, fmcli.py main) — value 4, S
2. The close tells you what's left: the undo line (git revert) and "nothing needed from you" when no criterion needs a check by hand (PARTIAL: undo exists in fm task revert output, not in finish) — value 3, S
3. `fm demo` ends with this repo's own next step when run inside a project (PARTIAL: a static "fm init" line, fmdemo.py) — value 3, S
4. `fm doctor` warns when state/ outgrows a budget, naming fm tidy (PARTIAL: tidy prunes; doctor checks only rule/CLAUDE.md size) — value 3, S
5. `fm night` holds a single-instance lease for its whole run (PARTIAL: fm run has one, fmserve.py:629; night takes only the short lock, fmnight.py:159) — value 3, S
6. `fm tidy` keeps a dated backup of the project's state files, the last 5 (GAP: refs/foreman/snapshots covers work, not state/) — value 3, S
7. `fm doctor` flags two Foreman installs at different versions (marketplace + install.sh) (PARTIAL: check_running_code catches a stale root, nothing compares versions) — value 3, S
8. Shell completion: `fm complete` prints verbs and live task ids, plus a bash/zsh hook (GAP) — value 3, M

## Folded into the UI work (T-0909 and its round 2)
#5 say why it's quiet (the pane's hero: "Nothing active", "no tool calls lately", the Up next card) · #1 a "caught it" moment (guard toasts exist; the pane's guard gauge) · #2 red→green beat (T-0909: a step glows as it gets done) · #9 band colour breathing (pulsing borders; the rail's comet) · close ceremony (T-0913)

## Later (premise holds; waits on evidence, design or cost)
reconcile tasks against git after resets (M, value 2) · per-verb crash-point enumeration (M) · stamp state writes with writer/version (M) · dead-man crash file (S, value 2) · last-known-good install and rollback (M) · upgrade rehearsal on a state copy (M) · `fm selftest` alias over doctor's hook bench (S; the installed copy lacks the tests folder) · exit codes labelled retryable/user/bug (S, value 2) · shuffled test order (S, value 2) · a hook error-rate SLO (M) · resume prefill in the composer (M; no mod API seen) · plain-words first-session band (M) · safe-to-close-the-lid light (M; needs a definition) · speakable slugs (M) · `fm digest --brag` (S, value 2) · "ship it" closes (policy change) · FIX case file (M, value 2) · route the remaining raw state writes through write_atomic (S, value 3; most are append logs)

## Done already
#13 two sessions editing one file (edit leases, fmbus.py:301-413, refused in PreToolUse) · #6 differential guard tests against real bash (test_guard_diff.py, T-0160) · #1 per-hook watchdog (hooks.json timeouts, onFailure block for the guard, the breaker) · refusals name what to do instead (fmguard messages)

## Skip (with reason)
atomic code-tree swap (L, value 1) · monthly state restore drill (needs backups first; value 1) · lock down after guard fail-opens (premise false: the guard fails closed) · rival-hooks CI matrix (L, value 2) · auto-bisect on red doctor (L, value 1) · reliability forecasting (L, value 1) · nightly chaos drill (L, value 1) · day time-lapse (L, value 2) · fm gift (L, value 2) · doctor fortune (value 1) · go calm when frustrated (hard to tune, value 2) · personal bests (value 1) · bug graveyard (value 1) · fm wrapped (fm digest --days covers it)

Yield: 8 grounded builds (≥ 3), mostly S at value 3: not dry, but the curve keeps flattening (round 5: 7 of 54, round 6: 6 of 49, round 7: 8 of 49, value mostly 3).
