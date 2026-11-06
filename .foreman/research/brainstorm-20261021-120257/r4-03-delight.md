# Brainstorm — lens: delight

- **Show the upstream as a "new arrivals" shelf** — FEATURE — value 4 — effort M — risk low — category: home screen
  Why: the user wants the six anthropics repos integrated "automatically", but the pack's ideas stay at the lockfile and registry level. Nothing makes that integration something they see. A shelf on the `fm code` home screen would show this week's new skills, renamed plugins and CHANGELOG items, each with a licence glyph and a one-key "try on this run only".
  Done when: after a pinned-repo sync, the home screen golden frame lists the new entries with glyphs, and `r` on one starts a run with it loaded for that run only.

- **Close every run with a "what you can say to a friend" line** — FEATURE — value 4 — effort S — risk low — category: close-out
  Why: the user's requests keep returning to wanting a polished experience ("better animations/looks", "10x better"), while the existing close-out ideas are mostly receipts and ledgers. A single plain sentence at close, written from the diff and the proof, gives them something to repeat or paste. It is also a cheap test of whether the run was understood.
  Done when: a finished run's last frame and its `--json` event both carry one sentence of at most 140 characters, with no task ids or jargon (a lint over a word list checks this).

- **Fire a "first sign of life" within 10 seconds, with a named wait** — FEATURE — value 5 — effort S — risk low — category: liveness
  Why: the user's own words are "it just isn't doing anything", and T-1336 and T-1354 only partly cover it. The delight is the first ten seconds feeling alive: a line like "claude is loading 15k tokens of context, 4s" that counts up and is replaced by real tool events as they arrive.
  Done when: a fake runner that stays silent for 15 seconds still gets a visible, changing wait line within 10 seconds, and the frame test asserts the line is present.

- **Remember half-typed requests in a draft shelf** — FEATURE — value 3 — effort S — risk low — category: request box
  Why: assumption: the user types long, multi-part requests, and the TUI now takes over the whole terminal. Losing a half-written request on Ctrl-C or a crash is a small hurt, and restoring it is a small joy.
  Done when: quitting with text in the request box and relaunching shows that text restored, and `Esc Esc` clears it.

- **Play a cookbook pattern as a named diagram of the run** — FEATURE — value 3 — effort M — risk low — category: motion
  Why: the cookbook patterns (evaluator-optimizer, orchestrator-workers) are in the pack as integration targets, but a user can't tell which one a run is following. A small live diagram with the active node lit makes the harness legible and gives users a screen worth showing others.
  Done when: a run that the planner labels `evaluator-optimizer` draws that two-node loop in the run view, with the active node highlighted in the golden frames.

- **Offer one weekly "adopt this?" decision card** — FEATURE — value 4 — effort M — risk low — category: upstream
  Why: automatic integration of six repos could pile up, and the pack lists many "Later from T-…" tasks that already show an unreviewed backlog. A single card per week, with a name, what it does, its licence class and a replay of a trial run, makes adoption a decision the user wants to make rather than a queue they must triage.
  Done when: after a sync with five new items, exactly one card is queued, and its keys (adopt, skip, later) update the adoption register.

- **Add `fm code why` as a one-screen answer, then make it the stall card** — FEATURE — value 5 — effort M — risk low — category: liveness
  Why: the user asked for `fm code` to explain "why isn't it doing anything", and T-1336 names a cause only after 120 seconds. One screen showing what the runner is waiting on, its startup tax, the last event time and a suggested next key lets a stall become a guided moment instead of a mystery.
  Done when: against a fake runner stalled on a permission prompt, the card names the prompt and offers a key to hand the run to a live CLI.

- **Add an intermission screen on rate limits** — FEATURE — value 3 — effort S — risk low — category: motion
  Why: the stall causes already include a rate limit. A deliberate calm screen with a countdown to reset, the other runners available, and a one-key switch turns a dead end into a pause.
  Done when: a fake runner emitting a rate-limit event shows the countdown screen, and switching runner continues the same task.

- **Show an ETA by analogy** — FEATURE — value 3 — effort M — risk low — category: planning
  Why: assumption: the run journal and past runs exist in `$FOREMAN_HOME`. "About like T-1330, which took 14 minutes and $0.40" beats a generic estimate, and it also quietly feeds the Claude Code vs. Foreman cost story the user cares about.
  Done when: with three past runs stored, a new plan shows the nearest one by kind and size, and a test asserts the analogy is chosen by overlap of files and request kind.

- **Wild: hatch a draft skill from a repeated habit** — FEATURE — value 4 — effort L — risk med — category: skills — wild
  Why: assumption: the user repeats similar requests, as in "Release 1.2.43/44/45…". After the third near-identical request, Foreman offers a drafted SKILL.md that already passes the Agent Skills spec lint, with the user's own wording as its description. This turns the skills repo from something Foreman consumes into something the user produces.
  Done when: three similar release requests lead to a draft in a staging folder that passes the lint and is never activated without a yes.

- **Wild: swap cookbook patterns mid-run like cartridges** — FEATURE — value 3 — effort L — risk med — category: orchestration — wild
  Why: assumption: the harness can restart from a journaled step. A key on a stuck run switches the loop shape (single pass, evaluator-optimizer, orchestrator-workers) while keeping the plan, so the user experiments with strategies, not just models.
  Done when: pressing the swap key during a run re-enters from the last journaled step under the new pattern, and the event log records both patterns.

- **Wild: a "gift task" after Foreman's own mistakes** — FEATURE — value 3 — effort M — risk low — category: trust — wild
  Why: the user has pushed back repeatedly on Foreman misreading them (the "don't stop" veto bug). When Foreman gets something wrong, it queues a small, proven, unrequested fix or nicety in a side branch for one-key accept, so a mistake is followed by something good rather than only an apology.
  Done when: after a recorded misread, a side-branch task with passing proof is shown on the next home screen and discarding it leaves the main tree unchanged.

- **Unlock themes from real milestones** — FEATURE — value 2 — effort S — risk low — category: motion
  Why: the user asked for "better animations/looks/not just static colors". Themes that are earned (first proved task, the 50th, the first overnight queue) give looks a reason to exist and make the TUI worth showing off.
  Done when: a fresh install lists one theme, a counter file at 1 proved task unlocks the second, and the frame test shows the picker with locked entries dimmed.

- **Wild: print a trailer in an empty project** — FEATURE — value 2 — effort S — risk low — category: first run — wild
  Why: the user wanted better website examples and "anything" to be possible. Running `fm code` in an empty folder plays a 20-second scripted run on a fixture. That shows what happens and doubles as the no-model smoke test.
  Done when: in an empty directory the app plays the scripted run with no network and no model, and exits zero.
