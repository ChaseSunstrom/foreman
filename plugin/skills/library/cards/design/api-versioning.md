---
name: api-versioning
title: API versioning
area: design
tags: [versioning, compatibility, deprecation, api, breaking-changes, contracts]
detect: []
related: [rest-api-design, openapi, grpc, graphql-schema, semver, zero-downtime-migrations]
---
Evolve APIs additively, version only for real breaks, and retire old versions with notice and measured usage.

## Verify
- `git show main:openapi.yaml > /tmp/old.yaml && npx oasdiff breaking /tmp/old.yaml openapi.yaml`: no breaking change in the same version (needs oasdiff installed).
- `buf breaking --against '.git#branch=main'`: protobuf compatibility against main.
- `curl -si localhost:8080/v1/items | grep -iE 'deprecation|sunset|link'`: deprecated routes announce themselves.
- `pytest -q tests/compat`: recorded v1 requests and responses still pass against the current code.

## Test first
Keep golden requests from each supported version and run them in CI.
```python
@pytest.mark.parametrize("case", load_cases("tests/compat/v1/*.json"))
def test_v1_contract_still_holds(client, case):
    r = client.request(case["method"], case["path"], json=case.get("body"))
    assert r.status_code == case["status"]
    for key in case["required_fields"]:
        assert key in r.json()
```

## Do
- Define breaking: removing or renaming a field or route, changing a type, tightening validation, changing defaults, adding a required input, changing error codes clients branch on.
- Treat additions as compatible: new optional fields, new endpoints, new enum values (and document that clients must tolerate unknown values).
- Choose one scheme and keep it: a path prefix (`/v1/`), a header, or a date-pinned version. Path is the simplest for most teams.
- Announce deprecation with `Deprecation` and `Sunset` headers, release notes and a migration guide.
- Measure per-version usage (by key or client) and contact remaining callers before removal.
- Share business logic across versions and translate only at the edge (request and response adapters).
- Give each tolerated change a default: a new required input gets a default that preserves old behavior.
- Run old and new side by side during migrations, and remove old only after usage reaches zero.

## Avoid
- Versioning by copying the whole codebase: bug fixes diverge. Keep one core with thin version adapters.
- Bumping the version for every addition: clients churn for nothing. Add fields compatibly.
- Silently changing semantics under the same version (units, defaults, ordering): clients break without a signal. Add a new field or version.
- Removing a field "nobody uses" without usage data: check logs first.
- Clients that crash on unknown enum values or fields: say in docs that they must ignore them, and test your own SDK.
- Many long-lived versions: set a support policy, such as two versions at a time.
- Breaking error codes or error body shape without notice: clients parse them.

## Review
- [ ] A breaking-change check runs in CI and passes, or a new version is created.
- [ ] Deprecations carry headers, dates and a migration path.
- [ ] Version adapters sit at the edge, with one shared core.
- [ ] Golden tests exist for each supported version.
- [ ] Removal is gated on observed zero usage.
