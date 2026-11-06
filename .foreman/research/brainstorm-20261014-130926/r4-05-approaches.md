# Brainstorm — lens: approaches

- **Rebuild the context pack builder so it stops polluting its own input** — FIX — value 4 — effort S — risk low — category: brainstorm hygiene
  Why: this pack shows four defects. "The user's own words" appears twice. Category-count rows ("- notifications 24", "- plugin, skill and MCP interoperability: 10") are listed as ideas. Foreman's own queue titles ("Round 2 brainstorm…", "Super-improve Foreman round 1") are counted as "asked". The header says Round 4 while the task says Round 2.
  Done when: a golden-pack test shows each section once, no `word N` histogram rows under ideas, no fm-authored task titles under the user's words, and one round id in the pack and the output filename.

- **Run a sweep round before any new brainstorm** — CLEAN — value 4 — effort S — risk low — category: backlog
  Why: the open list has stale or tiny items: T-0431 "Release 1.2.16" when 1.2.27 already shipped, the content-free T-0317 "There's new bug feedback", the S-sized T-0418, and the planned FIX T-0759. The approach is to close, fix or re-scope each one with a premise check (does the version, id or number in the title still match reality?) before generating more ideas.
  Done when: no open S task names a version or id that contradicts the ledger, and the sweep prints a close/fix/keep line for each.

- **Probe the host once and let every feature declare what it requires** — FEATURE — value 4 — effort M — risk low — category: host capabilities
  Why: T-0325 is blocked on a missing Arch tray library. assumption: the kernel is `hardened`, which commonly disables unprivileged user namespaces, so ideas built on the native sandbox may silently not work here. `fm doctor` would write a `host.json` (userns, tmux, tray lib, notifier, python floor) and the brainstorm pack would filter out ideas whose requirements are false.
  Done when: with userns disabled, a feature declaring `requires: userns` shows "unavailable: <reason>" in doctor and is excluded from the next pack.

- **Park L tasks on a user-fired ultra review and ingest the result** — FEATURE — value 3 — effort S — risk low — category: review
  Why: `/code-review ultra` is user-triggered and billed, and Foreman cannot launch it. So Foreman would stage the branch, write the focus list from the task's criteria with a cost note, and mark the task "awaiting ultra review" so the queue continues. When the user pastes the findings back, they become audit evidence.
  Done when: an L task reaches a parked state that prints the exact command, and pasted findings attach to its evidence and block close until they are triaged.

- **Tick the board in `$EDITOR` as a plain checklist** — FEATURE — value 3 — effort S — risk low — category: feedback loop
  Why: the known gap is that nobody has ticked the board, and `fm page` needs a browser plus an Artifact round trip. The cheapest alternative is `fm tick`, which opens a 30-line file with one `[keep|tune|drop]` per cluster and parses it on save. Trade-off: it has no visuals, but it is the lowest-friction route.
  Done when: editing the file and saving records ticks in the ledger and `fm research show` reflects them.

- **Measure child yield per dollar by model and lens** — PERFORMANCE — value 3 — effort S — risk low — category: child spend
  Why: every child now carries `--max-budget-usd` (this one has $15). assumption: the cap was set without data on which model/lens pair produces ideas the user later keeps. Log novelty-after-dedupe and later ticks per dollar, and pick model and lens from that.
  Done when: `fm research stats` prints a model × lens table of kept ideas per dollar from at least two rounds.

- **Write a reproducibility manifest for each brainstorm** — CLEAN — value 2 — effort S — risk low — category: provenance
  Why: ideas currently carry only prose. A manifest holding pack hash, lens, model, flags and parse-drop counts would make "why did this idea appear" answerable and make pack bugs like the duplicate sections visible.
  Done when: every catalogue entry links to a manifest, and re-running with the same pack hash reports the same parsed idea count.

- **Export the queue as todo.txt and iCalendar** — FEATURE — value 2 — effort S — risk low — category: interop — wild
  Why: assumption: the user already has a phone todo app or calendar. A read-only `fm export --todotxt|--ics` file (synced however they like, with no Foreman server) shows the queue and active step on any device. It also has no network surface and suits local-first use.
  Done when: the exported file imports cleanly into a todo.txt parser and shows T-ids, tiers and status.

- **Run an amnesiac round and count independent rediscoveries** — FEATURE — value 4 — effort M — risk low — category: demand signal — wild
  Why: the pile is thousands of lines, and children are told to avoid it, which steers them toward odd corners. Every other round, give children only the user's words, shipped work and open gaps, with no idea list. Ideas that fresh children keep reinventing are demand; ideas that never reappear were noise.
  Done when: a round prints "rediscovered by N of M lenses" per cluster and the top three seed the next queue.

- **Soft-launch round features that expire to off unless ticked** — FEATURE — value 3 — effort M — risk med — category: ratchet — wild
  Why: round 1 shipped many toggles and the user has ticked none. Invert the default: each round's opt-in features record a ship date and fire count, and unticked ones with zero fires after N days are switched off with one line saying how to restore them. Trade-off: it risks surprising the user, so it only affects features with a recorded zero fire count.
  Done when: a feature with no fires past its window reverts to its prior setting and the notice appears once.

- **Pin every close warning to a "what would the user do about it" check** — CLEAN — value 3 — effort M — risk low — category: warning precision
  Why: the last asks were two false-positive close warnings (tier-drift and `.claude/worktrees/`). Each warning would declare an action, and the harness replays it on the last 50 closed tasks and counts warnings no one acted on, which are demotion candidates.
  Done when: `fm doctor --warnings` lists each warning's fire count and action rate, and any warning below a set rate is flagged.

- **Run a local-only dry run of every new idea's "Done when"** — FEATURE — value 3 — effort M — risk low — category: queue quality
  Why: the output format demands one testable check per idea, but nothing runs it. At queue time, compile the check and run it against the current tree; it should fail now (the idea is real) and be runnable. This is the same defect that made the T-0775 check expire when its task left the queue.
  Done when: queueing an idea whose check already passes, or cannot run, is refused with the reason.
