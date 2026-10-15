---
name: gcp-cloud-storage
title: GCP Cloud Storage
area: cloud
tags: [gcp, gcs, storage, buckets, signed-urls, lifecycle, iam]
detect: [dep:@google-cloud/storage, dep:google-cloud-storage]
related: [gcp-iam, aws-s3, azure-blob-storage, gcp-cloud-functions]
---
Cloud Storage buckets: uniform bucket-level access, public access prevention, signed URLs for sharing, lifecycle rules and versioning.

## Verify
- `gcloud storage buckets describe gs://B --format='value(uniform_bucket_level_access,public_access_prevention,versioning_enabled)'`: access mode, public access prevention and versioning.
- `gcloud storage buckets get-iam-policy gs://B`: no `allUsers` or `allAuthenticatedUsers`.
- `gcloud storage ls -L gs://B/key`: object metadata, storage class and generation.
- `gcloud storage buckets describe gs://B --format='value(lifecycle_config)'`: lifecycle rules in place.

## Test first
Use a fake server or a dedicated test bucket and assert that signed URLs are short-lived and scoped.
```python
def test_upload_url_is_put_only_and_expires(storage, bucket):
    url = make_upload_url(bucket, "u/1/a.png", content_type="image/png")
    q = parse_qs(urlparse(url).query)
    assert int(q["X-Goog-Expires"][0]) <= 900
    assert "method=PUT" in url or q.get("X-Goog-SignedHeaders")
```

## Do
- Create buckets with uniform bucket-level access, public access prevention enforced, and a location chosen for latency and residency.
- Grant IAM roles (`roles/storage.objectViewer`, `objectCreator`) to specific service accounts at bucket level. Avoid project-wide storage admin.
- Share objects through V4 signed URLs with short expiry, a fixed method and content type. Use the signer's workload identity (`signBlob`) rather than a key file.
- Upload large files with resumable uploads and verify integrity with the CRC32C or MD5 returned.
- Enable object versioning and soft delete for data you cannot lose, with a lifecycle rule to expire old versions.
- Add lifecycle rules to move cold data to a colder storage class or delete it.
- Set CORS on buckets that browsers use directly, naming exact origins and methods.
- Use preconditions (`ifGenerationMatch=0`) so writes do not overwrite unexpectedly.
- Turn on audit logs for data access on sensitive buckets.

## Avoid
- Granting `allUsers` objectViewer for convenience: makes the bucket public. Serve through signed URLs or a load balancer with a backend bucket and a CDN.
- Fine-grained object ACLs on new buckets: harder to audit. Use uniform access.
- Long-lived service account keys to sign URLs: leakable. Use the credentials the runtime provides.
- Signed URLs that last days: they are bearer tokens. Keep them to minutes.
- Treating buckets as a filesystem: renames copy and delete, and listing is by prefix. Design key layouts accordingly.
- Hot sequential key names at very high request rates: spread the prefix.
- Skipping lifecycle: old versions and temp uploads accumulate cost.

## Review
- [ ] Uniform access and public access prevention on.
- [ ] IAM bindings name specific principals and roles.
- [ ] Signed URLs short, scoped and keyless.
- [ ] Versioning or soft delete and lifecycle rules set.
- [ ] CORS, if any, lists exact origins.
