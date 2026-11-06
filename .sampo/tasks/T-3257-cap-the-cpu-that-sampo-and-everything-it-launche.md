---
id: T-3257
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-06T00:36:56Z
updated: 2026-11-06T00:36:56Z
steer_method_rate: 0.218
---
# Cap the CPU that Sampo and everything it launches may use. The default ceiling is 50% of…
## Raw request
> why cant you limit how much CPU usage this uses, like to 50% or something
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- Cap the CPU that Sampo and everything it launches may use. The default ceiling is 50% of total machine CPU, which is about half the cores. A single user-facing setting controls it (config key or env var, e.g. `max_cpu_percent`), and the user can raise, lower or disable it.
- The cap covers every CPU-heavy surface, not just the main process: spawned shell commands, test runs, builds, linters, type-checkers, indexers, subagents and parallel workers.
- Enforce the cap with real limits, not just advice. Prefer the strongest mechanism available, in this order:
- cgroup quota (`systemd-run --user --scope -p CPUQuota=…`)
- `cpulimit` or CPU affinity (`taskset`)
- lower priority (`nice`/`ionice`) as the fallback
- Also cap concurrency to match the budget. Worker, thread and job counts (`make -j`, `pytest -n`, `cargo`/`npm` parallelism, subagent fan-out) are set to the allowed core share, not to the full core count.
- Detect which mechanisms the platform supports, such as cgroup v2 availability, permissions and whether the tools are installed. Pick the best one automatically and tell the user which one is active. If none can enforce a hard cap, say so plainly instead of implying a limit exists.
- Measure to verify. Sample actual CPU use under a load run and report whether it stayed at or under the ceiling. Add a test or check that fails if the limit stops being applied to newly spawned work.
- Handle the tradeoffs openly. Say that capping slows wall-clock time. Let the user override the cap for a single command or session without changing the default.
- Document the setting, its default, how enforcement works per platform and its known limits (e.g. short bursts, I/O-bound work, children that escape the cgroup) in the README/config docs and in `--help`.
- Make the change directly in the harness instead of just explaining why it isn't there. The answer to "why can't it" becomes "now it can", with the current limitations stated.
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
- 2026-11-06T00:36:56Z created
## Follow-ups captured
