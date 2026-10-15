---
name: localstack
title: LocalStack
area: cloud
tags: [localstack, aws, emulator, testing, docker, awslocal]
detect: [dep:localstack, dep:aws-cdk-local, dep:@localstack/*, dep:awscli-local, dep:testcontainers-localstack, file:docker-compose.localstack.yml]
related: [aws-s3, aws-lambda, aws-sqs-sns, aws-cdk, aws-sam]
---
LocalStack: emulate AWS services locally for integration tests, pointed at one edge endpoint, with fake credentials.

## Verify
- `localstack start -d`: the container starts in the background.
- `curl -s localhost:4566/_localstack/health`: services show as available or running.
- `aws --endpoint-url=http://localhost:4566 s3 ls`: the CLI reaches the emulator (or use `awslocal s3 ls`).
- `localstack logs`: container logs for failed calls and unsupported APIs.

## Test first
Point the SDK at the edge endpoint, then assert on real service behavior.
```python
import boto3

def test_queue_roundtrip():
    sqs = boto3.client("sqs", endpoint_url="http://localhost:4566",
                       region_name="us-east-1",
                       aws_access_key_id="test", aws_secret_access_key="test")
    url = sqs.create_queue(QueueName="q")["QueueUrl"]
    sqs.send_message(QueueUrl=url, MessageBody="x")
    got = sqs.receive_message(QueueUrl=url, WaitTimeSeconds=1)["Messages"][0]
    assert got["Body"] == "x"
```

## Do
- Read the endpoint from one env var (`AWS_ENDPOINT_URL`) so code is identical locally and in AWS.
- Use dummy credentials (`test` and `test`) and a fixed region.
- Create resources in test setup (fixtures, `awslocal`, CDK with `cdklocal`, Terraform with the endpoint overrides) and tear them down.
- Use S3 path-style addressing (`forcePathStyle: true` in JS, `addressing_style: path` in boto3) when virtual-host URLs fail.
- Pin the LocalStack image tag in `docker-compose` or the test config for repeatable runs.
- Mount `/var/run/docker.sock` when testing Lambda so it can start containers.
- Wait for health before tests; start it in CI as a service.
- Keep one real-AWS smoke test for what the emulator cannot prove.

## Avoid
- Treating a green LocalStack run as proof of IAM correctness: enforcement is off by default and differs from AWS.
- Hard-coding `localhost:4566` in application code: use configuration so production never targets it.
- `latest` image tags: behavior changes between runs.
- Sharing one LocalStack across parallel tests without unique resource names.
- Leaving real credentials in the shell: a misconfigured endpoint then hits real AWS. Export dummy ones for the run.
- Assuming every API or edge case is implemented: check the logs for 501 and unsupported-operation errors.

## Review
- [ ] Endpoint comes from config, never hard-coded in app code.
- [ ] Credentials are dummy values in test runs.
- [ ] Image tag is pinned; health awaited.
- [ ] Resources are unique per test and cleaned up.
- [ ] IAM and real-service behavior verified elsewhere.
