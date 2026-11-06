# Brainstorm — lens: blind spots

- **Gauge birth certificate: refuse a new gauge that cannot answer the eight missed-ask questions** — FEATURE — value 5 — effort M — risk low — category: instruments
  Why: T-2534 to T-2566 are all asks about an instrument, not the product: no control arm, no liveness, no input origin, no behaviour on partial input, no commit attribution, no already-built check, no grounding, no held-out split. Each gauge Mission 1 adds (tick usefulness, lateness, shadow grade) can repeat them.
  Done when: `fm genesis put` or `fm task new` for a task creating a gauge refuses without a certificate with seven lines (control, liveness, input origins, partial-input behaviour, attributing commit, already-built hit, denominator). A fixture gauge missing the liveness line is refused naming that line.

- **Fill a class-by-capability blind-spot grid with probes** — FEATURE — value 5 — effort L — risk med — category: coverage
  Why: the lens asks the missed-ask questions of the whole project. Eight classes times 13 capabilities is 104 cells, each either a probe result, an existing path, or a filed gap. This is more productive than inventing new classes because the classes already cost the user an ask each.
  Done when: `fm genesis blindspots` prints the grid and every cell holds a re-runnable probe command or a task id. A planted gap in one cell turns it red.

- **Add a zero-model-call invariant and dollar meter for the tick** — SECURITY — value 4 — effort S — risk low — category: cost
  Why: assumption: nothing asserts that a tick with no armed trigger spends $0. The user has a hard USD budget and "don't stop for budget" steers, so an install-free tick that quietly spawns a `claude -p` child is exactly the unrequested spend they would then ask about.
  Done when: a test runs the tick with a stub `claude` on PATH that fails on any call, with no trigger armed, and passes. A tick that does spawn a child writes its cost to `fm cost`.

- **Key replay tapes by patch-id so history rewrites don't rot them** — FIX — value 4 — effort M — risk low — category: measurement
  Why: assumption: replaying this repo's git history as the event stream is the main install-free measure. Foreman's `fm release` and ship cherry-picks onto main (T-2598) change SHAs, so tapes keyed by SHA go stale.
  Done when: a tape recorded before a cherry-pick replays to identical fire decisions after it. Test: rewrite a fixture branch and compare outcomes.

- **Stamp tick output lines with premises and revalidate them on read** — FIX — value 4 — effort M — risk low — category: staleness
  Why: assumption: a card computed by the tick at night and read at 9am can name tasks already closed or a HEAD already moved. The same "stale map" class showed up earlier ("as of an older HEAD" in the map line).
  Done when: every card line carries a HEAD and task-state stamp, and display drops or marks a line whose stamp no longer holds. A fixture that closes a task between compute and read shows that line struck.

- **Declare `needs:` preconditions in DONE-WHEN and probe them at task birth** — FEATURE — value 4 — effort M — risk low — category: premises
  Why: the mission text says "waits on the user's install", and a precondition outside the repo was only discovered after a week went by. Tasks should name their external dependencies (systemd user session, linger, `gh` auth, `claude` on PATH, network) and have them probed when the task is created.
  Done when: `fm task new` with `needs: systemd-user` on a box without it prints the unmet need and the substitute measure. A task with all needs met prints nothing extra.

- **Detect blind spots by release-lag: asks arriving within 72h of a release** — FEATURE — value 3 — effort S — risk low — category: feedback
  Why: assumption: asks that follow a release or Mission tend to hit what it shipped. Linking each ask to the preceding release and the area it touches would find classes automatically, instead of the user noticing them one at a time.
  Done when: `fm outcomes --lag` lists, per release, the asks within 72h that name its modules, and ranks releases by that count.

- **Run decision procedures with each input subset missing** — FIX — value 4 — effort M — risk low — category: robustness
  Why: T-2566 was `fm genesis select` deciding on held-out-only input. Other selectors and gates (sweep rows, `fm exam` grading, ratchets, `fm doctor` WARNs) can be wrong in the same way, and a property test would catch it before the user does.
  Done when: a harness enumerates every function named select/decide/grade/keep and feeds it each missing-field variant. Each returns a typed "insufficient" or a documented default, with none raising or silently choosing.

- **Make the first self-triggering result carry its own external check line** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: the pack's open question: which output does the user act on unchecked? A self-started result should show a one-line command the user can run outside Foreman (e.g. `git log --since=...`) to confirm it.
  Done when: every tick-originated task or card ends with a `verify:` line that runs standalone and exits 0 when the claim holds.

- **Wild: use direnv and editor folder-open tasks as a committed, install-free clock** — FEATURE — value 3 — effort M — risk med — category: triggers
  Why: wild. assumption: `.envrc` and `.vscode/tasks.json` with `runOn: folderOpen` live in the repo, so they need no OS-level install and fire when the user enters the project. Not yet listed among the clock ideas.
  Done when: `fm tick --install-edge` writes both files (printed first, behind a yes), and entering the fixture dir under direnv records a tick with source `direnv` in the lateness ledger.

- **Wild: gauge cross-examination — a cold child must name how each gauge reads green while broken** — FEATURE — value 4 — effort M — risk med — category: instruments
  Why: wild. A tool-less child that sees only the gauge's definition and ledger schema writes a failure scenario for each. Each scenario becomes a planted-fault test, targeting what the author could not see, in line with the standing "signals Foreman didn't author" rule.
  Done when: for each gauge in `fm doctor`, a stored scenario exists and a planted-fault fixture flips the gauge red, or the gauge is listed as unfalsifiable.

- **Wild: write the next Mission's missed-ask list before the Mission runs** — FEATURE — value 3 — effort S — risk low — category: prediction
  Why: wild. Seal a prediction of the three asks about the instruments of Mission 1 (e.g. "is the beat file honest?"). When the user actually asks, score the match. This turns the blind-spot miss list into a measured hit rate.
  Done when: a sealed file exists before the Mission's first commit. After the Mission, `fm genesis review` prints the matches and misses.

Next question: Which gauge in `fm doctor` today has no input the user could falsify by hand, and what is the cheapest outside check for it?
Next question: When a self-started action fails during the install-free period, what does the user see first, and is it read from a file or injected into a session?
