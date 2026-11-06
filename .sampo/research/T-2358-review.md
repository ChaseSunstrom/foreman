T-2358 review (fm-reviewer, one pass): changes needed; all fixed test-first before close.
MEDIUM fixed: a hook's ms growth was paid by other hooks' drops (5-run vs 20-run p95 made the doctor read low everywhere): ms is judged alone; ship and doctor both bench 5 runs (one estimator).
MEDIUM fixed: one key held CPU time when loaded and wall time otherwise: only unloaded wall-time p95 is measured.
MEDIUM fixed: a 0 size (a failed hook) counted as a 100% cut: sizes must be over 0.
MEDIUM fixed: trimming the largest SKILL body (loaded on demand) paid for always-on growth: only POOLED always-on metrics pay each other.
Fixed from 'noticed': every ship re-recorded the footprint, absorbing growth: the record is now a ratchet (a grown metric keeps its old value).
LOW fixed: injection_sizes catches OSError/SubprocessError (timeout 120 as before); MASTER fm ship line reworded; parameter renamed extra.
