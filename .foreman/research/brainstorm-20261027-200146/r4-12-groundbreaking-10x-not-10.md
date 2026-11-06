# Brainstorm — lens: groundbreaking: 10x, not 10%

- **Select tests by co-change history and fail-fast order** — PERFORMANCE — value 5 — effort M — risk low — category: test selection
  Why: `fm check --affected` and the full gate run every test in a fixed order, so a red often arrives after minutes of green. Git history already says which tests have broken alongside which files. Assumption: the project's history is deep enough to show co-change.
  Done when: on a fixture repo, a one-file change runs only the tests that co-failed with that file in the last 90 days, the first red appears before any other test starts, and wall time drops at least 10x against the full gate.

- **Address edits by stable symbol id, not by text block** — FEATURE — value 5 — effort M — risk med — category: editing
  Why: the demo's `fm edit` block form refused a delete because `===` ran into `>>>`. Each failed edit costs a full model turn. Assumption: most failed edits target a named function or class.
  Done when: an edit that names a symbol still applies after the file is reformatted, and the block-delete case from the demo applies on the first try.

- **Canary Claude Code's hook schema against each new release** — FIX — value 4 — effort S — risk low — category: compatibility
  Why: the pack shows repeated work on Claude Code version behaviour (the pane's background paint, T-1217, and the release-bisect idea). Assumption: hook payload fields change between releases without notice.
  Done when: a nightly job replays a recorded hook payload against the installed and newest Claude Code, and any field change opens a task naming the field.

- **Port a proven fix to sibling repos by code shape** — FEATURE — value 4 — effort L — risk med — category: reuse
  Why: once a fix is proven in one repo, the same bug pattern often exists in others. Assumption: the user runs several repos with shared idioms.
  Done when: a proven fix in repo A yields a candidate patch in repo B where the same AST shape matches, and the patch is either green on B's gate or listed for review, never applied silently.

- **Merge playbooks that behave the same, not just read the same** — CLEAN — value 4 — effort M — risk low — category: library hygiene
  Why: the library is 1,229 skills in `plugin/skills/` and aiming at tens of thousands. Text-similar merging misses duplicates that differ in wording but pass the same proofs.
  Done when: two playbooks with identical proof outcomes across the eval set collapse to one entry with an alias, and routing returns the survivor for both names.

- **Make the backlog an editable live table** — FEATURE — value 3 — effort M — risk low — category: backlog UI
  Why: the user steers by dropping, deferring and reprioritising, and the open list runs past 70 items. Changing a row by hand is faster than issuing commands.
  Done when: editing a row's value or effort in the table reorders the queue on the next render, and the same change is visible in `fm status` with no extra command.

- **Keep a per-repo local adapter trained on accepted diffs** — FEATURE — value 4 — effort L — risk high — category: local model
  Why, wild: closed tasks and the user's accepted or reverted diffs form a labelled set that no model sees today. Assumption: a small adapter can learn the repo's house style and common fixes.
  Done when: the adapter proposes the accepted diff for three held-out closed tasks, the gate passes each, and the run makes zero network calls.

- **Keep the queue moving on codemods when the model is unavailable** — FEATURE — value 4 — effort M — risk med — category: resilience
  Why, wild: a usage limit stops the whole queue, and `fm run` only waits or fails over. Mechanical tasks such as renames, import moves and signature updates need no model at all. Assumption: a large share of queued tasks are mechanical.
  Done when: with the model blocked for a usage limit, a queued rename task completes through a codemod, passes the gate, and is marked as deterministic in its receipt.

- **Cap each diff by its file's churn history** — SECURITY — value 3 — effort S — risk low — category: change safety
  Why: a single model run can rewrite a file far beyond the task's need. Assumption: a file's 90-day median churn is a reasonable ceiling for an ordinary change.
  Done when: a diff that adds or removes more lines than 3x the file's median is held for a one-line confirmation, and a diff under the cap proceeds with no prompt.

- **Turn each closed task into a scannable proof card** — DELIGHT — value 2 — effort S — risk low — category: receipts
  Why, wild: the receipt is text in the terminal and nowhere else. A QR code on the receipt lets a phone replay the failing test and the passing run.
  Done when: the close receipt includes a QR code that opens a static page showing the failing and passing output, and the page loads with no network request beyond its own file.
