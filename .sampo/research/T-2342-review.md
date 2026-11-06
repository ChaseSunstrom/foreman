T-2342 review (fm-reviewer, one pass): changes needed; fixed in cd4ceb3a before merge (DoorGate and tidy tests red first; the rest written alongside).
MEDIUM fixed: any 'Undo:' text lifted a park: only a restore command with an existing source counts.
MEDIUM fixed: _named matched substrings and negations: whole tokens, a destroy verb in the clause, no negation.
MEDIUM fixed: steps added or edited after focus were never classified: step/ac add|edit gate too.
MEDIUM fixed: destructive verify commands were two-way: verify rows get paths and are gated.
MEDIUM fixed: gitignored .env/*.db read as regenerable: local unless under build/dist/node_modules/__pycache__/.venv/target/.cache.
MEDIUM fixed: globs/env vars/bare names missed; a second verb list missed sed -i, >, tee, dd, cp/mv onto files, gzip, shred, truncate and prose verbs.
LOW fixed: repo/ancestor paths park; FIFOs skipped; gate errors become a PolicyError; snapshot drift warned at step done; fm tidy ages snapshots; the two-way nudge wording.
Open: drift warning silent when the path was deleted; verbs remain a regex beside the guard (no shared write-target parse).
