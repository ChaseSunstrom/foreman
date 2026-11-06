# Brainstorm — lens: bold bets

- **Rank forecasts by regret, not likelihood** — FEATURE — value 4 — effort M — risk low — category: anticipation
  Why: assumption: a likelihood-ranked forecast mostly predicts routine asks the user would type anyway. The ones worth pre-empting are the asks whose absence costs most, such as a missed proof, a red CI, or a stall. The pack's "Score a recency baseline first" idea measures hit rate only.
  Done when: `fm forecast --explain` shows p(ask) × cost-if-late per candidate, and a backtest on the last 30 days shows the regret-ranked top 3 covers more user-minutes than the likelihood-ranked top 3.

- **Replace guard regexes with a linear-time matcher** — PERFORMANCE — value 4 — effort L — risk med — category: guard speed
  Why: T-2668 times `fmguard.check` on pathological input, and the pack has a planted quadratic pattern. A bar catches a slow case after the fact. A DFA or RE2-style engine makes it impossible by construction.
  Done when: a 50k-character adversarial corpus runs in time linear in input size (a 10× input takes at most 12× the time), and the existing guard exam gives identical verdicts.

- **Build outbound packs from a field allowlist** — SECURITY — value 5 — effort M — risk med — category: privacy
  Why: the pack builder scrubs by denylist, and user asks are captured verbatim, so a pasted secret or path can reach a remote child. An allowlist schema says which fields may leave and nothing else does.
  Done when: a planted canary string in an ask, a steer and a task body never appears in any captured child prompt, and adding an undeclared pack section fails a test.

- **Test the forecaster for memorising secrets** — SECURITY — value 4 — effort S — risk low — category: privacy
  Why: anticipation trains on the verbatim asks ledger. A forecast that suggests "your next ask: …AKIA…" is a leak. Assumption: no scrub sits between the ledger and the predictor today.
  Done when: a test seeds a fake secret into a past ask, trains the predictor, and asserts the secret and its n-grams never appear in any forecast, log or cache file.

- **Precompute forecasts in the tick and read a file at session start** — PERFORMANCE — value 4 — effort S — risk low — category: session start
  Why: session-start injection is on the hot path, and the pack's own tasks ratchet start-up time. Anticipation must not add to it.
  Done when: session start adds at most 5 ms with the forecast on versus off (`bench_hooks.py`), and a missing or stale forecast file degrades silently to no forecast.

- **Transfer habit predictions across the user's repos** — FEATURE — value 3 — effort M — risk med — category: anticipation
  Why: assumption: habits such as "after adding a flag, ask for docs and a test" follow the user, not the repo, and per-repo ledgers are too thin to learn them. The user has many repos.
  Done when: a new repo with under 20 tasks gets a forecast whose backtest hit rate beats an empty one, and each suggestion names its source repo.

- **Hold out anticipation to measure induced demand** — FEATURE — value 3 — effort M — risk low — category: measurement
  Why: assumption: showing predicted asks may make the user stop steering, so the forecast shapes the asks it later scores as hits. A random 1-in-10 sessions with the forecast hidden gives a control.
  Done when: `fm forecast stats` reports ask volume, steer count and hit rate for the shown and hidden arms with their sample sizes.

- **Mine editable event→ask rules** — FEATURE — value 4 — effort M — risk med — category: anticipation
  Why: the pack proposes external triggers, but as a pile of separate ideas. A rule table (CI red on main → fix ask within 1 hour, support 7 of 9) can be read, edited and vetoed by the user, which a model can't.
  Done when: `fm forecast rules` lists mined rules with support and confidence, and a vetoed rule is never fired again.

- **Pick unattended windows from power and idle state** — FEATURE — value 3 — effort S — risk low — category: scheduling
  Why: the open questions ask what happens when the machine sleeps, suspends or loses network. Reading AC/battery, idle time and lid state (logind/upower) lets heavy runs start only when they can finish.
  Done when: with AC unplugged in a faked-power test, `fm run` defers, names "on battery" in its receipt, and resumes when AC returns.

- **Sync forecast tables, never ledgers, between the user's machines** — SECURITY — value 3 — effort M — risk med — category: privacy
  Why: assumption: the user has several machines (the pack asks which tasks need them). Counts derived from the ledger carry less than the ledger does. The ledger stays local.
  Done when: a synced table file contains only aggregate counts, a test shows no ask text in it, and the second machine's forecast improves in backtest.

- **Show an honest "I can't read you this week" state** — FEATURE — value 3 — effort S — risk low — category: calibration (wild)
  Why: the pack's drops show deciders that abstain almost always or never. A forecast should withhold itself when the next-ask distribution is flat, and say so with the entropy figure.
  Done when: below a stated confidence floor `fm forecast` prints one abstain line with the entropy, and the abstain rate appears in `fm doctor`.

- **Suggest the next ask as ghost text on the prompt line** — FEATURE — value 4 — effort M — risk med — category: delight (wild)
  Why: the foreman-ui mod already owns the prompt area. Fish-style grey autosuggestion accepted with Tab turns a forecast into one keystroke without sending anything.
  Done when: with a seeded forecast the prompt shows dim text, Tab fills the input without submitting, and Esc dismisses it for the session.

- **Read a local calendar file to switch to lean mode in crunch weeks** — FEATURE — value 2 — effort M — risk med — category: privacy-safe context (wild)
  Why: assumption: an optional local `.ics` the user points at tells Foreman when they're away or slammed. The file is read locally, the parse is never sent anywhere, and by default no file is read.
  Done when: with a configured `.ics` and an away block, the "while you were away" and queue settings change, and with no config nothing reads any calendar.

- **Show a forecast only when two independent predictors agree** — FEATURE — value 3 — effort M — risk low — category: anticipation quality
  Why: the pack proposes an n-gram predictor and a tool-less child separately. Gating display on agreement trades coverage for precision, which suits a feature that mustn't nag.
  Done when: a backtest shows precision of agreed forecasts above either predictor alone, with coverage reported beside it.

Next question: which of the user's repeated asks were already foreseeable from the ledger at the moment they first appeared, and which came from outside it?
Next question: what does the user do in the 60 seconds after seeing a wrong forecast, and is that moment ever measured?
