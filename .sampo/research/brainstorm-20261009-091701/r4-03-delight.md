# Brainstorm — lens: delight

- **Answer side questions without touching the task** (`fm btw`) — FEATURE — value 4 — effort M — risk low — category: interaction
  Why: Foreman's core promise is staying on task and capturing new requests. A mid-task "wait, how does X work?" currently either derails the thread or becomes a task. Assumption: users ask these constantly.
  Done when: `fm btw "why does lane merge refuse dirty trees?"` returns a cited answer from a read-only child, and the active task's focus, step and context are byte-identical afterward.

- **Show why a line exists, in the editor** — FEATURE — value 4 — effort L — risk med — category: editor surface
  Why: `fm why FILE[:LINE]` exists, but only in the CLI. Nothing shows task, lesson or surprise at the moment the user is editing. Assumption: a small VS Code/Neovim extension can call `fm why --json`.
  Done when: hovering a line Foreman changed shows its task, the lessons attached to it and the proof status, and the response arrives in under 300 ms.

- **Write commits and PRs in the user's own voice** — FEATURE — value 3 — effort M — risk low — category: taste
  Why: the pack's taste and request-dialect ideas cover input only. Generated commits, changelog lines and PR text read like a tool wrote them. Assumption: `git log --author` plus the user's captured briefs give enough style signal.
  Done when: a blind test on 10 past commits (5 the user's, 5 generated) shows the user picks the generated ones as theirs at least 40% of the time, and the style profile is viewable and editable.

- **Preview a brief before it exists** (`fm preview`) — FEATURE — value 4 — effort M — risk low — category: intake
  Why: capture classifies and plans only after commitment. A dry run could show the type, tier, gates, related tasks, likely files, queue collisions and cost estimate. This fits the user's terse-request style and the pack's repeated "wrong class" and "overlap" friction. Assumption: the classifier and `fm relate` can run without writing state.
  Done when: `fm preview "fix the login timeout"` prints those six fields and `fm task list` is unchanged afterward.

- **Show smoke screenshots inline in the terminal** — FEATURE — value 3 — effort S — risk low — category: evidence UX
  Why: `fm smoke` runs a headless browser at desktop and phone widths, but the user only gets a verdict line. Assumption: kitty/sixel/iTerm graphics protocols are detectable, with a text fallback.
  Done when: on a kitty-compatible terminal, `fm smoke` ends with both viewport thumbnails drawn inline, and on a plain terminal it prints file paths instead.

- **Catch bugs the user hits in their own dev tab** — FEATURE — value 5 — effort L — risk med — category: ambient capture
  Why: the user's recent asks ("Foreman checks the product the way its user uses it", JARVIS feedback relayed by hand) show bugs surfacing in real use. A local-only browser extension could watch localhost for error overlays, console errors and failed requests. Assumption: nothing leaves the machine.
  Done when: a thrown error in a localhost tab produces a captured FIX brief with the stack, a screenshot and the failing URL within 5 seconds, and no network call leaves the host.

- **Share a read-only live view of a run** — FEATURE — value 3 — effort M — risk med — category: collaboration
  Why: `fm serve`, `fm watch` and the Tauri app exist, but only for the owner. A teammate or the user's phone could follow a run over LAN or Tailscale, and a comment dropped on a step becomes a captured request. Assumption: off by default, with a token required.
  Done when: the link renders the live band, and a comment lands in the inbox tagged with its source. Requests without the token get 401.

- **Record the docs from real runs** — CLEAN — value 3 — effort M — risk low — category: documentation
  Why: MASTER.md is the single source of documentation, and `fm docs` already reports drift. Terminal casts recorded from scripted fake-agent runs (assumption: the cassette harness from earlier rounds exists) would be regenerated each release and fail it if they diverge.
  Done when: the release gate re-records every cast, diffs it against the stored one, and fails on any mismatch.

- **Mark what changed since each surface last looked** — FEATURE — value 3 — effort M — risk low — category: UI state
  Why: the user is often away while lanes finish (see the JARVIS merge complaints). A whole-session return screen is coarse. A per-item "new since you looked" dot on tasks, asks and decisions would be finer. Assumption: seen-state is stored per surface.
  Done when: opening a task in the desktop app clears its dot, the dot persists across restarts, and the band shows the unread count.

- **Complete task ids with their titles** — FEATURE — value 3 — effort S — risk low — category: CLI ergonomics
  Why: every one of the user's recent corrections involved typing `fm focus T-0278` style ids by hand. Shell completion that shows each id with its title and status costs little. Assumption: no completions ship today.
  Done when: in bash, zsh and fish, `fm focus T-04<tab>` lists matching ids with titles, and completion finishes in under 100 ms.

- **Wild: Hold an appeals court for refusals** — FEATURE — value 3 — effort M — risk med — category: guard UX
  Why: the user hit repeated false-positive refusals (`fm focus … ; sed -i`, the `rm` symlink case) and fixed each by hand later. A one-line "appeal: why" could replay the command against the guard, pull similar past rulings and return a verdict plus a proposed rule diff within a minute. wild
  Done when: appealing a known false positive produces a verdict citing at least one past ruling and a proposed fix that passes the guard's differential tests.

- **Wild: Seal time capsules for predictions** — FEATURE — value 3 — effort S — risk low — category: reflection
  Why: the user steers often on cost, pace and estimates. Sealing a prediction at plan time ("this takes 2 lanes, one afternoon") and opening it automatically at done would give a running calibration score and an honest grin. assumption: estimates are stored per task. wild
  Done when: finishing a task prints "you predicted X, it took Y" and `fm digest` shows the running hit rate.

- **Wild: Stream a 24/7 dogfood arena** — FEATURE — value 2 — effort L — risk med — category: showcase
  Why: seeded-bug projects scored by the discipline are already an idea in the pack. Replaying them continuously from recorded cassettes, with no live-model cost, gives a public page that doubles as a regression canary. wild
  Done when: the page replays the arena on a loop, and a deliberately broken release shows a visibly red run within one cycle.
