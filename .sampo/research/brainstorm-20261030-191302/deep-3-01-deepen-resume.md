# Brainstorm — lens: deepen: resume

- **Build a resume digest that ranks "since you left" by what the plan cares about** — FEATURE — value 5 — effort M — risk low — category: resume
  Why: combines "since you left" and "what changed, in the order I care about". Evidence: the user steers in the tower (gen-0 MUSTs, standing rules, `fm decide --check`); a resume that lists commits flat buries a changed standing rule under a docs commit. Assumption: Foreman can already diff git, ledger and tower files between two timestamps.
  Done when: after a scripted gap that changes a standing rule, a gate result and a docs file, the first prompt's digest lists the rule change first, the gate second, docs last, and a test asserts the order.

- **Seal the baton with a hash and verify it on every leg** — SECURITY — value 4 — effort S — risk low — category: resume
  Why: answers the left-over question "who checks that file wasn't edited between legs?". The charter seal (sha256, 444, ledger event) already exists for gen-0; the goal baton and done-definition have no such check.
  Done when: editing a goal's done-definition file between two legs makes `fm doctor` and the next resume report "done-definition changed since leg N" with the diff, and an unedited baton passes silently.

- **Cap the plan to the baton's budget and say what was dropped** — FIX — value 4 — effort M — risk med — category: resume
  Why: grows "warn when the plan is longer than the baton can carry" into a rule. Evidence: the pack's open question about the largest absorbable baton. Assumption: the baton has a measurable token size and a fresh session's first move can be scored.
  Done when: a 300-row plan produces a baton under the configured limit, the plan keeps a "carried / parked" split visible on resume, and a test shows that every parked row is still reachable through `fm` by id.

- **Replay the first move: test that a cold session picks the right next action from the baton alone** — FEATURE — value 5 — effort M — risk med — category: resume
  Why: a fingerprint says what changed, but not whether a fresh model reads the baton correctly. The exam machinery (held-out scenarios, child-authored kinds) already grades sessions, and a "resume" kind is missing.
  Done when: `fm exam` has a resume kind with at least 3 scenarios (killed mid-task, compacted, changed toolchain), each graded by whether the first action matches the expected one, and the scorecard shows a per-model-tier score.

- **Fingerprint the toolchain and re-baseline only the gates that depend on it** — PERFORMANCE — value 3 — effort M — risk low — category: resume
  Why: grows "fingerprint git and toolchain state". A full re-baseline after every gap is slow, and `fm map` already knows each gate's command. Assumption: gates can declare or infer which files and binaries they read.
  Done when: upgrading only the Python version re-runs the Python-dependent gates and leaves the rest cached, with the resume digest naming the reason for each re-run.

- **Add an external witness for kills that no hook saw** — FEATURE — value 4 — effort M — risk med — category: resume
  Why: answers the left-over question about stops with no hook. A heartbeat file (pid, last tool, last ledger offset) written on each hook and checked at next start tells "clean stop" from "killed" with nothing running while the session is down.
  Done when: killing a session with SIGKILL mid-task makes the next start print "last session ended without a stop (killed ~14:02, mid T-NNNN)", and a clean stop prints nothing.

- **Separate "the user changed their mind" from "a row was missing" in reopen records** — FEATURE — value 3 — effort S — risk low — category: resume
  Why: answers a left-over question directly. The user's steers are already captured as intake and `fm decide`; a reopen that follows a steer on the same goal can be tagged by that link, with no model guess.
  Done when: reopening a goal within a window of a logged steer tags it "steer-driven" and the miss rate excludes it, shown in a test with one tagged and one untagged reopen.

- **Let the user veto a carried-over plan row in one line on resume** — FEATURE — value 3 — effort S — risk low — category: resume
  Why: answers the veto question. After a long gap the digest shows each carried row with an id, and `fm drop T-id "why"` stores a standing rule so the same row isn't re-planned.
  Done when: dropping a row on resume removes it from the baton, the drop reason appears in the next digest, and replanning the goal doesn't bring the row back.

- **Resolve two open goals at Stop by naming the owner explicitly** — FIX — value 3 — effort S — risk med — category: resume
  Why: answers the left-over Stop-hook question. With two goals open, a close judged against the wrong ledger is a false "done".
  Done when: a test with two open goals closing one confirms the verdict is written only to that goal's ledger, and an ambiguous close asks which goal rather than guessing.

- **Wild: Resume as a letter from your past self — a one-paragraph, first-person handoff written at stop** — FEATURE — value 3 — effort S — risk low — category: resume wild
  Why: assumption: a short note written by the leaving session ("I was about to test X, I distrust Y") carries intent a ledger can't, and it can be checked against the ledger on resume, flagging claims the files contradict.
  Done when: a resumed session shows the letter with any contradicted claims struck through and cited.

- **Wild: Time-travel resume — `fm resume --as-of <date>` rebuilds the plan and baton as they stood then** — FEATURE — value 3 — effort M — risk low — category: resume wild
  Why: assumption: the ledger is append-only, so state at any past moment can be derived. It helps when a plan went wrong after a steer, and the long-horizon exam already rolls repos back to past commits.
  Done when: `fm resume --as-of` on a test goal prints the plan rows and open items matching a snapshot taken at that time.

- **Wild: Resume rehearsal — a nightly dry run that wakes a cold child on the baton and reports whether it would have made the right move** — FEATURE — value 4 — effort M — risk med — category: resume wild
  Why: assumption: the baton rots as the repo changes. A cheap Haiku child that reads only the baton and states its first move, compared with the plan's true next row, flags drift before the user returns.
  Done when: a scheduled rehearsal over a goal with a deliberately stale baton writes a "baton would misdirect" note to the inbox, and a fresh baton produces none.

- **Show the cost of a gap: tokens and minutes to get back to speed** — FEATURE — value 2 — effort S — risk low — category: resume
  Why: answers the question of whether reopen cost differs by class. Measuring the first N minutes after each resume, split by gap length and cause, gives the planner data on where to spend rows.
  Done when: `fm friction` lists median resume cost by gap bucket, and a test feeds three synthetic resumes and checks the buckets.

Next question: Which parts of a resume are the user actually reading, and would a one-line "nothing changed, continue T-NNNN" be better for most gaps than any digest?
Next question: When the baton, the ledger and the repo disagree after a kill, which one wins by rule, and does the user ever see the disagreement?
