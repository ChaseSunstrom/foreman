# Brainstorm — lens: night shift: what runs unattended while the user sleeps and leaves proven, ranked, ready-to-merge lanes by morning

- **Bookend the night with `fm goodnight` and `fm goodmorning`** — FEATURE — value 4 — effort M — risk low — category: ritual
  Why: assumption: the bedtime checks are separate asks, and the user will not run them one by one. `goodnight` snapshots a dirty checkout to a private ref. It also checks that credentials outlive the planned shift, that power is connected, and that the machine will not suspend. It ends by printing the departure card. `goodmorning` shows the diff against the snapshot, so lanes cannot silently collide with the user's half-done work.
  Done when: with a dirty tree, `fm goodnight` creates the ref and prints the card. `fm goodmorning` after a simulated shift lists exactly the files changed overnight.

- **Land the morning as a merge train with bisect on red** — FEATURE — value 5 — effort M — risk med — category: landing
  Why: the pack shows lanes, a gate lock and the `fm night` queue job, but no step that lands several proven lanes together. Individually green lanes can interact. `fm morning land` merges lanes in ranked order and runs the gates after each. On the first red it bisects to the culpable lane, parks it and carries on.
  Done when: in a fixture, two lanes that are green alone and red together land with the second parked and named, and main stays green.

- **Pick the morning by minutes available** — FEATURE — value 4 — effort S — risk low — category: review
  Why: assumption: the user is short on time at 7am, and review is the real bottleneck. Each lane gets an estimated review time from diff size and proof type. `fm morning 10m` selects the highest-value set that fits, ordered by the printed formula.
  Done when: given lanes with known sizes, `fm morning 10m` outputs a set whose estimated total is at most 10 minutes. It is the maximum-value subset in a test.

- **Hunt the integrated tree for a second wave** — FEATURE — value 4 — effort M — risk med — category: finders
  Why: fixes unmask bugs, such as a masked test or a newly reachable branch. Lanes are proven against main, not against each other. After the lanes pile up on a throwaway `night/integrated` branch, the finders run again on that tree and file only what is new there.
  Done when: in a fixture where fixing bug A exposes bug B, the second wave files B and the first wave did not.

- **Split the night across projects by marginal yield** — FEATURE — value 4 — effort M — risk med — category: scheduling
  Why: the user works across several repos, and the exam grades never-seen repos. A single-project shift wastes budget where yield is low. One shift takes a total budget and splits it by each repo's recent acted-on rate. It keeps an exploration floor for repos with no history.
  Done when: with two repos of known yields, spend splits in the expected ratio and the new repo still receives its floor.

- **Stop the shift on a correlated infra failure** — FIX — value 4 — effort S — risk low — category: reliability
  Why: assumption: an expired login, a full disk, a 429 loop or a missing toolchain failing every lane burns the budget. Existing breakers cover dropped findings, not infrastructure. When N lanes fail with the same signature, the shift checkpoints, writes one cause line to the card and stops spawning.
  Done when: injecting the same auth error into 3 lanes halts the queue after the third. The card names the cause, and `fm run` resumes after a fix.

- **Leave a lead for tonight with `fm tonight "<hint>"`** — FEATURE — value 4 — effort S — risk low — category: steering
  Why: the user's own words repeatedly steer what they care about, but nothing carries "this parser looks off" to the hunter. The hint becomes a first-priority hunt with the lead in the prompt. Its outcome is reported per hint, so a hunch that proves nothing returns as a clear "not found, here is the ground I covered".
  Done when: a hint naming a planted bug in a fixture gets that bug hunted first, and a hint with no bug returns a "clean" receipt for it.

- **Burn expiring headroom, not idle budget** — PERFORMANCE — value 3 — effort M — risk low — category: spend
  Why: the pack has pacing and refusal to start a queue that cannot finish before reset, but nothing says to use allowance that will otherwise lapse. Shift size is set from remaining weekly headroom and the time to reset, with a hard cap. The surplus is spent on lower-ranked proven findings.
  Done when: with simulated headroom of $X and 12h to reset, the planned shift spends within 10% of the target and never exceeds the cap.

- **Yield to the user's return** — FEATURE — value 3 — effort S — risk low — category: presence
  Why: assumption: the user sometimes comes back at 2am. Existing ideas freeze on a key, but nothing reads presence. On the logind idle hint going false, lanes pause with SIGSTOP (not killed), and a partial card is ready. They resume when the machine idles again.
  Done when: toggling the idle hint pauses all lane PIDs within 5s and resumes them, with no lane lost.

- **Use the project's real CI as an independent witness** — SECURITY — value 3 — effort M — risk med — category: proof
  Why: a lane's proof is run by the same machine that made the fix. With an explicit per-project setting, proven lanes are pushed to a `night/*` ref on the user's own remote, and the card shows CI's verdict beside Foreman's. Nothing is pushed without that setting, because a push is outward-facing.
  Done when: with the setting off, no push happens. With it on, the card shows a CI status for a pushed lane.

- **Rotate focus by weekday from a per-project recipe** — FEATURE — value 2 — effort S — risk low — category: coverage
  Why: assumption: one flat hunt repeats the same ground. `night.toml` maps weekdays to finder mixes, such as a flake soak on Monday and dependency trials on Tuesday. The default rotates through the finder kinds.
  Done when: two consecutive simulated nights run different finder sets, and the card says which recipe ran.

- **Wild: Set the shift's deadline from the user's real alarm** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: wild, assumption: an alarm time is readable from a calendar file or a phone link. The shift reads it, plans backwards, and finishes re-proving 20 minutes before it, so the card is fresh when the user wakes.
  Done when: with a fake alarm at 06:30, the last lane starts no later than the computed cutoff and the card timestamp is no later than 06:10.

- **Wild: Replay the night as a 20-second timelapse** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: wild, evidence: the tower graph page already exists. Lanes grow as branches, proofs flash green, dropped findings fade, and the morning card embeds the clip. It makes the night legible and is something to show others.
  Done when: `fm morning replay` renders a self-contained HTML clip from the night's journal with one frame per lane event.

- **Wild: A dream pass paints a smell heatmap for tomorrow's hunters** — FEATURE — value 3 — effort L — risk med — category: finders
  Why: wild, assumption: a small local model with leftover free compute can read the whole repo at night. It writes per-function "feels wrong" scores into an overlay on `fm map`. The next night's hunters sample by heat, and heat alone never admits a finding without a failing test.
  Done when: on a fixture with planted bugs, the hottest 10% of functions contain more planted bugs than a random 10%.

Next question: What does a user do at 7am when the card holds 14 proven lanes and 5 minutes, and does anything today tell them which two to land?
Next question: Which overnight failure would silently look like "clean" to the user, such as a dead model login or a missing toolchain?
