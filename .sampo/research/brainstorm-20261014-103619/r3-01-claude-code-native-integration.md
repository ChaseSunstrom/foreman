# Brainstorm — lens: Claude Code native integration

- **Probe the native tools and publish a verified field guide** — FEATURE — value 4 — effort M — risk low — category: native tools
  Why: wild. Assumption: the model's knowledge of Artifact, Monitor, SendMessage and ReportFindings trails the live behaviour (cutoff gap, 0 references today). A nightly throwaway session calls each native tool with harmless inputs and records payload shape, size caps, latency and failure text. The result is `native-fieldguide.md`, which Foreman reads before first use of a tool.
  Done when: `fm doctor` lists every tool on the live list with a probe result less than 7 days old, and a test fails if a tool Foreman calls has no field-guide entry.

- **Route every mechanism through a capability ladder** — CLEAN — value 4 — effort M — risk med — category: architecture
  Why: the earlier rounds proposed one-off fallbacks (SendMessage over send-keys, Monitor over polling, ReportFindings over a custom reviewer). Without a shared registry that is a dozen scattered if-trees. Each behaviour (wake, notify, review, publish, spawn) declares an ordered list of mechanisms with a live probe, and the first available one is used. Each use leaves a receipt saying which rung served it.
  Done when: `fm wiring` prints rung, probe time and last receipt for each behaviour, and a test with the native rung stubbed out shows the fallback running.

- **Audit settings shadowing at session start** — SECURITY — value 4 — effort S — risk low — category: guard integrity
  Why: Foreman runs in bypass mode and its guard is the only brake. A project-level or local settings file can disable hooks, flip the plugin off, override `env` or add allow rules. Assumption: `fm doctor` checks the install, not the merged per-project result. The audit reads all settings scopes and warns on anything that weakens Foreman's hooks.
  Done when: a fixture project whose settings disable hooks makes SessionStart emit a named warning and write a ledger event, and a clean project emits nothing.

- **Add an air-gap dial for cloud-bound native tools** — SECURITY — value 4 — effort M — risk med — category: privacy
  Why: Artifact, PushNotification, RemoteTrigger, remote isolation and cloud-bound SendMessage all send data off the machine, and the privacy gap is on the thin list. One setting, `cloud=off`, writes native deny rules for them, makes Foreman's own code paths skip them, and has `fm doctor` prove the result with a probe call.
  Done when: with `cloud=off`, a scripted attempt to publish an Artifact is denied and ledgered, and `fm doctor` reports "air-gapped: verified".

- **Move installer flags and toggles into plugin `userConfig`** — CLEAN — value 3 — effort M — risk med — category: simplicity
  Why: `install.sh` has 8 flags, plus many `fm` toggles and settings files. Assumption: plugin manifests can declare typed user config with a native config UI. The native config would replace the flag matrix and the state a user can't see.
  Done when: a fresh install needs zero flags, the settings appear in the native plugin config screen, and `--security` and `--docs` become two config values with the same effect.

- **Hide skills the model never uses** — PERFORMANCE — value 3 — effort S — risk low — category: token cost
  Why: 73 skill descriptions are in context every session, and the user keeps asking for token savings. Transcript mining shows which skills are ever auto-invoked. Skills with no automatic use get `disable-model-invocation` (or user-only) and are called by `fm` or by name.
  Done when: the injected skill-description token count drops by a measured amount on a baseline session, and `fm bench` shows no regression.

- **Show Foreman state in the spinner verbs and tips** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: wild. The user complained that "it will start working on different steps without updating the step". The spinner is the one line always on screen while the model works. Assumption: spinner verbs and tips are settable in settings and read live. Foreman writes a phase-aware set such as "Verifying T-0754 step 3/5…" and "Waiting on review…".
  Done when: during a run the spinner text names the current task and step, and it updates after `fm task step`.

- **Bring up Foreman inside remote lanes from a repo-pinned plugin** — FEATURE — value 4 — effort L — risk med — category: remote
  Why: earlier rounds proposed remote isolation, cloud routines and a cloud sibling, but a cloud checkout has no `~/.claude/foreman`. The repo pins the plugin and marketplace in its settings. The lane receives its task bundle, and on exit returns a branch plus a ledger patch that the local Foreman merges.
  Done when: a remote lane started on a clean repo loads the guard, executes one task, and its ledger events appear locally after merge.

- **Resolve models by role from the live roster** — FEATURE — value 4 — effort M — risk med — category: model routing
  Why: T-0755 asks whether Foreman can spawn lower-tier agents, and `scout=haiku` and `"sonnet"` are hardcoded. Routing tables store roles (cheap-reader, builder, judge). A resolver maps roles to whatever the live roster exposes, probes that each model exists and accepts the effort setting, and falls back when it doesn't.
  Done when: removing a model from the resolver's roster in a test reroutes the role with a ledgered notice, and no model name appears in the lanes code.

- **Bundle model, effort, style and permissions into task-class postures** — FEATURE — value 3 — effort M — risk med — category: orchestration
  Why: model, effort, fast mode, output style and permission mode are tuned separately across the earlier ideas. A posture such as "S-fix", "L-plan" or "night-verify" sets them together at task start and restores the previous values at close.
  Done when: starting an S task and an L task shows different, logged posture values, and the previous settings return after `fm task finish`.

- **Back `fm smoke` with the native browser tools for logged-in flows** — FEATURE — value 3 — effort M — risk med — category: verification
  Why: the existing screenshot harness has its own tmux and browser plumbing and can't reach authenticated pages. Assumption: the host exposes a browser-control tool in the session. Smoke prefers it when present and keeps the old path as the fallback rung.
  Done when: a smoke run against a login-gated fixture page captures a screenshot of the post-login view.

- **Label each step so the native rewind picker is readable** — FEATURE — value 3 — effort M — risk med — category: undo
  Why: wild. Foreman can already resync after a native rewind, but the picker only shows raw prompts. Assumption: a hook can add a marker the picker displays. Each step start leaves a marker like "T-0754 step 3: add retry" so the user rewinds to a named step.
  Done when: after three steps, the native rewind list shows three named Foreman markers, and rewinding to one makes `fm resume` report that step.

- **Keep one persistent push notification that updates in place** — FEATURE — value 3 — effort S — risk low — category: notifications
  Why: wild. Assumption: pushes can be keyed or replaced. Instead of a stream of pings, a single notification mutates through "running step 3/5", "needs you: choose A/B" and "done". It fires only on state change.
  Done when: a three-step task produces one notification slot with at least three successive texts, not three separate entries.

- **Replay recorded hook payloads in a hot-reload dev loop** — FEATURE — value 3 — effort M — risk low — category: developer experience
  Why: the repo has 341 files, 149 tests and a hook latency gate, but each edit needs a manual reload and re-run. `fm dev` watches `plugin/`, reloads the plugin in a dev session, and replays the last N real payloads. It prints changed hook outputs and latency deltas against `bench_hooks.py`.
  Done when: saving a hook file prints "output diff: 0/20, p95 +2 ms" within 5 seconds, and a deliberately broken hook shows the diff.
