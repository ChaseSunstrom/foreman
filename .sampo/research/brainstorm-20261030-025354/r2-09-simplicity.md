# Brainstorm — lens: simplicity

- **Make one `fm find` verb that does one thing: hunt, prove, report** — FEATURE — value 5 — effort M — risk med — category: initiative core
  Why: Initiative is spread over scout, adopt, deps, docs, inbox gh, night; the exam shows the deterministic finders found 0 of 108 planted defects. One verb with one output (a list of proven findings, or "nothing proven") is the smallest surface that can be graded on the exam's `none` and `bug` kinds.
  Done when: `fm find` on a never-seen exam repo prints either findings that each carry a red test, or the literal line `nothing proven`, and `fm help` lists adopt/scout/deps/docs as aliases of it.

- **Let the finding be a failing test file and nothing else** — FEATURE — value 5 — effort S — risk low — category: proof
  Why: Mission asks to "prove each finding with a failing test". A finding with no schema beyond `test path + one-sentence claim` removes the ledger, kinds table and per-finder formats. assumption: the stack has a runnable test command (else see "cannot prove" below).
  Done when: a finding is stored as one test file plus a one-line claim; deleting the file deletes the finding; `fm find check` fails on any finding whose test is green on the untouched tree.

- **Replace the deterministic finders with one read-only model pass per hot file** — FEATURE — value 5 — effort M — risk med — category: finder
  Why: fmdocs.scan + fmsecrets found 0/108; plain Claude finds 3/3 at about 0.17 USD each. One bug-shaped question per file from `fm map`'s hot list, writing a repro, is far less machinery than six probe families. assumption: cost stays near the plain-Claude figure per file.
  Done when: on the held-out exam repos the pass reaches at least the plain-Claude arm's bug recall, at a per-finding cost shown on the receipt.

- **Treat "none" as a result with a one-line receipt** — FEATURE — value 4 — effort S — risk low — category: false positives
  Why: the mission is graded on the exam's `none` kind; every finder that must emit something will file noise. The simplest cure is permission to say `nothing proven (N files read, N claims refuted)`.
  Done when: on the exam's `none` repos `fm find` exits 0 with zero findings and the receipt line; a test pins that it never invents a finding to fill the list.

- **Rank with one number from facts `fm map` already has** — FEATURE — value 3 — effort S — risk low — category: ranking
  Why: the mission wants value ranking, but weights tuned without data are theatre. Use `importers of the file × changes in the last 90 days`, sort descending, show the two numbers beside each finding.
  Done when: the list is ordered by that product, and a test with two findings in files of different fan-in shows the order and both numbers.

- **Hand the fix to a plain lane whose whole prompt is the red test** — FEATURE — value 4 — effort S — risk low — category: fix lane
  Why: the pipeline asked for is "fixes it in a lane". Reusing `fm run` with the test path as the task text adds no new pipeline stage.
  Done when: `fm find --fix N` creates one task whose body is the claim plus the test path, and it closes only when that test is green and the prior suite is still green.

- **Stop the setup probe filing Foreman faults in user projects** — FIX — value 4 — effort S — risk low — category: noise
  Why: the pack's "Noticed" line says probe_doctor may queue Foreman setup failures as tasks in user projects. Deleting that path is simpler than filtering it.
  Done when: a project with a broken Foreman install gets zero queued tasks from scout/find, and a test asserts it.

- **Cap a run at three proven findings** — FEATURE — value 3 — effort S — risk low — category: budget
  Why: attention is the scarce resource and an unbounded night run creates a pile nobody reads. assumption: three is a sane default; make it the one setting.
  Done when: `fm find` stops at three proven findings and prints how many candidates it left unexamined.

- **Remember dismissals in a plain text file** — FEATURE — value 3 — effort S — risk low — category: dedupe
  Why: re-filing a declined finding is the fastest way to lose trust. One line per fingerprint (test name + file hash) in a text file, no database.
  Done when: dropping a finding and rerunning `fm find` on the unchanged file does not show it again; changing the file does.

- **Say "cannot prove here" instead of guessing on stacks with no runnable tests** — FEATURE — value 3 — effort S — risk low — category: honesty
  Why: the exam spans python, js, ts, ruby, rust and c; some will have no test command. Reporting an unproven hypothesis as a finding breaks the proof rule.
  Done when: a repo with no runnable test command yields `cannot prove here: no test command`, not a finding.

- **Wild: try deleting code before adding any** — FEATURE — value 3 — effort M — risk med — category: simplicity
  Why: wild. A finder that removes a dead function or branch and keeps the change only if the suite stays green turns "less code" into proven work, with the passing suite as the proof.
  Done when: on a planted repo with one unused function, `fm find --delete` proposes its removal with the green suite as evidence.

- **Wild: reject any finding that doesn't fit in one sentence** — FEATURE — value 3 — effort S — risk low — category: clarity
  Why: wild. A claim that needs a paragraph is usually a vague worry. A hard one-sentence limit filters hunches with no model call.
  Done when: a finding whose claim exceeds one sentence is refused at filing with the reason shown.

- **Wild: use mutation as the finder** — FEATURE — value 3 — effort L — risk med — category: finder
  Why: wild. Flip one operator in a hot function; if the suite stays green, the missing test is the finding and the failing test to write is obvious. It needs no model to detect, and it is deterministic.
  Done when: on a repo with a function whose tests never check its output, the mutation pass reports it with the surviving mutant as the repro.

Next question: What does a plain Claude session cost per proven finding on the `none` repos, and is Foreman's extra ceremony ever worth that gap?
Next question: Which exam kinds can be proven by a failing test at all, and which need a different kind of reproduction?
