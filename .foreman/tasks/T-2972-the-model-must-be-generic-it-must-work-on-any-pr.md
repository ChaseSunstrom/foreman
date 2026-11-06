---
id: T-2972
type: FEATURE
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-04T14:04:21Z
updated: 2026-11-05T04:44:34Z
steer_method_rate: 0.218
---
# The model must be generic. It must work on any project built with Sampo, not just the…
## Raw request
> we will want it to be a generic model in the sense that we don't want it to just work on the sampo repo itself, but other things made with sampo, and maybe brainstorm on features the model should have, like what it's trained on and such, etc., I will be gone again so don't ask any questions
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- The model must be generic. It must work on any project built with Sampo, not just the Sampo repo. Nothing in its code, config, prompts, fixtures or training data may hardcode Sampo-repo paths, names, layout or conventions.
- Anything Sampo-specific must be learned or discovered from each project at run time. Examples are the project's Sampo artifacts, plans, proofs, task and verification formats, and its languages, test commands and docs. These go behind a documented adapter or config interface, not inline assumptions.
- Check generality with evidence. Run and evaluate the model on at least two projects other than the Sampo repo, preferably differing in language, size and structure. Report the results per project, and flag any case where behavior only works on the Sampo repo as a defect.
- Brainstorm the model's feature set in a written design doc kept in the repo. Cover what it does (plan, prove, finish work), its inputs and outputs, how it handles unfamiliar project structure, how it explains its decisions, and how it fails safely. Mark each feature as proposed, recommended or reje…
- The brainstorm must cover training and data: what the model is trained or tuned on, data sources and their licenses and provenance, per-project versus pooled data, and held-out projects for evaluation. It must also cover contamination and leakage between train and eval, privacy and secret scrubbing…
- Define how success is measured. State concrete metrics and acceptance checks for generality, such as pass rate on unseen projects and the gap between Sampo-repo and other-project performance. State the baselines they are compared against.
- Keep the docs, tests, examples, configs and any eval harness consistent with the generic design. Update every surface the change touches, so no README, schema or test still assumes the Sampo repo only.
- The user is away, so do not ask questions. Decide on a reasonable default, act, and record each assumption and open decision in a clearly labeled section of the design doc for the user to review on return.
- Keep outward, destructive and irreversible actions behind explicit user approval. That covers uploading or training on any project's code or data, using external services or paid compute, publishing, pushing, deleting or overwriting. Do the local, reversible work (design, code, offline evals) and l…
- Report outcomes faithfully on return. Give what was done and verified, what was skipped or failed with its output, and which decisions were assumed.
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
- 2026-11-04T14:04:21Z created
- 2026-11-05T04:44:34Z dropped: covered: the model brainstorm (T-2973) made sampo-decide generic across projects: trained on every project's lake, scored on a held-out project (T-2970), adoption needs 3+ held-out projects
## Follow-ups captured
