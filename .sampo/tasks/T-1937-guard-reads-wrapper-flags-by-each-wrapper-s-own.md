---
id: T-1937
type: SECURITY
tier: M
status: blocked
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T08:14:02Z
updated: 2026-10-29T08:20:32Z
base: 914eef1b8faf2b75b9e97faba5624c04b232e307
base_tree: b315a806e29e5a70e459b3c028d88b78f80366f7
plan0_at: 2026-10-29T08:18:00Z
plan0_scope: []
paused_tree: b315a806e29e5a70e459b3c028d88b78f80366f7
---
# Guard reads wrapper flags by each wrapper's own table: command -p, time -p, setsid -c, exec -a, stdbuf -o L and time -o hid rm -rf ~
## Raw request
> Guard reads wrapper flags by each wrapper's own table: command -p, time -p, setsid -c, exec -a, stdbuf -o L and time -o hid rm -rf ~
## Interpretation
Wrapper commands (sudo, doas, time, exec, stdbuf, nice, ionice, flock, timeout, env, setsid, command, builtin, nohup…) are stripped by one shared branch that assumes -n/-c/-p take values. Wrong per wrapper: 'command -p rm -rf ~', 'setsid -c rm -rf ~', 'nice -n 5'-style clusters, 'sudo -Eu root', 'flock F -c CMD', 'env -S CMD' hide the real program. Read each wrapper's options the way its getopt does, so the command it runs is the one judged.
## Assumptions (confidence)
## Acceptance criteria
- [ ] command -p, time -p, setsid -c, exec -a NAME, stdbuf -o MODE, /usr/bin/time -o FILE and -f FMT before rm -rf ~ are refused; nice -n, ionice -c and sudo -u still strip their values — verify with `python3 plugin/tests/run.py test_guard test_guard_evasions test_guard_exec_vectors`
## Non-goals
## Approach (options → choice → why)
Chosen: a per-wrapper table of value letters and long names (_WRAP_OPTS), read cluster-aware like _xargs_opts; flock -c and env -S hand their text back as sh -c / a re-split argv. Rejected: judge both readings (doubles every check, complex); refuse any unknown wrapper flag (over-refuses everyday sudo/nice lines).
## Risks and rollback
## Execution prompt
## Steps
1. [ ] Adversarial tests red, then per-wrapper value-flag table in _strip_wrappers, green; replay cases  <- CURRENT
2. [ ] Adversarial tests for every wrapper row (red), then the table (green), replay cases
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-10-29T08:14:02Z created
- 2026-10-29T08:18:00Z focused
- 2026-10-29T08:20:32Z blocked: Paused: a safety classifier stopped part of the design reply mid-task; left for the user to review before resuming
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1924-review: Verdict: changes needed.** One adversary finding is real and new. The relative-`cd` change lets a line pass that was refused before. I ran nothin…
- research T-0270-review-1: Verdict: changes needed.** The new code has one regression and several ways around it. I read the code only. I could not run commands, so every…
- research T-0338-review: Changes needed. I could not run anything (no execution tool), so each finding comes from tracing the code by hand. The two HIGH findings are bypa…
- decision 2026-10-22: T-1585: the guard refuses commands that name CLAUDECODE or CLAUDE_CODE_ENTRYPOINT to unset or override them, not a whole fresh environment (env -i, …
