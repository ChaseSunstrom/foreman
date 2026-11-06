Verdict: changes needed (1 HIGH, 1 MEDIUM, 4 LOW); reviewer ran nothing (read-only).

## lens: adversary
- HIGH — trusted() accepted Foreman's home, and foreman_home() follows FOREMAN_HOME, so `FOREMAN_HOME=<tree> fm prove <tree>` ran an untrusted tree's tests without --yes-run. FIXED: the Foreman-home exception is gone (nothing needed it); test: naming a tree Foreman's home runs none of its code.
- HIGH (second trigger) — FOREMAN_STATE pointed at a self-written trust list. DECIDED, not guarded: a session doing that is set on running the code and could run the tests directly; the yes governs Foreman's own initiative. Docs (module docstring, MASTER) say so. No guard rule added (fm decide).
- LOW — trust is per path, not per content. Kept (the request: per tree); docs and CHANGELOG say so.
- LOW — remember() raised outside cmd_prove's try. FIXED: a failed write is reported and the run goes on; a broken trust list trusts nothing (tested).

## lens: intent
- MEDIUM — unrun untested candidates took --limit slots from provable kinds. FIXED: they sort last when the tree's code can't run (tested at --limit 1 both ways).

## lens: edge
- corrupt trust file and a prefix-sharing sibling path: tested (trusts nothing; a yes on proj leaves proj2 untrusted).

## lens: operator
- No hooks, loops or new cost; one small JSON state file, written only on the user's yes.

## lens: maintainer
- LOW — Foreman-home branch untested: removed instead. own_tree has no callers left.

Noticed: none.
