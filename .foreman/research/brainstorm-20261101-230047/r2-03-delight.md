# Brainstorm — lens: delight

- **Show a "while you slept" morning card** — FEATURE — value 5 — effort M — risk low — category: delight
  Why: the night tick "logs only when something happens", so the user has no pleasant moment where self-started work becomes visible; the nightly digest exists but is a log, not a greeting. Assumption: the user opens a session or the web UI most mornings.
  Done when: after a night tick that started one lane, the first `fm next` or web UI load shows one card naming what ran, what it cost, what landed on a `night/<date>` branch, and the one yes waiting, in under 8 lines.

- **Celebrate the first self-started success once** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: Mission 4's whole point is "work starts without me"; the first time a trigger fires and the work passes its gate is the product's proof moment and nothing marks it. Assumption: a trigger-fired task has an origin stamp.
  Done when: the first trigger-originated task closing green prints a single plain-words line ("Your CI watcher fixed itself while you were out") and never prints it again (test asserts once-only).

- **Render every queued install as one card with one-word answers** — FEATURE — value 5 — effort M — risk low — category: approvals
  Why: the mission says installs (timers, units) are "queued for one yes"; several earlier ideas bundle grants, but the delight is a card showing the exact unit text, what it will wake, and `yes / no / later`. Assumption: the queue lives in a file only a user-run verb writes.
  Done when: `fm yes` lists all pending installs as one screen with the unit text and cost estimate, and one word per row applies it; a test shows a `later` row reappears next session.

- **Preview a trigger on last week before it arms** — FEATURE — value 4 — effort M — risk low — category: trust
  Why: users trust a timer more when they see "this would have fired 3 times: Tue, Wed, Fri, and here is what each would have done". Assumption: git, CI and file events from the last 7 days can be replayed from existing logs.
  Done when: `fm when --preview <rule>` prints the dates and the would-be tasks for the past 7 days without starting any lane.

- **Say why a trigger didn't fire** — FEATURE — value 4 — effort S — risk low — category: transparency
  Why: silent automation feels broken; the tick logs only on action. Assumption: skip reasons (quiet hours, battery, debounce, budget) are known at decision time.
  Done when: `fm triggers why <name>` prints the last skip with its reason and the condition that would release it.

- **Offer a quiet-hours dial instead of a cron string** — FEATURE — value 3 — effort S — risk low — category: scheduling UX
  Why: users who install timers think in "not while I'm working" and "overnight", not crontab syntax. Assumption: the tick already has a notion of user activity in the repo.
  Done when: `fm when` accepts `overnight`, `weekdays 9-5 off`, and `when idle`, and shows the next three wake times in plain dates before saving.

- **Compile "whenever X, do Y" typed in chat into a trigger draft** — FEATURE — value 4 — effort M — risk med — category: natural language
  Why: users already type standing intents as steers; turning a sentence into a reviewable trigger row (never auto-installed) closes the gap. Assumption: a draft goes through the same one-yes queue.
  Done when: typing "whenever CI goes red on main, fix it" in a session produces a trigger draft file plus the install card, and nothing arms until `fm yes`.

- **Tell the user kindly when a trigger has never helped** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: standing rules around lean substance say unproven growth should not persist; a gentle "this watcher fired 9 times and you never acted on it, retire it?" respects that. Assumption: acted-on can be read from task outcomes.
  Done when: a trigger with N fires and zero accepted outcomes surfaces one retire-or-keep prompt in the morning card, and a chosen keep silences it for 30 days.

- **Draw the night on the web UI as a timeline strip** — FEATURE — value 3 — effort M — risk low — category: web UI motion
  Why: the web UI is the only surface found; motion that explains state suits lanes starting and stopping unattended. Assumption: lane start/stop times are logged.
  Done when: the web UI shows a horizontal strip of the last night with each lane as a bar (trigger name, outcome color, duration), with an empty state ("nothing needed doing") and a loading state, and a screenshot test covers both.

- **Wild: Play the night back as a ten-second timelapse** — FEATURE — value 3 — effort M — risk low — category: delight (wild)
  Why: assumption: people show others what their tool did while they slept; a replay of lane bars growing, files touched, and green checks landing is shareable. Builds on the timeline strip.
  Done when: a "play" button on the night strip animates the night in about 10 seconds from logged events, honoring reduced-motion by showing the end state.

- **Wild: Knock twice to cancel everything** — FEATURE — value 3 — effort S — risk low — category: control (wild)
  Why: assumption: a panic stop that is a playful, memorable gesture feels safer than a buried verb; ideas list a `fm halt` and tripwire file, this makes it tactile.
  Done when: touching `~/.claude/foreman/STOP` (or running `fm halt`) makes the next tick stop all triggers and lanes, and the morning card states who stopped them and how to resume.

- **Wild: Leave a postcard from the lane** — FEATURE — value 2 — effort S — risk low — category: delight (wild)
  Why: assumption: unattended work reads colder than it is; each self-started lane ends with a two-sentence plain note ("I found the flaky test, fixed the race, held back one thing for you") in the user's own voice settings.
  Done when: every trigger-started lane writes a `postcard.md` of at most 40 words with a "held back for you" line, and the morning card quotes it.

- **Show "what would wake me" on the status line** — FEATURE — value 3 — effort S — risk low — category: status line
  Why: the user can't see armed triggers without running a verb; a compact count with the next wake builds trust. Assumption: the status line has room for one short segment.
  Done when: the status line shows e.g. `⏰ 3 armed · next 02:10` and shows nothing when no trigger is armed.

- **Offer to schedule what the user does by hand every week** — FEATURE — value 4 — effort M — risk med — category: proactive
  Why: the "asked" stream shows recurring request shapes (ship bets, cold reads, weekly digests). Assumption: a shape repeated three weeks running can be detected from task titles.
  Done when: after the third weekly repeat of the same request shape, Foreman offers one trigger draft through the install queue, and declining it records a reason so it is never re-offered.

Next question: Which of the self-started artifacts (branches, notes, cards) does the user actually look at in the first minute of a session, and is there evidence from past digests that they read any of them?
Next question: What would make a user feel unsafe about work starting without them, and which of those fears can be answered with one line on screen rather than a setting?
