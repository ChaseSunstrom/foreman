1. **Answer.** Foreman has a per-project JSON view model (`fm ui --json`) and a read-only MCP server. The only cross-project data are a hand-readable `registry.md`, the shared `state/events.jsonl` and the per-session snapshots. There is no global `--json` command. Session control is Claude-only: `claude remote-control` under systemd, `claude -p` for `fm run`, and git worktrees for lanes. The guard core is mostly agent-agnostic, but the hook handlers read Claude Code's payload fields directly.

2. **Findings: machine-readable surfaces**
- `fm ui --json` is built by `view(p)` in `plugin/lib/fmwatch.py:375-407` and printed by `cmd_ui` at `fmwatch.py:410-420`. Output is `{"v":1,...}`, or `{"v":1,"project":null}` outside a project. Per-project only. High.
- Its fields are: project, root, mode{autonomy, drive, sensitive, trust, standing}, active{brief detail, stage, audits, blockers}, next, queue (20), inbox (10), approvals, closed, today_done and resume_after_reload. It also carries budget, bench, research, vetoes, revisit, recent, health, a `watch` path list, latency and checks. Items waiting on plan approval include a `plan` object (`fmwatch.py:358-362`). High.
- `--json` is added to every command by `add()` (`plugin/lib/fmcli.py:2062`), but it only takes effect where the handler calls `fmcli.out` (`fmcli.py:27-31`). `out()` is called by capture, task ops, focus, drive, autonomy, queue and lane. The same check in `fmcli.py:79` covers init. Commands that don't call it ignore the flag. `fm state` is only checked at `fmcli.py:150`, medium. High.
- `fm mcp` (`plugin/lib/fmmcp.py:16-29`) is read-only and exposes 7 tools: `state`, `next`, `recall`, `research_list`, `research_read`, `task_show`, `checks`. It takes no project argument and serves nothing from a sensitive project (`fmmcp.py:52-53`). It shells out to `fm` (`fmmcp.py:44-47`). Single project (cwd). High.
- Layout: `state/projects/<slug>/{meta.json,ledger.jsonl,tasks/,research/,run.lock,progress.line}`, per `fmcore.py:446-459`, `fmcore.py:596`, `fmserve.py:112`, `fmwatch.py:401`.
  - `registry.md` is the global project index (`fmcore.py:498-504`), markdown only. `all_projects()` (`fmcore.py:446`) is the only multi-project enumerator, and no command exposes it as JSON.
  - `state/events.jsonl` is global (`fmhooks.py:123-130`) and carries `session_id` and `project`. Event kinds: `guard_block`, `bg_start`, `bg_done`, `drive`, `drive_wait`, `drive_reload`, `subagent_start`, `subagent_stop`, `next`, `hook_ms`, `tool`, `tool_fail` (`fmhooks.py:410`, `1096`, `1466`, `1512`).
  - `ledger.jsonl` is per project, one line per event: `{ts, session_id, project, task, event, data}` (`fmcore.py:591-598`).
- `state/sessions/<sid>.json` is written by the Claude Code statusline hook (`plugin/hooks/statusline:119-129`). Fields: ts, session_id, project, cwd, model, context_pct, context_size, cost_usd, lines_added, lines_removed, rate_limits, cache_hit_ratio. It is global (across projects) but only exists for Claude sessions that run the statusline. High.

3. **Findings: session management**
- `fm serve` writes a systemd user unit (`fmserve.py:60-77`). The argv at `fmserve.py:65-66` is `env claude remote-control --name "<dir> (foreman)" --spawn same-dir [--permission-mode M]`. Start is at `fmserve.py:119-140` (`systemctl --user enable --now`). Stop is at `fmserve.py:157`. List/status are at `fmserve.py:184-210`. The CLI prints text only. Start also forces autonomy full and drive on. High.
- `fm run` builds argv in `_claude_cmd` (`fmserve.py:306-309`): `claude -p <prompt> [--permission-mode] [--model]`. The single-task call is at `fmserve.py:547`. Parallel lanes use `Popen` with `start_new_session=True` and `FOREMAN_DRIVE_TASK` set (`fmserve.py:327-328`, max 3 at `fmserve.py:264`). `fm run` is mutually exclusive with `fm serve` (`fmserve.py:488`) and holds an flock on `run.lock` (`fmserve.py:491-495`). Logs go to `state/logs/run-<slug>.log`. High.
- `fm lane` (`plugin/lib/fmlanes.py:16-79`) runs `git worktree add` at `<main>.lanes/<id>` on branch `foreman/<id>`. Actions are list, new, rm, brief. All return JSON via `out`. High.
- Other `claude` argv builders: `fmresearch.py:231`, `fmideas.py:32`, `fmbench.py:244`.

4. **Findings: Claude coupling and the adapter seam**
- Payload parsing is in the handlers `HANDLERS` (`fmhooks.py:1565-1571`) and `_pre_tool_use` (`fmhooks.py:703`). They read `tool_name`, `tool_input`, `session_id`, `cwd`, `transcript_path`, `agent_transcript_path`, `last_assistant_message`, `tool_use_id` and `scratchpad_dir`. The block reply is Claude's `hookSpecificOutput` plus exit code 2 (`fmhooks.py:752-755`). High.
- Tool names are Claude's: `FILE_TOOLS = {Write,Edit,MultiEdit,NotebookEdit}` and `Bash` (`fmguard.py:20`, `49-57`). The guard itself is pure, with no imports from the rest of Foreman (`fmguard.py:24`).
- Adapter seam:
  - `fmguard.findings(tool_name, tool_input, ctx)` (`fmguard.py:49`)
  - `fmguard.check(...)` (`fmguard.py:60`)
  - `fmguard.message(block, ctx)` (called at `fmhooks.py:741`)
  - `fmhooks._guard_ctx(pl, guard)` (`fmhooks.py:777`), which needs only cwd and scratchpad_dir
  - `fmhooks._guard_decision(pl, guard)` (`fmhooks.py:697`)
  - The adapter has to map the other agent's tool names and payload to `Bash`/`Write`/`Edit` and `{command|file_path}`.

5. **Findings: mutating actions (all via `fm`, with `-p SLUG`)**
- Capture: `fm capture` (`fmcli.py:2079`), `--json` works (`fmcli.py:170`).
- Drive: `fm drive on|off` (`fmcli.py:1475-1481`), `--json` works.
- Autonomy: `fm autonomy standard|full` (`fmcli.py:1979-1988`), `--json` works.
- Plan approval: `fm task set ID approved=true` (`fmcli.py:14`, `930`; the `set` parser is at `fmcli.py:2167`).
- Start: `fm focus` (`fmcli.py:1090`).
- Drop: `fm task drop` (`fmcli.py:2245`).
- Guard-category asks: `fm ask` (`fmcli.py:1310`). It only records the request. The grant comes from the user's own prompt (`fmcli.py:1311`), so the app cannot grant it. `--json` support is not confirmed.

6. **Risks / surprises**
- For the global view, the app must walk `projects/*/meta.json` itself, or add a new `fm projects --json`.
- `fm serve` status, start and stop have no JSON mode, so the app would have to parse text or call `systemctl`.
- Reading `ledger.jsonl` or `events.jsonl` directly bypasses nothing, but the format is not versioned. Only `fm ui` carries `v:1`.
- `fm mcp` is single-cwd, so one process is needed per project.

7. **Not checked**
- Whether `fm state --json`, `queue --json` and `ask --json` give useful output.
- Per-project `meta.json` schema.
- The `fm run` loop beyond line 540.
- The remote/sync features.
- `mods/foreman-ui`.
