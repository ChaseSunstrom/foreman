# Brainstorm — lens: beautiful UI and motion

- **Design the home screen as a project deck, not a list** — FEATURE — value 5 — effort M — risk low — category: app shell
  Why: T-1330 makes `fm code` open a home over every project; the pack's ideas cover run views, not the multi-project landing. Each project is a card with a live mini station-track, queue depth, blocked/inbox badges and the active runner's glyph, ordered by "needs you" first. Arrow keys glide a focus ring between cards; Enter zooms into that project's run view with the card expanding to fill the screen.
  Done when: a golden-frame test of the home with 3 fixture projects (one active, one blocked, one idle) shows all three cards ordered blocked/active/idle, and Enter on one renders that project's run view.

- **Show a "no progress" diagnosis in place of a silent spinner** — FIX — value 5 — effort S — risk low — category: liveness
  Why: the nixie run "just isn't doing anything" for minutes while a planner ran at 66k–133k input tokens per call. The spinner must change character with evidence: first "waiting on claude, 41s, N bytes received", then after a threshold a plain line naming the likely cause (nested session loading plugins, endpoint unreachable, model queue) and the keys to act (w wait, k kill, m switch runner).
  Done when: a fake runner that emits nothing for N seconds makes the frame show the elapsed-silence line and a cause hint by the threshold, asserted in a golden frame.

- **Add a runner picker that looks like a fleet bay** — FEATURE — value 4 — effort M — risk low — category: runners
  Why: T-1328 finds every CLI/model; the `m` picker is a flat list today (assumption). Render each detected runner as a slot with a signature glyph/hue, status (found, key missing, unreachable, last bench grade) and a one-key "test ping" that animates a pulse along the slot until it answers. Setup becomes a visible check, not a config file hunt.
  Done when: with a fake PATH containing two CLIs and one dead endpoint, the picker frame shows three slots with distinct statuses and `p` on the dead one ends in a red "unreachable" state.

- **Make first launch a guided, zero-text setup strip** — FEATURE — value 4 — effort M — risk low — category: onboarding
  Why: the user asked for "better config/setup" and hit `fm` not being a command at all. On first `fm code`, a three-chip row (command on PATH, runner found, project known) fills in with check animations, offering one-key fixes (link into ~/.local/bin, pick default runner), and writes the config line itself.
  Done when: in a clean HOME with a fake claude on PATH, the first launch frame shows three chips resolving and, after the fix key, `fm code` is recorded as the config's default runner.

- **Draw duplicate-Foreman detection as a visible "who's in charge" badge** — FEATURE — value 4 — effort S — risk low — category: trust
  Why: the user wants no duplicate Foreman when Claude Code is the worker (T-1327). The header badge shows the session nesting depth ("Foreman → claude (bare)"), turning amber with a one-key explanation if a worker reports its own Foreman hooks loaded.
  Done when: a worker started under the harness reports a bare-context flag and the header shows "worker: bare"; a fixture with hooks loaded shows the amber state.

- **Animate orphan cleanup on quit** — FIX — value 4 — effort S — risk low — category: lifecycle
  Why: the planner kept running after quit (T-1326). Quit shows a short "stopping claude… codex… done" countdown with each child's pid fading out, and refuses to vanish until children are gone or force-killed, so the user sees nothing is left behind.
  Done when: quitting with a sleeping child process leaves no process alive and the exit frame lists it as stopped.

- **Ghost-lane for multi-project runs** — FEATURE — value 4 — effort L — risk med — category: multi-project
  Why: "manage multiple projects" implies concurrent runs. A thin lane per running project at the bottom shows its track as a one-line dotted rail; flicking `Tab` swaps which lane is the stage, with a crossfade. Assumption: concurrent runs are permitted by leases.
  Done when: two fixture runs in different directories show two lanes, and Tab swaps the focused run without stopping either.

- **Put a token-weight meter on every worker launch** — FEATURE — value 3 — effort S — risk low — category: cost visibility
  Why: 66k–133k input tokens per nested call was the hidden cause of slowness. Show a "launch weight" bar per call, red above a threshold, with the note "plugins loaded: 14" when the cause is known.
  Done when: a fake stream reporting 120k input tokens renders a red weight bar with the number in the activity lane.

- **Wild: Let the home screen be a harbor map** — FEATURE — value 3 — effort L — risk med — category: delight
  Why: wild. Projects are boats moored at a dock; running ones bob, blocked ones show a flag, finished ones leave a wake line. Works from the same data as the deck and falls back to it on small terminals.
  Done when: `fm code --home harbor` renders one boat per fixture project with distinct states in a golden frame.

- **Wild: Auto-open a "what's wrong" overlay when friction is detected** — FEATURE — value 4 — effort M — risk med — category: self-diagnosis
  Why: wild, from "Foreman should figure this out without being asked." If a run is silent beyond the threshold or the user mashes keys with no effect, an overlay checks the runner, PATH, lease and config, and shows results as a rapid checklist ticking down with a suggested fix.
  Done when: a fixture with a broken runner path triggers the overlay and it names that path as the failing check.

- **Wild: Command line that doubles as a request box** — FEATURE — value 4 — effort M — risk low — category: input
  Why: wild-ish, matching claude's feel. A bottom prompt where typing plain text starts a request, `/` opens commands, `@` picks a project and `!` picks a runner, with chips rendering inline as you type.
  Done when: typing "@nixie !codex fix the parser" renders two chips and starts a run in that project with that runner.

- **Wild: Dock-pane trailing mode for use beside Claude Code** — FEATURE — value 3 — effort M — risk med — category: surfaces
  Why: wild. The same home collapsed to a 30-column strip showing only the "needs you" count and the active lane's rail, for sitting next to a Claude session; builds on the existing breakpoint plan.
  Done when: at width 30 the frame renders the strip with counts and no horizontal overflow.

- **Persist the last view so reopening feels like resuming** — FEATURE — value 3 — effort S — risk low — category: continuity
  Why: assumption: claude-like apps reopen where you left off. Restore last project, selection and scroll, and on start show a one-line "since you left: 2 tasks closed, 1 blocked" digest that fades after a few seconds.
  Done when: closing and reopening with fixture events shows the same selected project plus the digest line.
