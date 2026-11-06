# Brainstorm — lens: moonshots nobody ships

- **Ablate the diff** — FEATURE — value 4 — effort S — risk low — category: proof
  Why: assumption: green gates don't show which hunks matter, and the planned mutation checks cover tests, not the diff itself. `fm task finish` reverts each hunk (`git apply -R`) in a scratch worktree and reruns the task's proofs. A hunk whose removal leaves every proof green is flagged "unneeded or untested" and shown with the ask "keep, cut or add a test?".
  Done when: a fixture task with one deliberately useless hunk is flagged at finish, and the other hunks (whose removal turns a proof red) are not.

- **Infer invariants from passing runs** — FEATURE — value 4 — effort M — risk med — category: verification
  Why: assumption: no harness infers rules from behaviour. Python-first, Daikon-style: trace the test run with `sys.monitoring` and record function-level facts (never None, always sorted, x < y, a return is one of N values). Store them per function under `.foreman/invariants/`. After an edit, rerun and print "this diff newly breaks 3 inferred invariants", even when every test is green.
  Done when: a fixture function that starts returning None after an edit is reported with the invariant it broke while the existing tests stay green.

- **Mark uncertainty as typed holes in code** — FEATURE — value 4 — effort M — risk low — category: planning — wild
  Why: the pack has "Park questions as assumptions" and the user's complaints about guessing, but no code-level mechanism. The builder writes `FM_HOLE(q="retry on 429?", default="yes")` instead of guessing. `fm holes` lists them across lanes and asks once in a batch, and close is refused while any hole is open. Answers rewrite the marker into code and a recorded decision.
  Done when: a task with an open hole can't close, and `fm holes answer` removes the marker and the close then passes.

- **Port with the old code as the oracle** — FEATURE — value 4 — effort L — risk med — category: migration
  Why: assumption: rewrites and language ports are where agents silently change behaviour, and "Fan out migrations" and "Pin behaviour" cover only same-language shards. `fm port old new` records real call arguments from the existing tests, builds a differential harness that runs both implementations on recorded plus fuzzed inputs, and treats any divergence as the failing test. The builder works until divergence is zero or each remaining one is explicitly accepted.
  Done when: a fixture Python function ported to a deliberately off-by-one version fails the harness with a minimal diverging input.

- **Delegate with attenuating capability chains** — SECURITY — value 4 — effort M — risk med — category: safe delegation
  Why: the pack has per-role read-only checks and allowlists, but no object that proves what a subagent may do. Each lane gets a signed capability file (paths, command classes, spend, expiry). The guard checks it on every call. A subagent can only mint children with narrower capabilities, macaroon-style, so a child can't exceed its parent.
  Done when: a child asking for a path outside its parent's capability is blocked, and the block names the narrowing step in the chain.

- **Inject a hostile-input pack by detected concept** — FEATURE — value 4 — effort S — risk low — category: tests
  Why: cards fire by library, but no catalogue keys off concepts. When a new test or fixture touches dates, money, paths, unicode, concurrency or parsing, the edit hook adds a short pack: DST gaps, leap seconds, `\u0000`, RTL marks, 0.1+0.2, symlinks, empty and huge inputs. The finish check asks "which of these did your test cover?".
  Done when: editing a test that parses a date triggers the dates pack once per session, and the receipt shows it fired.

- **Review behaviour changes, not lines** — FEATURE — value 4 — effort M — risk med — category: review
  Why: the user steers on how things look and behave, and reading diffs is the bottleneck. At finish, run old and new commits on generated and recorded inputs (CLI args, HTTP fixtures, function calls) and print observable differences as sentences ("`fm foo` now exits 2 on empty input"). Approve or reject each, and a rejection becomes a failing criterion.
  Done when: a fixture change that alters an exit code yields one behaviour line, and rejecting it reopens the task.

- **Clarify with five concrete examples, not questions** — FEATURE — value 3 — effort S — risk low — category: intake
  Why: the user hates both guessing and interrogation (asks are already deadline-defaulted). For a vague brief, produce five input→output or screen examples, with the user pressing y/n on each. Accepted examples become acceptance criteria and rejected ones become negative tests.
  Done when: a vague brief yields 5 examples, and the yes/no answers appear as criteria on the task.

- **Learn per-library competence and escalate on weak spots** — FEATURE — value 3 — effort S — risk low — category: learning
  Why: only 6 of 1,084 cards ever fired, and hot-file scoring is by file. Count rework (fix-after-edit, red-then-green) per imported library and per project. When a task touches a library with high rework, auto-fetch its card or docs before editing and mention the score in the brief.
  Done when: after seeded rework events on one library, the next task importing it shows the doc fetch and its score.

- **Seance: interview a finished session** — FEATURE — value 3 — effort M — risk low — category: memory — wild
  Why: "why is this line here?" is answered from the ledger, but the ledger loses the reasoning. `fm seance T-0412 "why not a queue here?"` replays that task's transcript digest, plan and diffs into a cheap fresh agent told to answer only from that evidence, and to say "not recorded" otherwise.
  Done when: asking about a closed fixture task quotes its plan step, and an unanswerable question returns "not recorded".

- **Inject faults into the user's project** — FEATURE — value 4 — effort M — risk med — category: robustness — wild
  Why: chaos is planned only for Foreman itself. `fm chaos` reruns the project's tests in a lane with an env shim that fails the network, disk-full, slow clocks and killed subprocesses (preload and monkeypatch shims, Python and Node first). Tests that crash unhandled become FIX tasks with the injected fault as the repro.
  Done when: a fixture app with an unguarded `requests.get` is reported as failing under "network down", with a one-line repro.

- **Rebase by intent, not by patch** — FEATURE — value 3 — effort M — risk med — category: lanes — wild
  Why: assumption: lanes die to textual conflicts when main moves. When a lane's base moves, run two candidates: a textual rebase, and a fresh lane that replays the lane's brief and plan on the new base. Keep whichever passes the task's proofs with the smaller diff, and tell the user which won.
  Done when: a fixture lane whose base renamed a function ends with the proofs green via one of the two candidates, and the receipt names it.
