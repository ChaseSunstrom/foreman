---
name: minio
title: MinIO
area: data
tags: [minio, s3, object-storage, presigned, buckets, mc]
detect: [dep:minio, file:minio.env]
related: [parquet-arrow, iceberg, delta-lake]
---
MinIO as S3-compatible storage: mc, bucket policies, presigned URLs, versioning and S3 client configuration.

## Verify
- `mc alias list`: the alias and endpoint you intend (avoid pointing tests at production).
- `mc ls local/bucket`: the bucket exists and is reachable with the credentials.
- `mc admin info local`: server status, drives online and usage.
- `mc anonymous get local/bucket`: the bucket is not anonymously readable unless intended.

## Test first
Run tests against a disposable MinIO (container) with a unique bucket per test.
```python
def test_presigned_put_roundtrip(s3, bucket):
    url = s3.presigned_put_object(bucket, "a.txt", expires=timedelta(minutes=5))
    assert requests.put(url, data=b"hi").status_code == 200
    assert s3.get_object(bucket, "a.txt").read() == b"hi"
```

## Do
- Point S3 SDKs at the endpoint with path-style addressing (`force_path_style` in AWS SDKs, or the minio client defaults).
- Create per-application service accounts (`mc admin user svcacct add`) or users with least-privilege policies on a bucket prefix.
- Serve user uploads and downloads through presigned URLs with short expiry; validate content type and size server-side.
- Enable versioning (`mc version enable local/bucket`) for data you cannot lose, and add lifecycle rules (`mc ilm rule add`) for expiry.
- Use multipart upload for large files; clients do this automatically past a threshold.
- Run distributed mode with erasure coding for production, with drives of equal size.
- Use TLS and set `MINIO_ROOT_USER` and `MINIO_ROOT_PASSWORD` from secrets, not defaults.
- Keep object keys uniform in prefix design and avoid millions of tiny objects when files could be batched.

## Avoid
- The default `minioadmin` credentials: well known. Set strong root credentials and use service accounts.
- Using root credentials in applications: no auditing or scoping. Create scoped accounts.
- Public buckets for convenience: data exposure. Use presigned URLs.
- Virtual-hosted-style addressing without DNS wildcards: requests fail. Use path style or configure `MINIO_DOMAIN`.
- Expecting S3 features to be identical: some APIs differ. Test the exact operations you use.
- Single-drive single-node as a durable store: no redundancy. Use erasure-coded distributed mode.
- Long-lived presigned URLs (days): leaked links stay valid. Use minutes.

## Review
- [ ] Apps use scoped service accounts, not root.
- [ ] No anonymous access except by explicit decision.
- [ ] Presigned URL expiry is short; uploads validated.
- [ ] Versioning and lifecycle configured where needed.
- [ ] Production uses TLS and erasure coding.
