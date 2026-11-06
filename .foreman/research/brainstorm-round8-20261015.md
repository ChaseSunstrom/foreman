# Round 8 brainstorm catalogue (2026-10-15)

Probe: `fm ideas` with performance + simplicity, 2 rounds, past all 31 earlier idea indexes (brainstorm-20261015-143454): 45 new titles, 33 of them marked near a finished task. Grounded in the main thread (reads and timings; the rest were near-duplicates of shipped work).

## Build
1. Say plainly that the Codex, Gemini CLI and opencode adapters are built to those tools' documented hook formats but not yet verified against live CLIs (T-0335–T-0337 are blocked on exactly that): README and `fm agents install` output — value 3, S

## Later (premise holds, value ≤ 3)
skip `fm doctor` checks whose inputs haven't changed (doctor takes ~9 s and is a gate; a cache risks a stale pass) · nudge whole-file Writes that change under 10% of a file (Claude Code's own prompt already steers to Edit) · shape unbounded Grep/Glob calls · make tidy backups incremental (5 × a few MB today) · key the pyc cache by tree hash · a state-version floor that deletes old readers · stop committing demo recordings (each take adds ~4 MB; README needs them inline) · one non-interactive contract for installer and fm prompts

## Done already or measured fine
`fm complete` 72–112 ms and bare `fm` ~320 ms (no budget needed) · recording-only hooks already async (4 in hooks.json) · per-turn injection budgets (doctor's injection check) · hook latency from real runs (doctor's hook SLO) · one install (T-0923 doctor check) · local paths in tracked files (doctor's git hygiene, T-0836) · cost of work snapshots (3 s budget, 14-day prune)

## Skip
resident hook server, prefetching gates, warm spare children, tmpfs tier, cold-cache bench, motion from frame lag (wild, L or speculative) · `--because` waiver for every escape flag, one standing-rule store, lib file ratchet, verb-path distillation, deletion tasks per Claude Code release, reading-order tour (large churn for little user value) · derive versions from one tag, move root files under docs/, a surface-delta trailer, a two-minute-rule tour, one-page product page, fixture repos from specs, feature toggles by file (process changes with no user-visible gain)

Yield: 1 grounded build of value 3, no value-4+ ideas: dry. The recursive loop stops here.
