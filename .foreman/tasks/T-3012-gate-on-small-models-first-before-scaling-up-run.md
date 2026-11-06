---
id: T-3012
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-04T19:35:56Z
updated: 2026-11-04T19:35:56Z
steer_method_rate: 0.218
---
# **Gate on small models first.** Before scaling up, run the compression method on the…
## Raw request
> and if the "smaller" models work with that compression and whatever, we can try the humungous frontier open source ones down to one thats runnable on a single gpu like what I have
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- **Gate on small models first.** Before scaling up, run the compression method on the small models and compare each against its uncompressed baseline. Set the pass criteria beforehand and record them: quality delta (perplexity or task benchmarks), size or VRAM reduction, and throughput. If the small…
- **Move up the ladder without re-asking once the gate passes.** Apply the same pipeline to progressively larger open-weights models, from the largest frontier open-source models down to the largest one that runs on the user's single GPU. Cover the whole range, and don't stop at the first success or …
- **Measure the hardware first.** Read the GPU model, VRAM, driver, system RAM and free disk. Before downloading any model, estimate whether it fits: compressed weights, plus KV cache and activation overhead at the test context length. Classify each model as fits on one GPU, needs offload or multi-GP…
- **Test only what's feasible locally.** For models too large for the GPU, use methods that work within local limits, such as layer-by-layer or streamed compression, or evaluating a subset. State exactly what was and wasn't measured, and never extrapolate a result as if it were measured.
- **Keep the comparison controlled.** Use the same method, settings, eval harness, datasets and seeds across all model sizes. Keep a baseline run for each model. Record results in one table with model, parameter count, compressed size, VRAM used, quality delta and speed.
- **Find and report the limits.** Identify where the method starts to degrade or break as size grows, and which is the largest model that works well on the user's GPU. Report failures, skips and OOMs with their output, not just successes.
- **Handle downloads safely.** Put each model in its own new, empty directory. Take weights only from official or verified sources and check checksums where published. Don't enable `trust_remote_code` or run repo scripts without reading them. Check free disk before pulling large files.
- **Keep it reproducible.** Save scripts, configs, library versions, seeds and raw outputs in a separate directory from the downloaded weights. Update any tests or docs the pipeline touches so the whole ladder can be rerun.
- **Get a grant for anything outward, costly or irreversible.** This covers renting cloud GPUs, spending against the $200 budget, uploading models or results to a hub or any external service, and deleting or overwriting existing models or results. Look at a target before removing it.
## Assumptions (confidence)
## Acceptance criteria
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-04T19:35:56Z created
## Follow-ups captured
