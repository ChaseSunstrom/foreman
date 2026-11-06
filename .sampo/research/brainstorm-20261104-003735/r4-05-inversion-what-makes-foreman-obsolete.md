# Brainstorm — lens: inversion: what makes Foreman obsolete

- **Tag every host workaround with a repro, and delete it when the repro goes green** — CLEAN — value 4 — effort M — risk low — category: host-gap
  Why: the drive carries several patches for engine gaps (T-0575, T-0115, T-2873, T-2900, T-2901): `background_tasks` omits running subagents, event-scan tails are too short, resumed sessions leave dead work open. Each one is code that a host fix would make obsolete.
  Done when: every `# HOSTGAP:` marker in `plugin/lib/sampo/` points to a repro script, and a version-change run flips a stubbed-fixed repro to green and opens a "delete workaround" task naming the marker.

- **Run a minimal drive first and escalate to the full drive only on a stall** — FEATURE — value 5 — effort M — risk med — category: drive-simplicity — wild
  Why: assumption: a stateless loop (read the queue head, run one `-p` call, verify, repeat) cannot hit most of the 0→0.1 drive-stop classes, since those come from counting agents, pacing and phantom holds. If it matches the smart drive on overnight yield, most drive logic is dead weight.
  Done when: on a replayed night, the 40-line loop completes at least 90% of the tasks the full drive does, and the full drive starts only after the loop logs a stall record.

- **Audit other agents' unattended PRs as a verifier-only role** — FEATURE — value 4 — effort M — risk low — category: succession
  Why: if the host or forge gains native routines and issue agents, Sampo's starting of work becomes redundant, but proof-before-merge does not. Assumption: the user will have PRs authored by agents Sampo never launched.
  Done when: `sampo audit-pr <url>` runs the diff through the done-gate and posts a clause-receipt comment on a PR that a different tool created, with no Sampo task needed.

- **Find duplicate schedulers when a trigger is registered** — FIX — value 3 — effort S — risk low — category: triggers
  Why: assumption: the user already has cron, systemd timers, GitHub Actions `schedule:`, dependabot or host routines. Two schedulers doing one job is the first sign a Sampo trigger is surplus.
  Done when: registering a trigger lists any matching crontab line, user unit, workflow `schedule` or routine in a scratch fixture, and refuses without `--allow-duplicate`.

- **Count review minutes against minutes saved for every trigger** — FEATURE — value 5 — effort M — risk low — category: value-ledger
  Why: existing ideas count output taken, not the human cost of taking it. A trigger whose results take longer to review than to write by hand is net-negative even when merged.
  Done when: the web UI records open-to-merge or discard time per triggered result, and a trigger with review time above its manual estimate for 14 days is auto-parked with the numbers shown.

- **Probe whether background runs bill from a separate quota pool and route by it** — FEATURE — value 3 — effort S — risk med — category: cost
  Why: the request wants unlimited local-model background volume, while the usage pace and budget cap exist for the shared pool. If the host prices background separately, the pace logic for it is obsolete.
  Done when: `sampo doctor` prints "background pool: shared / separate / unknown" from a recorded probe, and the pace degrade path is skipped only when it says separate.

- **Uninstall every self-start object with zero residue** — SECURITY — value 4 — effort M — risk low — category: reversibility
  Why: triggers will create timers, path units, git hooks, webhook listeners and scoped credentials. Leaving Sampo should leave nothing running or armed.
  Done when: a manifest lists each created OS object, `sampo trigger uninstall --all` removes them, and a before/after diff of units, crontab, `.git/hooks` and listening ports on a scratch home is empty.

- **Rebuild the trigger registry from 30 days of behaviour and diff it** — FEATURE — value 3 — effort M — risk low — category: derived-state — wild
  Why: assumption: if the registry can be regenerated from ledgers and the user's own commits, it is derived data and not state worth protecting. A mismatch shows which triggers encode knowledge nothing else holds.
  Done when: a monthly lane produces a rebuilt registry and a diff report, and each registry entry is tagged "reproducible" or "irreplaceable".

- **Run a dead-host day against a fake host with no hooks, events or background list** — CLEAN — value 4 — effort M — risk low — category: host-independence — wild
  Why: the standing rule says Sampo must work with no `claude` on PATH, and the drive's counting leans on host internals.
  Done when: `roundtrip.py` has a variant on a stub host, and the drive still picks a task, runs it, verifies it and records a stop reason, with each guarantee that needed a hook labelled "lost".

- **Hand one night to a rival agent CLI using the same brief files** — PERFORMANCE — value 3 — effort M — risk low — category: benchmark — wild
  Why: briefs are already harness-neutral. Overnight progress under another agent with Sampo only verifying shows how much of the yield comes from the drive and how much from the model.
  Done when: one replayed night runs under Codex or Gemini CLI with the same queue, and the morning card reports tasks closed and false dones for both.

- **Show the trigger registry as a "what only Sampo can do" shortlist** — CLEAN — value 3 — effort S — risk low — category: focus
  Why: the plan sets out many trigger kinds. Tagging each as host-native-possible, forge-native-possible or Sampo-only shows where the moat is before more are built.
  Done when: each trigger kind in the spec carries one of the three tags with a cited alternative, and `sampo doctor` lists the Sampo-only kinds first.

- **Set a hard retirement date on the polling fallbacks** — CLEAN — value 2 — effort S — risk low — category: debt
  Why: assumption: CI and issue watchers will start by polling. Polling outlives the webhook or check-run events that replace it unless a date forces the removal.
  Done when: every poller declares an `expires:` field and `sampo doctor` fails once the date passes without an extension note.

Next question: which unattended-night outcomes would the user keep if every Sampo trigger were turned off tomorrow, and does any ledger record the answer?
Next question: which of Sampo's host workarounds would a single upstream fix delete, and has anyone filed that fix?
