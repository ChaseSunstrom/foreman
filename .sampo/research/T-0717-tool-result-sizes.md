# T-0717: where tool-result tokens go (30 days, all local transcripts incl. subagents)

Measured with scratchpad/sizes.py over 64,393 tool results (~31.7M tokens, chars/4).

| tool | results | tokens | p50 | p95 | p99 | top 5% share | >5k-token results |
|---|---|---|---|---|---|---|---|
| Read | 8,147 | 15.9M | 819 | 9,446 | 14,042 | 31% | 925 results = 54% of Read tokens |
| Bash | 45,043 | 13.8M | 104 | 1,256 | 2,880 | 37% | 82 results = 4% |
| Grep | 4,143 | 1.3M | 129 | 1,273 | 2,528 | 33% | 0 |
| WebFetch | 251 | 0.12M | 268 | 1,330 | 8,061 | 45% | 5 = 32% |

- Read results over 3k tokens, by extension: .diff 3.24M (reviewers reading `fm audit prep` diffs), .py 2.33M, .rs 1.10M, .ts 1.04M, .volt 1.00M, .md 0.63M.
- Bash results over 3k tokens, by command: sed (ranges) 537k, cd … 383k, cat 365k, grep 201k.

## Conclusions

- Bash output isn't the lever. It is long-tailed but small per result, and the runners are already piped or quiet (T-0702).
- Unchanged re-reads aren't the lever either: Claude Code already stubs them (T-0702).
- Big full-file Reads are the lever: 925 results over 5k tokens hold 8.6M tokens a month.
  - Audit diffs: 3.2M. `fm audit prep` could exclude fixtures, lockfiles and generated files (listed by name and line count) and split a big diff into per-file parts read on demand. When I trimmed fixtures by hand on T-0701, 117 KB became 63 KB.
  - Source files: an outline-first read. A full Read of a file over ~600 lines gets its outline and a pointer to read ranges. The PostToolUse hint arrives after the tokens are spent.
