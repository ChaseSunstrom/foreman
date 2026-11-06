# T-2970: sampo-decide, the first model trained on Sampo's own outcomes (2026-11-04)

## What
A rank-16 LoRA adapter on Jeff v1.3 (Qwen3.5-0.8B base, decision readout), trained on this box's RTX 5070 Ti.

**Training setup:**
- lr 1e-4, effective batch 16, 3 epochs;
- dev loss selected step 130;
- about 20 minutes.

**Data:** the training lake, labelled only by outcomes and by the user's own words:
- **intake-type:** only where the user tagged the request (FIX:, FEATURE:, ...);
- **intake-tier:** from the realized scope size;
- **close-holds:** from held vs fixed later or reverted.

**Splits:**
- train 1,462 Examples, dev 116, temperature 104;
- split by whole projects;
- one project held out of every fold.

**Serving:** by the Jeff server as `sampo-decide`, profile `jeff-sampo-decide`.

## First held-out result
Bench run m20261104-130414488 (`sampo exam models --loo --limit 200`). The adapter is scored only on the one project it never saw; 25 requests per use.

| use | sampo-decide | majority | BM25 k-NN | Jeff triage | Jeff base |
|---|---|---|---|---|---|
| intake-tier | **0.64** | 0.12 | 0.32 | 0.40 | 0.28 |
| intake-type | 0.76 | 0.72 | 0.63 | 0.56 | 0.52 |

## Reading
- **Tier** has the largest lead any contestant has shown on this question (+0.52 over the majority on that project).
- **Type** is level with the majority (+0.04).
- **One project, 25 rows, isn't evidence for adoption.** The floor needs 3+ held-out projects with none worse. The next step trains one adapter per held-out project (8 trains, about 20 min each on this GPU) and scores each on its own project (captured).
- **Several Ollama decision contestants were missing from this run.** kev, tev1 and d3 were being re-pulled after the store was lost, so this run reads "GONE" for them. The flip report's kev:4b live → shadow is that absence, not a loss.
