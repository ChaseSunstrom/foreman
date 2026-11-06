# Brainstorm — lens: grid

I wrote these against the grid below. The pack's surfaces line lists only the web UI, so I added the CLI, hooks and Ward, the site, and lanes from the entry points. Several of the cells I chose sit near ideas already on the slate, and each Why line says what is different. I checked none of this on the machine, so every assumption is marked.

**Grid.** The columns are missing, wrong, slow, unsafe and unclear.
- **Rows:** hook, CLI, state dir, web UI and site.
- **Actors:** user, agent, other agents or lanes, and unattended runs.

**Cells left empty:**
- Site × lanes (lanes never touch the site).
- Web UI × unattended × missing (already covered by existing card ideas).
- CLI × user × missing (nothing in the pack suggests a missing verb).

- **Name the two hook entries behind the double SessionStart** — FIX — value 4 — effort S — risk low — category: hooks
  Cell: hook × user × unclear.
  Why: the pack says 2,733 characters are injected twice, but the existing ideas stop at "find who registers it twice". `doctor` should tell the user which two registrations fire and what clears the second. Assumption: the second copy comes from the thin `foreman` shim plus `sampo`, or from settings plus plugin.json.
  Done when: with both plugins enabled, `sampo doctor` prints a line naming the two hook sources, and after the fix prints "SessionStart: 1 registration".

- **Inject one product name only** — CLEAN — value 3 — effort S — risk low — category: injection
  Cell: hook × agent × unclear.
  Why: the rename left `fm` and `sampo` spellings both live, and the injected text probably names both. That costs characters and confuses the agent about which verb to call. Assumption: the injected text mixes the names.
  Done when: a test fails if SessionStart or per-turn text contains `fm ` or `foreman` outside a single alias note, and the injected size drops.

- **Measure the shim import tax** — PERFORMANCE — value 3 — effort S — risk low — category: hooks
  Cell: CLI × agent × slow.
  Why: T-2748 moved the code to `plugin/lib/sampo/` and left `fm*.py` shims behind. Every old-name call imports twice, and `bench_hooks.py` may not isolate this. Assumption: the shims eagerly import their targets.
  Done when: `bench_hooks.py` reports shim-path versus direct-path milliseconds, and the shim path adds under 5 ms.

- **Redirect `rm` of state to `sampo prune --plan`** — FEATURE — value 4 — effort S — risk low — category: Ward
  Cell: Ward × agent × unclear.
  Why: with a 2.4 GB state dir, an agent asked to "free space" will reach for `rm -rf`. The Ward block message should teach the safe verb rather than only refuse. Assumption: prune plan and trash verbs exist from other slate items.
  Done when: a bait command deleting a state-dir path is blocked, and the message contains a runnable `sampo prune --plan` line that parses.

- **Scan injected text for personal data before a non-local model sees it** — SECURITY — value 4 — effort M — risk low — category: privacy
  Cell: hook × user × unsafe.
  Why: SessionStart text may carry the home path, username, repo remotes or steer text, and it goes to whichever model backs the harness. Assumption: some of these appear today.
  Done when: a fixture session start containing a planted email and `~` shows both redacted or flagged in `sampo doctor`, with a test that fails if a new injected field carries one.

- **Give each harness its own injection card, tested per harness** — FEATURE — value 3 — effort M — risk med — category: devices
  Cell: hook × other agents × wrong.
  Why: Codex, Gemini and opencode have weaker or missing hooks (T-0337, T-0335), yet likely receive Claude Code's wording about hooks and mods. Assumption: the AGENTS.md and GEMINI.md exports reuse the Claude text.
  Done when: each harness card contains no reference to a hook or tool that harness lacks, checked by a per-harness name list.

- **Show a live "resume cost" line when a drive restarts** — PERFORMANCE — value 3 — effort S — risk low — category: unattended
  Cell: unattended × state × slow.
  Why: T-2900 and T-2901 show resume and wait logic is active work. A resume now reads the full 2.4 GB project state. Assumption: no one has timed it.
  Done when: the first line after resume prints milliseconds spent reading state, and a bench asserts it stays under 2 s on a fixture 5× current size.

- **Make the site's Genesis data carry a scrubbed-by-construction flag** — SECURITY — value 3 — effort M — risk med — category: site privacy
  Cell: site × user × unsafe.
  Why: a standing rule publishes `site/genesis` data on every tower change, and the steers contain the user's verbatim words, endpoint names and decisions. The steer list already holds "never show jarvis" and "never name Claude" as corrections. Assumption: the publisher has no allowlist today.
  Done when: the publish step fails on any field not on an allowlist, and a planted private-endpoint string in a steer is refused.

- **Wild: Plant a canary sentence in MASTER.md** — SECURITY — value 3 — effort S — risk low — category: docs, wild
  Cell: state/docs × agent × unsafe.
  Why: when Read refuses MASTER.md, an agent can `cat` or `sed` it through Bash and burn 75k tokens anyway, which defeats the lean goal. A unique sentence in the doc, found in later transcripts or outputs, would show that route is taken. Assumption: transcripts are scannable at no token cost.
  Done when: a scan of the last N sessions reports "full-doc reads via Bash: k" and the canary appears in the sharded index test.

- **Wild: Run a tmpfs fire drill for the child dir** — PERFORMANCE — value 3 — effort M — risk med — category: lanes, wild
  Cell: lanes × state × slow and unsafe.
  Why: this child runs from `/run/user/1000/…`, which is RAM. Lanes and children that copy state or worktrees there can exhaust it. Assumption: there is no cap today, since the pack lists none.
  Done when: filling the tmpfs to 95% makes a child spawn refuse with a named reason rather than hanging, and a test shows it.

- **Wild: Let the agent file a "what I wish I knew" note on turn 1** — FEATURE — value 3 — effort S — risk low — category: injection, wild
  Cell: hook × agent × missing.
  Why: slimming the injection removes information. Asking the agent to write one line when it needed something absent gives a free signal about what was cut wrongly. Assumption: agents will comply under a one-line prompt.
  Done when: after a cut ships, `sampo lean` lists the top 5 missing-info notes and their count per session.

- **Wild: Print a one-line "Sampo cost" on the Ward-block message itself** — FEATURE — value 2 — effort S — risk low — category: user value, wild
  Cell: Ward × user × unclear.
  Why: users see a block and cannot tell whether it came from a rule they chose. Appending "rule R, added by steer S" ties the safety cost to its justification.
  Done when: every block names its rule id and the steer or threat row it enforces, and a test covers all rules.

- **Pin MASTER.md anchors with a redirect map after sharding** — CLEAN — value 3 — effort S — risk low — category: docs
  Cell: docs × agent × wrong.
  Why: the README, skills and the site link to `MASTER.md#…`. A split would break them silently. Assumption: many such links exist across 2,358 files.
  Done when: a test resolves every `MASTER.md#anchor` in the repo to a shard file, and fails on a miss.

Next question: Which of the five (missing, wrong, slow, unsafe, unclear) has the fewest filed tasks across the whole grid, and is that because it doesn't happen or because nobody measures it?
Next question: Does the Ward behave the same when the agent is a local model (qwen3.8-27b) that the user is actively moving the orchestrator role onto?
