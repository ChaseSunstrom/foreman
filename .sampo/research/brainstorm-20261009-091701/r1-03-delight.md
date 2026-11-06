# Brainstorm — lens: delight

- **Replay a finished task as a scrubbable timeline** — FEATURE — value 5 — effort L — risk med — category: replay
  Why: the ledger, checkpoints, evidence per step and guard events already exist, but the only view of a finished task is a brief. The user steered toward a Tauri app with smooth animation and controlling every session. Assumption: the ledger has enough timestamps to reconstruct order.
  Done when: `fm ui --json` exposes an ordered event stream for a task, and the desktop app plays it with a scrub bar that shows the step, the diff and the evidence at each moment.

- **Show a "what Foreman did while you were away" return screen** — FEATURE — value 5 — effort M — risk low — category: briefing
  Why: `fm night`, `fm run`, `fm serve` and `fm digest` all work unattended, but the user returns to separate outputs. The JARVIS idle complaints show they leave sessions running. Assumption: the user wants one entry point, not five commands.
  Done when: on the first session or app open after 30+ minutes away, one screen lists tasks finished, tasks blocked and why, a decision awaiting them and the cost, with a single key to act on the top item.

- **Narrate the guard's refusals as a friendly teaching moment** — FEATURE — value 4 — effort M — risk low — category: guard UX
  Why: several recent requests (T-0404, T-0409, symlink rm) came from refusals that were correct but unhelpful or confusing. Each refusal should name the exact fix, the part of the command that tripped it (T-0423 already records this), and a copy-ready corrected command.
  Done when: every guard refusal includes a "run this instead" line, and a test asserts that line is present for each refusal category in the replay corpus.

- **Give the band a sense of progress with a live "pace" mood** — FEATURE — value 3 — effort S — risk low — category: statusline
  Why: the band and pane are the always-visible surface, and the step-stuck bug (T-0406) shows that people read them closely. Assumption: a small state glyph (cruising, waiting on a gate, blocked on the user) is quick to read and cheap to compute from existing task state.
  Done when: the statusline shows one of at least four distinct states derived from the task and drive state, and a test covers each mapping.

- **Hold a "ship party" release ritual** — FEATURE — value 3 — effort S — risk low — category: release
  Why: the user asked for Release 1.2.13 through 1.2.16 in a row, each time pushing to GitHub main and JARVIS. A one-command ritual would remove that repetition and make it feel good.
  Done when: `fm release` bumps the version, writes the changelog from merged tasks, runs gates and prints a summary card with the numbers (tasks, tests added, lessons learned). It pushes only after explicit confirmation.

- **Generate a "taste portrait" the user can read and edit** — FEATURE — value 4 — effort M — risk low — category: personalization
  Why: `fm taste` already infers what the user keeps, drops and steers. The drops show real preferences (YAGNI on guard surface, no blocking before 75% usage). Showing this as an editable page lets the user correct Foreman's model of them.
  Done when: the app shows the taste profile as plain sentences with provenance links to the original choices, and editing or deleting a sentence changes what `fm ideas` receives.

- **Draw the project as a living map that lights up where work is happening** — FEATURE — value 4 — effort L — risk med — category: visualization
  Why: `fm map`, `fm impact` and `fm tour` already carry layout, test links and hot files, but only as text. Lanes working in parallel could show as colored regions on a treemap, with files pulsing as they are edited.
  Done when: the desktop app renders the map from `fm map` data, and an edit in a lane highlights that file's cell within 2 seconds.

- **Wild: Give Foreman a voice that reports at the end of a long run** — FEATURE — value 3 — effort M — risk low — category: voice
  Why: wild. `fm notify` takes any command, so a local text-to-speech call is feasible. The user runs unattended queues and could hear "three done, one blocked on a decision" from across the room. Assumption: the user has a local TTS available and opts in.
  Done when: with the setting on, `fm run` finishing speaks a one-sentence summary through the configured command, and nothing is spoken with the setting off.

- **Wild: Hold a post-mortem court where past mistakes argue the plan** — FEATURE — value 4 — effort L — risk med — category: planning
  Why: wild. Foreman records surprises, lessons, vetoes and decisions, and `fm second` already runs a debate. Before a plan is approved, specialist agents could each speak for one past failure ("last time this file broke the guard") and the plan must answer each one. It becomes delightful because the plan arrives already hardened.
  Done when: for a task touching files with recorded surprises or lessons, the plan includes a short "objections answered" section citing those records, and a test confirms a lesson-linked file triggers it.

- **Wild: Turn each finished task into a one-screen shareable "receipt"** — FEATURE — value 3 — effort M — risk low — category: sharing
  Why: wild. `fm pr` already builds a description with proof. A visual receipt (before/after screenshot from `fm smoke`, red-to-green test count, time, cost) is something people show others. Assumption: smoke screenshots are stored with the task.
  Done when: `fm receipt T-xxxx` writes a self-contained HTML or PNG file with those items, and it contains no paths or secrets (checked by `fm secrets`).

- **Wild: Run a "ghost user" that tries the product like a first-time visitor and posts a clip** — FEATURE — value 5 — effort L — risk med — category: product check
  Why: wild. The user asked that Foreman check the product the way its user uses it, and `fm smoke` runs a headless browser at two viewport sizes. A ghost explorer that follows links and forms with no script, and records a short video of anything odd, makes bugs vivid.
  Done when: `fm smoke --explore` runs a bounded session, records a trace or video, and the report lists at least one finding on a seeded broken page in a fixture project.

- **Celebrate small wins in the pane with a clear checkmark motion** — FEATURE — value 2 — effort S — risk low — category: motion
  Why: T-0406 showed that step progress drifts out of sync, which makes ticking feel unreliable. A short animation when evidence lands on a step, and when the step advances, makes the moment legible.
  Done when: in the UI, recording evidence for a step animates the step state change once, and reduced-motion settings disable it.

- **Offer a "what should I do next" card ranked by what the user would pick** — FEATURE — value 4 — effort M — risk low — category: queue
  Why: the drive was changed to name queued tasks when idle (T-0401) because 20+ items sat unworked. Ranking those offers by the taste profile and by `fm relate` dependencies makes each offer likely to be accepted.
  Done when: the three offers shown during idle are ordered by a documented score, and a test shows that an unblocked dependency of the last finished task ranks first.

- **Draw a small cost-and-pace gauge that stays quiet until it matters** — FEATURE — value 3 — effort S — risk low — category: budget
  Why: the user said budget and pace limits shouldn't block anything until 75% usage, and that subagents shouldn't be capped by tokens. A gauge that appears only past that threshold respects both.
  Done when: the gauge is hidden below 75% usage, appears above it, and the statusline test covers both cases.
