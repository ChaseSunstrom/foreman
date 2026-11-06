# Brainstorm — lens: ecology and evolution

- **Map the fitness landscape per task** — FEATURE — value 4 — effort M — risk low — category: prediction
  Why: assumption: if k cheap plan sketches from different starts converge on the same files and proof, the task is a smooth peak. If they diverge, it is rugged and needs a stricter gate or the user. Tier guess: high.
  Done when: `fm plan --ruggedness` prints a score for a brief, and over 20 closed tasks the score correlates with reopen or retry count.

- **Partition lane niches by competitive exclusion** — FEATURE — value 4 — effort M — risk med — category: coordination
  Why: builder lanes share a repo in worktrees. Assumption: lanes that overlap in files or modules are what cause merge conflicts. The scheduler would give each lane a non-overlapping niche (path set) and queue overlapping briefs behind it. Tier guess: xhigh.
  Done when: a seeded two-brief overlap runs serially while disjoint briefs run in parallel, and the receipt names the niche each lane held.

- **Meter the error threshold for self-edits** — FEATURE — value 3 — effort M — risk low — category: reliability
  Why: Foreman edits its own rules, lessons and skills (1388 skill files). Eigen's error catastrophe is the point where mutation outruns selection. Track self-edits per week against verified-good closes, and warn when edits outpace the verification that vets them. Tier guess: high.
  Done when: `fm doctor` shows a mutation-load row, and a synthetic burst of unverified rule edits turns it red.

- **Gate lessons by expression conditions (epigenetics)** — PERFORMANCE — value 4 — effort M — risk med — category: context cost
  Why: `fm burden` fixes show that injected context is a felt cost. Each lesson gets a trigger predicate (file glob, verb, error text) and is loaded only when it matches. Others stay silent but stored. Tier guess: high.
  Done when: on a fixed session replay, injected lesson characters fall at least 30% and no lesson that was cited before goes unloaded.

- **Keep a guard refugium for recolonization** — SECURITY — value 4 — effort S — risk low — category: guard resilience
  Why: it answers the open question about a missing, truncated or unreadable rules file at hook time. Keep a frozen, hash-checked last-known-good copy of rules and grants. On corruption, unattended paths fail closed to the refugium and write a ledger record. Tier guess: medium.
  Done when: `fm drill` truncates the rules file and the hook blocks as the refugium would, and a ledger entry names the fallback.

- **Detect convergent reinvention at intake** — CLEAN — value 4 — effort M — risk low — category: dedupe
  Why: the user's own words show 3 of 4 slate items already built, and several c-items were dropped as "mostly built". Compare each new brief with existing verbs by behaviour (help strings, tests, ledger use), not by name, and flag analogues before any lane spends money. Tier guess: high.
  Done when: replaying the dropped c13, c16 and c21 briefs flags `fm replay`, `check_predictions` and `fm usage --prune` with no false flag on a truly new brief.

- **Report trophic efficiency of spend** — FEATURE — value 3 — effort M — risk low — category: observability
  Why: Ecology tracks how much energy survives each level. Report what share of dollars survives each level: user ask, brief, lane, review, landed and unreverted. It extends the yield-per-dollar receipt (c22) to show where spend is lost. Tier guess: high.
  Done when: the drive receipt prints a per-level survival table whose levels sum to total spend.

- **Detect inbreeding depression in the lesson pool** — FEATURE — value 3 — effort M — risk med — category: learning
  Why: assumption: lessons learned from one repo and one model's own closes lose novelty over time. Flag when new lessons are near-duplicates of old ones and yield per lesson falls. Offer a genetic rescue by importing a lesson from outside (a fresh repo, another model). Tier guess: xhigh.
  Done when: a synthetic pool of near-duplicate lessons trips the flag, and the report names the rescue candidates.

- **Give lanes inclusive-fitness credit** — FEATURE — value 3 — effort M — risk med — category: credit assignment
  Why: a lane that adds a shared test helper or fixes a flaky test raises other lanes' success but earns nothing for itself. Hamilton's rule credits it by the downstream closes it enabled (r·b > c). Feed that into lane reputation and routing. Tier guess: xhigh.
  Done when: a seeded helper lane shows downstream credit in `fm outcomes`, and a no-effect lane shows none.

- **Run a mycorrhizal context bus for lanes** (wild) — FEATURE — value 3 — effort L — risk med — category: agents
  Why: assumption: parallel lanes each re-read the same files and re-pay the same context. A shared underground channel passes facts and cache between lanes, with surplus going to the starved lane. Tier guess: extreme.
  Done when: two lanes on adjacent briefs spend measurably fewer input tokens with the bus on than off, with equal proof results.

- **Speciate per repo and test hybrid viability** (wild) — FEATURE — value 3 — effort L — risk high — category: self-adaptation
  Why: assumption: one global rule set fits no repo well. Let each repo drift its own guard, lessons and gates (allopatric speciation). Periodically cross two subspecies and run the proof suite on the hybrid to see which adaptations are portable. Tier guess: extreme.
  Done when: two forked configs diverge on a fixture, and the hybrid report lists adaptations that failed on the other repo.

- **Mine the fossil record for the cause of extinctions** (wild) — FEATURE — value 2 — effort M — risk low — category: archaeology
  Why: Foreman retires verbs by usage (`fm usage --prune`) but never records why a rule, lesson or verb died or what replaced it. A necropsy file per retired item (last use, cause, successor) makes retirement reversible and answers "who notices first". Tier guess: medium.
  Done when: retiring a verb writes a necropsy record, and `fm tidy --fossils` lists it with its successor.

- **Quarantine Foreman's own invasive processes by default** — SECURITY — value 4 — effort M — risk med — category: authority
  Why: it answers the open question on inherited authority. Lanes, ticks, `fm code` tools and prover children should start with no push grant, credentials or ledger key. Each holds only the tokens its brief names, and a probe at spawn lists what it holds. This is the enforcement side of the quarantine idea above. Tier guess: high.
  Done when: a test child spawned with defaults fails to push or sign, and `fm doctor` lists inherited authority per process class.

Next question: which of Foreman's rules or lessons does the user override or silently undo, and does that pattern select against them before the user says so?
Next question: do lanes in parallel actually conflict, and where do they overlap, so that niche partitioning is worth building?
