**Verdict:** approve with nits. This covers only T-2865's own code, which in this diff is two later patches to moonscale.py, one hunk in rune.py and the StoreLock tests. I could not run anything; the review is from reading.

## lens: intent / edge / maintainer (the only ones that apply to this slice)

- MEDIUM — `plugin/lib/sampo/moonscale.py:124-134` (`status`) — Duplicates and merges are never counted, so the per-stage counts do not add up.
  - Only `kept` and `rejected` are summed. The exact and embed stages emit `dup` (lines 842, 858) and the tier stage emits `merged` (line 904), so those rows appear in no bucket.
  - Reproducer: seed two identical moons, run `fm moons funnel --stage exact`, then `fm moons funnel --status`. It reports `exact 1 kept, 0 rejected` and the dup is invisible. Exact and embed can never show a non-zero rejected count.
  - Fix: add `dup` and `merged` counts to each stage's dict and to `status_line`, with a test where a row is duped.
  - Confidence: high.

- LOW — `plugin/lib/sampo/moonscale.py:124-134` — `status` counts the rows whose last event is at a stage, not how many passed through it.
  - After a complete run every row has moved to novelty, so exact, embed, kill and tier all read "0 kept".
  - The docstring says this ("a row's last event there"), but "kept" in the output line suggests funnel counts. The AC "funnel counts" is better served by cumulative counts per stage.
  - Fix: count events per stage from the full funnel log, not just each row's last event, or label the line "resting at".
  - Confidence: medium.

- LOW — `plugin/lib/sampo/rune.py:4060-4069` — `--status` is honoured only for `funnel`.
  - `fm moons families --status` falls through to `store_lock` and `families(p)`, which rewrites `families.json` although the user asked for a read-only report.
  - Fix: reject `--status` with any verb other than `funnel`, or make it work for families too.
  - Confidence: high.

- LOW — `plugin/lib/sampo/moonscale.py:109` — `store_lock` creates the moons directory and `.funnel.lock` before the lock is taken.
  - `families()` deliberately writes nothing when there are no survivors and no `families.json` (line 1017), but `fm moons families` on an empty project now creates `moons/.funnel.lock`.
  - Fix: skip the `makedirs` when the directory does not exist and use a lock location outside the store, or accept it. No test pins either behaviour.
  - Confidence: medium.

Checked and found fine:
- **`_ask` writer routing:**
  - A sensitive project still raises before any cloud call.
  - The `writer="local"` path raises `LocalOnly`.
  - `tests/test_small_cards.py:251-264` covers the routing.
- **Lock:**
  - `os.open` makes the fd non-inheritable, so child model processes do not hold the lock.
  - The only unlocked `funnel()` callers, `louhi.py:1146` and its `_gen_funnel`, use a scratch store.
- **`ORDER[ORDER.index(s) - 1]`:** the first stage's predecessor is "write", not a wrapped index.

## Acceptance criteria
- Candidate store with grid cell, line and fate; the write rejects internal-only or untestable moons: `add()` at `moonscale.py:209-227` records a `write` event for every row, rejected ones included. Not verifiable here (tests not run).
- Grid generator, routing to local models or Haiku: `_ask` routes as described, with the strongest model used only for `cheap=False`. Not verifiable here (tests not run).
- Families, with the climb and floor on them: `families()` at lines 987-1021 clusters by single link. The climb and floor code is outside this diff. Not verifiable here.
- 10,000 candidates and the Moons page showing families, tiers, stage, evidence and funnel counts: not verifiable from this diff, which holds no site/genesis page change. The `status` counts (above) are the funnel-count surface in it.

## Implicit decisions
- The lock is a flock on `.funnel.lock` in the moons directory, with the pid written inside.
- A busy lock exits 1 with the message on stderr.
- Sonnet is priced at 5x the Haiku fallback.
- `status` reports where each row currently rests (its last event), not pass-through counts.

## Not checked
- site/genesis and the Moons page: not in the diff, and the diff shows no `moons.py` change.
- All other files in the diff: live.py, louhi.py, smallcards.py, verifier.py, traces.py, jeffexport.py, lake.py, mint.py, models.py, cli.py, core.py, CHANGELOG, MASTER.md, docs/map, plugin/web/live (so no design lens), fixtures and tests other than `test_moons_scale.py`.
- Pre-audit secret hits in live.py and test_live.py: outside this scope.
- Nothing was run.

**Noticed:** none
