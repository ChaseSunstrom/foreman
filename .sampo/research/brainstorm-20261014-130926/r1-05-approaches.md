# Brainstorm — lens: approaches

- **Verify the mail monitor in a real interactive session** — FIX — value 5 — effort M — risk low — category: reliability
  Why: round 1 lists the `foreman-mail` monitor's arming in a live interactive session as unverified, and `fm bus --wake` now skips tmux when the heartbeat looks fresh. A false "fresh" heartbeat means a silently idle session. Approach: spawn a throwaway interactive `claude` in a pty, send it bus mail, and assert the mail arrives with no tmux typing.
  Done when: a test script starts a pty session, posts mail, and fails if the session does not receive it within N seconds. `fm doctor --live` reports "monitor armed" or the specific failure.

- **Run compact output in shadow first, then ask once** — FEATURE — value 4 — effort S — risk low — category: tokens
  Why: it is built and measured at about 1.04M tokens per 30 days saved, but off until the user says yes, and the user has not said yes. Approach: a shadow mode logs what it would have rewritten, and whether any failure line would have been lost, without changing any output. After a week, one "enable?" line shows the real numbers.
  Done when: shadow mode writes per-output records without altering tool results. `fm cost` prints "would save X tokens, 0 failure lines lost". A single `fm compact on` flips it.

- **Add a claimed-vs-measured receipt for each round** — FEATURE — value 4 — effort M — risk low — category: observability
  Why: nobody has ticked the board, and round 1 made numeric claims (tokens saved, hook p50, push behaviour) with nothing re-checking them later. `fm round receipt` would re-run each claim's measurement and render a table through `fm page`, with a tick per row that closes the board item.
  Done when: the receipt command prints each round-1 claim with its recorded and current value, flags any that differ by more than a stated tolerance, and its output renders as an Artifact page.

- **Ship each round-1 feature with a fire counter** — FEATURE — value 4 — effort M — risk low — category: observability
  Why: round 1 added about ten behaviours (sessionTitle, the Stop-hook push ask, outward-tool refusal, compact rewrite, effort pass-through). Nothing records whether they ever fire. A counter file per feature gives evidence for keeping or removing each, and a baseline for any later ablation.
  Done when: each named feature increments a counter in state, `fm doctor` lists counts with last-fired time, and a test confirms zero overhead beyond one append.

- **Add passive recurrence counters for the deferred clusters** — FEATURE — value 4 — effort S — risk low — category: user value
  Why: T-0787 to T-0799 were deferred for lack of evidence (burst folding "no evidence it recurs", supply chain "no incident", crash recovery "no incident"). Instead of re-debating them, count cheaply: messages arriving within 60s of each other, hand-edited transcripts, crash-looped sessions. After 30 days the promote-or-kill decision is data.
  Done when: the counters exist, `fm research list` or a new `fm evidence` shows them per cluster, and each deferred task carries a promote threshold.

- **Derive the step pointer from tool activity (finish T-0759)** — FIX — value 4 — effort M — risk med — category: reliability
  Why: T-0759 is planned: the pointer lags the work. Approaches range from a nudge at edit time, through deriving the step from the files each step names, to mirroring the native task list. The smallest one that works is deriving it from the files an edit touches against the files each step names, with the explicit pointer kept only as a tiebreaker.
  Done when: a fixture where edits name a later step moves the pointer, and a long run of edits on one step does not. Both are covered by tests.

- **Fail closed on unclassified native tools in sensitive repos** — SECURITY — value 4 — effort S — risk low — category: security
  Why: round 1 refuses named outward tools (PushNotification, Artifact, SendMessage, RemoteTrigger). A new Claude Code release can add an egress tool this list has never seen. `fm doctor` already compares the CC version, so it can diff the live tool list against the classified set. In sensitive repos, unknown tools are refused until classified.
  Done when: a fixture with an unknown tool name is refused in a sensitive repo and allowed otherwise, and `fm doctor` lists unclassified tools.

- **Property-test `fm page` redaction** — SECURITY — value 3 — effort S — risk low — category: privacy
  Why: T-0786 needed home, user and path-spelling hardening after the fact, which suggests redaction was found by incident rather than by search. Generate paths and usernames in many spellings (symlinked home, `~`, `/run/user/…`, URL-encoded, mixed case) and assert none survive in the HTML.
  Done when: a generated-input test runs over at least 500 variants, and every failure it finds is added as a fixed case.

- **Turn the 2026-10-14 headless-drive incident into a permanent drill** — FIX — value 3 — effort M — risk low — category: agents
  Why: round 1 fixed one-off `claude -p` sessions that answered and stopped instead of driving the queue. Nothing proves the fix holds across Claude Code versions. A drill runs a scripted `claude -p` in a scratch Foreman project and asserts it does not drive, then runs an interactive one and asserts it does.
  Done when: the drill runs under `fm doctor --live`, and it fails if either behaviour flips.

- **Wild: Ablation switches for every round**
  — FEATURE — value 3 — effort L — risk med — category: simplicity
  Why: wild. The user said "recursively improve" and the project already carries about 73 skills and a large hook surface. Each round's features would land behind named switches, and `fm round ablate N` turns a round off in a scratch lane and runs the bench. A round that earns nothing gets removed rather than accumulating.
  Done when: `fm round ablate` runs the bench with a chosen round's features off and prints the delta on first-pass rate and tokens.

- **Wild: A scoreboard of "things you never had to ask twice"**
  — FEATURE — value 3 — effort M — risk low — category: delight
  Why: wild. The user's own steers show repeated asks (pre-1.2.27 release steps, re-asks about the same failure classes). Recording each time a rule or lesson prevented a repeat gives the user a number to feel and Foreman a way to rank which lessons matter. Shown on the return card.
  Done when: each lesson hit that preceded a pass is counted, and `fm since` prints the weekly count with the top three lessons.

- **Wild: A pre-round "interview the transcript" pass**
  — FEATURE — value 3 — effort M — risk low — category: developer experience
  Why: wild. The brainstorm pack is now thousands of lines of mostly repeated ideas, yet the strongest signals come from the user's real messages and the known gaps. Before each round, a cheap child reads only the recent steers, drops and failures and writes one page of "what this user is actually trying to do", which replaces the idea dump as the pack's lead section.
  Done when: the pack builder emits that page and caps the rest of the idea list at cluster names and counts, and the pack shrinks by a measured percentage.

- **Show a returning-session card that states the first failing check** — FEATURE — value 3 — effort S — risk low — category: docs
  Why: after round 1 there are many new surfaces (monitor, page, compact output, session titles) and `MASTER.md` is the only guide. Generate the section describing each from the CLI and hook definitions, so `fm doctor` fails when a shipped feature has no documented line.
  Done when: `fm doctor` reports any round-1 feature missing from `MASTER.md`, and the check passes after the docs are generated.
