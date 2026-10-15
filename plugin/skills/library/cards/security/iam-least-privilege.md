---
name: iam-least-privilege
title: IAM least privilege
area: security
tags: [security, iam, aws, permissions, roles, cloud]
detect: []
related: [kubernetes-security, secrets-management, audit-logging, zero-trust, authorization]
---
Cloud identities get one role per workload, named actions on named resources, short-lived credentials, and conditions that bound blast radius.

## Verify
- `aws accessanalyzer validate-policy --policy-document file://policy.json --policy-type IDENTITY_POLICY`: findings for wildcards, bad actions and risky grants.
- `aws iam simulate-principal-policy --policy-source-arn ROLE_ARN --action-names s3:DeleteBucket`: the role is denied what it should never do.
- `git grep -nE '"(Action|Resource)": *"\*"|Action: *\*|actions *= *\["\*"\]' -- ':!*test*'`: wildcards in policy files and IaC.
- `trivy config .`: IaC scan covering common IAM misconfigurations.

## Test first
Fail the build on wildcard grants in policy files.
```python
import json, glob

def test_no_wildcard_actions_or_resources():
    for f in glob.glob("infra/policies/*.json"):
        for s in json.load(open(f))["Statement"]:
            if s["Effect"] != "Allow":
                continue
            acts = [s["Action"]] if isinstance(s["Action"], str) else s["Action"]
            res = [s["Resource"]] if isinstance(s["Resource"], str) else s["Resource"]
            assert not any(a == "*" or a.endswith(":*") for a in acts), f
            assert "*" not in res, f
```

## Do
- Create one role per workload or function. Never share a role across services.
- List exact actions and exact resource ARNs. Where a trailing wildcard is unavoidable, scope it to a prefix.
- Prefer temporary credentials: instance or task roles, OIDC federation for CI. Use no long-lived access keys.
- Add conditions: source VPC or IP, tags, MFA for human admin, `aws:PrincipalOrgID` for sharing.
- Set permission boundaries or organisation SCPs as a ceiling for delegated admins.
- Separate human, CI and runtime identities. Require MFA for humans.
- Review unused permissions with last-accessed data and trim them on a schedule.
- Define roles in IaC and review changes in pull requests.

## Avoid
- `Action: "*"` or `AdministratorAccess` to unblock a deploy: read the AccessDenied event and add the one action.
- `Resource: "*"` on data stores: name the bucket, table or key ARN.
- Access keys in env files or CI variables: use OIDC federation or instance roles.
- Trust policies with `Principal: "*"` or an account root where one role is meant: name the principal and add conditions.
- Letting a role create roles or attach policies (`iam:*`, `iam:PassRole` on `*`): this is privilege escalation. Restrict PassRole to named roles.
- One admin user shared by a team: use individual identities with audited sessions.

## Review
- [ ] No wildcard actions or resources on Allow statements, except justified prefixes.
- [ ] Each workload has its own role and short-lived credentials.
- [ ] Trust policies name principals with conditions.
- [ ] `iam:PassRole` and role-management actions are tightly scoped.
- [ ] Unused permissions are reviewed periodically.
