# Brainstorm — lens: grid

- **Add `sampo wake` so a session can schedule its own continuation** — FEATURE — value 5 — effort M — risk med — category: self-triggering
  Cell: CLI × agent × missing. Why: the pack lists schedules, file, CI and issue triggers, all set up by the user. An agent waiting on a 40-minute build or a usage-limit reset can only hold the drive, which is the "drive stops" gap. The verb would be `sampo wake --when "ci green on branch X" --in 25m --note "..."`. The brief it files is capped by depth, budget and TTL, and it fires through the same trigger intake as the rest.
  Done when: a session calls the verb and exits; the condition fires and a new session resumes with the note. A test shows a wake that files another wake stops at the depth cap.

- **Attach to a running unattended lane and take over** — FEATURE — value 4 — effort M — risk med — category: observability
  Cell: Smith TUI and pane × user × missing. Why: overnight work is invisible while it runs and the user can only kill it or wait. `sampo attach LANE` would give a read-only tail of the lane's events with a takeover key. Takeover pauses the lane at a tool boundary and hands over its checkpoint, so the user continues in the same worktree.
  Done when: attach shows live events; takeover leaves the lane paused with a valid lease released, and `sampo resume` returns control.

- **Dry-run every queued install in a throwaway prefix before asking for the yes** — SECURITY — value 4 — effort M — risk low — category: installs
  Cell: CLI × user × wrong. Why: the request says installs are "queued for one yes", but a yes on an untested install is a guess. The install runs in a temp prefix, the repo's gates run against it, and the card shows pass or fail with the manifest hash.
  Done when: a queued install's card carries a "tested in scratch: pass/fail" line; a failing install is shown but is not offered a one-key yes.

- **Gate local-model grant tiers on a measured injection-resistance score** — SECURITY — value 5 — effort M — risk med — category: unattended safety
  Cell: unattended × local models × unsafe. Why: the user wants unlimited local models for background volume, and weaker models are easier to steer from issue or CI text. A bench of planted-injection scenarios scores each profile, and the score sets the highest grant tier its trigger-born runs may get. A model below the bar can read and draft only.
  Done when: `sampo louhi models` prints an injection score per profile, and a trigger run on a sub-threshold model cannot reach a write grant (test).

- **Give every event an idempotency key that survives restarts and redelivery** — FIX — value 4 — effort S — risk low — category: trigger intake
  Cell: web UI and CLI intake × unattended × wrong. Why: assumption: webhooks and file watchers redeliver after a drive restart or resume (T-2900 was a resume bug). The key is source + id + content hash, stored in a small seen-set with a TTL, and a duplicate logs "skipped: seen".
  Done when: replaying the same CI-red event twice, across a drive restart, files one task.

- **Tier trigger-born transcripts to digest plus failures** — PERFORMANCE — value 3 — effort M — risk low — category: state size
  Cell: unattended × hooks × slow. Why: the pack's 2.4 GB state is unexplained, and unlimited local volume will multiply it. After close, a night run keeps a digest, its failed tool calls and its receipts, and the full transcript goes to a TTL tier.
  Done when: a synthetic 50-run night adds under a stated byte budget, and the failed calls are still searchable.

- **Sample local-routed trigger decisions against a frontier second opinion** — FEATURE — value 4 — effort M — risk low — category: routing quality
  Cell: unattended × decision models × wrong. Why: failed tool calls up by half suggests some routing is wrong, and nothing here grades it. About 5% of triage and routing calls are re-asked of a stronger model at idle, and the disagreement rate is kept per profile and per task kind. A profile whose rate is high gets demoted to draft-only.
  Done when: a ledger shows disagreement per profile, and a planted bad router is demoted within N samples.

- **Stamp one state-snapshot id on every surface** — FIX — value 3 — effort S — risk low — category: consistency
  Cell: web UI, pane, status line × user × unclear. Why: assumption: the pack lists several surfaces that read the drive and trigger state separately. If the pane says "waiting" and the web UI says "idle", the user can't tell which is right. Each render shows a short snapshot id and its age, and a mismatch beyond a threshold is flagged.
  Done when: the pane and web UI show the same id for the same moment, and a deliberately stale surface shows "stale Ns".

- **Give each trigger a home machine with a lease** — FEATURE — value 3 — effort M — risk med — category: multi-machine
  Cell: unattended × other machines × wrong. Why: assumption: the pack's local-model hosts (jarvis and others) suggest more than one machine, and synced state could fire a schedule twice. The registry names one home, the lease is renewed by heartbeat, and a failover is logged.
  Done when: two simulated machines sharing the registry fire a 02:00 schedule exactly once; a killed home hands over within the lease TTL.

- **Burn a night error budget that freezes trigger changes** — FEATURE — value 4 — effort S — risk low — category: reliability
  Cell: unattended × drive × unclear. Why: drive stops went from 0 to 0.1 and failed calls are up half, which is a trend with no gate. Drive stops and failed calls per night-hour count against an SLO. When it is burned, new or edited triggers queue as drafts and only fixes land.
  Done when: forcing the budget over the line blocks `trigger add` with the reason and the burn figure.

- **Wild: Yes-preview, a simulated night with the install applied** — FEATURE — value 4 — effort L — risk med — category: installs
  Cell: user × installs × unclear. Why: a yes is hard to undo and the user never sees what it unlocks. A clone gets the install, the queued work is replayed there, and the card shows which tasks would newly pass.
  Done when: the card lists "N tasks newly runnable if yes" from a real clone run.

- **Wild: Stigmergy notes, decaying marks on files for the next triggered run** — FEATURE — value 3 — effort M — risk low — category: agent memory
  Cell: other agents × lanes × missing. Why: assumption: night lanes forget what the previous run learned about a file. A run leaves a short note keyed by path ("flaky under -j8"). Notes decay, are read by the next run that touches that file, and are fenced as data.
  Done when: a second run that touches the file sees the note; an expired note is gone.

- **Wild: Trigger-predict quiz** — FEATURE — value 2 — effort S — risk low — category: legibility
  Cell: user × trigger list × unclear. Why: a tool-less child reads only the trigger file and predicts what fires tomorrow; the user sees the diff against the real dry run. A mismatch means the trigger names or descriptions are unclear.
  Done when: the quiz scores a fixture trigger set, and a deliberately ambiguous trigger scores low.

Cells left empty:
- Site × unattended: the site is static, so no trigger risk lands there.
- Smith TUI × other agents: no evidence that other agents drive Smith.
- Most "unsafe" cells for the web UI: the pack's earlier ideas already cover same-origin and diff-shown edits.

Next question: when the local model endpoint is busy or mid-swap, which triggers fall back to doing nothing, and does the morning card say so?
Next question: which of the failed tool calls come from triggered sessions rather than interactive ones, and does the data separate them?
