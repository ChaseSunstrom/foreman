---
name: upload-security
title: File upload security
area: security
tags: [security, uploads, files, mime, storage, malware]
detect: [dep:multer, dep:python-multipart, dep:busboy, dep:formidable, dep:python-magic, dep:file-type]
related: [path-traversal, input-validation, xss, rate-limiting, security-headers]
---
File uploads: bound size and count, verify content type by bytes, rename, store outside the web root, and serve as a download.

## Verify
- `pytest -q tests/security/test_uploads.py`: oversize, wrong-type, polyglot and traversal-name uploads are refused.
- `curl -s -o /dev/null -w "%{http_code}" -F "file=@big.bin" localhost:8000/upload`: a file over the cap returns 413.
- `curl -sI localhost:8000/files/ID | grep -iE "content-disposition|x-content-type-options"`: served files are attachments with `nosniff`.

## Test first
```python
import io, pytest
def upload(client, name, data, ctype="image/png"):
    return client.post("/avatar", files={"file": (name, io.BytesIO(data), ctype)})

def test_html_renamed_to_png_is_rejected(client):
    assert upload(client, "a.png", b"<script>alert(1)</script>").status_code == 415

def test_traversal_filename_is_not_used(client, upload_dir):
    r = upload(client, "../../evil.png", b"\x89PNG\r\n\x1a\n" + b"0" * 32)
    assert r.status_code in (201, 400)
    assert not (upload_dir.parent.parent / "evil.png").exists()
```

## Do
- Enforce limits at the proxy and in the app: maximum bytes, file count, and request time. Stream to disk and stop at the cap.
- Allowlist extensions and detect the real type from magic bytes (`python-magic`, `file-type`); require both to agree.
- Generate the stored name yourself (random id plus a fixed extension) and keep the original name only as metadata.
- Store outside the web root or in object storage with private ACLs, and serve through a handler that checks authorization.
- Send `Content-Disposition: attachment`, the stored `Content-Type`, and `X-Content-Type-Options: nosniff`. Serve user content from a separate domain.
- For images, re-encode with a library to drop metadata and embedded payloads, and cap pixel dimensions.
- Scan with an antivirus engine (ClamAV) when files are shared with other users.

## Avoid
- Trusting the client `Content-Type` header or file extension: both are attacker-set. Sniff the bytes.
- Using the submitted filename in the path: traversal and overwrite. Use a generated name.
- Serving uploads inline from your main origin: stored XSS via HTML or SVG. Use `attachment`, a sandbox domain, and `nosniff`.
- Allowing SVG, HTML or PDF as "images": they carry script. Block them or sanitize and serve downloadable only.
- Accepting executables or scripts in a web-served directory (`.php`, `.jsp`): disable execution there, and store elsewhere.
- Decompressing archives and images without limits: zip bombs and decompression bombs. Cap expanded size and pixel counts.
- Reading the entire upload into memory: stream it.

## Review
- [ ] Size, count and rate limits are enforced.
- [ ] Type is verified by content, with an extension allowlist.
- [ ] Stored names are generated and the path is fixed.
- [ ] Files are served as attachments with `nosniff`, ideally from another origin.
- [ ] Access to stored files is authorized.
