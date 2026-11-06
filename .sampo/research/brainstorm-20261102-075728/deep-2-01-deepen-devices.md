# Brainstorm — lens: deepen: devices

- **Publish one goal-state file every surface reads** — FEATURE — value 5 — effort M — risk low — category: devices
  Why: the existing list (MCP resource, `--plain`, waybar line, todo.txt mirror, phone page) all re-derive goal status separately; assumption: one versioned `goal-state.json` (done-when checks, current row, lease holder, last proof, "done vs stopped" verdict) written atomically on each task change, with every surface a thin renderer.
  Done when: deleting the file and running `fm goal status` regenerates it, and the plain, bar, MCP and web renderers all print the same done/stopped verdict from it in one test.

- **Fold the surfaces into a single `fm goal glance` verb with named profiles** — FEATURE — value 4 — effort S — risk low — category: terminal
  Why: `--plain` at 40 columns, the status-bar line and the tmux line are three outputs of one need; assumption: profiles `plain`, `bar`, `watch`, `json` share one truncation and priority order (verdict, current step, next blocker).
  Done when: each profile's output fits its width limit on a 200-row goal and keeps the verdict first.

- **Make the phone page act through a signed one-shot "answer" link** — FEATURE — value 5 — effort M — risk med — category: phone
  Why: the pack's `fm ask` is blocked on Codex, Gemini and opencode, and the user steers "never block on the user"; assumption: when a row is parked on a question, the phone page shows the question with the choices, and a tap posts an expiring, single-use signed answer that `fm ask` consumes.
  Done when: tapping a choice on a paired phone resolves a parked `fm ask` once, and replaying the link is refused.

- **Push only the "stopped vs done" transitions to the phone** — FEATURE — value 4 — effort M — risk low — category: notifications
  Why: the request says it must know "when it's actually done rather than merely stopped"; assumption: a self-hosted ntfy or Web Push sends at most three event kinds (done with proof, stopped needing you, stalled over N hours) and nothing else.
  Done when: a fake-clock week produces only those kinds, and a mute setting suppresses them all.

- **Queue phone-side edits and merge them on reconnect** — FEATURE — value 4 — effort M — risk med — category: offline
  Why: the offline-run and sync-folder ideas imply edits made away from the desk; assumption: reorder, defer, and "not this" taps are stored as an append-only op log on the phone page and replayed with conflict notes.
  Done when: two edits made offline, one conflicting with a desk change, merge on reconnect and the conflict is shown rather than dropped.

- **Give the sync-folder mirror a write-back inbox** — FEATURE — value 3 — effort S — risk med — category: sync
  Why: the todo.txt mirror is read-only today; assumption: a line added or ticked in the mirror (from any todo app) becomes an intake capture or a user-marked done request, and ticking never closes a task without its proof.
  Done when: appending a line to the mirror file creates an intake item, and ticking a row only queues a proof run.

- **Offer a car and voice read-out of the goal** — FEATURE — value 3 — effort S — risk low — category: voice
  Why: assumption: the goal plan carries days; a spoken 20-second brief ("two of nine rows left, blocked on one question of yours") works for a car or speaker through a local TTS, and a spoken answer maps to the ask above.
  Done when: `fm goal say` produces a text of at most 60 words that a local TTS can play, and the answer path accepts "yes" or "no" for a pending question.

- **Add a device-trust ledger to `fm doctor`** — SECURITY — value 4 — effort S — risk low — category: trust
  Why: pairing, tokens, mTLS pins and QR links are many new doors, and the pack's open question asks which gauges the user cannot falsify; assumption: a list of every paired device, scope, expiry and last use, with one command to revoke all.
  Done when: `fm doctor` lists each device and `fm devices revoke --all` makes every earlier token fail.

- **Wild: Make the goal a lock-screen live tile that shows the finish line** — FEATURE — value 3 — effort L — risk med — category: delight
  Why: wild; assumption: a progress ring whose segments are done-when checks, which fills only on a really-run proof, so a stopped goal never looks finished.
  Done when: a ring segment turns solid only after its check has a recorded passing run.

- **Wild: Let a spare e-ink or old tablet be a "goal board"** — FEATURE — value 3 — effort M — risk low — category: ambient
  Why: wild; assumption: a no-JavaScript page refreshing every minute on any old device by the desk, large type: verdict, current row, who is working, what needs you. Burn-in safe, no login except the read-only token.
  Done when: the page renders in a text browser and exceeds 24pt on the verdict at a tablet width.

- **Wild: Hand the goal over by NFC tag or QR to another machine** — FEATURE — value 3 — effort M — risk med — category: handoff
  Why: wild; assumption: a tap or scan carries a one-time pointer to a goal bundle (plan, steers, last proof) so a laptop, a CI box or a second harness resumes where the first stopped, using the lease so only one holds it.
  Done when: a second machine resumes from the bundle, takes the lease, and the first machine's writes are refused.

- **Settle a device-sourced fact against something outside Foreman** — FIX — value 4 — effort M — risk low — category: calibration
  Why: the pack asks which outputs are only graded by Foreman itself; assumption: a "phone saw it" receipt records whether the user opened, ignored or answered each notification, feeding the trigger-kind false-alarm weighting.
  Done when: `fm outcomes` shows per-trigger open, answer and ignore rates from device receipts.

- **Add a "same day, different clock" check between devices** — FIX — value 2 — effort S — risk low — category: sync
  Why: the pack asks which clock to trust when the fake-clock week and the real timer disagree; assumption: each device page shows the server time and its own skew, and a warning appears when expiry or lease times differ by minutes.
  Done when: a phone with a clock set 10 minutes off shows a skew warning and doesn't accept a token as unexpired.

Next question: Which of these surfaces would the user actually open in a week of real use, and what record of past opening (not Foreman's own guess) could decide that before building any?
Next question: When two devices act on the same goal row at once (a desk lease and a phone tap), which wins, and where is the loser told?
