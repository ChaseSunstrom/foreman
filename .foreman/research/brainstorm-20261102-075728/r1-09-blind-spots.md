# Brainstorm — lens: blind spots

**Method.** The eight missed asks fall into six classes. For each class I asked the question a brainstorm should have asked, then asked it of the whole project.

| Class | Missed asks | Question |
|---|---|---|
| Measured with no control | T-2534, T-2536 | What is each gauge compared against? |
| Alarm with no cause | T-2535 | When a gate trips, can it name what changed? |
| Unattended thing dead without notice | T-2542 | What proves each background path is alive? |
| Duplicate at birth | T-2546 | Does this already exist? |
| Input shape slips past a refusal | T-2547 | What input shape does each writer accept that it shouldn't? |
| Learner fed its own output, or run on partial input | T-2554, T-2566 | What does each learner read, and what if half of it is missing? |

Several ideas below are only a few lines each. Where the pack shows no evidence, the line says "assumption".

- **Give every steer check a planted violation** — FEATURE — value 4 — effort M — risk low — category: steers
  Why: about 40 standing steers, each with an automatic check from `fm decide --check`. Nothing shows a check can fail. A check that has never failed is the same blind spot as a gauge with no control.
  Done when: `fm genesis sweep` plants a violation per steer in a scratch copy, and any steer whose check stays green is listed red.

- **Print a control-arm table for every ratchet and gauge** — FEATURE — value 4 — effort M — risk low — category: measurement
  Why: the guard-only arm (T-2534) and ablate (T-2536) were each added after a user ask. The class question is "what is the do-nothing baseline here?"
  Done when: `fm doctor` lists each gauge with its baseline arm or the words "no control", and a new gauge without one fails the lean check.

- **Check every writer against its own refusal list** — FIX — value 3 — effort M — risk low — category: input validation
  Why: T-2547 refuses a Mission with no grounding. Other writers (`fm capture`, `fm decide`, `fm task new`, `genesis put`) probably have the same gap. Assumption: not audited.
  Done when: a test feeds each writer five malformed shapes (missing section, count mismatch, empty, duplicate, truncated) and each is refused or logged with a repair line.

- **Run each learner on its own with the Foreman-authored share removed** — SECURITY — value 4 — effort M — risk med — category: learners
  Why: T-2554 found Mission briefs and mistaken captures feeding the user model. The foresight, calibration and lessons learners likely share that flaw.
  Done when: each learner reports its input count by origin, and the exam fails if Foreman-authored input is above 10%.

- **Test every decision procedure with each input split empty** — FIX — value 4 — effort M — risk low — category: reliability
  Why: T-2566 (`select` ignoring held-out-only lines) shows the pattern. Candidates by name: `fm genesis select`, `fm ship --chance`, and the calibration windows from T-2610.
  Done when: each procedure has a test per empty split, and the result is "inconclusive" or a refusal, never a silent keep or revert.

- **Name the cause on every tripped gate, ratchet or WARN** — FEATURE — value 4 — effort M — risk low — category: observability
  Why: T-2535 named the commit behind lean growth. The same need exists for the bench gate, sweep rows, doctor WARNs and the Brier gap.
  Done when: each red row prints "since <commit/task>: <metric before> to <after>", or "cause unknown" with a bisect command.

- **List every unattended path with its last-alive time** — OBSERVABILITY, filed as FEATURE — value 4 — effort S — risk low — category: liveness
  Why: T-2542 covered systemd units. Others are untested: the drive, `fm genesis live` publishes, ci-watch, lanes, hooks that fall back to the committed library. Assumption: some of these have no liveness row.
  Done when: `fm doctor` shows a table of unattended paths, each with last run time and result, and any path older than 3 intervals is flagged.

- **Check "already built" at every filing point, not only capture** — FIX — value 3 — effort S — risk low — category: duplicates
  Why: T-2546 covers capture and `fm task new`. Genesis Mission briefs, tick-filed tasks, "Later from" bundles and sweep-created fix tasks are other filing points.
  Done when: each filing path calls the same match and prints the clause and task id, and a test files a known duplicate through each path.

- **Add a "last verified on" harness stamp to every capability claim** — DOCS, filed as CLEAN — value 3 — effort M — risk low — category: docs
  Why: the README says "works on Codex, Gemini, opencode", but T-0335, T-0336 and T-0337 are blocked and unverified. The site's claims are checked against exam lines, but harness support is not.
  Done when: a generated matrix in the README shows verified, unverified or hook-less per feature and harness, and `fm doctor` fails when the README claims more than the matrix.

Wild ideas:

- **Hold a blind-spot bounty each generation (wild)** — FEATURE — value 3 — effort M — risk low — category: genesis
  Why: assumption. The 8 misses were found only after the user asked. A cold child that has never seen the code writes the 5 questions it would ask a stranger's product, and any that match a later user ask score a hit.
  Done when: the sweep records a sealed list per generation and reports the hit rate against asks arriving in the next 30 days.

- **Run a "user is away for a week" drill (wild)** — FEATURE — value 3 — effort L — risk med — category: unattended
  Why: assumption. Many gaps are visible only when no human touches the system. A fixture repo runs seven days of injected events with the real tick, and the drill lists what broke silently.
  Done when: a report lists each unattended path as alive, dead or silent, with the injected fault that exposed it.

- **Put a "what I can't see" panel in the web UI (wild)** — FEATURE — value 3 — effort M — risk low — category: ui
  Why: assumption. The user keeps finding blind spots by asking. The panel lists each gauge's omissions, the learners with no control, and the paths with no liveness row.
  Done when: the panel renders from `fm doctor --json`, and each line links to the verb that would close it.

Next question: Which of the user's steers have no automatic check at all, and would a planted violation of each be caught within one sweep?
Next question: Which filing paths and writers are not yet covered by a refusal or an "already built" check?
