---
name: path-traversal
title: Path traversal
area: security
tags: [security, path-traversal, files, filesystem, zip-slip, lfi]
detect: []
related: [upload-security, input-validation, command-injection, unsafe-deserialization]
---
Path traversal: never join user input into a filesystem path unchecked; resolve it and prove it stays inside the base directory.

## Verify
- `pytest -q tests/security/test_paths.py`: `..`, absolute, encoded and symlink inputs are refused.
- `semgrep scan --config p/security-audit --error`: no file open or send with user-controlled paths.
- `grep -rnE "(open|send_file|sendFile|readFile|os\.path\.join|path\.join)\(.*(req|request|params|user|name|filename)" src/`: each hit goes through the safe resolver.

## Test first
```python
import pytest
BAD = ["../../etc/passwd", "/etc/passwd", "..%2f..%2fetc%2fpasswd",
       "....//....//etc/passwd", "a/../../b", "x\x00.png", "C:\\Windows\\win.ini"]

@pytest.mark.parametrize("name", BAD)
def test_download_stays_in_base_dir(client, name):
    r = client.get("/files", params={"name": name})
    assert r.status_code in (400, 403, 404)
    assert b"root:" not in r.content
```

## Do
- Prefer ids: map an opaque id to a stored path in a database and never accept a path from the client.
- Otherwise resolve then compare: Python `p = (BASE / name).resolve(); p.is_relative_to(BASE.resolve())` or `os.path.commonpath`, Node `path.resolve(base, name)` then `startsWith(base + path.sep)`, Go `filepath.Rel` then reject results starting with `..`.
- Decode once, normalize, then check; use the same value to open.
- Reject null bytes, absolute paths and drive letters in names. Accept `[A-Za-z0-9._-]` only where possible.
- For archives, validate each entry's resolved destination before extracting (zip slip), skip symlinks and device entries, cap total size and file count.
- Use `send_from_directory` (Flask), `FileResponse` only on checked paths, and Go `os.OpenRoot` or `http.Dir` with care.
- Run the process with minimal filesystem permissions and keep uploads outside the web root.

## Avoid
- Checking `".." in name` and stopping: encoded, doubled and absolute forms get through. Resolve and compare against the base.
- `startswith(base)` without a separator: `/data/files-evil` matches `/data/files`. Use `is_relative_to` or add the separator.
- `os.path.join(base, user)` when `user` is absolute: Python discards `base`. Reject absolute input first.
- Checking the path before following symlinks: a link inside base points out. Resolve the real path (`realpath`, `resolve()`).
- `tarfile.extractall` or `zipfile.extractall` on untrusted archives with no filter: use `filter="data"` on Python versions that support it, or validate members.
- Check-then-open races (TOCTOU): open with the resolved path or a directory file descriptor and not the original string.

## Review
- [ ] No user string reaches a filesystem call unresolved.
- [ ] The resolved path is proven inside the base directory.
- [ ] Archive extraction validates each member.
- [ ] Symlinks are resolved or rejected.
- [ ] Tests cover `..`, absolute, encoded, null-byte and symlink inputs.
