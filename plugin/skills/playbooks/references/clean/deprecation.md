<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Deprecation: announce, shim, remove

Use when a public function, CLI flag, config key, endpoint, file format or setting is going away or changing
shape, and someone outside this change may depend on it. Internal code with every caller in this repo needs no
deprecation: change the callers in the same commit.

Built on library cards: `fm lib show semver` (when removal is allowed), `fm lib show api-versioning` (endpoints
and formats), `fm lib show changelogs` (writing the notice), `fm lib show feature-flags` (staged switch-offs).

## The procedure

1. **Find the users.** Grep this repo, and where you can, dependents, logs or telemetry for calls to the old
   surface; for a rename, `fm codemod rename OLD NEW` shows every use as a diff and writes nothing until `--apply`
   (run it once the replacement ships, step 2). Pass: the brief states the count found and where you looked.
2. **Ship the replacement first.** The new path works and is documented before the old one warns. Pass: a test
   calls the replacement directly.
3. **Shim the old path onto the new one.** The old entry point becomes a thin wrapper that converts its
   arguments and calls the replacement, so there is one implementation, not two. Pass: the old path's own tests
   still pass unchanged.
4. **Warn where the caller will see it,** naming the replacement and the removal version or date. Never warn
   on a path the caller can't change.
   - Python library: `DeprecationWarning` with `stacklevel=2`, so it points at the caller's line. By default
     Python shows it only when that line is in `__main__`; elsewhere it is hidden unless tests (pytest) or
     `-W` turn it on, and once shown it repeats once per calling location. If end users of an application must
     see it, use `FutureWarning`, which is shown by default.
   - CLI flag or config key: one stderr line per run.
   - HTTP: headers on every response from the old endpoint (example below), not once.
5. **Announce** in the changelog under a Deprecated heading and in the docs for the old surface, with a
   before/after example. Pass: the changelog line names old, new and removal version.
6. **Wait the stated window.** Removal goes in a major version (semver) or after the announced date, never in a
   patch. Capture the removal as a task now, with its date, so it isn't forgotten.
7. **Remove** the shim, its tests, its docs and the warning in one change; the changelog moves the item to
   Removed. Pass: grep for the old name finds only the changelog.

## A warning that points at the caller

Runs as is (Python, stdlib only). `stacklevel=2` makes the warning name the caller's file and line, not the shim.

```python
import warnings

def total(items):
    return sum(items)

def old_total(items):
    warnings.warn("old_total() is deprecated; use total() (removal in 3.0)", DeprecationWarning, stacklevel=2)
    return total(items)

with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    assert old_total([1, 2]) == 3
assert w[0].category is DeprecationWarning and "use total()" in str(w[0].message)
```

Run the suite with `python -W error::DeprecationWarning` to prove nothing in this repo still calls the old path.

## Headers for a deprecated endpoint

`Deprecation` (RFC 9745) takes a structured date, `@` and Unix seconds, for when deprecation began; `Sunset`
(RFC 8594) takes an HTTP-date, for when the endpoint stops working; `Link` names the notice and the replacement.

```http
Deprecation: @1798761600
Sunset: Thu, 01 Jul 2027 00:00:00 GMT
Link: <https://example.com/docs/deprecations/v1-orders>; rel="deprecation"
Link: <https://api.example.com/v2/orders>; rel="successor-version"
```
