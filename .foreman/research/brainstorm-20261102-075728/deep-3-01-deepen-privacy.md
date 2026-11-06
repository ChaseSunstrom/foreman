# Brainstorm — lens: deepen: privacy

- **Seal a goal as private and make the label a single gate every outward path reads** — FEATURE — value 5 — effort M — risk med — category: privacy
  Why: the pack's goal-to-plan loop carries a plan over days; the "private" label, egress ledger and manifest ideas are all the same check at different points. One `private` flag on the goal, consulted by ship, push, model-child spawns, `fm lib` and web fetches, lets the other ideas hang off it. Assumption: outward paths are enumerable in `fm` (ship, ask, night tick, brainstorm children, mail).
  Done when: with the flag on, a test calls each outward verb and each is refused or routed to a local engine, and the refusal names the goal and the flag.

- **Unify egress into one ledger that manifest, finish card and doctor all read** — FEATURE — value 5 — effort M — risk low — category: privacy
  Why: the pack lists three separate ideas (ledger, manifest, finish card) and Foreman already keeps ledgers for bets and outcomes. One append-only row per send (destination, bytes, goal id, harness, content hash) makes the rest views. Assumption: model-child spawns are funnelled through a few call sites.
  Done when: `fm egress show T-id` lists every send for a task, and the finish card's total matches the sum of the ledger rows on a fixture run.

- **Redact on the way in: one scrubber for journal, goal file, prompts and exam captures** — SECURITY — value 5 — effort M — risk med — category: secrets
  Why: the pack's separate ideas (journal scan, goal-file refusal, redacted eval capture in T-0035) need the same detector. Build it once with a test corpus and let each caller choose block or mask. Assumption: no shared secret detector exists today.
  Done when: a fixture with a fake AWS key, a token and `/home/<user>/` is masked in the journal, refused in the goal file, and masked in an eval capture, all by one module.

- **Make the canary a standing exam kind and let it grade every tick job** — SECURITY — value 4 — effort M — risk low — category: leak testing
  Why: the pack's open questions ask what can be graded against something outside Foreman's own ledgers. A planted canary that is never in the task's inputs is a signal Foreman didn't author, which fits the steer on outside signals. Assumption: exam scenarios can seed a canary into env or a dotfile.
  Done when: an exam scenario plants a canary in `~/.config` and a run that sends it to any child, log, site file or commit fails with the sink named.

- **Run local-only mode in a network namespace as a test, not a promise** — SECURITY — value 4 — effort M — risk low — category: verification
  Why: the standing rule that Foreman works with no claude on PATH implies a no-network path; nothing in the pack proves it. Assumption: `unshare -n` is available on the user's hardened Arch kernel (check; may need a user namespace).
  Done when: the roundtrip e2e passes under `unshare -rn` with the egress ledger empty, and fails if a test adds a socket call.

- **Route model children through a local redacting proxy that is the only door out** — SECURITY — value 4 — effort L — risk high — category: proxy
  Why: the pack's proxy idea; combined with the namespace test, the proxy becomes the sole permitted destination, so the ledger is complete by construction rather than by discipline. Assumption: Claude Code and others honour a base-URL env var.
  Done when: with the namespace allowing only the proxy's socket, a brainstorm child completes, and every request appears in the ledger with its redactions counted.

- **Give each harness a data-class policy: what may reach claude, codex, gemini, or a local model** — FEATURE — value 4 — effort M — risk med — category: policy
  Why: bets already record their harness; `fm code` runs on any model. Sending source to a third-party CLI differs from sending it to a local engine. A per-path rule file (`secrets/**` never leaves; `docs/**` anywhere) is enforced at the ledger. Assumption: users run mixed harnesses.
  Done when: a rule denying `secrets/**` to non-local harnesses blocks a codex-bound prompt that includes such a file, and the block is logged.

- **Add a "what left this machine" section to the end-of-run Genesis report** — FEATURE — value 3 — effort S — risk low — category: reporting
  Why: the run produces a final report and the site publishes Genesis data to main on every tower change (a standing rule). That is outward publishing of derived data. Assumption: site/genesis JSON may carry task titles or paths.
  Done when: a scan of site/genesis output in a fixture run finds no absolute home path, email or secret pattern, and the report lists each published file.

- **Scan site and ship output for the user's own identifiers before any push** — SECURITY — value 4 — effort S — risk low — category: publishing
  Why: the pack's push grant lets Foreman push to main through `fm ship`; the system context shows an email and home path that must never reach a public repo. Assumption: ship has a pre-push hook point.
  Done when: a staged file containing the user's email or `~` makes `fm ship` stop with the file and line, and a clean diff passes.

- **Wild: A "paranoid replay" that re-runs a finished goal with every outward path denied, to show the plan survives offline** — FEATURE — value 3 — effort L — risk med — category: replay
  Why: wild. It joins the namespace and ledger ideas: a finished goal's plan is replayed against a recorded model transcript and fails if any step needs the network.
  Done when: `fm replay --offline T-id` reproduces the same task closes from the recorded transcript with zero socket attempts.

- **Wild: Honeytoken tripwires in the repo that page the user if anything outside the session ever reads them** — SECURITY — value 3 — effort M — risk med — category: tripwire
  Why: wild. Extends canaries from tests into real life: a fake credential in a decoy file whose use by a tool, child or dependency is detected by the guard's file-read hook and noted in the next session.
  Done when: a hook-run read of the decoy file produces a named alert in `fm doctor`, and ordinary builds don't touch it.

- **Wild: A privacy diff on every prompt change — "this edit will now send X to Y"** — FEATURE — value 3 — effort M — risk low — category: review
  Why: wild. Foreman's own skills, hooks and brainstorm packs grow (a lean ratchet exists); a check that compares the set of fields assembled into context packs per commit makes growth in what is sent visible, like the ratchet does for chars.
  Done when: adding a new field to the brainstorm context pack makes `fm ship` print "pack now includes: <field>" and require acknowledgment.

- **Make every privacy claim in the README a failing check when unproven** — CLEAN — value 3 — effort S — risk low — category: claims
  Why: the standing rule on proof before presentation already has the sweep compare public claims to exam lines; "local-first" and "nothing sent" are claims of that type. Assumption: the README or site makes such claims.
  Done when: removing the namespace test turns the sweep red on the claim naming it.

Next question: Which Foreman files persist outside the repo (journals, bet ledgers, memory, systemd units), and which of them hold prompt text or user identifiers that a backup or sync tool might copy?
Next question: What does the user want to happen when a private goal needs a capability only a remote model has: fail, ask once with `fm ask`, or degrade to a weaker local model?
