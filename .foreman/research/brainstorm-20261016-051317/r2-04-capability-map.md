# Brainstorm — lens: capability map

- **Export Foreman events as OpenTelemetry** — FEATURE — value 4 — effort M — risk low — category: observability
  Why: assumption: the pack has a ledger, spend and hook-latency data but no way to send them to Grafana, Honeycomb or Datadog, which most best-in-class agent tools offer. Observability is listed as thin.
  Done when: with `fm otel on` pointing at a local collector, one closed task produces a trace with task, stage and gate spans plus cost attributes, and with it off nothing is sent.

- **Scope gates to the workspace you touched** — FEATURE — value 4 — effort M — risk med — category: monorepo
  Why: the map lists one global gate set (`fm doctor`, a roundtrip, a bench). Assumption: user monorepos have per-package test commands, and running everything is slow and noisy.
  Done when: in a fixture monorepo, editing `packages/a` runs only `a`'s gate and its dependents' gates, and `fm map` prints the workspace graph.

- **Import and export specs from spec-kit and Kiro** — FEATURE — value 4 — effort M — risk low — category: spec-driven
  Why: assumption: spec-first tools (requirements, then design, then tasks) are where rival tools compete. The pack only has "pre-register success test", not a full requirements chain.
  Done when: a spec-kit `spec.md` imports into a brief with acceptance criteria as red-first checks, and a closed task exports back to the same format.

- **Split big diffs into stacked PRs** — FEATURE — value 3 — effort M — risk med — category: shipping
  Why: assumption: Graphite-style stacks are table stakes for review. The pack has "ship to a PR" and a merge train, but nothing breaks an L-sized diff into reviewable slices. "Slice L tasks vertically" exists only for planning.
  Done when: a 600-line branch becomes 3 ordered branches, each passing gates alone, with PR descriptions linking the stack.

- **Sync the queue two-way with Linear, Jira and GitHub Projects** — FEATURE — value 3 — effort M — risk med — category: integrations
  Why: assumption: "turn GitHub issues into tasks" covers inbound GitHub only. Teams track work elsewhere and want status and receipts written back.
  Done when: a Linear issue becomes a task, and closing the task comments the evidence bundle and moves the issue to Done, with a dry-run diff first.

- **Add a performance-budget gate for the user's project** — FEATURE — value 3 — effort M — risk low — category: gates
  Why: Foreman benches its own hooks (`bench_hooks.py`) but offers users no equivalent. Assumption: a "p95 ≤ X ms or bundle ≤ Y KB" criterion is a natural verify type.
  Done when: a task with `perf: cmd=…, max=…` fails close when a seeded slowdown breaches the budget, and the run output shows the baseline delta.

- **Gate dependencies on licence and SBOM** — SECURITY — value 3 — effort S — risk low — category: supply chain
  Why: "check new dependencies before installed" and SAST scanners are covered, but licence policy and a CycloneDX SBOM are not. Assumption: teams need both before adoption.
  Done when: adding a GPL dependency to a repo whose policy forbids GPL blocks close with the offending package named, and `fm sbom` emits valid CycloneDX.

- **Add a screen-reader linear mode for the pane** — FEATURE — value 3 — effort S — risk low — category: accessibility
  Why: reduced motion and a colourblind palette are queued, but a pane built from braille gauges and lanes reads badly to assistive tech. Assumption: nobody has tested that.
  Done when: `fm ui --linear` prints one stable, ordered, ASCII-only status block with no redraw spam, and a snapshot test pins it.

- **Build a local semantic code index (opt-in)** — FEATURE — value 4 — effort L — risk med — category: retrieval
  Why: `fm map` is structural, and Cursor, Cody and Continue all ship semantic search. Assumption: a local embedding model keeps this inside the privacy-first stance, with nothing uploaded.
  Done when: `fm find "where do we retry failed uploads"` returns ranked file ranges from a local index that updates incrementally, and a network-off run still works.

- **Keep docs and changelog in sync with the public surface** — FEATURE — value 3 — effort M — risk low — category: docs
  Why: "README claims into checks" covers claims only. Assumption: a changed public symbol or verb should force a docs and changelog update, and broken links should be caught.
  Done when: renaming a verb in a fixture fails close until docs and the changelog entry change, and link check passes.

- **Run coordinated multi-repo tasks** — FEATURE — value 3 — effort L — risk high — category: multi-repo
  Why: assumption: real changes often span a library and its consumer. The pack has cross-repo transplant (wild) and sibling search, but not one task spanning repos with ordered landing.
  Done when: one brief lists two repos, each gets a worktree and gates, and merges land in dependency order or neither lands.

- **Wild: Accept tasks from other agents through an MCP inbox** — FEATURE — value 3 — effort M — risk med — category: interop
  Why: wild. The pack serves the brain over MCP (read side); this serves the queue (write side), so Cursor, Codex or a chat bot can file a task with a scoped, rate-limited token.
  Done when: an MCP client calls `foreman.enqueue`, the task appears in the queue marked with its origin, and an untrusted-text check runs on the payload.

- **Wild: Apply the discipline to infrastructure and data repos** — FEATURE — value 4 — effort L — risk med — category: domain packs
  Why: wild. Pack gates like `terraform plan` with no destroys, `kubectl --dry-run=server`, SQL migration up/down round trip and dbt tests, so "prove it with commands you ran" works outside app code.
  Done when: in a Terraform fixture, a task that would destroy a resource cannot close until the plan shows none, and the plan output is stored as the receipt.

- **Wild: Let a second person watch live and steer by comment** — FEATURE — value 3 — effort L — risk high — category: collaboration
  Why: wild. A read-only pane link where a teammate's comment on a step becomes a queued steer for the owner to accept, extending the QR phone idea into review while work happens.
  Done when: two browsers open the same session, a comment on a step appears in the owner's pane as a pending steer, and the viewer cannot run anything.

- **Wild: Generate a "what would Foreman do" report for any open-source repo** — FEATURE — value 3 — effort M — risk low — category: adoption
  Why: wild. `fm appraise <url>` clones read-only into a scratch folder and writes a one-page map covering gates it found, weak spots, hot files and first three suggested tasks. It doubles as a shareable demo for the "make it THE plugin" goal.
  Done when: running it on a public fixture repo writes an HTML page without touching the clone's tracked files and without network use beyond the clone.
