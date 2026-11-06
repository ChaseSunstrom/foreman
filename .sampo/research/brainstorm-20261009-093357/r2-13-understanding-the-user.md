# Brainstorm — lens: understanding the user

- **Keep an aspiration ledger and alarm on drift** — FEATURE — value 5 — effort M — risk low — category: intent
  Why: The user had to restate "I want genuine capabilities/intelligence", and the open queue (T-0435..T-0455) is almost all infrastructure, so the stated wish and the actual work diverged. Assumption: aspirations can be captured as one-line quotes with a status.
  Done when: `fm aspirations` lists each user-stated aspiration with its quote and the tasks that serve it, and a queue with zero tasks toward one raises a flag at the next planning pass (tested with a fixture queue).

- **Grade the endorsement on every task** — FEATURE — value 4 — effort S — risk low — category: provenance
  Why: Tasks are logged "asked: FEATURE: …" even when the user only bulk-approved a brainstorm ("I like almost all of those"), so a hearty ask and a shrug look identical. Assumption: the intake source can be tagged.
  Done when: each task shows one of explicit-ask, bulk-approved, or Foreman-invented, and `fm queue` can sort or filter by it.

- **Resolve "almost all" into its exceptions** — FEATURE — value 4 — effort S — risk low — category: intake
  Why: "Almost all" implies a residue the user never named. Foreman currently treats the whole list as approved, and the cleanup and YAGNI steers suggest unspoken exceptions get built anyway. Assumption: the residue can be guessed from past drops and vetoes.
  Done when: after a blanket approval, Foreman asks one batched question naming the 3 items most likely excluded, and the answers are recorded on those tasks.

- **Predict over-build from the user's past drops** — FEATURE — value 4 — effort M — risk med — category: scope
  Why: Drops include "YAGNI: loosening the brief gate adds guard surface" and an over-built budget cap ("savings only to prevent over usage"). Built-then-dropped work is a labelled dataset. Assumption: drops can be tied back to brief features such as first-version size or new surface.
  Done when: before an M/L build, intake prints an over-build risk with the 2 matching past drops, and a replay over the history ranks known dropped items above kept ones.

- **Restate every delegation as a bounded mandate** — FEATURE — value 4 — effort S — risk low — category: autonomy
  Why: "Feel free to continue with those" is open-ended, so Foreman either stops too early or runs too far. Assumption: delegation phrases can be detected at intake.
  Done when: a delegation phrase produces a stored one-line mandate (scope, stop conditions, lapse time) that drive shows at each checkpoint and the user can edit in one command.

- **Learn from the user overriding Foreman's own ranking** — FEATURE — value 4 — effort S — risk low — category: taste
  Why: C079 was marked skip and the user added it anyway, which is a direct signal that Foreman's value scoring disagrees with theirs. Assumption: overrides can be logged where the ranking is produced.
  Done when: each override is recorded with the idea's features, and the next `fm ideas` scoring shifts weights so a similar idea no longer ranks as skip (checked by a unit test).

- **Pre-answer the likely follow-ups** — FEATURE — value 3 — effort M — risk low — category: reporting
  Why: Steers such as "trace why and fix" are follow-up questions the user had to ask after a close-out. Assumption: past follow-ups can be clustered by task type.
  Done when: a done report carries a collapsed "you'll probably ask" section with answers drawn from the evidence, and the hit rate against the user's next message is logged.

- **Make intelligence legible with one insight line per task** — FEATURE — value 4 — effort S — risk low — category: reporting
  Why: The user wants "genuine" intelligence, but a good judgment call leaves no trace in the report. Assumption: the judgment call can be taken from the brief's rejected options or a changed plan step.
  Done when: every L task close-out names one place Foreman departed from the obvious path, with the reason and the evidence; a task with none says so explicitly.

- **Elicit abstract wishes with vignettes** — FEATURE — value 3 — effort M — risk low — category: elicitation
  Why: "Planning/brainstorming/thought process, all of it" is too abstract to verify, and the first brainstorm answered it with infrastructure. Assumption: users find it easier to pick between concrete scenes than to define a capability.
  Done when: for an aspiration-level request, Foreman writes 3 short scenes of a session with the capability and records which one the user picks, then derives acceptance criteria from it.

- **Wild: Provoke a correction with a confident wrong guess** — FEATURE — value 3 — effort S — risk low — category: elicitation
  Why: assumption: people correct a bold wrong statement faster than they produce a description. Examples: "I think you want Foreman to stay quiet mid-run" or "I think you care most about speed".
  Done when: once a week Foreman states one deliberately falsifiable belief about the user's priorities, and the reply (agree, correct, or ignore) is stored as portrait evidence.

- **Wild: Keep a wish jar that ripens** — FEATURE — value 3 — effort M — risk low — category: capture
  Why: assumption: half-formed "sometime I'd like…" remarks are lost because capture requires a full task. Foreman would hold them and attach evidence whenever related work or friction appears.
  Done when: a vague wish stays as a jar entry, gains linked evidence on a relevant task, and surfaces as a proposed brief once it has 3 hits.

- **Wild: Write the letter from the user's future self** — FEATURE — value 3 — effort S — risk low — category: unspoken needs
  Why: assumption: the user's regrets, such as cleanup that never happened, are predictable from their steers. A weekly letter lists what they'll wish they'd asked for.
  Done when: `fm letter` produces up to 5 imagined regrets, each citing its steer evidence, and each can be accepted into the queue or rejected, with the rejections feeding the taste model.
