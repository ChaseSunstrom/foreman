# Brainstorm — lens: invented: the session that can read its own map

- **Write one self-map file every session can Read** — FEATURE — value 5 — effort M — risk low — category: introspection
  Why: SessionStart injects 2,733 characters twice and the per-turn burden is 48 to 76 characters, but nothing records what the session currently holds. The ideas so far each fix one channel.
  Done when: `sampo self` writes `self.json` of at most 1.5 KB, which a Read accepts. It lists each injected block with its owner, characters, hash, age, and what was withheld this turn with the pull command. A test asserts the block sizes match what the hooks actually emitted.

- **Report what compaction lost** — FEATURE — value 4 — effort M — risk med — category: continuity
  Why: assumption: long drive sessions compact often. Existing ideas steer the compactor or resume with bookmarks, but none diff the self-map before and after compaction.
  Done when: after a forced compaction, a hook diffs the pre- and post-compaction self-maps and re-injects only the lost Ward, task and steer lines. The re-injection is at most 400 characters, and a test fails if any guard clause is missing afterwards.

- **Look up where an instruction came from** — SECURITY — value 5 — effort M — risk med — category: injection defense
  Why: Sampo already treats pasted text and untrusted content as data, and open items cover taint tracking and hidden text. None gives the session a way to ask "who said this?" when an instruction looks odd.
  Done when: `sampo origin "<quoted text>"` returns user, Sampo-injected, file, tool-result or unknown, with its ledger line. A planted instruction in a fetched file comes back as `file`, not `user`.

- **Fence recursive scans of the state directory** — PERFORMANCE — value 4 — effort S — risk low — category: lean
  Why: project state is 2.4 GB. A session that runs `grep -r` or `find` over it stalls and floods its context, and no listed idea addresses this.
  Done when: a PreToolUse rule blocks recursive scans rooted in the state dir and prints a `sampo recall` or `sampo state map` pointer instead. The block is covered by a Ward exam case, and ordinary scans of the repo are unaffected.

- **Cap tool output by remaining headroom** — PERFORMANCE — value 4 — effort M — risk med — category: context
  Why: the refused Read of MASTER.md (75,758 tokens) shows the cost of learning about a limit only after hitting it. The gauges exist, but no output is sized against the headroom they report.
  Done when: a Bash, grep or verb output larger than 25% of measured headroom is truncated to a head and tail plus a "N lines left out, flag to show them" line. A test with a near-full gauge triggers the truncation.

- **Flag version skew inside a live session** — FIX — value 3 — effort S — risk low — category: safety
  Why: the install-versus-source drift note prints at session start only. Overnight drive sessions outlive upgrades and the rename migration, so they may run on old Ward text.
  Done when: a hook compares the session's loaded guard hash with the installed one and adds one line to the per-turn string on mismatch. A test upgrades the install mid-session and sees the line on the next turn.

- **Let the session file map corrections** — FEATURE — value 3 — effort M — risk med — category: map accuracy
  Why: the session is the only reader that finds the map wrong while it works. Nothing records a correction, such as a stale `fm*.py` shim path in the cold-read list.
  Done when: `sampo map note "<claim is wrong>" --path P` stores the note. A zero-token check confirms or rejects the claim against the repo, and a confirmed note updates the map. An unconfirmed note is shown as "disputed", not applied.

- **Write each session's own start card, fact-checked** (wild) — FEATURE — value 4 — effort L — risk high — category: lean start
  Why: assumption: a session knows best what the next one needs, and the 2,733-character block is generic. Other ideas cache or dedupe the block, none has the session write it.
  Done when: at Stop, the session writes a card of at most 600 characters. A checker deletes any line it cannot verify against the ledgers or git, and the Ward line is always kept. The next SessionStart injects that card in place of the static block, and a cold-child exam finds no regression.

- **Make injection demand-driven with "want" bids** (wild) — FEATURE — value 4 — effort L — risk med — category: adaptive context
  Why: injected blocks are chosen by the authors' guesses. Existing ideas count re-Reads or score outcome change, but the session's own pulls are never the signal.
  Done when: `sampo want <section>` returns the section and logs the pull against the task kind. After N sessions of the same kind, a block that is never wanted drops out of the default injection and a block wanted every time moves in. The Ward is excluded from demotion, and the rule is shown in `self.json`.

- **Replay what the session held when it erred** (wild) — FEATURE — value 3 — effort L — risk med — category: debugging
  Why: assumption: after a bad action, nobody can say which injected line was in context at that turn. Sampo keeps ledgers and transcripts but no per-turn context composition.
  Done when: sparse self-map snapshots of 2 KB or less every 10 turns are stored with the task. `sampo blame <turn>` prints the blocks in context at that turn and which of them the action quoted.

- **Hand each lane a map slice and take back its delta** — FEATURE — value 3 — effort M — risk low — category: lanes
  Why: parallel lanes each pay the full injection. The "not checked" hand-back covers work, not the child's own picture of the repo.
  Done when: a lane's SessionStart is at most 40% of the parent's. The hand-back adds "map lines I added or found wrong", and the planner merges them. A two-lane test shows the smaller injection and the merged lines.

- **Hold a conversation with a frozen past session's map** (wild) — FEATURE — value 2 — effort M — risk low — category: archaeology
  Why: assumption: the user asks "why did it do that?" about a night run and today only has a transcript to read.
  Done when: `sampo ask-past T-id turn "<question>"` answers from the stored snapshot and transcript only. It prints which snapshot it used and refuses to answer from today's state.

- **Detect a session that cannot see its own map** — FIX — value 3 — effort S — risk low — category: introspection
  Why: Read refuses MASTER.md and the sessions kept going, so no gauge shows a session working blind.
  Done when: any refused or truncated Read of a file the injection names writes a `blind` row. `fm doctor` lists the files with counts, and a test reads a planted oversized file and sees the row.

Next question: which injected lines does a session never act on, and does the self-map plus a pull verb carry the same behaviour at a tenth of the characters?
Next question: when a session reads its own map and finds it wrong, who owns the fix, and is that owner a reader that already exists?
