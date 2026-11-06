# Brainstorm — lens: user value

**Questions left earlier, answered through the user-value lens**
- *What does the user get if they never open the web UI?* Nothing, unless the forecast arrives as one `fm next` row or a SessionStart line. Every Anticipation cell should name that delivery path, and a cell that only renders in the UI shouldn't count.
- *Which outputs does no session path read?* Any forecast the user can't act on in one word. I treat those as the first deletion candidates.

**Ideas**

- **Warn about habit-breaking changes from the user's own history** — FEATURE — value 4 — effort M — risk low — category: forewarning
  Why: assumption: a renamed or retired verb hurts most where the user types it daily. Standing rules require a retired-verb name for new verbs, but nothing weights the changelog by what this user actually runs.
  Done when: after an update that renames a verb the fixture history uses 5+ times, session start names that verb and its replacement, and stays silent about verbs the user never used.

- **Show a retro demo at install: "what I'd have caught last month"** — FEATURE — value 4 — effort M — risk med — category: onboarding
  Why: the pack shows T-0862 and T-0863 (newcomer tour, start ladder) deferred for lack of evidence the first-run guide isn't enough. A replay of the user's own past transcripts is evidence they can't dismiss. assumption: transcripts exist on the machine.
  Done when: `fm foresight demo` on a fixture history prints 3 backtested heads-ups, each with the date it would have fired and what happened next, and sends nothing off-machine.

- **Put one anticipation dial per project** — FEATURE — value 3 — effort S — risk low — category: control
  Why: the rules mute a signature after two dismissals, but the user has no single, visible way to say "warn only" or "off here". assumption: users want a project-scoped switch.
  Done when: `fm foresight warn-only|off|on` is persisted per project, and `fm doctor` shows the current mode and what it suppresses.

- **Review the Anticipation capability on a schedule, and demote it if it doesn't pay** — FEATURE — value 4 — effort M — risk low — category: accountability
  Why: per-signature muting exists, but nothing checks whether the whole capability earns its context. The rules say lean growth must be measured. Once it has 20 or more resolved predictions, it should be reviewed against the shuffled baseline.
  Done when: a 30-day review prints adopted/ignored counts and cost beside the baseline, and auto-demotes to warn-only (undoable) if it's below baseline.

- **Size lanes to the user's review capacity** — FEATURE — value 3 — effort M — risk med — category: lanes
  Why: assumption: speculative drafts pile up faster than the user reads them. The "yes-bundle" idea batches questions but never limits how much review is generated.
  Done when: with a cap of 3 open drafts, a fourth predicted draft is queued as a title-only stub, and `fm next` shows the count waiting.

- **Predict reviewer comments from past review history** — FEATURE — value 3 — effort L — risk med — category: pre-flight
  Why: assumption: the repo has a PR comment history reachable through `gh`. This is a different signal from the user's own corrections.
  Done when: on a fixture repo, `fm foresight review` lists 3 predicted comments with the past comment each came from, and a hit-rate is recorded once real feedback arrives.

- **Add a regret button for misses** — FEATURE — value 3 — effort S — risk low — category: feedback
  Why: "that again" and `fm doubt` exist as ideas, but nothing lets the user record "this surprised me and cost minutes" against the cell that should have caught it.
  Done when: `fm regret "<words>"` files the miss with a minutes estimate and links it to the nearest empty or filled cell. Empty cells rank by accumulated minutes.

- **Rank the 58 cells by minutes lost, not by row order** — FEATURE — value 4 — effort S — risk low — category: coverage
  Why: the standing rule says each generation fills the empty cells first, but not which first. The `fm friction` and reopen data in the ledger already carry the cost signal.
  Done when: `fm genesis cells --by cost` lists empty cells in descending order of reopen and friction minutes, each with its source row.

- **Replay review: show hit-rate by what the user asked** — FEATURE — value 3 — effort M — risk low — category: transparency
  Why: assumption: a user trusts a forecaster more when it shows which ask types it gets right. T-2546 showed the word-overlap matcher met no bar, so honest per-kind rates matter.
  Done when: `fm foresight rates` prints hit@3 by ask kind (FIX, FEATURE, CLEAN) and abstains below 10 samples.

- **Wild: Offer a swipe deck that calibrates the user's annoyance threshold** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: wild. Ten past nudges shown with the context, and the user swipes useful or annoying in the web UI. The result sets the evidence floor per kind. Done when: after 10 swipes, the stored floor changes and a fixture nudge below it is suppressed.

- **Wild: Print the ask you'd probably send, with a one-word "go"** — FEATURE — value 5 — effort L — risk high — category: prediction
  Why: wild. After a close, the top predicted follow-up appears in `fm next` as a drafted, grounded task. A single word accepts it, and it expires unmerged in 48 hours. It must pass the "already built" check first. Done when: on a planted-history fixture the draft appears, and "go" files it as a real task.

- **Wild: Watch upstream issues for the functions the user actually imports** — FEATURE — value 3 — effort L — risk med — category: forewarning
  Why: wild. This goes beyond abandonment scoring. A new upstream bug about an API in the user's import graph becomes a one-line heads-up before it bites. Done when: on a fixture with a pinned dependency and a mocked advisory feed, the warning names the importing file.

**Next question:** For each of the 58 cells, which one-word user action (go, no, later) would the output need, and which cells have none?
**Next question:** If a user has run Foreman for a week and ignored every forecast, what does the product do differently on day eight?
