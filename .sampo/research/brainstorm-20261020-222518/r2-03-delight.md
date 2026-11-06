# Brainstorm — lens: delight

- **Suggest the next request from the repo** — FEATURE — value 4 — effort M — risk low — category: home screen
  Why: Bare `fm code` is meant to open like `claude`, but an empty request box is the blankest screen in the app. Open tasks, TODO comments, red tests and the last run's loose ends are all on disk. Assumption: ghost-text suggestions don't clash with the planned "open on the failing test" idea.
  Done when: in a fixture repo with one TODO and one deferred task, the empty box shows both as ghost text, Tab fills one, and Enter runs it.

- **Offer a follow-up after every close** — FEATURE — value 4 — effort M — risk low — category: continuity
  Why: Users keep saying "again, but…" and "also…". The pack's closing moments (receipt, confetti, postcard) all end the conversation. Assumption: users want to amend a result right after seeing it.
  Done when: after a closed run, typing "also add a test for the empty case" creates a new task that names the previous task and its diff as context, and the history view links the two.

- **Reveal the result with one key** — FEATURE — value 3 — effort M — risk med — category: payoff
  Why: Seven request kinds close green, but the user never sees what they got. Diffs and receipts are shown, not the result itself. Assumption: the project's run command is detectable from `fm map`.
  Done when: after a "new project" run in a fixture, pressing `o` runs the detected entry command, or opens the built page, in a throwaway pane and shows its output without touching the repo.

- **Paste a screenshot into the request** — FEATURE — value 3 — effort M — risk med — category: input
  Why: "It just isn't doing anything" and "looked like crap" are things people show, not describe. Assumption: at least one runner (claude, codex, vision-capable HTTP models) accepts images.
  Done when: pasting or dragging an image path into the request box attaches it, and the plan's request record cites the file. A runner without image support shows a one-line "this runner can't see images" and offers one that can.

- **Say goodnight to start an unattended shift** — FEATURE — value 4 — effort M — risk med — category: ritual
  Why: The user has asked for "full auto" and "don't stop until complete" repeatedly. The pieces exist (unattended queue, stop-line, postcard) but are separate commands. Assumption: `systemd-inhibit` or `caffeinate` is available to hold off sleep.
  Done when: `fm code goodnight` runs the queue under a sleep inhibitor with a stated spend cap and stop-line, then writes a morning digest. A test with a fake runner proves it exits cleanly at the cap.

- **Rotate "you haven't tried this" tips from local usage** — FEATURE — value 3 — effort S — risk low — category: discovery
  Why: The user found out they could run `fm code` as an app, switch runners and run `fm code bench` by asking. A footer tip taken from features this install has never used teaches the product without a tour. Assumption: a local-only usage counter is acceptable.
  Done when: with a fresh state file the footer shows a tip about an unused feature, and after that feature is used its tip stops appearing.

- **Show what the first call is loading, live** — FEATURE — value 4 — effort S — risk low — category: trust
  Why: The nixie run sat silent while 66k–133k input tokens were loaded per call. Watching the weight appear is the honest version of the spinner. This differs from the planned quote and meter: it is a short animated list of the plugins and rules as they load, ending in "ready in 11 s".
  Done when: a worker launch against a fake CLI that logs its startup steps shows each step in Activity as it arrives, with the total at the end.

- **Give each runner a career card** — FEATURE — value 2 — effort S — risk low — category: personality
  Why: The picker, bench grades and learned routing already exist but show no history. Each runner would get a card with tasks closed, held-rate, typical cost, best request kind and a last-seen line. Assumption: run history stores the runner name.
  Done when: opening the runner picker shows a card per runner whose numbers match `fm code bench` and history for a seeded fixture.

- **Ask for a mid-run status in plain words** — FEATURE — value 4 — effort M — risk low — category: reassurance
  Why: "Isn't doing anything" is a question the user asks while the run is live. A key (`?` or just typing in the box) returns one sentence built only from the event log, such as "waiting on claude for 3 min; last tool call was Read plan.md; nothing is stuck on you." No model call.
  Done when: against a recorded stalled-planner log, the sentence names the waiting runner, the silence duration and the last event, and it contains nothing absent from the log.

- **Wild: Add a "ghost of Foreman past" that predicts the run's length** — FEATURE — value 2 — effort M — risk low — category: anticipation
  Why: Assumption: past runs of the same request kind and runner give a usable range. A faint marker on the track shows where similar runs usually are by now. Seeing "you're ahead of usual" or "slower than the last four" turns waiting into a small race.
  Done when: with five seeded past runs, the track draws a ghost marker at the median stage for the elapsed time, and it disappears when fewer than three exist. Wild.

- **Wild: Turn the home screen into a living desk of project cards** — FEATURE — value 3 — effort L — risk med — category: home screen
  Why: Multi-project management is the headline ask, and a list wastes it. Each project is a card showing a mini track, a count of blocked and waiting items, and a card that lifts when something needs you. The pack has a harbor map and a project deck, but neither brings in the other lanes' live status or lets you drag a request onto a card to run it there.
  Done when: with two fixture projects, one active and one blocked, the home view shows both cards with correct state. Moving the selection and pressing Enter on a request in the box runs it in the selected project. Wild.

- **Wild: Let the user name a runner a nickname and a voice** — FEATURE — value 2 — effort S — risk low — category: personality
  Why: Assumption: the user will adopt a tool they have named. Config would hold `nick = "Old Faithful"` for the claude worker, and status lines, toasts and receipts would use it ("Old Faithful closed T-1330 green").
  Done when: setting a nickname on a runner changes its name in the TUI header, history and the closing receipt, and `fm code config` shows the real id beside it. Wild.

- **Close each run with a one-line "what I'd do next"** — FEATURE — value 3 — effort S — risk low — category: continuity
  Why: Work ends in a receipt, but the user's habit is to chain requests ("keep going", "don't stop"). The harness already knows blocked and deferred items. It would offer the single most relevant next task and run it on Enter.
  Done when: closing a task that has one open follow-up in the same area prints that task's id and title as the suggestion, and Enter starts it.

- **Wild: Hand off a live Claude Code session by saying "take this to fm code"** — FEATURE — value 4 — effort L — risk high — category: handoff
  Why: The pack says users move between Claude Code and `fm code`, and duplicate-Foreman problems show the two overlap. Assumption: session transcripts can be read locally. A one-liner would bundle the current request, what has been tried and the open files into a new run, so the user never re-explains.
  Done when: in a fixture session with a transcript, `fm code --adopt` creates a task whose request text and context cite that session's last request and changed files. No network call is made. Wild.
