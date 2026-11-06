# Brainstorm — lens: tower archaeology

- **Write a RESUME.md the tower regenerates on every put** — FEATURE — value 5 — effort M — risk low — category: resume
  Why: assumption: a fresh session today must reconstruct the next step from gen-1/*, lineage.md and not-yet.md. Chat context holds it, and the pack shows tower files live only in genesis storage.
  Done when: a session given only RESUME.md names the in-flight generation, the next step, open blockers and the last decision, matching a hand-written key.

- **Record a structured verdict for every rewrite that loses** — FEATURE — value 5 — effort M — risk low — category: lineage
  Why: the selection rule keeps a rewrite only if it closes more exam scenarios than its parent. The pack shows no stored reason for a loss, so a later session may retry the same rewrite.
  Done when: each loser in lineage.md has parent and child scenario counts, the scenarios that flipped either way, cost ratio, and a one-line cause, and `fm genesis status` prints them.

- **Score a cold-resume exam with a tool-less reader** — FEATURE — value 5 — effort M — risk med — category: exam
  Why: fm exam already has tool-less authors, hidden keys and a held-out third. Reuse them: a child reads only the tower files and answers resume questions such as "what is the next step?", "why did gen-2's Seed lose?" and "which MUST is at risk?".
  Done when: `fm exam run --kind resume` scores a three-generation fixture tower, and deleting the "why lost" text from the fixture lowers the score.

- **Add `fm genesis resume` with an integrity check** — FEATURE — value 4 — effort M — risk low — category: verb
  Why: gen-0 must stay verbatim and read-only, and the held-out third must stay unseen. Resuming should verify both before acting.
  Done when: the verb prints the briefing, fails with a clear message if the gen-0 hash changed, a not-yet entry lacks a blocker, or a status says "running" with no live process, and passes on a clean fixture.

- **Give every not-yet entry attempts, blocker and a retry trigger** — FEATURE — value 4 — effort S — risk low — category: ledger
  Why: the steer says a failed spike gets at least 2 different approaches, then goes to the ledger and is retried each generation. A resumer must see what was tried so it doesn't repeat it.
  Done when: the ledger rejects an entry with fewer than 2 recorded approaches, and each entry shows the last-retried generation and next trigger.

- **Journal intent before each tower step so crashes resume cleanly** — FEATURE — value 4 — effort M — risk med — category: reliability
  Why: assumption: Seed → Missions → critique → selection → drift → sweep is multi-step and long-running. A crash or usage cap mid-step leaves a half-written generation.
  Done when: killing the orchestrator mid-critique and re-running `fm genesis resume` finishes the generation without duplicate or missing files.

- **Snapshot the user's steers and NEVERs verbatim into the tower** — FEATURE — value 4 — effort S — risk low — category: provenance
  Why: the pack's steers ("not hardcoded", "weakness-finding by outside signals only", "no idea killed for ambition") are standing rules that exist only in chat history. A new session would not know them.
  Done when: steers.md holds each dated steer verbatim, the Seed template cites it, and the drift check flags a mission that contradicts one.

- **Add `fm genesis diff gen-a gen-b`** — FEATURE — value 3 — effort M — risk low — category: lineage
  Why: assumption: with three generations, a resumer wants what changed in Seed, missions and exam flips, not three full documents.
  Done when: the diff lists changed Seed lines, added or dropped missions, and scenarios that flipped pass/fail, on a fixture tower.

- **Lint the tower for staleness and holdout leakage** — SECURITY — value 4 — effort M — risk low — category: integrity
  Why: the inversion risk is overfitting the held-out third. Holdout scenario text appearing in a generation doc, or exam results older than the spec, makes the archive misleading.
  Done when: the lint fails on a fixture where a holdout scenario id or phrase appears in a Seed or critique, and on exam results older than the current spec.

- **Show a "you are here" marker and next step on the site tower page** — FEATURE — value 3 — effort S — risk low — category: site
  Why: the user asked for every doc readable in full and per-generation detail on the page. A resume pointer would complete that, and the page is already live.
  Done when: the exported page highlights the current generation, shows the next step from RESUME.md, and has a screenshot test.

- **Tag each tower claim with the commit it was verified against (wild)** — FEATURE — value 3 — effort L — risk med — category: staleness
  Why: wild. The user wanted Foreman to be "genuinely smarter", and fmmap.drift learns from git co-change. Tower claims such as "the coverage grid has no empty cells" could carry a commit hash and be flagged when the files they rest on change.
  Done when: editing a file a claim cites marks that claim stale in `fm genesis status`.

- **Time-travel a scenario across generations to find who broke it (wild)** — FEATURE — value 3 — effort L — risk med — category: bisect
  Why: wild. With a Seed, missions and exam per generation, `fm genesis bisect SCENARIO` could replay the exam against each generation's recorded state and name the generation where it flipped.
  Done when: on a fixture with a planted regression, bisect names the correct generation.

- **Have a child write an oral history of each dead end (wild)** — FEATURE — value 2 — effort M — risk low — category: narrative
  Why: wild. A tool-less child reads a generation's files and writes a short post-mortem (what we believed, what the exam showed, what we'd try next) into gen-n/story.md. Prose carries intent that bare tables lose.
  Done when: every generation closes with a story.md, and the cold-resume exam scores higher with it than without.

- **Seed cold starts from a nearest-ancestor tower in a cross-project library (wild)** — FEATURE — value 3 — effort L — risk high — category: carry-over
  Why: wild. Gen-0 §3 says winning Seeds, lenses and lineage carry over as defaults. A library of finished towers, matched by project kind, would give a stranger repo a proven starting point, and the cold-resume exam could prove it helps.
  Done when: on a held-out generated project, a Seed borrowed from the nearest tower covers more MUSTs than a Seed written from scratch. Nothing leaves the machine.

Next question: What is the smallest set of tower files that lets a stranger session resume correctly, and how do we measure that with the cold-resume exam instead of guessing?
Next question: When two sessions open the same tower at once (loop auto-start and a user), which one owns the next step, and where does the tower record that?
