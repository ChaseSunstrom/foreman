# Brainstorm — lens: unspoken needs

- **Stop brainstorming when it starts repeating itself** — FEATURE — value 4 — effort S — risk low — category: brainstorm
  Why: this pack's "ideas so far" restates "unproven receipt state", "restore drill" and "outside gauge check" five or more times each, so later rounds spend budget rediscovering the same items.
  Done when: `fm ideas` clusters a run's output against the catalog, prints the new-cluster rate per round, and recommends stopping once a round yields under 20% new clusters. Clusters rediscovered by 3 or more lenses are ranked first.

- **Score intake precision from the user's own drops** — FEATURE — value 4 — effort S — risk low — category: intake
  Why: the "dropped" lines are labelled false positives: a bash-input echo, a re-pasted steer, a credential line. T-2624 fixed only the credential class.
  Done when: `fm intake --precision` replays the dropped and kept asks through the classifier. It reports drop rate per paste shape (shell echo, quoted steer, log, key), and a test fails if any shape in the corpus is captured as an ask.

- **Run the user's examples as red-first tests** — FEATURE — value 4 — effort M — risk med — category: criteria
  Why: T-2583's criterion said 8+ characters while its own example "4% lost" has 7. Examples inside criteria are the user's real intent, but nothing executes them.
  Done when: `fm task new` extracts quoted examples marked as matching or not matching a criterion. The prove step runs each against the implementation, and a contradicting example blocks the start with the two lines quoted.

- **Make two cold readers interpret each DONE-WHEN independently** — FEATURE — value 4 — effort M — risk low — category: criteria
  Why: the user's corrections are mostly about how a criterion was read, such as T-0034's scope and the beyond-row steer. Divergent readings are cheap to detect before any code is written.
  Done when: for L and M asks, two tool-less children restate the criterion as a checklist. If the checklists differ, the task gets a one-line "read as X, could mean Y" note and the stricter reading is the default. A fixture with a known ambiguous criterion triggers it.

- **Wake deferred tasks when matching evidence arrives** — FEATURE — value 4 — effort M — risk low — category: backlog
  Why: more than 30 "Later from T-07xx/08xx" tasks sit deferred with prose conditions like "needs evidence the first-run guide…". Nothing connects a later friction entry or failure to the task it would justify.
  Done when: `fm friction`, exam failures and doctor warnings are matched against deferred and blocked task text nightly. A match above a threshold re-opens the task with the matching line quoted. A planted friction entry wakes the right fixture task.

- **Spool child output off tmpfs before the session ends** — FIX — value 3 — effort S — risk low — category: durability
  Why: assumption: brainstorm children run under `/run/user/1000/fm-children-1000`, which is tmpfs and disappears on logout or reboot, taking in-flight outputs and any partial findings with it.
  Done when: each child's final and partial output is copied to the durable state directory on exit. A test that clears the tmpfs path mid-run still lets `fm ideas` recover the output.

- **Stamp each result with a model fingerprint and canary it** — SECURITY — value 3 — effort M — risk low — category: measurement
  Why: bets, exam lines and cold reads all compare across weeks, while models update underneath (Sonnet 5.5 and Haiku 5.5 here). A silent shift would look like a Foreman regression or gain.
  Done when: every bet, exam line and cold read records a model id. A fixed 10-prompt canary run nightly flags when answers drift beyond a set distance, and `fm exam` marks lines that span a flagged change as non-comparable.

- **Record guard blocks the user worked around** — FEATURE — value 3 — effort M — risk med — category: guard
  Why: the guard's purpose is stopping commands "you'd never want run", but false blocks cost more than anything else in bypass mode. Nothing measures them; the existing ideas cover the "close call" shelf, not the false-positive side.
  Done when: a block followed within 5 minutes by the same intent via another route is logged as a probable false block. `fm doctor` lists the top three rules by that rate, each with a proposed narrowing and a unit test pair that keeps the true positive blocked.

- **Promote steers across repos only when they recur** — FEATURE — value 3 — effort M — risk med — category: steers
  Why: the standing-intent file is one source across projects, but most of the 30 steers are project-specific (Genesis, exam cadence). Without scope, they either leak into other repos or never reach them.
  Done when: each steer carries a scope (project or global). A steer matched by a similar correction in a second repo is proposed for promotion with both quotes shown, and nothing is promoted without the user's yes.

- **Rank capabilities by correction regret** — FEATURE — value 3 — effort S — risk low — category: prioritization
  Why: the user's steered lines, such as T-2583's criterion and the beyond-row change, are corrections on specific capabilities, but the Seed ranks by exam and outcomes only.
  Done when: corrections are attributed to a capability by task id, and `fm genesis` prints a regret count per capability next to its exam score. The next Seed's first Mission targets the highest-regret capability with a failing check.

- **Bet on whether each idea will ship and be used** — FEATURE — value 3 — effort M — risk low — category: calibration — wild
  Why: Foreman already settles bets and scores Brier, while lens quality is judged by hand and T-0829 only drops dry lenses. Ideas are a cheap thing to bet on, with settlement at 30 days.
  Done when: each filed idea records a "shipped and used within 30 days" probability. The settlement reader scores each lens's Brier and shows which lens's confidence is best calibrated.

- **Sign an absence contract before leaving** — FEATURE — value 3 — effort M — risk med — category: unattended — wild
  Why: the standing rules say never block and wait out limits. The user's unstated need is knowing exactly what happened while away, and that nothing outward happened beyond what they allowed.
  Done when: `fm away until Thu --spend 40 --no-outward` writes a manifest. The tick refuses anything outside it, and on return one screen lists work done, spend, refused actions and the few decisions that need the user.

- **Schedule heavy runs around the user's own rhythm** — FEATURE — value 2 — effort S — risk low — category: scheduling — wild
  Why: assumption: steer timestamps show when the user is awake and reading. Heavy tower runs and fan-out brainstorms could finish just before those hours, and interruptions land when they are most likely to be read.
  Done when: `fm night` derives active hours from steer and ask timestamps in the ledger. It starts costly jobs to end 30 minutes before the usual first message, and a test with synthetic timestamps shifts the start time accordingly.

- **Produce a redacted support bundle** — FEATURE — value 3 — effort S — risk low — category: support
  Why: Foreman is public on GitHub with a site, but a stranger's bug report has no standard way to carry doctor output, versions and hook timings. T-2624 shows pasted secrets are a real hazard.
  Done when: `fm support` writes one archive with doctor output, versions, recent hook errors and ledger shape counts, passed through the credential redactor. A planted key in the fixture home never appears in it.

Next question: which of the user's steers have been silently reversed by a later one, and does any reader still enforce the old one?
Next question: what does the user do in the first five minutes after a long unattended run ends, and could Foreman have done that step beforehand?
