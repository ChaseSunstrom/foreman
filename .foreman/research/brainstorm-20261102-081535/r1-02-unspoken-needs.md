# Brainstorm — lens: unspoken needs

- **Route every claim to its cheapest sufficient prover** — FEATURE — value 5 — effort M — risk med — category: verification
  Why: The ask spans UI, data, docs, ops, performance and intent, and today each lives in a different verb (`fm shot`, `fm flow`, `fm task prove`, the sweep). The need behind it is "I shouldn't have to know which tool proves this." `fm verify "<claim>"` would classify the claim, pick the prover, run it, and say "no prover exists" when none does.
  Done when: five claims (a UI state, a doc default, a row count, a p95 and a plain-English intent) each reach a different prover and print a grade. A sixth claim with no prover prints `unproven: <reason>`.

- **Turn "unproven" into a ranked proof-debt list with conversion costs** — FEATURE — value 5 — effort M — risk low — category: honesty
  Why: The request says what can't be proven gets labelled unproven. A bare label is only a to-do. Each one should carry a reason class (needs a human eye, needs another OS, needs time, needs data, needs a credential), the cheapest action that would prove it, and who has to take that action.
  Done when: `fm unproven` lists every unproven label from open tasks with reason class, converter and owner, sorted by what each unblocks. A fixture task with two labels shows both.

- **Make proofs expire when the thing proved changes** — FEATURE — value 4 — effort M — risk med — category: freshness
  Why: A screenshot, a data profile or a doc check proves something about a tree that moves on. Assumption: proofs are stored with no input hash today. Each proof would record the hash of the files, data and config it covers, and go stale on change.
  Done when: editing a file a UI proof covers flips that proof to `stale` in `fm doctor`. Editing an unrelated file does not.

- **Add a no-model lint pass to `fm shot`** — FEATURE — value 4 — effort M — risk low — category: ui
  Why: T-1217 (the pane painted the wrong grey) was caught by eye. The checks would run on the page and the DOM: clipped or overflowing text, contrast below AA, console errors, 4xx requests, empty or loading states left on screen, and no keyboard path to an element.
  Done when: a fixture page with one clipped label and one low-contrast button fails `fm shot --lint` naming both. The clean page passes.

- **Profile data and diff it after every change** — FEATURE — value 4 — effort M — risk low — category: data
  Why: The request names "data" with no existing proof beyond tests. A fingerprint of a table or file (row count, null rate, uniques, ranges, key overlap) is stored, then diffed after the change. A source-to-sink count reconciliation is part of it.
  Done when: dropping 3% of rows in a fixture migration makes `fm data diff` report the row-count and null-rate shift. An identical rerun reports "no drift".

- **Check doc defaults and constants against the code** — FEATURE — value 4 — effort M — risk med — category: docs
  Why: "Docs against code" usually fails on a number: a timeout, a default flag value or a limit. Extract "default X", "N seconds" and "up to N" claims from docs and find the matching constant in code. Ambiguous matches are reported as unmatched, never guessed.
  Done when: a fixture doc says "timeout 30s" while the code says 60, and the check reports the pair with both file:line locations.

- **Pin a performance slowdown to a function** — FEATURE — value 3 — effort M — risk low — category: performance
  Why: A bench gate that says "slower" sends the user hunting. Assumption: today it reports a median and a threshold only. Keep a cheap profile per bench run and diff the top frames when the gate trips.
  Done when: a planted slow loop in a fixture makes the tripped gate name that function as the top delta.

- **Check declared ops config against the live host** — FEATURE — value 3 — effort M — risk med — category: ops
  Why: The ops proofs in the pack (timer liveness, install rehearsal) cover Foreman itself. A project's own units, ports, file modes and env vars need the same kind of read-only probe: does what the deploy files declare match what runs, and does it answer?
  Done when: a fixture unit that declares port 8080 while the live listener is on 8081 shows up as a mismatch in a read-only report that changes nothing.

- **Scrub screenshots and flow captures before they are stored** — SECURITY — value 4 — effort S — risk low — category: privacy
  Why: `fm shot` and `fm flow` write images and DOM dumps that can hold emails, tokens and home paths, and evidence files can reach the site or a bug report. Assumption: image and DOM text are not scrubbed today. Blur pattern matches in the DOM text before the shot is taken.
  Done when: a fixture page showing a fake token and the user's email produces a stored shot with both masked, and the stored DOM dump has them replaced.

- **Show a behaviour sheet for "did it do what I meant"** — FEATURE — value 5 — effort M — risk med — category: intent
  Why: The final request-to-product gap is where users end up correcting Foreman. At finish, run the built thing on five realistic inputs drawn from the user's own words. Show the real input→output pairs and let the user mark the wrong ones with one key. Marked rows become tests.
  Done when: a fixture task finishes with a five-row sheet, and marking row 3 wrong creates a failing test named for it.

- **Wild: Show an ink-fade claims board** — FEATURE — value 3 — effort M — risk low — category: ui
  Why: assumption: a page of every public claim is more honest if its ink visibly fades as its evidence ages or its covered files change, and one click re-proves it. This is wild.
  Done when: a claim whose proof is 20 commits stale renders visibly lighter than a fresh one, and the re-prove button restores it.

- **Wild: Probe the boundaries of the user's wording** — FEATURE — value 4 — effort M — risk med — category: intent
  Why: Misreadings cluster at the edges of a request ("older than a week" — is 7 days in or out?). A tool-less child lists the boundary inputs the sentence leaves open. Foreman runs the build on them and shows only the places where the behaviour is a choice, for the user to settle. This is wild.
  Done when: for "delete files older than a week", the report shows the 7-day-old file's actual fate and asks in or out.

- **Wild: Queue human-eye proofs for a phone** — FEATURE — value 4 — effort M — risk med — category: devices
  Why: Many unproven items are "needs a human to look". Batch them as image-plus-question cards, one tap each, readable on a phone through the local web UI, so five minutes away from the desk converts them to proven or failed. This is wild.
  Done when: three queued cards answered on the phone move three items from unproven to proven or failed in `fm unproven`.

- **Wild: Replay the project's own real logs through old and new builds** — FEATURE — value 3 — effort L — risk med — category: ops
  Why: The best proof that nothing broke is last week's real traffic or job inputs. Assumption: the project keeps logs or fixtures that can be replayed offline. Run them through the old and new builds with the network off, and diff the outputs. This is wild.
  Done when: a fixture log replay shows zero diffs on an identical build and names the differing line when one function changes.

Next question: Which of the user's last 20 "is it really done?" doubts were about intent, and which about environment, and does the split show where proof effort should go?
Next question: What does the user do with an "unproven" label after reading it — ignore it, ask Foreman to prove it, or prove it by hand — and what records that?
