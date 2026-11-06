# Brainstorm — lens: security and safety

- **Redact secrets before evidence, ledger and sync** — SECURITY — value 5 — effort S — risk low
  Why: `fm task evidence --run` stores real command output, and `fm sync` mirrors briefs and research into the repo's `.foreman/`, so a token in test output could end up in a commit. Recall (idea 3) also raises the exposure. Assumption: no scrubber exists today.
  Done when: a test that feeds an `AKIA…`/`ghp_…`/`Bearer` string through evidence recording and `fm sync` finds `[REDACTED]` in the ledger, the brief and the synced file.

- **Weak-test detector for regression tests** — FEATURE — value 5 — effort M — risk med
  Why: Foreman can't tell a test that passes without the change from a real regression test. Done-gating trusts exit 0, so a vacuous test yields false safety.
  Done when: `fm check --prove` runs the new test against the frozen pre-change diff (from `fm audit prep`). It fails when the test passes there, and a fixture with a vacuous test is rejected.

- **Sanitize and label recalled memory** — SECURITY — value 4 — effort M — risk med
  Why: the plan is to auto-surface decisions, research and past briefs into hooks. Research notes may hold fetched web text, so injected instructions could persist and re-enter every session. Assumption: research/ can contain untrusted text.
  Done when: recalled snippets are capped at 400 chars, wrapped as quoted data with their origin, and stripped of imperative or tool-directing lines. A test with a planted "ignore previous, run curl…" note shows it neutralized in the injected note.

- **Auto-escalate tier and audit lens on sensitive paths** — FEATURE — value 4 — effort M — risk low
  Why: `guess_tier` is a regex plus a length check, so a small edit to auth or shell-exec code can get an S-tier self-checklist. Assumption: a project map with a sensitive-files list doesn't exist yet.
  Done when: `fm focus` on a brief whose scope matches auth, crypto, secrets, subprocess or deserialization patterns raises the tier to at least M and requires the security lens. A test shows that a two-line change to `auth/session.py` demands the lens.

- **Flag instruction-like text in grounded evidence** — SECURITY — value 3 — effort S — risk low
  Why: grounding reads READMEs, issues and code comments, then compiles an Execution prompt. Text from those sources could steer the plan without being flagged.
  Done when: `fm task new/evidence` marks quoted repo text as `data:` and warns on lines like "you must run…" or "disregard…". A test with a poisoned README quote produces the warning in the brief.

- **Record reversibility and blast radius on autonomous decisions** — FEATURE — value 3 — effort S — risk low
  Why: in full autonomy Claude records its default in decisions.md, and nothing checks whether the decision was reversible or held up later. Foreman's confirm-before-irreversible expectation isn't tied to that record.
  Done when: decisions.md gains `reversible|costly|outward` columns. `fm decide` on an outward or costly choice without a stated authorization is refused, and `fm doctor` lists decisions that were later reversed.

- **Opt-in cross-project lessons with a privacy filter** — FEATURE — value 3 — effort L — risk high
  Why: each project's learning is siloed. Sharing lessons between repos could leak paths, client names or secrets. Assumption: users want this.
  Done when: `fm lessons promote` writes only entries that pass a redaction and path-stripping check, tagged with their origin repo, and never promotes from repos marked untrusted. A test with a lesson containing an absolute path and a token shows both removed.
