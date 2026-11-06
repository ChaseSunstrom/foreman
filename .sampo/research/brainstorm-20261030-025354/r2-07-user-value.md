# Brainstorm — lens: user value

- **Open every finding as a failing test the user can run in one command** — FEATURE — value 5 — effort M — risk low — category: proof
  Why: the exam shows finders caught 0 of 108 planted defects, and Mission 3 demands a failing test before any code is touched. A finding the user can reproduce with one pasted command is the only kind they will trust, so the finding itself should be that command.
  Done when: every item in the findings list carries a `repro:` line that exits non-zero on the untouched tree, and `fm find show F-n` prints and runs it.

- **Return a "clean" verdict with the evidence behind it** — FEATURE — value 5 — effort S — risk low — category: trust
  Why: the exam grades the `none` kind in never-seen repos, and a user who hears "nothing found" can't tell a clean repo from a blind scan. assumption: users currently get silence, not a result.
  Done when: scanning a planted-clean repo prints "clean: N files read, M probes run, 0 proven" and files no task.

- **Replace deterministic finders with a read-only model hunter that must attach a repro** — FEATURE — value 5 — effort L — risk med — category: finders
  Why: fmdocs.scan and fmsecrets found 0 of 108 planted defects while plain Claude found 3/3 on held-out bugs at about 0.17 USD each. The user wins only if the model finds and a test judges.
  Done when: on the held-out exam bug kind, the hunter's recall beats the 0/108 baseline, and every filed finding has a red test on the untouched tree.

- **Show a morning card: one line per proven finding, one key to land or drop** — FEATURE — value 4 — effort M — risk low — category: review
  Why: the user steers by short asks and drops; unasked work only helps if accepting it costs seconds. fm night already exists, so the card is its output. assumption: a queue of lanes finishes unattended.
  Done when: after `fm night`, `fm find card` lists each fixed finding with diff size, proof and cost, and `y`/`n` lands or reverts it.

- **Rank findings by value per dollar with the formula printed beside each** — FEATURE — value 4 — effort S — risk low — category: ranking
  Why: the mission asks for ranking by value, and the user has asked repeatedly for "why is this next" style legibility. assumption: reach and proof strength are derivable from fm map.
  Done when: each ranked finding shows `score = reach × severity ÷ est. cost` with its inputs, and a test pins the order on a fixture.

- **Stop filing Foreman's own setup failures as tasks in user projects** — FIX — value 4 — effort S — risk low — category: noise
  Why: the pack notes probe_doctor may queue Foreman setup failures in user projects, which is exactly the unasked work a user resents.
  Done when: a project with a broken hook install gets a doctor warning and zero backlog tasks from scout.

- **Remember dismissals by fingerprint so a declined finding never returns** — FEATURE — value 4 — effort S — risk low — category: noise
  Why: the user repeatedly drops items, and re-filing them wastes attention. Fingerprint by test name plus file hash.
  Done when: dropping a finding and rescanning an unchanged tree files nothing; changing the file reopens it.

- **Reject fixes that pass by hardcoding the test's literal** — SECURITY — value 4 — effort M — risk med — category: fix quality
  Why: a lane told to turn a test green can cheat. Users judge the whole feature on whether fixes hold, and 30-day survival is the outside signal the steers prefer.
  Done when: a fixture fix that returns the expected literal is rejected by a second varied-input check, and an honest fix passes.

- **Offer a first scan with its cost and a "no" path** — FEATURE — value 3 — effort S — risk low — category: onboarding
  Why: an earlier question asks what a user does when an auto-start proposal appears. Show the dollar cap, the files read-only guarantee, and the decline command in the offer itself.
  Done when: the first `fm scout` in a new project prints cost cap, scope and `fm scout --no` before spending anything.

- **Wild: Plant canary bugs in a scratch copy of the user's repo and publish Foreman's recall there** — FEATURE — value 4 — effort L — risk med — category: calibration
  Why: wild. The exam only grades Foreman on repos the user doesn't own; this tells the user how much to trust it on theirs.
  Done when: `fm find calibrate` plants N bugs in a temp copy, runs the hunter, and prints recall without touching the real tree.

- **Wild: A prosecutor and defender pair argue each finding before it reaches the card** — FEATURE — value 3 — effort L — risk med — category: precision
  Why: wild. Cheap false positives are what make users stop reading; an adversarial cold read prices that in before the user sees it.
  Done when: findings the defender refutes are listed under "dismissed by review" with the reason, and the card shows only survivors.

- **Wild: A weekly "what I found for you" note in plain words** — FEATURE — value 3 — effort M — risk low — category: reporting
  Why: wild. Users outside the terminal still get value if one paragraph says what broke, what was fixed and what it saved.
  Done when: `fm find weekly` writes a one-page note with counts, fixes landed, and one sentence per finding, no jargon.

- **Cap each hunt by cost per confirmed finding** — PERFORMANCE — value 3 — effort S — risk low — category: spend
  Why: Foreman's session costs more than plain Claude for the same score; the user must see that unasked work does not outspend its yield.
  Done when: a hunt stops once spend exceeds a set multiple of its confirmed finds, and the receipt reports dollars per proven finding.

Next question: Do users who accept findings keep them 30 days later, and which finding kinds are they never keeping?
Next question: What should a user see when the repo has no runnable tests, so a proof is impossible?
