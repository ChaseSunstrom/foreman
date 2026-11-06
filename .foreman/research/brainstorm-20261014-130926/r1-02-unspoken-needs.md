# Brainstorm — lens: unspoken needs

- **Re-fetch tripwire for compact output** — FEATURE — value 4 — effort S — risk low — category: tokens
  Why: compact output rewrites Bash results over 6,000 chars to head, failure lines and tail. The savings figure (~1.04M tokens/30 days) is measured. The cost of lost information is not. Assumption: if the model re-runs the same command or reads the spill file soon after, the digest hid something it needed.
  Done when: a test replays a re-run-after-compact sequence, and `fm doctor` lists that command pattern as exempt after N re-fetches.

- **Shadow-mode compact output with a one-line ask** — FEATURE — value 4 — effort S — risk low — category: tokens
  Why: compact output "is off until the user says yes", and nobody has been asked in a form that is easy to answer. Run it in dry-run for a few days, logging what would have been dropped and any failure lines it would have lost. Then ask once with real numbers: "saves X tokens, lost 0 failure lines in N outputs, enable?"
  Done when: with the setting off, `fm cost` shows a "would have saved" line, and a single yes flips the setting.

- **Run a live arming canary for the mail monitor** — FEATURE — value 5 — effort M — risk med — category: liveness
  Why: the pack lists "arming in a live interactive session is unverified (monitors start only in new sessions)" as a known gap. `fm doctor --live` posts a self-addressed bus message, waits briefly, and records whether the monitor delivered it. At session start, show one line only when something is missing, such as "mail monitor: not armed, session predates install".
  Done when: a session started before install reports "not armed", a new one reports "armed (receipt <ts>)", and both cases are tested.

- **Snapshot metrics per round and judge the round by them** — FEATURE — value 5 — effort M — risk low — category: self-improvement
  Why: the user's steer is "recursively improve", meaning repeated rounds, but nothing measures whether round 1 helped. At round start and end, snapshot hook p50, tokens per task, idle-while-queued minutes, first-pass rate and guard false positives. Round 2's pack leads with the deltas, and a flat or negative delta becomes a task.
  Done when: `fm round show 1` prints before/after for at least four metrics, and the next `fm ideas` pack includes that table.

- **Tick the board: a keep/tune/revert review of shipped items** — FEATURE — value 4 — effort S — risk low — category: feedback
  Why: "nobody has ticked the board yet". After a round ships, show a one-screen list of what shipped, each with one key: keep, tune (with a one-line reason) or revert. Reasons are stored as steers. Reverts open a `fm task new --redo`.
  Done when: running the review marks each shipped item with a verdict in state, and a `tune` reason appears in the next pack under "The user's own words".

- **Lint verify commands for self-expiring references** — FIX — value 4 — effort S — risk low — category: verification
  Why: the dropped item says the check "grepped the queue for T-0775, which left the queue when it was done". Refuse at plan time any verify that greps queue or inbox membership, tmp paths, dates or live session ids, and suggest a durable form such as a file, test or ledger fact. This extends the existing "unrunnable verify refused" check.
  Done when: planning a verify that greps the queue for its own task id is refused with a rewrite hint, and a test covers it.

- **Generate reader tests from real writer output** — FIX — value 4 — effort M — risk low — category: reliability
  Why: two user-reported bugs came from a stored string `✗ exit N` that readers matched as `exit N`. For each persisted result format, capture samples from the actual writer (`fm task finish` results) as fixtures, and run every reader (track record, catch rates, give-up mining) against them.
  Done when: reverting either of the two fixes makes a generated test fail.

- **Track warning precision at close** — FEATURE — value 3 — effort M — risk low — category: observability
  Why: round 1 fixed two false close warnings (tier drift, `.claude/` left behind). Record each close warning together with whether the next action heeded or ignored it. Warnings ignored more than 90% of the time over N closes are demoted to the ledger and not shown.
  Done when: `fm doctor` lists per-warning heed rates, and a warning below the threshold is no longer printed at finish.

- **Turn deferral reasons into unlock triggers** — FEATURE — value 3 — effort M — risk low — category: planning
  Why: round 1 deferred clusters for stated reasons: "after liveness", "mod update blocked", "needs per-project servers". Store each as a checkable condition, for example "monitor arming verified" unlocks the fleet registry. Surface a task when its condition turns true, so it stops sitting idle in deferred.
  Done when: marking the arming canary green moves T-0792 to "ready" with the reason shown.

- **Spend leftover round budget on small deferred tasks** — FEATURE — value 3 — effort M — risk med — category: autonomy
  Why: assumption: rounds often converge early with budget unspent, while S items such as T-0759, T-0418 and T-0431 sit deferred or planned. A sweeper takes S-tier, low-risk tasks with existing plans, runs them in lanes, and leaves results for review. It may not release or publish.
  Done when: with $ remaining and no new ideas, a round closes at least one S task, and nothing outward-facing happens without confirmation.
  **wild**

- **Predict which shipped items the user will drop** — FEATURE — value 3 — effort S — risk low — category: taste
  Why: the dropped list shows a pattern: premises disproved by measurement (Read-hook if-filters, delta reads), and by-design guard rules. A cheap child reads that list plus the round's shipped list and flags the likely-dropped items, each with the measurement that would settle it. Run those measurements first.
  Done when: for the round, at least one flagged item has a measured premise attached before anyone reviews it.
  **wild**

- **Test discoverability with a cold agent** — FEATURE — value 3 — effort M — risk low — category: docs
  Why: round 1 added the mail monitor, session titles, push-on-ask, `fm page` and `fm research list/show`. A fresh child with only README and MASTER.md is asked "how do I get notified when Foreman needs me?" and "how do I see the queue on my phone?". Failed answers become doc tasks.
  Done when: the test lists each round-1 feature as found or not found, and the unfound ones are queued.
  **wild**

- **Stamp each round's catalogue with a closing receipt in `fm research`** — CLEAN — value 2 — effort S — risk low — category: docs
  Why: the don't-repeat list is thousands of lines, and the user keeps saying "past every earlier idea". Record per round how many ideas were shipped, queued, dropped and repeated, with one line each on why dropped. Round N+1's brief can then say "round 1 gave X, kept Y".
  Done when: `fm research show round-1` prints those four counts and the drop reasons.
