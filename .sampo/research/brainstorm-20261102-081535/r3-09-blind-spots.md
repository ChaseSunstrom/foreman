# Brainstorm — lens: blind spots

## Blind-spot questions for verification

Each earlier miss maps to a question, and I asked it of the verification layer rather than of the product. Provers are gauges too, so the same eight classes (control arm, cause naming, silent death, already built, input contamination, partial input, omitted denominator, unreachable output) apply to them. The pack shows several provers (`fm shot`, `fm flow`, the exam arms) but no proof of the provers' own liveness or recall.

- **Ideas 1–4** cover provers that read green while blind: split skew, self-referential evidence, correlated misses, under-claiming.
- **Ideas 5–9** cover the same classes where a user's wording becomes a check.
- **Ideas 10–12** are wild.

- **Issue each prover a birth certificate** — FEATURE — value 4 — effort M — risk low — category: verification
  Why: T-2534..T-2566 were all gauges or checks that could not answer the control-arm, cause, liveness, denominator and partial-input questions. Provers (`fm shot`, `fm flow`, doc checks) are born with no such gate. The earlier "gauge birth certificate" idea covered gauges only.
  Done when: registering a prover with any of the eight questions unanswered is refused, and the refusal names the missing answer.

- **Flag evidence that came from a single split** — FIX — value 4 — effort S — risk low — category: proof integrity
  Why: T-2566 (select ignored exam lines answered only on the held-out split) shows verdicts silently built on half the inputs. Proofs can have the same skew: scenarios from one split, one author, or one harness.
  Done when: a proof whose evidence rows all share one split, author or harness is stamped `skewed: <which>`, and a fixture with held-out-only rows produces that stamp.

- **Reject self-referential proofs** — SECURITY — value 4 — effort M — risk med — category: proof integrity
  Why: T-2554 (the user model read Foreman-authored briefs) is the same contamination class. A proof whose inputs are all files Foreman wrote cannot confirm anything about the user's meaning.
  Done when: each proof lists the origin of every file it read, and a proof with zero non-Foreman-authored inputs is labelled `circular` and not counted as proven.

- **Measure proof recall by trying to prove the unproven** — FEATURE — value 4 — effort M — risk low — category: verification
  Why: the pack reports only over-claiming ("whatever can't be proven gets labelled"). Under-claiming is untracked: an "unproven" label that an installed tool could have settled still costs the user a manual check.
  Done when: `fm doctor` samples N unproven labels, runs every available prover on each, and prints "X of N were provable with tools already present".

- **Check enumeration parity between the ask and the proof** — FIX — value 3 — effort S — risk low — category: intake
  Why: T-2547 refused Missions whose briefs outnumbered their grounding lines. T-2583 (an example that broke its own rule) shows the same count mismatch in criteria. No check compares what the user listed with what the proof lines cover.
  Done when: a request with 4 comma- or numbered items and a DONE-WHEN with 3 probes is refused with the uncovered item named.

- **Lint vague verbs into measurable thresholds** — FEATURE — value 3 — effort S — risk low — category: intake
  Why: "does it do what the user meant" fails at words like "works", "fast", "safe", "clean". The adjective dictionary idea covered only "best-in-class".
  Done when: a criterion containing a listed vague verb with no number, command or example is refused, and a test pins one refusal per listed verb.

- **Prove forgetting** — SECURITY — value 3 — effort M — risk low — category: privacy
  Why: the "let the user model forget" idea has no proof step. The pack asks which Foreman files hold prompt text that a backup could copy.
  Done when: after `forget X`, a scan of the state directory, journals and exam captures finds zero occurrences of X, or lists the files that still hold it.

- **Measure whether provers fail together** — PERFORMANCE — value 3 — effort M — risk low — category: verification
  Why: assumption: correlated provers add little confidence. Reviewers have a pairing idea, but no per-prover miss matrix exists.
  Done when: planting 10 faults produces a prover-by-fault miss matrix, and a task whose proofs all come from provers with identical misses is labelled `correlated`.

- **Read-receipt the Unproven footer** — FIX — value 3 — effort S — risk low — category: proof presentation
  Why: assumption: an Unproven line that never changes what the user does is noise, and the user's own words show them repeatedly asking for verification manually.
  Done when: a ledger records, per footer, whether the user's next 3 messages reused its words. A 30-day report names the share ignored.

- **Check proofs from the machine the user actually uses** — FEATURE — value 3 — effort M — risk med — category: ops
  Why: this environment's working directory is under `/run/user`. Proofs, shots and flow captures may live on tmpfs and vanish on logout, which is a silent death. The pack's tick and timer ideas never ask where evidence is stored.
  Done when: a proof stored on a volatile path is stamped `volatile`, and `fm doctor` lists proofs that would not survive a reboot.

- **Wild: Run a contrarian verifier** — FEATURE — value 3 — effort M — risk med — category: verification
  Why: wild. A tool-less child is told the claim is false and must name the one observable that would show it. That observable becomes a probe, and a probe that actually fires is a real catch.
  Done when: on a fixture with a planted false claim the contrarian names a probe that fails, and on a true claim its probe passes.

- **Wild: Let dormant proofs wake on a premise change** — FEATURE — value 3 — effort L — risk med — category: proof lifecycle
  Why: wild. Each proof records its premises (version, config, dataset hash). A watcher re-runs it only when a premise changes, and flags it `stale` otherwise.
  Done when: changing a recorded premise re-runs exactly the dependent proofs and no others.

- **Wild: Show a proof weather report at session start** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild. One line says "clear: 14 proven, 2 unproven, 1 skewed", with the one claim the user most likely cares about first.
  Done when: the session-start note shows that line and omits it when nothing changed since the last session.

Next question: Which proofs does the user themselves re-run by hand, and what does that say about which proof kinds they don't yet trust?
Next question: What happens to proof evidence when the state directory lives on tmpfs or another volatile path?
