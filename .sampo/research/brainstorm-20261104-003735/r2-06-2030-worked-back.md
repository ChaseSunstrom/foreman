# Brainstorm — lens: 2030 worked back

- **Add `sampo emit` as a local event spool** — FEATURE — value 4 — effort S — risk low — category: triggers
  Why: assumption: by 2030 most event sources (git hooks, make, editors, phone shortcuts, other agents) can't speak webhooks but can all drop a file or call a CLI. Today's ideas cover watchers (inotify, CI, issues) but not a push door.
  Done when: `sampo emit build.red --json '{...}'` from a shell script starts the matching trigger, and the ledger row names the emitter.

- **Mint a scoped credential per triggered run** — SECURITY — value 5 — effort M — risk med — category: unattended security
  Why: the pack fences trigger text as data and caps the outward-action envelope, but nothing shows what credentials an unattended run holds. Assumption: it inherits the user's ambient tokens.
  Done when: a triggered run's environment holds only a short-lived token for its declared envelope, and a planted `git push` to another repo is refused.

- **Write `sampo unwind --since <time>`** — FEATURE — value 5 — effort M — risk med — category: user value
  Why: the user wants overnight progress unattended, but the pack has no cheap way to take a bad night back. Assumption: waking to twelve branches, three PRs and a comment is the fear that stops people granting the overnight yes.
  Done when: after a scratch night of triggered runs, one command closes the PRs, deletes the branches and reverts local commits made by triggered runs, and prints what it skipped as unsafe.

- **Attach a signed provenance attestation to every unattended PR or commit** — SECURITY — value 4 — effort M — risk low — category: provenance
  Why: assumption: by 2030 maintainers will only take agent-authored changes carrying proof of the rules, model and gates behind them. Sampo already holds the ledgers that supply it.
  Done when: a triggered PR body carries an attestation (trigger id, wake reason, model digest, gate results, Ward version) that `sampo verify-attest` checks offline.

- **Store trigger event payloads as hash plus redacted excerpt with a TTL** — SECURITY — value 4 — effort S — risk low — category: privacy
  Why: issue and CI text come from third parties and may hold personal data or secrets. A "why did this start?" ledger would otherwise keep them verbatim, and the Genesis site publishes ledger-derived data.
  Done when: the ledger keeps only a payload hash and a 200-character redacted excerpt, expiring after N days, and a planted fake API key in an issue body never reaches disk.

- **Push events into a live session, not only spawn new ones** — FEATURE — value 4 — effort M — risk med — category: devices/agents
  Why: assumption: with a session already working in the repo, a CI-red event is better steered into it than raced by a second worker. The pack's triggers all start fresh work, and the drive already knows which sessions are running.
  Done when: a CI-red event arriving while a session works the same branch is delivered to it as fenced data, with no second lane started.

- **Make trigger fixtures: `sampo trigger test` with golden event→decision files** — FEATURE — value 3 — effort S — risk low — category: developer experience
  Why: the pack proposes replaying history, but nothing lets a trigger set be code-reviewed and tested in CI. A fixture of event in, fire/skip/reason out catches a bad edit before the night.
  Done when: editing a trigger so a golden fixture flips decision fails `sampo trigger test`.

- **Climb an autonomy ladder per trigger: observe, draft, branch, push** — SECURITY — value 4 — effort M — risk low — category: unattended trust
  Why: the pack mentions a read-only first lane for CI-red, but not a general earned promotion. The user's 0→0.1 drive stops and a 50% rise in failed tool calls say unattended trust must be earned per trigger.
  Done when: a new trigger can only observe, and promotion to the next rung needs N accepted outputs plus one explicit key.

- **List orphaned triggers by owner** — CLEAN — value 2 — effort S — risk low — category: teams
  Why: assumption: by 2030 Sampo runs in shared repos, and triggers outlive the person who made them. Today a trigger has no owner field.
  Done when: every trigger records its author, and `sampo doctor` flags those whose author no longer has repo access or whose grants have lapsed.

- **Wild: Accept signed requests from other people's agents into a quarantined inbox** — FEATURE — value 4 — effort L — risk high — category: agents
  Why: wild; assumption: a teammate's or a vendor's agent will want to ask yours to act. A signed, data-only inbox with the lowest grant tier turns that into a trigger source without opening a command channel.
  Done when: a signed message becomes a dormant brief only a human can promote, and an unsigned or injected one is dropped with a logged reason.

- **Wild: Read the morning card aloud on a car or watch surface** — FEATURE — value 3 — effort M — risk low — category: devices
  Why: wild; the pack has a morning card, a phone digest and a tray but no voice. Local text-to-speech keeps it on the owner's hardware.
  Done when: `sampo morning --speak` reads the done, waiting and unsure sections in under 45 seconds using a local voice, with no network call.

- **Wild: Run heavy local-model volume when power is cheap or solar surplus is high** — PERFORMANCE — value 3 — effort M — risk low — category: local models
  Why: wild; the user wants local models used "without limit" for background volume. A 27B model running all night has a real power bill, and by 2030 tariffs may vary by the hour. Assumption: the user's utility or inverter exposes a price or surplus signal.
  Done when: with a price source configured, queued local batches wait for a cheap window unless marked urgent, and the morning card reports kWh and cost.

- **Wild: Draw triggers as a constellation on the astrolabe** — FEATURE — value 3 — effort M — risk low — category: ui
  Why: wild; the look is Kirjokansi, with a turning sky and heat as "running now". Each trigger becomes a star: brightness is recent accepted yield, a dim star is one nobody takes, and a flare shows a fire in progress.
  Done when: the web UI shows every trigger as a star, a muted or lease-expired one renders dim and hatched, and reduced-motion users get a static chart.

- **Expire each trigger's authority on a lease, renewed with one key** — SECURITY — value 4 — effort S — risk low — category: consent
  Why: queued installs and overnight grants are one-yes events, and nothing says a yes decays. Assumption: a yes given in November shouldn't still authorize the same writes in March.
  Done when: a trigger past its lease fires only in observe mode, and the morning card offers a one-key renewal listing what was done under it.

Next question: What does the user already do by hand every day that a trigger would replace, and which of those can't be observed from the repo or ledgers?
Next question: Which of the 2030 sources (other agents, host routines, phone shortcuts) will arrive before Sampo has a stable event schema to receive them, and who owns versioning it?
