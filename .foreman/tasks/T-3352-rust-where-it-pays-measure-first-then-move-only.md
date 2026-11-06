---
id: T-3352
type: PERFORMANCE
tier: M
status: captured
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-06T05:33:13Z
updated: 2026-11-06T05:33:13Z
---
# Rust where it pays: measure first, then move only the measured hot path. Candidates: (1)…
## Raw request
> Rust where it pays: measure first, then move only the measured hot path. Candidates: (1) the per-tool-call hooks (PreToolUse guard, PostToolUse attribution) start a fresh python3 every call (~50+ ms each, x every tool call of every session and builder): try a resident hook process first (the T-3297 fork-server idea applied to hooks), and port the guard's command parser to Rust only if the resident process still leaves it slow; (2) any scan over the 300,000-file state or the test-selection graph that a profile shows CPU-bound after its algorithm is fixed. Constraints: the plugin must still work with python3 alone (a prebuilt binary is an optional speed-up with a pure-Python fallback, never a requirement), and builds come from CI, not a toolchain on the user's machine. Bench numbers before and after (bench_hooks, perf_bench). Tonight's big wins were algorithmic, not language: sync export 6-8 s → 0.4 s (T-3349). User: 'could we/should we start writing/rewriting stuff in Rust that will massively help with performance?'
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-06T05:33:13Z created
## Follow-ups captured
