# fm code brainstorm catalogue (T-1331, round 1)

Source: research/brainstorm-20261020-222518 (fm ideas, 10 lenses, 4 rounds, 3 deepened; 522 distinct ideas). Grounded in two halves by independent agents: runners, setup, reliability, projects (R1–R25: 451 ideas) and the app experience (U1–U25: 236 ideas); the 71 UI ideas the runners half handed over are in the UI half, so every idea is placed. Marks: build (a brief follows), planned (an existing task covers it), skip (reason given).

# fm code brainstorm: runners, setup, reliability, projects and self-improvement

Source: brainstorm-20261020-222518/ideas.md (522 ideas). This half: 451 ideas in 25 clusters. The other 71 (pure UI, visual, motion, TUI layout) are listed at the end and left to the UI half.
Grounding is against plugin/lib at 038047b8. Value is 1-5 to the user. Effort is S/M/L. Planned tasks: T-1327 nested quiet, T-1328 runner registry, T-1329 live progress, T-1330 app home and --task, T-1332 self-started rounds.

| id | capability | ideas | grounding | value | effort | risk | mark |
|---|---|---|---|---|---|---|---|
| R1 | Nested Foreman: worker and planner sessions run without Foreman's own context | 12 | planned T-1327 | 5 | S | low | planned T-1327 |
| R2 | Lean workers: cut and show the startup tax | 16 | partial | 5 | M | med | build |
| R3 | One live Foreman when it's installed twice (plugin, dev checkout) | 8 | partial | 3 | S | low | build |
| R4 | Runner registry: any CLI or model, detected, with one config line | 17 | planned T-1328 | 5 | M | med | planned T-1328 |
| R5 | Preflight: probe each runner and the project before the first request | 13 | partial | 5 | M | low | build |
| R6 | Liveness: live progress and a first sign of life | 13 | planned T-1329 | 5 | M | low | planned T-1329 |
| R7 | Stall detection and diagnosis (fm code why) | 18 | partial | 5 | M | low | build |
| R8 | Process lifecycle: no orphans, clean stops | 14 | partial | 4 | S | low | build |
| R9 | Durable runs: journal, resume, recovery | 19 | partial | 3 | S | low | build |
| R10 | Limits, rate limits and failover across runners | 15 | partial | 4 | M | med | build |
| R11 | Cost: price, record and cap what fm code spends | 9 | partial | 3 | S | low | build |
| R12 | Routing and runner evaluation | 24 | partial | 3 | M | med | build |
| R13 | Config: one resolved, explained, validated set of settings | 38 | partial | 4 | M | low | build |
| R14 | Install, first run and doctor (fm on PATH, the first request works) | 25 | partial | 5 | S | low | build |
| R15 | Entry point and CLI grammar | 14 | partial | 3 | S | low | build |
| R16 | Multi-project home and project resolution | 29 | planned T-1330 | 4 | S | low | planned T-1330 + build extension |
| R17 | Unattended and cross-project work management | 33 | partial | 4 | M | med | build |
| R18 | Self-improvement triggers: Foreman starts the round itself | 31 | planned T-1332 | 4 | S | low | planned T-1332 + build extension |
| R19 | Worker isolation and safety | 12 | partial | 3 | M | med | skip |
| R20 | Proof and verification quality | 17 | done (mostly) | 2 | M | low | skip |
| R21 | Intake and planning | 25 | partial | 3 | M | med | skip |
| R22 | Continuity: follow-ups and handoff between runners or sessions | 14 | partial | 3 | S | low | build |
| R23 | Integrations and surfaces beyond the terminal | 17 | partial | 2 | M | med | skip |
| R24 | Model quality: local and small models, context, structured output | 9 | partial | 3 | S | low | build |
| R25 | Harness tests and observability: misbehaving fakes, replay, drift | 9 | partial | 4 | S | low | build |

## R1. Nested Foreman: worker and planner sessions run without Foreman's own context

**Grounding (planned T-1327):** fm code marks its CLIs with FOREMAN_WORKER_OF (fmcode.py:525, :1118), read only by the lease bus (fmbus.py:38). FOREMAN_QUIET=1 already turns every hook but the guard off (fmhooks.py:47-49) and fm bench uses it (fmbench.py:428), but fm code never sets it: T-1327 sets it for workers and planners, and this applies to codex/gemini/opencode too, because their Foreman hooks go through the same fmhooks (fmagents.py:1-4). Detecting nesting by process ancestry (297) adds nothing once the env marker is set, so it's covered by the marker.

**Score:** value 5 · effort S · risk low · **planned T-1327**

**Brief:** Build as planned. Add one criterion: fm code's start event says 'nested sessions: guard only', so the user can see it's on. Test: a fake CLI that records its env sees FOREMAN_QUIET=1 and FOREMAN_WORKER_OF.

