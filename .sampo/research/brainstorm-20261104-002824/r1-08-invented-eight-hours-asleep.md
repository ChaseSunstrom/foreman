# Brainstorm — lens: invented: eight hours asleep

- **Run a bedtime preflight canary** — FEATURE — value 5 — effort S — risk low — category: unattended reliability
  Why: the recent drive fixes (T-2873, T-2900, T-2901) show unattended paths failing silently on small things. The user's only chance to catch that is before sleeping. Assumption: Foreman can detect "user idle for N minutes plus evening hours".
  Done when: when the user goes idle in the evening, one tiny throwaway task runs the full unattended path (lane spawn, local endpoint reachable, a no-op `fm ship --dry-run`, alert channel). It prints a single green or red line, and a red line names the broken hop.

- **Release a phantom-held drive after 20 quiet minutes** — FIX — value 5 — effort M — risk med — category: drive watchdog
  Why: T-2873, T-0575 and T-0115 show the drive waiting on subagents that are dead or already done. Overnight, one phantom hold loses the whole night.
  Done when: a test with a fake agent list and no ledger or event progress for 20 minutes makes the drive drop the hold, log "released phantom hold: <ids>", and take the next task. A live agent that is still emitting events keeps its hold.

- **Batch the night's local work by model, one switch per night** — PERFORMANCE — value 4 — effort M — risk low — category: local models
  Why: the steer says a llama-swap switch costs about 3 minutes with no detection, and that qwen3.8-27b should be used first. Interleaving models wastes the night.
  Done when: the night queue is sorted so the 27B-class tasks run first and the MoE tasks run in one later block. A simulated 12-task night makes at most one switch, and the receipt shows the minutes saved.

- **Reserve the last 90 minutes for re-proof on merged main** — FEATURE — value 5 — effort M — risk low — category: morning trust
  Why: the user wants major progress by morning. Lanes that each passed alone can still break each other once merged.
  Done when: 90 minutes before the user's usual wake time, no new work starts. Every task landed that night has its Exam and proof re-run against the merged tree. The morning card lists "N landed, M still green on merged main", and any red task is flagged first.

- **Fall back to local models during a usage-limit wait** — FEATURE — value 4 — effort M — risk med — category: quota and local
  Why: the steer is to wait out real limits and keep going on everything that isn't blocked. Hours of local-model capacity sit idle during that wait.
  Done when: while a limit pause is active, the drive runs only a whitelisted class (docs, red-first tests for existing code, Moonscale candidate fills, cold reads) on the local profile. Everything is tagged `local-night`. The first Claude task after the reset starts without any manual step.

- **Review the day's landed commits overnight with a different model** — FEATURE — value 4 — effort M — risk low — category: outside signal
  Why: the standing rule wants weakness-finding from signals Foreman didn't author, and cold reviews by a different model. The only time that is cheap is while the user is asleep.
  Done when: each night a local 27B child reads only the day's diffs and writes findings, each with a quoted line. The morning card shows the findings count, and only findings that quote a line are kept.

- **Set a zero-wake pager policy** — FEATURE — value 4 — effort S — risk low — category: notifications
  Why: "stop asking me for stuff" and "never interrupt mid-run" are both standing steers. Without an explicit rule, any alert path could wake the user.
  Done when: a named list of wake-worthy conditions exists (disk full, credentials expiring, push failed on main, runaway spend). Every other event queues for the morning card. A test fires 20 mixed events and asserts only the listed ones reach the pager.

- **Run a night league of local models on Sampo's own closed tasks** — FEATURE — value 4 — effort L — risk low — category: model bench
  Why: the Model bench asks (T-2886, T-2887, T-2894) want measured local backends. Idle hours are the free place to run them, and the result can drive routing.
  Done when: a night run replays held-out closed tasks across the available local models and writes a table by task kind. The routing table changes only if the new arm beats the incumbent on the held-out set, and the change is recorded with the margin.

- **Compare the night's spend and progress against a sealed plan** — FEATURE — value 3 — effort S — risk low — category: observability
  Why: unattended spend today is only visible afterward. A plan sealed at bedtime makes the morning receipt a diff rather than a story.
  Done when: at bedtime a plan is written with lanes, the model per lane, a dollar cap and the do-not-touch paths. The morning receipt shows planned versus actual per line, and any overrun is highlighted.

- **Wild: Turn the night into a dial on the astrolabe** — FEATURE — value 3 — effort M — risk low — category: delight — wild
  Why: the Kirjokansi theme is a turning sky with a brass instrument. Assumption: the web UI can render it from ledger timestamps.
  Done when: the morning page shows the night as a dial with a hand per lane, where tasks are arcs coloured by outcome. Scrubbing the dial shows what each lane was doing at that hour. Reduced-motion users get a static dial.

- **Wild: Hold a nightly "ghost user" that predicts a handful of asks and is scored by the morning** — FEATURE — value 4 — effort M — risk low — category: anticipation — wild
  Why: the request is a model of the user that drafts the next ask. A tool-less local child that sees only the last day's ledger and the user's steers guesses three asks and drafts a brief for each.
  Done when: the morning card shows drafts, and a first message that matches one (judged by a cold read) marks it a hit. The hit rate is shown beside a recency baseline, and the feature mutes itself if it stays below that baseline for 14 days.

- **Wild: Keep a sleeping-lamp status that tells you at a glance if the night is safe** — FEATURE — value 3 — effort S — risk low — category: devices — wild
  Why: the user can't check a terminal from bed. Assumption: they have a phone that can open a local page or receive a push.
  Done when: one status endpoint returns green, amber or red with a one-line reason. It turns amber if progress stalls for an hour and red only for a listed wake condition, and a phone page and a tray colour both read from it.

Next question: What does the user actually do in the first five minutes after waking, and which of those actions could the night have done for them?
Next question: Which overnight task classes have the best record of surviving 14 days after landing, so the night can start with those?
