# Brainstorm — lens: inversion: what makes Foreman obsolete

- **Measure Sampo's marginal value against the bare model on every capability** — FEATURE — value 5 — effort M — risk low — category: necessity
  Why: the user's lean ask (SessionStart 2,733 chars twice, per-turn burden 48–76 chars, MASTER.md 75k tokens) and "a capability whose free arm beats the session arm is a top gap". Ideas so far include a bare-model ablation and necessity corpus, but no standing per-capability verdict joined to the injected-token cost of that capability.
  Done when: `sampo louhi necessity` prints one row per hook, verb and skill with injected tokens, bare-model pass-rate delta and a keep/native/retire verdict, over at least 20 held-out scenarios.

- **Attach a "native-in-host-by" probe to every discipline rule** — FEATURE — value 4 — effort M — risk low — category: obsolescence
  Why: assumption: Claude Code, Codex, Gemini CLI and opencode keep absorbing plan mode, permission rules, and done-gates. Prior ideas watch release notes; none give each rule a runnable probe that shows the host now blocks the same thing without Sampo.
  Done when: each guard rule and gate has a `native:` command that, run on a host with Sampo off, either reproduces the block (rule marked redundant) or fails (rule stays), and the result is stored with the host version.

- **Split the package into a 200-line portable core and optional shells** — CLEAN — value 4 — effort L — risk med — category: simplicity
  Why: README claims "discipline layer for any agent", yet plugin/lib is 259 files and 2,358 in the map. If hosts absorb the rest, the survivor is Ward plus prove plus the done-gate; assumption: that triple is what no host will ship.
  Done when: a directory of ≤ 25 files passes the Ward exam and the prove/done-gate e2e roundtrip with nothing else installed.

- **Cap session-start injection at a hard token budget with overflow behind a pull verb** — PERFORMANCE — value 5 — effort S — risk low — category: context
  Why: the request names SessionStart injecting 2,733 characters twice. Inversion: what if the model needed none of it unprompted? Inject only a pointer plus facts that changed the outcome in the ledger.
  Done when: `bench_hooks.py` and a transcript check show SessionStart emits once, ≤ 600 characters, and an exam arm shows no pass-rate drop.

- **Make MASTER.md a generated index plus per-verb shards each under 8k tokens** — FIX — value 4 — effort M — risk low — category: docs
  Why: MASTER.md is 75,758 tokens so Read refuses it; a doc agents can't read is a doc that makes the tool unusable without itself.
  Done when: no docs file exceeds 20k tokens, a lint fails above that, and every verb has an anchor an agent can Read in one call.

- **Report "days since Foreman changed an outcome" per capability** — FEATURE — value 4 — effort S — risk low — category: observability
  Why: assumption: ledgers already hold hook decisions and outcomes (`fm outcomes`). A capability that has not blocked, caught or corrected anything for N days is the first candidate to go dormant.
  Done when: `sampo doctor` lists capabilities with zero outcome-changing events in 30 days and each prints its injected-token cost.

- **Auto-dormant mode: capabilities that stop earning their tokens go silent until a trigger fires** — FEATURE — value 4 — effort M — risk med — category: lean
  Why: the pack's lean-substance rule parks unmeasured growth but never silences shipped growth. Dormant means no hook text, only a wake predicate.
  Done when: a capability with 30 idle days stops injecting, and the e2e suite shows it wakes on its trigger within one turn.

- **Shrink the 2.4 GB project state with age-based compaction and a size ceiling** — PERFORMANCE — value 4 — effort M — risk med — category: state
  Why: the request names 2.4 GB of project state. Ledgers and transcripts older than a window can be summarised into a few kilobytes, with the original archived or dropped.
  Done when: state for this project falls below 300 MB, `fm doctor` and the readers pass on the compacted copy, and a size ceiling warning fires at 80%.

- **Wild: Run a quarterly "host catches up" duel against a stock agent with Sampo removed** — FEATURE — value 4 — effort M — risk low — category: necessity
  Why: assumption: the strongest sign of obsolescence is a plain host passing the held-out duel (T-1231). Scheduling it on each new host release turns the question into a dated trend line on the site.
  Done when: a published chart shows Sampo-vs-bare pass-rate delta per host version, and a delta under a set margin files a "retire or narrow" task.

- **Wild: Let Sampo write its own retirement plan on demand** — FEATURE — value 3 — effort S — risk low — category: simplicity
  Why: a tool that can say which parts to delete as models improve earns trust; none of the pack's ideas yet generate the plan itself.
  Done when: `sampo sunset` prints an ordered list of capabilities to retire, each with the evidence row that supports it, and the dry run removes nothing.

- **Wild: Have a cold child explain Sampo in five sentences from the README alone, and fail the docs if it cannot** — CLEAN — value 3 — effort S — risk low — category: docs
  Why: assumption: a product too large to summarise is one a host can't absorb or a user can't adopt; the README and MASTER.md bloat suggest drift.
  Done when: a tool-less child's summary names Ward, plan, prove and queue, and a nightly check fails when the summary omits any.

- **Gate every new hook byte on a measured outcome change** — SECURITY — value 3 — effort S — risk low — category: guard
  Why: the request says "guard intact" while cutting context; cuts must not remove a protection quietly. Pair each trim with the Ward exam so safety stays fixed while text shrinks.
  Done when: the ship gate fails when injected characters grow without a recorded outcome row, or when the Ward exam pass count falls.

Next question: Which capability, if switched off for a week, would the user notice first, and does any ledger record that they noticed?
Next question: What will the hosts ship natively in the next two releases that overlaps Ward or the done-gate, and how would Sampo find out the day it lands?
