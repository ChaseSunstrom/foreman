# Brainstorm — lens: 2030 worked back

- **Probe the host's Read limit and size every doc shard to it** — FIX — value 4 — effort S — risk low — category: context
  Why: MASTER.md is 75,758 tokens and Read refuses it. A fixed shard constant would break again when the host's cap moves. Assumption: the cap can be found by probing or from the refusal message.
  Done when: `sampo doc --check` reads the cap from a recorded probe, and a test that halves it fails until the shards are regenerated.

- **Hash-pin doc shards and verify them on every served read** — SECURITY — value 3 — effort S — risk low — category: injection
  Why: sharding makes `sampo doc <verb>` a new channel into model context, and anything that edits a shard on disk can write instructions there. Assumption: shards will be generated files.
  Done when: editing one byte of a shard makes `sampo doc` refuse and print the expected hash, and a test covers it.

- **Test that a planted `sampo` package cannot shadow the plugin's modules** — SECURITY — value 3 — effort S — risk low — category: supply chain
  Why: the rename put the code under `sampo.*`, and "sampo" is a plausible name for a PyPI or system package. Hooks run on every tool call. Assumption: some entry points do not yet run with `-I`.
  Done when: a test puts a hostile `sampo/__init__.py` on `PYTHONPATH` and in site-packages, and every hook and verb still imports the plugin copy.

- **Price the injected text over a year and gate on it** — PERFORMANCE — value 4 — effort S — risk low — category: lean
  Why: 2,733 characters injected twice, plus 48 to 76 per turn, looks small until it is multiplied by sessions and turns in the ledgers. The ship gate would print an annual token bill and cache-miss count and fail on growth without a waiver. Assumption: ledgers hold enough session counts to extrapolate.
  Done when: `sampo lean --bill` prints one dollars-per-year line per injection channel, and the ship gate fails a +10% change.

- **Scan the hook path for stdlib features slated for removal** — CLEAN — value 3 — effort S — risk low — category: durability
  Why: hooks run on bare `python3` on a rolling Arch host, where deprecated stdlib modules do disappear. A removal would silently take down the Ward (fail-open). Assumption: nobody has checked the hook imports against the removal schedule.
  Done when: a test lists every stdlib import in the hook closure against a dated removal table, and it fails on a planted `cgi` import.

- **Add an algorithm id to every ledger hash and signature** — SECURITY — value 3 — effort M — risk med — category: ledger
  Why: hash-chained ledgers are meant to outlive 2030's crypto defaults. Without an id field, a later change makes old chains unverifiable. Assumption: the chain currently hard-codes one hash.
  Done when: each record carries `alg`, the verifier dispatches on it, and a fixture with a second hash verifies alongside the old ones.

- **Add an evidence-hold class that pruner and redactor both respect** — SECURITY — value 3 — effort M — risk med — category: privacy
  Why: the 2.4 GB prune needs a plan, but some ledgers (grants, Ward verdicts, pushes) may need to be kept as proof for years while chat transcripts should go. Redaction must not erase held records silently. Assumption: no such class exists yet.
  Done when: a held record survives `prune --apply`, and a redaction request on one prints the hold and its expiry instead of acting.

- **Tag every Ward verdict with the principal that issued the command** — SECURITY — value 4 — effort M — risk med — category: guard
  Why: by 2030 most commands come from orchestrators and sub-agents, not the user. A principal field (user, orchestrator, sub-agent, lane, cron) lets rules differ by caller and lets the ledger show who tried what. Assumption: hook payloads carry enough to tell sub-agents from the main session.
  Done when: the verdict ledger has a `principal` column, and one rule applies only to sub-agents with a test.

- **Re-run the Ward exam when a stronger model ID appears** — SECURITY — value 4 — effort S — risk low — category: guard
  Why: the environment lists newer, stronger models than the ones the guard was tested against. A guard good enough for yesterday's attacker is the risk. Assumption: the exam can be driven by model ID.
  Done when: `sampo doctor` flags "Ward exam not run on <model>" for any listed model and clears after a run with a recorded result.

- **Give every lean waiver a fuse date that fails CI when it lapses** — CLEAN — value 3 — effort S — risk low — category: lean
  Why: growth waivers, pending-measurement rows and "dropped with a noted remainder" notes pile up without end. A date forces a decision (renew with evidence, or cut).
  Done when: a waiver with a past date fails the ship gate and names its owner task.

- **Keep a 2030 backcast file that each Mission must move** — FEATURE — value 3 — effort S — risk low — category: process
  Why: Missions are judged one at a time, so lean can lose to features every generation. The file holds a dated target for chars per turn, state GB and Read-safe docs. Each Mission close prints the delta. Assumption: the user wants fixed targets rather than relative ones.
  Done when: `sampo genesis check` prints each target with its current value and fails a Mission that moves one the wrong way.

- **Wild: Open a cold-return mode after 90 days away** — FEATURE — value 4 — effort M — risk low — category: devices
  Why: a returning user (or a new orchestrator) faces stale installs, a changed host and a fat state directory. One session-start card would show what changed in the host, in the Ward and in the state, and offer a diet. Assumption: the last-seen date is recorded.
  Done when: a fake clock 91 days ahead makes the next start print the card once, and it stays silent otherwise.

- **Wild: Print a one-page paper Ward card with a hash you can read by eye** — SECURITY — value 2 — effort S — risk low — category: restore
  Why: after a restore or a rename there is no outside check that the Ward is intact. A printable card lists rule names, protected paths and a short hash for the user to compare after any restore. Assumption: the ruleset can be canonicalised.
  Done when: `sampo ward card` is byte-stable across runs, and a changed rule changes the hash.

- **Wild: Share a cross-harness denial note** — FEATURE — value 3 — effort M — risk med — category: multi-agent
  Why: Claude Code, Codex and Gemini often work in one repo, and each learns separately that a command is refused. The first refusal would post a short, hashed "denied here" note that the others read before trying. Assumption: non-Claude hooks are weaker, so they gain most.
  Done when: a command refused under one harness is skipped by a second harness's shim in a test, with a ledger line saying why.

Next question: which of the four Mission 5 numbers (2,733 chars, 75,758 tokens, 2.4 GB, 48–76 per turn) will already have grown past its target when a stranger first installs Sampo, and what measures that?
Next question: if the user's main harness changed tomorrow, which of the lean and safe guarantees would stop being true without any test failing?
