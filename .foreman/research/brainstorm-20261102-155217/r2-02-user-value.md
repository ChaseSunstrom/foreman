# Brainstorm — lens: user value

Answering a left-over question first: when the user's hand and Foreman's hand both change the same thing, the fix is to settle it in a one-table rule. That is already on the list ("Settle hand-vs-Foreman precedence in one table"), so I don't repeat it.

- **Keep a promise ledger** — FEATURE — value 4 — effort M — risk low — category: trust
  Why: assumption: Foreman prints "Next:", "later" and "I'll file a follow-up", and the pack shows 30+ "Later from T-xxxx" deferred tasks. Nothing shown checks that those promises were kept.
  Done when: a fixture session that prints "I'll file X" with no X filed makes `fm doctor` list one overdue promise with its source line.

- **Tokenise identifiers reversibly before any cloud send** — SECURITY — value 4 — effort M — risk med — category: privacy
  Why: assumption: the pack has a redacting proxy and a scrub on the way in, but no scheme that lets the model still reason about names. This replaces hostnames, client names, emails and paths with stable placeholders and maps them back in the output.
  Done when: a test pack containing `acme-prod-db.internal` reaches a fake model as `HOST_1`, and the returned patch is restored to the real name with no placeholder left in the file.

- **Classify repo sensitivity from its contents on first contact** — SECURITY — value 3 — effort S — risk low — category: privacy
  Why: assumption: "Label a goal private" asks the user to do it by hand. Signals like `.env`, keys, "confidential" or NDA words, medical or financial schemas, or a client-named remote can set the egress policy automatically and say why.
  Done when: a fixture repo with a `.env` and a "CONFIDENTIAL" header opens as `private`, with the triggering file named in one line, and a clean fixture opens as `normal`.

- **Log the waits the user feels** — PERFORMANCE — value 3 — effort S — risk low — category: latency
  Why: assumption: the pack benchmarks hooks and cold start, but only from the system's side. It does not time prompt to first output, ship gate duration or the `fm next` wait as the user sees them.
  Done when: `fm doctor` prints the three longest user-felt waits from the last 7 days, each with its p50 and p95.

- **Pre-run the user's habitual first commands** — PERFORMANCE — value 3 — effort M — risk med — category: anticipation
  Why: assumption: the shell and `fm` history shows a pattern, for example `fm next`, `git status` and the test command in the first minute of a session. Running the read-only ones in the background at session start makes them instant. The speculation is labelled, expires, and switches itself off when its hit rate is under 30%.
  Done when: a replay of recorded sessions shows a cache hit rate printed per habit, and a planted 0%-hit habit is disabled after N sessions.

- **Detect a bad stretch and go quiet** — FEATURE — value 4 — effort S — risk low — category: anticipation
  Why: the user's dropped items show a run of re-grounded drops, and several steers are corrections. After N consecutive dropped or corrected suggestions, Foreman pauses non-urgent output for 24h and asks one question: "what is wrong with what I'm offering?"
  Done when: a fixture ledger with 5 consecutive drops produces exactly one question and no slate until it is answered or the hold expires.

- **Ratify costly decisions the user never vetoed** — FEATURE — value 3 — effort M — risk med — category: autonomy
  Why: the standing rule is to decide with `fm decide --kind costly` and keep going, and the user rarely re-confirms. After a 14-day silent window, a decision is promoted to a standing steer with its automatic check. The report lists each promotion, and one key reverses it.
  Done when: a decision aged 15 days with no veto appears as a steer with a check, and `fm decide --revoke` removes both.

- **Tell questions from requests at intake** — FIX — value 3 — effort S — risk low — category: intake
  Why: assumption: some "asked:" entries are slate lines or questions that became tasks. A message ending in "?" with no change verb should get a cited answer from the ledgers and MASTER.md, not a filed task.
  Done when: "what did T-2645 change?" returns an answer and files nothing, while "change X" files a task.

- **Whisper when the user opens a file a deferred task covers** — FEATURE — value 3 — effort M — risk low — category: editor
  Why: (wild) 30+ deferred tasks sit unseen. When the editor opens a file named in a deferred brief, a one-line status-bar note says "T-0217 touches this — wake it?".
  Done when: opening a fixture file named in T-0166 yields exactly one whisper, and it is not repeated that day.

- **Count hours given back, net of false alarms** — FEATURE — value 4 — effort M — risk med — category: value
  Why: (wild) "Report a spend receipt" exists, but nothing counts the user's time. This is a lifetime counter: minutes saved by landed work, minus the minutes spent on false blocks, repeated asks and reverted work. It prints conservatively and shows its working.
  Done when: the counter's inputs are all listed on one screen, and a planted false-block event lowers the total.

- **Hold a Sunday-night "week ahead" draft built only from the user's own history** — FEATURE — value 3 — effort M — risk low — category: anticipation
  Why: (wild) The user's recurring arcs are Genesis generations, ship days and exam deferrals. A zero-token draft says "likely this week: gen-3 Mission 8, an end-of-run exam decision, and a ship". The Monday ledger then scores it.
  Done when: the draft is written from fixture ledgers with no model call, and a scoring line appears the next Sunday with hits and misses.

- **Make the ledger size and age visible to the user's disk** — PERFORMANCE — value 2 — effort S — risk low — category: footprint
  Why: assumption: the pack reports 2139 files and no per-ledger growth rate. A one-line forecast, "ledger X reaches 100 MB in N days", makes compaction a choice and not a surprise.
  Done when: `fm doctor` prints each ledger's size and its projected date to a user-set ceiling.

Next question: which of Foreman's anticipatory outputs (cards, whispers, pre-runs, drafts) has the user ever acted on, and what is that rate against ignored or dropped ones?
Next question: what does the user do in the first minute of a session, from shell and `fm` history, and which of those steps could be ready before they type?
