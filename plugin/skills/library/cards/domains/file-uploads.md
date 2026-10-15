---
name: file-uploads
title: File Uploads
area: domains
tags: [uploads, multipart, s3, presigned-urls, validation, malware]
detect: [dep:multer, dep:busboy, dep:formidable, dep:@uppy/core, dep:tus-js-client, dep:@aws-sdk/s3-request-presigner, dep:python-multipart, dep:react-dropzone, dep:filetype, dep:python-magic]
related: [image-optimization, forms, webhooks, gdpr, unicode]
---
Safe file intake: size and type limits, content sniffing, server-chosen names, private storage, and direct-to-bucket uploads for large files.

## Verify
- `curl -F "file=@big.bin" localhost:3000/upload -w "%{http_code}\n" -o /dev/null`: oversized files are rejected (expect 413).
- `file --mime-type -b upload.dat`: actual content type from magic bytes, compared with the claimed one.
- `curl -F "file=@evil.php;type=image/png" localhost:3000/upload -i`: a lying `Content-Type` and extension are rejected.
- `aws s3api get-public-access-block --bucket NAME`: bucket blocks public access.

## Test first
Test the hostile cases first.
```python
import io, pytest

@pytest.mark.parametrize("name,data,status", [
    ("a.png", b"\x89PNG\r\n\x1a\n" + b"0" * 10, 201),
    ("a.png", b"<?php echo 1;", 415),          # wrong magic bytes
    ("../../etc/x.png", b"\x89PNG\r\n\x1a\n", 201),  # name is ignored
    ("big.png", b"\x89PNG\r\n\x1a\n" + b"0" * (5 * 2**20), 413),
])
def test_upload(client, name, data, status):
    r = client.post("/upload", files={"file": (name, io.BytesIO(data), "image/png")})
    assert r.status_code == status
    if status == 201:
        assert "etc" not in r.json()["key"]
```

## Do
- Enforce a maximum size at the proxy and in the framework (`limits.fileSize` in multer or busboy, `client_max_body_size` in nginx), and stream instead of buffering whole files.
- Allow-list types by sniffing magic bytes, not the extension or `Content-Type` header.
- Generate the storage key yourself (UUID plus a safe extension); store the original name as metadata only.
- Store outside the web root, or in private object storage; serve through signed URLs or a controller that checks authorization.
- For large files, issue a presigned `PUT` or POST policy with content-length-range and content-type conditions, short expiry; use multipart or resumable (tus) uploads.
- Serve user files from a separate domain with `Content-Disposition: attachment` and `X-Content-Type-Options: nosniff`.
- Scan with ClamAV or a service for shared or downloaded files; quarantine until clean.
- Re-encode images and strip metadata; cap pixel dimensions to prevent decompression bombs.
- Delete orphaned uploads with a lifecycle rule.

## Avoid
- Using the client filename in a path: traversal (`../`) and overwrites. Use your own key.
- Trusting `Content-Type` or extension: attackers set both. Sniff content.
- Serving uploads inline from your main origin: HTML or SVG runs script (stored XSS). Use a sandbox domain or attachment disposition.
- Reading the whole upload into memory: easy denial of service. Stream with a size cap.
- Public-read buckets by default: data leaks. Block public access and sign.
- Allowing archives to extract unchecked: zip slip and zip bombs. Validate entry paths and total size.
- Presigned URLs with long expiry and no conditions: reusable for arbitrary content. Constrain size, type and time.

## Review
- [ ] Size, type (by content) and count limits enforced server-side.
- [ ] Keys are server-generated; no user-supplied path segments.
- [ ] Files are private, authorized on access, and served with safe headers.
- [ ] Large uploads use direct, constrained, expiring URLs.
- [ ] Malware scanning and cleanup of orphans are in place.
