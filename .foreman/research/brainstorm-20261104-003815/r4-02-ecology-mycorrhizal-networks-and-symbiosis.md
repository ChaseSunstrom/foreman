# Brainstorm — lens: ecology: mycorrhizal networks and symbiosis

- **Stream agent state through one event file the drive tails by inotify** — PERFORMANCE — value 4 — effort M — risk low — category: drive
  Why: T-2873, T-2874 and T-2901 all patched the drive's running-set scan. It re-reads 1,500-line tails and fights the engine's background list, and it re-pushes every few minutes. A hypha carries one flow in each direction, so one writer appends start/stop lines to a single file and the drive wakes on change.
  Done when: a replay of the T-2873 shapes gives the same running set with zero tail scans, and an idle drive makes no reads between events.

- **Shard ledgers per lane and merge them at read time** — PERFORMANCE — value 4 — effort M — risk med — category: state
  Why: assumption: lanes append to shared ledgers, and the pack mentions PIPE_BUF-size appends and lock contention. Each lane writes only its own `O_APPEND` shard (mode 0600), and readers merge by timestamp. This also stops a compromised lane from rewriting another lane's evidence.
  Done when: 8 parallel lanes writing 64 KB records produce no interleaving, and a lane's write to another lane's shard is refused in a test.

- **Gate ledger and card merges on vegetative compatibility** — SECURITY — value 4 — effort M — risk low — category: merge safety
  Why: fungi fuse only with compatible genotypes, and an incompatible fusion is cut off to stop viruses spreading. Lane evidence, cards and any future cross-install exchange should merge only when schema version and guard-rules hash match. A mismatched record is quarantined, not merged.
  Done when: merging a shard stamped with a different guard hash leaves the target ledger unchanged and files a quarantine line.

- **Weed the small-model card store before cards reach prompts** — SECURITY — value 5 — effort M — risk low — category: injection
  Why: T-2909 added `research/cards/cards.jsonl`, cards written for small models and injected into their prompts. A poisoned card becomes a persistent injection. Leafcutter ants weed their fungus garden against the parasite *Escovopsis*. A weeder pass scans cards for instruction-shaped text and untrusted-source provenance, then has a cold child re-read them. Failures go to quarantine.
  Done when: a planted "ignore the Ward" card is quarantined by `sampo cards weed`, and the admit path refuses cards with no provenance.

- **Wrap tool results in a mantle that normalises them before the model sees them** — SECURITY — value 4 — effort M — risk med — category: injection
  Why: T-0791 holds 18 deferred injection ideas, and none sanitises tool output deterministically. An ectomycorrhizal mantle is the sheath between soil and root. The mantle strips ANSI and zero-width and bidi characters, caps length, and tags instruction-like spans as data.
  Done when: a fixture with bidi-hidden text arrives with the characters removed and the span tagged. A second fixture of ordinary diffs passes through byte-identical.

- **Put a tool-less reader between untrusted text and any lane holding tools** — SECURITY — value 4 — effort L — risk med — category: injection
  Why: web, MCP and fetched pages are the open door. A reader lane with no tools turns the text into a fixed schema, and the tool lane sees only that schema. The same split works for local models in Smith (T-2908).
  Done when: a page that says "run rm -rf" reaches the tool lane only as a quoted field, and a test shows the tool lane never received the raw page.

- **Rank local models by hijack susceptibility and let that set their tool tier** — SECURITY — value 4 — effort M — risk low — category: local models
  Why: the user runs several local models, including an uncensored variant, and T-2908 puts Smith on them. A repo-planted instruction suite (the cordyceps test) gives each model a hijack rate. Models above a threshold get read-only tools.
  Done when: `sampo louhi models` prints a hijack-rate column, and a model above the threshold is refused Edit in Smith.

- **Flag cheater and recon lanes by read/write asymmetry on shared state** — SECURITY — value 3 — effort S — risk low — category: lane monitoring
  Why: a mycoheterotroph takes from the network and gives nothing back. A lane that reads many other lanes' evidence and cards while writing none is either broken or probing. Flag it in the existing per-turn line.
  Done when: a synthetic lane that reads 50 foreign shards and writes none is flagged, and normal lanes never are.

- **Warm a new lane from its mother's indices** — PERFORMANCE — value 3 — effort M — risk low — category: lanes
  Why: assumption: each lane rebuilds the map, tree-sitter and embedding caches. A seedling is fed by the mother tree. Reflink-copy the parent's cache directory and refresh only the files the lane's diff touches.
  Done when: time-to-first-map in a new lane drops at least 5× on this repo, and the cache is byte-equal after a refresh.

- **Wild: Handshake with the host on install, like Nod and Myc factor signalling** — FEATURE — value 4 — effort M — risk low — category: harness
  Why: wild. T-0337 shows Gemini has no usable Stop, and T-0335 and T-0336 show codex and opencode are unverified. Sampo should emit a signed no-op probe through each hook event at install and record which events the host really delivered. A verb then activates only where its event arrived, and `sampo doctor` says which are dormant.
  Done when: on a host with a dead event, doctor lists the verbs left dormant, and none of them claim to be armed.

- **Wild: Measure the percolation threshold of the drive's dependency graph** — PERFORMANCE — value 3 — effort M — risk low — category: resilience
  Why: wild. Network science asks how many hyphae must be cut before the colony fragments. The check removes random lanes, leases and shards in a scratch estate and records the fraction at which the drive stalls. It reports the weakest single link first, so the next hole is found by measurement.
  Done when: the drill prints a threshold and a top-3 list of single points of failure, and fixing the top one raises the threshold on a rerun.

- **Wild: Give lanes a pheromone codebook for inter-lane notes** — PERFORMANCE — value 3 — effort M — risk med — category: tokens
  Why: wild. Ants coordinate with a few chemical symbols rather than prose. Lane-to-lane messages such as "claimed", "blocked on X" and "evidence at hash" become fixed codes of 12 bytes or fewer plus a decode table. Free-form notes stay as an escape hatch and are fenced as data.
  Done when: a 4-lane run uses at least 50% fewer inter-lane note tokens, and a decoder test round-trips every code.

- **Wild: Add a hyphal-tip budget so exploration only extends where food was found** — PERFORMANCE — value 3 — effort S — risk low — category: funnel
  Why: wild. Tips that find nothing stop growing, and tips that find resource branch. At 10,000 candidates, each family gets a small probe allowance that grows only when its last probes passed the cheap stage, so dry families stop costing local-model minutes.
  Done when: on a replay of the funnel log, total stage-2 calls drop at least 30% with the same set of promoted moons.

Answer to a left question (which lines does a session never act on): the cheater/recon flag and the handshake give a measured "dormant verb" list. A line naming a dormant verb can be dropped from the injection at no cost.

Next question: which shared stores (cards, lessons, steers, Genesis site data) cross a trust boundary before they enter a prompt, and which of them has no provenance field today?
Next question: if the host's hook delivery differs per harness, which of Sampo's "armed" claims are currently asserted, not observed?
