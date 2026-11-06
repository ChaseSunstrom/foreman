# Brainstorm — lens: ecology: succession and niches

- **Replay the funnel as primary succession on a bare repo** — FEATURE — value 4 — effort M — risk low — category: succession
  Why: assumption: new installs get the full ceremony at once, while the pack shows ceremony costs (2,733 chars, 75,758 tokens, 48–76 per turn) growing. Ecological primary succession adds pioneers (Ward, plan-before-edit) first, and later species (lessons, exams, moons) only when soil exists (history, tests, ledgers).
  Done when: `sampo stage` prints one of pioneer/shrub/climax for a repo from measured signals (commit count, test presence, closed tasks), and a fresh-repo e2e shows only the pioneer set injected.

- **Compute a keystone score per verb by simulated extinction** — FEATURE — value 4 — effort M — risk low — category: keystone
  Why: the pack's open questions ask which capability the user would notice first if switched off for a week, and ledgers don't record it. The score is built from the hook and verb call graph plus the ledgers: how many other verbs' outputs degrade when one is removed.
  Done when: `sampo keystone` ranks the verbs, and removing the top one in a scratch clone fails more e2e/exam checks than removing the median one.

- **Give each funnel cell a carrying capacity** — PERFORMANCE — value 4 — effort S — risk low — category: moons funnel
  Why: the 10,000-candidate grid risks monoculture, with near-duplicate families filling the cheap stage while local models spend time on them. A per-cell cap, with overflow evicted by lowest novelty, bounds the store and GPU time.
  Done when: after a seeded 10,000-candidate run, no cell holds more than N survivors, evictions are logged in the funnel log, and the stage-2 count drops against an uncapped run on the same seed.

- **Gate funnel stage promotion on a diversity floor** — FIX — value 3 — effort S — risk low — category: moons funnel
  Why: the user pushed back that "the moons aren't that moon-y", which is what a collapsed pool produces. A Shannon-index check across families should stop a stage from promoting a homogeneous set.
  Done when: a planted all-one-family batch is refused promotion with the index printed, and a mixed batch passes.

- **Keep a seed bank with germination predicates** — FEATURE — value 4 — effort M — risk low — category: not-yet
  Why: the standing rule says failed spikes go to not-yet.md with a blocker, and every Seed retries what a new capability may unblock. Today that is manual prose. Each entry gets a machine-checkable wake predicate (model ID appeared, verb exists, blocker task closed, endpoint up).
  Done when: `sampo seeds wake` lists the entries whose predicate flipped and files a retry task for one, and a test flips a blocker to see an entry wake.

- **Run a prescribed burn on dormant state** — SECURITY — value 3 — effort M — risk med — category: state hygiene
  Why: the 2.4 GB state and the many deferred "Later from T-07xx" tasks are fuel load, and the standing rule forbids killing ideas for ambition. A burn here moves them to a compressed pack with a tombstone and wake predicate rather than deleting, then counts what regrows (re-opened or re-read).
  Done when: `sampo burn --plan` shows the bytes and items by class, apply moves them to a pack with tombstones, and the resprout count appears in the next report.

- **Add a decomposer lane for dead candidates and failed spikes** — FEATURE — value 3 — effort M — risk low — category: reuse
  Why: killed moons and reverted self-edits carry rationale that the funnel log keeps but nothing mines. A cheap local-model lane extracts reusable nutrients (a blocker class, a rubric line, a failure shape) into small cards.
  Done when: after a funnel run, the lane writes at least one card per N kills, each citing a log row, and the next generation's pack includes them.

- **Detect invasive injected text by its crowding of the per-turn budget** — PERFORMANCE — value 3 — effort S — risk low — category: context budget
  Why: assumption: new hooks, skills and imported plugins colonise the per-turn character budget with no owner. Treat the budget as a contested resource and report each source's share and growth rate.
  Done when: a doctor line lists the top three sources by share, and a synthetic new injector pushing past its quota fails the ship gate.

- **Wild: Quorum-gate dangerous promotions across independent lineages** — FEATURE — value 4 — effort M — risk med — category: promotion
  Why: wild — the pack shows cold reads where a single judge's verdict decides. Require agreement from judges with different model families and different prompts before a moon is crowned, as bacteria do before they commit.
  Done when: a moon promoted only by one lineage is held with "no quorum" printed, and a test with three agreeing lineages passes it.

- **Wild: Grow a mycorrhizal lesson network between lanes** — FEATURE — value 4 — effort L — risk med — category: lessons
  Why: wild — lanes and repos learn alone, while T-0217 wants lessons with a confidence signal. A shared graph lets a lesson move from a lane that passed first time to the lane that needs it, weighted by co-recall, and a dying lane leaves its nutrients behind.
  Done when: a lesson learned in lane A is injected into lane B on a matching task kind, with its edge weight shown, and removing the edge removes the injection.

- **Wild: Send a hyphal alarm from a lane that hits a Ward block or a poisoned file** — SECURITY — value 3 — effort M — risk med — category: lanes
  Why: wild — lanes run in parallel and each rediscovers the same injection or bad file. A tiny content-hash broadcast lets sibling lanes pre-tighten, as stressed plants prime their neighbours.
  Done when: a planted poisoned file blocked in lane A causes lane B to refuse it before its first read, within one tick.

- **Set ceremony by repo's succession stage in the Smith local arm** — PERFORMANCE — value 3 — effort S — risk low — category: local models
  Why: local models on the pack's "uplift" work lose context to ceremony that suits a mature repo. Early-stage repos get the thin card.
  Done when: Smith on a local model in a pioneer-stage repo receives at most N characters of injected text, and its exam score does not drop against full ceremony.

- **Wild: Hold a mast year for moons** — FEATURE — value 3 — effort M — risk low — category: moons funnel
  Why: wild — instead of a steady trickle, the funnel idles until the local endpoint is quiet, then floods one night with a synchronized burst at 10,000 scale, which swamps the dedupe predators and lets rare families survive. A fallow stretch precedes it.
  Done when: a `sampo moons mast` run produces its batch in one window, with the survivor-family count above that of the preceding trickle runs.

Next question: Which of these ecological signals (stage, keystone score, diversity index) is the user willing to see surfaced unprompted, given they dislike being asked for things?
Next question: What does the funnel log record about why each candidate died, and could a decomposer actually learn from that?
