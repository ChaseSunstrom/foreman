# Brainstorm — lens: grid

- **Flag a spec-versus-code conflict instead of building to the example** — FEATURE — value 4 — effort M — risk low — category: meaning
  Cell: CLI × agent × wrong.
  Why: assumption: spec examples are sometimes the stale side. Meaning is the largest unproven class (599), and compiling examples into criteria will force code to match a wrong example. Run each example on the parent commit. If it fails there and the doc isn't the thing the user changed, record a "conflict" verdict, ask once with a default, and build nothing.
  Done when: a planted stale example in a fixture spec produces a conflict record and no code change.

- **Lint criteria for tautologies** — FIX — value 4 — effort S — risk low — category: proof quality
  Cell: Smith TUI × weak local model × wrong.
  Why: assumption: small local models write checks like `grep` for the string they just wrote or `x == x`. A static pass over the compiled criterion rejects self-referential or constant assertions before it is filed.
  Done when: a fixture set of 10 tautological criteria is all rejected and 10 real ones all pass.

- **Redact secrets from extracted examples** — SECURITY — value 3 — effort S — risk low — category: privacy
  Cell: CLI × user × unsafe.
  Why: assumption: a pasted spec can contain tokens or private hostnames. Criteria are stored verbatim and later exported to the site, so redact at extraction time, not at publish.
  Done when: a spec containing a fake token yields a stored criterion with the token masked and the criterion still runs.

- **Run each criterion across an environment matrix** — FEATURE — value 3 — effort M — risk low — category: meaning
  Cell: CLI × agent × unclear.
  Why: assumption: an example that passes only from one cwd, locale, timezone or unset HOME is a different claim from the one written. Run in 3 shifted scratch environments and label divergent ones "environment-bound" rather than proven.
  Done when: a criterion that reads the cwd is labelled environment-bound; an independent one stays proven.

- **Close provisionally and flip the verdict late** — FEATURE — value 4 — effort M — risk med — category: latency
  Cell: hooks × agent × slow.
  Why: the Stop gate can't afford slow criteria, and a timeout is already "unproven". Add a "proving…" close state that finishes in the background, then flips to proven or reopens the task and tells the next session.
  Done when: a 60-second criterion lets the Stop hook return in under 2 seconds, and a failing late result reopens the task.

- **Put a price and a prove-now button on every unproven label** — FEATURE — value 4 — effort M — risk low — category: web UI
  Cell: Web UI × user × unclear.
  Why: an unproven shelf says what isn't proven but not what proving it would cost. Show seconds, tokens and the exact `sampo` command. The button only prints or queues that command, so the UI proposes and the CLI disposes.
  Done when: every shelf row shows a cost estimate and a copyable command, and none runs without a CLI call.

- **Weight `fm next` by the age of unproven closes** — FEATURE — value 3 — effort S — risk low — category: queue
  Cell: CLI × unattended × missing.
  Why: assumption: an unattended drive keeps closing new work while old claims stay unproven. Raise a task's priority by the days its unproven claims have gone unchecked, so debt gets paid without a separate brake.
  Done when: in a fixture queue a 10-day-old unproven close outranks a fresh S task.

- **Render hook-injected notes through the role table** — FIX — value 4 — effort M — risk low — category: neutrality
  Cell: hooks × other agents × wrong.
  Why: the standing rule says Sampo is not Claude-specific, but injected notes and `Next:` lines may still name Claude, the user's machine or vendor models. Docs lint doesn't cover runtime strings. Scan every string a hook or verb emits and fail on forbidden names.
  Done when: a test that runs each hook with Codex-, Gemini- and opencode-shaped payloads finds no vendor or host name in the output.

- **Hash the spec line behind each criterion** — FEATURE — value 3 — effort S — risk low — category: staleness
  Cell: docs × agent × wrong.
  Why: assumption: a criterion outlives the sentence it came from. Store the source line's hash with it. If the line changes, mark the criterion "source changed" instead of passing or failing it.
  Done when: editing one spec sentence flips exactly its criterion to "source changed".

- **Detect contradictory criteria between lanes** — FEATURE — value 3 — effort M — risk med — category: lanes
  Cell: other agents × lanes × wrong.
  Why: parallel lanes (the user's Missions 5–8 steer) each compile examples from overlapping specs. At merge, run every lane's criteria against every other lane's tree and list the pairs that disagree.
  Done when: two fixture lanes with opposite examples for one verb are flagged at merge and not silently landed.

- **Normalise paths in stored evidence at record time** — SECURITY — value 3 — effort S — risk low — category: privacy
  Cell: unattended × user × unsafe.
  Why: the user's rule is that public surfaces never name their machine. Evidence kept from "a run" holds /home paths and hostnames, which leak later through the site export. Rewrite them to `~` and `$REPO` when recorded.
  Done when: a ledger scan after a fixture run finds no absolute home path or hostname.

- **Record a human-witnessed proof class** — FEATURE — value 4 — effort S — risk low — category: meaning
  Cell: web UI × user × missing.
  Why: some meaning claims only the user can check ("this reads right"). One key marks a claim "witnessed by user on date", a class separate from machine-proven. It expires when the cited files change.
  Done when: witnessing a claim shows it as a distinct class and a change to its cited file clears it.

- **Downgrade an unproven claim to the strongest sentence that is proven** (wild) — FEATURE — value 4 — effort M — risk med — category: docs
  Cell: docs × user × unclear.
  Why: wild: instead of only hatching a claim as unproven, propose a weaker rewording that the existing checks do prove ("exits 0 on the fixture" in place of "works"). The user accepts or keeps the original unproven.
  Done when: for 20 flagged claims, at least half get a rewording whose checking command passes.

- **Predict the output before running it** (wild) — FEATURE — value 3 — effort M — risk low — category: docs
  Cell: docs × agent × wrong.
  Why: wild: a tool-less child sees only the docs and guesses what each documented command prints. The real output is diffed against the guess. A mismatch marks the doc misleading, which finds meaning errors that never fail a test.
  Done when: a fixture doc with one wrong example is the only one whose prediction diverges.

- **Add a "which orchestrator?" mystery guest to demos** (wild) — FEATURE — value 2 — effort S — risk low — category: neutrality
  Cell: site × other agents × unclear.
  Why: wild: every site scene picks its orchestrator label from a rotating role name at build time. If the page reads the same for any label, the neutrality claim has a visible proof.
  Done when: building the site with three different labels yields pages identical apart from that one word.

Cells left empty:
- unattended × agent × unsafe, because the existing ideas already cover sealing criteria and the guard.
- web UI × unattended × slow, because a last-good snapshot idea is already listed.

Next question: Which of the 599 meaning-class items does the user's later behaviour (re-asking, editing, dropping) show were wrong, and what do those share?
Next question: Can a spec example be compiled into a criterion by a zero-token parser for the three most common formats, or must a model always write it?
