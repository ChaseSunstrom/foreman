# Brainstorm — lens: capability map

- **Constrain the model's slot output at the decoder** — FEATURE — value 5 — effort M — risk low — category: reliability
  Why: the harness has the model fill one small checked JSON slot at a time, and weak local models fail that check the most. llama.cpp, vLLM and Ollama accept a JSON-schema or grammar parameter, and OpenAI-style endpoints accept `response_format`, so malformed slots can be prevented instead of retried. Assumption: the model client doesn't use these today.
  Done when: a fake endpoint that honours the schema parameter gets it on every slot call, and a test shows zero parse retries where the unconstrained run needed at least one.

- **Ask one question when a request is ambiguous** — FEATURE — value 5 — effort M — risk low — category: intake
  Why: Claude Code's ask-a-question flow is missing here. The user's "just isn't doing anything" runs suggest the planner is guessing silently. Unattended runs decide, log the assumption, and continue.
  Done when: a vague request ("make it faster") in the TUI shows a multiple-choice prompt before the plan, and with `--unattended` it logs a "decided: X because Y" line instead.

- **Add a slash-command prompt box** — FEATURE — value 4 — effort M — risk low — category: app UX
  Why: the user wants fm code to feel like Claude. The pack lists keys (n, h, m, d, t) but no input line with history, `/model`, `/project`, `/cost`, `/queue`, `/why`, multiline entry, or Up-arrow and Ctrl-R recall. Assumption: no such line exists yet.
  Done when: typing `/model codex` in a pty test switches the runner, and Up-arrow restores the previous request across restarts.

- **Store API keys in the OS keychain** — SECURITY — value 4 — effort S — risk low — category: secrets
  Why: `models.json` plus env keys is the only credential path the pack shows. Add `secret-tool`, macOS `security` or `pass` lookup via a `key: "keychain:name"` reference. Plaintext keys in a file that "config import" may also copy around is a leak waiting to happen.
  Done when: a config using `keychain:` resolves through a stub secret tool, and `fm code config explain` and the run logs never show the value.

- **Advise which local model fits this machine** — FEATURE — value 4 — effort M — risk low — category: local models
  Why: the user wants "ANY model", and local Ollama and LM Studio are named. Nothing checks VRAM or RAM against model size, offers to pull a fitting model, or starts a stopped server. Assumption: stdlib can read `/proc/meminfo` and `nvidia-smi` or `system_profiler` output.
  Done when: with a fake hardware profile and a fake Ollama tag list, `fm code runners --fit` ranks the models that fit and says why the others don't.

- **Classify a red check as flaky or real** — FEATURE — value 4 — effort S — risk low — category: verification
  Why: the harness proves "fails first, passes after". A flaky test passes the first check for the wrong reason, or blocks a close for no reason. Rerun the failing check N times and record the pass rate in the receipt.
  Done when: a test that fails 1 time in 3 is labelled flaky and doesn't count as fail-first proof, and a deterministic failure still counts.

- **Enforce a declared file scope per plan** — SECURITY — value 4 — effort M — risk med — category: guard
  Why: worker turns are judged per changed file by the guard, but the plan's intended files aren't a contract. An edit outside the plan's files should pause for a re-plan or approval. This tightens the guard and doesn't loosen it.
  Done when: a fake worker that touches an undeclared file triggers a visible "out of scope" verdict, and the same edit passes after the plan is amended.

- **Fire user hooks and webhooks on run events** — FEATURE — value 3 — effort S — risk med — category: integrations
  Why: extensions are Python panels only. A `.foreman/code.toml` list of `on = task.closed|run.failed|needs-you` commands, run through the guard, covers notify-send, Slack and CI triggers without code. Assumption: the harness already emits one event stream.
  Done when: a configured `on task.closed` command receives a JSON payload on stdin in a test, and a guard-refused command is reported and doesn't run.

- **Lay prompts out for provider caching** — PERFORMANCE — value 3 — effort S — risk low — category: cost
  Why: the user hit 66k–133k input tokens per planner call. For direct Anthropic and OpenAI-style endpoints, a stable prefix (rules, repo map) with `cache_control` markers cuts the repeat cost, and the receipt can show cached versus fresh tokens.
  Done when: a recorded two-call run shows the second call's cached-token count above 0, and the prefix is byte-identical between calls.

- **Ship install channels that fix `fm` not being on PATH** — FIX — value 4 — effort M — risk low — category: distribution
  Why: `fm` wasn't a command in the user's shell, which was fixed by hand. They run Arch and have a `nixie` project. Provide a Nix flake, an AUR PKGBUILD, a Homebrew formula and a checksum-verified installer that links `~/.local/bin/fm`.
  Done when: in a clean container, the installer puts `fm` on PATH and `fm code --version` works, and a tampered checksum aborts it.

- **Wild: Backtest a runner on the repo's own history** — FEATURE — value 4 — effort L — risk med — category: evaluation
  Why: wild. Mine past bug-fix commits that include a test, check out the parent, give the runner the commit message as the request, and score it by whether the original test passes. This gives real, per-repo routing evidence without hand-made bench cases. Assumption: enough fix-with-test commits exist.
  Done when: `fm code backtest --runner claude -n 3` prints pass or fail per historical commit on a fixture repo.

- **Wild: Discover model servers across the LAN** — FEATURE — value 3 — effort M — risk med — category: local models
  Why: wild. mDNS and a port probe find other machines' Ollama and llama.cpp servers, so a laptop can borrow the desktop's GPU. They are listed as runners, labelled "remote", and never used without opt-in because the prompts leave the machine.
  Done when: with a stub server on a second loopback port, `fm code runners --scan` lists it as unapproved, and a run refuses it until approved.

- **Wild: Run the queue only when the machine is idle and plugged in** — FEATURE — value 3 — effort M — risk low — category: scheduling
  Why: wild. The "unattended with a stop-line" idea covers when to stop. This covers when to start: pause when keyboard idle time drops, on battery, or when the load average rises, and resume quietly. Pausing is by SIGSTOP on the process group, so no work is lost.
  Done when: a fake "user active" signal pauses a running worker within 2 s and resumes it when the signal clears.

- **Split a big request into a dependency graph of tasks** — FEATURE — value 4 — effort L — risk med — category: planning
  Why: today one request becomes one task. Epic-sized asks ("make fm code amazing") need ordered subtasks, each checked, with the dependent ones blocked until the earlier ones close. The existing queue and the "blocked" state already hold this.
  Done when: a request that names three separable changes creates three tasks with `blocked-by` links, and they run in dependency order in a fake-runner test.
