# Brainstorm — lens: night shift: what runs unattended while the user sleeps and leaves proven, ranked, ready-to-merge lanes by morning

- **Order the shift so a kill at any hour leaves value** — FEATURE — value 4 — effort S — risk low — category: scheduling
  Why: assumption: the existing ideas pick *which* findings to run (knapsack, cap), not their order. A usage cutoff or crash at 3am can strand the best lane half-proven.
  Done when: given a fixture queue and a kill at a random point, the journal shows at least one merge-ready lane, and lanes ran cheapest-proof-first among equal-value ones.

- **Fork on a blocking question and let the user pick in the morning** — FEATURE — value 4 — effort M — risk med — category: unattended
  Why: the pack's lanes park on `fm answer` and the user drops or steers often, so a lane that stalls at 1am wastes the rest of the night. Assumption: most questions have a plausible default branch.
  Done when: a lane that asks a question continues on its default branch, and the card shows both outcomes labeled by answer, with one key to choose.

- **Probe the model with a known-answer canary between lanes** — FEATURE — value 4 — effort S — risk low — category: reliability
  Why: provider-incident ideas exist, but a silently degraded model gives plausible junk and the proof gate may not catch weak fixes. Assumption: a planted one-file bug with a fixed fix can be run cheaply.
  Done when: a canary that fails twice halts new lanes, and the card says "paused at 02:40, model failed canary".

- **Make parallel lanes collision-proof** — FIX — value 4 — effort M — risk med — category: lanes
  Why: `PARALLEL_MAX 3`, and flake finders exist, so lanes sharing ports, temp dirs or a test DB create false reds. Those would be mis-filed as flakes.
  Done when: three lanes on a fixture that binds a fixed-port server and a shared sqlite file all pass, each with a private port range, `TMPDIR` and DB name.

- **Close the permission gaps before bedtime** — FEATURE — value 4 — effort M — risk low — category: unattended
  Why: `T-0335` (ask grants on other CLIs) shows approval prompts are a known stall. Assumption: required tools and paths can be predicted from the finding kind.
  Done when: at queue time each lane gets "will need: X" and lanes needing an ungranted tool are parked with a reason, so none stalls at an approval prompt overnight.

- **Auto-stage proven lanes onto a `night/` branch by earned trust** — FEATURE — value 4 — effort M — risk med — category: landing
  Why: the pack's morning-card ideas end at "one key to land". Per-kind accept history could let kinds the user always accepts arrive pre-staged. Main is still never touched.
  Done when: after N accepted lanes of a kind, new ones of that kind appear on `night/` with a one-command fast-forward, and one reject resets that kind to card-only.

- **Cap the unreviewed pile and shrink the shift when it grows** — FEATURE — value 4 — effort S — risk low — category: pacing
  Why: assumption: if the user skips the card for days, stale lanes rot and cost money. Existing cap ideas count findings per day, not unread lanes.
  Done when: with 5 unreviewed lanes (the default) the next shift runs only a re-prove of old lanes, and the card says why.

- **Judge stalls on awake time so suspend isn't a stall** — FIX — value 3 — effort S — risk low — category: reliability
  Why: stall ideas use transcript growth and a monotonic clock, but a laptop that suspends mid-shift makes a lane look hung or burns its timeout. Assumption: the shift can run on a laptop.
  Done when: a test that simulates a 40-minute suspend gap (boot-time clock jumps, monotonic doesn't) kills no lane and journals "resumed after suspend".

- **Show how a lane collides with the user's dirty checkout** — FEATURE — value 3 — effort S — risk low — category: landing
  Why: lanes live in worktrees, but the user may leave uncommitted edits. Morning "land" can fail or clobber them. Assumption: `git status` at shift start and end is cheap.
  Done when: a card row flags "touches foo.py, which you have edited and not committed", and a test with a dirty-file fixture shows the flag.

- **Budget disk and share dependency caches across lane worktrees** — PERFORMANCE — value 3 — effort M — risk low — category: resources
  Why: 3 parallel worktrees × `node_modules` or cargo targets over a night can fill a disk. Reflinked fixtures are mentioned, but not lane dependency trees.
  Done when: a shift on a fixture with a 500 MB dependency tree uses under 1.5× that in total and reaps finished worktrees.

- **Wild: Keep the machine quiet with a noise budget** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: wild. A laptop at full fan next to a bed ends the night early. Cap lane CPU by cgroup and a thermal ceiling, and the shift trades a little speed for silence.
  Done when: with `fm night --quiet`, sustained CPU stays under the set percent, and the card shows time lost to the cap.

- **Wild: Rehearse the user's first five morning commands at dawn** — FEATURE — value 3 — effort M — risk med — category: trust
  Why: wild. Learn what the user runs first (pull, test, build) from shell history and run those on `night/` an hour before wake, so the card can say "your morning is green".
  Done when: the card shows each command's result on the staged branch, and a failing one blocks the "all good" banner.

- **Wild: Hand an unfinished shift to a teammate's machine at their dawn** — FEATURE — value 2 — effort L — risk high — category: team
  Why: wild. Reuse state-capsule and handoff ideas so a shift that ran out of budget at 4am finishes where it's daytime. Assumption: a shared repo and consent.
  Done when: a capsule exported on machine A resumes on B at the exact stage, with a journal line on both.

Next question: When the user finally opens the morning card, how long do they take per row, and does that attention time predict which kinds of lane they trust?
Next question: What does a shift leave behind that is expensive to undo (installed packages, caches, branches), and who cleans it up if the user never opens the card?
