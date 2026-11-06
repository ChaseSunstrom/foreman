# Brainstorm — lens: unspoken needs

- **Cluster captured messages into one task on arrival** — FEATURE — value 5 — effort M — risk med — category: capture
  Why: T-0755 to T-0760 are six S-sized captures from one stream of thoughts, and the user had to ask "put them into one task/milestone" by hand. `fm batch` exists but only runs on request. T-0760 also duplicates the request.
  Done when: sending 4 related messages in one session yields one batch with duplicates merged. A one-line digest, "I read your 4 messages as: …", appears, and the user can split it with one command.

- **Keep the full raw prompt on every capture** — FIX — value 4 — effort S — risk low — category: capture
  Why: T-0756 stored "also, the …" and was dropped because no transcript held the rest. Capture truncates, so the user's actual words are lost. Assumption: the full text is available in the UserPromptSubmit payload.
  Done when: capturing a 3,000-character prompt stores it verbatim, and a prompt that ends mid-sentence is flagged "possibly cut off" in the captured task.

- **Turn complaints into regression tests** — FEATURE — value 5 — effort M — risk med — category: self-repair — wild
  Why: "can you make sure it doesnt sit idle" and "it will start working on different steps without updating the step" are complaints about Foreman itself. They arrive as ordinary S captures with no repro. Assumption: complaint phrasing is detectable (words like "noticed", "again", "doesnt").
  Done when: a prompt matching a complaint pattern auto-creates a FIX against Foreman with the transcript excerpt attached. Closing it requires a test that fails on the old behavior.

- **Look up won't-fix precedent at capture** — FEATURE — value 4 — effort S — risk low — category: decisions
  Why: There are three or more dropped guard reports (heredoc writes, `python -c` imports, `$_` args), each closed "working as intended" with reasoning that was later re-derived. `fm decide` holds the answers but nothing consults it when a similar FIX arrives.
  Done when: capturing a FIX that matches a recorded won't-fix decision shows the precedent and its reason, and offers a one-step close.

- **Park questions instead of stopping** — FEATURE — value 5 — effort M — risk med — category: autonomy
  Why: The user wants no idling and no hand-me-commands, yet an ambiguous criterion blocks the run. Assumption: blocks are partly question-driven, not only permission-driven.
  Done when: a task with an unresolved question is marked "parked with question", the queue advances to the next task, and all parked questions appear in one batch at the next stop or digest.

- **Compile vague mandates into measurable targets** — FEATURE — value 5 — effort M — risk med — category: planning
  Why: "super improve … smarter, faster, better, etc." (T-0760) has no done criterion. Foreman already has bench, scorecard, hook latency and first-time-pass data to anchor one.
  Done when: a mandate-style request produces 4–6 numeric targets drawn from existing metrics. A before/after table is written at close, and the task can't close with a target unmeasured.

- **Draft releases from finished tasks** — FEATURE — value 4 — effort M — risk med — category: release
  Why: Releases 1.2.17–1.2.27 were each requested by hand in the form "Release X (T-a to T-b) to GitHub main and JARVIS". Assumption: the task range and milestone names are derivable from the ledger. The publish step is outward-facing, so it needs one confirmation.
  Done when: `fm release propose` outputs the task range, changelog text, a before/after metrics receipt and gate results in one preview. Nothing is published until the user approves.

- **Generate the self-docs inventory from the CLI** — FIX — value 3 — effort S — risk low — category: docs
  Why: T-0686 left `fm bisect` out of MASTER.md and the `fm doctor` self-docs check failed. A hand-maintained command list drifts.
  Done when: adding a subcommand without docs fails at task close with a generated patch for the missing MASTER.md entry, and the patch applies cleanly.

- **Make debug-scaffolding scans syntax-aware** — FIX — value 3 — effort S — risk low — category: scanners
  Why: The scan flagged CHANGELOG.md:10 (T-0695) and a string literal in test_execution.py:102 (T-0746). That is two false positives of one kind.
  Done when: debug calls named in Markdown, comments, or string literals are not flagged, a real call in code still is, and both earlier cases are fixtures.

- **Report interrupted work after Esc** — FEATURE — value 4 — effort M — risk med — category: trust
  Why: Foreman resumes at the exact step after `/compact`, but a user interrupt mid-edit is the one case where steps and files can disagree. This ties to the step-drift complaint. Assumption: interrupts are visible through hook events or tool-result gaps.
  Done when: after an interrupt, the next prompt gets a short note listing the step state and uncommitted files that step touched, and marks the step "interrupted, unverified".

- **Explain why it went idle** — FEATURE — value 4 — effort S — risk low — category: observability
  Why: The user said it "sits idle" and no one has diagnosed the cause. A wake mechanism treats the symptom without classifying it. Assumption: causes include turn ended with a non-empty queue, waiting on a subagent, waiting on a permission prompt, or a rate limit.
  Done when: `fm doctor` lists the last 7 days of gaps over 60 seconds with a labeled cause each, and the top cause is shown first.

- **Resolve the user's shorthand to known targets** — FEATURE — value 3 — effort S — risk low — category: language — wild
  Why: Requests use "JARVIS", "Frontier 11", and "GitHub main and JARVIS" as undefined shorthand. Assumption: they map to fixed deploy targets and roadmap items.
  Done when: Foreman keeps a glossary learned from past tasks, expands those terms in plans, and asks once when it meets an unknown term, then remembers the answer.

- **Argue against the plan before large tasks** — FEATURE — value 3 — effort M — risk low — category: planning — wild
  Why: The pack shows steers saying earlier rounds felt "not revolutionary", and a dropped Frontier 02 only after measurement showed no gain. Assumption: a cheap haiku-tier skeptic can challenge a plan's premise (does the host already do this?) before work starts.
  Done when: each L-tier plan gets a one-paragraph "what already exists / what would make this unnecessary" check, and a plan whose premise fails is flagged before step 1.
