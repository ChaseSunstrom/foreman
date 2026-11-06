# Brainstorm — lens: bold bets

- **Run the plugin parity matrix in CI** — FEATURE — value 5 — effort M — risk low — category: plugin parity
  Why: the request requires every feature to work in the Claude Code plugin, but the e2e roundtrip and bench run only the CLI. Assumption: a headless `claude -p` session with the plugin loaded can call each fm verb and the hooks. Each verb that passes in the CLI but fails inside the plugin is a parity gap.
  Done when: CI fails the build if any fm verb listed in `fm help` has no plugin-session case, or if a case's plugin run differs in exit code or journal events from its CLI run.

- **Drop per-command hooks for a transcript-tailing observer** — PERFORMANCE — value 4 — effort L — risk med — category: hook latency
  Why: PreToolUse:Bash:script p95 sat at about 310 ms over its 300 ms budget, and a full read cost 124 s of CPU, mostly box and startup. Assumption: Claude Code's session transcript JSONL carries enough of each tool call to derive run state after the fact, so only the guard keeps a hook.
  Done when: with the observer on and only the guard hook installed, `bench_hooks --runs 20` has PreToolUse:Bash median under 50 ms and the journal matches the hook-driven journal for the same replayed session.

- **Synthetic user persona files complaints nightly** — FEATURE — value 4 — effort M — risk med — category: user simulation — wild
  Why: the user's own words show the same pain returning ("fm quiet ignores stdin", "defer --until reset"), and nothing tests the workflow the way that user phrases it. Assumption: a scripted persona built from the last 30 request phrasings can drive a fixture repo through the common paths.
  Done when: a nightly run executes 20 persona requests against the fixture repo and writes one complaint per request that fails or takes over 3x its baseline, with the transcript attached.

- **Infer the gates from CI workflow files on `fm init`** — FEATURE — value 4 — effort S — risk low — category: onboarding
  Why: the map lists gates by hand (`fm doctor`, roundtrip, bench), and CI red on main was only noticed after the fact. Assumption: the repo's `.github/workflows` run commands that already define its gates.
  Done when: `fm init` in a repo with a test workflow proposes the same commands CI runs, and the proposal passes `fm doctor` without edits.

- **Machine-wide spend ledger across every project** — FEATURE — value 5 — effort M — risk low — category: cost at scale
  Why: the usage burn and the weekly reset are one account pool, but `fm cost` and the budget are per project. A run in one repo can exhaust the window another repo needs. Assumption: the reset and the spend can be read from one local ledger.
  Done when: two projects run concurrently on one machine, `fm cost --all` reports the combined spend against the reset, and a queue in either project refuses to start when the combined ledger is past the cap.

- **Ship a stable and canary plugin channel** — FEATURE — value 4 — effort M — risk med — category: release channels
  Why: the site and the mod deploy from `build`, and a bad release reaches every installed copy at once. The plugin marketplace cards exist, but there is no staged channel. Assumption: the marketplace supports two named channels.
  Done when: `fm update --channel canary` installs from the canary channel, the stable channel only moves after the canary has run the parity matrix green for 24 hours, and both channels report their version in `fm status`.

- **Let teams share a gate cache keyed by tree hash** — FEATURE — value 4 — effort L — risk high — category: team speed
  Why: several checkouts re-run the same full gate on identical trees, and `check --affected` already memoizes locally. Assumption: teams accept a shared cache over their network, and a cache hit is only safe when the tree hash and toolchain hash both match.
  Done when: a second machine with the same tree and toolchain hash skips the full gate, reports `cache hit <hash>`, and a changed toolchain hash forces a real run.

- **Expose Foreman as an embeddable verb API for other plugins** — FEATURE — value 3 — effort L — risk med — category: extensibility
  Why: other Claude Code plugins re-implement the queue, the guard and the proof step. Assumption: a versioned, JSON-in JSON-out contract for six verbs (queue, prove, guard, check, close, status) is enough for a plugin to embed Foreman.
  Done when: a contract test runs a second plugin's fixture against the six verbs, pins the JSON schema version, and fails if a verb's output changes without a version bump.

- **Learn quiet hours from when the user types** — FEATURE — value 3 — effort M — risk low — category: attention
  Why: the user asked for the agent to act without asking, and the receipts and alerts still arrive at 3 a.m. Assumption: the timing of the user's prompts is stable enough across weeks to learn a sleep window.
  Done when: after 14 days of prompt timestamps, notifications and digests are held outside the learned window and released at its end, and a single override in the window delivers immediately.

- **Blame each proof to the request that earned it** — FEATURE — value 3 — effort S — risk low — category: traceability
  Why: the journal links tasks to commits, but a proof's reason is lost once the task closes. Assumption: the task's request text is stored with the proof and can be shown by `fm blame <file:line>`.
  Done when: `fm blame` on a changed line prints the task id, the request sentence and the proof command, and returns non-zero when no task wrote that line.

- **Make `fm doctor` a single pass/fail with the budget as one failing check** — CLEAN — value 3 — effort S — risk low — category: diagnostics
  Why: the rules file went over its 6,400-character budget at T-1520 and stayed over until someone asked. The doctor reports many checks but has no single verdict. Assumption: a failing budget should block the next `fm doctor` pass.
  Done when: `fm doctor` ends with one verdict line, exits non-zero when the rules file is over budget, and the verdict names the file and the characters over.
