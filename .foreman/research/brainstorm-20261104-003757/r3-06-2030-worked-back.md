# Brainstorm — lens: 2030 worked back

- **Count interruptions avoided per tool** — FEATURE — value 4 — effort S — risk low — category: user value
  Why: the standing steers say "stop asking me for stuff, keep going" and "never interrupt the user mid-run". No idea so far prices an acquired tool in the unit the user cares about. Calls and saves are covered, but not asks avoided.
  Done when: `sampo tool stats` lists each tool with the number of fm ask or install prompts a replayed gap transcript no longer raises, and a tool with zero over 30 days is flagged.

- **Turn each Ward refusal of a legitimate intent into a safe-equivalent tool gap** — FEATURE — value 4 — effort M — risk med — category: security
  Why: the Ward blocks commands, and the agent then improvises around the block. Refusal-to-gap is not in the lists, and rm → `prune --plan` is only one hand-picked case.
  Done when: a blocked-then-retried command pair in the ledger files a gap record naming the intent. A built safe tool then makes the same intent pass the Ward without a rule change.

- **Write a standing grant policy the user authors once** — FEATURE — value 5 — effort M — risk med — category: security
  Why: grant lists so far are expiring, batched and hash-pinned, but each one still reaches the user. By 2030 the queue is hundreds of items long. Assumption: the user prefers one rule ("stdlib-only, no network, under 200 lines, Ward-clean") to approving every item.
  Done when: a policy file auto-satisfies a matching grant with a receipt. A non-matching grant still queues, and the Ward exam fails if the policy can widen itself.

- **Forecast breakage on future runtimes** — PERFORMANCE — value 3 — effort S — risk low — category: reliability
  Why: forged tools are mostly Python and shell. Prior ideas mention stdlib removals only for the hook path, not for the shelf.
  Done when: a weekly lane runs every shelf tool's own test under the newest pre-release interpreter with `-W error`. It lists the tools that would break and the deprecation each one hits.

- **Probe networked tools for liveness and cache "nothing exists" results with an expiry** — FIX — value 3 — effort S — risk low — category: reliability
  Why: assumption: registry entries and APIs die over four years, and each session otherwise rediscovers that by failing. A negative-search cache with a TTL also stops repeated fruitless searches.
  Done when: a dead endpoint marks its tool "stale" before a session picks it. A repeat search for the same gap within the TTL reads the cache, and the cache is bypassed when the registry hash changes.

- **Give forged tools a fixed error grammar a 4B can act on** — FEATURE — value 4 — effort S — risk low — category: small models
  Why: the steer is to make small models match frontier through scaffolding. Cards and passports cover how to call a tool but not how to recover from its failures, which is where small models stall (assumption).
  Done when: every shelf tool prints failures as `ERR code | cause | next: <one command>`. A lint fails a tool that doesn't, and the 4B recovers from planted failures more often with the grammar than without.

- **Pin a frozen frontier reference set so the claim doesn't chase a moving baseline** — FEATURE — value 4 — effort M — risk low — category: measurement
  Why: "match frontier results" is judged against a model that changes under the same name. A parity curve compared with a drifting reference measures nothing.
  Done when: each exam scenario stores the reference transcript, model id and date. A later local-model run is scored against that frozen copy, and the report says which reference vintage it used.

- **Lock the weights the claims were measured on** — SECURITY — value 3 — effort S — risk low — category: reproducibility
  Why: the exam records name profiles ("qwen3.8-27b"), not file hashes. A silent re-quantise or a removed upload would make old lift numbers unreproducible. Assumption: the endpoint serves GGUF files.
  Done when: each exam arm record carries the weights hash and size. `sampo doctor` flags a card whose measured weights no longer match the served ones, and marks its lift "stale".

- **Shadow a forged tool against the host-native feature on real calls** — PERFORMANCE — value 4 — effort M — risk med — category: retirement
  Why: bake-off and native-replacement ideas run once on fixtures. Real inputs are what show when the host has caught up.
  Done when: for N real invocations both paths run and their outputs are compared. After enough agreement the tool is auto-demoted to "retire proposed" with the diff history attached.

- **Put tool search behind a resolver interface with cassette contract tests** — CLEAN — value 3 — effort M — risk low — category: developer experience
  Why: registry APIs and MCP discovery will change by 2030. A pluggable resolver keeps the find step from rotting, and recorded responses catch protocol drift offline.
  Done when: each search backend implements one `resolve(need)` contract. Replaying its cassette passes in CI, and swapping the backend changes no caller.

- **Wild: write the spec and tests now, forge at the next model upgrade** — FEATURE — value 4 — effort M — risk low — category: agents
  Why: assumption: models in 2030 are much stronger and cheaper. A gap the 4B can't forge today still has a cheap, exact spec. Parked specs make the next model generation start with finished exam questions.
  Done when: `sampo gap park` stores a spec, tests and a passport stub. After a model change a lane forges every parked gap and reports which now pass.

- **Wild: forecast next quarter's gaps from stack release notes and ledger history** — FEATURE — value 3 — effort L — risk med — category: capability
  Why: the pre-build idea starts from the current manifest. Reading what host and stack releases are about to change goes one step further and can be scored against the gaps that actually arrive.
  Done when: a weekly forecast lists predicted gaps with a confidence. The next quarter's real gap records settle each one, and the hit rate is printed.

- **Wild: ship a public-safe starter shelf distilled from the user's own** — SECURITY — value 3 — effort M — risk med — category: privacy
  Why: the shelf is built from private repos' failures. A tool-less cold child can check that a distilled copy leaks no paths, names or machines before any other user or harness receives it.
  Done when: the export contains only tools whose originating gap text is rewritten and scanned, and a blind reader fails to name the owner, machine or repo from it.

Next question: if a stranger inherits the shelf in 2030 with no ledger, which tools can they still tell are safe to run, and what proves it?
Next question: which acquired tool would the user notice missing first, and does anything record that it fired?
