# Brainstorm — lens: unspoken needs

- **Make triggers obey the standing steers** — FIX — value 5 — effort M — risk med — category: safety
  Why: The steers say `--round-first` holds Foreman-filed items (ci, self, discovered) and `--pace off` waits out limits. A trigger that files tasks is the easiest way to get around both without anyone noticing. Assumption: trigger-filed items skip the drive's hold check today.
  Done when: with `--round-first` on, a fake CI-red event files a capture marked "held by round-first" and `fm next` doesn't offer it. A test covers this.

- **Fire on state, not only on clocks** — FEATURE — value 5 — effort M — risk med — category: triggers
  Why: The user defers the full exam to "once Missions 1-8 are built" and holds T-2450, T-2444, T-2428 and T-2441 until "round 1 is done". Those are conditions, not times, and today a session has to notice them. Assumption: the tick only knows time, files and CI.
  Done when: a row `when open_missions==0 → fm exam run --final` fires exactly once on the tick after the last Mission closes, and a repeat tick adds nothing.

- **Turn a new steer into a trigger veto** — FEATURE — value 4 — effort M — risk low — category: steers
  Why: Every steer already becomes a standing rule with a check, but nothing links "stop doing X" to the triggers that do X. A trigger then keeps firing against what the user said. Assumption: nothing links steers to triggers today.
  Done when: recording a steer "no new maintenance tasks until round 1 ends" puts every matching trigger in shadow mode, and `fm triggers` names the steer that did it.

- **Let one yes cover a class of installs** — FEATURE — value 4 — effort M — risk med — category: installs
  Why: The user gave a durable push grant ("feel free to push to main at any time") and doesn't want to answer the same question twice. Mission 4 queues installs "for one yes". Assumption: each timer or unit needs a separate yes today.
  Done when: after one yes on "user-level fm timers under `~/.config/systemd/user`", a second timer of that class installs with a logged receipt and no prompt, and a system-level unit still queues.

- **Arm the CI watch from `fm ship` itself** — FEATURE — value 4 — effort S — risk low — category: ci
  Why: T-2527 added `fm ci-watch --last-ship` and the ship bets settled "11 held in a row", so the user already runs the watch by hand after each ship. Assumption: nobody wired the arm step into `fm ship`.
  Done when: `fm ship` leaves a pending watch row, the tick settles it without a session, and a ship that is never watched fails a test.

- **Keep watcher payloads on local models for sensitive repos** — SECURITY — value 4 — effort M — risk med — category: privacy
  Why: The four model rules in the asked list say sensitive repos resolve local backends only. Issue and CI text is the new untrusted input that reaches a model with no session open. Assumption: the watcher design doesn't mention this yet.
  Done when: a watcher on a repo marked sensitive with no local backend files the raw capture with no model call. A test asserts zero outbound model calls.

- **Check watcher credentials are read-only** — SECURITY — value 3 — effort S — risk low — category: credentials
  Why: Issue and CI watchers need a GitHub token, and an unattended lane holding a write-scoped token is the worst case. Assumption: the token comes from `gh auth` and its scopes are never inspected.
  Done when: `fm doctor` names the token's scopes per watcher and goes red if a watcher has push or admin scope.

- **Budget the idle tick** — PERFORMANCE — value 3 — effort S — risk low — category: tick
  Why: The night tick "logs only when something happens", which also hides what an empty tick costs. Hook p95 already has a ratchet and the tick has none. Assumption: no idle-tick measurement exists.
  Done when: `fm doctor` prints the idle tick's median wall time and tokens (zero), and CI fails if the idle tick spends tokens or exceeds the stated budget.

- **Generate the trigger docs from the registry** — FEATURE — value 3 — effort S — risk low — category: docs
  Why: Docs are listed as thin, and the proof-before-presentation steer says public claims must match a producing command. Hand-written trigger prose will drift. Assumption: no trigger page exists yet.
  Done when: MASTER and the site's trigger section are built from the trigger table, and a test fails when a documented trigger isn't installed or an installed one isn't documented.

- **Spawn the blind-spot question from each missed ask** — FEATURE — value 4 — effort M — risk low — category: learning
  Why: The pack's "what earlier brainstorms missed" list is built by hand from the user's asks, and T-2504 and T-2505 are in it. A watcher on the asked stream could do that step. Assumption: no automatic loop from a missed ask to the next brainstorm exists.
  Done when: an ask that matches no earlier idea files a "question a brainstorm should have asked" capture within one tick, grouped with its siblings.

- **Run heavy exams in the idle window (wild)** — FEATURE — value 3 — effort M — risk med — category: scheduling
  Why: The user paused long-horizon runs and wants them only at the end or for a regressing capability, and runs cost real time and quota. Assumption: the end-of-run exam is started manually.
  Done when: the exam starts only when the machine is idle and plugged in, pauses when the user returns, and resumes from its checkpoint.

- **Have a blind child write the triggers it would want (wild)** — FEATURE — value 3 — effort M — risk low — category: blind spots
  Why: The steers want weakness-finding from signals Foreman didn't author. Assumption: a tool-less child reading only the user's steers and asked stream would propose triggers the design misses.
  Done when: each generation, a child's proposed trigger list is diffed against the real table and the unmatched ones are filed as captures.

- **Rehearse one chaos night before the first install (wild)** — FEATURE — value 3 — effort L — risk med — category: reliability
  Why: Mission 3 found that three of five briefs were built or had no failure behind them, so the user distrusts untested paths. Assumption: no rehearsal of a full unattended night exists before the user's yes.
  Done when: the yes card shows a replayed night with a duplicate event, a clock jump and a killed lane, plus the table of what each did.

Next question: Which of the 59 cells would a trigger fire on a surface the user has never opened, and what would show that it fired?
Next question: What does the user do the first morning after an unattended night, and is the first thing they see the thing they need?
