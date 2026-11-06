# Brainstorm — lens: approaches

- **Probe the host's spend cap before using Foreman's own counter** — FEATURE — value 4 — effort S — risk low — category: cost
  Why: the pack shows a hand-built usage governor and watchdog; an installed Claude Code may already expose a per-run spend cap. assumption: the installed `claude -p` has a budget flag. Probe it in `fm doctor` and fall back to the counter only when it is missing, so version skew cannot silently drop the cap.
  Done when: on the installed version, `fm doctor` names the cap path in use, and a run with a $0.01 cap stops at the host limit with a journal line saying so.

- **Batch overnight brainstorm lenses through the Message Batches API** — PERFORMANCE — value 4 — effort M — risk med — category: cost
  Why: every lens child sends the full context pack in real time, and the "cost at scale" request in the pack points at that repeated spend. assumption: batch pricing is cheaper on this account and latency of hours is acceptable for overnight rounds. Interactive runs stay synchronous.
  Done when: a batched round yields the same count of parsed ideas as a direct run on the same pack, and `fm cost` shows the batch discount on the round's receipt.

- **Cascade each brainstorm round: a cheap draft, a strong judge on the top five** — PERFORMANCE — value 4 — effort M — risk med — category: cost
  Why: the pack asks for 10–15 ideas per lens, and most of the spend goes to ideas that die in dedupe. assumption: a cheap model's ideas are good enough to shortlist. The strong model only scores the shortlist, so cost falls with the lens count.
  Done when: on the same pack, the cascade's top five overlap a strong-only run's top five in at least three of five, at under half the cost, per `fm cost`.

- **Replace the custom hook timer with hyperfine** — CLEAN — value 3 — effort S — risk low — category: observability
  Why: the pack's hook bench has a noisy p95 that was not reproducible on a quiet machine; a standard tool gives a repeatable median and confidence interval without new timing code.
  Done when: `bench_hooks` reads its numbers from hyperfine output, the custom timing code is deleted, and the median for one hook matches a manual hyperfine run within 10%.

- **Make the plugin the only surface, enforced by a parity test** — CLEAN — value 5 — effort S — risk low — category: developer experience
  Why: the request says every feature must work in the Claude Code plugin, but nothing in the pack checks that each `fm` verb has a `/foreman:` command.
  Done when: CI fails if any verb in the command table lacks a plugin command, and a test invokes each plugin command once and checks exit 0.

- **Turn blocked items into predicates that unblock themselves** — FEATURE — value 4 — effort M — risk low — category: blocked pile
  Why: the pack lists about 10 blocked items, such as T-0325 needing a library and T-0418 waiting on an install. Each of these has a checkable condition, so a human does not need to notice when it clears.
  Done when: a blocked item with an `unless:` predicate, such as a binary present or a version installed, moves to queued within one sweep after the predicate turns true.

- **Keep state in SQLite WAL instead of per-file JSON with hand-made locks** — CLEAN — value 4 — effort L — risk med — category: reliability
  Why: the pack shows many state files, leases and gate locks, along with fixes for hung holders and crash hygiene. One transactional store removes most of that custom locking. assumption: SQLite is acceptable in the plugin's dependency budget.
  Done when: a test kills a writer mid-update and a reader sees the pre-update state, and no per-task JSON state file remains in `plugin/lib`.

- **Hand host-level refusals to Claude Code permissions and keep only the guard's exceptions** — SECURITY — value 4 — effort M — risk med — category: security
  Why: the guard hook carries a list of refused commands that the host's permission rules could express directly. Delegating those rules shrinks the hook's code and attack surface. Any rule the host cannot express stays in the guard, with a reason.
  Done when: every guard rule is either a host permission entry or a listed exception with a reason, and the bypass-mode refusal tests still pass.

- **Pin the plugin to a tested Claude Code range and refuse to run outside it** — FIX — value 4 — effort S — risk low — category: reliability
  Why: the pack's version-skew work has been reactive, with a fix after each Claude Code release. A declared range that fails closed with a one-line fix turns silent drift into a clear message.
  Done when: running the plugin against a Claude Code version outside the range exits non-zero with the range and the upgrade command, and a test covers both the in-range and out-of-range cases.

- **Pair each brainstorm lens with a rival that attacks its top idea before filing** (wild) — FEATURE — value 3 — effort M — risk low — category: user value
  Why: the lenses only produce ideas, so nothing tests whether the best idea holds up. A second child whose only job is to break the top idea would filter weak ideas before they reach the ledger.
  Done when: each round's filed ideas each carry a rival's verdict, and a seeded weak idea in a test pack is marked rejected.

- **Run the queue inside the interactive session through a slash command, with zero child processes** (wild) — FEATURE — value 4 — effort M — risk med — category: simplicity
  Why: the pack shows heavy machinery for headless runs, including watchdogs, leases and spawn caps. For a single user at a desk, the existing session can walk the queue directly, which avoids most of that machinery. assumption: the user is at the desk for most runs.
  Done when: `/foreman:next` completes one queued task end to end in an interactive session, and the journal shows no spawned `claude -p` child for that task.

- **Store the queue on an orphan git ref that syncs with push** (wild) — FEATURE — value 3 — effort L — risk med — category: devices
  Why: the pack's "every surface" goals need the queue on more than one machine. Git already syncs and merges, so a `refs/foreman` branch would give a queue that follows the repo without a server.
  Done when: two clones see the same queue after a fetch, and an edit to one task on each clone merges by task ID without losing either change.
