# Brainstorm — lens: reliability

- **Reap orphaned children from a process registry** — FIX — value 5 — effort M — risk med — category: process hygiene
  Why: the pack shows a hung check holding the gate lock for over 40 minutes, and a child holding pipes after its parent died. Assumption: children are tracked only in the parent's memory, so a killed run leaves them with no owner.
  Done when: `kill -9` on a run leaves no child whose parent is init and whose cwd is the project within 5 s, checked by a test.

- **Fail a gate that runs zero tests** — FIX — value 5 — effort S — risk low — category: gate trust
  Why: T-1807 showed a fake `git` that exited at once and made a lock look unheld. A gate that exits 0 after running nothing is the same failure mode. Assumption: some gate commands pass without executing any test.
  Done when: a gate whose output reports 0 tests collected is recorded as failed with the reason "ran nothing", and a test seeds an empty suite and sees that.

- **Shuffle test order per run and log the seed** — FIX — value 4 — effort S — risk low — category: flake repro
  Why: the pack shows failures that appear only on CI (chromium under parallel load, uutils `sleep`). Order coupling between tests is a likely cause. Assumption: the suite has order dependencies that have not been measured.
  Done when: a shuffled failure prints `--seed N`, and rerunning that seed on the same tree fails the same test in 3 of 3 runs.

- **Refuse a gate that disagrees with itself** — FEATURE — value 4 — effort M — risk low — category: gate trust
  Why: T-1810 reported red CI on main from a cancelled run, a false alarm that cost a session. A gate that flips on an unchanged tree teaches people to ignore it. Assumption: some gates are nondeterministic.
  Done when: running the same gate twice on an unchanged tree with different verdicts marks it "unstable", and `fm done` refuses to close on it.

- **Run each gate with a private HOME, TMPDIR and an allowlisted environment** — FIX — value 4 — effort S — risk low — category: hermetic gates
  Why: T-1791 showed an inherited 200k window failing 10 bench tests. Gates currently inherit the caller's environment. Assumption: other inherited variables could change gate results the same way.
  Done when: a gate run with a poisoned `CLAUDE_CODE_*` variable and a foreign `HOME` gives the same verdict as a clean run, tested.

- **Check for leaked descriptors, children and lease files at run end** — FIX — value 4 — effort S — risk low — category: resource leaks
  Why: an edit lease outlived its run for 20 minutes in the pack. Only that leak was caught; the rest are unmeasured. Assumption: other leaks exist.
  Done when: a run that exits with an open lease or a live child writes a named leak line to the journal, and a seeded leak in a test is reported by name.

- **Frame each journal line with a length and CRC** — FIX — value 3 — effort S — risk low — category: journal integrity
  Why: several surfaces write the same journal, and a crash can leave a torn final line. Assumption: concurrent writers can tear a line today.
  Done when: a journal truncated at every byte offset of a three-event fixture reads back every earlier event intact and names the torn line.

- **Apply backpressure from the journal writer to its lanes** — PERFORMANCE — value 3 — effort M — risk med — category: backpressure
  Why: when the disk stalls, unbounded buffering grows memory and loses events on a crash. Assumption: the writer has no bound today.
  Done when: with the writer blocked for 10 s, the lane pauses at the cap, and a test counts every event after the writer resumes with none lost.

- **Make SIGHUP and SIGINT checkpoint before exit** — FIX — value 4 — effort S — risk low — category: clean shutdown
  Why: a closed terminal kills a run mid-write, and the lease and lock are released only on a normal exit. Assumption: runs die on SIGHUP today without a checkpoint.
  Done when: SIGHUP sent mid-task leaves a checkpoint, releases the lease, and `fm status` reads "stopped at step N, resumable".

- **Pin one exit-code table for every verb and test it** — CLEAN — value 3 — effort S — risk low — category: exit codes
  Why: the pack's `fm quiet` case exited 0 while doing nothing, which broke a script's assumption. Scripts rely on exit codes, and nothing enforces a shared table. Assumption: verbs choose codes ad hoc.
  Done when: a test fails if any verb exits with a code missing from the documented table.

- **Wild: hold a shutdown inhibitor until the checkpoint lands** — FEATURE — value 3 — effort M — risk low — category: power safety
  Why: wild: a systemd inhibitor lock can delay reboot or sleep until a run has written its checkpoint, so a power event never lands mid-write. Assumption: the host runs systemd.
  Done when: `systemd-inhibit --list` shows Foreman's lock during a run and the lock releases only after the checkpoint is written.

- **Wild: hardlink-snapshot the state directory before each risky verb** — FEATURE — value 4 — effort M — risk low — category: rollback
  Why: wild: hardlinks cost almost no space, so every destructive verb can keep a cheap, restorable copy of the state it is about to change, pruned by age. Assumption: state files are small and rarely rewritten in place.
  Done when: `fm undo` after a risky verb restores the state byte-for-byte, checked by diffing against the snapshot.

- **Wild: power-cycle a VM at random points during a queue** — FIX — value 3 — effort L — risk low — category: crash torture
  Why: wild: a nightly torture job pulls the virtual plug at random moments in a queue and requires zero lost or duplicated events. Assumption: the crash-point tests do not cover arbitrary timing.
  Done when: 50 random power cuts in a seeded queue each recover with zero lost or duplicated journal events, and the seed for any failure is printed.
