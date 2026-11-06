# Brainstorm — lens: approaches

- **Tail the CLI's own session transcript for progress** — FEATURE — value 5 — effort M — risk low — category: liveness
  Why: the nixie run showed nothing for minutes. Claude and Codex already write per-session JSONL files (assumption: `~/.claude/projects/*/*.jsonl` and `~/.codex/sessions`), whatever output mode the harness chose. Stream-json parsing (T-1329) covers only one mode; tailing the file also covers `CMD {prompt}` templates and non-streaming runs.
  Done when: a fake runner that appends to a transcript file while printing nothing to stdout makes Activity show those events within 2 s.

- **Detect the harness by process ancestry, not only the env marker** — FIX — value 5 — effort S — risk low — category: duplicate Foreman
  Why: the user wants no duplicate Foreman when Claude is the worker. A lineage env var is lost whenever a worker goes through `nohup`, `tmux` or `env -i`. Assumption: walking parent pids (`/proc` on Linux, `ps` on macOS) for a live `fm code` harness is the backstop.
  Done when: a SessionStart hook run with a scrubbed environment under a fake harness parent emits no Foreman session context.

- **Promote deferred tasks when matching evidence appears** — FEATURE — value 4 — effort M — risk low — category: self-improvement
  Why: about 35 tasks are deferred as "later: needs evidence of…" (T-0862 to T-0869, T-0827 and others). The user wants Foreman to notice what to work on without being asked. A matcher that scores new friction phrases and failure logs against deferred titles would flip a task to queued, with a receipt of the matching quote.
  Done when: a seeded complaint matching T-0862 moves it to queued, and the receipt names the quote.

- **Keep prompt prefixes byte-stable so provider caching works** — PERFORMANCE — value 4 — effort M — risk low — category: token tax
  Why: planner calls cost 66k–133k input tokens. If the harness's system and rules prefix varies per call (timestamps, ordering), the cache never hits. Assumption: the prefix varies today. This differs from slimming the worker, which only shrinks the prefix.
  Done when: a test builds two consecutive planner prompts for one task and asserts an identical first N bytes, and the bench reports the cached-token share.

- **Turn a red CI run into a queued task** — FEATURE — value 4 — effort M — risk low — category: unspoken need
  Why: three of the user's recent asks were "CI red on Linux 3.12…" followed by a hand-written diagnosis. With `gh` present, Foreman could fetch the failing job log, queue a task with the log tail as its failing check, and show it on the home screen.
  Done when: a stubbed `gh run view --log-failed` creates a task whose first criterion reproduces the failing command.

- **Pass workers an environment allowlist** — SECURITY — value 4 — effort S — risk med — category: worker isolation
  Why: every runner inherits the full shell environment, including cloud keys and tokens. Assumption: `spawn_runner` doesn't filter it. A per-runner allowlist (PATH, HOME, its own API key variable) with a `config` override limits what a prompt-injected worker can read or send.
  Done when: a fake worker run with `AWS_SECRET_ACCESS_KEY` set prints an environment without it, and `--env-pass NAME` restores it.

- **Carry lessons between projects through stack cards** — FEATURE — value 3 — effort M — risk med — category: multi-project
  Why: "Lessons carry confidence" (T-0217) is deferred and stack cards exist. Once fm code spans projects, a fix learned in nixie should surface in another Python project, tagged by stack card and shown with its origin.
  Done when: a lesson saved in project A appears in the planner context of project B with the same stack card, and not in a project with a different stack.

- **Run every command in the docs in CI** — CLEAN — value 3 — effort M — risk low — category: docs
  Why: the user asked for better website examples and "I should be able to do anything with it". Docs that drift undermine that, and the repo already enforces "every claim backed by a check that runs". Fenced blocks tagged `fm-run` would execute in a fake HOME and diff their output against the page.
  Done when: editing a documented flag name makes the docs job fail with the page and line.

- **Plan speculatively while the request is being typed (wild)** — FEATURE — value 3 — effort L — risk med — category: latency
  Why: assumption: first-call latency is the felt "not doing anything". After a typing pause, a local or cheap runner drafts a plan, and Enter reuses it if the text is unchanged. Draft planning stays local-only unless the user sets otherwise.
  Done when: a scripted pause-then-Enter shows the plan station completing in under 1 s on a fake runner, and an edited request discards the draft.

- **Plant honeytokens to catch a hijacked worker (wild)** — SECURITY — value 3 — effort M — risk low — category: injection defense
  Why: the deferred T-0791 holds 18 injection and supply-chain ideas. A decoy secret file placed in a scratch location, or a canary string in the repo, flags any worker turn that reads or emits it. The guard already inspects every changed file.
  Done when: a fake worker that prints the decoy value fails the turn with a "tripwire" verdict naming the line.

- **Learn a new CLI by watching you use it once (wild)** — FEATURE — value 3 — effort L — risk med — category: any CLI
  Why: "manage ANY CLI" can't rest on a hard-coded adapter list or `--help` parsing alone. `fm code --watch CMD` would record one hand-driven session in a pty and derive the prompt syntax, the done marker and the stall signature into a runner spec. Assumption: tools like this have consistent prompts and exit patterns.
  Done when: watching a scripted fake REPL produces a runner spec that runs a second request unattended.

- **Run each worker in a systemd user scope when available (wild)** — CLEAN — value 3 — effort M — risk med — category: orphan control
  Why: the nixie planner outlived the quit. A cgroup scope can be killed whole, and it can enforce memory and CPU caps, which process groups cannot. Process groups stay as the macOS and non-systemd fallback.
  Done when: killing the harness with SIGKILL on a systemd host leaves no descendant process after 2 s.
