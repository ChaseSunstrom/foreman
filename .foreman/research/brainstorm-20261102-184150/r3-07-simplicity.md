# Brainstorm — lens: simplicity

- **Write one `now.txt` for every device** — FEATURE — value 4 — effort S — risk low — category: devices
  Why: the Desktop tray is blocked on a missing library (T-0325) and the pane, web UI and tick each render state separately. assumption: a phone, watch, tmux bar or Syncthing folder can all read a 5-line text file.
  Done when: after any task change, `cat <state>/now.txt` shows the active task, the next command, the wait reason and the age, and a test checks it matches `fm next`.

- **Add one offline switch for every model call** — SECURITY — value 4 — effort S — risk low — category: privacy
  Why: privacy is listed as thin, and brainstorm, cold-read and steer-expand children all send packs out through separate paths. assumption: one chokepoint can wrap them.
  Done when: with `FM_OFFLINE=1`, every child-spawning verb refuses with one line naming itself, and a test lists every spawn site and fails if one skips the check.

- **Make `fm exam brief T-id` the only Exam runner** — CLEAN — value 4 — effort M — risk low — category: exam
  Why: the carried gap is that every brief's Exam names an outcome measure and a live-state reading, and today each brief invents its own checking command. assumption: one runner can parse both lines.
  Done when: running it on a brief prints PASS, FAIL or UNREAD with the two readings on two lines, and a brief without both lines exits with a usage error.

- **Score a dissent with one fact: did the closed task survive 14 days?** — FEATURE — value 4 — effort S — risk low — category: dissent
  Why: `fm outcomes` already holds 14-day close survival (M-12 spike), and "dissents scored against outcomes" is a carried gap. Reusing it adds no new ledger.
  Done when: `fm outcomes --dissents` lists each dissent as upheld, overruled or too early, using only existing records, and a fixture with three dissents prints each case.

- **Give the Exam one 15-second reading budget** — PERFORMANCE — value 3 — effort S — risk low — category: exam
  Why: live-state readings run in a cold process and nothing bounds how long they take. assumption: any reading that needs more than 15 seconds belongs in a scheduled job instead.
  Done when: a reading that runs past 15 seconds is killed, reported UNREAD with the reason "slow", and a test uses a sleeping reading.

- **Put the three canary hits on one line beside each "not built" claim** — FEATURE — value 3 — effort S — risk low — category: grounding
  Why: the "canaries near the idea" carried gap is easiest to ship as a single line (`near: fm x, T-123, MASTER §y`) rather than a section.
  Done when: every "not built" claim in a Mission file has a `near:` line or the text `near: none found (searched N paths)`, and the Mission check fails if neither is present.

- **Append one rolling hook-timing file instead of a separate bench per concern** — PERFORMANCE — value 3 — effort S — risk low — category: performance
  Why: the lean row, `bench_hooks.py` and doctor each compute hook p95 separately (T-2727 touched the rise rule). assumption: a 200-line ring file can feed all three.
  Done when: hook runs append (name, ms) to one ring file, `fm doctor` and the lean row both read it, and `bench_hooks.py` output matches on a fixture.

- **Cap the guard at 150 rule lines and fail the build above that** — SECURITY — value 3 — effort S — risk med — category: security
  Why: the guard refuses interpreter writes it can't read (fmguard.py:292), and every added rule is more surface a person must audit. assumption: current rules can be merged under the cap.
  Done when: a test counts the rule lines in the guard and fails over 150, and the existing guard exam still passes.

- **Wild: write the whole product on one index card** — FEATURE — value 3 — effort S — risk low — category: legibility
  Why: wild; the standing intent calls for plain explanations, and the README and MASTER.md keep growing. A cold child reads only a 12-line card and must predict what five given commands do.
  Done when: the child gets at least 4 of 5 predictions right, and the card sits at the top of `fm help`.

- **Wild: delete-first first Tuesday** — CLEAN — value 3 — effort M — risk med — category: lean
  Why: wild; on the first Tuesday of the month the tower may file only removals, and every Mission must name what it deletes before what it adds. The 44-item blocked pile and the 30+ "Later from" tasks are the first candidates.
  Done when: the first-Tuesday queue contains only subtractions, and each one records its removed lines or items.

- **Wild: typewriter mode for small screens** — FEATURE — value 3 — effort S — risk low — category: devices
  Why: wild; `FM_PLAIN=1` gives 40-column, no-colour, no-motion output for a watch, SSH on a phone or a car display, and each reading (verdict, wait, next) is one line.
  Done when: `fm next`, `fm status` and `fm doctor` fit within 40 columns with that switch on, checked by a width test.

- **Merge the three "ship gate" waits into one named line** — CLEAN — value 3 — effort S — risk low — category: shipping
  Why: the user typed "Ship N commits to main" about eight times (T-2676, T-2686 and others); `fm next` names the ship step only sometimes. One line, `Ship: N commits waiting → fm ship`, shown in every state.
  Done when: in each tower and queue state `fm next` prints the ship line whenever unshipped commits exist, and no ship request needs typing for a week.

Next question: which of these ideas would the user have to approve versus Foreman simply doing, and does the answer match how they have handled "ship" so far?
Next question: for the thin areas (performance, security, privacy, devices), what is the smallest measured number that shows each is improving?
