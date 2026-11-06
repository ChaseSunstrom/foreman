# Brainstorm — lens: bold bets

- **Replace the Python hook path with a static native binary** — PERFORMANCE — value 5 — effort L — risk med — category: hooks
  Why: The pack's tracked pain is per-turn hook cost and import tax. Earlier ideas (zygote, warm daemon, prefilter) all stay in Python. Assumption: a Go or Rust Ward and dispatcher can reach about 1–2 ms with no daemon to babysit.
  Done when: for a week, the binary and the Python Ward both see replayed real hook payloads with zero verdict diffs, and `bench_hooks.py` p99 is at least 10x lower.

- **Pre-clear the plan's commands at plan time** — PERFORMANCE — value 4 — effort M — risk med — category: Ward
  Why: Sampo plans before it edits, so the commands are mostly known early. Assumption: plan steps can name their commands. Verdicts are computed once at plan approval and stored by rules hash, so the live hook becomes a lookup and bad plans fail before any edit.
  Done when: a plan listing a refused command is rejected at approval, and a pre-cleared command costs under 1 ms on the hook path.

- **Make the Ward taint-aware** — SECURITY — value 5 — effort L — risk med — category: injection
  Why: There are many injection-defense and biomagnification ideas, but none enforce anything. Text from web pages, tool results and local-model output carries a taint tag. A command whose arguments derive from tainted text needs the stricter rule set.
  Done when: a planted instruction in a fetched page that makes the agent run a borderline command is blocked, while the same command from the user's typed prompt passes.

- **Model-check the Ward's rule set** — SECURITY — value 4 — effort L — risk low — category: assurance
  Why: Ward tests are examples, not proofs. Compile the rules to an automaton and check bounded properties against a shell-grammar subset, such as "no accepted string writes a protected path". Assumption: the rules fit a bounded model of the shell grammar.
  Done when: CI runs the property check, and a mutated rule that opens a path makes it fail with a counterexample string.

- **Sign user-only grants in one touch** — SECURITY — value 3 — effort M — risk med — category: grants
  Why: The standing rules say anything only the user can grant waits in the final report and never interrupts. Add a single passkey (WebAuthn) touch in the web UI that signs the whole batch, with per-item expiry. The agent cannot mint these tokens.
  Done when: a protected-core edit and a merge each refuse to run without a valid signed token, and one touch clears the full batch.

- **Run the funnel as a sequential probability ratio test** — PERFORMANCE — value 4 — effort M — risk low — category: funnel
  Why: Moons at scale means 10,000 candidates through cheap-first stages. Instead of fixed judge calls per stage, each candidate gets calls one at a time until its likelihood ratio crosses accept or reject. Assumption: the judges' agreement rates can be estimated from the kill log.
  Done when: on 10,000 candidates, judge calls drop at least 40% versus fixed stages, with unchanged agreement on a held-out labelled sample.

- **Find the batching knee of the local endpoint** — PERFORMANCE — value 4 — effort S — risk low — category: local models
  Why: Bulk work runs on a llama-swap endpoint where a model switch costs about 3 minutes, but nothing here measures parallel-slot throughput. Sweep concurrency from 1 to 16 and set funnel concurrency at the knee.
  Done when: the bench prints tokens per second versus concurrency, and a 10,000-candidate dry run finishes in a stated time at the chosen setting.

- **Scale the candidate store to 10,000 and beyond** — PERFORMANCE — value 3 — effort M — risk low — category: storage
  Why: `candidates.jsonl` plus an append-only funnel log was built at small scale. Add segment files with a sparse index and memory-mapped embeddings. Cold dedupe and lookup should stay flat.
  Done when: a synthetic 100,000-row store answers a candidate lookup in under 50 ms cold and stays under a set RAM ceiling.

- **Sample verifier re-checks at the herd-immunity rate** — SECURITY — value 3 — effort M — risk med — category: lanes
  Why: Lanes pass work to each other, so one poisoned artifact can spread. Estimate a poison's reproduction rate from planted decoys, then set the fraction of outputs given an independent re-check so that rate stays below 1 (the epidemiological herd-immunity threshold).
  Done when: a planted poison seeded into one lane never reaches main across 50 simulated runs, at a re-check rate under 30%.

- **Cap transmission hops on lessons, drafts and self-edits** — SECURITY — value 4 — effort M — risk low — category: provenance — wild
  Why: assumption: a mislearned lesson spreads like a prion, since a lesson built on a lesson converts others. Each artifact carries a hop count and a root-evidence pointer. After 2 hops without a human or a passing exam touching it, it goes inert.
  Done when: a lesson derived from another lesson without a root ledger fact is refused at recall, and the refusal is listed in `doctor`.

- **Shard the funnel across the user's other machines** — PERFORMANCE — value 3 — effort L — risk med — category: estate — wild
  Why: The estate file idea already joins machines and models. Idle machines pull funnel shards by content hash over a local-only channel, so 10,000 candidates finish overnight on hardware the user already owns. Assumption: there is a second machine or GPU. Nothing leaves the user's network.
  Done when: two machines split a 2,000-candidate run, and the merged log is identical in verdicts to a single-machine run.

- **Give each lane a programmed self-destruct** — SECURITY — value 4 — effort M — risk low — category: lanes — wild
  Why: Lane controls today are fences and leases. A lane dies when it breaks its own contract: a Ward hit, a write outside its declared file set, or a budget breach. Its uncommitted writes are wiped and a corpse report goes to the parent.
  Done when: a lane that writes outside its declared files is killed, its worktree is clean, and `fm next` shows one corpse-report line.

- **Race the tower against a frozen seed lineage** — SECURITY — value 3 — effort L — risk med — category: drift — wild
  Why: Self-edits can each pass the gates while jointly eroding guard behavior, which is the ratchet-style drift that single-edit gates miss. Assumption: a sealed gen-0 copy exists to compare against. A nightly replay of the guard exam on both lineages flags any drift in verdicts that the current gates did not predict.
  Done when: a planted cumulative drift of 5 small edits is caught by the nightly diff while each individual edit passes its own gate.

Next question: Which of these ideas needs no new verb and can be switched on purely by an existing session path, given the rule that every capability must be reached from a real session path?
Next question: How many of the 10,000 moons would a bare model also produce, and does the cheap-first funnel measure that before spending any judge calls?
