# Brainstorm — lens: tower archaeology

- **Add a schema version and `fm genesis migrate`** — FIX — value 4 — effort M — risk med — category: durability
  Why: Genesis was built in pieces (T-2077, T-2078, T-2080, T-2090), so a tower three generations old was written by older code. Nothing in the pack versions the tower format. Assumption: tower files carry no schema marker today.
  Done when: a fixture tower in the old layout opens read-only with a "needs migrate" notice, and `fm genesis migrate` upgrades it with every gen-0 byte unchanged, verified by hash.

- **Stamp every tower artifact with its author** — FEATURE — value 4 — effort S — risk low — category: provenance
  Why: a later session can't tell a hand edit, a tool-less child's output and an old template's output apart. Without that it can't judge how far to trust a file. Assumption: only the file contents are stored now.
  Done when: each file under a generation lists writer (model or human), fm version and prompt hash, and `fm genesis status` flags any file lacking a stamp.

- **Treat hand edits to tower files as steers** — FEATURE — value 4 — effort M — risk med — category: integrity
  Why: the user steered the tower by hand more than once (storage-only rule, ≥9 scenarios, standing rules). An edit Genesis doesn't know about gets silently overwritten or contradicts its own lineage.
  Done when: editing a tower doc outside `fm genesis put` makes the next `status` report "hand-edited since last put", logs the diff as a steer, and the next generation's Seed cites it.

- **Give a resuming session a tiered reading path** — FEATURE — value 4 — effort S — risk low — category: resume
  Why: the user wants every doc readable in full, but a cold session has a finite context. Assumption: no ordering or token cost is recorded.
  Done when: the tower index lists a minimal path ("read these 3 files, about 4k tokens, to take the next step") and a full-audit path, with token estimates, regenerated on each put.

- **Make resuming a handshake: restate, then compare** — FEATURE — value 4 — effort M — risk low — category: resume
  Why: a cold session can read the wrong thing and carry on confidently. Cheap check: before acting it must state the next step, the open not-yet items and the NEVERs in its own words, then the tower compares them against its recorded values.
  Done when: `fm genesis resume` refuses to run a stage until the restatement matches the recorded next step and NEVER list, and a planted wrong restatement is rejected in a test.

- **Reconcile the tower with the task queue on open** — FIX — value 3 — effort S — risk low — category: consistency
  Why: tower docs cite tasks (T-2077 and others) whose status moves independently of them. Stale "in progress" claims send a resumer after finished or dropped work.
  Done when: opening a tower lists every cited task id whose current status differs from what the doc says, and a fixture with a closed task shows the mismatch.

- **Match new missions against dead rewrites before spending** — FEATURE — value 4 — effort M — risk low — category: memory
  Why: the not-yet ledger and the verdicts record that something lost, but nothing says a fresh Mission is about to repeat it. The standing rule says a failed idea gets at least 2 different approaches. This check would enforce that.
  Done when: a Mission whose text overlaps a past losing rewrite is prefaced with that lineage entry, and a fixture that retries a lost approach is flagged as "same approach, attempt N".

- **Flag contradictions across generations** — CLEAN — value 3 — effort M — risk low — category: consistency
  Why: gen-2's Seed can disagree with gen-1's critique and nobody notices. A tool-less reader that sees only the docs can find the conflicts.
  Done when: `fm genesis lint --contradictions` reports a planted pair of conflicting statements across two generations in a fixture tower, with both file lines.

- **Decay claim confidence by churn in the files it cites** — FEATURE — value 3 — effort M — risk med — category: staleness
  Why: fmmap already learns co-change from git history, so the signal exists. A claim about `plugin/lib/fmexam.py` is weaker once that file has changed a lot, even without a commit tag.
  Done when: each tower claim that names a path shows "N commits since written", and claims over a threshold appear in a "recheck first" list on the resume page.

- **Séance: ask a past generation a question, answer from its files only** — FEATURE — value 3 — effort M — risk low — category: documentation holes — wild
  Why: assumption: the best test of whether the records are enough is asking a question like "why did gen-1 reject rewrite B?" to a tool-less child that sees only gen-1's files. Questions it can't answer become a "gaps in the record" list.
  Done when: `fm genesis ask gen-1 "<q>"` answers using only that generation's files, cites lines, and says "not recorded" for a planted unrecorded fact.

- **Show the tower as dig strata on the site** — FEATURE — value 2 — effort M — risk low — category: site, delight — wild
  Why: the user wants per-generation detail on the page (seed, missions, critiques, exam, decisions). Layers per generation, with finds (winning rewrites), fossils (dead ends) and the plow line (current work) make that scannable.
  Done when: the exported page has a strata view where clicking a layer opens that generation's full docs, with reduced motion respected.

- **Ask each generation for three warnings at close** — FEATURE — value 3 — effort S — risk low — category: handoff — wild
  Why: the Seed and missions record what was planned. The things the generation wished it had known are rarely written. Assumption: no such field exists.
  Done when: closing a generation requires a "warnings" file of exactly three items, and the next Seed template quotes them verbatim.

- **Keep losing rewrites in a graveyard and let a session exhume one** — FEATURE — value 3 — effort S — risk low — category: lineage
  Why: a verdict says why a rewrite lost, but a later session can't see what it said, so it cannot tell whether the loss was close or the exam was weak.
  Done when: `fm genesis exhume <rewrite>` prints the full loser text, its exam scores per scenario and the parent's side by side.

- **Cross-check a recorded next step with a fresh model** — FEATURE — value 3 — effort M — risk low — category: resume
  Why: a tool-less reader from a different model asks "what would you do next?" from the files alone. If its answer differs from the recorded next step, either the files are unclear or the plan is wrong. Both are worth knowing.
  Done when: `fm genesis resume --check` records agreement or the disagreement text, and a fixture with an ambiguous next step gets disagreement.

Next question: What does a tower look like after a fm version upgrade changes the exam generator or the scenario kinds, and can old exam scores still be compared with new ones?
Next question: Who else reads a tower besides a resuming session (a reviewer, a teammate, the site visitor), and does each need a different entry point?
