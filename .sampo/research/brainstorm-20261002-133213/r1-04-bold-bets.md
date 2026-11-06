# Brainstorm — lens: bold bets

- **Ship a Foreman mod with a docked live pane** — FEATURE — value 5 — effort L — risk med
  Why: `fm watch` needs a second terminal and the statusline is one non-interactive line, while mods offer `$.ui.open` panes, AbovePrompt bands and Buttons. Assumption: `fm task show/state --json` is enough to feed it (T-0076 says criteria and steps are missing, so fix that first).
  Done when: `claude plugin test` mounts the pane and shows the active task, steps, stage bar and queue from mocked `fm` JSON. Pressing a "Next" button calls `fm` via `$.process.run`.

- **Enforce gates in-process with tool.call** — SECURITY — value 5 — effort M — risk med
  Why: the known limitations say Bash edits are invisible to scope checks and tripwires, the guard is a regex speed bump, and "Next:" hints can be ignored. `tool.call` sees every tool call and can deny or rewrite it.
  Done when: in a mod-enabled session, a Bash `sed -i` on an out-of-scope file is denied or recorded against the active brief. Classic hooks still behave the same under `claude -p`.

- **Replace Next: text with prompt.compose injection** — PERFORMANCE — value 4 — effort M — risk low
  Why: hooks inject "Next:" text on every prompt and Stop, and the user is token-sensitive. `prompt.compose` can replace a section instead of appending, and `session.append` can prune stale hints from the transcript.
  Done when: a mod-enabled session has measurably fewer injected tokens per turn than classic mode, and exactly one current "Next" section is present.

- **Add a Haiku-driven "smart gate" classifier** — FEATURE — value 4 — effort M — risk med
  Why: `$.model.complete` can classify cheaply in-process. Candidates are whether a prompt is a new request or a follow-up (capture vs chase), whether a command is dangerous beyond the regex, and whether evidence actually supports an acceptance criterion. Assumption: the added cost per prompt is small.
  Done when: on a labeled fixture set of prompts and commands, the classifier beats the regex guard's false-negative rate. It falls back to classic behavior when `$.model` is unavailable.

- **Wake idle sessions with $.prompt.submit for drive mode** — FEATURE — value 4 — effort M — risk high
  Why: "drive" and full autonomy currently depend on Stop-hook nudges. A timer can check `fm next` and queue the next prompt when idle, so the queue is processed unattended.
  Done when: with a queued brief and an idle session, the mod starts a turn on that brief within N seconds. A kill switch (`fm quiet`) stops it, and the mock-clock test passes.

- **Show per-task cost and verification heat as Raster sparklines** — FEATURE — value 3 — effort S — risk low
  Why: `fm cost` and the tool-latency data already exist, and the mod `Raster` element is made for sparklines and heatmaps. Shown in the pane or in the `CommandOutput` for `/fm cost`.
  Done when: `/fm cost` renders a per-step bar or sparkline from `fm cost --json` output in the mod test harness.

- **Register Foreman as model-callable tools and slash commands** — FEATURE — value 4 — effort M — risk low
  Why: planning friction comes from filling sections through several `fm` calls with exact names (T-0075, T-0080). `tool.register` can expose one `mcp__foreman__plan` tool that takes a structured object. `command.register` gives `/fm` as a native command.
  Done when: one `plan` tool call fills Approach, criteria and steps in a brief with evidence links intact. A test confirms no section duplicates.

- **Fix the inbox bugs that the mod depends on** — FIX — value 3 — effort S — risk low
  Why: T-0076 (`show --json` omits criteria, steps, depends), T-0075 and T-0080 all block the mod from reading and writing briefs reliably.
  Done when: `fm task show --json` includes criteria, steps and depends. A round-trip `task set --section` keeps the evidence links and creates no duplicate section.
