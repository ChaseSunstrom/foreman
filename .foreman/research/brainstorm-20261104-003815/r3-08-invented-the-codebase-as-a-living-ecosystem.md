# Brainstorm — lens: invented: the codebase as a living ecosystem

- **Select Ward rules by thymic negative selection** — SECURITY — value 4 — effort M — risk low — category: Ward
  Why: the pack tracks retry-after-block rate and wants "tighten-only" tuning, but no adoption gate measures false blocks before a rule ships. Assumption: the user's shell and tool history is available locally.
  Done when: a candidate Ward rule that fires on any command in the user's last-90-day local history is rejected, and `sampo doctor` prints the count of rules that passed.

- **Pin local model weights by digest** — SECURITY — value 4 — effort S — risk low — category: supply chain
  Why: install.sh now offers opt-in Ollama with embedding models (qwen3-embedding, bge-m3, nomic-embed-text) and a reranker, and the pack lists "local model weights" as footprint. Assumption: pulls are by tag today.
  Done when: a pull whose digest isn't in a committed pin table is refused, and a test swaps a tag's digest and sees the refusal.

- **Fence the uncensored model as data-only** — SECURITY — value 4 — effort S — risk low — category: trophic fence
  Why: the user steered Small-model uplift toward the uncensored variant "for ideas at any volume". Assumption: `models.generate` output can reach prompts or commands today with no type distinction.
  Done when: output tagged `untrusted-model` can't be passed to a command-running path, and a test where it embeds `rm -rf` fails closed.

- **Add an allelopathy screen between lanes** — SECURITY — value 3 — effort M — risk med — category: injection
  Why: T-0791 (injection and supply-chain defenses, 18 ideas) is deferred. Lanes read each other's artifacts and briefs, and a poisoned lane output would act on its neighbours. Assumption: briefs and evidence files are read raw.
  Done when: cross-lane artifacts are read through a tagged, instruction-stripped view, and a planted "ignore previous" line in a lane file isn't obeyed by a reading lane.

- **Generate Ward fixtures from the verb table** — SECURITY — value 4 — effort M — risk low — category: attack surface
  Why: each new verb that runs commands or writes outside the tree adds surface. The ideas so far cover alias-map fixtures but not per-verb coverage. Assumption: a verb table is enumerable from cli.py.
  Done when: CI fails if any verb marked "executes or writes outside repo" lacks at least one Ward block fixture.

- **Run the hook path as a pre-forked zygote** — PERFORMANCE — value 4 — effort L — risk high — category: hook latency
  Why: the gates run `bench_hooks.py --runs 20`, and the ideas list a "shim import tax" with no fix. A warm interpreter on a per-user socket would skip startup. Assumption: Python startup dominates hook time.
  Done when: bench_hooks shows median hook latency at least 50% lower with the zygote on. If the zygote is dead, hooks fall back to cold start with the same verdicts, and the socket accepts only the same uid.

- **Give each hook event an import niche** — PERFORMANCE — value 3 — effort S — risk low — category: hook latency
  Why: the shims moved code to `plugin/lib/sampo/`, so hook imports could have grown unseen. Assumption: some events import the whole CLI.
  Done when: `python -X importtime` per event is recorded with a module whitelist per event, and ship fails when an event imports a module outside its niche.

- **Coalesce embeddings across lanes in a pollinator broker** — PERFORMANCE — value 4 — effort M — risk med — category: moons at scale
  Why: Moonscale runs `models.embed` over 10,000 candidates, and several lanes may embed at once on one local endpoint where a model switch costs about 3 minutes. Assumption: calls are made one lane at a time.
  Done when: N concurrent embed callers are batched into fewer endpoint requests, with results identical to the unbatched path and throughput measured on 10,000 shingles.

- **Reorder funnel stages by kills per cost, as an optimal forager would** — PERFORMANCE — value 4 — effort S — risk low — category: funnel
  Why: the funnel is "cheapest first" by fixed design. The ideas so far log unique kills per stage but never reorder on them. Assumption: stage cost and kill counts are in the funnel log.
  Done when: a stage with a higher kills-per-second rate runs first on the next batch, and total funnel seconds on a replayed 10,000 drop versus the fixed order.

- **Back the drive off with a torpor curve** — PERFORMANCE — value 3 — effort S — risk low — category: drive
  Why: T-2873, T-2900 and T-2901 show the drive re-pushing or mis-waiting on an unchanged running set. Assumption: an idle wait still polls at a fixed interval.
  Done when: with an unchanged running set the wake interval grows geometrically to a cap and resets on any change. A replayed 45-minute builder wait causes fewer than 5 pushes.

- **Wild: plant sentinel chickens in every lane HOME** — SECURITY — value 4 — effort M — risk low — category: honeytokens
  Why: lanes and the uncensored model run unattended, and nothing detects credential-hunting. Assumption: lane HOME can be a scratch directory. wild
  Done when: a fake `~/.aws/credentials` in a lane HOME trips a Ward alarm and `sampo next` line when any command reads it, while normal lane work never touches it.

- **Wild: measure the R0 of a poisoned lesson** — SECURITY — value 3 — effort M — risk low — category: epidemiology
  Why: T-0217 gives lessons a confidence that rises on recall, and the ideas cover a mycorrhizal lesson network. None measures how far one false lesson spreads. Assumption: lessons are recalled by similarity. wild
  Done when: a planted bad lesson run through a replayed week of sessions yields a measured R0 (new tasks it misleads per carrier), with a ship gate that fails at R0 ≥ 1.

- **Wild: order Done-when proofs like a slime mould** — PERFORMANCE — value 3 — effort M — risk low — category: proof scheduling
  Why: long Done-when proof lists run in written order, so a cheap failing proof can sit behind slow ones. Assumption: history has pass, fail and seconds per proof. wild
  Done when: proofs run in descending fail-probability per second. On a replayed set, time to the first failure drops, and a green run's verdict is unchanged.

Next question: Which hook or lane path would a hostile local-model output reach a shell through without crossing the Ward?
Next question: What is the real split of hook time between interpreter start, imports and work, per event, under four parallel lanes?
