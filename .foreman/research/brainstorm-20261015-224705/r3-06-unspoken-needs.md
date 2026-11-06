# Brainstorm — lens: unspoken needs

- **Slice every L task into vertical, independently landable pieces** — FEATURE — value 4 — effort M — risk med — category: planning
  Why: T-0034 and T-0035 are L tasks that sit deferred. A task too big for one session never gets built, and the unattended path can't pick it up. First version: `fm task slice` drafts 3–6 slices, each with its own test and a stub contract for the pieces not yet built. Each slice is queued as an S task.
  Done when: slicing a fixture L task yields slices that each close and pass the gates alone, and the queue shows the parent's progress as n/m.

- **Mock three pane layouts before writing any TSX** — FEATURE — value 4 — effort M — risk low — category: ui workflow
  Why: the user kept cycling through "still cluttered", "graphs too big", "liked the old plot chart" and "no gaps". The harness already renders frames (shot.py). First version: a UI task renders 2–3 candidate text frames at the user's terminal width and height, and the user picks one by number. Wild.
  Done when: `fm ui mock` prints N labelled frames from one fixture state at a given size, and the chosen number is recorded on the task.

- **Gate every injected card, hint and lesson on a Haiku-floor test** — FEATURE — value 4 — effort M — risk low — category: quality
  Why: the T-0978 Haiku probe found small-model gaps (the repo's own test runner, for-loop waits, unknown task ids). The user wants least token use and a plugin that works unasked. First version: replay a recorded obstacle through `claude -p --model haiku` with only the card in context. A card that fails is flagged for rewrite.
  Done when: `fm lib check --floor` lists which cards Haiku fails on, and a failing card exits non-zero.

- **Fold deferred "Later from T-…" tasks into one demo-able epic** — FEATURE — value 4 — effort M — risk low — category: backlog
  Why: about 35 deferred items (T-0787 to T-0866) are fragments of earlier brainstorms, and the user said the ideas "seem very simple". Drop/do/ask triage is already planned, but it keeps the fragments separate. First version: cluster the deferred tasks by shared files and topic (from `fm map`), then draft one epic whose acceptance is a single end-to-end demo script.
  Done when: `fm epic draft` turns a fixture set of 5 related deferred tasks into one epic with a runnable demo criterion and links back to the originals.

- **Refuse to keep resume state on volatile storage** — FIX — value 3 — effort S — risk low — category: resume
  Why: assumption: capsules, checkpoints or leases can land under `$XDG_RUNTIME_DIR` or `/tmp`, which logout or reboot wipes. That is exactly when a session "was stopped". First version: `fm doctor` and the capsule writer resolve the real mount, warn on tmpfs, and fall back to `~/.local/state`.
  Done when: pointing Foreman's state at a tmpfs path in a test produces a doctor warning, and the capsule is written to the durable fallback.

- **Bootstrap a fresh machine from the brain in one verb** — FEATURE — value 4 — effort M — risk med — category: portability
  Why: the user wants fixes to travel to other sessions, clones and machines. The native-install PATH failures (`~/.local/bin/claude`) show that machines differ. First version: `fm bootstrap` checks claude (native or npm), installs the plugin and pane mod at the pinned versions, pulls `.foreman/`, and ends with a green doctor line.
  Done when: running it in a clean container with only git and python leaves `fm doctor` green, or names the first missing piece with its fix command.

- **Nudge the matching Foreman verb once, when the user does it by hand** — FEATURE — value 3 — effort S — risk low — category: discovery
  Why: Foreman has dozens of verbs and 70+ skills, and the user said they shouldn't need to ask for any of it. Several planned features are only useful if they get found. First version: a PostToolUse rule matches a hand-typed `!` command (such as `git worktree list` or `git log -S`) to a verb map and shows a one-line tip, once per verb.
  Done when: a fixture session typing `git worktree list` shows the resume tip once and never again.

- **Compost finished and abandoned worktrees** — CLEAN — value 3 — effort S — risk low — category: hygiene
  Why: resume, `resume --all` and lane features multiply worktrees. `fm ui` already lists them on every gather, and the preflight is only about disk. First version: for a merged or untouched-for-N-days lane, write a patch bundle and capsule to the archive, then remove the worktree and branch. `fm resume` can restore from the archive.
  Done when: composting a merged fixture lane frees the directory, and resuming from the archive recreates an identical tree.

- **Reserve a moonshot slot with a kill metric and a receipt even on failure** — FEATURE — value 3 — effort S — risk med — category: portfolio
  Why: "these seem very simple" is a portfolio problem. The 800+ idea titles lean incremental, and nothing guarantees capacity for ambitious bets. First version: one in five unattended build slots goes to a tagged moonshot. It carries a timebox and a predeclared kill criterion, and it closes with a "what we learned" note whether it ships or is cut.
  Done when: a moonshot task past its timebox is auto-parked with a receipt naming the unmet kill metric.

- **Wild: Mark a session golden with one key and reuse its trajectory** — FEATURE — value 3 — effort M — risk low — category: learning
  Why: assumption: the user can tell a great run from a mediocre one, and Foreman only learns from failures and corrections. First version: store the golden session's brief and the order of its tool calls (names and file classes, not content). Inject it as a three-line skeleton when a similar task starts.
  Done when: after marking a fixture session golden, a similar new brief receives the skeleton in its context block, and `fm why` names the source session.

- **Wild: Push-to-talk steer, transcribed locally** — FEATURE — value 3 — effort M — risk med — category: voice
  Why: the user sends long, sprawling, multi-ask messages, and verbatim intake capture (T-0790) is still deferred. Speaking is a natural fit for that style. First version: a pane key records audio and transcribes with a local whisper.cpp binary if one is installed. The transcript goes into intake as a verbatim steer, with nothing leaving the machine.
  Done when: with a stub transcriber, the key press writes one verbatim intake item tagged `voice`, and with no binary installed it reports that and sends nothing.

- **Wild: Archive each shipped feature as a 5-second pane replay** — FEATURE — value 2 — effort M — risk low — category: delight
  Why: the user asked to re-record the demo and refresh the README pictures, and every shipped task already leaves ledger events. First version: render the task's stage rail, steps and done strip from the ledger into one SVG, reusing the demo/live.svg pipeline. It is attached to the close and linked from the changelog line.
  Done when: closing a fixture task writes `replay.svg`, and the changelog entry links to it.
