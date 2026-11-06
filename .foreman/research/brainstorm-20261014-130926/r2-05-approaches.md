# Brainstorm — lens: approaches

- **Canonicalise every path once, then property-test the spellings** — CLEAN — value 4 — effort M — risk med — category: guard / correctness
  Why: Three of today's fixes are the same bug: `.claude/worktrees/<lane>/` edits (T-0807), `.claude/` counted as "left behind" (T-0812), and home/user spellings in `fm page` (T-0786). Each was patched in its own module. Assumption: guard, scope, tier-drift, lanes and page each normalise paths separately.
  Done when: one `canon_path()` is imported by all five modules, and a property test over `~`, `$HOME`, symlink, `./`, trailing slash and worktree-prefixed spellings finds no module that disagrees.

- **Check a lane's base before it forks from `head`** — FIX — value 4 — effort S — risk low — category: lanes
  Why: Round 1 set `worktree.baseRef=head`, so a lane never sees uncommitted work in the main tree. The lane-merge start-point bug (T-0812) shows lanes are already fragile around their base. Assumption: nothing warns when the tree is dirty.
  Done when: `fm run --parallel` on a dirty tree prints which files the lane will not see and asks to stash, commit or continue; a test covers the dirty and clean cases.

- **Record `--affected` misses and widen the selection on its own** — FEATURE — value 4 — effort M — risk med — category: gates / tokens
  Why: Builders now run `fm check --affected`. If the full suite at close fails where the affected run passed, nothing records it, so a wrong test map stays wrong. The track-record bugs today show Foreman's metrics already miss real failures.
  Done when: a close-time full-run failure that `--affected` passed writes a miss entry naming the file and test; the next `--affected` for that file includes the test; `fm doctor` shows the miss rate.

- **Stream mail to the monitor as a pointer, not the body** — SECURITY — value 4 — effort S — risk low — category: liveness / injection
  Why: The `foreman-mail` monitor puts bus mail straight into the model's context, which is a new unauthenticated input channel. A fixed envelope (kind, T-id, one line, `fm bus read <id>`) is cheaper in tokens and gives injected text nowhere to sit. Assumption: the monitor currently streams full message text.
  Done when: monitor lines are capped at 120 characters and contain no free text from the sender; a test sends a 5 KB mail and sees only the envelope.

- **Redact and restrict the compact-output spill store** — SECURITY — value 4 — effort S — risk low — category: privacy / tokens
  Why: Compact output saves full Bash text (about 44M characters per 30 days) under `state/outputs` for 7 days. That includes env dumps and tokens, and the tidy pass only deletes on age. Assumption: the files are written with default permissions and no scrub.
  Done when: spill files are mode 0600, a known fake token in a command's output is masked in the stored file, and the stub says the file was redacted.

- **Give sensitive repos a no-cloud attention path** — FEATURE — value 3 — effort S — risk low — category: notifications / devices
  Why: Sensitive repos now refuse `PushNotification`, so a drained queue or open ask in those repos reaches nobody who is away from the terminal. Assumption: no fallback exists.
  Done when: in a sensitive repo, an open ask triggers a terminal bell plus a local desktop notification (OSC 777 or `notify-send`) carrying only the T-id, and no outward tool is called.

- **Leave a manual `/rename` alone** — FIX — value 2 — effort S — risk low — category: session title
  Why: `sessionTitle` is set on every startup, resume and fork. A title the user chose by hand would be overwritten. Assumption: Foreman does not record who set the current title.
  Done when: Foreman sets a title only when none is set or the stored title was Foreman's own; a resumed session with a user title keeps it.

- **Route every list and field input through one coercion function** — CLEAN — value 2 — effort S — risk low — category: cli design
  Why: T-0810 fixed `fm task set` list fields for `a,b` and `[a, b]` as a one-off. Other `fm` verbs likely parse lists their own way. Assumption: more than one parser exists.
  Done when: all `fm` verbs that take list fields use one `coerce_list`, and one table test shows the same inputs giving the same results across the verbs.

- **Auto-tick the board from the user's next move** — FEATURE — value 3 — effort M — risk med — category: feedback loop
  Why: "Nobody has ticked the board" is a known gap, and the user drops items by simply ignoring them. A task still open and untouched after 3 sessions, or an opt-in left off, is a quiet vote. Assumption: ticking by hand will keep not happening.
  Done when: `fm research show` lists each round-1 item with a derived kept/untouched/reverted state and the evidence behind it, and a test covers each state.

- **Wild: Add an ambition dial for rounds (`fm ambition 1-5`)** — FEATURE — value 3 — effort S — risk low — category: recursion — wild
  Why: The user's repeated "super improve… etc. etc." asks for more with no scale. One number could set the mix: 1 means fixes and deletions only, 3 means round-2 style, 5 means new capabilities and wild items. Assumption: round scope is currently implied by prompt wording.
  Done when: `fm ideas` reads the dial, and at level 1 the lens set contains no capability-map lens; a test checks both ends.

- **Wild: Mark round boundaries as git tags and build the brief from `git log round-N..`** — CLEAN — value 3 — effort S — risk low — category: recursion / doing less — wild
  Why: Several ideas propose a new round ledger. The commit titles already say what shipped, and a tag costs nothing to store. Trade-off: it loses non-code outcomes such as dropped ideas, so keep it as the cheap default and add a ledger only if it proves too thin.
  Done when: `fm round tag` creates `round-N`, and the next brainstorm pack's "shipped" section is generated from commits since the last tag.

- **Wild: Open each session with "previously, in Foreman"** — FEATURE — value 3 — effort S — risk low — category: delight — wild
  Why: Foreman changes itself every day, and the user learns what changed only by asking. A one-line greeting from the last three commit titles since the user's last session would show that without a page. Assumption: SessionStart can carry one extra line.
  Done when: the first message of a session after a self-update shows at most one line summarising the changes, and nothing is shown when nothing changed.

- **Wild: Add a per-hook "would the user notice" probe** — PERFORMANCE — value 3 — effort M — risk med — category: hooks / simplicity — wild
  Why: A hook that never changes a decision for 30 days is a candidate to remove. Today only latency is measured. Assumption: the ledger can tell a hook that fired from one that changed an outcome.
  Done when: `fm doctor` lists each hook with fires, outcome-changing fires and p50 time, and flags any with zero outcome-changing fires in 30 days.
