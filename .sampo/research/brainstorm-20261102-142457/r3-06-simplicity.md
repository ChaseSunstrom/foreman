# Brainstorm — lens: simplicity

- **Render the web UI from `--json` only** — CLEAN — value 4 — effort M — risk low — category: ui
  Why: assumption: the web UI reads ledgers through its own paths, so the UI and CLI can disagree. The pack lists no shared source, and T-0166 shows `register.tsx` already carrying logic it shouldn't.
  Done when: a test fails if any web view calls anything but a verb's `--json`, and each view equals its CLI twin on a fixture.

- **Ratchet the web UI to zero build and zero external requests** — SECURITY — value 3 — effort S — risk low — category: ui
  Why: assumption: `plugin/templates/web/index.html` is a single file today. A byte ceiling plus a CSP of `default-src 'self'` keeps it from growing a toolchain or a phone-home, and the DNS-rebinding hardening idea gains a smaller surface.
  Done when: CI fails when the template exceeds N KB, when it contains a non-local URL, or when a bundler config appears.

- **Fit every web view in 80×24 without scrolling** — FEATURE — value 3 — effort S — risk low — category: ui
  Why: assumption: views grow by accretion, and the pane/narrow-terminal work (T-1217, 40-column ideas) shows size pressure. One-screen is a rule a person can check by eye.
  Done when: a golden-screenshot test at 80×24 passes for each view, and a view that overflows fails the gate.

- **Declare each agent adapter as data, behind one conformance fake** — CLEAN — value 4 — effort M — risk med — category: agents
  Why: T-0335/36/37 are long-blocked on codex/gemini/opencode because each adapter is code that needs live verification. A table of hook names, flags and transcript paths that a single fake exercises shrinks the surface.
  Done when: adding or removing a harness is a data-file edit, and one conformance run reports each adapter's cells as verified or unverified.

- **Give every multi-agent flow a tested single-agent path** — FEATURE — value 4 — effort M — risk low — category: agents
  Why: assumption: brainstorm, audit and lanes assume fan-out. The user's standing rule that Foreman works with no `claude` on PATH implies a degraded one-agent path should exist and be exercised.
  Done when: `FM_AGENTS=1` runs brainstorm and `fm audit` end to end on a fixture, and the output differs only in breadth.

- **Hard-cap sub-agent depth at 1 and width at one constant** — SECURITY — value 3 — effort S — risk low — category: agents
  Why: assumption: depth and width limits are scattered. The unattended drive, the lanes and the orchestrator ideas all multiply spend and attack surface.
  Done when: a child that tries to spawn a child is refused with a `Next:` line, and one constants file holds the width limit.

- **Keep the roster of agent roles in one table** — CLEAN — value 3 — effort S — risk low — category: agents
  Why: assumption: roles (reviewers, cold readers, lens children) are defined across skills and libs. One table of role, model, tools and budget lets "who can do what" be read in one screen and audited.
  Done when: a lint fails on a spawned role not in the table, and `fm agents` prints the table.

- **Add `fm config --diff`, showing only non-default values** — FEATURE — value 3 — effort S — risk low — category: CLI
  Why: "Resolve `fm config` values with their source" is listed, but a full dump is the wrong default. Seeing only the deviations is how a user finds an unsafe override.
  Done when: on a fresh install it prints "all defaults", and after one change it prints exactly that line with its source.

- **Ratchet the count of state files; a new one must merge or retire another** — CLEAN — value 3 — effort M — risk med — category: state
  Why: ledgers, flakes.json, steers and the rest keep multiplying, and the ideas list proposes several more. A count ratchet is simpler than the classification schemes already proposed.
  Done when: `fm doctor` lists the state-file count against its ceiling, and an extra file fails the ship gate.

- **Prove state is readable with `cat` and `grep` alone** — SECURITY — value 3 — effort S — risk low — category: state
  Why: assumption: a user in trouble can't run a broken `fm`. The hash-chain and rescue-doctor ideas assume tooling, but plain lines are the lowest-risk reader.
  Done when: a test reads each state file with `grep`/`cut` only and extracts task id, status and verdict.

- **Wild: Monk mode, a profile with four tools and no shell** — FEATURE — value 3 — effort M — risk med — category: safety (wild)
  Why: the safest bypass is no bypass. A profile exposing read, edit, test and `fm task` for docs or review sessions removes the whole guard problem for those sessions.
  Done when: a session in monk mode cannot run Bash, and a replayed shell-heavy task fails with a message naming the full profile.

- **Wild: Complexity advocate, a child that reads each diff and scores new nouns** — FEATURE — value 3 — effort M — risk med — category: agents (wild)
  Why: Foreman cold-reads for safety but nothing reviews for the count of new verbs, flags and files a diff introduces. A tool-less child reading only the diff is cheap.
  Done when: `fm ship` prints "new nouns: N (verbs, flags, files)" and blocks above a set budget without a recorded reason.

- **Wild: Agents pay rent** — CLEAN — value 3 — effort M — risk med — category: agents (wild)
  Why: each sub-agent role should show a pass-rate or cost delta over doing the step inline. Lens-rate data exists (T-0829), so the evidence is partly there.
  Done when: a role with no measured gain for 60 days is listed by `fm doctor` as an eviction candidate, with its numbers.

- **Wild: Lazy state, with nothing created until the first write that matters** — SECURITY — value 2 — effort S — risk low — category: footprint (wild)
  Why: assumption: a read-only trial of `fm map` or `fm doctor` still creates directories. That undermines the uninstall-leaves-nothing claim.
  Done when: on an empty home, running `fm doctor` and `fm map` leaves a filesystem diff of zero files.

Next question: which of Foreman's surfaces (web UI, pane, site, Desktop) can be deleted with no loss of an action the user has taken in the last 30 days?
Next question: which sub-agent roles does Foreman spawn that the user has never read the output of?
