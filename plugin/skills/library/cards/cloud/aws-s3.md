---
name: aws-s3
title: AWS S3
area: cloud
tags: [aws, s3, storage, buckets, presigned, encryption]
detect: [dep:@aws-sdk/client-s3, dep:@aws-sdk/s3-request-presigner, dep:@aws-sdk/lib-storage, dep:boto3, dep:aws-sdk-s3, dep:aws-sdk-go-v2/service/s3]
related: [aws-iam, aws-lambda, aws-cloudformation, localstack]
---
S3 buckets and objects: private by default, encrypted, least-privilege access, presigned URLs, lifecycle rules.

## Verify
- `aws s3api get-public-access-block --bucket B`: all four block settings are true.
- `aws s3api get-bucket-encryption --bucket B`: default encryption is on.
- `aws s3api head-object --bucket B --key K`: the object exists, with its content type, size and encryption.
- `aws s3 ls s3://B/prefix/ --recursive --summarize | tail -2`: object counts under a prefix.

## Test first
Test against `moto` or LocalStack, not a real bucket.
```python
import boto3
from moto import mock_aws
from app.store import save_report

@mock_aws
def test_save_report_sets_encryption_and_key():
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket="b")
    save_report(s3, "b", "u1", b"x")
    head = s3.head_object(Bucket="b", Key="reports/u1.csv")
    assert head["ServerSideEncryption"]
```

## Do
- Enable Block Public Access at account and bucket level. Serve public content through CloudFront with OAC.
- Use default SSE (SSE-S3 or SSE-KMS); require TLS with an `aws:SecureTransport` deny.
- Hand clients presigned URLs (short expiry, fixed key and content type) instead of proxying uploads.
- Use multipart upload for large objects (`lib-storage` `Upload` in JS, `upload_file` in boto3).
- Add lifecycle rules: abort incomplete multipart uploads, expire temp prefixes, transition cold data.
- Enable versioning on data you cannot regenerate.
- Design key prefixes for listing; list with pagination (`ListObjectsV2` returns at most 1000 keys).
- Set `Content-Type` and `Cache-Control` on put.

## Avoid
- `list_objects_v2` without a paginator: silently truncates at 1000 keys. Use `get_paginator`.
- Public-read ACLs or `Principal: "*"` bucket policies: use presigned URLs or CloudFront.
- Assuming read-after-write needs sleeps: S3 is strongly consistent; fix the actual bug.
- Putting user input straight into the key: normalise it and strip `..` and leading slashes.
- Fetching whole large objects into memory: stream the body or use ranged GETs.
- Bucket-triggered Lambda writing back into the same prefix: infinite loop.
- Region mismatch: pass `region_name`; creating buckets outside us-east-1 needs `CreateBucketConfiguration`.

## Review
- [ ] Public access blocked and encryption on.
- [ ] Presigned URLs have short expiry and constrained key.
- [ ] Listings paginate.
- [ ] Lifecycle rules exist for temp and multipart data.
- [ ] Bucket policy grants specific principals only.
