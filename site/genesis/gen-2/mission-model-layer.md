# Mission 1 — model layer (gen 2, the user's gen-2 steer of 2026-10-31, T-2437)

Parent: gen-2/seed.md row 1 → the user's steer recorded as T-2437, under gen-0.md (its goal, MUSTs and NEVERs are
quoted in the seed and apply here unchanged).

## Capability
A provider-agnostic decision interface: a call names a kind and an input and gets back a choice, a score and a
probability with calibrated confidence. Backends are tried cheapest first: deterministic rules, then local models
(selfjev-4b or jeff behind the Jev-compatible API at TYPESAFE_BASE_URL, Von for intent routing, Jevlike for
task-specific models trained from Foreman's own history), then TypeSafe's hosted Jev, then Claude. The same shape
serves embeddings (search, recall, dedupe), rerankers (leads), vision (UI checks) and local code models through fm code
and the user's vLLM or llama-swap servers. Candidate uses: intake type and tier, fm find lead triage, coverage-cell and
done-claim checks, the model router (#9), idea dedupe and scoring.

## The user's rules for it (T-2437, verbatim in substance)
- Never inside the guard or the evidence gates: models advise, proof decides.
- Sensitive repos use local backends only.
- Installs and model downloads go through the install queue for the user's yes.
- Each use is kept only if the exam shows it beats the path it replaces on accuracy, cost or latency, its
  probabilities checked against outcomes.

## Gaps this Mission targets (coverage: the Model layer area, 47 idea cells; planned, open until the exam closes them)
- The interface and registry: build × other agents, build × MCP, build × CLI, operate × Claude Code (sensitive: local
  only), operate × CLI (doctor health).
- The policy checks: verify × Claude Code (no model in the guard or a gate), ship × CLI (no unapproved backend).
- Measured uses: verify × CLI and verify × headless/server (exam arms and shadow replays), verify × MCP and learn × CLI
  (probabilities into the prediction book and the Brier ledger), ship × Claude Code (live only by a decision row
  citing the exam).
- First uses in shadow mode: plan × Claude Code (intake type and tier), find × Claude Code and find × CLI (lead
  triage), understand × Claude Code and find × headless/server (embedding recall and dedupe).
- Surfaces: plan × MCP, understand × site, operate × MCP, the AGENTS.md cells.
- Not in gen 2 (tier 4, after the interface has an exam): Jevlike training (build × headless/server, learn ×
  headless/server), vision checks (verify × fm code), Von routing (plan × fm code); they stay idea cells, and the
  four candidates wait in not-yet.md as unevaluated.

## Approaches
1. One decide() on fmmodels: a registry entry per backend (cost, latency, sensitive_ok), a cascade that stops at the
   cheapest backend whose confidence clears the kind's bar, every answer written to the prediction book, and each use
   in shadow mode (logged beside the path it would replace) until an exam arm shows it beats that path. Fails if: a
   use's exam never runs (then it stays shadow, which costs only the logged call).
2. Each caller calls its own model directly. Fails if: the sensitive-repo and install rules must be enforced in every
   caller, and no use can be compared with another.
3. One cloud model for every kind. Fails if: it breaks the sensitive-repo rule and never tests the cheaper backends
   the user named.
4. Use what exists: fmmodels already resolves local and cloud profiles; fmforesight's prediction book and
   fmoutcomes' Brier ledger already score probabilities against outcomes; fm ask --later is the install queue; fm exam
   grades arms on held-out scenarios. Approach 1 composes these rather than adding a stack.
Choice: 1 on 4 (85%): one place enforces the user's four rules, and shadow mode means no use changes behaviour before
its exam says so.

## Exam
The layer is graded per use, not as a §2 capability: one arm per use runs the model path and the path it would replace
on the same held-out scenarios (intake type and tier on the user's own past requests; lead triage on fm find's planted
defects; dedupe on near-duplicate captures). Each kind has 9 or more scenarios with a held-out third, the outside
third authored by a tool-less child (`--author child`). A use's verdict is accuracy, cost and latency against its
path, plus the Brier score of its probabilities; zero-token arms run each generation, the session arms at the
end-of-run exam (rule 6).

## Long-horizon goal (end of run)
The same goals run with the layer's live uses on and off: cost per finished goal and the true-done rate decide whether
the layer stays.

## Lean
No new verb: backends show in fm doctor (health and latency) and in fm outcomes --judgment (calibration); decide() is
a library call and an MCP tool. Hook p95, rules size and injected context don't grow: nothing runs in a hook.

## Tier share
Briefs 1-4 are tier 3-4 (a capability Foreman lacks, and the exam arms that judge it); brief 5 is tier 2 (surfaces).
Four of five, 80%.

## Done when
decide() answers through the registry with the four rules enforced and tested; at least one use has run its exam arm
against the path it replaces, and it is live or stays shadow by an fm decide row citing those numbers; the surfaces
and docs name what each use decides and how it scored.

## Briefs (fm intake)
```
FEATURE: decide() on fmmodels: a kind and an input return choice, score and probability from a backend registry (cost, latency, sensitive_ok), cheapest first, each answer in the prediction book
FEATURE: the user's four model rules as tests: no model import in fmguard or the evidence gates, sensitive repos resolve local backends only, backends and downloads only through fm ask --later, no live use without an fm decide row citing its exam
FEATURE: model exam arms: per use (intake tier, lead triage, dedupe), the model path against the path it replaces on held-out child-authored scenarios, accuracy, cost, latency and Brier
FEATURE: the first uses in shadow mode: intake type and tier, fm find lead triage, embedding dedupe of captures, each logged beside the path it would replace
FEATURE: model layer surfaces: MCP decide tool, fm doctor backend health, the site's Model layer page, the AGENTS.md line, MASTER, README and CHANGELOG
```
