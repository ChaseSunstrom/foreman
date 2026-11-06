# Brainstorm — lens: user value

- **Tell the user when a timer would add nothing** — FEATURE — value 4 — effort S — risk low — category: measurement
  Why: the gap is "waits on the user's install". Assumption: the user's session-start times can be read from transcripts. Replay the pending items against those real times and print the detection delay a timer would have saved. Say "don't install" when the gaps are short.
  Done when: `fm doctor` prints one line, "a timer would have started N of M due items on average H hours earlier", or "adds nothing" with the figures. A fixture of gaps under an hour yields the "adds nothing" verdict.

- **Record misses the user notices (`fm missed`)** — FEATURE — value 4 — effort S — risk low — category: measurement
  Why: assumption: precision can be graded from dismissals, but recall can't, because a trigger that never fired leaves no row. One sentence from the user, such as "CI went red at 14:00, nothing happened", becomes a false-negative row and a planted-event regression case.
  Done when: `fm missed "<text>"` appends a row, and `fm exam` includes it as a replayable scenario. The trigger report shows recall as hits ÷ (hits + misses).

- **Label every self-triggering claim with its evidence grade** — CLEAN — value 4 — effort S — risk low — category: honesty
  Why: the pack says self-triggering is "unmeasured until the end-of-run exam", and the proof-before-presentation steer applies. Each README, site and doctor claim carries one of: live, replayed, planted, unmeasured.
  Done when: the sweep goes red on a self-triggering claim with no grade, and a claim graded "live" with no live tick rows fails.

- **Auto-resolve a yes-card to its default by a date** — FEATURE — value 4 — effort M — risk med — category: autonomy
  Why: the standing rule is "never block on the user", and T-0325, T-0335, T-0337, T-0352 and T-0418 sit blocked. Each card names its default and a date. The next session edge applies the default through `fm decide --kind costly`, with a one-line undo. Irreversible or outward actions are never auto-resolved.
  Done when: a card past its date is resolved at the next session start and shows in the final report. An outward-action card stays open.

- **Show watched hours on a timeline strip** — FEATURE — value 3 — effort S — risk low — category: ui
  Why: without a timer, "watching" only happens inside sessions. Draw the last 7 days as a strip of watched versus unwatched hours on the status line and web UI. This is honest about the blind time, not just a trigger count.
  Done when: the web UI strip matches the tick and session ledger for a fixture week, and the unwatched share is printed by `fm doctor`.

- **Add `fm demo tick`, a sandbox first fire** — FEATURE — value 3 — effort M — risk low — category: onboarding
  Why: T-0862 and T-0863 defer a newcomer tour until the first-run guide proves insufficient. In a throwaway repo, plant a failing test and a due deferred task, run the session-edge tick, and show what it filed. The user sees self-triggering work with no install and no spend.
  Done when: the demo runs offline in under 60 seconds, leaves no state outside its temp dir, and ends with a one-line summary of what fired.

- **Export a redacted tick tape for bug reports** — FEATURE — value 3 — effort S — risk low — category: privacy
  Why: assumption: the tick log holds paths, branch names and commit text. A misfire is hard to report without sending those. `fm tick tape --redact` hashes paths and strips text, and the tape stays replayable on the virtual clock.
  Done when: replaying the exported tape reproduces the same fire decisions, and a grep for the fixture's secret strings and home path finds none.

- **Serve fire receipts as a local Atom feed (wild)** — FEATURE — value 3 — effort S — risk low — category: devices
  Why: the user reads receipts on a phone or in a feed reader without any outbound service. The web UI serves `/feed.atom` on loopback by default, and on the LAN only with an explicit setting and token. A QR code on the page pairs a phone.
  Done when: a feed validator accepts the feed, a loopback fetch lists the last 20 fires, and a non-loopback request without the setting is refused.

- **Pair machines by a heartbeat git ref (wild)** — FEATURE — value 3 — effort M — risk med — category: devices
  Why: assumption: the user has more than one machine, so one machine's silence could be reported by another's session. Each session writes a beat to a private ref, and the other says "laptop hasn't ticked in 9 days". The ref is opt-in and holds no content.
  Done when: with two clones and a stale beat, the second session prints the silence line. With the setting off, no ref is written.

- **Add a silent-day dividend (wild)** — FEATURE — value 3 — effort S — risk low — category: measurement
  Why: random hold-outs are in the earlier ideas, but the user's own choice of a quiet day is not. The user says `fm quiet today` and Foreman starts nothing. Afterwards it lists what it held back, and the user marks each item "missed it" or "didn't care".
  Done when: a quiet day starts no lane, and the next morning's card lists the held items with two-word answers. The answers feed the trigger's value score.

- **Leave a sealed note for a future condition (wild)** — FEATURE — value 3 — effort S — risk low — category: user value
  Why: assumption: the cheapest self-trigger for a human is a reminder. `fm leave "check the migration" --when "I next touch src/db"` or `--when 2026-12-01` surfaces at the matching session edge, no timer. It also gives the tick a user-authored event source to grade.
  Done when: the note appears once at the first matching edge and never again, and a path condition that never matches expires with a named reason.

Next question: which self-triggering result would the user act on without checking it, and what is the one-line external command that would verify it?
Next question: what does a week of the user's own session-start timestamps predict about detection delay, before any tick runs?
