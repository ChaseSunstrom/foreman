# Brainstorm — lens: 2030 worked back

**Lens note:** I read "2030 worked back" as: assume hosts ship native tool discovery, models build tools on the fly, and small models are strong. Then ask what Mission 7 must be today so it survives that. Assumptions are marked.

- **Treat forged tools as spec plus tests, with code as a regenerable cache** — FEATURE — value 5 — effort M — risk med — category: tool forge
  Why: assumption: by 2030 a stronger model writes better code from the same spec, and the earlier notes already say "acquired tools need retire-when". The durable asset is the contract, not the script.
  Done when: `sampo tools regen NAME` rebuilds a forged tool from its spec and tests alone, and the tool is replaced only if the tests pass and the new version is no larger.

- **Derive least-privilege sandbox profiles by tracing the tool's own test run** — SECURITY — value 5 — effort M — risk med — category: quarantine
  Why: the pack's quarantine ideas say "trial in a cage" but not how the cage is sized. This machine runs a hardened kernel, so Landlock or bubblewrap is plausible. Assumption: tests exercise the real paths.
  Done when: a tool's manifest lists the filesystem paths and network hosts observed in its tests, and a call touching anything else is refused in a test.

- **Keep a Wanted board of failing tests that name tools nobody has built yet** — FEATURE — value 4 — effort S — risk low — category: gap ledger
  Why: gap records exist as an idea, but nothing says a later, stronger model or another user can fill a gap. A wish is a red acceptance test plus a one-line need.
  Done when: `WANTED/` holds at least 5 machine-readable entries, and one is closed by a build whose test turns green.

- **Pin the MCP protocol version and run a nightly conformance check on built servers** — PERFORMANCE — value 4 — effort S — risk low — category: protocol drift
  Why: `plugin/templates/mcp-server/test_server.py` exists, so the template is the natural place. Spec drift is the most likely silent break by 2030.
  Done when: a nightly run exercises each built MCP server with a reference client at the pinned version, and names the failing server.

- **Add a license and provenance ledger for every found or vendored tool** — SECURITY — value 4 — effort S — risk low — category: supply chain
  Why: the pack covers hash-pinning and maintainer change but not licenses. The rea source shows MIT checks are done by hand. Assumption: Sampo's own distribution makes this a ship concern.
  Done when: `sampo doctor` lists each acquired tool with its license, and an unknown or incompatible license blocks promotion.

- **Record tool-call traces from forged-tool runs as a local dataset for the small-model adapters** — FEATURE — value 4 — effort M — risk med — category: small models
  Why: the standing steer is to make 4B/9B/27B models match frontier results. Tool-use traces (need, call, result, verdict) are exactly what the small decision models lack. Assumption: the traces are redacted and kept local.
  Done when: a trace file with at least 200 redacted, verdict-labelled calls exists and feeds one exam arm.

- **Measure gap-to-usable-tool time and publish the trend** — PERFORMANCE — value 3 — effort S — risk low — category: observability
  Why: nothing in the pack says how long the lack-a-tool loop takes. A falling curve is the 2030 proof that Mission 7 works.
  Done when: each acquisition logs start, quarantine pass and first real-path use, and the web UI shows the median per week.

- **Record-replay cassettes for tool tests** — CLEAN — value 3 — effort M — risk low — category: test reliability
  Why: tools that call the network cannot be tested offline or in 2030 when endpoints are gone. Cassettes make tests deterministic.
  Done when: a forged network tool passes its tests with the network disabled, using stored cassettes.

- **Wild: Run a recurring supply-chain fire drill against the quarantine** — SECURITY — value 4 — effort M — risk low — category: red team
  Why: assumption: quarantines rot unnoticed. A cold child plants a malicious update in a scratch tool, and the drill passes only if the quarantine catches it.
  Done when: the drill runs on a scratch tool, and a planted exfiltration attempt is blocked and reported with the rule that caught it. wild

- **Wild: Write a time capsule of the tools Sampo wishes existed, sealed by hash and re-opened at each model upgrade** — FEATURE — value 3 — effort S — risk low — category: forecasting
  Why: pairs with the Wanted board. Each generation seals its top 10 wished-for tools, and a new model is scored on how many it can now build.
  Done when: a sealed file exists, and a later run scores a new model against it. wild

- **Wild: Hold a build-off between the 27B and a frontier model on the same Wanted entry, and let the entry's own tests judge** — PERFORMANCE — value 4 — effort M — risk low — category: exam arm
  Why: it is the cheapest honest test of the "scaffolding closes the gap" steer applied to tool building. The same tests judge both builds.
  Done when: one scorecard row shows pass rate, tokens and wall time for each builder on at least 5 entries. wild

- **Add a generated owner's manual of the tool shelf, one page, readable by the user in 2030** — CLEAN — value 3 — effort S — risk low — category: docs
  Why: thousands of tools and cards cannot be audited by reading directories. The manual lists what each does, when it last fired and what it may touch.
  Done when: the page renders from the shelf data, and a tool with no recorded use appears under "never used".

- **Make install grants expire and scope them to one tool and one run** — SECURITY — value 4 — effort S — risk low — category: grants
  Why: the mission says install grants are queued. Without expiry a yes given in 2026 still holds in 2030. This matches the standing rule that approval in one context doesn't extend to the next.
  Done when: a grant older than its TTL or used for a different tool is refused and the refusal names which condition failed.

Next question: which acquired tool has the user actually called twice from a real session path, and how many of the shelf's tools have never been called at all?
Next question: when a host ships its own tool discovery, what is the one test that tells Sampo to stop acquiring and defer to it?
