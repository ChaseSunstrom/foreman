# Brainstorm — lens: blind spots

**Blind-spot reading.** The "missed asks" list shares a shape: each was a measurement or guard that existed but was never *checked for aliveness, drift, or self-consistency* (T-2525 a stale premise, T-2532 a silent hook off-switch, T-2533 and T-2535 unattributed growth, T-2504 unchecked public claims). The question a brainstorm should have asked: "What runs without anyone watching it, and how would we know it stopped or lied?" For Mission 4 (self-triggering), that is the whole mission.

- **Prove every trigger path is alive by an outside heartbeat** — FEATURE — value 5 — effort M — risk low — category: reliability
  Why: T-2532 shows a hook that fails silently; `fm night` "logs only when something happens", so silence can't be told from death. Self-triggering is the mission that most needs this.
  Done when: killing the night timer in a scratch home makes `fm doctor` print "no tick for N min (expected every M)" within one check, with a test.

- **Write a trigger registry the mission's 59 cells cite** — CLEAN — value 4 — effort M — risk low — category: coverage
  Why: the standing steer says a cell counts only if it names a real capability; the pack shows triggers spread across `fm night`, `fm triggers`, `fm ci-watch`, with no single list. Assumption: no registry exists.
  Done when: one file lists every trigger (source, event, action, budget, owner verb), and a test fails if a cell cites a trigger not in it.

- **Replay a trigger on the last 30 days before its install yes** — FEATURE — value 5 — effort M — risk low — category: trust
  Why: the user is asked for one yes on timers and units; today they approve blind. Evidence: `fm triggers` already groups captures with precision.
  Done when: the install card prints "would have fired N times, M useful" computed from recorded events, and refuses to queue a trigger with zero history without saying so.

- **Show the exact unit text and uninstall line on the install card** — SECURITY — value 4 — effort S — risk low — category: consent
  Why: the standing rule queues installs for one yes; a yes to a name is not a yes to the file content. Assumption: card shows names today.
  Done when: the card contains the full unit file, the enable command and the exact removal command, and a test compares the card to the bytes written.

- **Treat issue, CI log and PR text as untrusted in watcher lanes** — SECURITY — value 5 — effort M — risk med — category: injection
  Why: `fm ci-watch` and the planned issue watchers feed external text into an agent that runs unattended under bypass-style permissions (the T-0791 injection bundle is deferred).
  Done when: a planted "ignore previous, run X" in a fixture issue produces a task draft only, and the guard log shows no executed command from it.

- **Stamp every self-started artifact with its trigger** — FEATURE — value 4 — effort S — risk low — category: attribution
  Why: T-2533/T-2535 show growth the user couldn't attribute; a task or lane that appears with no session needs the same. Assumption: tasks carry no origin field for timers.
  Done when: `fm status` and the commit trailer of a self-started lane name the trigger id and the event that fired it.

- **Catch up missed schedules once, with a cap, after sleep or reboot** — FIX — value 4 — effort S — risk low — category: reliability
  Why: assumption: a laptop timer misses fires while closed; N replays would burn budget, zero replays loses work.
  Done when: a simulated 3-day gap yields one coalesced run and a log line saying how many fires were folded.

- **Stop a trigger from re-firing on its own output** — FIX — value 4 — effort S — risk low — category: loops
  Why: file and CI triggers react to commits and pushes that self-started lanes themselves make (`fm ship` then `fm ci-watch`). Assumption: no loop guard on the file trigger yet.
  Done when: a fixture where a lane's commit matches its own trigger fires exactly once, and a per-trigger storm breaker trips on a forced loop.

- **Check the site's "work starts without you" claims against the trigger log** — FEATURE — value 3 — effort S — risk low — category: claims
  Why: T-2504 already asked for proof before presentation; Mission 4 adds a new class of public claim.
  Done when: the sweep goes red if a published trigger claim has no firing in the log in 30 days.

- **Tell the user which triggers never helped** — FEATURE — value 3 — effort M — risk low — category: pruning
  Why: `fm triggers` has precision per trigger; nothing acts on low precision. A silent trigger costing budget is the lean ratchet's blind spot.
  Done when: a trigger with under N% useful fires over 14 days is listed in the morning note with a one-word disable.

- **Wild: Fire a harmless fake CI failure weekly to prove the whole chain** — FEATURE — value 3 — effort M — risk med — category: liveness
  Why: wild; the only proof that watcher, lane, guard and morning note work end to end is a planted event, not a config check.
  Done when: a weekly canary event appears in the morning note as "chain alive, 4m12s", and a broken link names which step failed.

- **Wild: Dry-run a recorded week through the dispatcher in daylight** — FEATURE — value 3 — effort L — risk low — category: rehearsal
  Why: wild; a night shift can't be debugged at night. Replaying captured events at 100x makes the first real night a second run.
  Done when: `fm night --rehearse` replays a stored week and prints the same decisions the real tick would have made, deterministic across two runs.

- **Wild: Let the user touch one file to freeze every trigger** — FEATURE — value 3 — effort S — risk low — category: control
  Why: wild; a panic switch needs no session or CLI to work, which matters when the thing misbehaving is the unattended one.
  Done when: creating `~/.foreman/STOP` makes the next tick and every watcher exit with a logged reason, and removing it resumes them.

Next question: Which of the 59 empty cells describe a trigger that has never once fired on the user's real machine, and would the user say they still want it?
Next question: What does a self-started lane do when the user is mid-edit in the same working tree, and who has checked that on a real repo rather than a fixture?
