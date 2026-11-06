# Brainstorm — lens: simplicity

- **Use one proof line for every kind of check** — CLEAN — value 5 — effort M — risk low — category: proof format
  Why: the pack shows many separate verifiers (shot, flow, task prove, docs, bench, exam), each with its own gauges and wording. assumption: their outputs differ in shape.
  Done when: `fm shot`, `fm flow`, the docs check and the bench each emit `claim | method | proven/failed/unproven | reason`, and one parser reads all four.

- **Allow only three verdicts and a closed list of reasons for "unproven"** — FEATURE — value 5 — effort S — risk low — category: honesty
  Why: the request says whatever can't be proven is labelled unproven. The pack also records exam grades split into false dones and real ones. assumption: free-text hedges like "likely OK" still leak into closes.
  Done when: a close that contains a hedge word and no verdict fails `fm task finish`. "Unproven" must carry one of `no-tool`, `no-env`, `subjective`, `no-baseline` or `needs-user`.

- **Cap each task at three claims, each with a probe** — FEATURE — value 5 — effort M — risk med — category: meant-check
  Why: "does it do what the user meant" is the hardest case and has no probe. Restating DONE-WHEN as at most three claims tied to the user's own words keeps it small. A claim with no probe is printed as unproven.
  Done when: `fm task prove` lists at most three claims, each next to the quoted user phrase it came from. A fixture task with an unprobed claim shows "unproven: subjective".

- **Check docs against code only on literal tokens** — FEATURE — value 4 — effort S — risk low — category: docs
  Why: the pack has docs-unknown proof tests and MASTER.md clauses. Prose can't be checked. Commands, flags, paths and numbers can, by running `--help` or grep.
  Done when: a README that names a nonexistent flag or file fails the check with the line number, and prose-only claims are reported as unproven, not skipped.

- **Add a `fm prove` front door that picks the method from the claim** — CLEAN — value 4 — effort M — risk med — category: surface
  Why: the user has to know which of many verbs fits. Existing verbs stay as the engines behind it. assumption: kind detection from file extensions and keywords is good enough.
  Done when: `fm prove "the login page shows an error on a bad password"` runs the UI path, and `fm prove "p95 under 50ms"` runs the bench path. Each prints its verdict line.

- **Make performance verdicts one number against one stored baseline** — PERFORMANCE — value 4 — effort S — risk low — category: perf proof
  Why: T-2605 already compares median wall time on a loaded bench, and noise has caused flakes. Reuse that and add no framework.
  Done when: a perf claim reports the median of 5 runs against the stored baseline, and a spread over the noise floor yields "unproven: noisy", not a pass or fail.

- **Make UI proof one screenshot plus one text or accessibility assertion** — FEATURE — value 4 — effort S — risk low — category: UI proof
  Why: `fm shot` exists, and pixel diffs are brittle. A claim like "the page shows X" needs only a text assertion on the rendered output.
  Done when: `fm flow` fails when the asserted text is absent from the captured page, and the shot's hash is stored with the verdict.

- **Treat mutating infra and data probes as unproven by default** — SECURITY — value 4 — effort S — risk low — category: ops proof
  Why: infra and data checks can do damage, and the guard already exists. Only read-only probes (counts, checksums before and after, status reads) count as proof.
  Done when: a probe containing a write is refused with "unproven: needs-user", and a read-only data probe records before and after counts.

- **Require every new verifier to retire an existing gauge** — CLEAN — value 3 — effort S — risk low — category: simplicity
  Why: the lean ratchet and Pay-for-each-addition steers show growth is a worry. assumption: the ratchet can name the retired gauge.
  Done when: a diff that adds a verifier with no deletion or alias in the same change fails `fm check`.

- **Stamp expiry on a proof with a hash of the files it covered** — FEATURE — value 4 — effort M — risk low — category: staleness
  Why: the finish oracle can say done on code that changed afterwards. wild: no, this is plain. Hashing covered files means a stale proof reads as unproven automatically, with no timer.
  Done when: editing a covered file flips that proof to "unproven: stale" in the next `fm status`.

- **Wild: ship the proof as a standalone `proof.sh` with exit codes 0, 1 and 77** — FEATURE — value 4 — effort M — risk med — category: portability
  Why: wild. The user can rerun the proof without Foreman, and 77 means unproven, borrowing the automake skip code.
  Done when: `sh proof.sh` in a clean clone with no `fm` on PATH reproduces every verdict from the task's proof file.

- **Wild: have the Stop hook append a literal "Unproven:" footer when the final message lacks one** — FEATURE — value 4 — effort S — risk low — category: honesty
  Why: wild. The footer is built from the proof file, so the model can't leave out what it didn't prove.
  Done when: a session that closes with an unproven claim ends with a footer listing it, and a fully proven one ends with none.

- **Wild: run a stranger test in which a tool-less child sees only the claim and the evidence file** — FEATURE — value 3 — effort M — risk med — category: meant-check
  Why: wild. This is the cheapest way to catch evidence that doesn't support its claim. It uses the existing tool-less child pattern.
  Done when: planted mismatched evidence in a fixture gets "would not believe" from the child, and matching evidence gets "would believe".

- **Show three counts at finish and no percentage** — CLEAN — value 3 — effort S — risk low — category: receipt
  Why: the user's steers favour plain receipts over scores. "Proven 4, failed 0, unproven 2 (why)" can't be gamed by padding.
  Done when: the finish card prints exactly that line, derived from the proof file.

Next question: which kinds of claim did the user have to verify by hand last month, and did any proof line from Foreman cover them?
Next question: when a proof is "unproven", what does the user actually do next, and could Foreman offer that single action?
