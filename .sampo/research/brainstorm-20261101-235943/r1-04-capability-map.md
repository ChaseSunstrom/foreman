# Brainstorm — lens: capability map

Reference products for anticipation: Cursor Tab and Copilot next-edit, CodeScene hotspots, Launchable predictive test selection, atuin/fish history suggest, Netdata forecasting, Reclaim.ai, Jules and Devin proactive task suggestions. The ideas below are the capabilities from that set that the pack does not already list. Most of the 58 cells collapse into a few families (machine, history, edit, environment), so each idea below is a family probe that can stamp several cells.

- **Forecast tmpfs and disk runway before spawning lanes** — FEATURE — value 4 — effort S — risk low — category: machines
  Why: the child dir is `/run/user/1000/…` (tmpfs), and T-2543 was an ETXTBSY flake on the same kind of volume. "Cap scratch use" caps the space but does not predict when it runs out.
  Done when: with a faked fill rate, `fm doctor` and the lane spawner both print "tmpfs full in ~N min" and refuse a new lane under a set runway.

- **Keep a per-machine failure profile** — FEATURE — value 4 — effort M — risk low — category: machines
  Why: gen-0 #3 says "my machines", and T-2529 (Python without setuptools) was interpreter-specific. Key gate outcomes by host fingerprint (OS, kernel, Python, claude version).
  Done when: a fixture run recorded on host A and replayed on host B prints "this gate failed on B before: <signature>" before the run starts.

- **Show a hotspot-times-reopen risk line at plan time** — FEATURE — value 4 — effort M — risk med — category: risk
  Why: CodeScene-style churn × complexity × bug-fix history is not in the pack. Backtest it on closed tasks, and ship only if the flagged files reopen at least 2x the base rate.
  Done when: `fm plan` names the top hotspot files it touches, and the backtest report shows the lift over the base rate.

- **Rank tests by learned failure likelihood** — PERFORMANCE — value 3 — effort M — risk low — category: testing
  Why: `fm ship` runs affected-first but with no learned ordering, and a Launchable-style ranking would fail faster. Assumption: failure history is kept per test.
  Done when: replayed over the last 50 red runs, the failing test comes in the first 10% of the order at least 80% of the time.

- **Pre-empt flag and verb mistakes with a generated synonym table** — FIX — value 3 — effort S — risk low — category: friction
  Why: T-2540 (`remove`/`delete`/`del`), the `--by harness` steer and `--last` were all found by users after the fact. Generate neighbours for every verb and flag from edit distance and a small synonym list, and accept them with a note.
  Done when: a test feeds 30 plausible near-misses and each either maps to the right verb or gives one "did you mean" line, never a bare error.

- **Suggest the likely next verb from verb n-grams** — FEATURE — value 3 — effort M — risk med — category: ghost-next
  Why: atuin and fish suggest from history, and Foreman holds a full verb log per stage. It shows only if top-1 is correct at least 50% in backtest, else stays silent.
  Done when: the status line shows the suggestion, and the backtest table prints top-1/top-3 against the "repeat the last verb" baseline.

- **Queue sibling edits from the user's uncommitted hand edits** — FEATURE — value 4 — effort M — risk med — category: next-edit
  Why: Cursor Tab predicts follow-on edits, and nothing in the pack watches hand edits. A renamed signature leaves unedited call sites, listed at Stop.
  Done when: a fixture that renames a function by hand gets the unedited call sites named before the session ends.

- **Read every harness's transcripts into one user model** — FEATURE — value 4 — effort M — risk med — category: user-model
  Why: a standing rule says Foreman is not Claude-specific, and bets already carry a harness field. A model built from Claude transcripts alone misses codex, gemini and opencode asks.
  Done when: `fm me` shows request counts per harness, and a fixture codex transcript changes a prediction.

- **Score dependencies for abandonment risk** — FEATURE — value 2 — effort M — risk low — category: supply
  Why: the stack-card library is huge but static. Add release cadence, open-issue age and maintainer count for the deps a project actually imports, as a plan-time warning on adds.
  Done when: adding a dep untouched upstream for 2+ years prints a warning naming that date.

- **Warn at departure about unpushed work on the other machine** — FEATURE — value 3 — effort S — risk low — category: machines
  Why: gen-0 says "my machines". Assumption: the user works on several, and a dirty tree or unpushed commit on one is invisible from the other.
  Done when: the session end note lists unpushed commits and dirty files, and the next session on another host (simulated) names them.

- **Run a future canary on the gate at faketime +90d with latest deps** (wild) — FEATURE — value 4 — effort M — risk low — category: time bombs
  Why: wild; the pack has Python 3.14 setuptools drift and host-update drift, but nothing that runs the suite in the future for cert expiry, date-dependent tests or deprecations. The night tick files tasks.
  Done when: a planted test that fails after a fixed date is caught by the canary and filed as a task before that date.

- **Pre-read the next likely file into the graph cache** (wild) — PERFORMANCE — value 2 — effort M — risk low — category: warm
  Why: wild; from co-change history, compute blast radius and file summaries for the most likely next file while the user types. Keep only if the cache hit rate beats 40%.
  Done when: a hit-rate counter shows hits and misses, and the feature turns itself off below the threshold.

- **Print one annoyance forecast at session start** (wild) — FEATURE — value 3 — effort S — risk low — category: delight
  Why: wild; join friction history to current state ("tests run 2x slower at 91% disk, CI red on main since Tuesday") into a single line chosen by past complaint frequency.
  Done when: the line appears only when at least one factor is over threshold, and a quiet fixture prints nothing.

- **Lock each family probe to a cell and a session path** — CLEAN — value 4 — effort M — risk low — category: coverage
  Why: the earlier open question says many of the 58 cells are one capability, so each family above gets one probe naming the cells it covers and the hook or verb that calls it.
  Done when: `fm genesis check` lists each filled cell with its probe and its session-path reach, and a cell with neither shows as unfilled.

Next question: Which of these predictors have a measured baseline (repeat-last-request, base rate) on real history, and which would ship with no way to tell they were worse than doing nothing?
Next question: What does the user do on a machine other than this one that Foreman never sees?
