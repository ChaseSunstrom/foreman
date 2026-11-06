T-2340 review (fm-reviewer, one pass): changes needed; fixed in 8c9dcf10 before merge, red first.
MEDIUM fixed: a spike could reach main via pick() after the L was re-tiered (the refusal was CLI-only): merge() refuses spikes for every caller; pick/score refuse a re-tiered design race.
MEDIUM fixed: builder-written spike notes entered the trusted L plan undefanged: c.defang(_flat()).
MEDIUM fixed: design text could join the last option and satisfy its outcome/exists/do-less checks: _split_options cuts at the Design race marker first.
MEDIUM fixed: --score after a pick overwrote 'Picked': refused once spikes are closed.
LOW fixed: spike lanes skipped by finished_lanes/awaiting_merge; unapproved explore L refused; ties toward the stated option; empty spike branches kept.
Open: finding 3 tested on _split_options directly, not through _content_gaps; a non-design race can still be re-scored after its pick.
Self-change gate (T-2352) passed the branch twice (first merge conflicted on test_lanes, second landed).
