# Brainstorm — lens: context per turn

- **Cache the session-start block by content hash and inject once per session id** — PERFORMANCE — value 5 — effort S — risk low — category: context budget
  Why: the request says SessionStart injects 2,733 characters twice; the earlier "Fire SessionStart once per session id" ideas never named the cache key. Hash the block and keep it in a per-session marker file, so a second registration (a shim plugin, or a resume) emits a 40-character "same as before" stamp instead of the full text.
  Done when: a test that runs two SessionStart hooks in one session id shows total injected characters ≤ 2,800 and the second run emits ≤ 80.

- **Put a per-turn byte budget table in the repo and fail the ship gate when a turn exceeds it** — CLEAN — value 4 — effort S — risk low — category: context budget
  Why: per-turn burden is 48 to 76 characters and varies. Nothing names who owns each character. Add a budget table with an owner per line (Ward liveness, task, nudge), and let `bench_hooks.py` assert the sum against it.
  Done when: adding a 100-character per-turn line makes `python3 plugin/tests/bench_hooks.py` exit non-zero and name the line.

- **Generate MASTER.md as an index of at most 3k tokens plus sections of at most 8k tokens each** — FIX — value 5 — effort M — risk med — category: docs
  Why: MASTER.md is 75,758 tokens, so Read refuses it, and the README links to it as "Docs". Keep the old `MASTER.md#anchor` links resolving through stub headings in the index.
  Done when: every file under the docs path is readable by a single Read call, and a link checker finds zero dead `MASTER.md#…` anchors.

- **Make a `sampo doc <topic>` verb that prints exactly one section** — FEATURE — value 4 — effort S — risk low — category: docs access
  Why: after sharding, an agent still needs a one-call path. This makes the injected text say "run sampo doc ward" instead of carrying the content, which moves characters out of the per-turn and start channels.
  Done when: `sampo doc ward` prints under 8k tokens and `sampo doc nosuch` lists the available topics.

- **Add a context-weight line in `sampo doctor` that splits injected characters by owner and by channel** — FEATURE — value 4 — effort S — risk low — category: observability
  Why: the gaps were found by hand on the machine ("every claim checked"). A permanent reading catches the next doubling. It should cover SessionStart, per-turn, skill descriptions and tool-result nudges.
  Done when: `sampo doctor` prints one row per channel with characters, and a doubled hook registration shows up as a red row.

- **Emit the per-turn line as a delta, silent when unchanged** — PERFORMANCE — value 3 — effort S — risk low — category: context budget
  Why: 48 to 76 characters every turn is mostly a restatement. Send it on the first turn and when the Ward state, active task or stage changes, otherwise nothing. The Ward must still fail loud when it is off.
  Done when: over a 20-turn replay with no state change, the total per-turn characters are at most the first turn's, and a Ward-off flip emits a line on the next turn.

- **Test that the Ward survives every context cut by naming each guard clause in a required list** — SECURITY — value 5 — effort M — risk med — category: guard
  Why: "guard intact" is the constraint of this mission, and cutting injected text is what could erode it. List the clauses the guard needs the model to know, and fail the ship gate if the shrunken injection loses one.
  Done when: removing a listed clause from the injection makes the test fail naming that clause.

- **Plan the 2.4 GB state prune with a dry run, a TTL trash and a class table** — FEATURE — value 4 — effort M — risk med — category: state size
  Why: project state is 2.4 GB. The standing rule is to look before deleting. Classify paths as rebuildable, ledger or keep, and apply only to the rebuildable class, moving it to a trash with an undo.
  Done when: `sampo prune --plan` prints bytes per class, apply moves only rebuildable files, and `sampo prune --undo` restores them byte for byte.

- **Cap hook-path output size per event in the bench and record it with the timing** — PERFORMANCE — value 3 — effort S — risk low — category: hooks
  Why: the bench times hooks (`--runs 20`) but the mission also names characters. One file that records milliseconds and characters per event makes a regression in either visible in the same diff.
  Done when: the bench output contains a characters column and the ship gate compares it against the stored ceiling.

- **Wild: Have a cold child use Sampo from the injected text alone and report what it could not do** — FEATURE — value 4 — effort M — risk low — category: injection quality
  Why: assumption: shrinking the text is only safe if a reader with nothing else can still act. Run a tool-less child on the trimmed block, ask it five tasks, and score the answers. This is wild because it prices each cut in comprehension, not just characters.
  Done when: `sampo exam inject` prints a score for the current block, and a version with the verb list deleted scores lower.

- **Wild: Mute one injected line per week as a pre-registered trial and keep it muted only if outcomes hold** — FEATURE — value 3 — effort M — risk med — category: lean experiments
  Why: assumption: some lines no longer change outcomes with strong models. A rotating mute with a declared measure, such as first-time pass rate in `fm outcomes`, finds them. Ward lines are exempt.
  Done when: the ledger holds a mute record naming one line, the measure and the week, and a settle record shows the verdict.

- **Wild: Show a "weight card" in the pane that prices each injected line in characters and in how often the model referenced it** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: the user asks for lean and sees only totals. A card that lists the dead-weight lines makes the cut list obvious and shareable.
  Done when: the pane shows the top five heaviest unreferenced lines, each with a character count.

- **Give non-Claude harnesses a smaller start card than Claude Code gets** — FEATURE — value 3 — effort S — risk low — category: harness fit
  Why: the project says it is not specific to Claude Code; Codex and Gemini have no pane or tool rows, so any text about those surfaces is wasted there.
  Done when: the start block for a Codex session omits the pane text and measures at least 30% shorter than the Claude one.

Next question: which injected lines does the model actually act on, measured over the real transcripts and not guessed, and does that set stay stable across models?
Next question: when the state pruner and the Ward are both fail-open, which of them runs first on a full disk, and what does the user see?
