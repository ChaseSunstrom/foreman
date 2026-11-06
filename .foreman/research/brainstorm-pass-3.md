# Brainstorm pass 3 (2026-10-04) — grounded slate

Source: research/brainstorm-20261004-021539 (bold bets, simplicity, user-love, security and safety × 2 rounds, past passes 1–2 and two earlier lists; 85 new titles).

## Grounded and kept (the slate)
1. The guard reads what a command runs, not just the command — "census exec channels beyond git". Probed with a payload only a parse catches (rm -rf ~/Documents): `bash FILE`, `sh FILE`, `. FILE` and `source FILE` pass unchecked (the guard never opens the script), and so do tar --to-command / -I / --checkpoint-action=exec, ssh -o ProxyCommand / LocalCommand, rsync -e, zip -TT, less '+!cmd', vim -c '!cmd', BASH_ENV / PROMPT_COMMAND / LD_PRELOAD / NODE_OPTIONS=--require, and sed's e command. Writing a script to the scratchpad and running it is a common, honest pattern, so the script file is the channel that matters most. SECURITY M.
2. One `fm second` primitive for the review family — "merge four review items into one primitive with pluggable seats". T-0230 (installed review skills as lenses), T-0232 (debate pair), T-0233 (shadow plan review on another model) and T-0235 (daily second-Foreman review) all mean: a second, independent read of a plan or a diff, from a seat (a lens, a skill, a rival model, the reviewer's own first verdict). FEATURE M–L, built as the review-family batch.

## Grounded and dropped
- `fm guard try` dry-run — the block message already explains the verdict; fm replay covers the corpus. Not worth a verb.
- Show only ten verbs / sunset unused verbs — fm help's tiers already lead with the everyday ten; fm usage lists unused commands.
- Run every README command as a test, hook tamper detection, secret scrubbing at write, since-you-left card — exist (fm docs, doctor core integrity, redact, while-you-were-away).
- Jail verify commands in a no-network sandbox — needs bwrap/unshare per platform; not stdlib-portable.
- Interpreter code (python -c 'os.system(...)') — arbitrary by nature; the guard stays a mistake-catcher, not a sandbox. Script files are the realistic channel.

## Kept for later passes
- Trace each clause of the request to a criterion (mechanized intent check).
- fm undo ID with a verified rollback.
- Lint the final message's ✓ lines against the ledger.
