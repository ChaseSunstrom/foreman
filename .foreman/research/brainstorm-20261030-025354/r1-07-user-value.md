# Brainstorm — lens: user value

- **Replace the deterministic finders with a "read the code like a reviewer" finder** — FEATURE — value 5 — effort L — risk med — category: initiative
  Why: exam s0-001 shows fmdocs.scan + fmsecrets found 0 of 108 planted defects while plain Claude finds 3/3 held-out bugs at ~0.17 USD. Mission 3 is graded on `bug` and `none` kinds in unseen repos, so the finder must actually read source. Assumption: one cheap model call per hot file, ranked by churn and missing tests, is affordable.
  Done when: on the held-out exam's bug kind, the finder reports at least the planted bug in ≥2 of 3 never-seen repos at ≤0.20 USD per repo.

- **Refuse to report a finding without a failing test** — FEATURE — value 5 — effort M — risk low — category: proof
  Why: the request says "proves each finding with a failing test". The `none` kind in the exam punishes false positives, so unproven claims must not reach the user. Assumption: a finding with no repro in N tries is dropped, not downgraded.
  Done when: on a repo with zero planted defects (exam `none`), the pipeline outputs zero findings; on a planted bug, the output includes a test that fails on the unfixed tree and passes after the fix.

- **Rank findings by value with a visible score** — FEATURE — value 4 — effort M — risk low — category: ranking
  Why: the Missing list names "value ranking". Assumption: score = severity × likelihood of reaching users (hot path, churn, entry-point reachability) ÷ fix cost.
  Done when: `fm scout --rank` prints findings sorted with each term of the score shown, and a test pins that a crash on an entry path outranks a typo in docs.

- **Cut the false-positive tax with a "none" self-check** — FIX — value 5 — effort S — risk low — category: precision
  Why: exam includes `none` repos; a finder that always finds something fails them. Assumption: the finder may answer "nothing worth doing" and that is a scored success.
  Done when: running the finder on three clean fixtures yields "no findings" each time, with a one-line reason.

- **Stop queueing Foreman's own setup failures in user projects** — FIX — value 4 — effort S — risk low — category: scout
  Why: pack "Noticed: probe_doctor may queue Foreman setup failures as tasks in user projects." Assumption: such tasks should go to a Foreman-only list.
  Done when: in a fixture project with a broken Foreman hook, `fm scout` queues no task in that project and prints one Foreman-side note instead.

- **Run scout probes for the project's own language, from its CI and manifests** — FEATURE — value 4 — effort M — risk med — category: probes
  Why: the exam spans python, js, ts, ruby, rust, c; Foreman's probes are Foreman-only. Assumption: infer test/lint/type commands from CI files and manifests, run them read-only, and turn red output into findings.
  Done when: on a fixture for each of the six languages, scout runs the inferred check and a seeded failure becomes a finding naming the file.

- **Bisect flakes into a named test and a cause** — FEATURE — value 3 — effort M — risk med — category: flake finder
  Why: adopt already reruns gates once; the exam has a `flake` kind. Assumption: rerun the failing test alone N times, then with shuffled order, and report which.
  Done when: a seeded order-dependent test is reported as order-dependent with the polluting test named.

- **Fix findings in lanes with a cost cap and an exit receipt** — FEATURE — value 4 — effort M — risk med — category: pipeline
  Why: Foreman's session costs more than plain Claude for the same score; user pushes on cost. Assumption: cap per finding about 0.25 USD, abort and report when exceeded.
  Done when: a finding that cannot be fixed under the cap is closed as "found, proven, not fixed" with spend shown, and the lane leaves no stray edits.

- **Show a morning findings digest, one line each, accept with one key** — FEATURE — value 3 — effort S — risk low — category: ux
  Why: fm night already queues work; users reply with short asks. Assumption: findings default to proposed, never auto-merged.
  Done when: `fm morning` lists proven findings with value scores, and `fm morning accept 2` queues only that one.

- **Wild: Let Foreman plant its own bug and see if the finder catches it** — FEATURE — value 3 — effort M — risk low — category: self-test — wild
  Why: assumption: a mutation (flip an operator in a hot file) with a green suite measures finder recall in the user's own repo.
  Done when: `fm scout --calibrate` mutates a scratch copy, runs the finder, and prints recall as a fraction.

- **Wild: Keep a "bugs found, bugs real" scoreboard from 30-day survival** — FEATURE — value 3 — effort M — risk low — category: trust — wild
  Why: the standing steer says weakness-finding by outside signals; `fm outcomes` already tracks survival. Assumption: it can tag fixes born from findings.
  Done when: `fm outcomes --findings` shows the share of finding-born fixes still unreverted after 30 days.

- **Wild: Fuzz the entry points to turn crashes into findings** — FEATURE — value 3 — effort L — risk med — category: bug finder — wild
  Why: assumption: a crash from short random input is a self-proving finding with no model needed, and cheap.
  Done when: on a fixture with a parser that crashes on empty input, scout files a finding with a minimal input that reproduces it.

- **Skip repos the finder already cleared until the code changes** — PERFORMANCE — value 2 — effort S — risk low — category: cost
  Why: repeated scans cost money for no new information. Assumption: key the clearance on the tree hash of each scanned file.
  Done when: a second `fm scout` on an unchanged tree makes zero model calls and says so.

Next question: What does a finder's precision look like on real repos with no planted defects, and who labels the "found" items as true or false?
Next question: Should a finding that is real but low value be filed at all, or does the `none` grading reward silence?
