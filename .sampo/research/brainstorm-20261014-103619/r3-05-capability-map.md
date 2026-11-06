# Brainstorm — lens: capability map

- **Babysit every pushed PR until CI is green** — FEATURE — value 4 — effort M — risk med — category: CI loop
  Why: assumption: no PR or CI follow-through is visible in the pack. Monitor and `gh pr checks --watch` are available but unused, and the 1.2.x release tasks all end in a push.
  Done when: a pushed PR with a deliberately failing check is fixed and re-pushed by Foreman without prompting, and `fm task show` lists each CI run's verdict as evidence.

- **Host the drive from an Agent SDK supervisor instead of tmux** — FEATURE — value 5 — effort L — risk high — category: runtime
  Why: assumption: the SDK offers streaming input, interrupt, and in-process hook and permission callbacks. Today `fm bus` types into panes with send-keys, and the user complains "it sits idle". A supervisor process would own turns, wake the model with a real message and drop the per-hook Python spawn.
  Done when: `fm run --host sdk` finishes a 3-task queue with no tmux, and `bench_hooks.py` shows median hook latency below the current spawn path.

- **Serve a local-first phone cockpit as an installable PWA** — FEATURE — value 4 — effort M — risk low — category: privacy, surfaces
  Why: assumption: web UI exists, but Artifact and PushNotification publish to claude.ai or a phone service. A PWA on LAN or tailnet with local web-push gives the same view, asks and approvals with nothing leaving the owner's network. Cloud features stay behind explicit per-project opt-ins.
  Done when: a phone on the LAN installs the PWA, receives a push for a pending `fm ask`, and approves it, while `fm privacy` shows zero cloud-bound calls.

- **Add a cloud-feature switchboard with default-deny and receipts** — SECURITY — value 4 — effort S — risk low — category: privacy
  Why: the pack lists Artifact, RemoteTrigger, remote isolation, SendMessage and PushNotification as available but unused. Adopting them without a single gate would publish project data. A PreToolUse matcher can allow each one only if the project has opted in, and log every use.
  Done when: calling Artifact in a project without the opt-in is refused with the exact setting to flip, and an allowed call writes a ledger line naming the data classes sent.

- **Detect stale hooks after Foreman edits itself and offer a one-step reload** — FIX — value 3 — effort S — risk low — category: DX
  Why: assumption: Foreman changes its own plugin tree and releases often (1.2.16 to 1.2.27 in recent commits), and T-0418 shows an installed mod lagging the repo. Running sessions keep old hook code with no warning.
  Done when: after touching `plugin/lib`, the next prompt shows a one-line "hooks are stale: reload" note, and clears it after reload.

- **Verify web UIs through Claude's native browser control** — FEATURE — value 3 — effort M — risk med — category: verification
  Why: assumption: Chrome integration is available. `fm smoke` and the screenshot harness are Foreman's own, and a browser the user already has open could check logged-in pages the harness cannot reach.
  Done when: a smoke recipe with `driver: native-browser` loads an authenticated page and attaches a screenshot as evidence.

- **Print a per-task model-share receipt** — FEATURE — value 3 — effort S — risk low — category: user value
  Why: the user asked "can foreman spawn agents of lower models?" (T-0755) and wants fewer tokens. Subagent transcripts record the model per call, so the close-out can state what share ran on haiku, sonnet and opus, and the estimated saving against an all-top-model run.
  Done when: `fm task finish` output includes a "models: haiku 41% / sonnet 38% / opus 21%, est. saved N%" line that matches transcript usage totals within 2%.

- **Give each lane its own `--settings` overlay file** — SECURITY — value 3 — effort M — risk med — category: isolation
  Why: assumption: Claude Code accepts a per-launch settings file. Lanes and `claude -p` children now share `~/.claude` wiring, and the dropped heredoc case shows how hard guarding shared state is. An overlay carries permissions, env and hook switches per lane without touching the global files.
  Done when: two concurrent lanes launch with different permission sets, and neither run edits `~/.claude/settings.json`.

- **Generate a "what each setting costs you" page from measured hook and token data** — FEATURE — value 3 — effort S — risk low — category: docs, simplicity
  Why: the user keeps asking for faster, smarter and simpler together, and MASTER.md documents settings but not their price. Per-hook latency (bench_hooks) and injected-token counts could be joined to each setting.
  Done when: `fm doctor --costs` lists every setting with ms per event and tokens per session, and `fm doctor`'s self-docs check fails if a setting is missing a row.

- **Wild: Scaffold Foreman-disciplined Agent SDK projects** — FEATURE — value 3 — effort L — risk med — category: product reach
  Why: wild; assumption: other agents built on the SDK lack a guard, a ledger and a done-gate. `fm scaffold agent` would emit a starter project that vendors Foreman's guard, evidence ledger and resume logic.
  Done when: the generated agent runs, a dangerous command it attempts is blocked by the vendored guard, and its ledger passes `fm doctor`.

- **Wild: Spawn idle-time patch proposals on cheap models for captured tasks** — FEATURE — value 4 — effort M — risk med — category: speed
  Why: wild; the user said "make sure it doesn't sit idle", and T-0755 to T-0760 are captured but unplanned. A haiku lane in a worktree could draft a candidate diff for each captured S task, held as a proposal and never merged. When the task starts, the builder begins from that diff and the reviewer checks it.
  Done when: with 3 captured S tasks and an idle main lane, 3 proposal branches appear, and starting one records "seeded from proposal" with fewer builder tool calls than an unseeded baseline.

- **Wild: Turn a gripe into a self-checking fix with `fm gripe`** — FEATURE — value 4 — effort M — risk med — category: user value
  Why: wild; T-0317 ("There's new bug feedback") and the user's repeated corrections show complaints arriving as raw sentences. One command would take the sentence plus the last 20 ledger events, draft a reproducing check, run it red, and queue a FIX task that already contains the failing test.
  Done when: running `fm gripe "it started step 3 without updating the step"` yields a queued FIX with a test that fails on the current code.
