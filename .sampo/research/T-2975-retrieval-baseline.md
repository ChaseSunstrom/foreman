# T-2975: a retrieval baseline for Sampo's own deciders

Live bench on 2026-11-04: 1,585 closed briefs train, 200 held out. bge-m3 ran on local Ollama, k=7, and a use abstains under 4 votes of 7.

| Use | Contestant | Accuracy (answered) | Coverage | Accuracy (abstain counted wrong) |
|---|---|---|---|---|
| intake type | majority | 0.595 | 1.0 | 0.595 |
| intake type | k-NN (bge-m3) | 0.766 | 0.92 | 0.705 |
| intake type | BM25 | 0.761 | — | — |
| intake tier | majority | 0.58 | 1.0 | 0.58 |
| intake tier | k-NN (bge-m3) | 0.708 | — | 0.655 |
| intake tier | BM25 | 0.674 | — | — |

**Reading the table**
- The best earlier type decider scored 0.73.
- Retrieval beats it on the questions it answers, with no training at all.
- Tier beats majority for the first time.

**Why it matters for the generic model (brainstorm-20261104-model)**
- Retrieval is the floor every trained head must beat on whole held-out projects. T-2976 runs that leave-one-project-out comparison.
- It costs nothing to keep current: the nearest neighbours come from whatever briefs the project, or the lake, has today.

**The cache**
- Vectors are cached per model and text hash in Sampo's state (research/models/vectors.jsonl under the project's state dir), not in the repo.
- A rerun embeds only new briefs.
