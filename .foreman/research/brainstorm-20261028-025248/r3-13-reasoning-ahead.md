# Brainstorm — lens: reasoning ahead

- **Warm the first post-reset run from a pre-compacted context** — FEATURE — value 4 — effort M — risk med — category: usage timing
  Why: the weekly reset is the one point where the whole budget reopens at once, and T-1796 already compacts at 200k. Assumption: a run that starts cold after the reset spends its first replies re-reading the same files.
  Done when: the first run after a simulated reset sends under 140k context on its first reply, measured by `fm cost`.

- **Price each rules-file line in dollars per week** — FEATURE — value 4 — effort S — risk low — category: cost at scale
  Why: the rules file is over its 6,400-char budget (T-1520, 6,416 chars), and the cost is paid on every run, but no line shows its share. Multiply each line's tokens by the runs per week and it becomes a number.
  Done when: `fm doctor` prints a weekly dollar figure per rules section, and the sum is within 10% of `fm cost` for the same week.

- **Rehearse the gate on the runner image before it rolls** — PERFORMANCE — value 4 — effort M — risk med — category: CI drift
  Why: a runner-image change broke crash tests (T-1807, the copied sleep on Ubuntu 26) and CI chromium crashed under load (T-1806). Both were found after they broke main.
  Done when: a scheduled job runs the suite on the image named in the runner-images changelog and files pass or fail a week before that image becomes the default.

- **Stop the suite before it hits the CI cap** — FEATURE — value 4 — effort S — risk low — category: CI headroom
  Why: the 20-minute job cap hid where a test hung (the reason for run.py's 480 s kill), and the macOS job hit its 35-minute limit and cancelled main's run (T-1809). The runtime trend shows the cap coming before it arrives.
  Done when: at 80% of the cap, `fm doctor` warns and names the slowest test class.

- **Warn when a pinned action's runtime is due for removal** — FEATURE — value 3 — effort S — risk low — category: version skew
  Why: the Node 24 move (T-1804) was done by hand, pin by pin. Assumption: runtime deprecations arrive with a date that can be read ahead of time.
  Done when: `fm doctor` lists every pinned action whose runtime is deprecated, with its end date and the bump command.

- **Show a blocked item once per change in its unblock predicate** — CLEAN — value 3 — effort S — risk low — category: blocked pile
  Why: the blocked pile (T-0335 to T-0418 and more) lists the same items every session, even when nothing that would free them has moved. Repeated lines train the user to skip the section.
  Done when: session start shows each blocked item only when its predicate's value has changed since the last session.

- **Predict the gate lock's release and say when it frees** — PERFORMANCE — value 3 — effort M — risk med — category: gate contention
  Why: a hung check in another project held the lock for over 40 minutes, and the current 15-minute wait has no estimate of when the holder will finish. Assumption: the journal's past holds predict the typical length.
  Done when: the wait message shows a free-by time that falls within 2 minutes of the real release across 10 recorded holds.

- **Wild: price every announced model before it ships** — FEATURE — value 2 — effort S — risk low — category: model drift
  Why: wild. Cost math is rerun when the model changes, but only after the change lands. Pricing each announced model in advance makes the switch a one-line cost-table edit.
  Done when: adding a new model ID to the cost table produces a dollars-per-green-gate figure with no code change.

- **Wild: a seven-day tide table of spend, printed at session start** — FEATURE — value 3 — effort M — risk low — category: budget foresight
  Why: wild. Spend is shown as a running total, not as a shape. A tide table shows which hours and days the budget will run dry, so the user can plan around the rising water.
  Done when: `fm status` prints seven daily spend bands, and today's band matches the total from `fm cost`.

- **Wild: a red-streak forecast before each push** — FEATURE — value 3 — effort M — risk low — category: CI foresight
  Why: wild. Main's CI has gone red from cancelled runs and a false alarm (T-1810). A forecast from the last 30 runs of this repo, shown before the push, turns a surprise into a known risk.
  Done when: each push logs a forecast, and the forecast is scored against the outcome after the run.

- **Wild: a reliability diagram of Foreman's own forecasts** — CLEAN — value 2 — effort M — risk low — category: self-calibration
  Why: wild. Foreman now makes forecasts (budget, lock release, red streaks). Nothing checks whether they come true, so none of them can be trusted or tuned.
  Done when: at least 20 forecasts are logged, and a calibration plot is written with each forecast's stated and observed rate.
