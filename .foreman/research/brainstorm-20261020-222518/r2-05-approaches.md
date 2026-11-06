# Brainstorm — lens: approaches

- **Keep one resident worker session per project and runner** — PERFORMANCE — value 5 — effort M — risk med — category: speed
  Why: the nixie run stalled on cold nested Claude calls of 66k–133k input tokens each. T-1327 slims the load, but every call still pays the full start. Hold one `claude -p --input-format stream-json` process (or the CLI's equivalent) open per project, feed it plan, step and fix turns, and recycle it by token count or step kind. Trade-off: context bleeds between steps, so the reset policy matters.
  Done when: a 3-step run through a fake streaming CLI starts the process once (asserted by a spawn counter), and a kill mid-run leaves no orphan.

- **Plan routine requests without a model** — FEATURE — value 4 — effort M — risk low — category: do less
  Why: 7/7 request kinds closed only because the planner worked. Rename, docs and "run X" don't need one. Deterministic planners (grep → edit → check) for those kinds skip the slow, costly planner call. Anything unmatched falls through to the model. Assumption: those kinds make up much of real use.
  Done when: `fm code "rename foo to bar"` closes with zero runner calls in the event log, and its checks fail first and then pass.

- **Give every runner call a deadline, token ceiling and /proc probe** — FIX — value 5 — effort M — risk low — category: stalls
  Why: "just isn't doing anything" came from a silent multi-minute call. Past a soft deadline, read the worker's `/proc` (children, open sockets, cwd, CPU) and print a named reason such as loading plugins, retrying after a 429, or stuck in a tool. Past the hard deadline, salvage the diff (T-0831) and re-ask smaller. This is a different mechanism from the heartbeat and watchdog already planned: it inspects the process, not just the clock.
  Done when: a fake CLI that sleeps 90 s with a child process makes the run print "waiting on <child cmd>" within the soft deadline, then salvage at the hard one.

- **Describe runners as data manifests** — FEATURE — value 4 — effort M — risk low — category: any CLI
  Why: "any CLI" is only true if adding one doesn't need Python. A runner is a small TOML file: argv template, stream format (jsonl, stream-json or plain), how to cancel, how to read cost, and native instruction file names. `fm code runner add FILE|URL` validates it against a conformance script. Trade-off: some CLIs will still need code.
  Done when: a manifest for a fake CLI, dropped into `~/.foreman/runners/`, runs a task end to end with no Python edits.

- **Project one rules source into each CLI's native instruction channel** — FEATURE — value 4 — effort M — risk med — category: parity
  Why: Claude gets Foreman's rules through hooks, but codex, gemini and aider get nothing. Translate the project's rules into each CLI's own channel (flags, env, or a temp-injected `AGENTS.md`/`GEMINI.md`), never leaving files in the repo. Trade-off: injection shapes differ per CLI.
  Done when: after a run with a fake codex manifest, `git status` is clean and the CLI's recorded args or env contained the rules.

- **Cage the worker in bubblewrap or sandbox-exec** — SECURITY — value 4 — effort M — risk med — category: sandbox
  Why: the guard judges changed files after the fact, and the safety constraint says never weaken it. A write-only-in-project namespace makes the guard hold for CLIs that have no hooks of their own. This is separate from the network-namespace idea already listed. Fall back with a visible note when the tools are missing.
  Done when: a worker that tries `touch ~/outside` fails inside the cage, and the run reports the cage state in its header.

- **Wrap hand-launched CLIs with PATH shims** — FEATURE — value 4 — effort S — risk med — category: shell (wild)
  Why: assumption: the user also types `claude` or `codex` by hand. `fm setup` puts `~/.foreman/shims/{claude,codex,gemini,aider}` first on PATH. Each shim sets the worker-role env marker (so there's no duplicate Foreman), takes a lease, and then execs the real binary. This turns "manage ANY CLI" into a property of the shell, not of one app.
  Done when: running `claude` through the shim in a Foreman-launched pty shows the worker marker and a lease file, and the shim is removable with one command.

- **Let a new runner earn trust on probation** — FEATURE — value 3 — effort M — risk low — category: trust (wild)
  Why: a CLI auto-discovered by T-1328 is unproven. For its first N steps per request kind, a proven runner reviews its diff read-only. After N clean passes it runs unattended for that kind. The trust ledger is shown on the home screen. Trade-off: slower and costlier at the start.
  Done when: a fake runner whose first 3 diffs are rejected stays on probation, and a clean one is promoted after N passes, both visible in `fm code runners`.

- **Store run ledgers in git refs so they travel with the repo** — FEATURE — value 3 — effort M — risk med — category: persistence (wild)
  Why: multi-project management currently needs some registry. Writing journals to `refs/foreman/runs/*` makes projects self-describing, since the home screen just walks repos it finds, and a clone on another machine keeps its history. Trade-off: it must never be pushed by default, which touches the publish grant.
  Done when: a fresh clone via a local remote shows prior runs only after an explicit `fm sync`, and `git push` alone never sends them.

- **Run a worker on another machine over ssh** — FEATURE — value 3 — effort L — risk high — category: remote (wild)
  Why: assumption: the user has a GPU box or a second machine. The harness and guard stay local; the runner executes in a remote worktree and returns a patch. The guard then judges the patch exactly as it judges local changes. Trade-off: network failure modes, and the guard needs the patch to be complete.
  Done when: a loopback-ssh test runs a fake CLI "remotely", and a patch touching a guarded path is refused locally.

- **For Claude users, make bare `fm code` a thin launcher** — FEATURE — value 3 — effort S — risk low — category: reuse
  Why: reuse beats rebuild for the most common case. On a machine with Claude and the plugin installed, `fm code` with no request execs `claude` with the plugin and a per-project profile. That gives the real Claude app, no nested session and no duplicate Foreman. The harness-run loop is kept for other models and CLIs, and for `--task`. Trade-off: the harness no longer controls the loop in this mode, which may contradict "make fm code itself amazing".
  Done when: `fm code` in a project with the plugin installed starts exactly one Foreman context, which a hook-call counter confirms.

- **Show the cost of a session before it starts** — FEATURE — value 3 — effort S — risk low — category: transparency
  Why: the 66k–133k tokens per call were discovered only afterwards. A one-token probe measures the real startup tax per runner and project. The line "this runner starts at ~90k tokens; slim profile ~8k" shows before the first request and in the picker. This complements the profile work by making the saving visible and checkable.
  Done when: the picker shows a measured tax per runner, and a fake CLI that reports usage in its stream yields a matching number.

- **Mine the user's own complaints into a regression suite** — FEATURE — value 4 — effort M — risk med — category: self-improvement (wild)
  Why: the user said they shouldn't have to ask. Detect friction phrases in the user's own messages ("isn't doing anything", "why can't I"). Foreman then opens a diagnostic task with a failing check, such as "bare `fm code` shows progress within 10 s in a pty", before any fix. The suite grows with each complaint. Trade-off: false positives need a visible receipt and an off switch.
  Done when: feeding the phrase "it just isn't doing anything" to a test hook creates one task whose verify command fails on the current build.
