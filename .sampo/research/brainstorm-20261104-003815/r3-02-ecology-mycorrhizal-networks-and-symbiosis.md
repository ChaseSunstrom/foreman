# Brainstorm — lens: ecology: mycorrhizal networks and symbiosis

- **Share green test verdicts across lanes by input-tree hash** — PERFORMANCE — value 5 — effort M — risk med — category: gate speed
  Why: `plugin/tests/` holds 443 files, `sampo ship` runs the full suite, and many lanes run in parallel. Assumption: lanes re-run identical suites on identical trees. Like a common mycorrhizal network, one lane's verdict feeds the others. The key is a hash of the files each test read, plus the interpreter and env fingerprint.
  Done when: two lanes with the same tree run the suite, the second reports "N tests reused from lane X", and a one-byte change to a read file forces a real re-run.

- **Serve hooks from one warm daemon shared by all sessions** — PERFORMANCE — value 4 — effort M — risk high — category: hook latency
  Why: `bench_hooks.py` exists, so Python start-up per hook event is a known cost. One shared hypha beats a cold process per call. Assumption: start-up dominates hook time. The Ward must fail closed to the in-process path if the daemon is dead or stale.
  Done when: p95 hook latency drops at least 3x in `bench_hooks.py --runs 20`, and killing the daemon mid-run still blocks a planted bait command.

- **Broadcast a poisoned-content hash to every lane (systemic acquired resistance)** — SECURITY — value 4 — effort M — risk med — category: injection defence
  Why: T-0791 (injection and supply-chain defences) is deferred with 18 ideas. When a lane's Ward or reviewer flags a file, page or tool result as injected, it writes that content's hash to a shared "primed" list. Every other lane then treats the same bytes as hostile data, with a fenced-data wrapper and no instruction following. The list tightens only.
  Done when: lane A flags a planted page, lane B reads the same bytes and sees the fence, and B reads a one-byte-different page unflagged.

- **Run imported plugins, MCP servers and local-model agents in a nodule with a sanction valve** — SECURITY — value 4 — effort L — risk med — category: capability containment
  Why: the user's own words and ideas show imports of skills, plugins and local models. Legumes keep rhizobia in a sealed nodule and cut oxygen to ones that fix less nitrogen. Each symbiont gets a declared tool and path envelope, a contribution measure (accepted outputs per unit cost), and an automatic envelope shrink when its measured contribution drops. This is distinct from the existing "cheater cut-off" rating because the valve acts on permissions, not just on a score.
  Done when: a planted symbiont that returns junk loses a tool grant within N calls, and `sampo doctor` names the shrink and its reason.

- **Seal state in septa and plug a runaway writer (Woronin body)** — SECURITY — value 3 — effort M — risk med — category: state containment
  Why: the 2.4 GB state and the ENOSPC and write-rate ideas exist, but there is no containment unit. Hyphae are divided by septa, and a ruptured compartment is plugged so the rest keeps its contents. Split ledgers into compartments. A compartment that grows past its rate, trips a secret-shaped scan or fails a checksum gets sealed read-only and quarantined, and readers get a tombstone.
  Done when: a fault-injected writer looping on one ledger is plugged within a second, the other ledgers keep accepting writes, and `sampo state unplug` restores it.

- **Sign lane-to-lane messages with a kin tag** — SECURITY — value 3 — effort S — risk low — category: lane trust
  Why: lanes already whisper and hand off notes, and the injection brief is open. Plants recognise kin by root exudates. Each lane's notes carry an HMAC keyed by its lease token, and receivers drop unsigned or stale-token notes and say so once.
  Done when: a note forged by a file the lane read is dropped and logged, while a genuine sibling note arrives.

- **Keep a spore pool of pre-warmed lane worktrees** — PERFORMANCE — value 3 — effort M — risk low — category: lane startup
  Why: assumption: lane spawn pays for worktree, deps and state-resolution probes every time. Dormant spores germinate when conditions arrive. Keep K worktrees at current main, with caches reflinked, which a brief claims and fast-forwards.
  Done when: time-to-first-tool-call for a new lane falls at least 50% against cold spawn in the bench, and a stale spore is discarded rather than used.

- **Desynchronise heavy gates across lanes with a shared tide file** — PERFORMANCE — value 3 — effort S — risk low — category: load shaping
  Why: the drive has re-pushed on lane events and several lanes finish together. Mycelial pulses are phased to avoid contention. Lanes read a tide file and start suite, embedding and ship work in jittered slots. Urgent work skips the queue.
  Done when: with 6 lanes finishing together, peak concurrent suite runs stays at or below the cap and total wall time does not rise.

- **Score moons jointly for obligate pairs** — FEATURE — value 3 — effort M — risk low — category: moons funnel
  Why: the funnel dedupes and ranks each moon alone. Some moons only make sense as a pair (the lichen case). Among the top few hundred survivors, test pairs for complementarity and for a cold-read gain in wildness or value when merged. Promote pairs as one unit with both parent ids.
  Done when: on the 10,000 store, the funnel emits at least one pair the single-moon ranking had left below the cut, with a cold-read verdict recorded for it.

- **Wild: route tasks to models by Physarum flow reinforcement** — FEATURE — value 3 — effort M — risk med — category: model routing
  Why: assumption: routing between Claude, Jeff/Jev classifiers, qwen3.8-27b and qwen3.6-35b is hand-set, and a model switch costs about 3 minutes. Each task-kind to model edge has a conductance that thickens when the output passed its Exam and thins with decay and switch cost. Flow settles on a few thick tubes and keeps a trickle on others.
  Done when: after a replay of closed tasks, the routing table differs from the hand table on at least one task kind, and a replay of held-out tasks passes at least as often at lower cost.

- **Wild: send a truffle hound through old transcripts** — FEATURE — value 3 — effort M — risk low — category: lesson mining
  Why: the 2.4 GB state and host transcripts hold first-time passes that never became lessons. A small local model, taught by the ones that did, sniffs for buried near-misses, such as a recovered failure with no lesson filed. It files them as dormant candidates only.
  Done when: the hound surfaces at least 10 candidates from past sessions, and a cold reader rates at least 3 as new and true.

- **Wild: give each lane a root-hair budget for reading the repo** — PERFORMANCE — value 2 — effort S — risk low — category: context cost
  Why: roots grow hairs only where nutrients are found. A lane gets a small read allowance that grows only when a read led to an edit or a passing proof, and shrinks on reads that led nowhere. It is measured per task kind.
  Done when: median read volume per closed task falls without a fall in first-time passes on the planted-fault tier.

- **Wild: make a mycorrhizal mute week for the sharing itself** — SECURITY — value 2 — effort S — risk low — category: network audit
  Why: every sharing channel here (lessons, primed hashes, test verdicts, whispers) is also a spread path for bad data. One week a month a random channel is cut in lanes, and the exam records what got worse and what got better, which prices each channel's risk against its benefit.
  Done when: a report lists each channel with its on and off deltas and names at least one channel to tighten.

Next question: which of the sharing channels (test verdicts, primed hashes, lessons, whispers) has already carried a wrong item from one lane to another, and do the ledgers show it?
Next question: how much of a typical lane's wall time is start-up and gate repetition rather than model thinking, and is that split recorded anywhere?
