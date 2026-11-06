---
id: T-1788
type: FEATURE
tier: M
status: dropped
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-10-23T15:03:31Z
updated: 2026-10-23T15:34:49Z
---
# 3D soak and frame budget in a real browser: fm scene soak FILE drives fmshot's Chrome on a
## Raw request
> 3D soak and frame budget in a real browser: fm scene soak FILE drives fmshot's Chrome on a --hud build (globalThis.__fmScene) for N seconds, flags growing geometries/textures and a p95 frame time over budget; needs a local three.module.js and a WebGL path headless Chrome allows (failIfMajorPerformanceCaveat refuses SwiftShader), so it waits until both can be found here (from T-1530)
## Interpretation
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
- 2026-10-23T15:03:31Z created
- 2026-10-23T15:34:49Z dropped: covered by T-1530: fm scene soak runs the --hud build in headless Chrome with a local three.js, checks leaks, the frame budget and dispose
## Follow-ups captured
