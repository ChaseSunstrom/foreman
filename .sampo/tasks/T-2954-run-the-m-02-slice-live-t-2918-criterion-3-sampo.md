---
id: T-2954
type: RESEARCH
tier: S
status: blocked
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-04T10:28:00Z
updated: 2026-11-05T01:20:00Z
group: live runs when endpoint frees
---
# Run the M-02 slice live (T-2918 criterion 3): sampo moons regen --slice over every leaf…
## Raw request
> Run the M-02 slice live (T-2918 criterion 3): sampo moons regen --slice over every leaf module under 260 lines with its own test file, on the local 27B with Haiku as the second approach, once the 10k moons funnel frees the endpoint; file bench/moonshot/m02-slice-result.json with ran true and the M-02 stage line (Advanced at 2+ round trips), replacing the placeholder
## Interpretation
Reading 1 (taken): run moons regen --slice live on the local 27B (Haiku second) over every leaf module under 260 lines with its own test file, filing bench/moonshot/m02-slice-result.json with ran true and the M-02 stage line, so M-02 has a real result instead of the placeholder. Reading 2 (ruled out): a dry run or a sample: the criterion asks for the live slice.
## Assumptions (confidence)
## Acceptance criteria
- [ ] bench/moonshot/m02-slice-result.json reads ran true with every eligible leaf's outcome, and the moonshot catalogue's M-02 has its stage line (Advanced at 2+ round trips, else the blocker) — verify with `python3 -c "import json; d=json.load(open('bench/moonshot/m02-slice-result.json')); assert d['ran'] is True, d"`
## Non-goals
## Approach (options → choice → why)
1) use what exists: sampo genesis moonshot regen --slice as built (T-2918), run when the 27B endpoint is free: likely outcome: a filed result and a stage line. 2) on Haiku only: fails if: the slice is meant to test the local model first. 3) do less: a handful of leaves: fails if: the criterion names every leaf. Choice 1 (85%).
## Risks and rollback
## Execution prompt
## Steps
1. [ ] run the slice on the 27B when its endpoint is free; file the result and the stage line  <- CURRENT
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-04T10:28:00Z created
- 2026-11-05T01:20:00Z planned: it has criteria and steps
- 2026-11-05T01:20:00Z set approved=True
- 2026-11-05T01:20:00Z blocked: needs the 27B endpoint free: T-3006's reasoning arms hold it now and T-2878's Jarvis lane follows; runs between them
## Follow-ups captured
