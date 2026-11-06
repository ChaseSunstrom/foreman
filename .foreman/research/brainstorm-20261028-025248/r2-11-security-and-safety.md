# Brainstorm — lens: security and safety

- **Scrub invisible and bidi control characters from packs and task text** — SECURITY — value 4 — effort S — risk low — category: input hygiene
  Why: The pack and pasted user text go to the model as data, so hidden Unicode (zero-width, bidi overrides, tag characters) can smuggle instructions past a human reviewer. Assumption: the pack builder passes text through unchanged today.
  Done when: a fixture containing U+202E and U+E0000-range characters is stripped before the pack is written, and a test asserts the output has none of them.

- **Give model subprocesses an environment allowlist, not an inherited one** — SECURITY — value 5 — effort S — risk low — category: secret exposure
  Why: T-1791 shows subprocesses already inherit the shell's environment (a 200k window leaked into tests). Assumption: API keys and cloud tokens in the user's shell reach every model-run child and any command it runs.
  Done when: a run started with `GITHUB_TOKEN` set in the parent shows the variable absent in the child's `env`, and an allowlist test fails if a new variable is added without review.

- **Escalate any diff that touches CI, hooks, installers or lockfiles to a review card** — SECURITY — value 5 — effort S — risk low — category: supply chain
  Why: CI and Pages actions were pinned by SHA (T-1804), and hook files and install scripts run with the user's authority. Assumption: a normal task diff can quietly edit these paths, and nothing flags it at close.
  Done when: a fixture diff touching `.github/workflows/` or `plugin/hooks/` produces a needs-you card and blocks auto-close until the user confirms it.

- **Refuse commands assembled at runtime** — SECURITY — value 4 — effort M — risk med — category: guard
  Why: The guard matches command spellings (see "Fuzz the guard"), but `eval`, `base64 -d | sh`, and commands read from a file and then executed slip past text matching. Assumption: the guard is text-based and does not track what a pipe feeds into an interpreter.
  Done when: `echo cm0gLXJmIH4= | base64 -d | sh` and `eval "$X"` are refused with a plain-English reason, and both are in the refusal corpus.

- **Ask once before a new runner receives the repo** — PRIVACY — value 3 — effort S — risk low — category: consent
  Why: Packs go to Claude, Codex, Gemini and opencode when a lane uses them (T-0335, T-0336). Assumption: the user does not see which provider gets which context in a mixed-runner setup.
  Done when: the first pack sent to a runner not yet approved for this project shows the runner name and the file count, and it waits for a yes before sending.

- **Cap deletions per run and require a fresh approval beyond the cap** — SECURITY — value 4 — effort S — risk low — category: destructive change
  Why: A run can remove a whole module in one edit with no cap, and close only checks that tests pass. Assumption: a passing suite can still hide a large unintended deletion.
  Done when: a run that removes more than 200 lines or 5 files pauses with a needs-you card, and a test proves the pause.

- **Ratchet the refusal corpus so it can only grow** — SECURITY — value 4 — effort S — risk low — category: regression guard
  Why: Refusal cases are hand-added (see the "Fuzz the guard" idea), and nothing stops one being deleted to make a failing test pass. Assumption: a case removed in a cleanup would not be noticed.
  Done when: deleting a refusal case from the corpus makes `fm doctor` fail with the case name, unless the commit adds a `retired:` note.

- **Keep flagged injection text in a read-only quarantine folder** — SECURITY — value 3 — effort S — risk low — category: injection triage
  Why: wild — instead of dropping text the guard flags as injection, keep it in a read-only folder the user can review, so a false positive can be fixed and a real attack can be studied.
  Done when: a fixture with "ignore previous instructions" in a pasted note is saved under the quarantine folder, mode 0400, and listed by `fm` on request.

- **Replay refused commands into a sealed honeypot** — SECURITY — value 2 — effort M — risk med — category: threat study
  Why: wild — every refused command is re-run inside an empty container with no network and no home directory, so the team can see what the model was trying to do without exposing the machine.
  Done when: a refused `curl ... | sh` is re-run in the container, the host's filesystem and network are unchanged, and the attempt is logged with its refusal reason.

- **Publish a public ledger of reported guard bypasses** — SECURITY — value 3 — effort M — risk low — category: disclosure
  Why: wild — each reported bypass gets a dated entry, a failing regression test named after it, and a fix commit, so the guard's gaps are visible and closed in the open. Assumption: the project accepts external reports.
  Done when: a reported bypass produces a test that fails before the fix and passes after, and the ledger lists the entry with the commit hash.
