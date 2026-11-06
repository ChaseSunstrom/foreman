# Brainstorm — lens: inversion: how finishing fails — stops early, calls it done when it merely stopped, loses the plan to a compaction or crash, plans an incomplete version, drifts off the goal, gold-plates forever

- **Materialize the goal card on every ledger write** — PERFORMANCE — value 4 — effort S — risk low — category: hooks
  Why: hooks must pass the bench_hooks gate, and context over ~10 KB becomes a preview. Re-deriving the card from the ledger and contents list in SessionStart and Stop on every call is the slow and oversized path.
  Done when: the card is written to a file under the 10 KB cap on each goal write. Hook reads of it cost one file read, and bench_hooks shows no regression with 200 goal items.

- **Cache done-when verdicts by the tree hash of their inputs** — PERFORMANCE — value 4 — effort M — risk med — category: stop gate
  Why: the Stop drive and `fm task finish` re-run every criterion's verify command, and the full suite is ~4400 tests. Most criteria cannot have changed between drive rounds.
  Done when: a second Stop with no edits runs zero verify commands. Editing a covered file re-runs exactly the criteria that name it, and a test proves a cached green is never served after an edit.

- **Switch the drive's strategy when a round changes nothing** — FEATURE — value 4 — effort M — risk low — category: stop drive
  Why: DRIVE_MAX and the no-progress stop end a session by counting. They never change what the next round asks, so a stuck goal burns its rounds on the same prompt.
  Done when: after a round with an unchanged tree hash, the next drive prompt differs in kind (narrower step, different open item, or a replan request). A fixture with a stuck item shows three distinct prompt shapes before the stop.

- **Interleave the finish tail into every task** — FEATURE — value 5 — effort M — risk med — category: planning
  Why: gen-0 MUST lists tests, exam scenarios, docs, site page, pane and surfaces. Sessions that stop early drop exactly these because they sit last. Assumption: the tail is what gets cut most often.
  Done when: opening a goal generates, per contents row, a stub for each applicable tail item (docs, site, pane, surface). `fm task finish` refuses a row with a missing stub, and the goal can't show 100% while any stub is empty.

- **Plant a compaction canary in the goal card** — FEATURE — value 3 — effort S — risk low — category: compaction
  Why: PreCompact saves a "Resume here" section, but nothing checks the model still holds the goal afterwards. Assumption: summaries can drop the goal silently.
  Done when: the card carries a short random token. The next UserPromptSubmit after a compaction checks the visible context for it and re-injects the full card if absent. A test simulates a compaction that drops the token and sees the re-injection.

- **Watch hookless agents from outside** — FEATURE — value 4 — effort M — risk med — category: devices
  Why: Codex, Gemini and opencode get shims (fmagents.py) but likely lack a Stop hook. Assumption: for them "stopped" has no verdict today.
  Done when: `fm serve` notices a shim agent process exiting, writes a stop-cause and done-vs-stopped verdict from the goal ledger, and `fm resume` shows it. A killed fake agent yields "stopped" and not "done".

- **Resume a goal on a different surface than it started on** — FEATURE — value 4 — effort M — risk med — category: surfaces
  Why: the MUST says everything works on every surface, but resume is only exercised in one at a time. A goal that dies in Claude Code and continues in `fm code` hits untested paths.
  Done when: an exam scenario kills a goal mid-way on one surface and resumes on another. The first action on the second surface matches `fm goal step` from the files, and this is run for each pair of surfaces.

- **Extract non-goals from the user's words and check them at close** — FEATURE — value 3 — effort M — risk low — category: drift
  Why: drift checks trace tasks to contents rows, but nothing records what the user said not to build, such as "never ask me anything". Gold-plating and off-goal work both look like progress.
  Done when: NEVER/"don't"/"without" phrases become quoted non-goal rows. The closing audit lists any diff hunk or new verb that touches one, and a planted violation is flagged.

- **Grid stop cause × goal phase × surface like coverage.md** — CLEAN — value 4 — effort M — risk low — category: coverage
  Why: the Genesis coverage grid (1408/1408 cells) works for capabilities. Finishing failures are enumerable the same way (usage limit, crash, drive cap, "done" claim, compaction) against phases (planning, mid-task, closing audit).
  Done when: `fm genesis check` validates a failure grid where every cell names an exam scenario or a not-yet entry, and an empty cell fails the check.

- **Wild: Hold a "what would make me stop" pre-registration** — FEATURE — value 3 — effort S — risk low — category: planning
  Why: assumption: stops are chosen implicitly by fatigue and cost. Writing the stop rule when the goal opens (budget, a dry-round count, a marginal-value cutoff) makes "stopped" and "finished" separable later.
  Done when: a goal can't start without a sealed stop rule, and the end verdict quotes which rule fired, or says none fired.

- **Wild: Play a goal's end state back as a mock release note before work starts** — FEATURE — value 3 — effort M — risk low — category: planning
  Why: incomplete plans are the failure the user pushes against. Writing the finished "CHANGELOG entry and site page" first exposes missing rows early, and the note then becomes the closing audit's checklist.
  Done when: a goal can't leave planning without a drafted CHANGELOG entry. Each claim in it maps to a contents row, and an unmapped claim blocks the plan.

- **Wild: Say the goal's status aloud on request** — FEATURE — value 2 — effort S — risk low — category: voice
  Why: assumption: a user away from the terminal (phone, car) wants "done, stopped, or stuck, and what's next" in one breath. `fm goal say` renders the card as a ≤20-second script for a local TTS engine, and nothing leaves the machine.
  Done when: the command prints a script under 60 words naming the verdict, distance and next action, and a test checks it contains the stop cause.

- **Wild: Run a quarantine twin that re-closes each done goal on a fresh clone** — FEATURE — value 4 — effort L — risk med — category: verification
  Why: "done" can rest on state that only exists in the working directory (untracked files, an uncommitted fixture). Re-running the done-when commands on a clean checkout exposes that.
  Done when: closing a goal runs its criteria in a throwaway clone. A planted untracked-file dependency fails the clone run and blocks the close.

Next question: What do the first five minutes of a goal's resume cost in tokens and hook time on a ledger with hundreds of items, and where is the shed order when the card exceeds 10 KB?
Next question: Which stop causes are visible on a surface with no hooks at all (Desktop, Codex), and who writes the verdict when nothing is running to write it?
