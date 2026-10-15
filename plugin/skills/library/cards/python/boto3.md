---
name: boto3
title: boto3
area: python
tags: [python, aws, boto3, s3, cloud, sdk]
detect: [dep:boto3, dep:botocore, dep:moto, dep:aioboto3]
related: [pytest, pytest-mock, asyncio, pydantic-settings]
---
boto3: AWS SDK for Python with sessions, retry config, paginators and moto-based tests, never hard-coded credentials.

## Verify
- `python -c "import boto3; print(boto3.client('sts').get_caller_identity()['Arn'])"`: credentials resolve to the identity you expect.
- `pytest -q`: tests against moto with fake credentials.
- `aws sts get-caller-identity`: the same identity through the CLI.
- `grep -rnE "AKIA[0-9A-Z]{16}" .`: no access keys committed.

## Test first
Use moto (`mock_aws` decorator in moto 5) with dummy credentials set in the environment.
```python
import boto3
import pytest
from moto import mock_aws
from app.store import put_report

@pytest.fixture(autouse=True)
def aws_env(monkeypatch):
    for k in ("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN"):
        monkeypatch.setenv(k, "testing")
    monkeypatch.setenv("AWS_DEFAULT_REGION", "us-east-1")

@mock_aws
def test_put_report_writes_object():
    boto3.client("s3").create_bucket(Bucket="b")
    put_report("b", "r.json", {"a": 1})
    assert boto3.client("s3").get_object(Bucket="b", Key="r.json")["Body"].read()
```

## Do
- Let the default credential chain work (env, shared config, SSO, instance or task role). Use `boto3.Session(profile_name=...)` for explicit profiles.
- Create clients once and reuse them: they are thread safe. Sessions and resources are not.
- Set `botocore.config.Config(retries={"max_attempts": 5, "mode": "adaptive"}, connect_timeout=5, read_timeout=30)`.
- Paginate with `client.get_paginator("list_objects_v2").paginate(Bucket=b)` and not manual loops on `IsTruncated`.
- Handle errors via `botocore.exceptions.ClientError` and `e.response["Error"]["Code"]`.
- Use `upload_file` / `download_file` for big objects (multipart, retries) and `generate_presigned_url` for temporary access.
- Apply least privilege IAM, with encryption (`ServerSideEncryption`) and block public access on buckets.
- Use `aioboto3` or run calls in a thread for asyncio apps.

## Avoid
- Access keys in code, env files in git or Docker images: use roles and short-lived credentials.
- Calling `list_objects_v2` once and assuming complete results: max 1000 keys. Paginate.
- Catching bare `Exception` around AWS calls: hides throttling and permission errors. Catch `ClientError` and branch on the code.
- Creating a new client per call in hot loops: slow, and re-resolves credentials. Reuse.
- Mocking with `MagicMock` on clients: signature drift passes. Use moto or `botocore.stub.Stubber`.
- Running tests with real credentials in the environment: they may hit live AWS. Set dummy keys in an autouse fixture.
- Ignoring region: `NoRegionError` or wrong-region data. Set `region_name` or `AWS_DEFAULT_REGION`.

## Review
- [ ] No credentials or account ids in source, and roles are used at runtime.
- [ ] Clients are reused and configured with timeouts and retries.
- [ ] Listings are paginated and errors are matched by code.
- [ ] Tests run with fake credentials against moto.
