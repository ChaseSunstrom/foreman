# Brainstorm — lens: capability map

- **Run builders in an OS sandbox** — SECURITY — value 5 — effort M — risk med — category: security
  Why: builders run in bypass mode and the guard only reads commands (T-0275 is still open). Nothing in the pack confines a builder at the OS level. Assumption: bwrap or landlock is available on the user's Linux.
  Done when: a builder in a worktree that tries `echo x > ~/outside` or `curl` to a host off the allowlist fails with a logged denial, and a normal build and test run still passes.

- **Retire rules the model has outgrown** — FEATURE — value 5 — effort M — risk med — category: simplicity
  Why: the Haiku probe (T-0978), the "least token use" steer and the "Make healthy turns add zero bytes" idea all point at rules that cost tokens whether or not they are needed. Assumption: each rule can be tagged with the failure it prevents.
  Done when: `fm rules canary` runs each tagged rule's failure scenario with the rule off on the current model. A rule the model passes unaided in N of N runs is listed as "silent candidate", and a changed model ID triggers the run.

- **Check new dependencies before they are installed** — SECURITY — value 4 — effort S — risk low — category: supply chain
  Why: T-0791 covers supply chain only in general, and Foreman already reads dependency manifests for cards. Assumption: registry lookups need network, so this is opt-in.
  Done when: adding a nonexistent or brand-new (under 30 days) package to a manifest in a test repo is blocked or warned, with the registry age shown, and an existing popular package passes silently.

- **Install Foreman's git hooks for hand-made commits** — FEATURE — value 4 — effort S — risk low — category: developer experience
  Why: the guard and proof gates only see Claude's edits. Commits typed by the user, or by other tools, skip them. Assumption: users commit by hand sometimes.
  Done when: `fm git-hooks install` adds a pre-push hook that runs the repo's gates, and a push with a red gate is refused with the same message `fm` gives.

- **Search all past work in one verb** — FEATURE — value 4 — effort M — risk low — category: memory
  Why: the pack's many "learn once" ideas store hints, lessons, decisions and closed tasks separately. The user asked for "why have you not improved", which needs an answer to "have we hit this before?". Assumption: a local SQLite FTS index is acceptable.
  Done when: `fm recall "folder trust prompt"` returns the matching closed task, hint and lesson ranked, with ids, and nothing leaves the machine.

- **Detect prompt-cache breaks that Foreman causes** — PERFORMANCE — value 4 — effort M — risk low — category: tokens
  Why: the Bash prelude repeated exports 8x, and injections change per turn. Both can bust the prompt cache, which costs more than raw bytes. Assumption: cache read/write counts are readable from the transcript usage fields.
  Done when: `fm doctor` reports turns where cache-read tokens dropped after a Foreman injection, names the injection, and a golden test shows injected text is byte-stable across turns that did not change it.

- **Resolve PR review threads automatically** — FEATURE — value 4 — effort M — risk med — category: PR loop
  Why: "Ship to a PR and keep fixing until CI is green" covers CI, not reviewer comments. Assumption: `gh` is authenticated.
  Done when: given a PR with two review comments, `fm pr threads` makes one fixup commit per comment on a worktree branch, runs the gates, and drafts replies for the user to approve before they post.

- **Report which features are never used** — CLEAN — value 3 — effort S — risk low — category: simplicity
  Why: only 6 of 1,084 cards ever fired, and the backlog has 1,158 skill files. Existing ratchet ideas count files, not use. Assumption: local per-verb and per-hook counters are cheap.
  Done when: `fm usage` lists verbs, hooks and cards with zero fires in 30 days, and a monthly run opens deletion tasks for the top five.

- **Verify the installed plugin against its release** — SECURITY — value 3 — effort S — risk low — category: integrity
  Why: hooks run on every tool call in bypass mode, so a tampered hook file is a high-value target. Assumption: releases can publish a hash manifest.
  Done when: `fm doctor --verify` fails and names the file when an installed hook differs from the tagged manifest, and passes on a clean install.

- **Scaffold a hook with a recorded fixture** — FEATURE — value 3 — effort S — risk low — category: developer experience
  Why: the pack shows repeated hook test gaps (T-1001, T-1003, T-1007, T-1013). Assumption: contributors write new hooks by copying old ones.
  Done when: `fm dev hook new NAME` creates the hook, a stdin fixture captured from a real event, and a failing test, plus a bench entry.

- **Use terminal-native alerts** — FEATURE — value 3 — effort S — risk low — category: devices
  Why: blocked and done alerts matter, and Foreman's pane is a terminal surface. Assumption: the terminal supports OSC 9 or 777 notifications.
  Done when: a blocked task emits one notification escape that appears as a desktop notification in a supporting terminal, and does nothing in one that lacks support.

- **Wild: Attach a phone to the pane by QR code** — FEATURE — value 4 — effort L — risk med — category: devices
  Why: wild. The web UI surface exists, and a read-only live pane over the tailnet with a one-tap approve for blocked items would cover the phone surface. Assumption: the user has a tailnet or LAN.
  Done when: `fm ui share` prints a QR code, and the phone shows the live pane read-only, and one authenticated tap answers a blocked prompt.

- **Wild: Sonify the session** — FEATURE — value 2 — effort M — risk low — category: delight
  Why: wild. The user watches long runs, and an ambient sound for working, blocked, red and green lets them look away. Assumption: sound is off by default.
  Done when: with `sound=on`, a red-then-green proof plays two distinct tones, and with it off nothing plays.

- **Wild: Keep Foreman's own regression suite from user steers** — FEATURE — value 5 — effort L — risk med — category: self-improvement
  Why: wild. The user said "why have you not really improved". Each steer like "no gaps", "graphs too big" or "all fits on one screen" could become a checkable layout or behaviour test. Assumption: steers can be classified as testable.
  Done when: a recorded steer produces a failing test in the next task, and the final scorecard shows steers turned into tests this week.
