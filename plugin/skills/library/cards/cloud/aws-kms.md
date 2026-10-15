---
name: aws-kms
title: AWS KMS
area: cloud
tags: [aws, kms, encryption, keys, envelope-encryption, key-policy]
detect: [dep:@aws-sdk/client-kms, dep:@aws-crypto/client-node, dep:aws-encryption-sdk, dep:aws-encryption-sdk-client-kms]
related: [aws-iam, aws-secrets-manager, aws-s3, aws-rds]
---
KMS customer managed keys: envelope encryption for data over 4 KB, key policies plus IAM, encryption context, rotation on, and deletion treated as dangerous.

## Verify
- `aws kms describe-key --key-id KEY --query 'KeyMetadata.[KeyState,KeySpec,KeyUsage,Origin]'`: the key is Enabled with the expected spec and usage.
- `aws kms get-key-rotation-status --key-id KEY`: automatic rotation is on (symmetric keys).
- `aws kms get-key-policy --key-id KEY --policy-name default`: the policy names exact principals.
- `aws kms list-grants --key-id KEY`: no stale grants.
- `aws iam simulate-principal-policy --policy-source-arn ROLE_ARN --action-names kms:Decrypt --resource-arns KEY_ARN`: the role can decrypt and nothing else can.

## Test first
Round-trip with an encryption context, and assert a wrong context fails.
```python
def test_decrypt_fails_with_wrong_context(kms, key_id):
    ct = kms.encrypt(KeyId=key_id, Plaintext=b"x", EncryptionContext={"tenant": "a"})["CiphertextBlob"]
    with pytest.raises(kms.exceptions.InvalidCiphertextException):
        kms.decrypt(CiphertextBlob=ct, EncryptionContext={"tenant": "b"})
```

## Do
- Use `GenerateDataKey` for envelope encryption: encrypt locally with the data key, store the encrypted data key beside the ciphertext, and discard the plaintext key. Direct `Encrypt` handles at most 4 KB.
- Use the AWS Encryption SDK when you want envelope handling and key commitment built in.
- Always pass an `EncryptionContext` (tenant, table, purpose). It is logged in CloudTrail and bound to the ciphertext.
- Write key policies that give admin and use to separate roles. Keep the root-account statement so IAM can delegate.
- Grant `kms:Decrypt` or `kms:GenerateDataKey` only to the roles that need them, optionally with `kms:ViaService` and `kms:EncryptionContext` conditions.
- Turn on automatic rotation for symmetric keys. Use aliases (`alias/app-prod`) in code, never raw key ids.
- Use multi-Region keys only for real cross-Region needs.
- Use separate keys per environment and data class, and alarm on `ScheduleKeyDeletion` events.

## Avoid
- `kms:*` on `*` or `Principal: "*"` in a key policy: anyone with IAM can then use or administer the key. Name principals and actions.
- Encrypting large payloads directly: it fails past 4 KB. Use data keys.
- Omitting encryption context: ciphertext can be replayed across tenants. Bind it.
- Caching plaintext data keys forever or logging them: cache briefly with a limited number of uses, never log.
- Deleting a key to save cost: all data becomes unrecoverable after the waiting period. Disable first and watch for errors.
- Assuming rotation re-encrypts old data: it does not. Old versions stay available to decrypt.
- Hardcoding a key ARN per Region: parametrize through config or alias.

## Review
- [ ] Data over 4 KB uses envelope encryption.
- [ ] Every call carries a meaningful encryption context.
- [ ] Key policy separates admins from users and has no wildcards.
- [ ] Rotation is on and aliases are used.
- [ ] Deletion protection process and alarms exist.
