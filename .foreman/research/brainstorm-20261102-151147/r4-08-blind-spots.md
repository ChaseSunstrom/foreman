# Brainstorm — lens: blind spots

Each idea comes from asking one question of the whole project. A line starting "Q:" gives the question.

- **Fuzz every numeric flag with hostile values** — FIX — value 3 — effort S — risk low — category: input validation
  Why: T-2669 added `--stall-usd N`. Q: what do 0, -1, nan, inf, 1e400 and "5$" do to every numeric flag? Assumption: no one has swept these; the `fm run` stop flags are the likeliest to misbehave.
  Done when: a test feeds each hostile value to every numeric flag on `fm run`, `fm burden` and `fm budget`, and each is rejected with a one-line message or handled the same as a documented value.

- **Audit caps that live only in process memory** — FIX — value 4 — effort M — risk med — category: unattended safety
  Why: `--stall-usd` counts spend "since the last close". Q: which guards reset when the drive restarts, is killed or is re-exec'd? Assumption: some counters are held in memory, so a crash loop re-arms them.
  Done when: a test runs a drive, kills it with -9 at 90% of a cap, restarts it, and the cap trips at the remaining 10% (derived from the ledger).

- **Add dialect packs to the guard exam for non-bash shells** — FEATURE — value 3 — effort M — risk low — category: guard
  Why: T-2668 hardened bash parsing, and the listed ideas cover bash expansion and interpreter one-liners. Q: what happens when the command is fish, nushell, PowerShell, dash or busybox syntax run through `sh -c`? Assumption: the Arch-hardened host user may use fish.
  Done when: an exam set of 40 destructive commands in five shell dialects shows each is blocked, or is reported as "unparsed" with a counted fallback.

- **Cap line and record size in every ledger and transcript reader** — SECURITY — value 3 — effort S — risk low — category: reader robustness
  Why: T-2668 bounded time but not memory. Q: what does a reader do with a single 200 MB line or a deeply nested JSON record? Assumption: readers use `json.loads` per line without a size check.
  Done when: a test feeds each reader a 50 MB line and a 10,000-deep nest, and it skips both, reports the skip, and stays under a stated peak-memory bar.

- **Generalise the stall stop to disk, children and tool-call resources** — FEATURE — value 3 — effort M — risk low — category: runaway control
  Why: T-2669 stops on dollars without progress. Q: what other resource can run away with no task closing? Assumption: a loop writing logs or spawning children costs nothing in dollars. Dollars read zero on subscriptions, which makes this likelier.
  Done when: `fm run --stall-disk MB` and `--stall-procs N` stop a fake agent that only writes junk or forks, and the receipt names the resource.

- **Detect the user's own edits during a task** — FEATURE — value 4 — effort M — risk med — category: proof integrity
  Why: assumption: tasks run while the user also edits in an IDE, which the "second live session" and lane-throttle ideas don't cover. Q: whose hands changed the tree between the plan and the proof?
  Done when: a test edits a tracked file by hand mid-task, and the finish receipt lists it as "changed outside the session" and marks the proof as run on a mixed tree.

- **Note branch switches and rebases under an open task** — FIX — value 3 — effort S — risk low — category: task state
  Why: the pack lists no check that the checkout still matches the task's start tree. Q: what if the user checks out another branch or force-pulls mid-task?
  Done when: switching branches under an open task makes `fm status` show "task started on X, you are on Y" and `fm task finish` refuses to prove against the wrong tree.

- **Calibrate characters-to-tokens in `fm burden` from transcript usage** — FIX — value 3 — effort M — risk low — category: gauge accuracy
  Why: T-2667 reports injected characters, but the user feels tokens. Q: what is the ratio per source (code, prose, CJK, JSON)? A fitted ratio can be checked against transcript usage deltas.
  Done when: `fm burden --by-source` prints an estimated token column with the fitted ratio, and a test shows the estimate is within 20% of recorded usage on fixture transcripts.

- **Rate-limit capture wakes and log the wakes that were undone** — FIX — value 2 — effort S — risk low — category: triage
  Why: T-2656 wakes a deferred task when a near-duplicate is captured. Q: can the wake ping-pong or storm if the user re-defers it? Assumption: nothing bounds wakes per task.
  Done when: a test captures five near-duplicates of one deferred task, and the task wakes once, with the other four logged as "already awake".

- **Flag sync-folder conflict copies of ledgers** — FIX — value 2 — effort S — risk low — category: ledger resilience
  Why: the pack covers torn writes and tmpfs, not file-sync tools. Q: what if the state dir sits under Syncthing or Dropbox, which creates `*.sync-conflict-*` copies? Assumption: possible on a multi-machine setup.
  Done when: `fm doctor` warns on any conflict-pattern sibling of a ledger or on a state dir inside a known sync root.

- **Wild: Ask a cold child to guess each flag's meaning from its name alone** — FEATURE — value 3 — effort S — risk low — category: naming ambiguity — wild
  Why: the three-phrasings grounding idea in T-2659 is about briefs, and the same ambiguity hides in flag names. Q: does `--stall-usd N` read as "dollars since the last close" or as "total dollars"?
  Done when: a nightly exam has a tool-less child write one sentence per flag from the name and help alone, and any sentence that contradicts the code is listed.

- **Wild: Environment bingo, where a child invents a hostile first-day host** — FEATURE — value 3 — effort M — risk med — category: install exam — wild
  Why: the user's host (hardened kernel, tmpfs state, no `claude`) is itself unusual. Q: what is the weirdest plausible host? The child draws shell, locale, proxy, read-only home and NixOS, and `install.sh` plus `fm doctor` run in a container.
  Done when: ten random profiles run nightly, and each outcome is pass, or a failure with a named cause.

- **Wild: Cap replay ("what would 0.5×, 1× and 2× have done") before any new limit ships** — FEATURE — value 3 — effort S — risk low — category: limit calibration — wild
  Why: T-2669's cap has no evidence-based default. Q: over the last 90 days of the ledger, how often would each limit have fired, and was each stop right? The result is a three-row table, not a tuned default.
  Done when: `fm run --stall-usd N --dry-history` prints how many past runs would have stopped, and when.

- **Wild: Add a "things you'll ask me within a week" card at Mission close** — FEATURE — value 2 — effort S — risk low — category: blind-spot forecast — wild
  Why: the missed-ask list (T-2656 to T-2669) shows asks cluster around a just-shipped feature (a cap, a gauge, a guard fix). Q: what will the user ask about the thing built today? A child proposes five, and the real asks are scored later.
  Done when: each Mission close files five predicted asks, and a later check marks hits and misses.

Next question: which of Foreman's numeric defaults (caps, windows, thresholds) were picked without ever being run against the user's own history?
Next question: when the user's hand and Foreman's hand both change the same thing (tree, queue, ledger), which side does each reader trust?
