# Brainstorm — lens: inversion: how verification fails: green unit tests on the wrong behaviour, docs that lie about the code, a UI never looked at, infra changed blind, perf claimed unmeasured, research uncited, an unproven claim reported as done

- **Mutate the claim, not the code** — FEATURE — value 5 — effort M — risk med — category: proof
  Why: unit tests go green on wrong behaviour; the pack's `fm task prove` shows a test fails without the change, but nothing checks that the test fails when the *behaviour* is subtly wrong. Assumption: a mutation pass is not yet a proof kind.
  Done when: `fm prove --mutate TASK` applies N small mutations to the task's diff and records how many the task's verify commands caught; a task with 0 caught is labelled "tests don't constrain this change" in the unproven rollup.

- **Docs-vs-code claim extractor** — FEATURE — value 5 — effort M — risk low — category: docs proof
  Why: Mission 7 lists "docs against code"; the README makes numeric and flag claims ("6,400-char budget", "fm lane max 6"). Assumption: no verb extracts and re-checks them.
  Done when: `fm prove --docs README.md` lists every backticked command, flag, path and number in the doc, marks each found / missing / mismatched against code, and a seeded false claim in a fixture is reported.

- **Perf claim needs a recorded measurement or a label** — FIX — value 4 — effort S — risk low — category: perf proof
  Why: T-2284/T-2303 measure perf when asked, but a finish note saying "faster" without `--bench` still closes. Assumption: close doesn't scan prose for perf words.
  Done when: closing a task whose summary matches faster/slower/reduces latency/overhead with no Measurements section lands it in the unproven rollup as "perf claimed, unmeasured".

- **Screenshot must be looked at, by something else** — FEATURE — value 4 — effort M — risk med — category: UI proof
  Why: the unproven rollup counts UI changes with no visual check, but an `fm shot` that is taken and never inspected still counts as checked. Assumption: the shot file's existence satisfies the check.
  Done when: a UI-task shot only counts once a different-model child has described it against the criterion and the description is stored beside the image; a blank or identical-to-before screenshot is rejected.

- **Citation gate for research tasks** — FEATURE — value 4 — effort M — risk low — category: research proof
  Why: Mission 7 item 10 says research is held to the same standard; RESEARCH tasks (T-0336, T-1331) have no proof kind. Assumption: close accepts prose.
  Done when: a RESEARCH task can't close unless each claim line has a URL, file:line or command output that `fm prove --cite` fetches or opens and finds the quoted text in; failures are listed.

- **Infra dry-run diff as evidence** — FEATURE — value 4 — effort M — risk med — category: infra proof
  Why: seed row names infra; data has `--migration` but config, CI, systemd and Dockerfile edits close on a claim. Assumption: no `--infra` kind.
  Done when: `fm prove --infra` runs the available native dry-run (terraform plan, `docker build --check`, `systemd-analyze verify`, actionlint, `nginx -t`) on the changed files, stores the output, and records "no checker available" as unproven rather than pass.

- **Verdict disagreement ledger** — FEATURE — value 4 — effort M — risk low — category: reliability
  Why: left question "which verbs have a model on both sides with no user-owned check". Assumption: judge verdicts aren't compared with outcomes.
  Done when: every cold-read, second-read and done-gate verdict is stored with later outcome (reverted, re-fixed, reopened), and `fm doctor` prints each judge's false-pass rate.

- **Proof receipt with a "what this does not prove" line** — FEATURE — value 4 — effort S — risk low — category: delight/honesty
  Why: user wants unprovable things labelled; the rollup lists tasks but a close receipt doesn't say what stayed unchecked. Assumption: receipts list passes only.
  Done when: each `fm task finish` output ends with "Not proven: …" naming every criterion on typed evidence, and the line appears in the site and pane renderings.

- **Intent-match check: restate the diff back to the ask** — FEATURE — value 5 — effort M — risk med — category: meaning
  Why: "does it do what the user meant" is in the request; the pack shows repeated asks fixing misreadings (T-2285 plan gate miss). Assumption: a blind child reading only the diff isn't asked what request it answers.
  Done when: at close a tool-less child sees only the diff and states the request in one sentence; a cheap similarity score against the user's words below threshold marks the task "may not be what was meant".

- **Stale proof expiry** — FEATURE — value 3 — effort S — risk low — category: proof freshness
  Why: evidence recorded at close can rot after later commits. Assumption: evidence has no tree hash.
  Done when: evidence stores the hash of files it covered, and the rollup flags done tasks whose covered files changed since with no re-run.

- **Wild: Saboteur lane** — FEATURE — value 4 — effort L — risk med — category: adversarial proof
  Why: wild; a builder lane that tries to break a finished task (revert the fix piecemeal, feed bad input) and reports what the tests missed.
  Done when: `fm lane sabotage T-NNNN` produces a worktree where at least one behaviour-breaking change passes the task's tests, or reports none found after N tries.

- **Wild: Claim-to-check compiler for the README** — FEATURE — value 3 — effort L — risk med — category: docs proof
  Why: wild; each claim in the docs (including site stats) carries an executable check generated once and run in `fm doctor`, so the website can't drift (the user had to ask "is the site updated").
  Done when: changing a counted number in code without updating the site makes `fm doctor` fail naming the page and line.

- **Wild: Proof heatmap on the site** — FEATURE — value 3 — effort M — risk low — category: transparency
  Why: wild; a public grid of capabilities by proof kind (ran, measured, looked at, cited, typed, none) built from real evidence.
  Done when: the Genesis page renders the grid from `site/genesis` data, and a typed-only cell shows visibly different from a ran one.

- **Wild: Unprovable-claims court** — FEATURE — value 3 — effort M — risk low — category: honesty
  Why: wild; a nightly job samples closed tasks, asks a cold model to name the strongest unchecked claim in each close note, and files the top few as questions.
  Done when: running it on a seeded fixture of 5 closed tasks surfaces the planted unsupported claim.

Next question: Which proof kinds can be satisfied by a command whose output the builder wrote itself (a stub verify that always exits 0), and does anything detect a verify command that cannot fail?
Next question: When evidence is "inconclusive", what does the user see at 2 a.m. in the terminal, and is that different from "failed"?
