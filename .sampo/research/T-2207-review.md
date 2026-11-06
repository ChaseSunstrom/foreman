# T-2207 review (one fm-reviewer pass, five lenses): changes needed → fixed
- adversary HIGH: an earlier fail, unchanged, became accepted after one later miss (defeated T-2205's "fail again one still unmet"). FIXED: lines still in previous-reads are never accepted; test (find, plan, plan, find → blocks).
- adversary HIGH: a carried fail didn't revoke acceptance. FIXED: a carried line is flagged, so a second fail blocks; test.
- adversary MEDIUM: one unflagged read = accepted. FIXED: two consecutive unflagged reads (seen → lines).
- adversary MEDIUM: no context; exam tail outside the key. FIXED: each line hashed with its nearest heading; key = READ_CHILD + charter + exam tail; tests (moved line, new exam lines block).
- LOW: READ_CHILD not in key. FIXED. LOW: partial quote matching several lines. FIXED: carries only if every matching line is accepted. LOW: carried lines not on record. FIXED: carried_lines in genesis_read.
- state file: guard test added (test_guard_exec_vectors: echo/cp into genesis-accepted.json → state-direct).
- noticed (stale previous-reads quotes after a rewrite): T-2205's design, kept; not captured.
