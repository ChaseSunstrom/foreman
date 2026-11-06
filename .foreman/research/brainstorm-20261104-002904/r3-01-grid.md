# Brainstorm — lens: grid

- **Hold one spec example out of the brief** — FEATURE — value 5 — effort M — risk low — category: meaning
  Cell: CLI × agent × wrong (overfitting to the examples it was shown).
  Why: Meaning is the largest unproven class (599), and runnable criteria from spec examples can be satisfied by hard-coding the visible examples. Nothing above withholds any.
  Done when: with 3 or more examples in a spec, one is withheld from the builder's brief and runs at close. A planted stub that hard-codes the visible examples fails it.

- **Check that every literal survives into the criterion** — FIX — value 4 — effort S — risk low — category: meaning
  Cell: spec text × agent × wrong (the extractor misreads an example).
  Why: A zero-token guard on plan-time extraction. Every number, string and path in a spec example must appear verbatim in its generated criterion, or the criterion is marked unproven.
  Done when: a planted criterion that drops or alters one literal is rejected with the missing literal named.

- **Annotate doc reads with their unproven lines** — FEATURE — value 4 — effort M — risk med — category: docs claims
  Cell: docs × agent × wrong (an agent acts on a stale claim in MASTER.md or README).
  Why: 421 doc claims are flagged, but the agent that reads those docs never sees the flag. A read hook could prepend "lines 40–52 unproven" when the file is opened.
  Done when: reading a doc with N unproven claims yields an injected note of at most 3 lines naming the line ranges, and a file with none yields no note.

- **Render injected skill and hook text per detected host** — FIX — value 4 — effort M — risk med — category: orchestrator-neutral
  Cell: skills and hooks × other agents × wrong.
  Why: The steer is that any orchestrator must work. Skill bodies and hook notes likely still name Claude Code tools and slash commands, which misleads Codex, Gemini CLI and opencode.
  Done when: rendering the skill set for a fake non-Claude host yields no Claude-only tool names or `/foreman:` spellings. A lint runs this at ship.

- **Lease ports and scratch homes to each lane's proofs** — FIX — value 4 — effort M — risk low — category: reliability
  Cell: lanes × unattended × wrong and slow (proofs collide).
  Why: Criteria that start the web UI or use a scratch home will collide when parallel lanes (Missions 5–8) run them at once, giving false fails that read as unproven. Assumption: today's proofs don't allocate ports.
  Done when: two lanes running a web-UI proof together both pass, each on its own port and home. A forced collision is reported as "resource busy", never as a failure.

- **Fail any web UI proof that binds beyond loopback** — SECURITY — value 3 — effort S — risk low — category: web UI
  Cell: web UI × unattended × unsafe.
  Why: An unattended run that starts the server to prove something must not expose it. This is cheap to check with a socket listing during the proof.
  Done when: a planted server bound to 0.0.0.0 fails its proof with a named reason, and a loopback bind passes.

- **Show proof progress with an ETA from past runtimes** — FEATURE — value 3 — effort M — risk low — category: delight
  Cell: pane × user × slow, and unclear while waiting.
  Why: A run's proofs can take minutes with no signal, and a timeout then reads as unproven. A "running 40 s of about 90 s" row separates slow from stuck.
  Done when: the pane shows each in-flight proof with its elapsed time against the median of its last 5 runs. A proof with no history shows "no baseline".

- **Escalate proof tier when the user doubts** — FEATURE — value 4 — effort M — risk med — category: trust (wild)
  Cell: user × agent × unclear.
  Why: Phrases like "are you sure" or "did you actually run that" show the user didn't trust the last verdict. Escalating to the strongest available proof, and recording which tier ended the doubt, turns doubt into calibration data.
  Done when: a doubt phrase after a close triggers a re-prove at the next tier up. The ledger row records the tier the user accepted.

- **Print a generated proof badge in the README** — FEATURE — value 3 — effort S — risk low — category: public surface (delight)
  Cell: site and README × user × unclear.
  Why: Proven/unproven counts by class are computed, not typed. A badge or one-line table near the header that links to the unproven shelf shows the honesty directly.
  Done when: the README's counts come from a command and a test fails if the typed and computed numbers differ.

- **Run proofs only on the product's own role names** — CLEAN — value 3 — effort S — risk low — category: public surface
  Cell: bench and scene output × other agents × wrong (the machine and vendor names the user already pushed back on).
  Why: A role table exists in ideas above, but nothing sets the rule at write time. Every generator that emits into site/ or README must take names from the table and cannot accept a free string.
  Done when: the generators have no free-text name argument, and a test feeding "jarvis" or a vendor model name to one is rejected.

- **Reconstruct the README from the proof ledger alone** — FEATURE — value 4 — effort M — risk low — category: docs claims (wild)
  Cell: docs × agent × missing.
  Why: A tool-less child sees only the ledger of proven claims and writes the product's description. Sentences in the real README with no counterpart in that description are exactly the claims no run backs.
  Done when: a report lists README sentences missing from the reconstruction, and its count correlates with the flagged 421.

- **Put one unproven sentence a day on the site with a "prove this" request** — FEATURE — value 3 — effort M — risk med — category: delight (wild)
  Cell: site × user × missing.
  Why: Making the labelled gap visible and actionable turns the unproven shelf into a shared to-do. Assumption: the site can queue a request through the existing publish path.
  Done when: the site shows one unproven claim chosen by age, and a request from it appears as a filed task in the next drive tick.

- **Hide the answer key from the builder, the full version** — FEATURE — value 4 — effort L — risk med — category: meaning (wild)
  Cell: lanes × agent × wrong.
  Why: Extending the hold-out idea, a separate cold child writes extra criteria from the spec text alone, never sees the builder's plan, and its criteria run only at close.
  Done when: a task whose builder passed all visible criteria but failed a hidden one is labelled unproven, with the hidden criterion shown only after the close.

Empty cells and why:
- Site × other agents × slow: nothing there is slow and nothing needs fixing.
- Pane × other agents × unsafe: the pane is display-only and has no actions.
- Hooks × unattended × unclear: the degraded-line ideas above already cover it.
- Web UI × other agents × missing: no non-Claude agent consumes it today.

Next question: which of the 599 meaning-class unproven closes had a spec with only one example, so no hold-out is possible?
Next question: does any criterion generated so far assert more than "exit 0", and what share would fail a deliberately wrong implementation?
