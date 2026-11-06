# T-2978 and T-2987: scenarios minted from real projects (2026-11-04)

## How it works
`sampo exam gen --from-repo PATH [--only GLOB] [--test-cmd CMD] --n N --seed S`:
- takes the repo's HEAD with git archive, so the checkout is never touched;
- links its untracked deps (.venv, venv, node_modules) into a throwaway copy;
- applies one deterministic mutation per candidate: a flipped comparison, a dropped guard, an off-by-one bound;
- keeps the mutation only when the project's own tests go red, and only if the unmutated copy passes twice.

Grading uses the same linked deps, environment and time cap.

## Live runs

| Project | Language | Test command | Tried | Kept | Missed by its tests |
|---|---|---|---|---|---|
| Sampo, `plugin/lib/sampo/lake.py` | Python | `python3 plugin/tests/run.py test_lake` | 7 | 4 | 3 |
| jarvis-code | TypeScript | `npm run test` (tsc, then node --test; 63 s a run) | 12 | 4 | 8 |

- **Louhi's check.** `sampo exam check` passes all 4 Python scenarios. On the TypeScript run, a first check (before the grading-copy fix) failed on `tsc: command not found`: the grading copy dropped the linked node_modules, now fixed. After that, one check passed all 4. A later check under load had one clean run fail in three, a flaky test in jarvis-code that the check correctly flags.
- **A side product: mutation scores.** jarvis-code's tests miss 8 of 12 one-line mutants, and test_lake misses 3 of 7. That is useful feedback for each project, and could become a `sampo` report of its own.

## Not mintable yet
- **trader** (Python, uv venv). Its suite takes over 15 minutes in a copy, and the "not slow" subset still takes over 10. Per-mutant runs need a narrower `--test-cmd`, or test selection by coverage.
- **volt and gitter** (Rust). Not attempted yet. One cargo target per run is in place, so only the first build is slow, but that first build may exceed the 120 s cap: give the green runs a longer cap.

## What this feeds
- The distilled actor (T-2971): real-code train scenarios across languages, graded by the projects' own tests.
- The verifier (T-2977): test-graded false-done negatives from exam closes.
