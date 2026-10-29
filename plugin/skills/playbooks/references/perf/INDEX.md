<!-- Foreman's own index (written for Foreman, not ported). -->
# Performance playbooks: measure before and after

Paths are relative to the playbooks skill.

- `references/perf/profiling.md` — Find where the time goes before guessing: profilers per language, reading a profile, biggest frame first.
- `references/perf/benchmark-loop.md` — Making something faster, trying many variants, recursive optimization: baseline, one change, measure, keep or revert.
- `references/perf/benchmark-statistics.md` — Is the difference real? Noise band from repeated runs, equal budgets, wall time, ablation, raw runs kept.
- `references/perf/latency-critical.md` — Latency-sensitive systems (realtime dashboards, market data, streaming agents, execution paths): tail latency first.
- `references/perf/regex-backtracking.md` — A regex slow or hanging on long or hostile input: time an adversarial input, make the parts disjoint, or drop it.
