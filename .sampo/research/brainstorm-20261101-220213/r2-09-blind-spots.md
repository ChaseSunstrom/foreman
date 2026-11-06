# Brainstorm — lens: blind spots

Answers to earlier questions: (1) Offline proofs: anything judged by a local command, such as exit codes, hashes, plan diffs and docs-example runs. Anything that needs a vendor account should carry the label "unproven: outside Foreman's reach", and only the user may accept it. (2) When proofs disagree, the stricter and more recent one wins, and the conflict is shown to the user, not resolved silently.

**Blind-spot classes.** The user's late asks fall into five classes:
- Work that needs a session (T-2499).
- A dimension that wasn't split (T-2500).
- A gauge that measures form, not substance (T-2503, T-2504).
- A map that went stale (T-2502).
- A fix that broke its sibling's premise (T-2525).

I asked the question for each class of the whole project:

- **Session-bound work** — what else only advances while a session is open?
- **Stale maps** — what else shown to the model or user is older than it claims?
- **Sibling premises** — what else does a fix break that nobody listed?
- **Form-only gauges** — what else can go green without improving anything?
- **Lean and safe surfaces** — what, per surface, is never measured at all?

- **Audit every loop that only advances inside a session** — FIX — value 5 — effort M — risk low — category: operate/headless
  Why: T-2499 found bets that settled only when a hook fired; ci-watch, outcomes, the sweep and genesis live are likely the same.
  Done when: `fm doctor` lists each state-advancing path as tick-driven or session-bound, and a test firing no hooks shows every tick-driven path advancing.

- **Stamp every injected derived artifact with its age in commits** — FIX — value 4 — effort S — risk low — category: context
  Why: the pack's own map is "as of an older HEAD" (2098 files), and nothing says how stale it is.
  Done when: the injected map, card and lesson lines carry "N commits old", and one over a set threshold is flagged or omitted in a test.

- **Tag each test with the premise it asserts, and list siblings at finish** — FEATURE — value 4 — effort M — risk low — category: verify
  Why: T-2334's fix silently broke a premise held by the docs-unknown proof test, which T-2525 then had to repair.
  Done when: a fixture reproducing T-2334 makes `fm task finish` name the premise-sharing test before closing.

- **Add an "inflated by" line to every `fm doctor` gauge** — CLEAN — value 4 — effort S — risk low — category: measurement
  Why: the user had to ask for lean to measure substance (T-2503), and the templated-cell rule exists because counts were gameable.
  Done when: each gauge in `fm doctor --json` has a non-empty `inflated_by` field, and a test fails if one is missing.

- **Derive the guard's destructive-verb list from installed tools' help** — SECURITY — value 4 — effort M — risk med — category: guard
  Why: assumption: the rules are hand-written, and 42 blocks of one rule in 7 days show only a few classes fire in practice.
  Done when: for a fixture tool whose help text says "delete", `fm guard coverage` reports the unmatched verb.

- **Make the README demo carry its host version and go stale visibly** — FIX — value 3 — effort S — risk low — category: docs/claims
  Why: the README embeds a real Claude Code 2.1.301 session, and T-2504 asked that public claims be proven.
  Done when: `fm doctor` warns when the stamped host version differs from the installed one by a minor version.

- **Give each standing rule a last-fired date and a proposed retirement card** — CLEAN — value 4 — effort M — risk med — category: lean
  Why: 40+ steers are in force, and the rules size may not grow (§6).
  Done when: `fm decide --check list` shows days since each rule last fired, and one unfired for 60 days appears on a single retire-or-keep card, never auto-applied.

- **Budget the Desktop app's idle CPU and memory** — PERFORMANCE — value 3 — effort S — risk low — category: Desktop
  Why: assumption: the budgets cover hooks and bytes, but nothing covers a resident app (T-0325, T-0352).
  Done when: a 10-minute idle run reports CPU under 1% and RSS under a set cap, and CI fails above either.

- **Scan the state directory for secrets and loose file modes** — SECURITY — value 4 — effort S — risk low — category: privacy
  Why: research packs, steers and pasted content sit under `~/.claude/foreman/state`, including user words and account details.
  Done when: `fm doctor` reports 0 findings on a clean state dir and finds a planted canary key and a world-readable file.

- **Test shared-server isolation for headless use** — SECURITY — value 3 — effort M — risk med — category: server
  Why: assumption: the headless/server cells exist but the multi-user case isn't in the pack.
  Done when: in a two-user test, user B can't read user A's state, and the web UI refuses a non-loopback bind without a token.

- **Wild: Re-read every closed FIX's premise nightly** — FIX — value 3 — effort M — risk low — category: regression
  Why: wild; T-2525 shows fixes encode premises that later fixes break.
  Done when: a nightly lane re-checks each FIX's one-sentence premise against the current code and files a task when a planted contradiction is found.

- **Wild: Run `fm code` on a 4k-context local model as a lean torture test** — PERFORMANCE — value 3 — effort L — risk med — category: lean/local
  Why: wild; if the loop and injection fit a tiny window, they fit anywhere, and the 387k context per reply stops hiding bloat.
  Done when: one trivial task closes on a 4k-context local model, and the report lists what had to be cut to fit.

- **Wild: Time a stranger's VPS with no `claude` on it** — FEATURE — value 4 — effort M — risk low — category: install
  Why: wild; the standing rule says Foreman works with no `claude` on PATH, and nothing shows a clean-machine clock.
  Done when: a fresh container with no agent CLI runs `install.sh`, `fm doctor` and one task to close, and prints the elapsed time.

Next question: Which of Foreman's own numbers (the hook p95 of 278 ms, 387k context per reply) are averages that hide a worse tail on the surfaces nobody uses daily, such as headless/server and Desktop?
Next question: What does the user currently check by hand after a ship or a night run that no verb or doctor line yet checks for them?
