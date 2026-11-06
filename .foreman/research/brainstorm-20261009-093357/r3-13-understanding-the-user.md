# Brainstorm — lens: understanding the user

- **Pin the numbers the user dictates** — FEATURE — value 4 — effort S — risk low — category: fidelity
  Why: "budget/pace limits shouldn't block anything until 75% usage" and "fm friction --every 3" are exact values the user chose, and T-0320 shows one was first built wrong. No existing idea registers user-dictated constants.
  Done when: `fm pin 75% --quote "…" --at <file:const>` records the value with its source words, and a gate fails when the code constant differs from the pinned value.

- **Keep a stance ledger with supersession** — FEATURE — value 4 — effort M — risk low — category: memory
  Why: the user's stances change ("savings only to prevent over usage", "drop the cap"). Vetoes and decisions are static, so a plan can still rest on a superseded stance. Assumption: stances can be extracted from steers with a cheap pass.
  Done when: a new steer that contradicts an earlier stance writes a dated successor with the stated reason, and recall returns only the live stance, with lineage on request.

- **Map where the user has strong opinions** — FEATURE — value 4 — effort M — risk low — category: autonomy
  Why: steers cluster by area (Tauri, animations, budget semantics, cleanup), while many areas get a bare "continue". Foreman should consult in the hot areas and decide silently in the cold ones. Taste models exist; a per-area consult-or-decide router built from steer density does not.
  Done when: `fm opinions` lists areas by steers per task, and intake logs "consult" or "decide" for each open fork using that map.

- **Treat silence as ratification, with a revoke** — FEATURE — value 3 — effort M — risk med — category: learning
  Why: assumption: defaults the user never overrides across N tasks are quietly approved, but Foreman only learns from corrections. Promote such defaults to stated defaults and demote them on the first complaint.
  Done when: a default accepted untouched in 5 tasks appears in `fm defaults` with its evidence count, and one later steer against it removes it.

- **Resolve which Foreman a request is about** — FIX — value 3 — effort S — risk low — category: intake
  Why: Foreman is self-hosted. "The guard blocked me", "update foreman-ui" and "installed vs HEAD" could mean the plugin source, the installed copy, the consumer project or the live session. The dropped `fm task new … && edit` report shows this ambiguity.
  Done when: intake echoes "target: plugin source | installed copy | project | session" for requests that mention Foreman parts, and a wrong target takes one correction to fix.

- **Track answer debt** — FEATURE — value 3 — effort S — risk low — category: continuity
  Why: assumption: questions the user asks mid-flow get buried under captured tasks. Captured requests are tracked; questions aren't.
  Done when: each user question is logged with answered/unanswered status, and the session greeting and `fm status` list questions that are still unanswered.

- **Add a wrong-turn button on every ledger line** — FEATURE — value 4 — effort M — risk low — category: feedback
  Why: corrections today arrive as free-text steers that Foreman must interpret. A one-key "this is where it went wrong" with reason chips (misread, over-built, ignored a rule, too slow) gives labeled data and a replay point at no typing cost.
  Done when: in the web UI and band the user can flag any event, and the flag writes a labeled friction record that `fm friction` aggregates by reason.

- **Brief children with a values card** — FEATURE — value 3 — effort S — risk low — category: delegation
  Why: builders and reviewers get the task brief but not what this user cares about. Assumption: a short card of 8–10 live stances and vetoes would reduce rework.
  Done when: each fm-builder and fm-reviewer prompt includes the card, and a bench replay shows fewer reviewer findings that cite violated stances.

- **Surface mental-model gaps before obeying** — FEATURE — value 3 — effort M — risk low — category: understanding
  Why: the "cap vs pace" mix-up cost a build. When a request's wording implies a mechanism that differs from the implemented one, Foreman states the difference in one sentence before acting. This is narrower than the existing belief-modelling idea: it triggers only on a wording-versus-code mismatch.
  Done when: asking for "a cap" while a pace governor exists produces a one-line "this works as X, did you mean Y?" at intake.

- **Wild: Let the user underline the word that matters** — FEATURE — value 3 — effort S — risk low — category: interpretation
  Why: wild. Foreman guesses the load-bearing words and shows them bold in its echo ("I heard: not blocked **until 75%**"). The user can click to re-weight, and the corrected emphasis is stored as intake training data.
  Done when: the interpretation echo marks emphasized phrases, a click changes the weighting, and the brief's acceptance criteria are regenerated.

- **Wild: Run a tired-you glance on every close-out** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: wild. A cheap check asks whether a distracted user at 2am could grasp what was done and what needs them in 10 seconds. If not, it rewrites the close-out around that. This goes beyond the existing acceptance-glance rehearsal by adding mood variants.
  Done when: the close-out passes a length and clarity check, and the one needed action is the first line.

- **Wild: Defy the taste model on purpose** — FEATURE — value 3 — effort M — risk med — category: learning
  Why: wild. A taste proxy that only exploits its own predictions drifts from the user. With a small budget, Foreman makes one low-stakes choice the model wouldn't pick, labels it as a probe, and records the reaction.
  Done when: roughly 1 in 20 eligible low-risk choices is flagged as a probe, and the user's reaction updates the model's confidence.
