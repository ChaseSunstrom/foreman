# Brainstorm — lens: unspoken needs

**Questions earlier brainstorms left:** Only one fits this mission. Many standing steers assume someone is watching (ask-once, one-word yes, plan edits as the user's signal), and an unattended, self-filed task has no one to catch a thin plan. Idea 5 covers that.

- **Ground every idea against what's built before it is shown** — FEATURE — value 5 — effort M — risk low — category: brainstorm quality
  Why: The Missions 3/4 lesson says "most of #11 and #12 were already built". The unspoken need is that the user never has to check that for themselves.
  Done when: running `fm ideas` on a pack tags each idea built / half-built / new, with a grep hit in MASTER.md or plugin/lib or a ledger row as the proof, and a built one is dropped from the checklist page.

- **Collapse the idea catalog into canonical clusters with repeat counts** — CLEAN — value 4 — effort M — risk low — category: brainstorm quality
  Why: "Ideas so far" repeats the same ideas dozens of times (tripwire file, lean twin, sentence-to-trigger, replay-before-arm). Children burn words dodging a wall of near-duplicates. How often an idea recurs is itself a signal of which are robust.
  Done when: the pack lists each cluster once with an `×N` count and the "Ideas so far" section shrinks by at least half on the current pack.

- **Scope "ideas so far" to the mission's capability** — FIX — value 4 — effort S — risk low — category: brainstorm quality
  Why: This mission is #2 Exhaustive thinking, but the "so far" list is mostly triggers, lean and proof. Those anchor children away from planning, racing and doors. Assumption: the pack builder doesn't tag ideas by capability.
  Done when: a pack for mission N includes only ideas tagged to its capability or to no capability, and a test shows a trigger idea absent from a #2 pack.

- **Raise the plan-depth floor for self-filed and unattended tasks** — FEATURE — value 4 — effort S — risk low — category: planning
  Why: Tasks Foreman files itself (ci, self, discovered) have no user reading the plan, yet the depth rule scales only by size and risk. Assumption: the plan gate doesn't check the task's origin today.
  Done when: a task with a Foreman origin that has one option or no falsifier fails the plan gate, while the same plan on a user-typed S task passes.

- **Check plans as files so hookless harnesses get the gate** — FEATURE — value 4 — effort M — risk med — category: harness parity
  Why: T-0337 (Gemini Stop unwired) and T-0335 show other agents lack the hooks. Foreman is meant to be the discipline layer for coding agents, not only for Claude Code.
  Done when: `fm check` run after a Codex or Gemini session lints the plan file for readings, options and a falsifier, and fails on a fixture plan missing them.

- **Remember rejected approaches and block their silent return** — FEATURE — value 3 — effort M — risk low — category: planning
  Why: The user's rule is not to re-litigate settled decisions, but a new session after compaction can re-propose a rejected design. Assumption: rejected options live in prose, not a queryable index.
  Done when: a plan whose option matches a rejected one in decisions.md is flagged unless it names new evidence, shown by a fixture.

- **Show a plan board in the web UI with strike and star** — FEATURE — value 4 — effort M — risk med — category: web UI
  Why: The web UI is the only surface in the mission, and readings, options, outcomes and edge cases are a table, not prose. The user's plan edits are the one signal Foreman didn't author.
  Done when: the board lists a task's readings and options, striking or starring one writes a decision row, and a screenshot shows empty, loading and error states.

- **Add a `fm go` verb that takes the current leader mid-deliberation** — FEATURE — value 3 — effort S — risk low — category: planning
  Why: Assumption: deep thinking and racing make the user wait. They have said "don't block on me" but have no way to say "good enough".
  Done when: `fm go` during a race stops the lanes, records the leader and its remaining uncertainty, and the build starts.

- **Give weak models a scaffold for exhaustive thinking in `fm code`** — FEATURE — value 4 — effort M — risk med — category: any model
  Why: `fm code` is meant to work on any model (T-1207), but depth tuned on strong models may not carry. A fixed fill-in form for readings, options and failure modes is cheap to check.
  Done when: the same task on a small local model produces a plan that passes the gate, and the exam shows the scaffold arm at least matching the free arm.

- **Watch a chosen approach's flip condition after close** — FEATURE — value 3 — effort M — risk med — category: calibration
  Why: Plans state a falsifier before the build, but nothing watches for it afterwards. Assumption: no post-close check exists. The user keeps asking for outcome survival.
  Done when: a closed task whose flip condition later fires (a named test fails, a file reverts) files a reopen capture citing the original choice.

- **Show-don't-ask: mock demos of each reading (wild)** — FEATURE — value 4 — effort L — risk med — category: ambiguity
  Why: wild. Assumption: the user hates questions (steers say never block them), yet two readings sometimes disagree. Three ten-second stub outputs let them choose by looking.
  Done when: on a fixture ambiguous request, Foreman shows N stubbed before/after outputs and records which one the user picked.

- **Write a fear headline per big plan and check it at close (wild)** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: wild. A one-line "Foreman breaks X" headline is more memorable than a pre-mortem table. Closing with "did the headline happen?" gives a cheap miss signal.
  Done when: an L plan requires a headline line, and the finish receipt prints it with held or happened.

- **Sleep on L plans and re-read them cold in the morning (wild)** — FEATURE — value 3 — effort M — risk med — category: overnight
  Why: wild. A second look by a different model after a gap catches first-reading lock-in. The user already accepts night shifts.
  Done when: an L plan parked overnight gets a cold-read diff of readings against the user's words, and any new objection is attached before the build starts.

Next question: Which of the 58 empty #2 cells are about the planning phase, the racing phase or the stop-and-ask phase, and does each phase have an existing verb that a session actually calls?
Next question: What does the user see in the web UI at the moment Foreman decides not to deliberate deeply, and could they tell it was on purpose?
