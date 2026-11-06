# Brainstorm — lens: reliability

- **Fuzz every path-reading verb with hostile names** — FIX — value 4 — effort M — risk low — category: robustness
  Why: assumption: the map covers 2,129 files, and filenames, branches and paths with invalid UTF-8, newlines, leading dashes or 4 KB length are never exercised. A crash in the guard, `fm map` or a ledger write on one odd name fails silently or open.
  Done when: a fixture repo with 10 such names passes `fm map`, `fm guard`, a ledger write and the web UI render with no traceback and no corrupted ledger line.

- **Cap spawn depth for Foreman children** — SECURITY — value 4 — effort S — risk low — category: agents
  Why: assumption: headless `claude -p` children load the same plugin hooks, so a hook that calls `fm` that spawns a child can recurse and spend without bound. A depth counter in the environment is cheap and fits "lean and safe".
  Done when: a test with `FM_DEPTH` at the cap makes the spawn refuse with a one-line `Next:` and a ledger note, and a normal child runs unchanged.

- **Count doctor checks run against checks registered** — FIX — value 4 — effort S — risk low — category: measurement
  Why: the pack says earlier ideas mark "could not run" for proofs, but `fm doctor` itself isn't covered. A check that raises should show as red, not vanish and leave a clean "all clear".
  Done when: injecting an exception into one check makes `fm doctor` print `N-1 of N checks ran` plus a red row for it and exit nonzero.

- **Pin the drive to one code generation and re-exec at task boundaries** — FIX — value 4 — effort M — risk med — category: unattended
  Why: assumption: a multi-day `fm drive` imports modules once. A mid-run `fm ship` or upgrade leaves old code driving new state, a skew nothing detects.
  Done when: touching the installed lib during a fake drive makes it re-exec after the current task closes and log `code changed: restarted`, with no task lost.

- **Fall back along a ranked model chain when a pinned ID stops answering** — FEATURE — value 4 — effort M — risk med — category: agents
  Why: a daily probe of pinned model IDs is already filed, but a failed probe only reports. An overnight drive should drop to the next model and say so rather than die at 3am.
  Done when: with the primary ID stubbed to 404, a drive task completes on the fallback and the receipt names both models and the reason.

- **Dedupe hook-decision ledger writes by event key** — FIX — value 3 — effort S — risk low — category: ledger
  Why: assumption: a host that retries or replays a hook call (timeout, resume, compaction) records the same decision twice. That inflates rates in `fm outcomes` and the conservation checks.
  Done when: replaying one hook payload twice yields one ledger line and a `dup` counter, and the rates are unchanged.

- **Merge lanes in a scratch worktree before touching the live tree** — FIX — value 4 — effort M — risk med — category: agents
  Why: the mission brief says an L stays in the main thread while S/M lanes merge in mission order. A failed or conflicting merge into the live tree leaves the user's checkout half-merged. Assumption: merges are done in place today.
  Done when: a forced conflict leaves the live tree byte-identical and `fm lanes` shows the lane as `blocked: conflict` with the scratch path.

- **Time-bound lanes by progress, not wall clock** — FEATURE — value 3 — effort M — risk low — category: agents
  Why: T-0831 (salvage from capped children) covers lanes that hit a cap. A lane that is alive but making no tool calls or diffs for N minutes burns budget without tripping any cap.
  Done when: a stub lane that stalls 10 minutes is nudged once, then stopped with its partial diff saved, and the stall reason appears in `fm lanes`.

- **Render the web UI from a last-good snapshot with a visible stale banner** — FEATURE — value 4 — effort M — risk low — category: ui
  Why: "ui" is thin. If a ledger read fails (torn tail, damaged line), a blank page looks the same as "nothing happened". Earlier ideas stamp ages on packs but not on UI reads.
  Done when: corrupting the ledger tail still serves the previous snapshot with a banner `as of 14:02, ledger unreadable: fm fsck`.

- **Tie pane motion to a real heartbeat** — FEATURE — value 3 — effort S — risk low — category: ui
  Why: earlier ideas animate the stage rail to explain state. A spinner that keeps moving after the drive died is a false liveness signal worse than no motion.
  Done when: killing the drive process freezes every animated element within 5 seconds and dims it, checked in a frame test.

- **Offer a one-step revert after a config change followed by a red doctor** — FEATURE — value 3 — effort S — risk low — category: config
  Why: assumption: `fm config` edits aren't versioned. Config is the commonest self-inflicted break, and `fm doctor` already knows when state turns red.
  Done when: a config edit that turns a doctor row red makes `fm doctor` print the exact `fm config --revert` command, and running it restores green.

- **Wild: Ship a misbehaving fake host for every child-spawning test** — FEATURE — value 4 — effort M — risk low — category: testing
  Why: wild. One stub `claude` with a fault menu: truncated JSON, hung stdout, exit 0 with empty output, ignoring SIGTERM, ANSI noise. The drive and `fm ideas` run against it in CI. T-0336's blocked live checks get a stand-in.
  Done when: each of the 5 faults ends in a labelled ledger outcome within its deadline, with no hang.

- **Wild: Declare a worst case for every verb** — FEATURE — value 3 — effort M — risk low — category: legibility
  Why: wild. Each verb's help carries a tested line such as `worst case: may hang ≤30s, writes only .fm/, spends $0`. Rows that can't be filled expose verbs nobody has bounded, and the user can see the blast radius.
  Done when: a test fails for any verb whose help lacks the line or whose observed worst case under fault injection exceeds it.

- **Wild: Run `fm doctor --as-of DATE` over the ledger** — FEATURE — value 3 — effort L — risk med — category: diagnosis
  Why: wild. Replaying checks against past ledger snapshots finds the day a row first went red, so a regression gets a date and a commit range instead of a vague "it's been off for a while".
  Done when: `fm doctor --as-of 2026-10-20` prints that day's row states, and a planted regression is dated within one day.

Next question: which Foreman writes (ledgers, config, installed copy) can a second concurrent session or a host retry corrupt, and what would the user see?
Next question: which of Foreman's own reliability checks run only when the user types a verb, and which run with nobody watching?
