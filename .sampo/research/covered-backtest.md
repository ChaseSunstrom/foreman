# Already-built nudge backtest (T-2546)

Positives: 46 tasks dropped with an already/built note. Negatives: 400 done tasks. Each row matched only against MASTER.md clauses of earlier tasks.

```
min 2 share 0.5: built drops 4/46, new work 31/400
min 2 share 0.6: built drops 2/46, new work 15/400
min 2 share 0.7: built drops 0/46, new work 8/400
min 2 share 0.8: built drops 0/46, new work 5/400
min 3 share 0.5: built drops 4/46, new work 29/400
min 3 share 0.6: built drops 2/46, new work 13/400
min 3 share 0.7: built drops 0/46, new work 6/400
min 3 share 0.8: built drops 0/46, new work 3/400
min 4 share 0.5: built drops 4/46, new work 25/400
min 4 share 0.6: built drops 2/46, new work 12/400
min 4 share 0.7: built drops 0/46, new work 6/400
min 4 share 0.8: built drops 0/46, new work 3/400
```

Bar: flag a third or more of the built drops at under 1 in 10 of new work. No threshold meets it (best recall 4/46 at 31/400). Verdict: word overlap with MASTER clauses is too blunt; nothing prints at capture. A future matcher (embeddings through the model layer) must beat this grid on the same rows.


## Removed (T-2587, 2026-11-02)
The matcher (fmrecall master_clauses, covered_master, backtest_built) and `fm recall --backtest-built` were removed: nothing used them after this backtest met no bar. To rebuild, restore them from commit e51d82b0 (the last commit holding them) and rerun the grid on the same two id<TAB>title files.
