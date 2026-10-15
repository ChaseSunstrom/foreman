---
name: aws-cloudformation
title: AWS CloudFormation
area: cloud
tags: [aws, cloudformation, iac, templates, stacks, changesets]
detect: [file:*.template.yaml, file:*.template.yml, file:*.template.json, file:cloudformation/*.yaml, file:cloudformation/*.yml, file:.cfnlintrc]
related: [aws-cdk, aws-sam, aws-iam, aws-s3]
---
CloudFormation templates and stacks: lint, change sets, drift checks, safe updates for stateful resources.

## Verify
- `cfn-lint template.yaml`: schema and best-practice errors before deploy.
- `aws cloudformation validate-template --template-body file://template.yaml`: the template parses (syntax only).
- `aws cloudformation deploy --template-file template.yaml --stack-name S --no-execute-changeset`: creates a change set to review, executes nothing.
- `aws cloudformation detect-stack-drift --stack-name S`: out-of-band edits are found.

## Test first
Lint and assert on the parsed template.
```python
import yaml

def test_buckets_retain_and_encrypt():
    t = yaml.load(open("template.yaml"), Loader=yaml.BaseLoader)
    for name, r in t["Resources"].items():
        if r["Type"] == "AWS::S3::Bucket":
            assert r.get("DeletionPolicy") == "Retain", name
            assert "BucketEncryption" in r["Properties"], name
```
Use `BaseLoader` because the YAML contains `!Ref` and `!Sub` tags.

## Do
- Use `Parameters` with types and `AllowedValues`; use SSM parameter types for AMI and config lookups.
- Use `!Sub` over `!Join`; reference attributes with `!GetAtt`.
- Set `DeletionPolicy` and `UpdateReplacePolicy` (`Retain` or `Snapshot`) on databases, buckets and key stores.
- Always review a change set; look for `Replacement: True`.
- Use `Outputs` with `Export` only for stable cross-stack values; or pass parameters.
- Split stacks by lifecycle (network, data, app); use nested stacks or stack sets sparingly.
- Pass `--capabilities CAPABILITY_IAM` (or `CAPABILITY_NAMED_IAM`) deliberately.
- Add a stack policy or termination protection to production stacks.

## Avoid
- Hard-coded names (`BucketName`, `TableName`): updates that need replacement fail with a name conflict.
- Editing a resource in the console: the next update fails or reverts it. Fix the template, check drift.
- Deleting an export another stack imports: the update fails.
- Secrets as plain `Parameters` or `Default`: use dynamic references (`{{resolve:secretsmanager:...}}`) or `NoEcho` at minimum.
- `!Ref` on a resource where you want the ARN: `Ref` returns different things per type, so check the docs.
- Dependency cycles from mutual security-group rules: use separate ingress resources.
- Retrying a stack stuck in `UPDATE_ROLLBACK_FAILED` by redeploying: continue the rollback first.

## Review
- [ ] cfn-lint clean and change set reviewed.
- [ ] Stateful resources have retain or snapshot policies.
- [ ] No secrets in parameters or outputs.
- [ ] No hard-coded physical names on replaceable resources.
- [ ] IAM capabilities and wildcards justified.
