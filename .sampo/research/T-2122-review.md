Verdict: changes needed (1 HIGH, 9 MEDIUM, 3 LOW); reviewer ran nothing (read-only).

## lens: adversary
- HIGH — fm prove --yes-run: a session could pass it itself after the refusal told it how. FIXED: fmguard USER_ONLY_FM gains prove --yes-run (adversarial rows: --yes-run, --yes-r, --yes-run=1, fm --json prove; near misses fm prove . and --limit allowed; literal-scan row).
- MEDIUM — own_tree ran git log/config with only fsmonitor and hooks neutralised; a repo-local user.email forged the check. FIXED: -c log.showSignature=false, --no-show-signature, and the email comes from git config --global; tested with a repo-local email naming someone else.
- MEDIUM — "among the last 50 authors" says nothing about HEAD. FIXED: HEAD's author must be the user.
- MEDIUM — isolation is env-only; the docs claimed more. FIXED: reworded everywhere (runs as the user, with the network) and DBUS_/XDG_/GPG_/PYTHONPATH/NODE_OPTIONS/RUBYOPT dropped too; tested that GITHUB_TOKEN and FOREMAN_HOME don't reach the suite and HOME is the copy's.
- MEDIUM — brace stub could land in the next function after an expression-bodied arrow. FIXED: refused when a ';' comes before the '{' or the '{' is a destructured arrow parameter.
- MEDIUM — a swallowed stub error read as proven. FIXED: instrumentation now writes a marker file instead of raising; proven needs the control's marker present and the candidate's absent; tested with a test that reaches the function by name inside try/except.
- LOW — repo text printed unquoted. FIXED: symbol and the suite's last line are JSON-quoted.

## lens: edge
- MEDIUM — copytree failed on sockets/FIFOs and leaked tmp. FIXED: non-regular files skipped, a failed copy removes its folder, cmd_prove reports it (exit 2); FIFO tested.

## lens: operator
- MEDIUM — no total budget; killed runs leave copies. FIXED: DEADLINE 900 s (the rest stay leads) and _sweep clears fm-prove-* copies over a day old. Skipped: a copy-size cap and SIGTERM cleanup (the sweep covers leftovers).
- LOW — leads.jsonl had no reader. FIXED: dropped (YAGNI); leads are in the output.

## lens: intent / maintainer
- MEDIUM — "red 3/3" and model-written proofs aren't built. Captured as T-2199; bug/vuln/slow/flaky are leads with that reason.
- LOW — docs/dep/secret "proven" re-runs the same check. FIXED: evidence says so (the tree holds it, not its surroundings).
- MEDIUM — env and own_tree accept paths untested. FIXED (env test with a seeded token; HEAD-is-yours accept and forge test). rs/c branches untested (c unsupported, rs needs cargo); node/ruby renders skip when the toolchain is missing.

Noticed: fmfind._files on a copy without .git falls back to a walk, so a cold re-find may list files differently: the difference can only turn a proof into a lead.
