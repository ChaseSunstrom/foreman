# Sampo's own model, generic across every project built with Sampo — brainstorm catalogue (2026-11-04)

Request (T-2973): "should we/could we train a model to fit sampo better? like a better kev/whatever to do more things and more than just that too?" … "a generic model … not just the sampo repo itself, but other things made with sampo … brainstorm on features the model should have, like what it's trained on".

Run: `sampo ideas` with 9 lenses (user value, unspoken needs, capability map, approaches, reliability, simplicity, bold bets, grid, blind spots), 2 rounds: 235 distinct ideas in `research/brainstorm-20261104-081614/ideas.md` (every lens file beside it). Clustered below into 13 capabilities; every idea number refers to that index's order.

Grounding (canaries: `def shadow_uses` and `def live(` found in models.py; `plant` found in louhi.py; `def recall` found in recall.py — so an empty search for the "new" terms below could have found them):
- Exists: per-use adoption gated on an exam (`models.live`, 'model-live: USE' decision rows, shadow mode otherwise; T-2486, T-2894); the model bench over 200 held-out closed tasks (T-2886); Louhi's seeded exam that plants one defect per throwaway repo in six languages from templates; lexical recall (BM25, recall.py); the failure taxonomy (T-2926/T-2948); the loop breaker (T-2966); the planner split (T-2945).
- New (searched three phrasings each, none found): a retrieval/kNN decider, abstain with fallback, leave-one-project-out scoring, a training export with provenance and exclusion flags, any fine-tuning (LoRA/QLoRA), a Ward classifier, a user-taste model, per-project adapters, defect planting in real repos.

## Clusters (value 1-5 · effort · risk · mark)

A. Training lake — one flat, provenance-tagged export across all projects (ideas 17, 18, 27, 31, 46, 55, 59, 60, 72, 90, 98, 99, 100, 111, 113-116, 145, 154, 155, 167, 186, 191, 202, 213, 215, 227, 231). Rows from every project's briefs, ledgers, Smith journals and exam grades; labels from outcomes (done-and-held / reverted / later-fixed = regret); project ids and names stripped; time split and dedupe; per-project opt-out and sensitive repos excluded by real path; Claude-written text refused (only user, tool and local-model text); tool-result text quarantined; null-tolerant; project weighting so Sampo's own repo doesn't dominate; old names canonicalised; poisoned-row canaries. Value 5 · M · low · BUILD (everything else stands on it).

B. Measurement and adoption — leave-one-project-out bench, abstain, per-slot registry (1, 7, 16, 20, 28-30, 33, 38, 48, 56-58, 68, 71, 74, 76, 89, 97, 101, 102, 110, 117, 157, 171, 174, 177, 178, 180, 184, 188, 190, 195, 208, 218, 222, 223). Partial: models.live already gates a use on an exam row. New: whole projects held out, a coverage-vs-accuracy curve with abstain falling back to today's rules, a statistical floor for adoption, auto-revert when live agreement drops, a flip report per generation, per-language scores. Value 5 · M · low · BUILD.

C. Baselines before any training — retrieval/kNN decider over closed briefs, few-shot retrieval on the 27B, grammar-constrained decoding (44, 70, 103, 149, 150, 163-166, 170, 172, 175, 189, 197, 199). Value 4 · S · low · BUILD (the bar every trained head must beat; may win outright).

D. Decider heads, the better Kev — frozen bge-m3 embeddings plus tiny trained heads per decision (type, tier, route, approach choice, size/time, files touched, verify suggestions, vacuous-verify score) (6, 39, 45, 49, 50, 73, 84, 126, 130, 152, 153, 192). Value 5 · M · low · BUILD (= T-2970, now generic and gated by B and C).

E. Outcome verifiers — will this close hold (false-done judge), will this brief survive, resembles reverted work, stale premise, blast radius, co-change companions, tests a diff will break (2, 3, 15, 32, 47, 77, 85, 127, 138-140, 143, 205, 224). Value 5 · M · med · BUILD the close-holds verifier first (exp 2's main problem: closes that aren't fixes).

