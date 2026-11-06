# Brainstorm — lens: grid

Surfaces are the web UI, the CLI (`fm`/`sampo`), the hooks and the lanes. Actors are the user, the agent, other agents (lanes) and the unattended run. Failure modes are missing, wrong, slow, unsafe and unclear. I'm going deep on the cells where the pack shows evidence, and I skipped the many cells the ideas-so-far list already fills.

- **Forecast tonight's stop reason from the last nights' stops** — FEATURE — value 5 — effort M — risk low — category: unattended
  Cell: CLI × unattended × missing. Why: T-2900 and T-2901 (the drive's false waits) and the user's "asleep, wants progress by morning" show the night usually ends by a stop reason, not by finishing. Fix the most likely cause before bed.
  Done when: `fm anticipate night` prints the top 3 predicted stop reasons from past stop records, each with a one-line pre-fix, and a backtest over the last 14 nights names the actual stop in its top 3 at least 60% of the time.

- **Infer the user's sleep window from ledger gaps** — FEATURE — value 4 — effort S — risk low — category: unattended
  Cell: unattended × user × unclear. Why: assumption: the drive currently treats "asleep" as declared. The gaps between event timestamps give an hourly activity histogram, and a timezone shift shows up as a moved histogram.
  Done when: `fm doctor` shows the inferred quiet window, and a ledger fixture shifted by 6 hours moves it within 3 days.

- **Mine hand-edits after agent landings into brief defaults** — FEATURE — value 5 — effort M — risk med — category: user model
  Cell: CLI × user × wrong. Why: assumption: the user edits agent output the same way each time (naming, wording, rename vocabulary). The pushbacks "don't show jarvis" and "don't say it's you" read as repeated corrections. Diff each landed commit against the user's next commits on the same files. Recurring patterns become checklist lines in the next brief's Done-when.
  Done when: a fixture where the user rewrote the same term in 3 landings makes the next drafted brief carry that term rule with the 3 commit ids as evidence.

- **Warn at commit when the touched files co-fail with a gate** — FEATURE — value 4 — effort M — risk low — category: gates
  Cell: hooks × agent × slow. Why: the 2358-file map and the long ship gate show red often arrives late. History of red gates against changed-file sets can say "this change reddened `test_site_landing` 4 of 5 times" before the full suite runs.
  Done when: a pre-ship note names at most 3 likely-red tests with counts, and replaying the last 50 red gates ranks the real red test in the top 3 at least half the time.

- **Serialise lanes by predicted file conflict** — PERFORMANCE — value 4 — effort M — risk med — category: lanes
  Cell: lanes × other agents × slow. Why: T-2851 and T-2852 both touched the site and tower, and the work-in-progress merges and "builder stopped" commits show collisions. Learn from past merge conflicts which file pairs collide, then order the parallel lanes so colliding briefs don't run together.
  Done when: given two briefs with a historically colliding file pair, `fm lane --plan` puts them in sequence and says why.

- **Fingerprint the local endpoint with a golden prompt set** — SECURITY — value 4 — effort S — risk low — category: local models
  Cell: lanes × agent × wrong. Why: the llama-swap endpoint can be reconfigured and a model switch costs about 3 minutes, so quality drift would go unseen. Run a fixed 10-prompt, temperature-0 set nightly and hash the outputs.
  Done when: changing the served model or its template changes the fingerprint line in `fm doctor`, and drafts are held until the user acknowledges it.

- **Tell "nothing to do" from "could not do" in the morning card** — FIX — value 4 — effort S — risk low — category: unattended
  Cell: web UI × user × unclear. Why: the drive's wait-counting bugs (T-2873 to T-2901) all made a silent idle look like work. The card needs a typed idle reason: empty queue, held by round-first, blocked on a user-only grant, endpoint cold or phantom-held.
  Done when: each of the five idle reasons has a fixture and renders a distinct line.

- **Cap every prediction at what the user can check in 10 seconds** — FEATURE — value 3 — effort S — risk low — category: delight
  Cell: CLI × user × slow. Why: the user's "stop asking me for stuff" shows low tolerance for review load. Rank predicted drafts by review cost (lines, new nouns) and show only those under a threshold, the rest folded behind a count.
  Done when: the card never shows a draft whose Done-when exceeds 3 lines unless the user asks for it.

- **Wild: Rehearse the morning from yesterday's ledger** — FEATURE — value 3 — effort M — risk low — category: anticipation
  Cell: web UI × user × missing. Why: assumption: the best test of a predictor is the real day. At 02:00 the local model "plays the user" with only data up to midnight and writes 3 asks. In the morning the web card shows them beside what the user actually typed first. Misses become labelled gaps.
  Done when: the card shows predicted vs actual first asks, and the hit count appears in `fm doctor`.

- **Wild: Cast the other agents as characters who predict each other** — FEATURE — value 3 — effort L — risk med — category: agents
  Cell: lanes × other agents × unclear. Why: when each lane hands back, the next lane writes what it expects the planner to ask about it. Compare that with the planner's real next move, and the disagreements show where lane hand-backs under-explain.
  Done when: a hand-back field `expects_next` exists, and a weekly count of mismatches is logged.

- **Wild: Give the tower a pulse the user can feel when away** — FEATURE — value 2 — effort M — risk low — category: devices
  Cell: unattended × user × unclear. Why: the user sleeps and wants progress by morning. A phone-visible heartbeat (a plain web page with last-alive time and the stop forecast) lets them see "alive, 3 closes, no stops" without opening the terminal. Assumption: a local-network page is acceptable.
  Done when: the page loads with no remote origin and shows last-alive within 60 seconds of a lane event.

Cells left empty:
- Web UI × agent: the agent doesn't read the web UI.
- Web UI × other agents × unsafe: already covered by the stale-tab and non-instructional-data ideas.
- Hooks × user × slow: bench and ratchet ideas already fill it.

Next question: which of the user's repeated corrections (the rename vocabulary, "wilder moons", "no jarvis") were predictable from earlier edits, and how many sessions would the hand-edit miner have needed to catch each?
Next question: when the local 27B and a frontier model draft the same brief, which fields differ most, and does that difference predict which drafts the user rewrites?
