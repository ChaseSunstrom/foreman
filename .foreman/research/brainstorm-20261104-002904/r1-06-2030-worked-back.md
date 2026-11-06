# Brainstorm — lens: 2030 worked back

- **Compile spec examples into criteria at plan time** — FEATURE — value 5 — effort M — risk med — category: meaning proof
  Why: "meaning is the largest unproven class (599)" and the request says spec example assertions should become runnable criteria. Plan time extracts every `input → expected` pair from the spec or brief into a frozen `Criteria:` block of commands. A 2030 task has no prose acceptance that a machine never ran.
  Done when: a brief containing three example assertions files with three runnable criteria. Running them on the parent commit fails, and the builder cannot edit them.

- **Run every extracted criterion against a stub first** — FEATURE — value 4 — effort S — risk low — category: vacuity
  Why: assumption: auto-extracted criteria will sometimes pass on nothing (an empty output matching a loose regex). Each criterion must fail on an empty or no-op implementation, or it is labelled "cannot fail".
  Done when: a planted criterion that matches empty output is rejected at filing with the label "cannot fail".

- **Keep a claims table for docs, with cited-file hashes** — FEATURE — value 5 — effort M — risk med — category: docs
  Why: "421 docs flag claims no run has checked". Each doc sentence with a command, number or "always/never" becomes a row (claim, check command, hash of the files it cites, last-run result). Editing a cited file flips the row to stale without a model call.
  Done when: touching a file a README claim cites turns that claim "stale" in `doctor`, and re-running its check restores "held".

- **Lint public surfaces for vendor and host names by role** — SECURITY — value 4 — effort S — risk low — category: public surfaces
  Why: the user's steers: never show "jarvis", never name Claude as the orchestrator, and say "the orchestrator" and "decision model" instead. A ship-gate lint over `site/`, README, scene data and skills fails on vendor model IDs, endpoint profile names and home paths outside an allowlist of historical files.
  Done when: adding "jarvis" or a Claude model ID to `site/index.html` fails the gate with the line and the role word to use.

- **Hold a tool-less reader exam for docs** — FEATURE — value 4 — effort M — risk med — category: docs
  Why: assumption: a claim a cold reader can't predict is ambiguous. A tool-less child gets only a doc and each claim's setup, and predicts the output. The prediction is diffed against the real run, and a mismatch marks the doc ambiguous or wrong.
  Done when: a doc with a deliberately wrong example is flagged and a correct one is not, on a fixed fixture.

- **Label every unproven claim with a reason** — FEATURE — value 4 — effort S — risk low — category: unproven taxonomy
  Why: "whatever can't be proven is labelled unproven" is a single bucket. Split it into needs-human-taste, needs-network, needs-production, nondeterministic and no-check-written, and name who can discharge each one.
  Done when: the Mission report shows unproven counts by reason, and a claim with no reason fails `check`.

- **Ratchet the unproven count by class** — CLEAN — value 3 — effort S — risk low — category: ratchet
  Why: the 599 and 421 counts are a baseline. A committed file records per-class unproven counts, which may fall but not rise without a recorded waiver.
  Done when: adding a doc claim with no check raises the count and fails the gate until a check or a waiver is added.

- **Trace every site number to its source** — FIX — value 4 — effort M — risk low — category: site truth
  Why: the landing wires "real stats". Each rendered figure carries a `data-src` pointing at the generator and field, and a test recomputes it and compares.
  Done when: hand-editing a stat in `site/index.html` fails the test naming the source it should have come from.

- **Check that the same claims hold under three orchestrators** — FEATURE — value 4 — effort L — risk med — category: agent-agnostic
  Why: the standing rule says Sampo works with any agent, but only Claude Code is live-verified (T-0336). Run a small claim set under Claude Code, Codex and Smith, and report claims that hold under only one.
  Done when: a claim that passes on one orchestrator and fails on another is listed by role ("orchestrator A/B"), never by vendor.

- **Replay old claims on today's code (wild)** — FEATURE — value 3 — effort M — risk low — category: claim half-life
  Why: wild. Re-run the claims from a past generation on the current tree. The decay rate says how fast truths rot, and sets how often docs get rechecked.
  Done when: a report lists claims from generation N-2 that no longer hold, with the commit that broke each.

- **Mark claims that were only ever agreed by the author's model (wild)** — SECURITY — value 3 — effort M — risk low — category: independent evidence
  Why: wild, from the steer on signals Foreman didn't author. Each "held" claim records whether its evidence was a run, an outside tool or only the same family's read. Single-family claims display as "held, not independently".
  Done when: the claims table has an evidence-source column, and the web card filters to self-attested claims.

- **Grade a criterion by the bug it would have caught (wild)** — FEATURE — value 3 — effort L — risk med — category: meaning proof
  Why: wild. Mutate the finished change (flip a branch, swap a constant) and run the criteria. Survivors show where meaning is still unproven, and become new example prompts for the user.
  Done when: a task whose criteria miss a planted mutation reports "survivor at file:line" on its finish card.

Next question: Which of the 599 meaning claims could a criterion check mechanically today, and which need a human word, since that split sets the ceiling for the whole Mission?
Next question: When a doc claim goes stale, who fixes it, the doc or the code, and can Foreman tell which side the user would pick?