Ideas (12):
- Detect Foreman-inside-Foreman at the process level (#18)
- Show a lineage badge for who is running whom (#32)
- Stop nested Foreman with a depth marker (#74)
- Detect and refuse duplicate Foreman when run as a Claude plugin worker (#118)
- Detect and collapse duplicate Foreman by a lineage marker in the process environment (#212)
- Detect the harness by process ancestry, not only the env marker (#297)
- Refuse to nest by one environment variable (#322)
- Adopt a "lineage" env marker so any Foreman-in-Foreman collapses to one owner (#333)
- Refuse a second Foreman when the worker is Claude Code with the plugin loaded (#360)
- Gate every worker launch on a lineage env marker, not a detection heuristic (#415)
- Pin down the nested-Foreman depth marker at the environment and process level (#430)
- Detect Foreman-in-Foreman by a marker in the environment and lease (#499)

## R2. Lean workers: cut and show the startup tax

**Grounding (partial):** The planner and worker CLIs run with the user's full Claude setup: every plugin, MCP server and user setting (fmcode.py:61, :68). That's where the 66k-133k input tokens per call come from. Foreman already has a lean, guarded launch: fm bench's bare arm passes the guard hook in --settings with --setting-sources project,local (fmbench.py:343-352, T-0963), and fm ideas adds --strict-mcp-config with an empty --mcp-config (fmideas.py:51). Each call's input tokens are already recorded (fmcode.py:288-293, fmmodels.py:381-383), but nothing keeps them per runner or shows them before a launch. T-1327 only switches Foreman's own hooks off.

**Score:** value 5 · effort M · risk med · **build**

**Brief:** Done when the claude planner and worker launch lean by default (the user's plugins and MCP servers dropped, Foreman's guard kept through --settings, as fm bench's bare arm does), one config line turns lean off, and the first call's input tokens are kept as that runner's startup tax and shown before the next launch. Test: a recording fake claude sees the lean flags and a --settings file that holds only the PreToolUse guard; a nested Bash the guard refuses is still refused; the token count lands in the runner record.

Ideas (16):
- Slim nested workers by default (#3)
- Quote the startup tax before a worker runs (#29)
- Measure and cap the worker launch tax (#42)
- Run workers in a lean, isolated profile (#53)
- Run nested workers with a bare profile by default (#84)
- Wild: Offer a "token diet" profile that reports and trims what nested workers load (#125)
- Show what the first call is loading, live (#157)
- Keep one resident worker session per project and runner (#179)
- Probe every runner for its real startup tax (#236)
- Wild: Offer a "token diet" profile for nested Claude (#245)
- Show the money before it burns: a startup-tax estimate per runner, per project (#261)
- Run workers bare by default (#323)
- Give each worker CLI a measured "startup tax" that gates the launch (#338)
- Set a per-runner startup budget in config and enforce it (#370)
- Show the startup tax before launching a worker, and offer the lean profile (#389)
- Run a startup-tax doctor that trims nested CLI cost (#503)

## R3. One live Foreman when it's installed twice (plugin, dev checkout)

**Grounding (partial):** fm doctor WARNs when two Foreman installs exist (check_dual_install, fmdoctor.py:422-441) and when a session ran older code than is installed (check_running_code, fmdoctor.py:454-481). fm code and the TUI never show either. Unclear: whether a doctor check catches the same hooks registered twice (plugin hooks plus settings.json hooks). None of the checks read in this pass does.

**Score:** value 3 · effort S · risk low · **build**

**Brief:** Done when fm code's start event names the Foreman running it (root and version), and the run warns once when the doctor's installs or running-code check would WARN. Also add a doctor check for Foreman's hook registered twice. Test: a fake second install in a temp home makes fm code --json carry the warning.

Ideas (8):
- Detect duplicate Foreman installs and fix them (#41)
- Detect duplicate Foreman installs and name the live one (#95)
- Detect duplicate Foreman installs and choose one owner (#237)
- Make duplicate-Foreman detection a visible fact, not just a silent fix (#268)
- Wild: Ship Foreman as one file that deletes itself from the plugin copy (#330)
- Detect which Foreman is live across plugin, pip/pyz and dev checkout (#364)
- Name the duplicate-Foreman fact on screen (wild) (#395)
- Detect duplicate Foreman and say who wins (#516)

## R4. Runner registry: any CLI or model, detected, with one config line

**Grounding (planned T-1328):** WORKERS and PLANNERS cover claude, codex, gemini and aider, plus custom 'CMD {prompt}' templates (fmcode.py:60-71, :764-775). The template is split with shlex and the prompt substituted per argv word, so 475 is already done. fm session knows the streaming argv for claude, codex, gemini and opencode (fmsession.py:27, :77-84), and fm agents installs Foreman's hooks and an instructions block into codex, gemini and opencode (fmagents.py:18), which is part of 183/167. T-1328 makes one registry (adding qwen, cursor-agent and custom runners), picks the default automatically and adds a config line. Not planned: learning an unknown CLI from --help or by watching, ACP, importing other tools' configs, human or rubber-duck runners.

**Score:** value 5 · effort M · risk med · **planned T-1328**

**Brief:** Build as planned. Skip the extras: a template learned from --help could grant shell access unattended (risk high), and ACP needs a protocol client that isn't stdlib (L). Revisit once the registry exists.

Ideas (17):
- Wild: A "rubber duck" runner that only asks questions (#13)
- Learn a runner from its own `--help` (#63)
- Speak Agent Client Protocol to agent CLIs (#66)
- Collapse runner setup to zero questions plus one line (#82)
- Teach Foreman an unknown CLI by probing it (#99)
- Import runner config from other tools (Claude settings, Aider config, Codex config, env API keys) (#121)
- Write one rules file per CLI from a single source (#167)
- Describe runners as data manifests (#182)
- Project one rules source into each CLI's native instruction channel (#183)
- Define runners as 8-line spec files (#198)
- Import runners from the tools already on the machine (#239)
- Learn an unknown CLI from its help text (#240)
- Learn a new CLI by watching you use it once (wild) (#306)
- Describe runners as 8-line data manifests and ship five (#418)
- Reject shell-string runner templates and pass the prompt as argv (#475)
- Define runners as 8-line manifests, learned by probing (#505)
- Run a runner that is a human (#509)

## R5. Preflight: probe each runner and the project before the first request

**Grounding (partial):** Local servers are probed for reachability only (GET /models, 0.3 s; fmmodels.py:149-160). The plan's verify commands are checked for runnability (fmcore.unrunnable via _plan_problem, fmcode.py:1175). Nothing checks that a CLI is logged in, accepts its flags, or answers at all, so a broken default fails minutes in, as it did for the user. The TUI's picker lists only CLIs found on PATH (fmcodetui.py:1336-1340).

**Score:** value 5 · effort M · risk low · **build**

**Brief:** Done when fm code runners --check (and the app's first launch) runs a tiny bounded prompt through each runner and sorts it into ok / not logged in / flag refused / endpoint down / no answer in N s, plus latency and CLI version. The result is cached as a capability card until the version changes, and fm code refuses a failing default before planning, naming the fix. Test: fake CLIs that exit 'not logged in', hang, reject a flag, or answer, each get the right status. Depends on T-1328.

Ideas (13):
- Preflight the runner before the first request (#2)
- Preflight a project before the first run (#17)
- Probe every runner into a capability matrix (#43)
- Probe each runner before the first real request (#55)
- Preflight every runner with a one-token probe (#70)
- Preflight every runner before its first real call (#93)
- Run a preflight "can this runner work here?" probe per project and runner (#119)
- Give every runner a one-line "hello" on selection (#276)
- Probe a project on first open and write its setup card (#361)
- Preflight "can this run work here?" before the first model call (#362)
- Derive a project's gates from its own CI files (#476)
- Probe each runner with a canary before real work (#491)
- Probe every runner for real and cache a capability card (#514)

## R6. Liveness: live progress and a first sign of life

**Grounding (planned T-1329):** Today a CLI's turn is silent until it exits: the planner's communicate() (fmmodels.py:359) and the worker's run_bounded (fmcode.py:679). fm session already parses claude, codex, gemini and opencode stream events (fmsession.py:114), so T-1329 can reuse that. T-1329 covers streaming activity and a heartbeat.

**Score:** value 5 · effort M · risk low · **planned T-1329**

**Brief:** Build as planned, with one more criterion (385/416/332): a 'launched' event naming the runner, pid and what it waits on comes out within 1 s of spawn, before any model output, so no screen is ever blank. Test: a fake CLI that sleeps before printing still yields the launched event first.

Ideas (13):
- Print a heads-up when the run is waiting on the CLI, not on you (#39)
- Make a run's first 30 seconds visibly alive (#129)
- Make every silent minute self-explaining with a live "what it's waiting on" line (#141)
- Trust the first minute: show "alive" evidence before any model answers (#258)
- Show the first-call wait as a named countdown (#271)
- Tail the CLI's own session transcript for progress (#296)
- Show a single "last heard from the runner N s ago" line (#327)
- Wild: Make "nothing happening" impossible by running the worker visibly in a split (#331)
- Make `fm code` a launch-time contract: a 10-second "first sign of life" SLA (#332)
- Make the first-sign-of-life deadline a failing test (#385)
- Make the wait feel like a workshop with a "what it's doing" line from the process itself (#397)
- Show a 10-second sign-of-life contract with a named wait (#416)
- Add a first-byte deadline to every runner launch (#424)

## R7. Stall detection and diagnosis (fm code why)

**Grounding (partial):** fm code has no stall concept: a turn waits up to --worker-timeout (1200 s, fmcode.py:55) with no word. Foreman has the parts elsewhere: fm run calls a session stalled when its transcript stops moving (_watch/_transcript_mark, fmserve.py:512-541), and heartbeats with stale_beats and a doctor check (fmserve.py:656-690, fmdoctor.py:943). There's no fm code why and no diagnostic bundle.

**Score:** value 5 · effort M · risk low · **build**

**Brief:** Done when a runner with no output, stream event or transcript growth for N s (a config setting) gets a 'stalled' event with a named cause: no bytes since launch, waiting on a terminal prompt, rate-limit text, or the process idle on CPU. The run offers retry, switch runner or stop, and fm code why prints the current or last run's state, its last event and the probe. Test: a silent fake is flagged with the right cause; a slow-streaming fake is not. Depends on T-1329 for the stream signal.

Ideas (18):
- Diagnose a silent run in the first ten seconds (#1)
- Diagnose a silent run before the user asks (#14)
- Diagnose silent runs and say why (#40)
- Diagnose stalls and offer a fix (#54)
- Add a stall watchdog with a named diagnosis (#68)
- Add one `fm code why` command that answers "is it doing anything?" (#83)
- Add a silence watchdog that diagnoses and acts (#94)
- Ship `fm code why`: one command that explains the last run or the current silence (#145)
- Ask for a mid-run status in plain words (#159)
- Run a silence watchdog that classifies why a run is quiet and acts (#213)
- Add a one-line `fm code why` plus a shareable diagnostic bundle (#220)
- Export a one-paste bug report for Foreman's own failures (#265)
- Wild: Environment fingerprint that explains "works here, not there" (#319)
- Run every child non-interactive and name the prompt it hangs on (#401)
- Name the silence with a stall classifier (#425)
- Classify silence with a stall doctor (#490)
- Detect a silent runner and say so within 20 seconds (#504)
- Make the stall watchdog a config policy, not a hope (#521)

## R8. Process lifecycle: no orphans, clean stops

**Grounding (partial):** Mostly done. Each worker turn runs in its own process group, killed at the end, and on Linux fm code is subreaper of everything it started (fmcode.py:679-760). The CLI planner's group is killed on timeout or stop (fmmodels.py:358-366), SIGTERM/SIGHUP unwind (T-1326, fmcode.py:1009), TUI quit stops the run (fmcodetui.py:1228, :1263), and the terminal is restored (fmcodeterm.py:203). Missing: survivors after a SIGKILL or crash of fm or the TUI, and macOS has no subreaper. fm ideas already keeps a start-time-checked child registry swept later (fmideas.py:96-200), but fm code doesn't use it.

**Score:** value 4 · effort S · risk low · **build**

**Brief:** Done when every runner fm code spawns is registered (pid plus start time) in the registry fm ideas uses, and the next fm code or app start kills and reports survivors. Test: kill -9 fm code while a fake CLI holds a forked grandchild; the next fm code start reaps it and says so, and a reused pid with a different start time is left alone.

Ideas (14):
- Reap orphans after a hard kill (#56)
- Reap orphaned runners with a process registry (#67)
- Make one process group the unit of a run (#85)
- Reap orphans and offer to resume interrupted runs (#98)
- Route every runner launch through one `spawn_runner()` (#197)
- Make Enter cancel-safe: Ctrl-C always returns a summary and leaves no processes (#260)
- Run each worker in a systemd user scope when available (wild) (#307)
- Outlive the harness's death: pdeathsig plus a sidecar reaper (#310)
- Judge liveness by a lease, not a PID (#311)
- Bound runner output with a ring buffer that spills to disk (#316)
- Reap children with a process-group lease, not a PID list (#423)
- Run every runner in a process group with a parent-death reaper (#426)
- Repair the terminal after any death (#432)
- Put every spawned CLI in one process group with a lease file (#489)

## R9. Durable runs: journal, resume, recovery

**Grounding (partial):** Done: every message and action is journaled, and fm code --resume rebuilds the run (fmcode.py:4, :1027, :1285-1331), with tests for a killed run and a kill between calls (test_code.py:295, :314). TUI 'r' resumes (fmcodetui.py:1271). Missing: a kill during planning loses the plan, since events wait until the task exists (fmcode.py:236). Nothing offers an unfinished run on the next start. A run can't outlive the TUI, because quit stops it (fmcodetui.py:1228).

**Score:** value 3 · effort S · risk low · **build**

**Brief:** Done when fm code (and the app's home) names each unfinished journal on start, e.g. 'T-x stopped at step 2/3: fm code --resume T-x', and the kill tests cover every station boundary (plan made, task made, each step, fix round, close) with no duplicate task or commit. Skip the supervisor daemon and sentinel (97/210/498, L): fm run and T-1330's detached runs cover running without a viewer.

Ideas (19):
- Resume any interrupted run exactly where it stopped (#6)
- Survive the closed lid: resumable runs (#19)
- Journal every run so `fm code --resume` continues after a crash (#69)
- Kill the process at random points and compare the end state (#78)
- Run a supervisor daemon so the TUI is only a client (#97)
- Let Foreman keep a "last session" so reopening resumes the thing you were doing (#147)
- Store run ledgers in git refs so they travel with the repo (#187)
- Write a run journal and resume from it (#192)
- Wild: Quarantine a crash loop into safe mode (#196)
- Make fm code a persistent supervisor daemon with the TUI as a thin client (#210)
- Wild: Take over a project the user abandoned: "what was I doing here?" (#256)
- Remember a run's last words when the terminal closes (#275)
- Make a project's "resume point" a first-class object across app launches (#336)
- Greet with a one-line "welcome back" that names where you left off (#396)
- Journal each step before acting so a run can resume (#427)
- Kill-at-random-point chaos test in CI (#428)
- Wild: Make a self-healing safe mode after a crash loop (#434)
- Make the run journal the single source of truth (#488)
- Wild: Let a sentinel process supervise the TUI and the runs (#498)

## R10. Limits, rate limits and failover across runners

**Grounding (partial):** fm code has --max-steps, the worker timeout, a 120 s command timeout, and --escalate after 3 fix rounds (fmcode.py:53-55, :1236-1240). Model calls retry 429/5xx 3 times, waiting at most 20 s (fmmodels.py:54). fm run already spots Claude's usage-limit text and waits (--wait), or hands a task packet to codex, gemini or opencode (fmserve.py:30, :302-317), but fm code does neither. It has no whole-run deadline or no-progress limit and no fallback chain.

**Score:** value 4 · effort M · risk med · **build**

**Brief:** Done when fm code sorts a runner's failure (usage limit with reset time, auth, crash, timeout), waits out a usage limit up to a configured cap and resumes from the journal, and otherwise falls back to the next runner in a configured chain, with the reason recorded. A whole-run deadline stops and blocks cleanly. Test: a fake that prints Claude's usage-limit line then succeeds is waited on; a fake that keeps failing falls over to the second fake; both are visible in the events.

Ideas (15):
- Budget and cap nested planner calls (#71)
- Fall back across runners on classified failures (#72)
- Let one sentence reroute a running task to another runner (#135)
- Pause on a runner's usage limit and resume at reset (#168)
- Give every runner call a deadline, token ceiling and /proc probe (#181)
- Wild: A "second opinion" button that sends the stuck step to another runner (#267)
- Spend-aware retry budget for endpoint calls (#315)
- Put a time and money box in the request (#374)
- Hand off a half-done task between runners with a packet (#404)
- Give each runner a circuit breaker with classified fallback (#429)
- Escalate a stuck step up a runner ladder (#450)
- Ship conservative default caps and say so at first run (#481)
- Bound every run by budget, deadline and no-progress limit (#492)
- Pause on rate limits and sleep through them (#493)
- Fall back along a runner chain with a reason on record (#494)

## R11. Cost: price, record and cap what fm code spends

**Grounding (partial):** fm code counts tokens per call and in total (fmcode.py:288-293) but never prices them. It ignores claude's total_cost_usd (fmmodels.py:375-383), and its spend never reaches the global budget ledger. fm bench already records total_cost_usd through fmbudget.record (fmbench.py:449), and fm ideas caps children with --max-budget-usd from fmbudget (fmideas.py:59). fm cost and fm digest read only Claude transcripts. Nothing uses provider caching (no cache_control in fmmodels).

**Score:** value 3 · effort S · risk low · **build**

**Brief:** Done when each fm code call's cost (claude's total_cost_usd, or tokens times an optional price in models.json) goes to fmbudget's ledger under the project, the close line shows the run's dollars, and the claude runner gets --max-budget-usd from fmbudget.effective. Test: a fake claude reporting a cost lands in the ledger and in the closed event. Skip up-front estimates (wait for R2's per-runner tax) and cache-layout work.

Ideas (9):
- Show per-project cost and time spent, weekly (#9)
- Cap and price every runner call up front (#15)
- Show the cost of a request before it runs (#132)
- Price and time the first call before it runs, with a one-key cheaper path (#146)
- Wild: Add a "ghost of Foreman past" that predicts the run's length (#160)
- Show the cost of a session before it starts (#190)
- Lay prompts out for provider caching (#290)
- Keep prompt prefixes byte-stable so provider caching works (#299)
- Cap spend globally across projects and runners (#403)

## R12. Routing and runner evaluation

**Grounding (partial):** fm code bench grades one model or CLI on seeded tasks into code-bench.jsonl (fmcodebench.py:1-6, :140), but nothing reads that file to choose a runner. --escalate is the only switch between runners. fmoutcomes keeps a track record per type and tier, not per runner (fmoutcomes.py). fm run --models picks Claude models per tier.

**Score:** value 3 · effort M · risk med · **build**

**Brief:** After T-1328: done when fm code runners shows each runner's record per request kind from its own journals (closed, blocked, fix rounds, tokens, minutes), and runner = auto picks the cheapest runner that is green on that kind (3+ runs), saying why in the start event. Test: seeded journals make auto pick the runner the record favours. Skip races, apprentices and backtests (L, spend-heavy).

Ideas (24):
- Pick the runner per task automatically, and show why (#5)
- Choose the runner by evidence, per request kind (#20)
- Audition every runner on my own repo (#27)
- Route steps across runners by role, cost and failure (#45)
- Wild: Race two runners on one task and keep the cheaper green one (#51)
- Wild: Learn the default runner per kind of request (#52)
- Race two runners on the plan and keep the better one (#64)
- Route tasks to the cheapest runner that has passed that kind (#96)
- Add a "which runner for which task" router with learned defaults from bench grades (#127)
- Wild: Publish a per-runner report card from the user's own history (#139)
- Give each runner a career card (#158)
- Let a new runner earn trust on probation (#186)
- Wild: Pick a runner by intent: `--careful`, `--cheap`, `--free` (#207)
- Add a runner "audition" that races all detected CLIs on a user's real repo and writes a routing table (#211)
- Wild: Hold a "rehearsal" run before trusting a new runner (#243)
- Price every runner by real outcome: cost per proved task, per kind (#253)
- Wild: Backtest a runner on the repo's own history (#292)
- Add a `fm code` portable runner "audition" that writes the routing table from the user's own repos (#335)
- Train a free apprentice by shadowing (wild) (#381)
- Race two runners on the plan only, keep the cheaper green plan (#421)
- Log whether the user kept the result (#453)
- Build a runner ledger that grades every runner per task kind (#501)
- Route each step to a runner by ledger and budget (#502)
- Replay a recorded run on a different runner (#508)

## R13. Config: one resolved, explained, validated set of settings

**Grounding (partial):** Settings are spread across $FOREMAN_HOME/models.json (fmmodels.py:29-31; a bad field is an error naming the file), $FOREMAN_HOME/tui.toml (fmcodetui.py:1483-1600; a bad setting is skipped with a line), per-project meta set through fm (sensitive), and flags. T-1328 adds a runner = line. Nothing shows the resolved whole or where each value came from.

**Score:** value 4 · effort M · risk low · **build**

**Brief:** Done when fm code config prints every effective fm code setting (runner, model, timeouts, lean, limits, theme) with its source (flag, env, project, global, default), --explain KEY says what it does, and a bad file names the line and falls back to defaults with one warning. Test: a project setting overrides the global one and the output says so. Skip the keychain, time machine, pasteable setup codes, plain-words config, profiles, sunset tests, schema migration and the TUI editor: too much machinery for a dozen settings.

Ideas (38):
- Wild: Type a sentence, get the runner (#12)
- Make config one file with a doctor that explains itself (#25)
- Talk to settings in plain words (#34)
- Layer config with an explainer and a first-run wizard (#44)
- Show where every config value came from (#58)
- Write config atomically, validate it, and self-repair (#76)
- Put every setting in one layered config with `fm code config` get/set/explain (#117)
- Store per-project overrides in `.foreman/code.toml`, committed or ignored by choice (#120)
- Validate config at load with line-accurate errors and a safe fallback to last-good (#122)
- Wild: Support a shareable setup as one pasteable code (runners, theme, defaults, no secrets) (#126)
- Write config atomically with a last-good copy and a doctor line (#194)
- Layer config as global, project and env with `fm code config explain` and last-good fallback (#221)
- Write layered project config that travels with the repo (#238)
- Wild: Accept a pasteable setup code (#242)
- Wild: Ask for config in plain words (#244)
- Store API keys in the OS keychain (#285)
- Use one config line, and derive everything else (#325)
- Wild: Pasteable setup code that carries runners, theme and defaults, never secrets (#343)
- Make `fm code` own the setup contract as one resolved-config object (#358)
- Make config schema-versioned with migration and a typed editor in the TUI (#363)
- Keep secrets out of config by reference (#365)
- Wild: Offer a config time machine (#367)
- Document config from the registry, and fail CI on drift (#371)
- Add `fm where`, one command listing every path Foreman reads or writes (#439)
- Give each setting a sunset test (wild) (#446)
- Pin trust to the hash of a project's `.foreman/code.toml` (#474)
- Respect read-only and XDG-managed config (#478)
- Switch whole named profiles in one key (#480)
- Generate every `FM_CODE_*` env override from the config schema (#483)
- Wild: Emit a "why it behaved this way" config receipt on every run (#486)
- Fence the config with schema, last-good and a repair command (#495)
- Resolve one config object, then print it as a receipt (#511)
- Show the resolved plan before the first token (#512)
- Keep project config in the repo, and trust it deliberately (#515)
- Write config as typed schema with migration and last-good fallback (#517)
- Edit config inside the TUI with live preview (#518)
- Wild: Say "make it faster and cheaper" and get a config diff (#519)
- Wild: Retire settings that never matter (#520)

## R14. Install, first run and doctor (fm on PATH, the first request works)

**Grounding (partial):** fm install-user links ~/.local/bin/fm and only warns when that folder isn't on PATH (fmsetup.py:47, :151-155). A plugin-only install never makes the link (fm_link appears only in fmsetup), and that's what the user hit. fm doctor has no PATH check and no fm code checks (fmdoctor.py check list). A first run with no model fails with a hint (fmcode.py:72, :1124-1129).

**Score:** value 5 · effort S · risk low · **build**

**Brief:** Done when the plugin's SessionStart (or the first fm run of any verb) makes the ~/.local/bin/fm link when it's absent and not someone else's, fm doctor FAILs with the fix when a login shell can't find fm, and fm code doctor runs R5's runner check plus PATH, installs and config in one screen. Test: with a temp HOME, the hook makes the link, and doctor flags a PATH without it. Skip the zipapp, self-deleting plugin copy and shell-history setup.

Ideas (25):
- Ratchet "first five minutes" in CI (#26)
- Show a roll call on first launch (#28)
- Make bare `fm` open the app and `fm setup` fix PATH (#57)
- Add `fm code setup` as a one-screen first-run wizard that is also the doctor (#116)
- Add `fm code install-check` that audits shell integration (PATH, completions, tmux, terminal capability) (#123)
- Ship `fm code doctor` that fixes the first-five-minutes path (#131)
- Install check that fixes the shell itself (wild) (#148)
- Ship `fm.pyz`, a single-file zipapp, so fm works with no plugin or PATH setup (#204)
- Run a first-launch wizard that is also the doctor (#235)
- Make the first request after install succeed or explain in under 60 seconds (#247)
- Offer "explain this repo to me" as the zero-risk first run (#252)
- Record each friction-free first run as a regression fixture (#269)
- Ship install channels that fix `fm` not being on PATH (#291)
- Ship `fm code` as a Claude-style bare launcher with a shell integration installer (#337)
- Add a first-run self-install that fixes PATH and shell (#359)
- Wild: Keep a project-local `fm code` shim that travels with the repo (#369)
- Pin the rule that `fm` must be on PATH as a doctor failure (#391)
- Honour proxy, custom CA and offline mirrors in the model client (#407)
- Run `fm code doctor` as the first-run wizard and the install fixer (#420)
- Keep an install ledger and add `fm code uninstall`/`reset` (#477)
- Wild: Let `fm code setup` write itself from the user's shell history (#485)
- Wild: Hold a "fresh machine" CI job that runs setup from nothing (#487)
- Wild: Have a self-heal pass at launch that fixes what it can (#500)
- Build a runner pit-crew that auto-heals setup (#507)
- Make config self-diagnosing with `fm code doctor` (#513)

## R15. Entry point and CLI grammar

**Grounding (partial):** Bare fm code errors 'needs a request' (fmcode.py:1029-1031); T-1330 step 2 makes it open the app. fm code tui --plain prints one line per event (fmcli.py ~5711). Some errors name the next command (the resume hints at fmcode.py:484, :1068), but most CodeError paths don't.

**Score:** value 3 · effort S · risk low · **build**

**Brief:** Done when every fm code failure (CodeError, ModelError, Blocked, usage) ends with one 'Next: <command>' line, and a request piped on stdin is read as the request or its context. Test: each failure path in test_code asserts a Next: line. Skip making bare fm code a thin exec into claude (189/414): it conflicts with T-1330's app.

Ideas (14):
- Make bare `fm code` do the one obvious thing (#81)
- Print a plain status line when not a tty (#87)
- For Claude users, make bare `fm code` a thin launcher (#189)
- End every fm code failure with one "Next:" command (#199)
- Pipe stdin in as the request context (#200)
- Give `fm code` one grammar: `fm code [REQUEST]`, everything else a flag (#201)
- Cap `fm code --help` at one screen and ratchet it (#202)
- Wild: Print the whole app state as a single sentence when you run `fm code` without a tty (#208)
- Make bare `fm code` print one answer before anything else (#320)
- Print `Next:` on every failure and delete the rest of the explainers (#326)
- Wild: Make `fm code` a plain prompt that never leaves the shell (#328)
- Make bare `fm code` a thin exec into the user's best CLI, wrapped by Foreman (#414)
- Make an unknown command do the nearest sensible thing and say so (#442)
- Use seven outcomes everywhere (#444)

## R16. Multi-project home and project resolution

**Grounding (planned T-1330):** fm projects lists every project with active task, queue and inbox, and --next ranks every project's next action (fmwatch.py:727-800). The global -p SLUG runs fm in another project, exact slug only (fmcli.py:51-56). A git folder silently becomes a project (fmcore.py:711-721). T-1330 adds the home screen over projects and fm code --task.

**Score:** value 4 · effort S · risk low · **planned T-1330 + build extension**

**Brief:** Extension beyond T-1330: done when -p takes a unique slug prefix or folder name ('in nixie' typed on the home resolves the same way), an ambiguous one lists the matches, and fm code's first line names the project and root it runs in, so a wrong-directory run is visible. Test: two projects, fm code -p nix --dry-plan resolves nixie, and 'ni' lists both. Skip monorepo package scoping until asked.

Ideas (29):
- Make `fm code` answer "what should I work on?" (#4)
- Fleet view: one project's stuck, another's done (#21)
- Wild: Ask any project from anywhere (#24)
- Type a request and see where it goes before Enter (#30)
- Jump to a project by name (#31)
- Make the home screen greet you with the state of play (#38)
- Wild: Resolve the project from the request (#50)
- Discover projects on its own (#62)
- Show the project list from what's already on disk, no registry (#86)
- Wild: Open the home screen on "what needs you", ranked across projects (#102)
- Answer "what should I do next?" from the home screen (#128)
- Wild: Say the project in the request, let Foreman find it (#137)
- Offer "what should I work on?" as the bare-`fm code` landing answer (#143)
- Make wrong-directory runs impossible to miss (#144)
- Suggest the next request from the repo (#151)
- Wild: Resolve the project and runner from a sentence typed on the home screen (#217)
- Resolve a request that spans projects into linked tasks (#250)
- Warn when the cwd isn't the project you meant (#259)
- Put a "did you mean this project?" resolver on the home screen (#264)
- Carry lessons between projects through stack cards (#302)
- Let the project be the current directory, nothing else (#324)
- Cross-project "what needs me" ranking that reads only existing task state (#339)
- Paste a folder path to adopt a project (#350)
- Trust the cwd before the first call (#384)
- Rank "what needs you" across projects by age and blocking (#388)
- Scope runs to a monorepo package with its own gates and runner (#413)
- Treat the project as cwd plus a warn-on-mismatch, no registry (#417)
- Wild: Make `fm code` ask which project from a sentence (#422)
- Scope gates by sub-package in monorepos and worktrees (#482)

## R17. Unattended and cross-project work management

**Grounding (partial):** fm run already works one project's queue unattended in claude -p sessions, with lanes, a usage-limit wait, failover, --max-usd, stall detection, notify, run.lock and systemd-inhibit (fmserve.py:722+, :30, :302, :523, :707). fm orders, night, away, notify, standing asks and autonomy exist. fm code takes no lock (no flock in fmcode.py), so two runs on one project collide. It never calls notify, and fm run can't use fm code's harness or another runner, or work across projects.

**Score:** value 4 · effort M · risk med · **build**

**Brief:** Done when fm code holds a per-project run lock (a second run says which run holds it), calls the fm notify command on close or block, and fm run --runner NAME [--all-projects] works the queue through fm code --task ID (T-1330 step 1), one task at a time per project, round-robin. Test: a second fm code in the same project is refused; fm run --runner fake closes queued tasks in two projects.

Ideas (33):
- Run the whole queue unattended with one stop-line (#10)
- Sweep one request across many projects (#36)
- Schedule the cross-project queue with caps and fairness (#46)
- Schedule runs across projects with runner quotas and fallback (#59)
- Lock tasks across projects and app instances (#75)
- Hand the user a "while you were away" digest across all projects (#134)
- Hand the user a morning digest across all projects when unattended runs end (wild) (#150)
- Say goodnight to start an unattended shift (#155)
- Make prompts optional, with every decision logged for review (#203)
- Wild: Treat a `TODO.fm` file in any project as the queue (#206)
- Wild: Make `fm code` refuse to start a second copy of itself, then adopt the first (#209)
- Add a cross-project scheduler with runner quotas, fairness and fallback on classified failure (#216)
- Show a weekly "what Foreman did for you" report across projects (#249)
- Keep a "standing permission" record so release and push never ask again (#263)
- Wild: Let Foreman say "I'm stuck" in your own notifications, with the fix attached (#266)
- Wild: Run the queue only when the machine is idle and plugged in (#294)
- Promote deferred tasks when matching evidence appears (#298)
- Hold a per-project lock so two app instances cannot run the same task (#344)
- Stop re-asking answered questions (#372)
- Run standing orders on events (#380)
- Keep the user's standing permissions as a ledger Foreman reads (#387)
- Write the release notes the user reads from their own requests (#390)
- Leave a morning digest of what the unattended runs did (wild) (#394)
- Wild: Ask "are you still there?" back from the harness (#398)
- Lease the project so two app instances can't run the same task (#431)
- Turn on an autonomy dial: `fm trust 0-3` (#436)
- Release when the queue drains (wild) (#437)
- Expire "Later from" tasks after N releases without evidence (#438)
- Decide with a timeout when the user is away (#455)
- Open a shadow week before acting (#459)
- Turn type-ahead into pending tickets (#467)
- Pick up a ticket and reorder the queue (#469)
- Pool runners as a fleet with per-runner concurrency lanes (#510)

## R18. Self-improvement triggers: Foreman starts the round itself

**Grounding (planned T-1332):** T-1332 turns friction in the user's words into a queued RESEARCH brainstorm-and-round task (urgent on repeat). Already there: the friction digest and its due() trigger (fmfriction.py:118, :300), fm friction --every, fm loop (fmloop.py), fm scout (fmscout.py), vetoes compiled into guard rules (T-1063, fmcli.py:5727), and trials (fmtrials.py). fm code's own failures (blocked, stalled, quit mid-run, no runner) feed none of these. fm night doesn't run fm code bench.

**Score:** value 4 · effort S · risk low · **planned T-1332 + build extension**

**Brief:** Extension: done when a blocked, stalled or killed fm code run, or a failed preflight, writes a code_friction ledger event under the 'fm code' area, and T-1332's per-area counter counts it the same as the user's words. Two in 7 days queue the round with no message from the user. Test: two blocked fake runs queue one RESEARCH task for fm code. Follow-up: a nightly fm code bench canary on every installed runner (M).

Ideas (31):
- Auto-brainstorm from friction, with a visible receipt (#7)
- Self-trigger the friction-to-round loop (#16)
- Wild: Complaint-to-check compiler (#23)
- File a task automatically from a stalled or failed run (#49)
- Run a nightly canary of the request kinds on every runner (#60)
- Self-notice friction and open a diagnostic (#77)
- Wild: Let Foreman file its own friction tickets from your words (#90)
- Wild: Let Foreman dogfood itself nightly across all runners (#101)
- Wild: Let Foreman notice setup friction itself and repair it unprompted (#124)
- Turn a stalled run into a task automatically (#130)
- Turn friction phrases into a standing, self-filed diagnostic round (#142)
- Mine the user's own complaints into a regression suite (#191)
- Make friction detection a built-in hook that opens a brainstorm task with a receipt (#214)
- Wild: Nightly self-dogfood canary that runs every request kind on every runner and files regressions (#219)
- Run setup friction through the self-notice loop (#241)
- Make user complaints into standing regression checks automatically (#251)
- Wild: Say "stop being annoying" and have Foreman trim its own prompts and notes (#257)
- Turn the user's complaint into the next task automatically (friction receipt) (#262)
- Compile every complaint into a standing regression check ("friction → check") (#334)
- Wild: Let Foreman write its own next brainstorm brief at the end of every release (#340)
- Wild: Let a pasted error or complaint configure the setup (#366)
- Convert "it just isn't doing anything" into a stall record automatically (#386)
- Let a complaint become a check, and show which check it became (wild) (#392)
- Turn the user's hand edits after a run into lessons (#409)
- Auto-file a friction task from the user's own phrases via a prompt hook (#419)
- Wild: Run a canary that auditions every runner nightly on a scratch repo (#433)
- Cluster the idea catalog before every round (#435)
- Promote a repeated correction into a standing rule (#449)
- Tune its own config overnight and show the evidence (#456)
- Offer config changes as diffs, never apply them (#479)
- Notice friction and open the config fix by itself (#522)

## R19. Worker isolation and safety

**Grounding (partial):** Strong already. After every worker turn the judge restores Git's config and hooks, undoes commits, and reverts files the guard refuses (fmcode.py:544-615). Workers get a credential-dropping environment (fmcode.py:75-103), and sensitive repos never go off-machine (fmcode.py:274-286). Lanes give worktrees (fmlanes.py), and fm code inside a lane already resolves to the project (fmcore.py:720). fm run has a sandbox (fmserve.py:390-448), and fm oops restores snapshots (fmcli.py:3781).

**Score:** value 3 · effort M · risk med · **skip**

**Skip reason:** Skip: the guard and judge already hold, and R17's lock stops two runs from colliding in one tree. Revisit --lane and the sandbox for fm code workers when parallel runs in one repo are wanted.

Ideas (12):
- Run each lane in its own git worktree (#47)
- Run worker turns in a throwaway worktree (#73)
- Snapshot each step to a shadow ref for instant rollback (#80)
- Undo a whole run in one command (#178)
- Cage the worker in bubblewrap or sandbox-exec (#184)
- Enforce a declared file scope per plan (#288)
- Pass workers an environment allowlist (#301)
- Plant honeytokens to catch a hijacked worker (wild) (#305)
- Enforce an org policy file for allowed runners, endpoints and paths (#408)
- Print a "won't do this session" line at start (wild) (#445)
- Wild: Run the harness in a rehearsal sandbox first (#496)
- Let a runner prove it can't see outside its project (#506)

## R20. Proof and verification quality

**Grounding (done (mostly)):** A FIX or FEATURE verify must fail before any work (fmcode.py:1179-1186). Each verify is recorded as evidence, and the close is harness-run (fmcode.py:633-648, :1259-1282). The flaky-test ledger in fm check (fmcore.py:2425), fm second (fmsecond.py) and fm task prove exist.

**Score:** value 2 · effort M · risk low · **skip**

**Skip reason:** Skip: proof is already the harness's strength, and none of these is the user's pain (setup, stuck runs, any runner, many projects).

Ideas (17):
- Let a second CLI cross-examine the diff (#37)
- Wild: Review my own hand edits as I make them (#175)
- Wild: Run a "second opinion" from a different runner only when the first one's proof is thin (#255)
- Classify a red check as flaky or real (#287)
- Close only on a checkable failure reason (#308)
- Re-verify each close from a clean checkout of the commit (#309)
- Quarantine flaky checks instead of trusting one pass (#314)
- Wild: A cheat corpus the harness must beat every release (#318)
- Show it working with a demo artifact (#377)
- Play a skeptical user against the result (wild) (#383)
- Select only the tests the change touches during verify (#406)
- Wild: Pre-mortem the plan with a second runner and turn its failure modes into checks (#411)
- Classify a task's verify command by why it is red at creation (#440)
- Run `fm gate`, one command for the three gates (#443)
- Hold out blind acceptance checks (#448)
- Warm a clean-tree baseline at launch (#451)
- Mutation-prove every diff (#452)

## R21. Intake and planning

**Grounding (partial):** fm code plans with a checked slot, answers questions without making a task (fmcode.py:1132-1150), plans without a model from --verify (fmcode.py:1152), and has --dry-plan. Foreman already turns a red CI run into a FIX brief (fmci.py:68), reads issues into the inbox (fm inbox gh), and has fm task split (fmsplit.py) and fm recall.

**Score:** value 3 · effort M · risk med · **skip**

**Skip reason:** Skip for now: once T-1330's fm code --task lands, every intake path Foreman already has (inbox gh, ci, split) feeds fm code. Revisit clarifying questions and splitting a request into several tasks when a bench seed shows an L request failing.

Ideas (25):
- Quote-back the request into a checkable definition of done (#8)
- Show "You said / we did" on the home screen (#33)
- Wild: Rehearse a request against a dry-run runner first (#138)
- Answer "did my words land?" with a request echo before any work starts (#140)
- Paste a screenshot into the request (#154)
- Mention files and images in the request (#166)
- Turn an issue into a run (#170)
- Record recipes for repeatable requests (#172)
- Wild: Do it like that commit (#176)
- Wild: Dictate a request (#177)
- Plan routine requests without a model (#180)
- Keep the user's own phrase-to-action vocabulary: learn "do the usual" (#248)
- Ask one question when a request is ambiguous (#283)
- Split a big request into a dependency graph of tasks (#295)
- Turn a red CI run into a queued task (#300)
- Plan speculatively while the request is being typed (wild) (#304)
- Wild: Treat the user's complaint as the spec by echoing it (#329)
- Wild: Rehearse a request against a "ghost" runner that returns canned plan shapes before spending anything (#342)
- Say no early with a fit check (#376)
- Answer "why is it like this?" from history (#378)
- Offer three plans with prices (#379)
- Bisect a bug from a sentence (wild) (#382)
- Compile a pasted stack trace or bug report into a failing test first (#405)
- Wild: Bisect a regression with the harness (#412)
- Scale the ceremony to the request (#441)

## R22. Continuity: follow-ups and handoff between runners or sessions

**Grounding (partial):** Task packets and fm run's failover hand a task to another agent (fmserve.py:302-317). fm session runs and resumes sessions for 4 agents (fmsession.py:77-84), and fm claude lists Claude sessions (fmclaude.py). fm code can only --resume an unfinished run: a closed run can't be followed up, and a stuck one can't be handed to an interactive CLI.

**Score:** value 3 · effort S · risk low · **build**

**Brief:** Done when fm code --after T-ID "<follow-up>" (or n right after a close in the app) plans a new task whose request carries the closed task's title, criteria and changed files, and a stuck run prints (or, in the app, runs) the command that opens the user's CLI on the task packet. Test: a follow-up's plan prompt holds the earlier task's title and files. Skip adopting live Claude sessions over a pty or transcript (L, fragile).

Ideas (14):
- Wild: Adopt an existing Claude Code session into fm code (#11)
- Supervise a human-driven interactive CLI through a pty (#65)
- Keep one conversation across runs, per project (#133)
- Wild: Adopt an already-running Claude Code session as a lane (#136)
- Offer a follow-up after every close (#152)
- Close each run with a one-line "what I'd do next" (#163)
- Wild: Hand off a live Claude Code session by saying "take this to fm code" (#164)
- Continue a closed run with a follow-up (#165)
- Wild: Adopt a live interactive Claude Code session into fm code through a pty (#218)
- Wild: Adopt a running interactive Claude Code session as a lane through its transcript file (#341)
- Hand a stuck run to a live CLI in one key (#373)
- Review finished runs as a deck, and reopen with a reason (#375)
- Offer a one-key "take it from here" when Claude Code itself stalls (wild) (#393)
- Transplant a session between CLIs (#457)

## R23. Integrations and surfaces beyond the terminal

**Grounding (partial):** fm mcp serves Foreman's state as read-only MCP tools (fmmcp.py). fm agents wires Foreman into codex, gemini and opencode (fmagents.py:1-18). fm serve runs Remote Control so the phone app works (fmserve.py:1-6), and fm pr handles threads and a merge train (fmpr.py). There's no fm code MCP or ACP tool, no PR creation, and no webhooks.

**Score:** value 2 · effort M · risk med · **skip**

**Skip reason:** Skip: the user asked for the terminal app, any runner and many projects. fm serve covers the phone. Revisit an fm code MCP tool after T-1330.

Ideas (17):
- Wild: Foreman as a menu-bar/tmux "shift supervisor" (#22)
- Serve fm code as an editor agent over ACP and MCP (#48)
- Expose the harness as an MCP server (#61)
- Wild: Offer `fm code` as a shell prompt segment instead of an app (#91)
- Wild: Offer fm code as an MCP tool that other agents call (#100)
- Dock beside Claude Code as a live companion, not a separate app (wild) (#149)
- Open a PR from a proved run (#169)
- Wild: Fix the command I just ran (#174)
- Wrap hand-launched CLIs with PATH shims (#185)
- Run a worker on another machine over ssh (#188)
- Ship an MCP/ACP server so Claude Code, Zed and Cursor can call fm code as a tool (#215)
- Finish the job for the user: land a proved run as a merged PR or local merge in one key (#246)
- Wild: Let the user text a request from their phone and get the receipt back (#254)
- Fire user hooks and webhooks on run events (#289)
- Wild: Expose the runner router as a local OpenAI-compatible endpoint (#410)
- Serve the harness as an OpenAI-compatible model (#447)
- Read the editor's cursor as request context (#458)

## R24. Model quality: local and small models, context, structured output

**Grounding (partial):** Local servers are found (fmmodels.py:67, :149) but assumed to have an 8192-token context (LOCAL_CONTEXT, fmmodels.py:69), which sets fm code's output caps (fmcode.py:1047). The plan prompt sends only the file list (fmcode.py:1093), even though fm map exists (fmmap.py). JSON slots are repaired up to twice (fmcode.py:196-218), with no constrained decoding.

**Score:** value 3 · effort S · risk low · **build**

**Brief:** Done when a local profile's context comes from the server itself (Ollama /api/show, llama.cpp /props n_ctx, vLLM /v1/models max_model_len), falling back to 8192, and fm code's caps follow it. Test: fake servers on loopback report 32768 and the profile carries it. Skip LAN discovery, honeypot slots, exemplars and grammar decoding for now.

Ideas (9):
- Pack a repo map for small local models (#171)
- Constrain the model's slot output at the decoder (#282)
- Advise which local model fits this machine (#286)
- Wild: Discover model servers across the LAN (#293)
- Wild: Honeypot slots that catch a model ignoring the schema (#317)
- Wild: Generate a setup that matches the machine's idle resources (#368)
- Probe the local model's real context window (#400)
- Serve the project's dependency docs from the installed versions (#402)
- Recall proved runs as few-shot exemplars for small models (#454)

## R25. Harness tests and observability: misbehaving fakes, replay, drift

**Grounding (partial):** The tests have a fake claude (test_code_worker.py:68) and resume-kill tests (test_code.py:295, :314). fm code bench seeds exist, and the events journal replays in the TUI (--events/--snapshot). There's no shared set of misbehaving runners (hang, silence, a terminal prompt, garbage JSON, rate-limit text, fork-and-exit) and no CLI version or output-shape drift check.

**Score:** value 4 · effort S · risk low · **build**

**Brief:** Done when one test helper provides a set of fake runners that hang, go silent, prompt on a TTY, print garbage JSON, print usage-limit text, or fork and exit, and R5, R7, R8 and R10's tests use them. Test: the helper's own self-check runs each fake and asserts its behaviour. Skip log-mutation fuzzing and recorded chaos suites.

Ideas (9):
- Cover every CLI adapter with a scripted misbehaving fake (#79)
- Pin and watch the CLI versions of every adapter (#173)
- Run every runner adapter against a misbehaving fake (#193)
- Wild: Mutate real logs to fuzz the whole app (#195)
- Run every command in the docs in CI (#303)
- Replay a run offline from recorded model slots (cassettes) (#312)
- Detect runner output schema drift at runtime (#313)
- Wild: Fuzz the config loader with generated configs and corrupted files (#484)
- Wild: Record real runner failures into a replayable chaos suite (#497)

## Slate

These are the build clusters, ordered by value squared over effort (S=1, M=2), so the user's biggest pains rank above cheap nice-to-haves. Dependencies are noted. The planned tasks come first as prerequisites: T-1327 (R1), T-1328 (R4), T-1329 (R6), T-1330 (R16 base), T-1332 (R18 base).

1. R14 Install, first run and doctor (fm on PATH, the first request works), effort S, value 5, score 25
2. R25 Harness tests and observability: misbehaving fakes, replay, drift, effort S, value 4, score 16
3. R8 Process lifecycle: no orphans, clean stops, effort S, value 4, score 16 (tests use R25)
4. R18 Self-improvement triggers: Foreman starts the round itself, effort S, value 4, score 16 (extension of T-1332)
5. R16 Multi-project home and project resolution, effort S, value 4, score 16 (extension beyond T-1330)
6. R2 Lean workers: cut and show the startup tax, effort M, value 5, score 12.5 (with T-1327)
7. R5 Preflight: probe each runner and the project before the first request, effort M, value 5, score 12.5 (after T-1328; tests use R25)
8. R7 Stall detection and diagnosis (fm code why), effort M, value 5, score 12.5 (after T-1329; tests use R25)
9. R9 Durable runs: journal, resume, recovery, effort S, value 3, score 9
10. R3 One live Foreman when it's installed twice (plugin, dev checkout), effort S, value 3, score 9
11. R15 Entry point and CLI grammar, effort S, value 3, score 9
12. R11 Cost: price, record and cap what fm code spends, effort S, value 3, score 9
13. R24 Model quality: local and small models, context, structured output, effort S, value 3, score 9
14. R22 Continuity: follow-ups and handoff between runners or sessions, effort S, value 3, score 9
15. R17 Unattended and cross-project work management, effort M, value 4, score 8 (after T-1330 step 1)
16. R10 Limits, rate limits and failover across runners, effort M, value 4, score 8 (uses R25 and the journal)
17. R13 Config: one resolved, explained, validated set of settings, effort M, value 4, score 8
18. R12 Routing and runner evaluation, effort M, value 3, score 4.5 (after T-1328)

## Left to the UI half (71)

- Name every run like a journal entry (#35)
- Delete the panels and settings nobody uses, measured locally (#88)
- Wild: Make the whole TUI one sentence that grows (#89)
- Replace the many themes with one palette plus an accent flag (#92)
- Design the home screen as a project deck, not a list (#103)
- Show a "no progress" diagnosis in place of a silent spinner (#104)
- Add a runner picker that looks like a fleet bay (#105)
- Make first launch a guided, zero-text setup strip (#106)
- Draw duplicate-Foreman detection as a visible "who's in charge" badge (#107)
- Animate orphan cleanup on quit (#108)
- Ghost-lane for multi-project runs (#109)
- Put a token-weight meter on every worker launch (#110)
- Wild: Let the home screen be a harbor map (#111)
- Wild: Auto-open a "what's wrong" overlay when friction is detected (#112)
- Wild: Command line that doubles as a request box (#113)
- Wild: Dock-pane trailing mode for use beside Claude Code (#114)
- Persist the last view so reopening feels like resuming (#115)
- Reveal the result with one key (#153)
- Rotate "you haven't tried this" tips from local usage (#156)
- Wild: Turn the home screen into a living desk of project cards (#161)
- Wild: Let the user name a runner a nickname and a voice (#162)
- Lint a six-noun vocabulary in all UI strings (#205)
- Project deck home screen with live cards (#222)
- Silent-run face: a "waiting on the CLI" scene (#223)
- Runner bay picker with capability lamps (#224)
- Orphan-reap choreography on quit (#225)
- Lineage ribbon for who runs whom (#226)
- First-launch roll call as the setup wizard (#227)
- Cross-project attention strip (#228)
- Config explainer view with provenance chips (#229)
- Wild: Harbor map of projects (#230)
- Wild: "Startup tax" bar that fills as the worker boots (#231)
- Wild: Type-ahead router preview (#232)
- Run-state tab title and prompt segment (#233)
- Skeleton-to-content load for the project deck (#234)
- Greet by project, not by banner (#270)
- Say "done" in one sentence a person would say (#272)
- Offer the next request as a ghost placeholder (#273)
- Let a failed guard refusal teach once, then go quiet (#274)
- Wild: Let the home screen keep a tiny desk plant per project (#277)
- Wild: Hum a different bell per outcome (#278)
- Wild: Print a postcard to the shell when you quit (#279)
- Rename the thing to what the user typed (#280)
- Make the wait for a worker feel like a workshop, not a spinner (#281)
- Add a slash-command prompt box (#284)
- Collapse the ~300 listed TUI ideas into a frozen "v1 screen" budget (#321)
- Morph a project card into its run screen (#345)
- Slide drawers over the run, not full-screen views (#346)
- Show a typed-ahead request as resolved chips (#347)
- Draw the queue as a dependency graph with flowing edges (#348)
- Add a transcript minimap scrollbar (#349)
- Fold the breadcrumb into a morphing header path (#351)
- Use the full width on big monitors (#352)
- Show inline screenshots when the task is about UI (wild) (#353)
- Send a runner to the pit lane when rate-limited (wild) (#354)
- Show a shared "now" spotlight across all projects (wild) (#355)
- Give errors one three-row face: happened, did, next (#356)
- Pick the whole look from a preview strip of live frames (wild) (#357)
- Celebrate a first-ever success in a project, once (#399)
- Zoom is the only navigation (#460)
- Let one thing move at a time (#461)
- Show a which-key popup after a pause (#462)
- Ship a TUI inspector for extension authors (#463)
- Show the CLI command behind every key (#464)
- Hold to confirm kill and stop (#465)
- Draw a project heat calendar on the home screen (#466)
- Add a presenter mode with double-height headings (#468)
- Wild: Pin run requests to a ticket rail (#470)
- Wild: Light the room from run state (#471)
- Wild: Cross-fade between projects as scenes with their own accent (#472)
- Probe the render path at launch and record the result (#473)


---

# fm code brainstorm: UI/UX catalogue (half 1 of 2)

Area: the app's experience and look, conversation, liveness on screen, onboarding, themes, the site, product bets. 236 of 522 ideas placed in 25 clusters; the rest (runner/model/setup/config/reliability/proof/multi-project) are listed at the end for the other half.

Grounding: done / partial / planned / new / premise false, cited to file:line. Value 1–5 to the user, effort S/M/L, risk low/med/high.

| id | capability | ideas | grounding | value | effort | risk | mark |
|---|---|---|---|---|---|---|---|
| U1 | Launch like `claude`: one command, one grammar | 11 | partial (bare `fm code` errors, fmcode.py:1030) + planned T-1330 | 5 | M | med | build |
| U2 | Home: the state of play across projects | 14 | planned T-1330 (list); ranking/greeting new | 5 | M | low | build |
| U3 | Home look: a living project deck | 10 | new (primitives exist: box, stations, Motion) | 4 | M | med | build |
| U4 | Request box: type, paste, mention, preview | 10 | partial (one-line append-only prompt, fmcodetui.py:1212) | 5 | M | low | build |
| U5 | Never looks stuck: liveness on screen | 25 | partial (shimmer, clock, spinner) + planned T-1329, T-1310 | 5 | M | low | build |
| U6 | Run view: layout, navigation and motion discipline | 6 | partial (layout config, overlays) + planned T-1308/1307/1313 | 3 | M | low | build |
| U7 | Keys and discoverability | 4 | partial (hints, `?` view) + planned T-1313 | 4 | S | low | build |
| U8 | Results and close-out: what changed, what's next | 11 | partial (close wave, answer, step diff) + planned T-1305, T-1312 | 5 | M | low | build |
| U9 | Errors, help and plain language | 8 | partial (one-line errors, no Next:) | 4 | S | low | build |
| U10 | Onboarding and the first run | 6 | partial (welcome screen) + planned T-1309 | 5 | M | low | build |
| U11 | Plain, piped and one-line modes | 4 | partial (--plain) + planned T-1308 | 3 | S | low | build |
| U12 | Themes, look and render fidelity | 3 | done (4 presets, contrast check) + planned T-1311; 92 premise false | 2 | S | low | skip |
| U13 | Personality and delight | 6 | new | 3 | S | low | build |
| U14 | Trust cues: who's in charge, what's running, a clean exit | 8 | partial (quit stops the group; nothing shown) | 4 | S | low | build |
| U15 | Queue as tickets: type ahead while it runs | 4 | partial (n refuses during a run) + planned T-1330 | 4 | M | low | build |
| U16 | Runner picker as a bay of lamps | 2 | partial (flat picker); needs T-1328 | 4 | S | low | build |
| U17 | Beyond the TUI: other surfaces | 13 | partial (read-only fmmcp, tmux line; no fm code surface) | 3 | S | med | build |
| U18 | Claude Code interop: hand off and adopt sessions | 9 | new for fm code | 4 | M | med | build |
| U19 | Workflow bets: from a proved run to shipped | 17 | partial outside fm code (fm pr, bisect, why, orders, oops) | 4 | M | med | build |
| U20 | Unattended runs, autonomy and digests | 16 | partial outside fm code (fm run is claude -p, digest, notify) | 4 | M | med | build |
| U21 | Learns from friction and from you | 25 | partial (fm friction, taste compile, evals add) | 4 | M | med | build |
| U22 | Conversation and intake: talk, not just submit | 13 | partial (questions answered; no follow-up or clarifying) | 5 | L | med | build |
| U23 | Site, README and demos | 2 | done/partial (examples gallery, README) + planned T-1309 | 3 | S | low | build |
| U24 | UI scope budget and extension tooling | 3 | partial (extension API) + planned T-1315 | 2 | S | low | skip |
| U25 | Continuity: reopen where you left off | 6 | partial (history, replay, --resume) + planned T-1305 | 4 | S | low | build |

## U1 — Launch like `claude`: one command, one grammar  (11 ideas · value 5 · M · risk med · **build**)

**Grounding:** partial + planned T-1330. Bare `fm code` errors "needs a request" (plugin/lib/fmcode.py:1029-1031); the app hides behind `fm code tui`, rewritten to a hidden --tui flag (plugin/lib/fmcli.py:5707, 5857); bare `fm` prints status + Next (ran it). T-1330's criterion makes bare `fm code` on a tty open the home. No stdin read in fmcode.py (grep sys.stdin: none); no help budget; no nearest-command fallback. 189/414 (thin exec into `claude`) conflict with T-1330 and give up the harness's judging.

**Brief:** `fm code` on a tty opens the app (T-1330); `fm code "req"` on a tty runs it inside the app, piped/non-tty prints plain lines; `fm code tui` stays an alias; `echo ctx | fm code "req"` adds stdin as context. Not the thin-exec variant (189, 414). Test: pty test that bare `fm code` draws the home; `fm code "x" | cat` prints plain lines with no escape codes; with piped stdin the --json start event's request carries the stdin text.

Ideas:
- #57 Make bare `fm` open the app and `fm setup` fix PATH
- #81 Make bare `fm code` do the one obvious thing
- #189 For Claude users, make bare `fm code` a thin launcher
- #200 Pipe stdin in as the request context
- #201 Give `fm code` one grammar: `fm code [REQUEST]`, everything else a flag
- #202 Cap `fm code --help` at one screen and ratchet it
- #320 Make bare `fm code` print one answer before anything else
- #337 Ship `fm code` as a Claude-style bare launcher with a shell integration installer
- #414 Make bare `fm code` a thin exec into the user's best CLI, wrapped by Foreman
- #442 Make an unknown command do the nearest sensible thing and say so
- #443 Run `fm gate`, one command for the three gates

## U2 — Home: the state of play across projects  (14 ideas · value 5 · M · risk low · **build**)

**Grounding:** planned T-1330 (home lists every project's queue/inbox/active/blocked, Enter runs). Inputs exist: fm next, fm queue (plugin/lib/fmcli.py:5308), fm projects, fm digest (fmcli.py:4964). Missing beyond T-1330: a "needs you" ranking across projects, a greeting line of what changed, jump-by-name, an attention strip inside a run view, a suggested next request.

**Brief:** On top of T-1330: the home orders projects by need (asks/blocked > failed runs > running > queue age), opens with one line of what changed since the last open, typing a name jumps to a project, and a run view shows a one-line strip when another project needs you. Test: 3 fixture projects (blocked, running, idle) → golden frame orders them blocked/running/idle; a run closed since the last-open stamp appears in the greeting; typing `nix` + Enter focuses nixie.

Ideas:
- #4 Make `fm code` answer "what should I work on?"
- #21 Fleet view: one project's stuck, another's done
- #31 Jump to a project by name
- #38 Make the home screen greet you with the state of play
- #102 Wild: Open the home screen on "what needs you", ranked across projects
- #128 Answer "what should I do next?" from the home screen
- #134 Hand the user a "while you were away" digest across all projects
- #143 Offer "what should I work on?" as the bare-`fm code` landing answer
- #151 Suggest the next request from the repo
- #228 Cross-project attention strip
- #270 Greet by project, not by banner
- #339 Cross-project "what needs me" ranking that reads only existing task state
- #355 Show a shared "now" spotlight across all projects (wild)
- #388 Rank "what needs you" across projects by age and blocking

## U3 — Home look: a living project deck  (10 ideas · value 4 · M · risk med · **build**)

**Grounding:** new. T-1330 specifies a list; no card renderer. Reusable parts: box() (plugin/lib/fmcodetui.py:348), stations() for a mini track (241), Motion/FX easing (430-498), the overlay fade (983-990).

**Brief:** Projects as cards (mini station track, queue depth, blocked/inbox badges, runner glyph), a focus ring that glides between them, Enter morphs the card into its run view; motion=reduced/off draws the end state at once. Wild variants (harbor map, cross-fade scenes, ghost lanes for concurrent runs, heat calendar) left out. Test: golden frames of the deck with 3 fixture projects, and of the morph at t=0, 0.15, 0.3 s; motion=off gives the final frame at t=0.

Ideas:
- #103 Design the home screen as a project deck, not a list
- #109 Ghost-lane for multi-project runs
- #111 Wild: Let the home screen be a harbor map
- #161 Wild: Turn the home screen into a living desk of project cards
- #222 Project deck home screen with live cards
- #230 Wild: Harbor map of projects
- #234 Skeleton-to-content load for the project deck
- #345 Morph a project card into its run screen
- #466 Draw a project heat calendar on the home screen
- #472 Wild: Cross-fade between projects as scenes with their own accent

## U4 — Request box: type, paste, mention, preview  (10 ideas · value 5 · M · risk low · **build**)

**Grounding:** partial. Prompt mode is one line, append/backspace only (plugin/lib/fmcodetui.py:1212-1222, drawn at 967); no cursor keys, history, multi-line, bracketed paste (no `2004h` in plugin/lib/fmcodeterm.py), slash commands, @file mentions or route preview. Commands are a registry (fmcodetui.py:1155-1161) a palette can list.

**Brief:** A real line editor (←/→, ↑ history, Ctrl-A/E/W/U, bracketed paste keeps newlines); `/` opens a palette of the app's commands (extension ones included); `@` completes tracked files; a one-line preview under the box says where the request goes (question / FIX / FEATURE, project, runner). Dictation (177) and image paste (154) left out (no portable stdlib path). Test: App key feed — a pasted bracketed block arrives as one multi-line request; `/dif`+Enter opens the diff view; `@pa`+Tab completes to a `git ls-files` path; the preview for "what does x do?" reads question.

Ideas:
- #30 Type a request and see where it goes before Enter
- #113 Wild: Command line that doubles as a request box
- #154 Paste a screenshot into the request
- #166 Mention files and images in the request
- #177 Wild: Dictate a request
- #217 Wild: Resolve the project and runner from a sentence typed on the home screen
- #232 Wild: Type-ahead router preview
- #273 Offer the next request as a ghost placeholder
- #284 Add a slash-command prompt box
- #347 Show a typed-ahead request as resolved chips

## U5 — Never looks stuck: liveness on screen  (25 ideas · value 5 · M · risk low · **build**)

**Grounding:** partial + planned T-1329 (CLI stream → Activity lines, 'still working Ns') and T-1310 (title, bell, 'why waiting' after 10 s). Exists: empty-panel shimmer (plugin/lib/fmcodetui.py:516-523), mid-panel 'planning the work' spinner (784-787), elapsed clock (856-860, 872), spinner in the status chip (888), tokens-per-call chart (644). Missing beyond those: last-heard counter with bytes, launch weight of the first call, ETA from past runs, rate-limit state, `fm code why` for a run seen from another shell, a stuck card with actions.

**Brief:** Beyond T-1329/T-1310: during a live run the status bar always shows 'last heard Ns ago'; after 10 s of silence an inline card names the wait (planner/worker/check, pid, bytes, last call's input tokens) with w wait / k kill / m switch runner; `fm code why` prints the same for the newest run from its events file. Test: fake runner silent N s with an injected clock → golden frame shows the card and keys; `fm code why` on a recorded events file names the stage and silence; pty smoke asserts a first Activity line within 10 s of start.

Ideas:
- #39 Print a heads-up when the run is waiting on the CLI, not on you
- #83 Add one `fm code why` command that answers "is it doing anything?"
- #104 Show a "no progress" diagnosis in place of a silent spinner
- #110 Put a token-weight meter on every worker launch
- #112 Wild: Auto-open a "what's wrong" overlay when friction is detected
- #129 Make a run's first 30 seconds visibly alive
- #141 Make every silent minute self-explaining with a live "what it's waiting on" line
- #145 Ship `fm code why`: one command that explains the last run or the current silence
- #157 Show what the first call is loading, live
- #160 Wild: Add a "ghost of Foreman past" that predicts the run's length
- #220 Add a one-line `fm code why` plus a shareable diagnostic bundle
- #223 Silent-run face: a "waiting on the CLI" scene
- #231 Wild: "Startup tax" bar that fills as the worker boots
- #233 Run-state tab title and prompt segment
- #258 Trust the first minute: show "alive" evidence before any model answers
- #271 Show the first-call wait as a named countdown
- #281 Make the wait for a worker feel like a workshop, not a spinner
- #296 Tail the CLI's own session transcript for progress
- #327 Show a single "last heard from the runner N s ago" line
- #331 Wild: Make "nothing happening" impossible by running the worker visibly in a split
- #332 Make `fm code` a launch-time contract: a 10-second "first sign of life" SLA
- #354 Send a runner to the pit lane when rate-limited (wild)
- #385 Make the first-sign-of-life deadline a failing test
- #397 Make the wait feel like a workshop with a "what it's doing" line from the process itself
- #416 Show a 10-second sign-of-life contract with a named wait

## U6 — Run view: layout, navigation and motion discipline  (6 ideas · value 3 · M · risk low · **build**)

**Grounding:** partial + planned T-1308 (breakpoints), T-1307 (view fades), T-1313 (focus ring, search). Layout is config (plugin/lib/fmcodetui.py:81-83, render 920-960); views are centred overlays over a shaded screen (983-990); Plan and Check-output panels exist but aren't in the default layout (805-821). No wide layout, drawers, breadcrumb or minimap.

**Brief:** At ≥160 columns a third column shows the existing Plan and Check-output panels; diff/history/picker open as a right-hand drawer that slides in (0.2 s) over the run instead of a centred box; the header shows a path (home › project › task › view). Zoom-only navigation (460) and the minimap (349) left out. Test: golden frame at 200x50 contains the Plan panel; a mid-slide frame shows the drawer partly in; the header text in the diff view reads the path.

Ideas:
- #346 Slide drawers over the run, not full-screen views
- #349 Add a transcript minimap scrollbar
- #351 Fold the breadcrumb into a morphing header path
- #352 Use the full width on big monitors
- #460 Zoom is the only navigation
- #461 Let one thing move at a time

## U7 — Keys and discoverability  (4 ideas · value 4 · S · risk low · **build**)

**Grounding:** partial + planned T-1313 (per-panel hint line). Status-bar hints (plugin/lib/fmcodetui.py:88, 895-900), `?` overlay built from the key config (993-1002), configurable keys (84-86). `q` during a run stops it at once (quit→stop, 1228-1230, 1263-1269): one stray key kills a run. No which-key popup, no CLI equivalents, no tips.

**Brief:** `q`/`s` during a live run ask to press again within 2 s before stopping; the `?` view shows the CLI command behind each key (d → git show, r → fm code --resume ID); a footer tip names one never-used command per launch from a local counter. Test: App.key('q') with a fake live child leaves it running and shows the confirm, a second q stops it; the help frame contains 'fm code --resume'; a tip disappears after its command is used.

Ideas:
- #156 Rotate "you haven't tried this" tips from local usage
- #462 Show a which-key popup after a pause
- #464 Show the CLI command behind every key
- #465 Hold to confirm kill and stop

## U8 — Results and close-out: what changed, what's next  (11 ideas · value 5 · M · risk low · **build**)

**Grounding:** partial + planned T-1305 (receipt card, final frame to scrollback), T-1312 (diff reveal). Exists: close wave (plugin/lib/fmcodetui.py:574-582), CLOSED chip, answers read whole (760-762), diff grouped by step (1310-1334), history rows with DONE/STOP (1032-1037). Missing: a one-sentence result in the user's words, run names, suggested follow-ups, finished-run review deck.

**Brief:** Beyond T-1305: the closed event carries one line 'You asked X → did Y · checks 3/3 · commit abc' and up to two suggested next requests; the close card shows them, history rows show that line instead of the task id. Inline screenshots (353) and release notes (390) left out. Test: fake run closes → frame contains the 'You asked' line and the suggestions; the history view row for it shows the same sentence.

Ideas:
- #33 Show "You said / we did" on the home screen
- #35 Name every run like a journal entry
- #152 Offer a follow-up after every close
- #153 Reveal the result with one key
- #163 Close each run with a one-line "what I'd do next"
- #272 Say "done" in one sentence a person would say
- #279 Wild: Print a postcard to the shell when you quit
- #353 Show inline screenshots when the task is about UI (wild)
- #375 Review finished runs as a deck, and reopen with a reason
- #377 Show it working with a demo artifact
- #390 Write the release notes the user reads from their own requests

## U9 — Errors, help and plain language  (8 ideas · value 4 · S · risk low · **build**)

**Grounding:** partial. fm code failures print one 'fm code: …' line, a resume hint only on model errors (plugin/lib/fmcode.py:1067-1074); the TUI shows STOP + a log note (State._on_error, plugin/lib/fmcodetui.py:225). No 'Next:' on fm code failures, no error card, no bug-report export, no `fm where`, no vocabulary lint. fm explain exists (fmcli.py:5289).

**Brief:** Every fm code failure (UsageError, CodeError, ModelError) ends with one 'Next: fm …' line, and the TUI draws errors as a three-row card (what happened / what Foreman did / next) with the next command one key away. Test: for each raise site, stderr's last line starts 'Next: fm ' and parses with fmcli's parser; an error event's frame shows the three rows.

Ideas:
- #199 End every fm code failure with one "Next:" command
- #205 Lint a six-noun vocabulary in all UI strings
- #265 Export a one-paste bug report for Foreman's own failures
- #274 Let a failed guard refusal teach once, then go quiet
- #326 Print `Next:` on every failure and delete the rest of the explainers
- #356 Give errors one three-row face: happened, did, next
- #439 Add `fm where`, one command listing every path Foreman reads or writes
- #444 Use seven outcomes everywhere

## U10 — Onboarding and the first run  (6 ideas · value 5 · M · risk low · **build**)

**Grounding:** partial + planned T-1309 (--tour, animated SVG). The idle screen is a welcome with keys (plugin/lib/fmcodetui.py:791-802); questions already answer with no task (plugin/lib/fmcode.py:1056-1057, 1137), so 'explain this repo' works but isn't offered. With no model the first request fails until m (pack). No first-launch checks on screen; runner detection itself is T-1328 (other area).

**Brief:** First launch (no runs yet) shows three chips — fm on PATH, a runner found and chosen, this folder is a Foreman project — each with a one-key fix, then offers 'explain this repo' as the first request (Enter runs it as a question). Test: clean HOME with a fake claude on PATH → frame shows the three chips' states; Enter on the offer spawns a run that ends answered with no task and no file change.

Ideas:
- #28 Show a roll call on first launch
- #106 Make first launch a guided, zero-text setup strip
- #227 First-launch roll call as the setup wizard
- #247 Make the first request after install succeed or explain in under 60 seconds
- #252 Offer "explain this repo to me" as the zero-risk first run
- #350 Paste a folder path to adopt a project

## U11 — Plain, piped and one-line modes  (4 ideas · value 3 · S · risk low · **build**)

**Grounding:** partial + planned T-1308 (one-line status below 50 cols or piped). --plain prints Activity line by line (plugin/lib/fmcodetui.py:1685-1694) but needs a request (1820-1823).

**Brief:** Beyond T-1308: bare `fm code` with stdout not a tty prints one state sentence (e.g. 'foreman: T-1330 step 2/5, 4m · 2 projects need you') and exits 0. The grow-from-one-sentence default (89) and a readline loop (328) left out. Test: subprocess with piped stdout prints exactly one line matching the pattern and no escape codes.

Ideas:
- #87 Print a plain status line when not a tty
- #89 Wild: Make the whole TUI one sentence that grows
- #208 Wild: Print the whole app state as a single sentence when you run `fm code` without a tty
- #328 Wild: Make `fm code` a plain prompt that never leaves the shell

## U12 — Themes, look and render fidelity  (3 ideas · value 2 · S · risk low · **skip**)

**Grounding:** done + planned T-1311 (gallery, hot reload). Four presets from one palette function (plugin/lib/fmcodetui.py:30-75), faint colours named and skipped (1525-1544), colour depth from the environment (plugin/lib/fmcodeterm.py:25-32). 92's premise is false: the themes already derive from one palette, and dropping to one accent loses the colour-blind 'signal' theme.

**Skip:** Skip: T-1311 covers the preview strip (357); 92's premise is false; a render probe (473) is low value next to T-1301's wide-character fix.

Ideas:
- #92 Replace the many themes with one palette plus an accent flag
- #357 Pick the whole look from a preview strip of live frames (wild)
- #473 Probe the render path at launch and record the result

## U13 — Personality and delight  (6 ideas · value 3 · S · risk low · **build**)

**Grounding:** new. No per-runner identity, no once-only moments; a bell is planned only for blocked/refusal (T-1310).

**Brief:** The first closed run in a project plays a once-only celebration (a brighter close wave and 'first proved change in <project>'), stored in project state so it never repeats; picking a runner shows a one-line hello (name, kind, last result). Career cards and nicknames (158, 162) wait for the runner ledger (other area); desk plant and outcome hums (277, 278) left out. Test: two closes in a fresh project → only the first frame has the celebration line.

Ideas:
- #158 Give each runner a career card
- #162 Wild: Let the user name a runner a nickname and a voice
- #276 Give every runner a one-line "hello" on selection
- #277 Wild: Let the home screen keep a tiny desk plant per project
- #278 Wild: Hum a different bell per outcome
- #399 Celebrate a first-ever success in a project, once

## U14 — Trust cues: who's in charge, what's running, a clean exit  (8 ideas · value 4 · S · risk low · **build**)

**Grounding:** partial. The header names worker/model (plugin/lib/fmcodetui.py:873); quit stops the run's process group (1228-1230, 1263-1269) and the screen stops it on any exit (1734-1737); T-1326 kills child CLIs. Nothing shows what was stopped; the lineage badge needs T-1327's marker (other area).

**Brief:** Quitting during a run shows 'stopping claude (pid N)… stopped' per child before the screen closes, and the line left in the shell names what was stopped; once T-1327 sets its marker the header reads 'worker: claude (bare)'. Test: fake child that sleeps; quit → last frame lists its pid as stopped and os.kill(pid, 0) raises.

Ideas:
- #32 Show a lineage badge for who is running whom
- #107 Draw duplicate-Foreman detection as a visible "who's in charge" badge
- #108 Animate orphan cleanup on quit
- #225 Orphan-reap choreography on quit
- #226 Lineage ribbon for who runs whom
- #268 Make duplicate-Foreman detection a visible fact, not just a silent fix
- #395 Name the duplicate-Foreman fact on screen (wild)
- #445 Print a "won't do this session" line at start (wild)

## U15 — Queue as tickets: type ahead while it runs  (4 ideas · value 4 · M · risk low · **build**)

**Grounding:** partial + planned T-1330 (a project's queue in the app). `n` during a run refuses: 'a run is going: s stops it' (plugin/lib/fmcodetui.py:1232-1236). fm queue/capture exist (fmcli.py:5308, 4668).

**Brief:** `n` during a run captures the request as a pending ticket on a rail under the track; when the run ends the next ticket starts; in T-1330's queue view space picks a ticket and ↑/↓ moves it. The dependency-graph view (348) left out. Test: key n + text + Enter during a fake live run → ticket listed and captured; after the exit event the next ticket's run is spawned.

Ideas:
- #348 Draw the queue as a dependency graph with flowing edges
- #467 Turn type-ahead into pending tickets
- #469 Pick up a ticket and reorder the queue
- #470 Wild: Pin run requests to a ticket rail

## U16 — Runner picker as a bay of lamps  (2 ideas · value 4 · S · risk low · **build**)

**Grounding:** partial; depends on T-1328 (runner registry, other area). `m` is a flat MODEL/WORKER list (plugin/lib/fmcodetui.py:1039-1046) from model profiles and workers on PATH (1336-1340); a dead server only sets a message (1287-1292).

**Brief:** After T-1328: each row has a status lamp (ready / key missing / unreachable / last bench score), the default is marked, and `p` pings the selected runner with a pulse until it answers. Test: fake PATH with 2 CLIs + a dead endpoint → 3 rows with distinct statuses; p on the dead row ends 'unreachable'.

Ideas:
- #105 Add a runner picker that looks like a fleet bay
- #224 Runner bay picker with capability lamps

## U17 — Beyond the TUI: other surfaces  (13 ideas · value 3 · S · risk med · **build**)

**Grounding:** partial. fmmcp serves Foreman state read-only over MCP (plugin/lib/fmcli.py:5124), no fm code tool; tmux status via `fm state --line` (README.md:215; fmcli.py:4662); the foreman-ui pane and Foreman Desktop exist (README.md:160, 235) but nothing in mods/ reads fm code runs; fm notify serves fm run only (fmcli.py:5804).

**Brief:** Narrow: run-event hooks — `on = closed|blocked|needs-you` commands in config get the event JSON on stdin, run through the guard; `fm state --line` includes the newest fm code run so tmux and prompt segments show it. MCP/ACP/OpenAI-compatible serving, phone, editor and room lights left out (L bets; the MCP fm-code tool is the one worth capturing). Test: a configured hook receives the closed event's JSON; a guard-refused hook command is reported and not run; `fm state --line` names a running fixture run.

Ideas:
- #22 Wild: Foreman as a menu-bar/tmux "shift supervisor"
- #48 Serve fm code as an editor agent over ACP and MCP
- #61 Expose the harness as an MCP server
- #91 Wild: Offer `fm code` as a shell prompt segment instead of an app
- #100 Wild: Offer fm code as an MCP tool that other agents call
- #114 Wild: Dock-pane trailing mode for use beside Claude Code
- #149 Dock beside Claude Code as a live companion, not a separate app (wild)
- #215 Ship an MCP/ACP server so Claude Code, Zed and Cursor can call fm code as a tool
- #254 Wild: Let the user text a request from their phone and get the receipt back
- #289 Fire user hooks and webhooks on run events
- #447 Serve the harness as an OpenAI-compatible model
- #458 Read the editor's cursor as request context
- #471 Wild: Light the room from run state

## U18 — Claude Code interop: hand off and adopt sessions  (9 ideas · value 4 · M · risk med · **build**)

**Grounding:** new for fm code. fm code only spawns non-interactive children (stdin DEVNULL, plugin/lib/fmcodetui.py:1351-1359; worker templates plugin/lib/fmcode.py:60); fm conductor lists live sessions with leases (fmcli.py:5002) as a base for adoption.

**Brief:** Narrow: `x` on a stuck or blocked run suspends the screen and opens the chosen CLI interactively in the project with the task brief as its opening prompt; on exit the screen returns and re-runs the task's checks. Adopting a live session through a pty or transcript (11, 136, 218, 341) and session transplant (457) left out (L, high). Test: a fake CLI records its argv/prompt and exits 0 → the App restores the screen and spawns the verify.

Ideas:
- #11 Wild: Adopt an existing Claude Code session into fm code
- #65 Supervise a human-driven interactive CLI through a pty
- #136 Wild: Adopt an already-running Claude Code session as a lane
- #164 Wild: Hand off a live Claude Code session by saying "take this to fm code"
- #218 Wild: Adopt a live interactive Claude Code session into fm code through a pty
- #341 Wild: Adopt a running interactive Claude Code session as a lane through its transcript file
- #373 Hand a stuck run to a live CLI in one key
- #393 Offer a one-key "take it from here" when Claude Code itself stalls (wild)
- #457 Transplant a session between CLIs

## U19 — Workflow bets: from a proved run to shipped  (17 ideas · value 4 · M · risk med · **build**)

**Grounding:** partial outside fm code: fm pr (plugin/lib/fmcli.py:5091), fm bisect (5023), fm why (5185), fm orders (5136), fm repeats (5393), fm oops for uncommitted work (5189). fm code commits each closed task but nothing in the app ships or undoes it.

**Brief:** Narrow: after a close, `u` undoes the run (git revert of its commit, recorded as a run in history) and `p` drafts the PR text via fm pr, pushing only with the publish grant. Issue/CI→run, recipes, fix-last-command, live review of hand edits, do-it-like-that, bisect from a sentence left out. Test: a closed fake run in a temp repo → u leaves a revert commit and the tree equals the pre-run tree; p prints the fm pr text and opens no socket without the grant.

Ideas:
- #169 Open a PR from a proved run
- #170 Turn an issue into a run
- #172 Record recipes for repeatable requests
- #174 Wild: Fix the command I just ran
- #175 Wild: Review my own hand edits as I make them
- #176 Wild: Do it like that commit
- #178 Undo a whole run in one command
- #206 Wild: Treat a `TODO.fm` file in any project as the queue
- #246 Finish the job for the user: land a proved run as a merged PR or local merge in one key
- #248 Keep the user's own phrase-to-action vocabulary: learn "do the usual"
- #300 Turn a red CI run into a queued task
- #378 Answer "why is it like this?" from history
- #380 Run standing orders on events
- #382 Bisect a bug from a sentence (wild)
- #383 Play a skeptical user against the result (wild)
- #405 Compile a pasted stack trace or bug report into a failing test first
- #412 Wild: Bisect a regression with the harness

## U20 — Unattended runs, autonomy and digests  (16 ideas · value 4 · M · risk med · **build**)

**Grounding:** partial outside fm code: fm run works the queue in claude -p sessions, not fm code runs (plugin/lib/fmcli.py:5778); fm notify (5804), fm digest (4964), fm autonomy (5424), fm standing (4691). T-1330 adds running a queued task with fm code --task.

**Brief:** In the app, `g` works the project's queue with fm code --task one task after another until empty, a task blocks twice, or a stop line is hit; on return the home shows a 'while you were away' digest (closed/blocked, commits, time, tokens) built from code/*.events.jsonl. Test: a fixture queue of 2 tasks with a fake runner → both close in order; the digest frame lists both with their commits.

Ideas:
- #9 Show per-project cost and time spent, weekly
- #10 Run the whole queue unattended with one stop-line
- #150 Hand the user a morning digest across all projects when unattended runs end (wild)
- #155 Say goodnight to start an unattended shift
- #203 Make prompts optional, with every decision logged for review
- #249 Show a weekly "what Foreman did for you" report across projects
- #263 Keep a "standing permission" record so release and push never ask again
- #266 Wild: Let Foreman say "I'm stuck" in your own notifications, with the fix attached
- #372 Stop re-asking answered questions
- #387 Keep the user's standing permissions as a ledger Foreman reads
- #394 Leave a morning digest of what the unattended runs did (wild)
- #398 Wild: Ask "are you still there?" back from the harness
- #436 Turn on an autonomy dial: `fm trust 0-3`
- #437 Release when the queue drains (wild)
- #455 Decide with a timeout when the user is away
- #459 Open a shadow week before acting

## U21 — Learns from friction and from you  (25 ideas · value 4 · M · risk med · **build**)

**Grounding:** partial: fm friction digests and --every N passes (plugin/lib/fmcli.py:5383-5391), fm taste compile turns repeated steers into warn rules (T-1063, CHANGELOG.md:217), standing steers flagged as rule candidates (fmcli.py:1816-1820), fm evals add turns a blocked task into an eval case (plugin/lib/fmcost.py:757). No detection of complaint phrases; a stalled or failed fm code run files nothing.

**Brief:** A stalled or blocked fm code run files one inbox item (source discovered) with its events path, stage and silence length, deduped per cause; the home shows it under 'Foreman noticed'. Complaint-phrase hooks and Foreman-meta ideas (340, 435, 438, 298) left out. Test: a fake run stalling past the threshold → exactly one capture holding the events path; a second identical stall adds to it, not a new item.

Ideas:
- #7 Auto-brainstorm from friction, with a visible receipt
- #16 Self-trigger the friction-to-round loop
- #23 Wild: Complaint-to-check compiler
- #49 File a task automatically from a stalled or failed run
- #77 Self-notice friction and open a diagnostic
- #90 Wild: Let Foreman file its own friction tickets from your words
- #130 Turn a stalled run into a task automatically
- #142 Turn friction phrases into a standing, self-filed diagnostic round
- #191 Mine the user's own complaints into a regression suite
- #214 Make friction detection a built-in hook that opens a brainstorm task with a receipt
- #251 Make user complaints into standing regression checks automatically
- #257 Wild: Say "stop being annoying" and have Foreman trim its own prompts and notes
- #262 Turn the user's complaint into the next task automatically (friction receipt)
- #298 Promote deferred tasks when matching evidence appears
- #302 Carry lessons between projects through stack cards
- #334 Compile every complaint into a standing regression check ("friction → check")
- #340 Wild: Let Foreman write its own next brainstorm brief at the end of every release
- #386 Convert "it just isn't doing anything" into a stall record automatically
- #392 Let a complaint become a check, and show which check it became (wild)
- #409 Turn the user's hand edits after a run into lessons
- #419 Auto-file a friction task from the user's own phrases via a prompt hook
- #435 Cluster the idea catalog before every round
- #438 Expire "Later from" tasks after N releases without evidence
- #449 Promote a repeated correction into a standing rule
- #453 Log whether the user kept the result

## U22 — Conversation and intake: talk, not just submit  (13 ideas · value 5 · L · risk med · **build**)

**Grounding:** partial: questions get an answer with no task (plugin/lib/fmcode.py:1056-1057, 1137; drawn at plugin/lib/fmcodetui.py:760-762); plan title and criteria are on screen (825, 599-609); --resume continues an interrupted run (fmcode.py:1027) but a closed run can't be followed up, nothing asks a clarifying question, a run can't be asked about mid-flight. fm clauses and fm oracle exist (fmcli.py:5300, 5646).

**Brief:** Enter after a close or answer opens the box as 'follow-up to T-…', and the child gets the prior request, plan, answer and diff summary as context (new --after T-… flag); a question typed during a run is answered from the files by an answer-only child without stopping the run. Three priced plans, fit check, rubber duck, scaled ceremony (379, 376, 13, 441) left out. Test: fake model, answer then follow-up → the second run's prompt contains the first answer; a mid-run question spawns an answer-only child (no task, clean tree) while the first child keeps running.

Ideas:
- #8 Quote-back the request into a checkable definition of done
- #13 Wild: A "rubber duck" runner that only asks questions
- #133 Keep one conversation across runs, per project
- #140 Answer "did my words land?" with a request echo before any work starts
- #159 Ask for a mid-run status in plain words
- #165 Continue a closed run with a follow-up
- #280 Rename the thing to what the user typed
- #283 Ask one question when a request is ambiguous
- #329 Wild: Treat the user's complaint as the spec by echoing it
- #374 Put a time and money box in the request
- #376 Say no early with a fit check
- #379 Offer three plans with prices
- #441 Scale the ceremony to the request

## U23 — Site, README and demos  (2 ideas · value 3 · S · risk low · **build**)

**Grounding:** done/partial + planned T-1309 (animated SVG). The fm code page shows each real example with its last screen (site/build.py:236-305, 356-362; test plugin/tests/test_docs.py:263); README's Foreman Code section (README.md:293-311) with demo/code-tui.mp4; fmdocs drift checks paths and npm/make commands only (plugin/tests/test_docsdrift.py:1).

**Brief:** A test runs every `fm code …` example in README's Foreman Code section through fmcli's parser (and the safe ones with --dry-plan on a fake model) and fails on a usage error; once T-1330 lands the site page gains the home screen's snapshot. Presenter mode (468) left out: T-1309 and the recordings cover demos. Test: the new test itself, red on a renamed flag.

Ideas:
- #303 Run every command in the docs in CI
- #468 Add a presenter mode with double-height headings

## U24 — UI scope budget and extension tooling  (3 ideas · value 2 · S · risk low · **skip**)

**Grounding:** partial + planned T-1315 (widget firewall). Extension API (plugin/lib/fmcodetui.py:1429-1450); a failing panel draws its error in place (903-908). No usage counts, screen budget or inspector.

**Skip:** Skip: usage-measured deletion (88) needs telemetry for one user; a frozen v1 budget (321) fights the 'make it amazing' ask (T-1306's golden frames already catch clutter); an inspector (463) serves extension authors who don't exist yet.

Ideas:
- #88 Delete the panels and settings nobody uses, measured locally
- #321 Collapse the ~300 listed TUI ideas into a frozen "v1 screen" budget
- #463 Ship a TUI inspector for extension authors

## U25 — Continuity: reopen where you left off  (6 ideas · value 4 · S · risk low · **build**)

**Grounding:** partial + planned T-1305 (final frame to scrollback). Past runs list and replay (plugin/lib/fmcodetui.py:1284-1308, 1397), --resume of a run (plugin/lib/fmcode.py:1027), Foreman's resume point (fm resume, fmcli.py:5305). The app keeps no last project/view.

**Brief:** On quit the app saves {project, view, task}; the next launch opens there with 'welcome back: T-… closed 2h ago' (or 'stopped mid-step 3: r resumes'). Test: App quit writes the file; a new App given it restores the mode and project and the first frame shows the welcome-back line.

Ideas:
- #115 Persist the last view so reopening feels like resuming
- #147 Let Foreman keep a "last session" so reopening resumes the thing you were doing
- #256 Wild: Take over a project the user abandoned: "what was I doing here?"
- #275 Remember a run's last words when the terminal closes
- #336 Make a project's "resume point" a first-class object across app launches
- #396 Greet with a one-line "welcome back" that names where you left off

## Slate (build clusters, value for effort)

| # | id | capability | value | effort | risk | depends on |
|---|---|---|---|---|---|---|
| 1 | U7 | Keys and discoverability | 4 | S | low | — |
| 2 | U9 | Errors, help and plain language | 4 | S | low | — |
| 3 | U14 | Trust cues: who's in charge, what's running, a clean exit | 4 | S | low | T-1326 (done), T-1327 for the badge |
| 4 | U16 | Runner picker as a bay of lamps | 4 | S | low | T-1328 |
| 5 | U25 | Continuity: reopen where you left off | 4 | S | low | — |
| 6 | U11 | Plain, piped and one-line modes | 3 | S | low | T-1308 |
| 7 | U13 | Personality and delight | 3 | S | low | — |
| 8 | U23 | Site, README and demos | 3 | S | low | T-1330 for the snapshot |
| 9 | U17 | Beyond the TUI: other surfaces | 3 | S | med | — |
| 10 | U2 | Home: the state of play across projects | 5 | M | low | T-1330 |
| 11 | U4 | Request box: type, paste, mention, preview | 5 | M | low | — |
| 12 | U5 | Never looks stuck: liveness on screen | 5 | M | low | T-1329, T-1310 |
| 13 | U8 | Results and close-out: what changed, what's next | 5 | M | low | T-1305 |
| 14 | U10 | Onboarding and the first run | 5 | M | low | T-1328 for detection |
| 15 | U1 | Launch like `claude`: one command, one grammar | 5 | M | med | T-1330 |
| 16 | U15 | Queue as tickets: type ahead while it runs | 4 | M | low | T-1330 |
| 17 | U3 | Home look: a living project deck | 4 | M | med | T-1330 |
| 18 | U18 | Claude Code interop: hand off and adopt sessions | 4 | M | med | — |
| 19 | U19 | Workflow bets: from a proved run to shipped | 4 | M | med | — |
| 20 | U20 | Unattended runs, autonomy and digests | 4 | M | med | T-1330 (--task) |
| 21 | U21 | Learns from friction and from you | 4 | M | med | U5 (stall signal) |
| 22 | U22 | Conversation and intake: talk, not just submit | 5 | L | med | U4 |
| 23 | U6 | Run view: layout, navigation and motion discipline | 3 | M | low | T-1308 |

## Left to the other half (286 ideas, by number in ideas.md order)

Runner/model/routing/cost, setup/install/doctor, config, reliability/stall diagnosis/orphans/journal/locks, proof and checks, multi-project resolution/scheduling. Borderline ones handed over: #1/#14/#40 (stall diagnosis), #24 (ask any project), #132/#146 (cost preview), #229/#518 (config views), #260 (Ctrl-C summary), #295 (split a request into a task graph), #432 (terminal repair), #512 (resolved-plan line at start).

1, 2, 3, 5, 6, 12, 14, 15, 17, 18, 19, 20, 24, 25, 26, 27, 29, 34, 36, 37, 40, 41, 42, 43, 44, 45, 46, 47, 50, 51, 52, 53, 54, 55, 56, 58, 59, 60, 62, 63, 64, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 78, 79, 80, 82, 84, 85, 86, 93, 94, 95, 96, 97, 98, 99, 101, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 131, 132, 135, 137, 138, 139, 144, 146, 148, 167, 168, 171, 173, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 190, 192, 193, 194, 195, 196, 197, 198, 204, 207, 209, 210, 211, 212, 213, 216, 219, 221, 229, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 250, 253, 255, 259, 260, 261, 264, 267, 269, 282, 285, 286, 287, 288, 290, 291, 292, 293, 294, 295, 297, 299, 301, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 322, 323, 324, 325, 330, 333, 335, 338, 342, 343, 344, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 381, 384, 389, 391, 400, 401, 402, 403, 404, 406, 407, 408, 410, 411, 413, 415, 417, 418, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 440, 446, 448, 450, 451, 452, 454, 456, 474, 475, 476, 477, 478, 479, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522
