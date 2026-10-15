---
name: gcp-iam
title: GCP IAM
area: cloud
tags: [gcp, iam, service-accounts, roles, security, adc]
detect: [dep:google-auth, dep:google-cloud-iam, dep:@google-cloud/iam, dep:google-cloud-secret-manager, dep:@google-cloud/secret-manager]
related: [gcp-cloud-run, gcp-pubsub, aws-iam]
---
GCP IAM: per-workload service accounts, predefined roles at the narrowest scope, Application Default Credentials, no keys.

## Verify
- `gcloud auth application-default print-access-token >/dev/null`: ADC resolves to a credential.
- `gcloud projects get-iam-policy P --flatten=bindings[].members --filter='bindings.members:serviceAccount:SA' --format='table(bindings.role)'`: exactly the roles this account holds.
- `gcloud iam service-accounts keys list --iam-account SA --managed-by=user`: no user-managed keys exist.
- `gcloud asset search-all-iam-policies --scope=projects/P --query='policy:allUsers'`: nothing grants public access.

## Test first
Fail on the IaC or exported policy before applying.
```python
import json

def test_no_primitive_roles_or_public_members():
    policy = json.load(open("infra/iam-policy.json"))
    for b in policy["bindings"]:
        assert b["role"] not in {"roles/owner", "roles/editor"}
        assert "allUsers" not in b["members"]
        assert "allAuthenticatedUsers" not in b["members"]
```

## Do
- Create one service account per workload; attach it to the resource (Cloud Run, GKE Workload Identity, GCE) and let ADC find it.
- Prefer predefined narrow roles (`roles/storage.objectViewer`) or custom roles over basic ones.
- Bind at the lowest scope: a resource (bucket, topic, secret) over the project.
- For CI use Workload Identity Federation with an attribute condition, not exported keys.
- Use impersonation (`--impersonate-service-account`, `roles/iam.serviceAccountTokenCreator`) for admin tasks.
- Add IAM Conditions for time or resource name limits; use `gcloud recommender` insights to trim unused roles.
- Use `roles/iam.serviceAccountUser` sparingly: it lets a caller act as the account.
- Authenticate libraries with `google.auth.default()` and the client's default constructor.

## Avoid
- Downloaded service account JSON keys in repos or images: use ADC, attached accounts or federation.
- `roles/owner` or `roles/editor` for a service account: grant the specific predefined role.
- The default Compute Engine service account with Editor: create a dedicated account.
- `allUsers` or `allAuthenticatedUsers` bindings (the latter means any Google account).
- Setting `GOOGLE_APPLICATION_CREDENTIALS` in production images: it overrides the attached identity.
- Granting at the project when the failing call touches one resource: scope it.
- Assuming a role change is instant: propagation can take minutes.

## Review
- [ ] One service account per workload with named roles.
- [ ] No basic roles, no public members, no user-managed keys.
- [ ] Bindings sit at resource scope where possible.
- [ ] CI uses federation.
- [ ] `serviceAccountUser` and token-creator grants are justified.
