# Brainstorm — lens: approaches

- **Make every finish sentence cite a proof id or be stamped unproven** — FEATURE — value 5 — effort M — risk low — category: user value
  Why: assumption: the weak point is the agent's closing report, not the tests. Cheapest approach, no new tooling: split the finish message into claims, match each to a `fm task prove`, `fm shot` or `fm flow` record, and auto-label the rest "unproven: no evidence".
  Done when: a finish message with one uncited claim is rendered with that claim marked unproven, and a test asserts the marker.

- **Execute the docs in a scratch copy** — FEATURE — value 5 — effort M — risk low — category: docs
  Why: the request lists "docs against code", and the README/MASTER carry many literal commands, flags and numbers. Approach: extract fenced commands and `fm VERB --flag` mentions, run them in a throwaway clone, and flag any that exit non-zero or are unknown flags. Trade-off: it only proves commands, not prose claims.
  Done when: renaming a flag in code turns a doc line red naming file:line, and a doc with a non-runnable example is labelled unproven (not red).

- **Give each proof kind an unproven reason code and an owner** — FEATURE — value 4 — effort S — risk low — category: observability
  Why: "whatever can't be proven gets labelled" needs a closed vocabulary. Proposed codes: needs-secret, needs-device, needs-human-eyes, no-tool-installed, nondeterministic. Each unproven item names who or what could close it, and they feed the existing user-only list.
  Done when: `fm task finish` prints unproven items grouped by reason code, and an item with no valid code is refused.

- **Snapshot the accessibility tree beside the pixels in `fm shot`** — FEATURE — value 4 — effort M — risk med — category: ui
  Why: pixel diffs flake on fonts and animation, while a role/name/state tree is stable and diffable text. Reuse the browser's own a11y snapshot, and fall back to pixels only for visual-only claims. Trade-off: it misses pure styling bugs.
  Done when: a flow run stores a tree file, and a deliberately removed button label fails the diff with the element named.

- **Probe each proof's sensitivity by planting a break** — FEATURE — value 4 — effort M — risk low — category: reliability
  Why: a UI, data or perf check that passes proves nothing unless it can fail. Approach: for each non-unit proof, apply a tiny scripted break (hide an element, drop a row, add 50 ms) in a scratch tree and require the check to flag it. A check that stays green is labelled "insensitive". This extends the existing red-first idea past unit tests.
  Done when: a flow with no assertions is reported insensitive.

- **Run the data proof as invariants on a copy, before and after** — FEATURE — value 4 — effort M — risk med — category: data
  Why: assumption: data changes today are proven by whatever tests exist. Approach: reuse SQLite or `csvkit`-class tools to compute counts, null rates, key uniqueness and checksums of untouched columns on a copy, then diff. Trade-off: invariants must be declared per task, so ship a default set (row count, schema, orphan keys).
  Done when: a migration that silently drops rows fails with the count delta.

- **Verify infra with each tool's own offline checker** — FEATURE — value 3 — effort M — risk low — category: infra
  Why: don't build infra verification. Map stack cards to existing dry-runs (`systemd-analyze verify`, `nginx -t`, `docker build --check`, `terraform validate`, `shellcheck`). If the tool is absent, the claim is labelled unproven: no-tool-installed, and the install is queued.
  Done when: a broken unit file fails the proof, and a machine without the checker yields the label rather than a pass.

- **Prove perf claims by interleaved A/B and say "inconclusive" when noise wins** — PERFORMANCE — value 4 — effort M — risk low — category: performance
  Why: a recent commit (T-2605) shows the self-change gate was fooled by noise. Approach: run base and head alternately from two worktrees, report median and spread, and refuse a "faster" claim when the effect is smaller than the spread.
  Done when: a 2% change under 10% noise prints inconclusive, not faster.

- **Scrub proof artifacts before they are stored or published** — SECURITY — value 3 — effort M — risk med — category: privacy
  Why: assumption: screenshots, flow transcripts and shot diffs can capture tokens, emails or home paths, and `fm genesis live` publishes to the site. Approach: run fixtures-only data for UI flows where possible, and otherwise scan text artifacts and OCR images for known secret shapes before keeping them.
  Done when: a planted fake token in a page makes the shot fail to save with the reason.

- **Wild: Let a docs-only child try the product in a sandbox** — FEATURE — value 4 — effort L — risk med — category: docs
  Why (wild): a tool-less reader can't act, so give a sandboxed child the README and nothing else, and ask it to perform three tasks. Every point where it gets stuck is a doc-versus-code mismatch no grep finds.
  Done when: a README with a wrong flag yields a stuck report quoting the step.

- **Wild: Ship runtime tripwire assertions as proof from real use** — FEATURE — value 3 — effort L — risk med — category: reliability
  Why (wild): some claims ("works with real data") can't be proven in a test. Let a task add a one-time `fm witness` line that records the first real execution of the claimed path, so the claim moves from unproven to witnessed once the user actually uses it.
  Done when: an unproven claim flips to witnessed with a timestamp after the path first runs.

- **Wild: Show three observed outputs and ask a one-word "surprised?"** — FEATURE — value 3 — effort S — risk low — category: user value
  Why (wild): "does it do what the user meant" is the one claim no tool proves. Rather than a long review, show three concrete before/after examples drawn from the request's own nouns, get yes or no, and record the answer as the intent proof (or leave it unproven if unanswered).
  Done when: the finish card carries intent: confirmed by user or intent: unproven.

Next question: Which past tasks did the user reopen after a finish that had all proofs green, and which proof kind would have caught each?
Next question: Which of these proof kinds can run with no `claude` on PATH and no browser installed, and what does each print in that case?
