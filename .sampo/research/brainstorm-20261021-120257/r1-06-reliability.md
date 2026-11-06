# Brainstorm — lens: reliability

- **Sync upstream assets transactionally with a last-good snapshot** — FEATURE — value 5 — effort M — risk low — category: integrations
  Why: the six repos are to be integrated "automatically", and the pack shows `fm plugins find/install` but nothing on partial or interrupted sync. assumption: a sync today can leave a half-written skills tree.
  Done when: a test kills the sync at each of 20 injected points and the active skills/plugins tree still matches either the old or the new pinned-SHA manifest, never a mix. A bad fetch leaves the previous snapshot active.

- **Parse registry.yaml with a stdlib YAML-subset reader fuzzed on real shapes** — FIX — value 4 — effort M — risk med — category: parsing
  Why: claude-cookbooks indexes via `registry.yaml`, and the constraint is stdlib-only Python with no PyYAML. A hand-rolled reader is the likeliest silent-corruption point. assumption: no such reader exists yet.
  Done when: a fixture set of the real registry's constructs (anchors, multiline strings, lists of maps) parses to expected JSON. A mutation fuzzer of 10k variants never crashes, hangs, or returns a partial result without an error flag.

- **Read marketplace.json tolerantly and reconcile renames** — FEATURE — value 4 — effort M — risk low — category: integrations
  Why: the claude-plugins-official file is about 190 KB with 166+ plugins, mixed `source` kinds (local path, git-subdir, url), sha pins and renames. One unknown field must not drop the whole catalogue.
  Done when: a fixture with an unknown source type, a missing sha and a renamed plugin yields per-entry statuses (ok/skipped/renamed). The 165 good entries load, and an installed plugin under an old name is mapped to the new one.

- **Run a poison-asset corpus through the skill and plugin indexer** — SECURITY — value 4 — effort S — risk low — category: ingest
  Why: the constraint is that third-party skills run nothing unguarded. Malformed SKILL.md files (bad frontmatter, name ≠ folder, description over 1024 characters, BOM/CRLF/bidi characters, symlink loops, a 50 MB body) are the first thing an auto-integrator meets.
  Done when: a checked-in corpus of at least 25 hostile assets is ingested. Each is quarantined with a one-line reason, the indexer exits 0 within a time cap, and none is ever routed.

- **Keep a license ledger that fails closed** — SECURITY — value 4 — effort S — risk low — category: legal/provenance
  Why: the pack notes docx/pdf/pptx/xlsx are source-available, financial-services is Apache-2.0, cookbooks MIT, and the tutorial has no licence ("ideas only"). Auto-adoption could copy text it may not vendor.
  Done when: every imported asset carries a licence record. An unknown or restricted licence blocks vendoring into the repo and allows reference-only use. A test with the tutorial repo's content proves no text is copied.

- **Bisect imports to find the asset causing a failure** — FEATURE — value 4 — effort M — risk low — category: diagnosis
  Why: with 19 skills, 166 plugins and a finance marketplace potentially active, a stall or conflict ("it just isn't doing anything") will be hard to attribute. assumption: only per-plugin conflict dicts exist today.
  Done when: `fm doctor --bisect-imports` takes a failing probe command, disables halves of the imported set in a scratch profile, and names the single asset (or pair) that flips the probe, in at most ceil(log2 N)+1 probe runs.

- **Fetch upstream offline-first with conditional requests and a circuit breaker** — PERFORMANCE — value 4 — effort M — risk low — category: network
  Why: auto-sync of six GitHub repos must not block `fm code` startup, which has already been criticised for silent waits (T-1336 stall work).
  Done when: with the network denied, `fm code` reaches its first output in under the existing startup budget. ETag/If-None-Match is used on refresh. After 3 failures the breaker opens for a backoff window and `fm doctor` says so.

- **Freeze a mini-corpus of each repo's shape, plus a non-blocking live drift canary** — FEATURE — value 3 — effort M — risk low — category: testing
  Why: the "every claim backed by a check that runs" rule means CI cannot depend on github.com. Upstream shape changes should surface as a task rather than a red build.
  Done when: CI runs the importers against checked-in synthetic fixtures with no network. A weekly canary diffs live shapes and files a captured task on drift without failing any gate.

- **Pass a deadline tree through every fm code run** — FIX — value 4 — effort M — risk med — category: run reliability
  Why: stalls are detected (T-1336), but planner, worker, check and judge each time out on their own. A parent can expire mid-child with nothing left to write the journal.
  Done when: a test asserts each child deadline ≤ parent minus a reserved grace, and a run killed by the root deadline still writes a final journal record naming which stage was cut.

- **Execute imported scripts only through one exec broker** — SECURITY — value 5 — effort M — risk med — category: containment
  Why: skills ship `scripts/`. The constraint is that nothing third-party runs unguarded, and a hung or noisy script is also a reliability fault.
  Done when: every imported-script path goes through one function enforcing the guard verdict, rlimits (CPU, memory, output cap), a process-group kill, and no network unless declared. A lint test fails on any other `subprocess` call under the importer modules.

- **Wild: Fetch each upstream by two independent paths and require tree-hash agreement** — SECURITY — value 3 — effort M — risk low — category: supply chain
  Why: "supply-chain compromise" is out of scope for assistance, and a single compromised mirror or CDN edge is the cheap attack on auto-sync. assumption: stdlib can do git-over-https plus the tarball API.
  Done when: sync accepts a SHA only if the git tree hash and the tarball-derived tree hash match. A test with a tampered stub server on one path is refused and logged.

- **Wild: Soak newly synced content in shadow before it can be routed** — FEATURE — value 4 — effort L — risk med — category: staged rollout
  Why: new upstream skills change the always-on token tax and may conflict with the existing guard or hooks, which the pack already worries about (context tax, hook latency).
  Done when: new assets sit in a "shadow" state for N sessions. They are loaded in dry-run, with token cost, conflicts and hook p99 recorded, and are promoted only if all stay under budget.

- **Wild: Hold an upstream-outage game day with a hostile local stub server** — FEATURE — value 3 — effort M — risk low — category: fault drill
  Why: real outages arrive as 429s, truncated bodies, wrong content types and slow-loris responses, not as clean failures.
  Done when: `fm doctor --drill upstream` starts a stdlib `http.server` that serves each of those faults to the sync and `fm code runners` paths. Every path ends in a named degraded state in under a time cap with no traceback and no state change.
