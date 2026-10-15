---
name: aws-secrets-manager
title: AWS Secrets Manager
area: cloud
tags: [aws, secrets-manager, secrets, rotation, kms, iam]
detect: [dep:@aws-sdk/client-secrets-manager, dep:aws-secretsmanager-caching, dep:@aws-lambda-powertools/parameters]
related: [aws-kms, aws-iam, aws-lambda, aws-ecs, localstack]
---
Secrets Manager for credentials and keys: read at runtime with a cache, rotate on a schedule, scope access by ARN, and never log the value.

## Verify
- `aws secretsmanager describe-secret --secret-id NAME --query '[RotationEnabled,RotationRules,KmsKeyId,LastRotatedDate]'`: rotation and the encryption key.
- `aws secretsmanager get-resource-policy --secret-id NAME`: who can read it across accounts.
- `aws secretsmanager list-secrets --filters Key=tag-key,Values=env`: inventory by tag.
- `aws iam simulate-principal-policy --policy-source-arn ROLE_ARN --action-names secretsmanager:GetSecretValue --resource-arns SECRET_ARN`: the role can read only what it should.

## Test first
Test the loader against LocalStack, including the missing and rotated case.
```python
def test_loader_returns_current_value_and_fails_closed(sm_client):
    sm_client.create_secret(Name="db", SecretString='{"password":"p1"}')
    assert load_secret("db")["password"] == "p1"
    with pytest.raises(SecretUnavailable):
        load_secret("missing")
```

## Do
- Store secrets as JSON with named keys. Fetch with `GetSecretValue` and cache in memory with a short TTL, using the caching client or Powertools parameters, so rotation takes effect without a redeploy.
- Enable automatic rotation for database credentials. Use the managed rotation templates for RDS and keep the rotation Lambda inside the VPC.
- Grant `secretsmanager:GetSecretValue` on the single secret ARN. Add `kms:Decrypt` on the key when a customer managed key is used.
- Use a customer managed KMS key for secrets shared across accounts, and a resource policy for the other account.
- Tag secrets with owner and environment. Use hierarchical names (`prod/app/db`).
- Handle `AWSCURRENT` and `AWSPREVIOUS` during rotation: retry once on auth failure by refetching.
- Use `ForceDeleteWithoutRecovery` only in tests. Set a recovery window on real deletes.
- Add a VPC endpoint for Secrets Manager when workloads run in private subnets.

## Avoid
- Secrets in environment variables set from plaintext IaC parameters: they land in state and console. Reference the secret at runtime.
- Calling `GetSecretValue` on every request: cost and throttling. Cache with a TTL.
- `secretsmanager:*` on `*`: scope actions and the ARN. The ARN carries a random suffix, so use `NAME-??????` patterns or the exact ARN.
- Logging the response or exception that embeds the value: log the secret name only.
- Rotation without testing the consumer: apps with a fixed connection pool keep the old password. Reconnect on auth errors.
- Putting non-secret config here: use Parameter Store, which costs nothing for standard parameters.
- Defaulting to the AWS managed key when sharing across accounts: it cannot be shared. Use a customer managed key.

## Review
- [ ] No secret value appears in code, IaC, logs or state files.
- [ ] Reads are cached and handle rotation.
- [ ] IAM allows one secret ARN and the key, not wildcards.
- [ ] Rotation is enabled and tested where credentials are database or API logins.
- [ ] Delete uses a recovery window.
