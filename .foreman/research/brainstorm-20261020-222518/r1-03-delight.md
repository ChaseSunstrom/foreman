# Brainstorm — lens: delight

- **Audition every runner on my own repo** — FEATURE — value 5 — effort M — risk med — category: runners
  Why: wild. The user wants "ANY CLI/model", but the pack's `fm code bench` uses seeded tasks, not their code. Assumption: worktrees are cheap enough to run candidates side by side.
  Done when: `fm code audition "<small request>"` runs it on each detected runner in its own worktree and prints a podium (time, tokens, checks passed, diff size). Choosing a winner writes the one-line default to config, and no worktree touches the main checkout.

- **Show a roll call on first launch** — FEATURE — value 5 — effort S — risk low — category: setup
  Why: T-1328 finds CLIs, but the user hit "no model → first request fails until you press m". Assumption: a 1-token ping per runner is acceptable.
  Done when: the first `fm code` with no config lists each found runner with a real "say ok" round trip (latency, ✓/✗ and the fix line for ✗), picks a working default automatically, and a fresh-HOME test shows a ready home screen with no keypress.

- **Quote the startup tax before a worker runs** — FEATURE — value 4 — effort S — risk low — category: honesty
  Why: the nixie run sat silent for minutes at 66k–133k input tokens per call, because nested Claude loaded every plugin. The user only learned this by digging.
  Done when: before the first CLI worker turn the TUI shows a measured "this CLI starts with ~N tokens of context, about Xs", offers a lean-launch key when one exists, and the number matches the stream's first usage event in a test.

- **Type a request and see where it goes before Enter** — FEATURE — value 4 — effort M — risk low — category: intake
  Why: `fm code` should open like claude, and the request box is the first thing seen. Assumption: kind detection can be a cheap local heuristic, not a model call.
  Done when: while typing, a ghost line shows "fix · nixie · claude worker · est. cost/time" (question, fix, feature or new project). The line updates within one frame, and a golden test covers 5 inputs.

- **Jump to a project by name** — FEATURE — value 4 — effort S — risk low — category: projects
  Why: "multiple projects" plus the nixie confusion (a run started from the wrong directory looks like it does nothing). Assumption: Foreman can see recently used project paths.
  Done when: `fm code nixie` or `/` in the home screen fuzzy-matches Foreman-known projects by frecency, shows the resolved path before starting, and a request that is not a project name still runs as a request.

- **Show a lineage badge for who is running whom** — FIX — value 4 — effort S — risk low — category: duplicates
  Why: the user asked to "prevent duplicate things when FM is installed as a claude plugin". T-1327 fixes nested sessions, but nothing shows the nesting.
  Done when: the header shows a chain like `you → fm code → claude (worker, lean)`. When launched inside a Claude Code plugin session it adds "sharing this session's Foreman" instead of starting a second one. A test asserts no second drive or request capture is registered.

- **Show "You said / we did" on the home screen** — FEATURE — value 5 — effort M — risk low — category: trust
  Why: the user said "I shouldn't even need to say anything", and complaints like "it just isn't doing anything" are already mined. The payoff stays invisible unless shown.
  Done when: home lists the last 5 friction phrases the user used, each linked to the task or release that answered it (or "still open"), and an unattended Foreman-filed item carries the quoted phrase that triggered it.

- **Talk to settings in plain words** — FEATURE — value 4 — effort M — risk med — category: config
  Why: the user wants "better config/setup". Assumption: a runner's own planner can turn a sentence into a config diff.
  Done when: typing `use codex for questions, claude for fixes` shows a diff of the config file, applies it only on confirm, rejects keys not in the schema, and `undo` restores the prior file.

- **Name every run like a journal entry** — FEATURE — value 3 — effort S — risk low — category: history
  Why: the history view lists runs by ID, and the user returns to many projects. Assumption: the plan's title can be slugged locally.
  Done when: each run gets a short human name (for example `fix-login-redirect`) used in history, the branch and the commit trailer. Names are unique per project, and the history list of a seeded repo reads as sentences.

- **Sweep one request across many projects** — FEATURE — value 4 — effort L — risk med — category: fleet
  Why: wild. Multi-project management implies "do this everywhere" (a license year, a CI bump). Assumption: lanes can run in parallel with per-project leases.
  Done when: `fm code sweep "<request>" --projects a,b,c` runs one harness per project and shows a board (queued, running, proved, red), and a red project never blocks the others or gets a commit without its checks passing.

- **Let a second CLI cross-examine the diff** — FEATURE — value 4 — effort M — risk med — category: review
  Why: wild. Foreman already judges each worker turn, and a different model family catches different mistakes. Assumption: two runners are installed.
  Done when: after proof passes, an optional reviewer runner reads the diff read-only and returns a checked JSON verdict. Disagreements appear as a banner with the quoted concern. The reviewer cannot write, and a test with a fake reviewer shows the banner.

- **Make the home screen greet you with the state of play** — FEATURE — value 3 — effort S — risk low — category: home
  Why: wild. The pack lists "while you were away" and a shift report, but not a single sentence you can read in a blink. Assumption: the data comes from the existing queue and inbox.
  Done when: the first line of home reads like "nixie: 2 proved overnight, 1 waiting on you. foreman: idle." The line is generated from queue state with no model call, and an empty-state test shows a friendly line instead of a blank.

- **Print a heads-up when the run is waiting on the CLI, not on you** — FIX — value 4 — effort S — risk low — category: liveness
  Why: "it just isn't doing anything". Existing ideas cover a heartbeat strip. This adds the explanation and the escape.
  Done when: after 20 s with no stream event the footer says which child process is alive (pid, CPU, what it last printed) and offers `k` to kill it and `r` to retry with another runner. A fake silent CLI test shows the line and that `k` leaves no orphans.
