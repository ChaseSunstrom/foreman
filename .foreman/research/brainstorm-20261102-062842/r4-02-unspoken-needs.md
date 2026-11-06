# Brainstorm — lens: unspoken needs

- **Run a compressed-week tick soak on a virtual clock** — FEATURE — value 5 — effort M — risk low — category: self-trigger measurement
  Why: the gap is "a week of live ticks graded, waits on the user's install". The user's steers keep saying "don't block on me." A recorded or synthetic week replayed at 1000x through the real dispatcher, with an injected clock, yields due-time, catch-up and double-tick results with no timer. Listed ideas mention replay, but none make the soak a graded exam line.
  Done when: `fm exam` prints a "tick-soak" line with fires due, fired, late, duplicated and missed for 7 simulated days, run on this machine with no systemd unit installed.

- **Grade each fire by whether the user's next action touched its output** — FEATURE — value 5 — effort M — risk med — category: outcome signal
  Why: the user acts on morning notes and filed tasks without checking them (an earlier question). The unspoken need is knowing whether self-started work was used. Settle each fire from git, task and ledger events (kept, dropped, ignored in 3 days), not from clicks. assumption: ledgers carry the trigger origin on each self-filed task.
  Done when: `fm outcomes --by trigger` lists, per trigger, fires, kept, dropped and unseen, with a denominator line.

- **Open every session with "ticks that would have run while you were away"** — FEATURE — value 4 — effort S — risk low — category: session path
  Why: with no install, the only free clock is session edges. Computing what was due since the last session and running it lazily (with lateness recorded) gives live data now and shows the user what a timer would add.
  Done when: a session start after a 2-day gap prints one line naming the jobs run and their lateness, and the lateness ledger gains rows.

- **Show the install counterfactual in the user's own minutes** — FEATURE — value 4 — effort S — risk low — category: install pitch
  Why: the install is a "yes" the user keeps not giving; the need behind it is knowing whether it pays. Use the lateness ledger and unattended-gap history to say "a timer would have started X hours earlier on N occasions".
  Done when: `fm doctor` replaces the generic missing-timer WARN with a figure computed from the ledger, or says "insufficient data" with the count needed.

- **Run a transient 20-second systemd timer probe, not an install** — FEATURE — value 4 — effort S — risk med — category: scheduler proof
  Why: the host has systemd and the install is the blocked step. A transient `systemd-run --user --on-active=20s` unit vanishes on its own and proves the chain (environment, linger, interpreter, library) without a permanent yes. assumption: user session bus is reachable; it may not be on this hardened kernel, in which case the probe records the cause.
  Done when: `fm tick probe` fires a unit that writes a beat file within 60 seconds and reports pass, or names the exact reason it could not run.

- **Add a null-tick control arm to the exam** — FEATURE — value 4 — effort M — risk low — category: measurement
  Why: no grade of self-triggering means anything without a "no tick" baseline (earlier gens flagged control arms). Same planted-event week replayed with the tick disabled, scoring how late the user's own session noticed each event.
  Done when: the exam line shows tick arm versus null arm notice-latency on identical planted events, with the difference.

- **Block grades whose inputs Foreman wrote itself** — FIX — value 4 — effort S — risk low — category: gauge honesty
  Why: standing rule: weakness-finding uses signals Foreman didn't author. A tick grade built from tick-filed tasks is circular.
  Done when: `fm genesis check` fails a tick gauge whose input rows are all from Foreman-origin events, naming the gauge.

- **Say "checked, nothing found" so quiet reads as alive** — FEATURE — value 3 — effort S — risk low — category: liveness
  Why: a quiet tick looks identical to a dead one. The unspoken need is trust that silence is health.
  Done when: each tick writes a one-line outcome (ran, nothing due, skipped with reason) and `fm status` shows the last one with its age.

- **Mine existing unattended resumes as free live ticks** — FEATURE — value 3 — effort M — risk med — category: evidence
  Why: usage-limit waits and drive resumes already happen unattended. Counting them as live data gives a real week now. assumption: they're logged with timestamps.
  Done when: a report lists the past 30 days' unattended starts with cause and lateness, or states how many were logged.

- **Add an "oops" undo for everything self-started in the last N hours** — FEATURE — value 4 — effort M — risk med — category: trust
  Why: the first hour after a Foreman mistake has no verb (an earlier question), and self-started work is where the user is least watching.
  Done when: `fm oops 6h` lists self-started branches, tasks and notes from 6 hours and reverts or closes them after one confirmation.

- **Wild: Let the user's first prompt of each local day be the daily tick** — FEATURE — value 3 — effort S — risk low — category: wild
  Why: assumption: most days start with a prompt; this needs no timer. wild.
  Done when: the first prompt after local midnight runs due daily jobs once and records "source: prompt".

- **Wild: Replay last Friday evening as a ghost shift** — FEATURE — value 3 — effort M — risk low — category: wild
  Why: the user can see what the tick would have done to a real, remembered moment. wild.
  Done when: `fm tick ghost --since fri` prints a timeline of would-be fires against the real git log with no writes.

- **Wild: Run the tick daily from a GitHub Actions workflow on a log branch** — FEATURE — value 3 — effort M — risk high — category: wild
  Why: off-machine clock with no install on the user's box; the repo already has CI. Needs an explicit setting since it sends data out. wild.
  Done when: with the setting on, a scheduled workflow commits a beat file to an orphan branch and `fm doctor` reads it; with it off nothing leaves the machine.

- **Wild: Hold out one in five fires as a causal control** — FEATURE — value 3 — effort M — risk med — category: wild
  Why: shows whether fires change outcomes rather than just happen. wild.
  Done when: held-out fires are logged as "withheld" and the outcome report compares kept rates between fired and withheld.

Next question: What does the user do when a self-started result is wrong, and which of those steps have no verb or receipt?
Next question: Which tick job has never produced output the user kept, and would they rather lose it than keep paying for it?
