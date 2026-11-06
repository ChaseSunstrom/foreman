# Brainstorm — lens: invented: the session that can read its own map

- **Inject a one-line map pointer instead of the SessionStart block** — FEATURE — value 5 — effort M — risk med — category: context
  Why: SessionStart injects 2,733 characters twice; the pack's Map line already carries gates, entries, layout and cards in a few hundred characters. The session can read its own map (`sampo map`) for the rest.
  Done when: a SessionStart payload for a fresh session is under 600 characters, emitted once, and a cold child given only it names the gate command and the verb for the map.

- **Fire SessionStart once per session id and source** — FIX — value 4 — effort S — risk low — category: hooks
  Why: the double injection is measured (2,733 characters twice); the double registration is the likely cause (assumption: plugin plus shim plugin both register the hook, given the foreman/sampo shim design).
  Done when: a test running the hook twice with the same session id emits the block once, and `sampo doctor` names any duplicate registration.

- **Shard MASTER.md into an index plus Read-safe sections** — CLEAN — value 5 — effort M — risk low — category: docs
  Why: MASTER.md is 75,758 tokens so Read refuses it; the session cannot read its own manual.
  Done when: every shard is under 8k tokens, a generated index lists anchors, and a test fails if any file under the docs path exceeds the Read ceiling.

- **Add `sampo doc <verb>` that prints one section** — FEATURE — value 4 — effort S — risk low — category: docs
  Why: pairs with the shards; "how do I X" is answered from anchors without reading the whole doc. Assumption: sections have stable anchors (the README already links `MASTER.md`).
  Done when: `sampo doc ward` prints under 2,000 characters and exits 2 with a did-you-mean on an unknown verb.

- **Let the session read its own context gauge** — FEATURE — value 4 — effort M — risk med — category: self-awareness
  Why: per-turn burden is 48 to 76 characters and measured by `fm burden`; the session itself can't see it. A `sampo ctx` verb reporting injected characters by source (start, per-turn, skills) lets the agent and the user judge cost.
  Done when: `sampo ctx --json` returns per-source character counts that sum to within 5% of the hook ledger for the session.

- **Guide any oversized Read with an outline** — FEATURE — value 3 — effort M — risk med — category: hooks
  Why: Read refuses MASTER.md with no fallback; the same happens to any large file in the 2,358-file tree. A PreToolUse note can point to `sampo outline <file>` (headings or defs with line ranges) when a Read would be refused.
  Done when: a refused Read of a 300k-character file yields a hook note naming `sampo outline`, and the outline fits one screen.

- **Check the Ward is intact at every start, silently** — SECURITY — value 5 — effort S — risk low — category: guard
  Why: the mission says "guard intact"; context cuts must not remove it. A 5 ms canary through the real hook path at SessionStart prints nothing when it blocks a known-bad command and one line when it doesn't.
  Done when: removing a Ward rule in a scratch home makes the next SessionStart emit a one-line warning, and the intact case emits zero characters.

- **Gate every context cut on a guard-clause index** — SECURITY — value 4 — effort M — risk low — category: guard
  Why: shrinking injected text could drop Ward wording the model relies on. Index each guard clause to the injected line that carries it.
  Done when: the ship gate fails when a cut removes a line that a clause entry points to without updating the index.

- **Prune the 2.4 GB state with a plan, a trash and an undo** — PERFORMANCE — value 4 — effort M — risk med — category: state
  Why: project state is 2.4 GB; hooks read ledgers. Assumption: most bytes are old transcripts and lane artifacts. Start with `sampo state du` by class, then `prune --plan`, apply to a TTL trash, never touching Ward state.
  Done when: `prune --plan` lists bytes by class, apply moves (not deletes) and `undo` restores byte-identical files, and hook bench numbers don't regress.

- **Fail the ship gate when injected context grows without a waiver** — CLEAN — value 3 — effort S — risk low — category: budget
  Why: the 48 to 76 per-turn figure and the 2,733 start figure are measured once; nothing holds them.
  Done when: a commit adding 100 characters to a hook payload fails `fm ship` unless a waiver line names the capability and its measure.

- **Wild: A cold child tries Sampo from the injection alone** — FEATURE — value 3 — effort M — risk low — category: exam — wild
  Why: assumption: a shrunk injection is only good if a fresh agent can still act on it. Run a tool-less child given only the SessionStart text and ask it to name the gate, the guard, and how to read the docs.
  Done when: the exam scores 3 of 3 on the shipped injection and fails on a planted version with the pointer removed.

- **Wild: Mute one injected line per week as a pre-registered experiment** — FEATURE — value 3 — effort M — risk med — category: lean — wild
  Why: assumption: some lines never change an outcome. Rotate through lines (never Ward ones), compare held-out outcomes, restore any that hurt.
  Done when: the ledger records the muted line, the arm comparison and a keep-or-drop verdict for one full week.

- **Wild: Leave a read trail for the next session** — FEATURE — value 2 — effort S — risk low — category: self-awareness — wild
  Why: the session that reads its own map should know which files it already opened. Stop appends a list of Reads and sizes; the next start shows only the top five unread hot files.
  Done when: a second session's start note names files the first never read, and is under 300 characters.

Next question: which injected lines does the model actually act on, as shown by transcripts, and which are never referenced after turn one?
Next question: does the sampo/foreman shim pair register hooks twice on a clean install, and does an uninstall of either leave the other working?
