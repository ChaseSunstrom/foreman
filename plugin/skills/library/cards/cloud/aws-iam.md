---
name: aws-iam
title: AWS IAM
area: cloud
tags: [aws, iam, security, policy, least-privilege, roles]
detect: [dep:boto3, dep:@aws-sdk/client-iam, dep:aws-cdk-lib, file:*.tf]
related: [aws-lambda, aws-cdk, aws-cloudformation, aws-s3]
---
AWS IAM: least-privilege roles and policies, scoped resources, conditions, and policy checks before deploy.

## Verify
- `aws iam simulate-principal-policy --policy-source-arn ROLE_ARN --action-names s3:GetObject --resource-arns BUCKET_ARN/key`: the role is allowed or denied exactly as intended.
- `aws accessanalyzer validate-policy --policy-document file://policy.json --policy-type IDENTITY_POLICY`: findings for wildcards, bad actions and syntax.
- `aws sts get-caller-identity`: which principal the code actually runs as.
- `aws iam generate-service-last-accessed-details --arn ROLE_ARN`: which granted services are never used.

## Test first
Fail on the policy document itself, before any deploy.
```python
import json

def test_no_wildcard_action_or_resource():
    doc = json.load(open("infra/policy.json"))
    for st in doc["Statement"]:
        if st["Effect"] != "Allow":
            continue
        acts = st["Action"] if isinstance(st["Action"], list) else [st["Action"]]
        assert "*" not in acts and not any(a.endswith(":*") for a in acts)
        assert st["Resource"] != "*"
```
Add a simulate-principal-policy case for one allowed and one denied action.

## Do
- Grant actions per resource ARN, never `Resource: "*"` unless the action has no resource-level support.
- Use one role per workload. Attach inline or customer-managed policies, not `AdministratorAccess` or `PowerUserAccess`.
- Restrict trust policies: pin the `Principal`, and add `aws:SourceArn` and `aws:SourceAccount` conditions for service principals.
- Use `sts:AssumeRole` with short sessions; for CI use OIDC federation (`sts:AssumeRoleWithWebIdentity`) with a `sub` condition.
- Use conditions: `aws:PrincipalOrgID`, `s3:prefix`, `aws:RequestedRegion`, `aws:MultiFactorAuthPresent`.
- Set permission boundaries or SCPs for delegated role creation.
- Resolve credentials from the default provider chain (env, profile, role).

## Avoid
- `"Action": "*"` or `"service:*"` to make an error go away: read the AccessDenied message, add the one missing action.
- Long-lived access keys in code, `.env` or CI secrets: use roles and OIDC.
- Trust policy `"Principal": {"AWS": "*"}` or an account root without conditions: any principal in that account can assume the role.
- `iam:PassRole` on `*`: scope it to the role ARN with `iam:PassedToService`.
- Reading an explicit Deny as a typo: Deny always beats Allow, and SCPs and boundaries cap everything.
- Testing with admin credentials locally: permissions bugs only appear in prod. Test as the real role.

## Review
- [ ] No `*` in Action or Resource without a written reason.
- [ ] Trust policy names a specific principal and has source conditions.
- [ ] No IAM users or static keys introduced.
- [ ] `iam:PassRole` and `iam:Create*` are scoped.
- [ ] Policy passed Access Analyzer validation.
