# Brainstorm — lens: bold bets

- **Earn write access one directory at a time** — FEATURE — value 5 — effort L — risk med — category: trust
  Why: assumption: a revert or a failed gate in git history can be read as a negative signal. Foreman starts each directory read-only, promotes it after a set number of proven closes, and demotes it on a revert, so "just go" stays safe in new code.
  Done when: a directory with no closes stays read-only, the Nth verified close promotes it, and a later revert demotes it before the next run starts.

- **Teach the user to predict the failing test** — FEATURE — value 3 — effort S — risk low — category: learning
  Why: the user repeatedly steers the same kinds of fixes ("step 1 is the profile", "dropped the RETRY_WATCHDOG step"). Before a proof runs, Foreman asks for one guess at which test fails and scores the guess over time. Assumption: the user wants to learn the codebase, not only get results.
  Done when: each proof shows a prompt with a guess box, the guess is stored beside the result, and `fm` reports a running hit rate.

- **Obituary for every deleted feature** (wild) — FEATURE — value 2 — effort S — risk low — category: delight
  Why: the backlog has 60+ "Wild" and deferred items, and each dropped or deferred one vanishes silently. A short obituary (what it was, what it cost to wait, why it ended) gives each removal a record and a moment. Wild: the tone is playful, not a funeral.
  Done when: removing a backlog item writes one dated line with its cost in tokens and reason, and `fm` prints the last three.

- **Let the repo post its own job ad** (wild) — FEATURE — value 2 — effort M — risk low — category: delight
  Why: the open-work list and the red gates already say what the codebase needs. Foreman turns the top three into a short public "we're hiring" card the user can answer with one task. Wild: the repo "applies" for its own work and the user accepts or rejects the application.
  Done when: `fm hire` lists three open needs with their gate evidence, and accepting one creates a queued task with that evidence attached.

- **Run the whole queue in a browser tab** (wild) — FEATURE — value 3 — effort L — risk high — category: surfaces
  Why: the web UI already exists (`plugin/templates/web/index.html`), but it only shows state. Assumption: a browser sandbox can run a read-only fixture repo end to end. A fresh tab with no install would show a finished task, its proof and its receipt.
  Done when: a fresh tab with no install completes the fixture task, and the receipt matches the CLI's output byte for byte.

- **Make the pack a manifest that the model pulls from** — PERFORMANCE — value 4 — effort M — risk med — category: cost
  Why: the context pack is pushed whole to every child, and the ideas-so-far section alone runs to hundreds of lines. A small manifest with section IDs, fetched on demand, targets the 140k-per-reply goal. Second-order on "cite pack sections by ID": that item cites sections, this one stops sending them.
  Done when: `fm cost` shows the first reply's input tokens fall under 40k on the fixture pack with the same accepted ideas.

- **Encrypt the journal at rest with an OS-keychain key** — SECURITY — value 3 — effort M — risk low — category: privacy
  Why: journals and receipts hold the user's own requests and corrections (see "The user's own words"). Redaction covers secrets, not the plain requests themselves. Assumption: the OS keychain is available on Linux and macOS.
  Done when: a journal file opened with a plain `cat` shows no readable request text, and `fm journal` reads it with the key.

- **Let a fresh clone inherit Foreman's memory** — FEATURE — value 3 — effort M — risk med — category: onboarding
  Why: the first hour in a new clone starts cold, which the "Greet a new project" and "first verified fix" ideas both touch. Inheriting only the rules, playbook index and gate list (never the journal) gives a new checkout its learned setup without copying private history.
  Done when: cloning a repo with a committed `.foreman/inherit.toml` gives the clone the listed gates and playbooks, and `fm status` shows no journal entries.

- **Write a living "how this repo runs" page** — DOCS — value 3 — effort S — risk low — category: docs
  Why: docs are a thin area in this pack, and the gates, layout and entry points already sit in the map. A page regenerated after each close, listing the real gates, the most-used verbs and the last three proofs, stays true because it is built from the journal.
  Done when: `fm docs` writes `HOW_THIS_REPO_RUNS.md` where every gate name matches `fm doctor` output, and a test fails if one does not.

- **Pool the usage budget across a team's machines** — FEATURE — value 4 — effort L — risk high — category: cost at scale
  Why: each machine keeps its own counter, so a team on one plan can overrun the reset without any single machine seeing it. Assumption: a team shares one account and the reset clock is per account. Risk high because the counter becomes shared state.
  Done when: two machines on one account show one shared remaining budget, and the second one pauses at the cap set by the first.
