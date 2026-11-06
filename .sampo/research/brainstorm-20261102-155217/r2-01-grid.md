# Brainstorm — lens: grid

Surfaces crossed: web UI, `fm` CLI, session-start and prompt hooks, lanes (other agents), the unattended drive and tick, and the Genesis site as a publish target. Actors are the user, the agent, other agents, and an unattended run. Cell names use surface × actor × failure.

- **Precompute the anticipation card at Stop, read it at SessionStart** — PERFORMANCE — value 3 — effort S — risk low — category: hook latency
  Cell: session hook × user × slow.
  Why: assumption: any predictor that computes at session start adds to the hook path, and the repo already ratchets hook time (`bench_hooks.py`).
  Done when: `bench_hooks.py --runs 20` p95 for SessionStart is unchanged with anticipation on. The hook reads one precomputed file and never opens a ledger.

- **Keep only normalised n-grams and task ids, not raw asks** — SECURITY — value 4 — effort M — risk low — category: privacy
  Cell: predictor store × user × unsafe.
  Why: the "user's own words" section shows asks are stored verbatim. A predictor built on them becomes a second copy of the user's most personal data. Assumption: the predictor needs only kinds and transitions.
  Done when: after the TTL (default 30 days) no raw ask text exists in the predictor's files. A test greps for a planted sentence and finds nothing, and the predictor's hit rate stays within 2 points on a fixture.

- **Put a hit-rate line in `fm doctor` and mute any predictor below its baseline** — FEATURE — value 4 — effort S — risk low — category: measurement
  Cell: CLI × user × unclear.
  Why: the pack has many "predict the next ask" ideas and no way to tell if one works. The pack also lists a deciders-with-no-sample-size row that was dropped as partly built.
  Done when: doctor prints `anticipation: 14/48 hit, recency baseline 11/48, on`. With a planted useless predictor it prints `muted` and surfaces nothing.

- **Bind each prediction to the ledger epoch and HEAD, and drop it when the user's first message contradicts it** — FIX — value 3 — effort S — risk low — category: staleness
  Cell: web UI × agent × wrong.
  Why: assumption: a stale "you'll probably ask X" shown after the user already steered elsewhere is worse than silence, and it trains the user to ignore the shelf.
  Done when: a test moves HEAD, or sends a steer-shaped first message, and the shelf is gone and a miss is booked.

- **Show a predicted-asks shelf in the web UI with evidence and a never button** — FEATURE — value 4 — effort M — risk med — category: anticipation
  Cell: web UI × user × missing.
  Why: assumption: the web UI is the only surface in the pack's surfaces line. The open-work list shows follow-ups (blocked adapters, deferred "Later from" tasks) that nobody surfaces by evidence.
  Done when: on a fixture ledger the shelf lists the known follow-up with the closed task ids behind it. "Never" suppresses that shape for good, and the page works with the predictor muted.

- **Inject a per-model, per-task-kind pre-warning only where that model has failed three or more times** — FEATURE — value 3 — effort M — risk med — category: agent steering
  Cell: prompt hook × agent × wrong.
  Why: `fm outcomes` and lessons already record failures. The anticipation here is of the agent's own error, not the user's ask. Assumption: failures are tagged by model.
  Done when: a fixture with three failures for (model, kind) injects one line on the fourth task of that kind. A kind with fewer than three failures injects nothing, and a plain-versus-warned A/B is recorded.

- **Require a lane to hand back "what the user will ask about this" in two lines** — FEATURE — value 2 — effort S — risk low — category: lanes
  Cell: lane × other agents × unclear.
  Why: assumption: lane hand-backs are summarised for the planner and nothing in the pack predicts the follow-up question the user asks about a merged lane.
  Done when: the lane hand-back schema rejects a result with an empty field. The field is compared with the user's next ask in the scoreboard.

- **Confine speculative overnight work to a branch that expires in 3 days** — SECURITY — value 4 — effort M — risk med — category: unattended safety
  Cell: unattended × user × unsafe.
  Why: assumption: drafts of predicted work spend idle quota. A wrong prediction must never touch main, the queue, or the push grant, and must not pile up.
  Done when: a test runs a speculative job and checks that main, the queue, and `fm next` are unchanged, and that the branch is deleted at day 3 unless adopted.

- **Show the first-minute "Foreman is degraded" card from the same file the anticipation card uses** — FIX — value 3 — effort S — risk low — category: unclear failure
  Cell: session hook × user × unclear.
  Why: the earlier questions ask what the user sees right after a silent fail-open. One precomputed card slot can carry either message.
  Done when: killing a hook import shows a one-line degraded card at the next session start, and a test asserts the slot is never empty on a fail-open.

- **Warn when the state directory or ledger growth will cross a ceiling inside a week** — PERFORMANCE — value 3 — effort S — risk low — category: unattended resilience
  Cell: unattended × user × missing.
  Why: assumption: the drive runs while the user is away and a full disk is the failure nobody sees. The earlier question about suspend, lost network and sleep points the same way.
  Done when: doctor projects days-to-full from the last 14 days of ledger bytes and warns under 7. A shrunk-disk fixture triggers it.

- **Wild: seal tomorrow's three likely asks at day close and show only the hits** — FEATURE — value 3 — effort S — risk low — category: delight
  Cell: web UI × user × unclear. wild
  Why: assumption: a visible miss costs trust and a visible hit earns it. Misses are booked in the scoreboard but never shown.
  Done when: the next-day card appears only when at least one sealed ask matched, and misses count only in doctor.

- **Wild: read a local calendar file to plan unattended work around the user's day** — FEATURE — value 3 — effort M — risk med — category: scheduling, privacy
  Cell: unattended × user × slow. wild
  Why: assumption: an `.ics` file already sits on the user's machine. Heavy runs would finish before the first meeting and the briefing would be ready. Local only, nothing sent anywhere.
  Done when: with a fixture `.ics`, the planner puts the heavy run before the first event. With no file it behaves as today, and a test asserts no network call.

- **Wild: let the predictor retire itself once it stops beating its baseline for 30 days** — CLEAN — value 3 — effort S — risk low — category: lean
  Cell: CLI × agent × wrong. wild
  Why: the standing steers prefer subtraction, and the existing "lean row pending" idea waits on a measurement that this one provides.
  Done when: a fixture with a 30-day losing streak removes the predictor's injection. The removal is recorded as a decision with the numbers, and doctor shows `retired`.

- **Wild: keep a trust-the-prediction dial the user can see and set** — FEATURE — value 2 — effort S — risk low — category: user control
  Cell: web UI × user × unsafe. wild
  Why: assumption: some users want anticipation off entirely, and "simplify" may mean fewer decisions asked of them.
  Done when: off, shelf-only, and shelf-plus-overnight are three states. The drive and hooks honour the state, and a test flips each.

Cells left empty:
- Desktop tray × any actor: blocked on T-0325, so there is nothing to build until the dependency lands.
- Genesis site × agent: it is a publish target, not an interactive surface.
- Lanes × other agents × unsafe: the capability-token and allowlist ideas already cover it.
- Unattended × other agents × wrong: the jury and reputation ideas cover it.

Next question: which of the predicted asks in the shelf would the user have typed within a day anyway, and which would they only have thought of because the shelf showed them?
Next question: does the user's own history contain enough repeated ask shapes for any predictor to beat "do the next open item" at all?
