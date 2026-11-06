# Brainstorm — lens: approaches

- **Route playbooks by the failing gate's error fingerprint** — FEATURE — value 4 — effort M — risk low — category: routing
  Why: The pack routes on request text, but a failed gate already names the problem in its output. Assumption: gate output is available before the playbook is chosen.
  Done when: A fixture with a known `TypeError` trace routes to its playbook with the request text removed.

- **Let each playbook's detector decide whether it loads** — FEATURE — value 4 — effort M — risk med — category: routing
  Why: Most of the 1,229 skills can't apply to any one repo. Each playbook ships a cheap check (a grep or command) and loads only when the check passes. Assumption: detectors are cheap enough to run per route.
  Done when: On the fixture repo, a playbook whose detector exits 1 never appears in `fm playbooks route` output.

- **Enable one stack bundle from the repo's manifests** — FEATURE — value 4 — effort M — risk low — category: loading
  Why: The pack already has per-stack cards (python, tailwind), so the bundle boundary exists. Manifests such as `pyproject.toml` or `package.json` reveal the stack without a model call.
  Done when: A Python-only fixture lists zero tailwind skills.

- **Route playbooks by git co-change history** — FEATURE — value 3 — effort M — risk low — category: routing
  Why: The commit log is long and T-numbered, so files that changed together are a free signal. Assumption: co-change pairs predict which playbook a file needs.
  Done when: On a fixture with a known co-change pair, editing one file surfaces the playbook for its partner.

- **Write model edits to an overlay and merge only proven diffs** — FEATURE — value 4 — effort L — risk med — category: safety
  Why: Edit leases exist because runs write straight into the tree and can collide or get stuck. An overlay upper layer gives the same isolation without leases. Assumption: overlayfs is available on the target systems, which may not hold on macOS or Windows.
  Done when: A run that fails its proof leaves `git status` byte-identical to before the run.

- **Fix the proof gap: run the full suite, not only the affected tests** — FIX — value 4 — effort M — risk low — category: verification
  Why: `fm check --affected` gives a fast signal, but a fix can pass its touched tests and break a distant one. Assumption: the affected-only proof is what closes tasks today.
  Done when: A fixture fix that breaks an untouched test fails the close, and the failing test's name appears in the receipt.

- **Keep one agent session warm across queued tasks** — PERFORMANCE — value 3 — effort M — risk med — category: latency
  Why: Each task spawns a fresh session that reloads the rules file and context pack. Assumption: the runner supports streamed input that carries several tasks in one session.
  Done when: Two queued tasks produce one session start in the journal, and the second task's receipt shows no rules reload.

- **Order gates by failure rate per second** — PERFORMANCE — value 3 — effort S — risk low — category: gates
  Why: The gate runs in a fixed order, so a cheap check that fails often waits behind a slow one that never fails. Ordering by failures per second of runtime surfaces breakage sooner. Assumption: the journal records per-gate outcomes and durations.
  Done when: On a fixture journal, the gate order puts the high-failure, low-cost check first.

- **Map one plain sentence to one fm verb and echo it** — FEATURE — value 3 — effort S — risk low — category: interface
  Why: The pack asks for fewer top-level verbs and fewer prompts. A sentence like "undo the last task" resolves to one verb, which is echoed before it runs.
  Done when: The fixture sentences "undo the last task" and "show what's blocked" each resolve to one verb with the echo shown.

- **Wild: let tests name the playbooks they need** — FEATURE — value 3 — effort S — risk low — category: routing
  Why: A test annotated `# needs: playbook-x` tells the router what it requires, so the suite becomes the index. Assumption: repo owners will annotate tests.
  Done when: A failing test with a `needs:` annotation adds that playbook to the next route with no request-text match.

- **Wild: write each playbook as a failing test the agent must turn green** — FEATURE — value 3 — effort L — risk med — category: playbooks
  Why: A playbook that is a test has a verdict the model can't argue with, so its usefulness is provable. Assumption: most playbook advice can be stated as a checkable property.
  Done when: A fixture playbook with a red test is loaded, and the run closes only after the test passes.

- **Wild: solve playbook routing like a crossword** — FEATURE — value 2 — effort L — risk med — category: routing
  Why: Each request leaves constraints (language, file types, tools) that cut the catalog down, and propagating them narrows the candidates without scanning each entry. Assumption: the playbook metadata carries enough constraints to propagate.
  Done when: A fixture catalog of 1,000 entries routes to the same single match as the full scan, in under a tenth of the scan's time.
