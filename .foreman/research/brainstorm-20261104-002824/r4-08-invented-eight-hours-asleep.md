# Brainstorm — lens: invented: eight hours asleep

- **Scope a steer to the night** — FEATURE — value 4 — effort S — risk low — category: steers
  Why: the pack's steers are all permanent (e.g. "no fm ask prompts"), and "Scope steers to paths and stacks" has no time axis. Assumption: users want bedtime-only rules such as "don't touch the installer tonight".
  Done when: `fm night --steer "don't touch install.sh"` blocks an edit at 03:00, is gone from the steer list after wake time, and leaves a ledger line recording its expiry.

- **Guard half-asleep replies** — SECURITY — value 4 — effort M — risk low — category: devices
  Why: assumption: phone pings ("wake-nobody pager", decision sheets) will sometimes get a reply from bed. A one-character "y" at 03:10 shouldn't spend a push grant.
  Done when: a reply arriving inside the sleep window to a card with an irreversible action is echoed back and acted on only after a second confirmation at least 5 minutes later; test with a scripted reply.

- **Print a night egress receipt** — SECURITY — value 4 — effort S — risk low — category: privacy
  Why: the pack has "mark grounding steps local or sent" and a per-release outbound-host diff, but no per-night record of what left the machine unattended.
  Done when: the morning card has one line, "sent: 0 bytes beyond the orchestrator" or a list of host, bytes and reason, built from a wrapper that logs every outbound call; a planted call to an unlisted host appears in it.

- **Stop the night on thermal or disk limits** — FIX — value 4 — effort M — risk med — category: devices
  Why: the 27B runs for hours unattended on the user's server. Assumption: nothing watches GPU temperature, GPU power or disk fill. The pack's resource-forecast idea covers disk growth, not hardware safety.
  Done when: a fake sensor reading above the limit pauses local-model jobs, logs "paused: thermal 91C", and resumes under a lower threshold; the cause shows on the morning card.

- **Run a night CI on the user's hand-made commits** — FEATURE — value 5 — effort M — risk low — category: verification
  Why: the user's hand edits bypass Sampo's gates. "Prove the user's CI can go red" and "Detect the user's own edits" exist, but nothing runs the full gate on the day's non-Sampo commits while the user is away.
  Done when: a commit made outside any task is tested on a clean clone overnight, a planted red is auto-bisected to its commit, and a finding is filed with the failing command.

- **Draft doc patches for the day's landed behaviour** — FEATURE — value 4 — effort M — risk low — category: docs
  Why: docs is a thin area. The existing ideas check docs against code, but none writes the patch. Assumption: the 27B is good enough to draft one, provided every `fm ...` example it quotes is executed in a scratch home.
  Done when: for a commit that adds a flag, the morning card links an unapplied patch to MASTER.md/CHANGELOG whose quoted commands all exit 0 in a scratch home. A patch with a failing quote is not offered.

- **Take quiet-machine benchmark readings at 04:00** — PERFORMANCE — value 3 — effort S — risk low — category: performance
  Why: `bench_hooks.py` is a ship gate. Daytime contention makes its numbers noisy, and "normalise by a reference loop" only partly fixes that.
  Done when: a nightly idle-machine run appends p50 and p95 for each hook to a series, and a 20% regression raises a finding that daytime noise alone would not.

- **Show a 3 a.m. visitor card and yield at once** — FEATURE — value 3 — effort M — risk med — category: devices
  Why: assumption: the user sometimes appears mid-night. "Throttle while active" and "hand the GPU back" exist, but nothing greets them with state or yields instantly.
  Done when: the first keypress in the sleep window prints at most 10 lines (sealed plan, current lane, last close, a "yield" key). Local model jobs stop within 5 seconds of that keypress, and the sealed plan resumes after 10 idle minutes.

- **Retry not-yet items when their blocker predicate flips** — FEATURE — value 4 — effort M — risk low — category: genesis
  Why: the standing rule says every Seed retries not-yet.md items that a new capability may unblock, and a failed spike gets 2 or more approaches. Today that retry is manual and per-Seed.
  Done when: each not-yet entry carries a one-line `unblocks-when:` predicate (a verb exists, a file exists, or a model is served). On a night when one turns true, a lane tries a new approach, and the result is recorded against the entry.

- **Reap whatever the night left running** — FIX — value 3 — effort S — risk low — category: unattended
  Why: T-2900/2901/2873 show the drive being fooled by dead or lingering agents. Assumption: stray shells and model clients can also outlive the plan and eat the morning's RAM and GPU.
  Done when: at wake, every process the drive started that is still alive is listed by owner task, those past their deadline are terminated, and the card says "left running: none".

- **Wild: Wake the machine in phases** — FEATURE — value 3 — effort M — risk med — category: devices
  Why: wild; assumption: the workstation can suspend and the night has idle stretches (quota waits, a 3-minute model switch). The idea is `rtcwake` to sleep through stalls and wake at phase boundaries.
  Done when: in a dry-run on a fake clock, a sealed 8-hour plan produces a wake schedule where the machine is suspended for at least 40% of the idle minutes, and no phase starts late.

- **Wild: Shadow the user's hand overnight** — FEATURE — value 5 — effort L — risk med — category: local models
  Why: wild; builds on the "delegation frontier" and "replay old asks" ideas, but uses the user's own hand-made commits. Assumption: commit messages are close enough to asks to serve as a test set.
  Done when: for 20 hand commits, the 27B tries each from its message in a scratch worktree, and the morning card says "unaided on N of 20", with a file-level diff match against the user's real change.

- **Wild: Show a night strip of eight embers on the site and in the pane** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: wild; fits the illustrated forge look and the rule that the site follows Genesis. One ember per hour, with brightness set by closes and colour by stop reason. It shows counts only, never user text.
  Done when: `site/genesis` data holds eight numbers per night. The page renders the strip with reduced motion respected, and a test fails if any free-text field appears in the data.

- **Wild: Mark each night's work "unwitnessed" until a human has seen it** — SECURITY — value 3 — effort S — risk low — category: trust
  Why: wild; assumption: the user can't tell which commits no human ever looked at. This extends the existing "not yet verified by anyone but me" count to everything landed while asleep.
  Done when: each night-made commit carries a trailer. `fm next` lists them as unwitnessed until the user opens the card or runs `fm seen`, and shipping them to main requires the flag to clear.

Next question: What is the shortest cold-start path to a trustworthy first night — what would a new user's first sealed plan include, and what would they need to see at 7 a.m. to run a second night?
Next question: Which part of the user's sleep window can be learned from ledger gaps alone, and how often is that estimate wrong (late nights, travel, naps)?