F. Smith actor distillation — verified runs only (durable success, not just green), rejection sampling and preference pairs with loops and refusals as negatives, best-of-N with tests as selector, a loop/dead-run predictor from the journal prefix, an error-to-escalation router, a tool-output compressor, the 27B as teacher (4, 5, 22, 26, 34, 41, 52, 61, 65, 67, 79, 86-88, 104, 159, 161, 168, 193, 198, 201, 203). Value 5 · L · med · BUILD (= T-2971, now with these parts).

G. Scenario minting — plant defects by mutation in any Sampo project's real code in throwaway worktrees, graded by its own tests; scenarios from lessons; canary projects; an open leaderboard (11, 36, 69, 95, 160, 206, 221). Partial: Louhi plants from templates. Value 4 · M · med · BUILD (the actor needs far more than 18 runs of verified scenarios, across real codebases).

H. Generic transfer and per-project fit — per-project LoRA adapters on a shared base kept local, cold start from nearest sibling projects, a project fingerprint, a contrastively tuned embedder for cross-project recall, share weights not text (8, 10, 23, 24, 35, 37, 42, 54, 81, 83, 91, 109, 123, 134, 144, 148, 169). Value 4 · L · med · LATER (captured; needs A, B and a base first).

I. The user's taste — accept/reject history as an interruption filter and a funnel/moons prefilter, pre-answer routine asks, draft steers before they're said, rank the queue by what the user picks, late asks as blind-spot labels, silence and undo as labels (9, 14, 19, 25, 43, 78, 82, 92, 94, 107, 121, 122, 129, 133, 135-137, 142, 147, 156, 196, 225, 234). Value 4 · M · med (privacy, over-trust) · LATER (captured; a moons-accept head is the first slice).

J. Ward models — an advisory risk head that may only tighten the rule-based guard, with an attacker probing it (12, 40, 51, 62, 93, 108, 124). Value 3 · M · high · LATER (captured; the guard stays rule-based, a model may only ask, never allow).

K. Serving and ops — GPU scheduling that yields to Ollama and the funnel, resumable VRAM-safe training, pinned serving stack, settings proven at the endpoint, per-slot quantisation and context from the bench, slot metering, quirk probes at install, model state moving with the home, a ship gate without a GPU (21, 63, 64, 105, 112, 118, 119, 158, 176, 179, 183, 212, 214, 216, 226, 228-230). Value 3 · M · low · BUILD the scheduler inside F; the rest captured.

L. Transparency — which slots use a model with a veto, one-line explanations, abstain reasons on the close line, a no-model switch per project, agreement and regret numbers, "model saved you" receipts, a wrong-calls digest (13, 106, 125, 128, 131, 132, 135, 141, 194, 209, 211, 219, 220). Value 4 · S-M · low · LATER (captured; lands with B's registry).

M. Wild research — a world model of tool results to rehearse plans, a ledger language model for surprise, a readable rulebook model, an Elo ladder of models and scenarios, a time-travel backtest, unanimous voting across heads, rename fuzzing (53, 66, 80, 96, 146, 185, 207, 210, 233, 235). Value 3 · L · high · LATER (captured as one research task).

## Slate (decided; the user is away)

1. A — the training lake export (M), first.
2. C — the retrieval/kNN baseline decider (S).
3. B — leave-one-project-out bench, abstain and adoption floor (M).
4. D — T-2970 the decider heads, gated by 2 and 3.
5. E — the close-holds verifier (M).
6. G — scenario minting in real repos (M).
7. F — T-2971 the distilled actor (L), last: it needs 1, 5 and 6.
Later (captured): H, I, J, K's remainder, L, M.

Why this order: every model needs the same data and the same honest bar; a retrieval baseline may already beat the bench's best decider at no training cost; the close verifier answers the problem the second uplift exam exposed; the actor needs verified scenarios at scale before rejection sampling can work.
