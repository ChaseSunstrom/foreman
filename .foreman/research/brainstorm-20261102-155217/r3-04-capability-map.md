# Brainstorm — lens: capability map

- **Arbitrate every anticipation through one slot per surface** — FEATURE — value 4 — effort M — risk low — category: anticipation
  Why: assumption: the earlier slate proposes a session-start card, ghost text, a web shelf, a status line, a file-open whisper and a toast, with no rule for which wins. Without one, each predictor spends the user's attention independently.
  Done when: a test feeds 6 candidate anticipations for one session start and exactly one card prints, chosen by expected value, with the rest listed under `fm anticipate --held`.

- **Record every anticipation as its own ledger class with an outcome** — CLEAN — value 4 — effort M — risk low — category: measurement
  Why: the pack has `fm drill` dropping one record class at a time and a doctor row for deciders with no sample size. Each new predictor would otherwise invent its own storage. A shared `anticipation` record (source, claim, shown, hit, ignored, muted) lets the baseline, mute and hit-rate lines read one place.
  Done when: `fm drill` with the anticipation class deleted makes every reader name the gap and not crash, and `fm doctor` prints one hit-rate row per source.

- **Add conditional reminders: `fm remind when <predicate> "<note>"`** — FEATURE — value 4 — effort M — risk low — category: reminders
  Why: Things, Todoist and Hammerspoon all have conditional reminders. The pack has a promise ledger and a file-open whisper but no way for the user to say "tell me when CI is green on branch X, the PR merges, version Y is released, or this file is touched". Predicates would be a closed list of file, git, CI, date and task-state checks.
  Done when: a reminder with `when task T-1 closed` fires once in the next session start card after T-1 closes, and never again.

- **Detect expected events that did not happen** — FEATURE — value 3 — effort M — risk med — category: anticipation
  Why: assumption: the pack's predictors all key on things that occurred (asks, failures, events). The useful signal is also the missing one: three releases without the usual docs pass, a push with no post-push CI watch, or a Friday with no `fm ship`. Detecting it needs a per-repo expected-sequence table built from the ledger.
  Done when: replaying a ledger fixture with a habitual step removed produces one "usually follows X, not seen" line, and the unmodified fixture produces none.

- **Hold the unattended drive on provider incidents and model sunset dates** — FEATURE — value 3 — effort S — risk low — category: unattended
  Why: the pack covers backoff with jitter and probing that pinned model IDs still answer. It has no external clock for a provider status feed or a published deprecation date. Assumption: a status JSON feed is reachable and an explicit setting allows the fetch.
  Done when: with a fixture status feed reporting an incident, `fm run` pauses with the named reason and resumes when the fixture clears. A fixture sunset date 7 days out adds a doctor warning.

- **Seed predictors with stack-card priors for repos with no history** — FEATURE — value 3 — effort M — risk low — category: cold start
  Why: `cards: python, cc-plugin-release, tailwind…` exist as stack cards. The history-based predictors (n-grams, transition tables) are empty on a new repo, which is where the first-minute impression forms. Priors such as "after a new dependency, expect licence and lockfile asks" would come from the card.
  Done when: in a fresh empty-ledger repo with a Python card, `fm anticipate` prints at least one card-sourced line marked "prior, no history" and never claims a hit rate.

- **Export the anticipation card into AGENTS.md and GEMINI.md** — FEATURE — value 3 — effort S — risk low — category: harness reach
  Why: the standing rule says Foreman is not specific to Claude Code, and compiling steers into other harnesses' files is already proposed. The anticipation card itself (predicted next asks, deferred tasks that match this repo state) is not, so Codex and Gemini sessions would get none of it.
  Done when: after `fm sync-agents`, AGENTS.md contains a marked, bounded "Likely next" block that is rewritten in place and stays under 12 lines.

- **Print an "expected to need you at" line when an unattended run starts** — FEATURE — value 3 — effort M — risk low — category: unattended
  Why: assumption: the user leaving a long run wants to know when to come back, not only the end-of-run forecast. The line would come from the median time to the first `fm ask` or blocked item in past runs, with a range, and be scored against the actual first interruption.
  Done when: a run start prints a time range, and the receipt records whether the first interruption fell inside it.

- **Show the user's open editor buffers as a next-ask hint, opt-in and local** — FEATURE — value 2 — effort M — risk med — category: signals (wild)
  Why: wild. Copilot and Cursor weight open files heavily. Foreman's predictors see only ledgers, not what the user is looking at. It needs an explicit setting, reads only paths (never contents), and is never sent to a model.
  Done when: with the setting off nothing is read, and with it on a test shows the hint list contains only repo-relative paths, and the privacy ledger records the read.

- **Score Foreman's surprise to the user before any costly decision** — FEATURE — value 3 — effort L — risk med — category: user model (wild)
  Why: wild. The pack has a user model that pre-answers `fm ask`. It could also grade how unexpected an action is: when a tool-less child given the user's steers and recent asks would not have predicted the action, Foreman asks first. This is the inverse of the pre-answer idea, and it targets "never block on the user" decisions that landed badly. Assumption: enough recorded drops exist to calibrate.
  Done when: on 20 past costly decisions, the surprise score separates the vetoed ones from the kept ones better than chance, and the number is printed with its sample size.

- **Open 90-day project predictions and settle them on the date** — FEATURE — value 2 — effort M — risk low — category: forecasting (wild)
  Why: wild. Sealed predictions in the pack look at the next ask. A long-horizon set ("these 5 files will churn most, this verb will be unused, this deferred task will be woken") tests the model of the project itself and gives the next Genesis seed real out-of-sample evidence from a clock Foreman did not control.
  Done when: `fm anticipate seal --days 90` stores a hashed file and `fm anticipate settle` on a fixture clock reports hits and misses against the ledger.

- **Pause on hesitation at an `fm ask` card** — FEATURE — value 2 — effort S — risk low — category: delight (wild)
  Why: wild. If a card sits unanswered far longer than the user's median reply time, the timed default countdown pauses and the card shrinks to the one-line recommendation, instead of timing out into a lowest-regret default the user didn't see. Assumption: reply latency is already in the `fm ask` ledger.
  Done when: a fixture where the reply latency exceeds 3× the median shows the shortened card and does not auto-apply the default.

Next question: which of the predictors proposed so far would still beat a plain "most recent open task" baseline on this user's own last 30 days, and has anyone run that?
Next question: when two anticipation sources disagree (history says X, an external event says Y), which does the user trust, and is there a recorded case to learn from?
