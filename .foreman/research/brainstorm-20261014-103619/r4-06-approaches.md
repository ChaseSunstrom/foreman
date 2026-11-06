# Brainstorm — lens: approaches

- **Mine unused surface from live payloads, flags and settings** — FEATURE — value 4 — effort S — risk low — category: native-integration
  Why: Foreman uses 14 hook events, but nothing shows which fields in their payloads or the statusline JSON it never reads. The same goes for `claude --help` flags and settings keys. Existing ideas record fixtures; none diffs fields. This is the cheapest way to find CC features without reading release notes. Trade-off: it finds fields, not meaning, so a human or agent still triages them.
  Done when: `fm doctor` lists, per event, payload keys seen in the last N runs that no `plugin/lib` code reads, and flags any key that wasn't there last week.

- **Deny credential-path reads on the native Read, Grep and Glob tools** — SECURITY — value 4 — effort S — risk low — category: guard
  Why: assumption: the guard is Bash-centred ("blocks dangerous commands in bypass mode"). In bypass mode the Read tool can still open `~/.ssh/*`, `.env` and cloud credentials, and the content then sits in the transcript. A PreToolUse matcher on those tools reuses the existing allowlisted-secret logic. Trade-off: it adds a hook match on the hot path, so keep the check to a string-prefix test.
  Done when: a fixture `Read ~/.ssh/id_ed25519` is refused with a fix hint, `Read .env.example` is allowed, and `bench_hooks.py` p50 doesn't regress.

- **Mine Claude Code's own debug log for failures it swallowed** — FIX — value 4 — effort S — risk low — category: observability
  Why: CC treats hook timeouts and non-2 exits as non-blocking, so a crashed guard can fail open without anyone seeing it. Existing ideas count Foreman's own swallowed exceptions and fail closed on crashes, but nothing reads the host's side of the story. Trade-off: the log format is unstable, so it needs a tolerant parser and a canary.
  Done when: a hook deliberately made to time out in a test session shows up in `fm doctor` as "guard did not run for N tool calls" within one session.

- **Compute the lethal-trifecta posture live** — SECURITY — value 4 — effort M — risk med — category: guard
  Why: the idea list has taint tracking and egress manifests, but not one derived session state. When the session has (a) touched private-class files, (b) ingested untrusted text (WebFetch, MCP, Artifact comments) and (c) has a live egress route, it should tighten itself. Trade-off: false tightening annoys a user who wants full autonomy, so it must release when taint is cleared by a fresh session or compaction.
  Done when: a scripted session that reads `.env`, then fetches a page, then tries `curl -d @file` or `git push` is held for a grant, and the same commands without the fetch pass.

- **Stamp every commit with task, lane, model and evidence-hash trailers** — FEATURE — value 3 — effort S — risk low — category: provenance
  Why: the ledger hash-chain and signed receipts live in central state. Trailers travel with the repo, so a reviewer or CI on another machine can check provenance. They also enable model-tinted blame, which exists only as a wild idea. Trade-off: trailers are not tamper-proof without signing.
  Done when: `git log --format=%(trailers)` on a task's commits shows `Foreman-Task`, `Foreman-Model` and `Foreman-Evidence`, and `fm verify-commit <sha>` recomputes the hash.

- **Declare every native dependency in one manifest** — CLEAN — value 4 — effort M — risk med — category: native-integration
  Why: the idea list already has fallback ladders, mask tests, an overlap tracker and a field guide as separate items. Each would otherwise keep its own list of "which CC features we rely on". One `native.toml` (feature, probe, fallback, owning module, expiry) would drive doctor, mask tests, docs and adoption tasks. Trade-off: it is migration work with no visible payoff until the second consumer exists.
  Done when: adding a new native feature requires one manifest entry, and `fm doctor`, the mask test and MASTER.md's native section are all generated from it with no hand edits.

- **Reject invisible and bidirectional characters in diffs and injected context** — SECURITY — value 3 — effort S — risk low — category: supply-chain
  Why: existing ideas neutralise control sequences when rendering, but nothing scans what an agent writes or what a fetched page injects. Trojan-Source-style characters can hide instructions or flip code meaning in a diff. Trade-off: legitimate i18n strings need an allowlist by file glob.
  Done when: a fixture diff containing U+202E fails the done gate with the file and line, and a fetched-page fixture containing zero-width text is stripped before it reaches context.

- **Run hooks with `-I -S` and prebuilt unchecked-hash bytecode** — PERFORMANCE — value 3 — effort S — risk med — category: hook-latency
  Why: hooks are latency-gated, and each one pays interpreter startup and imports. Existing ideas cover a resident daemon (large) and import budgets (per-module). This is the small step: a build step compiles `plugin/lib` with `compileall --invalidation-mode unchecked-hash`, and hooks start in isolated mode. Trade-off: Foreman editing its own source leaves stale bytecode unless the build step reruns, so the guard must refuse edits to `lib` without a rebuild.
  Done when: `bench_hooks.py --runs 20` shows a lower p50 on a cold start, and editing a lib file then running a hook gives the new behaviour.

- **Write big tool outputs to an evidence file and return a stub** — PERFORMANCE — value 3 — effort M — risk med — category: tokens
  Why: the existing "learned output digesters" depend on usage data. This is the plain version: a PostToolUse rule applies above a size threshold. The model gets head, tail, line count and a path, and the same file becomes the evidence that `fm task finish` already records. Trade-off: a hidden key line in the middle may be missed, so the stub must include grep-able error lines.
  Done when: a 5,000-line test log returns under 60 lines to the model, the full file is linked from the step evidence, and a failing test's name still appears in the stub.

- **Host the guard playground as an Artifact (wild)** — FEATURE — value 3 — effort M — risk low — category: trust UI
  Why: wild. A private Artifact page where the user pastes a command and sees the guard's parse and verdict. Its "ask Claude" control explains a refusal in plain words. It reuses the Artifact runtime that Foreman doesn't use yet and makes refusals teachable on the phone. Trade-off: the verdict logic must be a data-only export, or the page diverges from the real guard.
  Done when: a command pasted on the page shows the same allow or deny and reason as `fm guard check` for 20 corpus cases.

- **Print a Remote Control QR at night-run start (wild)** — FEATURE — value 4 — effort S — risk med — category: devices
  Why: wild. Remote Control sessions are in the tool list and unused. The idea list has phone pushes and a PWA cockpit, but not a one-scan way to steer the live session from a phone. Trade-off: this opens a remote steering path, so it needs an explicit setting and an expiry.
  Done when: with the setting on, `fm night` shows a scannable link in the band, and with it off nothing is printed or opened.

- **Mutate recorded hook payloads against every hook (wild)** — SECURITY — value 3 — effort M — risk low — category: resilience
  Why: wild. The scrubbed live payload fixtures would feed a fuzzer that nulls, truncates, oversizes or unicode-bombs each field. This proves each hook fails safe when CC changes a payload shape. Trade-off: it finds crashes, not wrong decisions.
  Done when: the fuzz run exits clean over 500 mutations per hook, with no traceback and no guard allow on malformed input.

- **Dead-reckon the band between events (wild)** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild. The band is event-driven, so it looks frozen during a long tool call. It could extrapolate the current step's elapsed time against that step type's historical median and show a soft "usually ~40s" cue. It is also a cheap honest signal for "idle versus slow" without an extra process.
  Done when: during a 60-second gate the band changes at least every 5 seconds, using only data already on disk.
