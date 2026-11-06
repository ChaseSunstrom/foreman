# Brainstorm — lens: approaches

- **Lint finishes against past false dones** — FEATURE — value 4 — effort S — risk low — category: false-done
  Why: T-2613 now splits exam false dones into name-only and real, and each failed check keeps its line and class. That is an unused labelled corpus of how Foreman has lied. Reusing it needs no new prover.
  Done when: a finish text built from a recorded false-done pattern is flagged with that class name, and 0 of the last 20 real passing finishes are flagged.

- **Query one world snapshot instead of writing a prover per claim** — FEATURE — value 4 — effort L — risk med — category: unified-proof
  Why: the pack has many one-off provers (surface diff, "prove what did not change", trace of touched files, residue). One before/after snapshot (tree hashes, listening ports, processes, schema dump, route list, `--help` output) turns each claim into a query over the diff. Assumption: a snapshot stays cheap and deterministic enough to diff.
  Done when: on a fixture repo, "no new listening port" and "schema unchanged" both resolve from the same two snapshots, and a planted extra port turns the first red.

- **Count instructions, not seconds, for perf claims** — PERFORMANCE — value 4 — effort M — risk med — category: performance
  Why: T-2605 shows the wall-time gate flaked and needed a median on a loaded bench. Instruction counts (`perf stat` or cachegrind) are nearly noise-free, so the noise-floor and A/B machinery isn't needed for most claims. Risk: a hardened kernel may restrict `perf_event_paranoid`, so valgrind is the fallback.
  Done when: two runs of one command differ by under 1% in count, a planted extra loop shows over 5%, and a host with neither tool gets "unproven: no counter".

- **Run the repo's own CI steps as the prover pack** — FEATURE — value 4 — effort M — risk med — category: reuse
  Why: this repo has a `test.yml` badge, and users' repos likely have workflows. Reusing their `run:` steps (via `act` or a parser) in a scratch copy adds provers without writing any. Assumption: most of those steps run offline.
  Done when: on a fixture repo with a workflow, each step is recorded as a proof with its exit code, and a step needing secrets or network is labelled unproven.

- **Add an HTML-only tier below `fm shot`** — FEATURE — value 3 — effort S — risk low — category: do-less
  Why: the surface is `plugin/templates/web/index.html`. Many UI claims (text, state, element present) don't need a browser. Fetch the page, assert on selectors, and stamp "layout not proven".
  Done when: a text-and-state claim on the local web UI is proven in under 1s with no browser launched, and a layout claim on the same page is still labelled unproven.

- **Decide flaky proofs sequentially** — FIX — value 3 — effort M — risk low — category: flake
  Why: the LeanKind flake and the waiting hook (T-2605, T-2606) show that fixed-N reruns are either wasteful or unsure. A sequential test reruns until it can call the result.
  Done when: a command that fails 10% of the time ends as "flaky-pass" within a run cap, and a stable command stops after 3 runs.

- **Probe expiry clocks** (certs, tokens, domains, licences in config) — FEATURE — value 3 — effort S — risk low — category: ops
  Why: assumption: ops claims like "deployed and fine" silently depend on things that lapse. The request names infra and ops, and this is a cheap read-only check.
  Done when: a fixture with a self-signed cert expiring in 5 days reports "expires in 5d", and a host with no network reports unproven for the remote ones.

- **Use the repo's type checker as a proof tier on touched files** — FEATURE — value 3 — effort S — risk low — category: static-proof
  Why: stack cards (python, tailwind) show Foreman knows the toolchain. A checker limited to the diff is a cheap, deterministic prover. It must never install one.
  Done when: "no type errors in touched files" is proven from the configured checker, and a repo with none gets "unproven: no checker configured".

- **Walk the web UI by keyboard in `fm flow`** — FEATURE — value 3 — effort M — risk low — category: ui
  Why: the foreman-ui work shows keyboard parity matters. A Tab traversal asserting reachability and visible focus is a different failure class from pixels or axe.
  Done when: a fixture page with one unreachable button makes the flow fail naming that element.

- **Rehearse infra on a throwaway local target** (compose, kind) — FEATURE — value 2 — effort L — risk med — category: ops
  Why: dry-run and lint prove syntax, not that the thing comes up. Assumption: the user's machine can run containers.
  Done when: a fixture manifest with a bad image reference fails at rollout inside the throwaway target, and the target is gone afterwards.

- **Predict the output, then run it, and score the surprise** — FEATURE — wild — value 3 — effort M — risk low — category: calibration
  Why: wild. Before any verify command the builder writes the output it expects. Mismatch is a stronger signal than pass or fail, and it feeds the existing bets ledger.
  Done when: a verify run with a recorded prediction stores a match or mismatch, and `fm outcomes` splits Brier by it.

- **Count the user's own clicking as proof** — FEATURE — wild — value 4 — effort L — risk med — category: live-coverage
  Why: wild. A dev build exposes which changed lines ran since boot. When the user pokes the app, each exercised claim lights up as human-witnessed, which fits "does it do what the user meant".
  Done when: after a scripted session touching one of two changed handlers, the claim for that handler reads witnessed and the other stays unproven.

- **Plant a conscience test for unwitnessed claims** — FEATURE — wild — value 2 — effort S — risk med — category: unproven
  Why: wild. Each unproven claim leaves a dated test in the user's repo that fails loudly after N days unless a human witness is recorded. Risk: it breaks the user's CI, so it needs opt-in.
  Done when: a claim with no witness fails the generated test after its date, and recording a witness turns it green.

Next question: Which proof kind has actually changed a decision for the user, and which has only produced receipts they never read?
Next question: Which of these provers need a tool the user's machine lacks, and what should Foreman do then: label unproven, ask once with `fm ask`, or degrade?
