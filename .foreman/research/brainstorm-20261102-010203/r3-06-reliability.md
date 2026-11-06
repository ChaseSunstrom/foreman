# Brainstorm — lens: reliability

Lens: reliability, applied to the immune-system moonshot. I avoided mechanisms the pack already lists (negative selection, anergy, fever, T-regs, memory cells, vaccination, quarantine, affinity maturation, missing-self, privilege) and took the ones it lacks.

- **Select new guard rules positively as well as negatively** — FEATURE — value 4 — effort S — risk low — category: guard
  Why: assumption: the pack has thymus-style "negative selection" ideas but only for false positives. A rule that never binds anything real is a silent hole.
  Done when: `fm` refuses a new rule unless it fires on at least 1 labelled replay case and 0 clean ones.
  Prior: mutation testing, "rule needs a failing test". Better by: a two-sided window on the 124-case corpus. Novelty: 3.

- **Write one rule per independent epitope of an incident** — FEATURE — value 4 — effort M — risk med — category: guard
  Why: the user's own push for "letter defeats intent" and evasion corpora. One regex per incident is easy to dodge.
  Done when: after a block, 3 rules are drafted (syntax, effect, target path), and a mutated evasion has to beat all 3 to pass.
  Prior: Falco and Tetragon split behaviour and syntax, but not per incident. Better by: polyclonal redundancy generated from one incident. Novelty: 3.

- **Make learned rules able only to tighten** — SECURITY — value 5 — effort S — risk low — category: guard
  Why: assumption: with auto-learned approvals and rule drafts, no invariant stops a learned artifact from relaxing the fixed guard.
  Done when: a test shows any learned or approved rule that lowers a shipped deny to allow is rejected at load time.
  Prior: none found (managed-policy layers are static). Better by: germline-versus-somatic tiers with a one-way ratchet. Novelty: 3.

- **Close every incident with a verified resolution phase** — FEATURE — value 4 — effort M — risk med — category: recovery
  Why: pack ideas fever and quarantine decay passively. Nothing checks that state returned to baseline.
  Done when: after a harm event, the incident stays open until the interrupted work is re-run, the baseline is restored, and emergency state is cleared. A stuck incident WARNs in `fm doctor`.
  Prior: SRE postmortem checklists. Better by: automatic, with chronic non-resolution as its own alarm. Novelty: 3.

- **Apply Koch's postulates before blaming a lesson, hook or rule** — FEATURE — value 4 — effort M — risk low — category: attribution
  Why: "name the cause when a gate trips" appears repeatedly, and the user asks for evidence over theory.
  Done when: a blame verdict needs the suspect removed from a clean clone (failure vanishes) and re-added (failure returns).
  Prior: git bisect and delta debugging for code, none for harness artifacts. Better by: ties into ablation duels. Novelty: 4.

- **Put a telomere on auto-evolved rules** — SECURITY — value 3 — effort S — risk low — category: drift
  Why: assumption: overnight mutation of guard rules (proposed elsewhere) drifts from vetted ancestors.
  Done when: a rule more than 3 mutations from a human-approved ancestor stops evolving and shows up in a re-approval card.
  Prior: none found. Better by: bounds self-modification. Novelty: 4.

- **Add hysteresis to every mode switch** — FIX — value 3 — effort S — risk low — category: stability
  Why: assumption: fever, quarantine and breaker modes with one threshold will flap near it.
  Done when: a replayed noisy signal near the threshold causes at most 1 enter and 1 exit, with exit set at a lower bar than entry.
  Prior: Schmitt triggers in control engineering. Better by: applying it to harness modes. Novelty: 2.

- **Run an amnesia check after every upgrade, compaction or GC** — FIX — value 4 — effort S — risk low — category: memory
  Why: the pack proposes GC for moved repos and state compaction, and a destructive cleanup could erase lessons without any alarm.
  Done when: a fixed panel of 10 known lessons must still recall after any state-mutating job, or the job rolls back.
  Prior: backup restore tests. Better by: tests recall, not file presence. Novelty: 3.

- **Absorb repeated blocked calls with a decoy** — PERFORMANCE — value 3 — effort S — risk low — category: noise
  Why: the frontier shows 15+ prompts per session, and a looping agent re-triggers notes and logs.
  Done when: the 2nd to Nth identical blocked call returns a cached verdict and the safe command, with one counter row instead of new alarms.
  Prior: retry backoff. Better by: silences amplification while still teaching. Novelty: 2.

- **Wild: Grow a per-hotspot micro-guard** — FEATURE — value 3 — effort L — risk med — category: local immunity
  Why: wild; assumption: files with repeated incidents get the same global rules as quiet ones.
  Done when: a file with 3 or more incidents gets its own small rule set from its history, and the set dissolves after 4 quiet weeks.
  Prior: none found. Better by: like tertiary lymphoid structures, formed only at chronic sites. Novelty: 5.

- **Wild: Distil a phage, a one-signature auto-fix** — FEATURE — value 3 — effort M — risk high — category: self-repair
  Why: wild; a known failure signature with a proven fix currently needs a full lane.
  Done when: a script runs unattended only on an exact signature match, and retires itself the first time it touches anything outside its declared files.
  Prior: runbook automation. Better by: narrow host range with built-in retirement. Novelty: 4.

- **Wild: Run a nightly challenge trial of a real incident** — FEATURE — value 4 — effort M — risk med — category: drills
  Why: wild; vaccination ideas replay attenuated inputs, but nothing runs a real past incident through detect, contain and resolve together.
  Done when: a night tick replays last week's worst incident into a scratch clone and the digest says which of the three stages failed.
  Prior: chaos engineering. Better by: uses the user's own incidents and scores the whole chain. Novelty: 3.

Next question: which Foreman mode or alarm has no exit condition, and what would flapping or never leaving it cost the user?
Next question: which learned or auto-evolved artifact could today loosen a fixed protection without a human seeing it?
