## Verdict: changes needed

## Findings

**MEDIUM** — EDGE lens — `~/.claude/foreman/plugin/lib/fmhooks.py:360-364` vs `~/.claude/foreman/plugin/lib/fmcore.py:20`
`_committed(name)` gates the fallback with:
```
root = c.git_root(lib)
if not root or os.path.normpath(os.path.join(root, "plugin")) != os.path.normpath(c.PLUGIN_ROOT):
    return None
```
`git_root()` resolves symlinks (`d = os.path.realpath(path)`) while walking up for `.git`, but `c.PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))` uses `abspath`, not `realpath`. If the plugin is reached through a symlink (a normal pattern for a plugin under active development, symlinked into `~/.claude/plugins/…`), `root` is the resolved real directory while `c.PLUGIN_ROOT` keeps the symlinked path, so the two normalized paths never match and `_committed()` always returns `None` for Foreman's own legitimate repo. This is exactly the fallback round 7 added to `_guard_ctx` for a broken `fmcore` (T-0037's fix): under a symlinked install, a runtime bug in `fmcore.find_project`/`active_brief` again silently loses the active task's grants with no recovery — reintroducing the self-lockout round 7 was written to close, for the fmcore-runtime path specifically. It fails closed (over-blocks), not open, so it is not exploitable, but it defeats the round's stated guarantee.
Fix: make `c.PLUGIN_ROOT` (or the comparison in `_committed`) use `realpath` consistently, e.g. `os.path.realpath(os.path.join(root, "plugin")) != os.path.realpath(c.PLUGIN_ROOT)`.
Confidence: high on the code inconsistency; medium on real-world triggerability (depends on install layout).

**LOW** — ADVERSARY lens (type-design nit) — `~/.claude/foreman/plugin/lib/fmcore.py:248-251`
`record()` computes field names via `getattr(cls, "__annotations__", {})`, which follows the MRO rather than reading only the class's own `__dict__`. None of the five `@record` classes currently subclass one another, so this isn't triggered today, but it's a latent trap: a future subclass of a `@record` class that adds no annotations of its own would silently inherit the parent's field list (and constructor semantics) instead of erroring. Not currently exploitable.
Confidence: high (verified by reading the decorator); impact is speculative/future.

**Verified clean (no finding):** `fmguard.py` (`~/.claude/foreman/plugin/lib/fmguard.py:8-11`) is genuinely stdlib-only; both fallback paths (`hook`'s `committed_library()` and `fmhooks._committed()`) strip all `GIT_*` env vars before shelling to git; `_pre_tool_use` returns exit 2 on every exception path (no fail-open found); `record()`'s mutable-default copying (`type(d)(d)`) correctly avoids cross-instance sharing for the `list = []` defaults introduced in `fmcore.py:182-183, 195-202`; missing/extra constructor args raise `TypeError` (no silent field loss); the `check_core_integrity` worktree gap seen in the diff (`isdir` vs a worktree's `.git` file) was already fixed in a later commit (`fmdoctor.py:236`, now `os.path.exists`).

## Not checked
- `fmsync` stat-cache removal (out of the two named lenses' scope).
- Non-Foreman-repo / planted-commit scenarios requiring prior write access to `.git` refs (would already require the `core` grant to plant the source file being committed; no new escalation found, not exhaustively fuzzed).
- Actual timing/perf numbers (p50/p95 claims) — not re-measured.
- `fm doctor`'s description-budget glob against nested `commands/**` layouts.
- Full `test_hooks.py`/`test_doctor.py`/`test_core.py` execution (read only, not run).
