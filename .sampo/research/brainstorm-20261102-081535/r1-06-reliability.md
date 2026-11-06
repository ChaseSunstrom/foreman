# Brainstorm — lens: reliability

- **Stamp every proof with its reality level** — FEATURE — value 5 — effort M — risk low — category: proof honesty
  Why: assumption: a green proof against a stub, fixture, mock or localhost looks the same as one against the real thing. The request wants unprovable things labelled, and "proved against a stand-in" is a middle state.
  Done when: `fm task prove` records one of real / fixture / stubbed / unknown per criterion, and a test with an HTTP mock server shows "stubbed" in the finish receipt.

- **Reject vacuous evidence in non-test proofs** — FIX — value 5 — effort M — risk low — category: verification
  Why: T-2606 handled "runs matched no test", but the same hole exists for `fm shot` (blank or error page), data checks (0 rows) and doc greps (0 files). Each of these passes trivially.
  Done when: a fixture where a shot renders an empty body, a query returns 0 rows and a grep scans 0 files gives three "unproven: vacuous" verdicts rather than passes.

- **Make `fm shot` deterministic before it compares** — FEATURE — value 4 — effort M — risk med — category: UI proof
  Why: assumption: baseline diffs of web UIs flake on clocks, animations, fonts and caret blink. Rendering twice and diffing exposes that noise.
  Done when: `fm shot` renders twice, masks the regions that differ between the two renders, and a page with a ticking clock compares equal to itself while a real layout change still fails.

- **Prove performance with interleaved A/B/A/B runs** — FEATURE — value 4 — effort M — risk low — category: performance proof
  Why: the request lists performance. Sequential before/after runs confound machine drift, and the T-2605 bench work showed noise decides outcomes here.
  Done when: `fm perf prove` alternates base and change N times, reports the median delta with an interval, and returns "inconclusive" when the interval spans zero. A test injects drift and still gets a correct verdict.

- **Re-probe eventually consistent claims after a settle delay** — FEATURE — value 4 — effort S — risk low — category: ops proof
  Why: assumption: infra and ops claims (DNS, caches, queue drains, deploys) pass at t0 and break at t+60s. A single probe over-claims.
  Done when: a criterion can declare `settle: 30s`, the proof runs at t0 and t+30s, and a flipped result is recorded as "unstable", never "proved".

- **Probe ops changes from a different vantage than the one that made them** — FEATURE — value 4 — effort M — risk med — category: ops proof
  Why: assumption: the agent checks a service from the same shell and env that configured it, so a local-only success counts as proof. An outside-path probe (fresh env, public address, second process) removes that shared bias.
  Done when: an ops criterion's verify runs with a scrubbed env and a separate working directory, and a fixture where the fix works only through the agent's own env var fails.

- **Fail a proof that leaves residue** — FIX — value 3 — effort S — risk low — category: reliability
  Why: assumption: verify commands that start servers or browsers leave processes, ports and temp files. A later proof then passes against a stale server from an earlier run.
  Done when: after each verify the runner diffs listening ports, child processes and the dirty tree, and a command that leaks a server is flagged with the leaked pid and port.

- **Resolve every flag, env var and path in docs to code symbols** — FEATURE — value 4 — effort M — risk low — category: docs vs code
  Why: "docs against code" is in the request. The ideas so far smoke-run the docs' commands, which does not catch a documented flag that is silently ignored (the "accepted-but-ignored flag" class).
  Done when: `fm docs verify` extracts backticked flags, env vars and paths from README and MASTER, and reports each as resolved, missing or ignored. A planted dead flag shows up.

- **Require absence claims to declare their scan scope** — FEATURE — value 3 — effort S — risk low — category: proof honesty
  Why: assumption: "no other callers", "nothing leaks", "no TODOs left" are common done-claims. They are only as good as the paths and languages scanned.
  Done when: a criterion phrased as absence must carry a scope, the receipt prints "none found in N files of kinds X", and an unscoped one is labelled unproven.

- **Keep a ranked unproven register with cost-to-prove** — FEATURE — value 4 — effort M — risk low — category: observability
  Why: the request says whatever can't be proven gets labelled. Labels scattered across receipts never become a queue. Each entry would carry the cheapest proof kind that could close it and the blast radius it sits on.
  Done when: `fm unproven` lists every open unproven label across tasks with age and a suggested proof kind, and closing one removes it.

- **Show an observed-behaviour sheet for "does it do what I meant"** — FEATURE — value 4 — effort M — risk med — category: intent
  Why: the request names "does it do what the user meant", which tests can't prove. Three or four real input→output pairs run by the agent, which the user can glance at, are cheaper to judge than a diff.
  Done when: finishing a FEATURE prints up to 4 really executed examples taken from the criteria's own commands, and the sheet is marked "user-judged, unproven" until the user acknowledges it.

- **Run the verify step in a write-discarding overlay** (wild) — FEATURE — value 3 — effort L — risk high — category: isolation
  Why: assumption: a verify command that creates the file or row it then checks "heals" the thing under test. An overlay with a reported write diff would expose that.
  Done when: a fixture verify that writes the artifact it asserts on returns "proof mutated its subject", with the written paths listed.

- **Drill each proof kind with a planted fault weekly** (wild) — FEATURE — value 4 — effort M — risk low — category: verifier recall
  Why: wild: the repo proves its own work, but nothing measures whether the shot, flow, data and docs verifiers actually catch bugs of their own kind. Recall per kind would be the first honest reliability number for the verifiers.
  Done when: a scratch copy gets one known fault per kind, and `fm doctor` shows caught/missed per kind, with a miss as WARN.

- **Re-verify a sample of closed proofs by a second method** (wild) — FEATURE — value 3 — effort M — risk med — category: verifier agreement
  Why: wild: a rotating re-prove exists, but it repeats the same method. Checking a UI claim by DOM query and again by screenshot diff, or a data claim by SQL and by an export checksum, turns disagreement into a reliability measure of the method itself.
  Done when: the nightly job re-proves 3 closed criteria with an alternate method and records agree/disagree. A disagreement files a task naming the weaker method.

Next question: Which proof kinds does the user trust enough to skip reading, and what past false-done made them stop?
Next question: For ops and data proofs, which systems can Foreman actually reach read-only from this machine, and where would "unproven" be the only honest label?
