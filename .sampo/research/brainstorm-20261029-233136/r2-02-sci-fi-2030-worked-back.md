# Brainstorm — lens: sci-fi 2030 worked back

- **Run rewrites in shadow before they can win** — FEATURE — value 5 — effort M — risk low — category: reliability
  Why: assumption: selection by exam alone misses how a rewrite behaves on the user's real sessions. By 2030 a candidate harness runs beside the live one on real work. Today the hooks already see every event.
  Done when: `fm genesis shadow <gen>` logs what the candidate would have injected or blocked on the last N hook events, with no side effects, and prints its agreement rate with the parent and with what the user actually did.

- **Mint exam scenarios from the project's own fix and revert commits** — FEATURE — value 5 — effort M — risk med — category: exam
  Why: the pack's exam is generated (`fm exam gen`). A 2030 exam grows from reality, and `git log` already holds planted-gap-quality failures with a known fix.
  Done when: `fm exam mine` turns ≥3 fix or revert commits into scenarios (parent checkout as the start, fix diff as the hidden key). The oracle passes them and the empty arm fails them.

- **Replay proposed guard rules against past command logs first** — SECURITY — value 4 — effort M — risk low — category: guard
  Why: the guard is a core feature, and a self-writing harness will want to add rules. A rule that blocks real past work is worse than none. Assumption: transcripts and hook logs keep enough commands to replay.
  Done when: a candidate guard rule prints "would have blocked K of N past commands" with the examples, and cannot be enabled without that report.

- **Give every self-written rule a half-life** — CLEAN — value 4 — effort S — risk low — category: simplicity
  Why: T-0794 (slim Foreman) and the skill-listing budget show bloat is a live pain. A harness that writes rules without retiring them gets heavier every generation.
  Done when: each tower rule records its last firing and hit count, and `fm genesis prune` lists rules unfired for 60 days as deletion candidates, with the evidence.

- **Fail a generation whose injected text exceeds a context budget** — PERFORMANCE — value 4 — effort S — risk low — category: performance
  Why: the user asked for skills "within the skill-listing budget", so Genesis's own output competes for the same space. Assumption: gen-0 and its rules are injected into every session.
  Done when: `fm genesis status` shows tokens injected per session for the current generation, and a rewrite that raises the figure past the set cap cannot be selected unless it closes more scenarios per token.

- **Answer "why does this rule exist" from lineage** — FEATURE — value 4 — effort M — risk low — category: docs
  Why: the pack's tower-archaeology ideas cover resuming and diffing. A fresh session still can't ask about a single rule. Rule-level provenance is the 2030 expectation for a self-written harness.
  Done when: `fm genesis why "<rule text or id>"` prints the generation that introduced it, the scenario or user steer that justified it, and the rewrites that touched it. It exits non-zero for a rule with no recorded source.

- **Compile each capability-spec MUST into a runnable check** — FEATURE — value 5 — effort L — risk med — category: spec
  Why: a spec that is only prose can't tell a tower it is done. Today the pieces exist: `fm exam` keys, `fm doctor` gates. Assumption: most MUSTs map to a command or a grep.
  Done when: `fm genesis spec --coverage` lists every MUST as `checked` (with its command) or `unverifiable`, and the tower refuses to call a capability closed on an `unverifiable` MUST alone.

- **Approve auto-start from your phone with a one-tap link** — FEATURE — value 3 — effort M — risk med — category: devices
  Why: the auto-start rule is protected core and needs the user's yes, and the user is rarely at the terminal when the queue runs dry. Assumption: a local-only web UI (already in `plugin/templates/web`) can sit behind the user's own tailnet or LAN.
  Done when: a queue-dry proposal appears as a signed one-time link on the local web UI, and one tap records the yes and starts the run. An expired or replayed link does nothing.

- **Pre-run the user's likely next ask in a throwaway lane** (wild) — FEATURE — value 4 — effort L — risk med — category: agents
  Why: the "asked" history shows the next ask is often a sibling of the last one (site stale → favicon stale → fm code section stale). Spare quota could start the sibling work unasked, in a discarded worktree.
  Done when: after a task closes, one speculative spike is queued in a lane marked `speculative`. A matching later ask adopts it, and a non-matching one is deleted with no merge and no push.

- **Run a Seed bracket that animates on the tower page** (wild) — FEATURE — value 3 — effort M — risk low — category: delight
  Why: assumption: the Seed is the highest-leverage choice, yet only one is tried. 2030 would race 4 Seeds on the same exam as a tournament. The tower page is already live and interactive.
  Done when: 4 Seeds run on one exam in parallel lanes, the page shows a bracket with each match's closed-scenario counts, and the winner is recorded in lineage with the losers' verdicts.

- **Speak a 60-second morning briefing from the tower, locally** (wild) — FEATURE — value 2 — effort M — risk low — category: delight
  Why: assumption: the overnight digest is read less than it would be heard. A local TTS engine keeps it on the owner's hardware.
  Done when: `fm genesis brief --audio` writes a ≤60 s audio file from the digest text with a local engine and no network call. The text and the audio match line for line.

- **Emit the capability spec as a human-readable contributor guide** (wild) — FEATURE — value 3 — effort S — risk low — category: docs
  Why: a capability spec "complete for this kind of project" is what a new human teammate needs too. Assumption: the spec is clear enough for a person to read.
  Done when: `fm genesis export --human` writes a CONTRIBUTING-style page from the spec. It drops the internal exam and lineage jargon, and every MUST appears as a plain sentence.

- **Report the tower's health from the statusline, not a command** — FEATURE — value 3 — effort S — risk low — category: observability
  Why: the Foreman pane and `fm genesis status` exist, but a 2030 harness is ambient. Assumption: the statusline is a cheap surface to read.
  Done when: the statusline shows one glyph and a count (e.g. `gen 3 · 41/52 · ◌ idle`) and flips to a warning when the tower stalls, the budget is near, or a proposal waits for a yes.

Next question: Which of the tower's decisions can be replayed deterministically from the journal, so a rewrite's win can be checked without any model call?
Next question: What does a second user on the same machine, with different MUSTs, do to a tower and its carried-over defaults?
