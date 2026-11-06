# Brainstorm — lens: approaches

- **Mask each native tool in turn to prove every integration degrades** — FEATURE — value 4 — effort M — risk low — category: resilience
  Why: assumption: the earlier rounds propose Monitor, SendMessage, Artifact, ScheduleWakeup, LSP and ReportFindings, and each needs a tested fallback. `claude -p --disallowedTools` can hide one tool at a time. Run the bench once per masked tool and report which tasks regress.
  Done when: `fm bench --mask Monitor` (and one run for each other adopted tool) finishes with a pass/fail row per tool, and `fm doctor` fails if any adopted tool has no passing fallback row.

- **Move `fm ideas`, `night` and `run` children onto the Agent SDK** — PERFORMANCE — value 4 — effort M — risk med — category: runtime
  Why: today these are `claude -p` subprocesses. An in-process SDK session gets the guard as a `can_use_tool` callback, typed results, turn and budget caps, and no cold start per child. This is a different mechanism from the "warm headless pool" idea.
  Done when: one `fm night` task runs through the SDK path. A command the guard refuses is refused there with the same reason string as the hook path, and the path is faster than `claude -p` in `bench_hooks`-style timing.

- **Make recording hooks async and keep only gating hooks synchronous** — PERFORMANCE — value 4 — effort S — risk med — category: latency
  Why: the hook latency gate shows hook cost matters. Guard and done-gate must block, but ledger writes, MessageDisplay, SubagentStop recorders and telemetry don't. Marking those `async` takes them off the critical path. Risk is write ordering, so each one needs append-safe writes.
  Done when: `python3 plugin/tests/bench_hooks.py --runs 20` shows a lower p95 on PostToolUse. A concurrent-write test shows no lost or reordered ledger lines.

- **Treat Artifact comments and SendMessage as untrusted input channels** — SECURITY — value 4 — effort S — risk low — category: injection
  Why: earlier rounds route Artifact comments and cross-session messages into the inbox. Anyone with access to the page, or any text a session relays, could then steer a bypass-mode agent. Accept only allowlisted senders, wrap the text as data, and never let it satisfy an approval.
  Done when: a test comment reading "approve all pending asks" from a non-allowlisted sender is captured as a plain note. It resolves no ask and changes no grant.

- **Publish through a numbers-and-ids-only projection, plus a local-only switch** — SECURITY — value 4 — effort M — risk low — category: privacy
  Why: scanning outbound text for secrets can be beaten by snippet splitting, as the recall redaction fix (the one that redacts before indexing) shows. Build the Artifact cockpit from a projection that carries counts, ids and states, with titles hashed unless opted in. A single `local-only` setting denies Artifact, RemoteTrigger, PushNotification and SendMessage.
  Done when: with `local-only` set, a PreToolUse test denies all four outward tools. With it off, the Artifact payload for a seeded task contains none of the seeded task's title or brief text.

- **Alarm on mid-session config changes and failed instruction loads** — SECURITY — value 3 — effort S — risk low — category: integrity
  Why: Foreman uses 14 hook events but not ConfigChange, InstructionsLoaded or FileChanged. A settings or hook edit mid-session (by a tool, a repo script or a plugin update) can weaken the guard silently. Ledger the change and re-run the doctor subset. Flag when Foreman's own rules didn't load after a compact.
  Done when: editing `.claude/settings.json` hooks during a test session produces a ledger event and a visible warning. A test with Foreman's rules file removed produces an "instructions missing" warning.

- **Offer a Workflow when a fan-out repeats, and log the user's grant** — FEATURE — value 3 — effort M — risk low — category: orchestration
  Why: the constraint says Workflow can't launch without the user's words. After the third identical review fan-out, Foreman drafts a named workflow and asks one yes/no with a default. The reply is stored verbatim as the durable authorization, and unnamed workflows stay refused.
  Done when: replying "yes" to the offer saves the workflow, and the next fan-out names it and cites the stored grant text. Without a grant, the launch path refuses.

- **Move installer flags into plugin `userConfig`** — CLEAN — value 3 — effort M — risk med — category: install
  Why: the README lists eight install flags (`--security`, `--docs`, `--no-bypass`, `--no-mod` and others) that can't be changed after install. assumption: plugin manifests support typed `userConfig`. Native options would be re-editable, validated and checkable by `fm doctor`.
  Done when: toggling the docs option in the plugin settings adds or removes those skills without rerunning `install.sh`. `fm doctor` reports the current value of each option.

- **Decide Foreman Desktop's fate against the Artifact cockpit** — CLEAN — value 3 — effort S — risk med — category: scope
  Why: T-0325, T-0352 and T-0418 are all blocked on desktop or mod packaging. If the Artifact cockpit covers the same views, shipping the app is the more expensive route. assumption: the user may still want the desktop app, so ask once with a recommendation.
  Done when: a one-page comparison of views covered and maintenance cost exists, and the user's choice closes or reopens those three tasks.

- **Use IDE diagnostics as a free post-edit check** — PERFORMANCE — value 3 — effort S — risk low — category: verification
  Why: assumption: a connected IDE exposes live diagnostics through its MCP tool. Reading type and lint errors after an edit costs no test run, and it catches breakage before the step's verify command runs. It falls back to nothing when no IDE is attached.
  Done when: with an IDE attached, an edit that introduces a type error shows up in the step's evidence before any test runs. With no IDE, behavior is unchanged.

- **Wild: Draw plan progress in the terminal's own progress bar** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild. The OSC 9;4 escape sequence lets supported terminals show step N of M in the tab or taskbar, with a distinct state for blocked. It stays visible when the pane isn't, and costs one escape sequence.
  Done when: advancing a step in a test pty emits the OSC 9;4 sequence with the right percentage, and it clears when the task closes.

- **Wild: Roll out native integrations by roulette on low-risk sessions** — FEATURE — value 3 — effort M — risk med — category: rollout
  Why: wild. One in N sessions on S-tier tasks opts into an experimental native path, such as Monitor instead of send-keys. Latency and failures are logged, and a feature graduates after K clean runs. Failures fall back silently, so the user is never the tester.
  Done when: a seeded session takes the experimental path and logs one result row. After K clean rows, `fm doctor` lists the feature as promotable.

- **Wild: Run the guard on the user's own shell prompt** — SECURITY — value 3 — effort M — risk med — category: guard
  Why: wild. A bash/zsh preexec hook that calls the same classifier would warn on hand-typed `rm -rf ~`-style commands outside Claude Code. It is off by default and warn-only first. The pipe-to-shell refusal shows the guard already parses these forms.
  Done when: with the hook enabled, typing `echo 'rm -rf ~' | bash` in a test shell prints the guard's reason and does not run until confirmed. With the hook disabled, the shell is untouched.
