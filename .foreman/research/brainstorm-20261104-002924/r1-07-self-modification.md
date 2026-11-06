# Brainstorm — lens: self-modification

- **Emit each SessionStart payload once per session** — FIX — value 4 — effort S — risk low — category: context
  Why: the pack says SessionStart injects the same 2,733 characters twice. Assumption: two registered hooks, or a resume/startup double fire.
  Done when: a recorded SessionStart for startup and for resume yields exactly one copy of the payload, and a test fails if a hash repeats in one session.

- **Shard MASTER.md into a generated index and per-area files** — CLEAN — value 5 — effort M — risk low — category: docs
  Why: MASTER.md is 75,758 tokens, so Read refuses it, and the README links to it as "Docs". The shards come from the verb table and anchors, so no hand-edited copy can drift.
  Done when: every generated shard reads under 20k tokens, the index is under 4k, and `fm doctor` goes red if any file Sampo tells an agent to read exceeds the Read limit.

- **Gate self-edits to guard and hook files on a verdict-diff** — SECURITY — value 5 — effort M — risk med — category: guard
  Why: the mission says "guard intact", and the standing rule orders the guard step first. The guard exam and the list of past blocked commands already exist.
  Done when: a lane patch that turns any block into an allow, or touches a guard or hook path without a recorded core yes, fails `fm ship` with the offending command named.

- **Ratchet every self-change against the hook benchmark** — PERFORMANCE — value 4 — effort S — risk low — category: speed
  Why: `plugin/tests/bench_hooks.py --runs 20` is already a listed gate, but nothing compares one change to the last. Assumption: the gate checks a fixed bar rather than the delta.
  Done when: a patch that adds more than 10% to the median or p95 of any hook fails the gate and prints the before and after numbers.

- **Replay recorded hook payloads through the old and new hook** — FEATURE — value 4 — effort M — risk low — category: safety
  Why: lanes edit the code the hooks run on, and a bad import in a hook fails every session. The ledgers hold real payloads.
  Done when: `fm hooks diff` replays the last 200 payloads, prints any output that differs between HEAD and the working tree, and ship refuses an unexplained diff.

- **Compile injected text from one source with a character budget** — CLEAN — value 4 — effort M — risk low — category: context
  Why: per-turn burden is 48 to 76 characters and session start is 2,733 characters, spread across several writers. A single compile step with a hard budget stops them growing again.
  Done when: all injected strings come from one file, each tagged with a source id, and the build fails when the SessionStart total or the per-turn maximum exceeds its stored ceiling.

- **Prune the 2.4 GB state by tier, with a dry run and an undo** — PERFORMANCE — value 4 — effort M — risk med — category: state
  Why: the pack reports project state at 2.4 GB. Assumption: transcripts and lane worktrees dominate it, and `fm drill --restore` exists to prove an undo.
  Done when: `fm gc --plan` lists bytes per class, `fm gc` frees at least 1 GB on a copy of the state, `fm doctor` is still green afterwards, and the undo restores the original.

- **Wild: Compress prose with a local model and accept it only if a quiz still passes** — FEATURE — value 4 — effort L — risk med — category: docs
  Why: assumption: the jarvis qwen models can rewrite MASTER.md sections and skill descriptions shorter. A second child answers 20 questions per section from the compressed text alone, and the rewrite is accepted only if the answers match those given from the original.
  Done when: one shard shrinks by at least 30% with quiz accuracy unchanged, and a deliberately lossy rewrite fails the quiz.

- **Wild: Mute one injected line per week as a pre-registered experiment** — FEATURE — value 3 — effort M — risk med — category: lean
  Why: no measurement ties any injected line to an outcome. Per the lean-substance rule, growth waits for a measurement.
  Done when: each experiment writes its stop rule first and a result row after seven days, a line whose removal shows no change in `fm outcomes` is deleted, and a line that coincides with a regression is restored.

- **Wild: Regenerate the shipped docs and injections from source and diff them (quine check)** — CLEAN — value 3 — effort S — risk low — category: drift
  Why: the README, MASTER.md and the site duplicate facts (the skills card, the hook notes). A rebuild-and-diff step catches drift without a model.
  Done when: `fm doctor` rebuilds the index, injections and verb list and goes red naming the first differing line when committed text differs.

- **Wild: Make the guard test itself with mutants of its recent blocks** — SECURITY — value 4 — effort M — risk low — category: guard
  Why: the guard must survive self-edits. A zero-token mutator (quoting, env prefixes, `bash -c`, path aliases) applied to the last 50 real blocks should stay blocked after every change.
  Done when: a seeded regression that lets one mutant through fails the suite and names the mutant.

- **Budget skill descriptions and flag low-trigger skills** — CLEAN — value 3 — effort S — risk low — category: context
  Why: `plugin/skills/` holds 1,396 files, and a `cc-skill-descriptions` card exists. Descriptions load into context every session.
  Done when: a lint caps description characters per skill and in total, and lists skills never triggered in 30 days of ledger as proposed removals.

- **Print the install-versus-source hash drift at session start only when it differs** — FIX — value 3 — effort S — risk low — category: reliability
  Why: assumption: self-modification lands in the repo but the installed copy lags, so sessions run old hooks silently.
  Done when: a stale install produces one line naming the command that refreshes it, and a matching install adds zero characters.

Next question: which injected strings or standing-rule texts has the model quoted or acted on in the last 30 days, so deletion can start with the ones it never used?
Next question: what happens when a lane's own self-edit changes the benchmark or the guard exam, and who checks the checker?
