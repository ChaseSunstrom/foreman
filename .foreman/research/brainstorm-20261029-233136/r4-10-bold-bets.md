# Brainstorm — lens: bold bets

- **Make Genesis grade itself against a frozen Foreman snapshot** — FEATURE — value 5 — effort L — risk med — category: self-hosting proof
  Why: the exam asks that the self-written gen-0 covers every MUST, NEVER and section of the hand-written one. Foreman is the only project with both a hand-written gen-0 and a full history. Assumption: a snapshot of the repo before gen-0 existed can be rebuilt from git.
  Done when: `fm genesis selftest` runs the writer on the pre-gen-0 snapshot given "make this great", and a report lists each hand-written MUST/NEVER/section as covered or missing, with the count.

- **Ship `fm genesis dream`, an idle-time speculative tower on a scratch clone** — FEATURE — value 5 — effort L — risk med — category: autonomy
  Why: the request says the tower starts on its own when the queue runs dry, but the repo is the user's live tree. Assumption: `fm lane` can already provide an isolated worktree.
  Done when: with the queue empty, a tower runs in a worktree, touches nothing in the main tree, and leaves a one-screen digest plus a ready-to-ship branch the user accepts or discards in one command.

- **Run a tournament of N gen-1 candidates from different Seeds** — FEATURE — value 4 — effort L — risk med — category: selection
  Why: selection currently compares a rewrite to its parent, so one lineage can only climb a local hill. `fm lane` race and `fm exam` already exist. Assumption: the budget envelope covers N.
  Done when: N Seeds produce N candidate gen-1s, all are graded on the same exam, the winner is recorded in lineage.md with each loser's score, and the tower continues from the winner only.

- **Mint exam scenarios from the project's own fix and revert commits** — FEATURE — value 5 — effort M — risk low — category: exam realism
  Why: the exam's planted gaps are authored by tool-less children, which can share the writer's blind spots. Real bugs the project already had are an outside signal, and "weakness-finding by outside signals only" is a standing steer.
  Done when: on a fixture repo with 5 fix commits, `fm exam gen --from-history` produces scenarios that fail on the parent-of-fix tree and pass on the fix, each verified by running both.

- **Compete against plain Claude on every selection, not just in the exam** — FEATURE — value 4 — effort M — risk low — category: outside signal
  Why: the steer says the head-to-head with plain Claude is how weakness is found. A generation that cannot beat the plain arm on its own held-out scenarios has proven nothing.
  Done when: each generation's close writes foreman-versus-plain closed counts and cost, and a generation where plain Claude closes at least as many is flagged "no lift" in status.

- **Generate the project's capability spec from its best-in-class peers** — FEATURE — value 4 — effort M — risk med — category: spec
  Why: the request is "complete and best-in-class for this kind of project", and the capability-map lens exists. A spec written only from the repo inherits the repo's own gaps. Assumption: a tool-less child can name peers from its own knowledge, with web access optional.
  Done when: for a fixture project, the spec lists at least 15 capabilities, each tagged with the peer that has it and with present, partial or absent in this repo, and the coverage grid is built from that list.

- **Hold a monthly 30-day survival check on Genesis output** — FEATURE — value 4 — effort M — risk low — category: outside signal
  Why: `fm outcomes` 30-day survival is a named outside signal. A Genesis win only counts if the user didn't revert it. Assumption: outcomes can be keyed by task id.
  Done when: tasks that Genesis created are tagged, `fm genesis status` shows survived, reverted and pending counts, and a reverted one automatically becomes an exam scenario.

- **Build a user-model proxy that answers Genesis's low-stakes questions** — FEATURE — value 4 — effort L — risk high — category: autonomy (wild)
  Why: the user's steers show they dislike being asked and dislike hardcoding. Assumption: steers, drops and asks are enough to predict a yes or no on routine choices.
  Done when: on a replay of 20 past user decisions, the proxy matches at least 80% and abstains on the rest, and each proxy answer is logged and revocable.

- **Let the tower seal a 30-day prediction and grade it** — FEATURE — value 3 — effort M — risk low — category: calibration (wild)
  Why: assumption: the tower's claims about what the project needs are unfalsified until time passes. A prediction such as "these three surfaces will be asked about next" scored against real asks turns that into a measured number.
  Done when: gen-0 writes a dated, hash-sealed prediction file, and after 30 days `fm genesis status` scores it against the asks that actually arrived.

- **Fork a tower and run the risky rule on a cloned project first** — FEATURE — value 4 — effort L — risk med — category: safe self-change
  Why: self-modification must be measured and reversible. A rule change that wins only on its own project is overfit. Assumption: fixture projects can serve as clones.
  Done when: a proposed template or lens change runs on the clone, is promoted only if it also holds on a second fixture, and the verdict is in lineage.

- **Turn "make this great" into a ranked menu of three outcomes** — FEATURE — value 4 — effort S — risk low — category: user value
  Why: a sweeping request can start an expensive tower. The user's own style is short, decisive asks. Assumption: three outcomes can be priced in advance.
  Done when: `fm genesis` with a vague line prints three outcomes with cost and time estimates and starts nothing until one is picked.

- **Replay the tower as a time-lapse on the site page** — FEATURE — value 3 — effort M — risk low — category: tower page (wild)
  Why: the user steered toward in-depth per-generation views of the tower page. Scrubbing generations makes lineage, dead rewrites and coverage-grid fill visible.
  Done when: the page has a play control that steps through each generation's grid and lineage, respects reduced motion, and works with keyboard alone.

- **Run Genesis on a folder that isn't code** — FEATURE — value 3 — effort L — risk med — category: generality (wild)
  Why: the request says "any project". The exam generator knows six languages only, and a docs or data folder has no gates to run. Assumption: a black-box exam of questions and checks over files can stand in.
  Done when: on a fixture folder of notes, Genesis writes a gen-0 and a spec, marks the code-only grid cells "not applicable", and still produces a graded held-out exam.

- **Publish a head-to-head receipt per project with a signed hash** — FEATURE — value 3 — effort M — risk low — category: trust
  Why: the tower claims to close planted gaps, but nothing outside Foreman can check it. Assumption: the exam, keys and results can be hashed together after the run.
  Done when: `fm genesis receipt` writes a file with exam hash, arm scores, cost and commit, and a second command re-verifies the hash and re-runs the oracle arm.

Next question: Which of the user's standing grants (publish to main, ship) would Genesis's auto-start inherit by accident, and is there a test that proves it inherits none?
Next question: When two towers exist for related projects, which learned defaults should cross over, and what measured result earns that transfer?
