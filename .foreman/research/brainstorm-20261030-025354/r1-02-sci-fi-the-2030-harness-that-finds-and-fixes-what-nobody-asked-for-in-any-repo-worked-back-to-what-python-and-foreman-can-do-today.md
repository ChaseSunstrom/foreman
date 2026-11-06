# Brainstorm — lens: sci-fi: the 2030 harness that finds and fixes what nobody asked for in any repo, worked back to what Python and Foreman can do today

- **Make the model the finder and the test the judge** — FEATURE — value 5 — effort M — risk med — category: initiative
  Why: the deterministic finders (fmdocs.scan, fmsecrets) found 0 of 108 planted defects, while plain Claude finds 3/3 at about $0.17. The pack also says Mission 3 is graded on `bug` and `none` in unseen repos.
  Done when: on a fixture repo with one planted bug, `fm scout --find` runs a read-only `claude -p` per hot module, discards every hypothesis that has no failing test, and files only the proven one.

- **Return "clean" as a first-class verdict** — FEATURE — value 5 — effort S — risk low — category: precision
  Why: the exam's `none` kind rewards saying nothing was wrong. Finders that always return something fail it.
  Done when: on a repo with no defects, `fm scout --find` exits 0, files zero tasks, and prints a receipt listing which probes ran and what each ruled out.

- **Replay git history as a private recall exam** — FEATURE — value 5 — effort M — risk low — category: measurement
  Why: the user's standing steer is to find weaknesses by outside signals only. Real bug-fix commits are free labelled defects in any repo.
  Done when: `fm scout --replay N` checks out the parent of N commits that fix bugs (by `fix` in the subject plus a changed test), runs the finders there, and reports how many were rediscovered, plus precision on commits that changed nothing risky.

- **Reject proofs that fail for the wrong reason** — FIX — value 4 — effort S — risk low — category: proof
  Why: a failing test is the pipeline's gate, but an ImportError or a missing fixture also fails. Without a check, junk gets "proved".
  Done when: a finding whose test fails on a collection or import error is marked `unproven`, and a test is accepted only if its failure message mentions the symbol under suspicion.

- **Hunt the sibling of every past fix** — FEATURE — value 4 — effort M — risk med — category: bug finder
  Why: assumption: bugs repeat in shape. Past fix diffs show the shape (a missing None check, an off-by-one in a slice), and a grep-plus-model pass can look for the same shape elsewhere.
  Done when: given a fixture where one file was fixed for an unchecked `.get()`, the finder flags the identical unfixed call in a second file with a failing test.

- **Rank findings by reach, proof strength and cost** — FEATURE — value 4 — effort M — risk med — category: value ranking
  Why: the ranking is missing in the Mission 3 gap list. Import-graph callers give a cheap reach number, and `fm outcomes` survival can later calibrate it.
  Done when: `fm findings` lists each item with a score and its three terms, and a test shows a finding in a widely imported module outranks the same finding in a leaf script.

- **Stop scout filing Foreman's own setup failures in user projects** — FIX — value 3 — effort S — risk low — category: scout hygiene
  Why: the pack notes probe_doctor may queue Foreman setup failures as tasks in user projects.
  Done when: a scout run in a project with a broken Foreman install files nothing about Foreman, and a regression test covers it.

- **Prove a flake by its reproduction rate** — FEATURE — value 3 — effort M — risk low — category: flake finder
  Why: the exam has a `flake` kind and `adopt` reruns once. A single rerun cannot separate a flake from a real failure.
  Done when: the finder reruns the suite N times with a shuffled order, a fixed seed and a changed TZ, then files only tests that both pass and fail, with the fail rate in the finding.

- **Prove a perf finding with a scaling test** — FEATURE — value 3 — effort M — risk med — category: perf finder
  Why: the `perf` kind needs more than "this looks slow". A runtime ratio at 1× and 4× input size is a checkable claim.
  Done when: a fixture with a quadratic loop yields a generated test that fails because 4× input takes more than 8× time, and it passes after the fix.

- **Wild: Prosecutor and defender agents** — FEATURE — value 4 — effort M — risk med — category: agents
  Why: wild. One child must write the failing test for a claim, and a second child tries to show the test is wrong or the behaviour intended. Only claims that survive are filed. This should lower false positives on the `none` repos.
  Done when: on a repo containing a deliberately odd but intended behaviour, the defender wins and nothing is filed; on a real bug, both rounds end in a filed finding.

- **Wild: Night watch seeded by the day's diff** — FEATURE — value 3 — effort M — risk low — category: overnight
  Why: wild. Each night the queue picks random recently changed functions and asks a child for three inputs that break them, then runs those inputs. A crash becomes a failing-test finding by morning.
  Done when: `fm night` includes a fuzz job, and a seeded bug in yesterday's commit is reported with its repro in the morning list.

- **Wild: Spend the night's budget as a knapsack over findings** — FEATURE — value 3 — effort M — risk med — category: planning
  Why: wild. Ranked findings carry an estimated fix cost, and the headroom before the usage reset is known. Pick the set that maximises value within it, and leave the rest filed.
  Done when: given five findings with scores and costs and a fixed budget, `fm run --fit` chooses the set with the highest total score, and a test checks that choice against brute force.

- **Wild: Publish a precision scorecard per ecosystem** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: wild. The pack shows the exam spans six languages, so a per-language table of filed, proved, fixed and survived keeps Foreman honest where it is weak.
  Done when: `fm exam --card` prints rows for python, js, ts, ruby, rust and c with counts of findings, proofs and false positives.

Next question: Which finder kinds does plain Claude beat Foreman on for cost per proved finding, and is the right move to have Foreman drive Claude for those instead of building its own?
Next question: How does an unattended lane tell a real bug from intended but odd behaviour without asking the user, given that the exam's `none` repos reward silence?
