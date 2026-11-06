---
id: T-0323
type: FEATURE
tier: L
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-06T01:12:05Z
updated: 2026-10-06T01:32:34Z
base: c3cfd12f8ecbfb019b8347fad76bac26126d3265
base_tree: 14680f683be6db6828ca1b4b7b25d772ad2429a7
verified: strong
---
# fm session: agent-agnostic session supervisor (claude, codex, gemini, opencode)
## Raw request
> fm session: agent-agnostic session supervisor (claude, codex, gemini, opencode)
## Interpretation
Start, list, watch, message and stop coding-agent sessions on a device, for any supported agent, from the CLI or the desktop app (locally or over ssh). Sessions run detached so they outlive the caller; their output is normalised into one event schema.
## Assumptions (confidence)
## Acceptance criteria
- [x] a session starts detached, streams normalised events and resumes on send, with a stub claude — verify with `python3 plugin/tests/run.py -k test_session`
- [x] codex, gemini and opencode lines normalise into the same schema — verify with `python3 plugin/tests/run.py -k test_session`
- [x] stop kills the whole process group and list reconciles dead pids — verify with `python3 plugin/tests/run.py -k test_session`
## Non-goals
## Approach (options → choice → why)
Options: (A) talk to each agent's server/SDK (opencode serve, codex app-server, Claude Agent SDK) — rich but four protocols and long-lived servers; (B) one detached runner per session that runs each turn through the agent's headless streaming mode (claude -p stream-json, codex exec --json, gemini -p stream-json, opencode run --format json), resumes by the agent's own session id, and normalises lines into events.jsonl. Choice: B — one code path, stdlib only, survives the app, every agent has it; servers can come later per agent if a mode needs them.
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests (red) with stub agents
2. [x] fmsession: store, runner, normalisers
3. [x] CLI: start/list/tail/send/stop/agents
4. [x] docs
## Resume here
## Docs impact
MASTER CLI line + module table; CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_session` → ✗ exit 1 · Ran 6 tests in 0.7s (7 classes, 16 at a time; slowest: Confirm 1s, Session 0s, Export 0s) / FAILED (1 classes) [ran] [tree 0f9c6d9855eb] (2026-10-06T01:20:52Z)
- (step 1) `python3 plugin/tests/run.py -k test_session -k Normalise` → exit 0 · Ran 14 tests in 1.9s (8 classes, 16 at a time; slowest: Session 2s, Confirm 1s, Session 0s) / OK [ran] [tree ab7d9c3df9ea] (2026-10-06T01:23:49Z)
- (step 2) `python3 plugin/tests/run.py -k test_session -k Normalise` → exit 0 · Ran 14 tests in 1.9s (8 classes, 16 at a time; slowest: Session 2s, Confirm 1s, Session 0s) / OK [ran] [tree ab7d9c3df9ea] (2026-10-06T01:23:51Z)
- (step 3) `python3 plugin/tests/run.py -k test_session -k Normalise` → exit 0 · Ran 14 tests in 1.9s (8 classes, 16 at a time; slowest: Session 2s, Confirm 1s, Session 0s) / OK [ran] [tree ab7d9c3df9ea] (2026-10-06T01:23:53Z)
- (ac 1) `python3 plugin/tests/run.py -k test_session` → exit 0 · Ran 14 tests in 1.8s (8 classes, 16 at a time; slowest: Session 2s, Confirm 1s, Session 0s) / OK [ran] [tree ab7d9c3df9ea] (2026-10-06T01:23:55Z)
- (ac 2) `python3 plugin/tests/run.py -k test_session` → exit 0 · Ran 14 tests in 1.9s (8 classes, 16 at a time; slowest: Session 2s, Confirm 1s, Session 0s) / OK [ran] [tree ab7d9c3df9ea] (2026-10-06T01:23:57Z)
- (ac 3) `python3 plugin/tests/run.py -k test_session` → exit 0 · Ran 14 tests in 1.9s (8 classes, 16 at a time; slowest: Session 2s, Confirm 1s, Session 0s) / OK [ran] [tree ab7d9c3df9ea] (2026-10-06T01:23:59Z)
- (step 4) `fm docs` → exit 0 · No doc drift in ~/.claude/foreman. [ran] [tree ab7d9c3df9ea] (2026-10-06T01:23:59Z)
- (step 2) `python3 plugin/tests/run.py -k test_session -k Normalise` → exit 0 · Ran 16 tests in 4.3s (8 classes, 16 at a time; slowest: Session 4s, Confirm 1s, Session 0s) / OK [ran] [tree bde188ba5a87] (2026-10-06T01:27:31Z)
- (step 3) `python3 plugin/tests/run.py -k test_session -k Normalise` → exit 0 · Ran 16 tests in 4.3s (8 classes, 16 at a time; slowest: Session 4s, Confirm 1s, Session 0s) / OK [ran] [tree bde188ba5a87] (2026-10-06T01:27:36Z)
- (ac 1) `python3 plugin/tests/run.py -k test_session` → exit 0 · Ran 16 tests in 4.3s (8 classes, 16 at a time; slowest: Session 4s, Confirm 1s, Session 0s) / OK [ran] [tree bde188ba5a87] (2026-10-06T01:27:40Z)
- (ac 2) `python3 plugin/tests/run.py -k test_session` → exit 0 · Ran 16 tests in 4.3s (8 classes, 16 at a time; slowest: Session 4s, Confirm 1s, Session 0s) / OK [ran] [tree bde188ba5a87] (2026-10-06T01:27:45Z)
- (ac 3) `python3 plugin/tests/run.py -k test_session` → exit 0 · Ran 16 tests in 4.3s (8 classes, 16 at a time; slowest: Session 4s, Confirm 1s, Session 0s) / OK [ran] [tree bde188ba5a87] (2026-10-06T01:27:49Z)
- (step 1) `python3 plugin/tests/run.py -k test_session -k Normalise` → exit 0 · Ran 16 tests in 4.3s (8 classes, 16 at a time; slowest: Session 4s, Confirm 1s, Session 0s) / OK [ran] [tree bde188ba5a87] (2026-10-06T01:27:54Z)
- (ac 1) `python3 plugin/tests/run.py -k test_session` → exit 0 · Ran 17 tests in 4.6s (8 classes, 16 at a time; slowest: Session 5s, Confirm 1s, Session 0s) / OK [ran] [tree eef54d3308f6] (2026-10-06T01:29:22Z)
- (ac 2) `python3 plugin/tests/run.py -k test_session` → exit 0 · Ran 17 tests in 4.5s (8 classes, 16 at a time; slowest: Session 4s, Confirm 1s, Session 0s) / OK [ran] [tree eef54d3308f6] (2026-10-06T01:29:26Z)
- (ac 3) `python3 plugin/tests/run.py -k test_session` → exit 0 · Ran 17 tests in 4.6s (8 classes, 16 at a time; slowest: Session 5s, Confirm 1s, Session 0s) / OK [ran] [tree eef54d3308f6] (2026-10-06T01:29:31Z)
- (step 1) `python3 plugin/tests/run.py -k test_session -k Normalise` → exit 0 · Ran 17 tests in 4.6s (8 classes, 16 at a time; slowest: Session 5s, Confirm 1s, Session 0s) / OK [ran] [tree eef54d3308f6] (2026-10-06T01:29:36Z)
- (step 2) `python3 plugin/tests/run.py -k test_session -k Normalise` → exit 0 · Ran 17 tests in 4.6s (8 classes, 16 at a time; slowest: Session 5s, Confirm 1s, Session 0s) / OK [ran] [tree eef54d3308f6] (2026-10-06T01:29:41Z)
- (step 3) `python3 plugin/tests/run.py -k test_session -k Normalise` → exit 0 · Ran 17 tests in 4.6s (8 classes, 16 at a time; slowest: Session 5s, Confirm 1s, Session 0s) / OK [ran] [tree eef54d3308f6] (2026-10-06T01:29:45Z)
- (step 4) `fm docs` → exit 0 · No doc drift in ~/.claude/foreman. [ran] [tree eef54d3308f6] (2026-10-06T01:29:46Z)
- (ac 1) `python3 plugin/tests/run.py -k test_session` → exit 0 · Ran 17 tests in 4.5s (8 classes, 16 at a time; slowest: Session 4s, Confirm 1s, Session 0s) / OK [ran] [tree eef54d3308f6] (2026-10-06T01:30:49Z)
- (ac 2) `python3 plugin/tests/run.py -k test_session` → exit 0 · Ran 17 tests in 4.5s (8 classes, 16 at a time; slowest: Session 4s, Confirm 1s, Session 0s) / OK [ran] [tree eef54d3308f6] (2026-10-06T01:30:49Z)
- (ac 3) `python3 plugin/tests/run.py -k test_session` → exit 0 · Ran 17 tests in 4.5s (8 classes, 16 at a time; slowest: Session 4s, Confirm 1s, Session 0s) / OK [ran] [tree eef54d3308f6] (2026-10-06T01:30:49Z)
- (audit intent) `one foreman:fm-reviewer pass (research T-0323-review), findings fixed test-first, plus a real Haiku session smoke run` → start/list/tail/send/stop/rm/agents for claude, codex, gemini and opencode; detached runner per session; one normalised schema; a real claude -p session resumed by its own id; list --follow for the app [tree eef54d3308f6] (2026-10-06T01:30:49Z)
- (audit adversary) `one foreman:fm-reviewer pass (research T-0323-review), findings fixed test-first, plus a real Haiku session smoke run` → ids fullmatch a fixed pattern (no paths); messages after -- never become options and a leading - is padded; resume ids starting with - are dropped; stop only signals a pid whose command line names this session (/proc or ps), and idle sessions hold no pid [tree eef54d3308f6] (2026-10-06T01:30:49Z)
- (audit edge) `one foreman:fm-reviewer pass (research T-0323-review), findings fixed test-first, plus a real Haiku session smoke run` → odd JSON shapes become raw events instead of killing the runner, which kills its agent if it does go down; send no longer writes meta (no lost agent_session); a stop marker beats a runner that hasn't started its turn; utf-8 with replacement for logs and agent output; tail on a removed session is a clean error [tree eef54d3308f6] (2026-10-06T01:30:49Z)
- (step 1) `python3 plugin/tests/run.py -k test_session -k Normalise` → exit 0 · Ran 17 tests in 4.5s (8 classes, 16 at a time; slowest: Session 4s, Confirm 1s, Export 0s) / OK [ran] [tree 4cde3bfcce9c] (2026-10-06T01:31:06Z)
- (step 2) `python3 plugin/tests/run.py -k test_session -k Normalise` → exit 0 · Ran 17 tests in 4.5s (8 classes, 16 at a time; slowest: Session 4s, Confirm 1s, Session 0s) / OK [ran] [tree 4cde3bfcce9c] (2026-10-06T01:31:10Z)
- (step 3) `python3 plugin/tests/run.py -k test_session -k Normalise` → exit 0 · Ran 17 tests in 4.5s (8 classes, 16 at a time; slowest: Session 4s, Confirm 1s, Export 0s) / OK [ran] [tree 4cde3bfcce9c] (2026-10-06T01:31:15Z)
- (ac 1) `python3 plugin/tests/run.py -k test_session` → exit 0 · Ran 17 tests in 4.5s (8 classes, 16 at a time; slowest: Session 4s, Confirm 1s, Session 0s) / OK [ran] [tree 4cde3bfcce9c] (2026-10-06T01:31:20Z)
- (ac 2) `python3 plugin/tests/run.py -k test_session` → exit 0 · Ran 17 tests in 4.5s (8 classes, 16 at a time; slowest: Session 4s, Confirm 1s, Session 0s) / OK [ran] [tree 4cde3bfcce9c] (2026-10-06T01:31:24Z)
- (ac 3) `python3 plugin/tests/run.py -k test_session` → exit 0 · Ran 17 tests in 4.5s (8 classes, 16 at a time; slowest: Session 4s, Confirm 1s, Session 0s) / OK [ran] [tree 4cde3bfcce9c] (2026-10-06T01:31:29Z)
- (step 4) `fm docs` → exit 0 · No doc drift in ~/.claude/foreman. [ran] [tree 4cde3bfcce9c] (2026-10-06T01:31:29Z)
- (audit intent) `one foreman:fm-reviewer pass (research T-0323-review), findings fixed test-first, plus a real Haiku session smoke run; operator and maintainer lenses in the main thread` → start/list/tail/send/stop/rm/agents for claude, codex, gemini and opencode; detached runner per session; one normalised schema; a real claude -p session resumed by its own id; list --follow for the app [tree 4cde3bfcce9c] (2026-10-06T01:32:34Z)
- (audit adversary) `one foreman:fm-reviewer pass (research T-0323-review), findings fixed test-first, plus a real Haiku session smoke run; operator and maintainer lenses in the main thread` → ids fullmatch a fixed pattern (no paths); messages after -- never become options and a leading - is padded; resume ids starting with - are dropped; stop only signals a pid whose command line names this session (/proc or ps), and idle sessions hold no pid [tree 4cde3bfcce9c] (2026-10-06T01:32:34Z)
- (audit edge) `one foreman:fm-reviewer pass (research T-0323-review), findings fixed test-first, plus a real Haiku session smoke run; operator and maintainer lenses in the main thread` → odd JSON shapes become raw events instead of killing the runner, which kills its agent if it does go down; send no longer writes meta (no lost agent_session); a stop marker beats a runner that hasn't started its turn; utf-8 with replacement for logs and agent output; tail on a removed session is a clean error [tree 4cde3bfcce9c] (2026-10-06T01:32:34Z)
- (audit operator) `one foreman:fm-reviewer pass (research T-0323-review), findings fixed test-first, plus a real Haiku session smoke run; operator and maintainer lenses in the main thread` → an agent that isn't installed shows as an error plus a failed result in the stream (not a silent hang); raw.log keeps the agent's own output for debugging; fm session agents says what's installed [tree 4cde3bfcce9c] (2026-10-06T01:32:34Z)
- (audit maintainer) `one foreman:fm-reviewer pass (research T-0323-review), findings fixed test-first, plus a real Haiku session smoke run; operator and maintainer lenses in the main thread` → one module, one small normaliser per agent with its own test; the event schema and which formats are verified live are in the module docstring [tree 4cde3bfcce9c] (2026-10-06T01:32:34Z)
## Log
- 2026-10-06T01:12:05Z created
- 2026-10-06T01:20:18Z focused
- 2026-10-06T01:32:34Z done
- 2026-10-06T01:32:34Z committed 70ad281 (5 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- decision 2026-10-06: Desktop app architecture: no daemon — the Tauri app drives fm --json locally or over ssh (Tailscale SSH) per device; agent sessions are supervised b…
- research T-0318-agents: Answer.** All four agents have a hook that can block a tool before it runs, except opencode, where a plugin can do it. Each has a JSON-RPC, HTTP …
- T-0324 [FEATURE L, planned, 4 steps] Foreman discipline on codex, gemini and opencode: fm hook --agent and fm agents install
- T-0322 [FEATURE M, done, 3 steps] fm projects --json and fm ui --follow: a device-wide read surface for the desktop app — lesson: A follow stream is the cheapest live AP…
- the similar finished task took 3 steps
## Lessons
- A detached supervisor needs one writer per file: let the runner own meta.json under its lock and give every other command a marker file instead
## Files touched
- plugin/tests/test_session.py
- plugin/lib/fmsession.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
