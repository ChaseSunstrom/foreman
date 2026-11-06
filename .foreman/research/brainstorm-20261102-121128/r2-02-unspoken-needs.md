# Brainstorm — lens: unspoken needs

- **Answer a re-pasted steer with the task that already did it** — FEATURE — value 4 — effort S — risk low — category: intake
  Why: three dropped asks were quoted steers the user had already seen acted on (T-2477, T-2480, T-2471). Each one cost a capture, a reading and a manual drop.
  Done when: capturing text that mostly quotes a stored steer files nothing and prints "already done by T-xxxx" with the steer date. A test with the T-2471 steer text passes.

- **Pick standing rules per task instead of injecting all of them** — PERFORMANCE — value 4 — effort M — risk med — category: context
  Why: the pack carries about 40 long steers, truncated mid-sentence. Most concern Genesis and are irrelevant to a one-line fix. Assumption: they are injected whole into sessions.
  Done when: an unrelated fix task's injected steer text shrinks at least 70% against the full list. A Genesis task still gets its steers, and no steer with a stored check is dropped silently.

- **Add a veto window to costly decisions Foreman made for you** — FEATURE — value 5 — effort M — risk med — category: autonomy
  Why: the rule "never block on the user, record it with fm decide --kind costly" means decisions pile up until the final report. By then, work built on them is expensive to reverse.
  Done when: each costly decision is listed in `fm next` with an expiry and a one-word reverse command. `fm decide --veto ID` reopens the affected tasks and records the veto, and an unvetoed decision shows as "stood" after expiry.

- **Print how many minutes of review today's work asks of you** — FEATURE — value 4 — effort M — risk low — category: legibility
  Why: the user steers hard on legibility ("proof before presentation", "plain receipts") and on the run advancing itself. Their attention is the scarce resource, but no output counts it. Assumption: each receipt can estimate its own reading time from its diff and proof size.
  Done when: the session-start note ends with "review: ~N min across M items, biggest first". Closing a task adds its share to that figure.

- **Draft the standing rule and its check from a user correction** — FEATURE — value 5 — effort M — risk med — category: steers
  Why: the user had to demand "every steer becomes a rule plus an automatic check". Corrections like the T-2583 "8+ characters" slip and the dropped-credential line still arrive as prose they must follow up on.
  Done when: a captured message tagged as a correction produces a proposed `fm decide --check` with its test, shown in the next session. The user approves it with one word, or it lapses unfiled.

- **Give removed flags a tombstone instead of an error** — FIX — value 3 — effort S — risk low — category: cli
  Why: the user ran `fm night --print-timer`, removed on purpose in T-2475, and it surfaced as a dropped ask. Their muscle memory and old docs outlive deletions.
  Done when: a removed verb or flag prints "removed in T-xxxx, use <replacement>" and exits non-zero. Intake treats the text as a command, not a task. A test pins `--print-timer`.

- **Scrub a pasted secret from every stored copy and say to rotate it** — SECURITY — value 4 — effort M — risk med — category: secrets
  Why: T-2624 stops redacted credentials reaching the inbox, but `MODELS_API_KEY=` and `JARVIS_TOKEN=` were pasted as plain text. Assumption: the originals still sit in transcripts, ledgers or captures.
  Done when: after a paste, a grep of Foreman's own stores finds no raw value. The session note says "a key was pasted; rotate it; N copies scrubbed".

- **Forecast the end of a long run** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: the user pauses the long-horizon exam until the end of the run, then asks for an end-of-run exam. They can't see how far off the end is. Gen-0's DONE-WHEN, empty coverage cells and open generations are all countable.
  Done when: `fm genesis eta` prints remaining cells, missions, generations and a cost range from past generations. It names the item that would end the run soonest, and it appears in the digest.

- **Generate a per-harness parity table from a conformance run** — FEATURE — value 4 — effort L — risk med — category: adapters
  Why: the standing rule says Foreman isn't Claude-specific, yet T-0335, T-0336 and T-0337 stay blocked and docs claim five agents. The user cares that claims match evidence.
  Done when: `fm doctor --parity` runs a scripted guard, plan and prove probe per installed harness. It prints supported, partial or untested per row and fails the site build if a README claim exceeds the table.

- **Wild: Interview the user for five minutes a week** — FEATURE — value 4 — effort M — risk low — category: user model
  Why: wild. The user model (fmforesight) already makes sealed predictions of their next steers. Its widest uncertainty is a question only they can answer, so ask it. Each answer becomes a steer with a check, and the quiz starts from the prediction it missed most.
  Done when: `fm interview` asks at most three questions drawn from the lowest-confidence predictions. Answers are stored as steers, and the next prediction record cites them.

- **Wild: Pre-mortem every long run** — FEATURE — value 3 — effort M — risk low — category: foresight
  Why: wild. Reversed rulings and misses recur: early-scored bets, templated coverage cells, false dones. Before a drive starts, Foreman writes "the three most likely ways this run embarrasses you" from past reversals, and the end report grades each one.
  Done when: each drive writes a pre-mortem file at start. The final report lists each prediction as happened, avoided or unknown.

- **Wild: Keep a changelog of the user's changing mind** — FEATURE — value 3 — effort S — risk low — category: steers
  Why: wild. Steers reverse each other: "pause long-horizon" then "run at the end", and "defer exams" then "deciding score". A dated diff of what the user now believes against what they said three weeks ago would catch drift they don't notice. Assumption: steers carry dates, as the pack shows.
  Done when: `fm steers --drift` lists pairs where a newer steer narrows, reverses or fulfills an older one. Each pair is marked superseded, or the user confirms it still holds.

- **Surface open tasks that only the user's hardware or credentials unblock, on their own screen** — FEATURE — value 3 — effort S — risk low — category: blockers
  Why: T-0325 needs `sudo pacman -S libappindicator`, T-0418 needs a manual update, T-0352 needs publishing, and each sits "blocked" with no copyable action. Assumption: this differs from the earlier list-of-blockers idea only by ending in one pasteable command per item.
  Done when: each blocked-on-user task prints the exact command or link in `fm next --user`. Running it and re-checking unblocks the task automatically.

Next question: which standing rules has the user effectively stopped following in practice, as shown by later steers or asks that contradict them, and does Foreman still enforce those?

Next question: how many minutes per day does the user actually spend reading Foreman output, and which surface do they open first when they return?
