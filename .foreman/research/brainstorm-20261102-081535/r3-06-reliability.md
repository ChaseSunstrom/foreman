# Brainstorm — lens: reliability

- **Run every prover inside a reaper scope** — FIX — value 4 — effort S — risk low — category: process hygiene
  Why: `fm shot` and `fm flow` start browsers and dev servers. A killed or timed-out run (usage-limit stop, hook deadline, Ctrl-C) can leave them behind, which poisons the next run's ports and makes it flaky. The pack lists "fail a proof that leaves residue" but not guaranteed cleanup after a kill. Assumption: `systemd-run --user --scope` or a process group is available.
  Done when: killing `fm flow` with SIGKILL mid-run leaves zero child processes and zero bound ports after 2 s, tested.

- **Store proof evidence in a content-addressed, off-tmpfs store** — FEATURE — value 4 — effort M — risk low — category: evidence durability
  Why: the working directory here is under `/run/user/1000`, which is tmpfs, and the pack already lists "keep in-flight child output off tmpfs-only paths". A proof that cites a screenshot or trace that has since vanished still reads as proven. Screenshots, traces and logs should be stored by hash with a size cap, and a missing hash should downgrade the proof to `unproven: evidence lost`.
  Done when: deleting one referenced artifact makes `fm task show` print that proof as unproven with the reason `evidence lost`.

- **Run a control on the parent commit for every red** — FEATURE — value 4 — effort M — risk med — category: failure attribution
  Why: a red result does not say whether the change, the harness or the environment caused it. Rerunning the same proof at HEAD~ (or the stash) separates "new red", "already red" and "red on both because the harness is broken". The pack has "explain red by last-green delta" and bisecting, but no immediate control run.
  Done when: a planted environment fault (port taken) yields `harness/env red` and a planted code break yields `change red`, in two fixture tests.

- **Retry only on known-transient signatures, and label a retry-pass as flaky-pass** — FIX — value 3 — effort S — risk low — category: flake policy
  Why: a blanket retry can hide real intermittent bugs, and no retry makes browser startup timeouts look like failures. A small signature list (ECONNREFUSED on a freshly started server, browser launch timeout) allows exactly one retry, recorded as `flaky-pass`, never `pass`.
  Done when: a fixture failing 1 in 2 on a transient signature shows `flaky-pass`, and one failing on an assertion is never retried.

- **Calibrate prover deadlines to a measured machine speed factor** — PERFORMANCE — value 3 — effort S — risk low — category: timeouts
  Why: the pack asks for time-boxed provers and a bench noise floor, but fixed seconds are too tight on a loaded laptop and too loose on a fast box. One 2-second calibration, cached with a decay, scales every deadline, and the factor is stamped on the proof.
  Done when: the same flow gets different deadlines under `taskset`-throttled and unthrottled runs, and the factor appears in the proof record.

- **Pause a judge child at a usage limit and resume, never record unproven** — FIX — value 4 — effort M — risk med — category: unattended resilience
  Why: standing steer 2026-10-31 #3 says to wait out real usage limits and resume. A model-judged proof that hits a limit mid-run should become `pending (limit)` and be finished later. Recording `unproven` for a transient limit corrupts the ledger. Assumption: the existing limit detection can be reused.
  Done when: a faked limit response leaves the proof `pending`, and after the fake clears the proof completes with the same inputs.

- **Kill -9 at every step of `fm prove`, `shot` and `flow`** — FIX — value 4 — effort M — risk low — category: crash safety
  Why: the pack proposes this for goal state and the tick, but not for the provers' own pipeline (start, capture, compare, write). Each step should end up resumable or cleanly `abandoned`, with no half-written proof ever read as a verdict.
  Done when: a harness kills the run at each of N numbered steps and then `fm doctor` reports no torn proof and no orphaned directory.

- **Replay golden evidence bundles through the prover on every upgrade** — FEATURE — value 4 — effort M — risk low — category: regression tape
  Why: "recall proofs made by a buggy prover" is after the fact. A frozen set of 20 bundles (a screenshot pair, a doc-versus-code case, a data diff), each with a hand-labelled verdict, is replayed at `fm ship`. A changed verdict blocks the ship and names the prover.
  Done when: editing the screenshot comparator's threshold flips one labelled bundle and the ship gate goes red naming it.

- **Make proof-ledger writes single-writer and torn-tail tolerant** — FIX — value 3 — effort S — risk low — category: ledger integrity
  Why: parallel lanes and the night tick can each finish a proof at once. An append lock, fsync and a reader that skips a truncated last line prevent a lost or half-parsed record. Assumption: the proof ledger is append-only text.
  Done when: 20 concurrent writers plus a truncated final line leave all 20 records readable.

- **Stamp host conditions on every proof and report flake correlation** — FEATURE — value 2 — effort S — risk low — category: diagnosis
  Why: flaky verdicts are cheaper to fix when you know they cluster at load average above 4 or free memory below 500 MB. Record the load, free memory and disk on each proof, and let `fm doctor` name the condition behind the most flips.
  Done when: seeded fixture flakes under load show up as `flips cluster at load>X` in doctor.

- **Wild: ship a hostile crash-test repo and soak every prover against it** — FEATURE — value 4 — effort M — risk low — category: soak (wild)
  Why: a bundled sample project that hangs, leaks processes, prints ANSI and megabyte-long lines, writes outside its directory and fails 1 run in 5. `fm doctor --soak` runs each prover on it and expects a bounded, labelled outcome every time. Assumption: nothing like it exists yet; the fixtures under `plugin/tests/fixtures` are well-behaved.
  Done when: all provers finish the soak with only `pass`, `fail`, `inconclusive` or `could-not-run`, never a hang or a crash.

- **Wild: use the previous Foreman release as a second verifier** — FEATURE — value 3 — effort M — risk med — category: N-version check (wild)
  Why: this is a cheap independent implementation. At finish, run the last released prover on the same evidence and flag any disagreement in verdict, since a regression in the new code is the most likely cause.
  Done when: a deliberately regressed comparator in a scratch copy produces a `verifier disagreement` line at finish.

- **Wild: add a lifeboat unit that finishes or abandons half-done proofs after a crash** — FEATURE — value 3 — effort M — risk med — category: recovery (wild)
  Why: an OOM kill or power loss mid-`fm flow` leaves a partial proof directory that nobody revisits. A user-level path unit, or the next session start, resumes it or marks it `abandoned: machine died` and tells the user.
  Done when: after a simulated kill, the next `fm` call shows the proof as abandoned or resumed, never silently missing.

Next question: Which provers have no deadline, process cleanup or `could-not-run` outcome today, and which of those have actually been seen to hang?
Next question: What does the user see when a proof's verdict changes between two runs of the same commit, and where does that flip get recorded?
