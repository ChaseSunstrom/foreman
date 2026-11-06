---
id: T-2877
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-04T03:33:39Z
updated: 2026-11-04T03:33:39Z
steer_method_rate: 0.218
---
# Use the local models freely and heavily for ideation, drafting, brainstorming, variant…
## Raw request
> feel free to go absolutely fucking wild with the local models and use them as much as you want for ideas, no hold backs and such, but I do want you to also examine their behaviour and genuinely make sampo able of using/controlling them and making them match your capability, because we both know smaller models arent great at what youre doing, so I want you to make it so they are too, and also create thousands of skills/playbooks/ui instructions/designs you create for smaller models that aren't as good at it and such, and other things as well, and put that into each tower gen too
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- Use the local models freely and heavily for ideation, drafting, brainstorming, variant generation and bulk work, with no self-imposed caps on how much. Cost is only local compute, and anything that leaves the machine stays behind the user's grant.
- Study how each local model behaves before relying on it, and record the findings per model. That means where it fails, which formats it follows, its context limits, its tool-calling reliability, its drift and loops, and its speed. Re-run the study when models are added or changed.
- Build into Sampo the ability to drive and control local models. This covers routing tasks to the right model, decomposing work into small steps, constrained or structured output, tool-call repair, retries with feedback, verification passes, loop and drift detection, and escalation to a stronger mod…
- Aim for local models to match frontier-model capability on the work Sampo does, closing the gap with scaffolding rather than hoping. Measure it with a repeatable eval that runs the same tasks on both and tracks the gap per task type. Report the real numbers, including where they still fall short.
- Create thousands of skills, playbooks, UI instructions, designs and similar assets written for weaker models. Each one should be explicit and stepwise, with worked examples, exact output formats, checklists and failure-recovery notes.
- Cover every area Sampo touches: planning, proving and testing, finishing, code, UI and design, docs, debugging, refactoring and tooling. Do not stop at the examples the user named, and add other asset types that help weaker models.
- Hold the generated assets to a quality bar: deduplicate them, validate their format, and test them by running a local model against them. Prune or revise assets that don't measurably help, so volume never replaces usefulness.
- Organize the library with an index, tags, per-model variants and versioning, so Sampo can select the right asset for the task and model at hand.
- Include the full current library, the model-behaviour profiles and the control layer in every tower generation, and regenerate or refresh them as part of each generation. Check that a fresh generation contains them and works with them.
- Act on this directly: build, generate, run and test. Don't just propose it.
- Keep irreversible, destructive or outward-facing actions behind the user's grant. That includes publishing, spending money, sending data to external services, and deleting or overwriting existing files. Check a target before replacing it.
- Report outcomes faithfully. Say what was generated, what was tested, what failed and what was skipped.
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
- 2026-11-04T03:33:39Z created
## Follow-ups captured
