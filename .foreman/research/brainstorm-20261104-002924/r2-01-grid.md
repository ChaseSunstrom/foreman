# Brainstorm — lens: grid

- **Log every refused Read, not only MASTER.md** — FEATURE — value 4 — effort S — risk low — category: agent × missing
  Why: the pack found the MASTER.md refusal by hand; nothing says how many other files (SKILL.md, tower files, ledgers) hit the same limit. Assumption: a PostToolUseFailure hook can see the "too large" error.
  Done when: a scratch session Reading a 100k-token file adds one line (path, tokens, session) to a local refusal log, and `sampo doctor` lists the top refused paths.

- **Lint that every file the injection names fits one Read** — CLEAN — value 4 — effort S — risk low — category: agent × wrong
  Why: the injection and skills point the agent at docs, and MASTER.md is one of them yet unreadable in a single call. Assumption: Read's limit is fixed and measurable.
  Done when: the ship gate fails if any path named in SessionStart text, a skill's "see" line or a `Next:` line exceeds the Read limit, and it passes after MASTER.md is sharded.

- **Attribute injected characters by actor** — FEATURE — value 4 — effort M — risk low — category: other agents × unclear
  Why: the 2,733 characters twice and the 48–76 per-turn figures are for one session. Subagents, lanes and `sampo smith` children may each pay the same tax, and nobody has counted them. Assumption: SubagentStart receives hook output.
  Done when: `sampo burden --by-actor` prints chars per actor (main, subagent, lane, unattended child) per event over the last 7 days.

- **Make prune apply verify the plan against live state** — SECURITY — value 4 — effort M — risk med — category: unattended × unsafe
  Why: the 2.4 GB state needs a prune, and a plan made at 02:00 can go stale by apply time as lanes write. Assumption: lanes hold paths open or fresh mtimes.
  Done when: apply re-hashes each planned path's mtime and size and its lease holder, skips changed or leased ones with a named reason, and a test that races a lane write proves nothing live is removed.

- **Rehearse prune-then-resume** — FIX — value 4 — effort M — risk med — category: unattended × missing
  Why: T-2900 and T-2901 show the drive's recovery depends on old records. A pruner that removes the wrong one breaks resume silently. Assumption: resume reads ledger history older than 14 days.
  Done when: a scratch-home test fills state, prunes at the default policy, then runs a session resume and a drive tick, and both behave identically to the unpruned control.

- **Add a web UI "bytes read" footer** — PERFORMANCE — value 3 — effort S — risk low — category: web UI × slow
  Why: the web UI is the pack's only listed surface and reads ledgers directly; at 2.4 GB nobody can see which view is heavy. Assumption: views read files per request.
  Done when: each page response header and footer shows bytes read and ms, and a test fails if the home view reads more than a set ceiling on a fixture state.

- **Stamp injected facts with their age** — FIX — value 3 — effort S — risk low — category: agent × wrong
  Why: the map line carries counts like "2358 files" that go stale mid-session while the text is repeated. Assumption: some injected numbers are cached.
  Done when: every number in SessionStart text is either computed at emit time (test asserts it equals a fresh count) or removed.

- **Show the user one line saying which copy of the guard text won** — FEATURE — value 3 — effort S — risk low — category: user × unclear
  Why: once the double injection is deduped, the user cannot tell the guard text arrived. Assumption: the user would not notice a missing copy.
  Done when: the pane or status line shows "Ward text: 1 copy, hash abcd" and turns red at 0 or 2 or more.

- **Wild: Record a guard black box** — FEATURE — value 3 — effort M — risk low — category: unattended × unclear
  Why: assumption: after an incident the question is "what did the model see when the Ward decided?". Keep a ring buffer of the last 50 Ward verdicts, each with the injected-context hash and token count at that moment.
  Done when: `sampo ward replay N` prints the verdict, the command and the context hash, and survives a prune.

- **Wild: Dim the context a session never touched** — FEATURE — value 3 — effort M — risk med — category: agent × slow
  Why: assumption: injection lines whose content the session never referenced are dead weight. Drop untouched lines from the next session start of the same repo and keep an "undim" key for the user.
  Done when: after 5 sessions the injection shrinks by lines never cited in tool calls, the Ward line is exempt, and an exam run shows no pass-rate drop.

- **Wild: Fill the tmpfs on purpose** — SECURITY — value 3 — effort S — risk low — category: unattended × unsafe
  Why: the working directory is under /run/user, a tmpfs, so state and child scratch compete for RAM and a full disk is one runaway child away. Assumption: the 2.4 GB state is not on the same tmpfs.
  Done when: a drill fills the child scratch to 100%, then confirms the hooks fail open with a printed degraded line, the Ward still blocks a known-bad command, and nothing is half-written.

- **Wild: Split guard.md from the session text** — CLEAN — value 4 — effort M — risk med — category: agent × unsafe
  Why: lean cuts risk shaving a Ward clause out of prose. Keep the guard clauses in one file with a hash, outside every compression and dedupe step.
  Done when: a diff of the injection before and after any trim shows the guard file's hash is unchanged, and the gate fails if it differs without a recorded waiver.

- **Count the user's re-Reads of a sharded doc** — PERFORMANCE — value 2 — effort S — risk low — category: user × slow
  Why: assumption: sharding MASTER.md can make the agent open five shards where one Read worked before, costing more than it saves.
  Done when: a comparison of Read calls per session before and after sharding shows no increase in median, or the index is revised.

**Cells left empty:** web UI × other agents (none read the UI), web UI × unsafe (covered by earlier ideas on stale tabs and CSP), user × missing (the plan already lists bare `sampo` hints), and unattended × clear/unclear for the site (out of this Mission).

Next question: which hooks fire for subagents and lanes at all, and does the dedupe fix change what they receive?
Next question: of the 2.4 GB, which part is the user's own irreplaceable history, and which part could be rebuilt from git?
