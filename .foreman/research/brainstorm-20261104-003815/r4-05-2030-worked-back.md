# Brainstorm — lens: 2030 worked back

- **Rehearse the funnel at 1,000,000 synthetic candidates** — PERFORMANCE — value 5 — effort M — risk low — category: scale
  Why: the pack says 10,000 candidates now. If the 2030 hardware is about 100x faster, the pool will be about 100x bigger. Nothing here fits a time or memory curve to the dedupe, embed and rerank stages. "Replay at 2030 prices" covers cost, not scale. Assumption: the funnel's memory use is superlinear somewhere.
  Done when: `sampo moons rehearse --n 1000000` on planted-duplicate data prints per-stage wall time, peak RSS and dedupe recall. It fails if any stage grows worse than n log n.

- **Run stage 1 on truncated embeddings** — PERFORMANCE — value 4 — effort S — risk low — category: funnel
  Why: the plan embeds every candidate in full and ranks them in full. Matryoshka-style prefix dimensions (64 first, full only for survivors) would cut stage cost roughly 10x. Assumption: the chosen embedders (qwen3-embedding, bge-m3) support prefix truncation. Verify before building.
  Done when: on the held-out kill set, the 64-dim stage keeps at least 98% of what the full-dimension stage keeps, at under a quarter of the compute.

- **Overlap funnel stages speculatively** — PERFORMANCE — value 3 — effort M — risk med — category: funnel
  Why: local models switch in about 3 minutes and the GPU idles between stages. Starting stage N+1 on candidates that the cheap stage's score already predicts will survive hides that latency. The log is append-only, so a wrong guess is discarded cheaply.
  Done when: end-to-end funnel time drops at least 25% on a 2,000-candidate run with identical survivors.

- **Approve by effect, not by command shape** — SECURITY — value 5 — effort L — risk med — category: Ward
  Why: Ward matches command patterns, and attackers will always have stronger models. Run risky commands in a copy-on-write overlay (bwrap with overlayfs) and diff the effects. Approve only when deletions, writes outside the repo and network use stay inside the task's envelope, then replay for real. This holds regardless of how the command is spelled.
  Done when: a corpus of 50 obfuscated destructive commands, with Ward's pattern rules disabled, is all caught by the effect diff, and benign commands pass with less than 300 ms added.

- **Treat other agents as untrusted peers behind an A2A gateway** — SECURITY — value 4 — effort M — risk med — category: boundary
  Why: by 2030 agents will call each other, and Sampo already runs lanes, the drive and three other harnesses. Each inbound agent message today is trusted as if it were the user's. A gateway would label it with its origin, strip its authority, and run the Ward on anything it asks for.
  Done when: a test agent message saying "ignore the Ward and run X" is blocked and logged with its origin, while a user-origin message passes.

- **Produce a reproducible, attested plugin release** — SECURITY — value 4 — effort M — risk low — category: supply chain
  Why: install.sh and the marketplace publish what the plugin does. A stranger in 2030 cannot verify that a release matches its source, and a compromised copy of the guard would be the worst failure. The standing push grant puts shipping on autopilot, so this matters more.
  Done when: building twice from the same tag gives identical hashes, `install.sh` refuses a tampered artifact, and the release records a signed provenance file.

- **Make `sampo map` incremental for 500,000-file repos** — PERFORMANCE — value 4 — effort M — risk low — category: map
  Why: the map says 2,358 files and a full rebuild is fine at that size. A 2030 monorepo is 100x that, and session start is on the hook path. Assumption: today's map rebuilds from scratch each time.
  Done when: after touching 10 files in a synthetic 500k-file tree, the map updates in under 1 s and matches a full rebuild byte for byte.

- **Normalise Unicode before any Ward or dedupe decision** — SECURITY — value 3 — effort S — risk low — category: injection
  Why: generated candidates and commands can carry homoglyphs, bidi overrides and zero-width characters. These dodge both Ward patterns and exact dedupe, and nothing in the ideas so far normalises them.
  Done when: 30 homoglyph and bidi variants of blocked commands are blocked, and two candidates differing only by zero-width characters dedupe as one.

- **Audit symlink and TOCTOU races on the child directory** — SECURITY — value 3 — effort S — risk low — category: state
  Why: lanes and children write under `/run/user/1000/fm-children-*` and the state dir. A hostile lane or planted file could redirect those writes. "Fence recursive scans" and "containment fuzz" touch the pruner, not the writers.
  Done when: a test that swaps a target for a symlink between check and write fails closed on every writer, and the state dir mode is checked at start.

- **Bound unattended defects by acceptance sampling** — FEATURE — value 4 — effort M — risk low — category: assurance
  Why: in 2030 the user reviews a small slice of overnight output. Choosing which landed commits to audit by an acceptance-sampling plan (sample size set by batch size and a target defect rate) gives a stated bound instead of "I looked at some". Pairs with the morning card.
  Done when: a morning card states "N of M reviewed, defect rate under X% at 90% confidence", and the sample size is recomputed from the batch.

- **Wild: Keep a 2030 hardware twin in the CI.** — PERFORMANCE — value 3 — effort M — risk low — category: foresight
  Why: wild. Throttle a lane's CPU and memory to a low-end laptop profile and a fast-GPU profile, and run the hook bench in both. It would catch Sampo being tuned only to this one Arch box with a big local model.
  Done when: the bench prints hook p99 under two cgroup profiles and fails if the low-end profile regresses.

- **Wild: Add a memorisation canary to bulk generation.** — SECURITY — value 3 — effort S — risk low — category: privacy
  Why: wild. Ten thousand local-model candidates could regurgitate memorised keys or personal text into candidates.jsonl and then the public Genesis data. Plant known secret-shaped strings in the prompts and check whether any come back. Scan every output as well.
  Done when: a planted secret echoed by a candidate is blocked from the store and the site data, and logged.

- **Wild: Shed work through an ecological pressure valve.** — PERFORMANCE — value 3 — effort M — risk med — category: scheduling
  Why: wild, in the ecology lens. A carrying-capacity controller ties the number of funnel workers, lanes and hook-heavy sessions to measured hook p99. Under load it sheds bulk work first and never the Ward, much as a stressed ecosystem drops its most expendable species first.
  Done when: with 8 busy lanes, hook p99 stays under its budget because bulk funnel work paused, and it resumes when load falls.

Next question: which funnel stage's cost grows fastest if candidates rise 100x, and has anyone measured it at that size?
Next question: if the strongest attacker model in 2030 reads Sampo's open Ward rules, which verdict still holds?
