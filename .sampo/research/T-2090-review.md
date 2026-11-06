**Verdict** — changes needed (two MEDIUM, both fixable in a few lines). I couldn't run the tests, since I only had read tools, so everything below is from reading the code.

## lens: intent
- MEDIUM — plugin/lib/fmgenesis.py:105-114 — `kick` drops the trailing edge. The stamp is written on every spawn, even an "up to date" one. After a Stop kick at t=0, a `put` at t=1 min is throttled, and so is the Stop at t=3 min. If the session ends, the change isn't published until some later put or turn end, possibly days later. This contradicts "publish on every tower change" and the message "reaches the site within minutes" (line 241). — When a call is throttled, schedule one deferred publish for the window's end. For example, spawn `fm genesis publish` after a sleep, guarded by a "pending" stamp. Alternatively, have `publish` re-export before exiting and loop once the window has passed. Add a test that a put inside the window still gets published. — confidence high

  Reproducer: `live on`, run `fm genesis put gap-map.md` (this kicks), then `put gen-1/seed.md` 10 s later. The second put never gets a publish.

## lens: adversary
- MEDIUM — plugin/lib/fmgenesis.py:173-174 — `worktree add … FETCH_HEAD` doesn't pin the fetched commit first. `fm ship` runs `rev-parse FETCH_HEAD` right after its fetch (fmrelease.py:346). Any other fetch in the repo, such as an IDE auto-fetch or `git fetch origin`, rewrites `FETCH_HEAD` between the two git calls. The first line of a plain `git fetch origin` is the branch HEAD tracks. The scratch commit is then built on that branch's tip, and line 187 pushes it to main as a fast-forward. That sends the whole branch to main with no ship test and no grant. The window is narrow, but the push has no ancestry or path check. — Fetch into a private ref (`+refs/heads/main:refs/foreman/genesis-main`) and add the worktree from that ref. Before pushing, assert that `git diff --name-only <base> <sha>` lists only `site/genesis/…` paths. — PLAUSIBLE
- LOW — fmgenesis.py:192-194 — The failure text is stored in meta and shown in status. It comes from git stderr and passes through `c.plain` and `c.fit` but not `c.redact`. A remote URL with embedded credentials could leak into it. — Wrap it in `c.redact(...)`. — low confidence

## lens: edge
- LOW — fmgenesis.py:89-102 — `live on` spends the grant before checking that the remote and main exist. If there is no `origin`, the grant is burned and every publish fails silently, visible only in status. Running `live on` a second time also spends another grant and wipes `last`, `pushed` and `hash`. — Run `git ls-remote --exit-code origin main` before `_spend`. When it is already on, return the current state without spending. — confidence medium

## lens: operator
- LOW — fmgenesis.py:100 — One grant gives an open-ended right to push to main, with no expiry, from a detached process, even after the granting task closes. `fm ship` spends one grant per push. This is acceptable if intended, but it should be a stated decision. The cost is fine: at most one export per 5 minutes across all sessions, and no network when nothing changed. — Document it in MASTER.md, or add a `since` age cap in status. — confidence medium

## lens: maintainer
- LOW — plugin/tests/test_genesis.py:316 — Nothing tests the failure path: a push that fails because main moved, an unreachable remote, the "waiting: fm ship" result, or "already publishing". The `except Exception` and `_record("failed:")` branches are untested, which is the checklist's failure-path item. — Add one test with a bad remote URL that asserts `genesis` status shows "failed:" and that the next publish retries. — confidence high

## Acceptance criteria
- `live on` needs and spends a grant, and `off` clears it: met (test_live_on…, fmgenesis.py:89-102).
- `publish` pushes data only when changed, skips when unchanged, never touches other paths: met in the normal case (test lines 316-341). The FETCH_HEAD race above is not covered.
- Puts and the Stop hook kick a throttled detached publish only while live: met for the throttle and the hook. Not met in spirit for the trailing edge.
- Status shows live state and last push, docs and paths-ignore updated: met (fmgenesis.py:299-311, test.yml, MASTER, CHANGELOG).

## Implicit decisions
- The remote is hardcoded to `origin` and the branch to `main`.
- The window is 300 s, with a shared stamp file.
- Publishes ignore the exam-lines cap except through the export.
- Files deleted from the tower are never deleted from main (`copytree` only adds).
- A failed publish is logged but not retried before the next window.

## Not checked
I did not run the tests. I did not confirm that `export()` writes only to its `out` directory, or that `fm genesis` JSON output has no consumers that `live: False` would break. I did not confirm that main is not branch-protected against the workflow skip.

**Noticed:** none
