# Brainstorm — lens: 2030 worked back

- **Keep an intent ledger every run is checked against** — FEATURE — value 5 — effort L — risk med — category: intent
  Why: tier xhigh, domain: law (a constitution). By 2030 the user directs many agents and can't re-read every diff. Intent is the scarce input. The steers show the user correcting criteria after the fact (T-2583 character count, the re-grounding to S). Prior art: ADRs and CLAUDE.md are static prose and nothing enforces them. Assumption: constraints can be stored as short testable clauses.
  Done when: `fm intent check` flags a planted diff that contradicts a stored clause and passes a clean one.

- **Taint-track untrusted content through to commands** — SECURITY — value 5 — effort L — risk med — category: guard
  Why: tier high. By 2030 agents read the web, MCP results and issues all day. The guard sees command strings only, and the open question about inherited authority points at this. Prior art: taint analysis in compilers; agent harnesses mostly use allowlists. Assumption: transcript hooks can see which tool result a command came from.
  Done when: a command whose arguments were copied from a fetched page needs confirmation in bypass mode, and the same command typed by the user does not.

- **Make source the intent and the code a regenerable cache** — FEATURE — value 5 — effort L — risk high — category: regeneration — wild
  Why: tier massive, domain: manufacturing (CAD file vs. printed part). If the intent clauses plus the proofs fully pin behaviour, the code can be rebuilt on any language, platform or model. Prior art: none found for agent harnesses. Assumption: proofs are strong enough to stand in for review.
  Done when: for one small fixture repo, deleting `src/` and running `fm regen` yields code that passes every stored proof.

- **Own the pager: turn production crashes into failing tests and fixes** — FEATURE — value 5 — effort L — risk high — category: operations
  Why: tier massive. By 2030 "building software" includes running it. The machinery already exists (brief, prove, lane, guard) and only the intake is missing. Prior art: Sentry autofix and similar, none of them evidence-gated. Assumption: the user can supply a log or crash feed.
  Done when: a pasted stack trace becomes a brief with a reproducing test that fails before and passes after the fix.

- **Record enough to re-derive any close on a successor model** — FEATURE — value 4 — effort M — risk low — category: durability
  Why: tier high, domain: archaeology/preservation. Models get deprecated within a year or so, and a ledger of results can't be re-audited without the inputs. Prior art: reproducible builds cover binaries, not agent runs. Assumption: prompts and tool outputs are already in transcripts.
  Done when: `fm rederive T-NNNN --model X` replays the brief and prove commands and reports whether the original proof still passes.

- **Attach a retire-when predicate to every verb and skill** — CLEAN — value 4 — effort M — risk low — category: obsolescence
  Why: tier medium, domain: sunset clauses in law. The earlier slate has automatic pruning by use, but a verb can be well used and still be redundant once a model does it natively. Each predicate would name a measurable condition, such as bare-model pass rate on its exam at or above X. Assumption: exams can run with a feature off.
  Done when: `fm tidy` lists a fixture verb whose predicate is met, with the measurement.

- **Run a shared ledger and lane-claim protocol for several humans** — FEATURE — value 4 — effort L — risk med — category: teams
  Why: tier xhigh. By 2030 a team of people each run swarms, and Foreman is single-user, with the ledger, tower and budgets all one person's. Prior art: merge queues and CODEOWNERS, none agent-aware. Assumption: the ledger can be merged with the hash chain intact.
  Done when: two clones claim the same brief and one is refused with the other's name; both ledgers pass `fm verify-ledger` after merge.

- **Rehearse migrations and infra changes on a cloned snapshot** — FEATURE — value 4 — effort M — risk med — category: proof kinds
  Why: tier high. The proof kinds today cover code and tests. Work by 2030 includes schemas, terraform plans and data pipelines, which need a before/after against real-shaped data. Prior art: shadow databases, `terraform plan`. Assumption: a local snapshot or fixture is available.
  Done when: a `fm prove --migrate` fixture fails on a lossy migration and passes on a lossless one.

- **Take a morning voice briefing and approve decisions by voice** — FEATURE — value 3 — effort M — risk low — category: devices — wild
  Why: tier medium. Overnight runs end with a queue of yes/no decisions that today sit in the terminal. Voice and phone are untouched surfaces, and a summary read aloud suits someone making coffee. Assumption: a local speech engine is acceptable.
  Done when: `fm brief --speak` reads the pending decisions aloud and a spoken "approve two" records the decision in the ledger.

- **Appoint an heir and keep a dead man's switch** — FEATURE — value 3 — effort M — risk med — category: continuity — wild
  Why: tier xhigh, domain: wills and trusts. If the user is away for N days, Foreman drops to a charter that allows only dependency patches, security fixes and an honest status page, then hands off to a named person. Prior art: Google's inactive account manager covers data, not maintenance. Assumption: users with side projects would want it.
  Done when: with the clock mocked past N days, a fixture run lands only charter-class tasks and writes a handoff note.

- **Prove a quote against a reference implementation (differential twin)** — FEATURE — value 4 — effort L — risk med — category: proof kinds
  Why: tier extreme, domain: science (a control group). For rewrites and ports, the best proof is the old build and the new build agreeing on recorded inputs. Prior art: differential and golden-master testing, not wired to briefs. Assumption: inputs can be captured from tests or logs.
  Done when: `fm prove --twin OLD` reports the first diverging input on a planted regression.

- **Cap what a swarm can do per hour of human review** — FEATURE — value 4 — effort M — risk low — category: attention
  Why: tier xhigh, domain: manufacturing (Little's law/WIP limits). By 2030 the bottleneck is review, not generation. Existing budgets cap dollars, not unreviewed output. The WIP limit would stop new lanes when unreviewed landed diff exceeds what the user has historically read. Assumption: the user's reading rate can be inferred from approval timestamps.
  Done when: with a fixture review backlog above the limit, `fm run` declines to start a new lane and names the limit.

- **Name every authority a spawned child inherits, and print it** — SECURITY — value 4 — effort S — risk low — category: authority
  Why: this answers an earlier question: which spawned processes inherit the push grant, credentials or signing key. Assumption: this list does not exist today in one place.
  Done when: `fm authority` lists each child kind with its inherited grants, and a test fails if a new child kind is missing from the list.

- **Let outsiders replay your proofs without your machine (wild)** — FEATURE — value 3 — effort L — risk med — category: verification — wild
  Why: tier extreme. Regulators and clients in 2030 will want to rerun the evidence in a container, not trust a signed PDF. A close would ship a container recipe plus the prove commands. This differs from the signed audit pack because it is replayable, not just signed. Assumption: proofs are deterministic enough.
  Done when: `fm export --replay T-NNNN` produces a bundle whose script reruns the proof in a clean container and matches the stored result.

Next question: which of Foreman's discipline steps would a 2030 model do unprompted, and which of its failure modes would grow with longer autonomy?
Next question: what does the user need to hand over to a successor (a person or a model) so the project survives without them?
