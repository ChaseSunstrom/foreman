---
name: threat-modeling
title: Threat modeling
area: security
tags: [security, threat-model, stride, design, risk, architecture]
detect: []
related: [owasp-top-10, authorization, secrets-management, input-validation]
---
Threat modeling: list assets, trust boundaries and abuse cases before building, and turn each abuse case into a test.

## Verify
- `test -s docs/threat-model.md`: a threat model file exists and is not empty.
- `grep -c "^- \[ \]\|^| T-" docs/threat-model.md`: the model lists threats with a mitigation or status.
- `pytest -q tests/security -k abuse`: each abuse case has an executable check (rename the selector to your convention).

## Test first
For a practice topic the check that fails first is an abuse-case test. Write the attacker's request and assert it is refused.
```python
# Abuse case A-3: a member invites themselves as owner.
def test_member_cannot_promote_self(client, member, org):
    r = client.patch(f"/orgs/{org.id}/members/{member.id}",
                     json={"role": "owner"}, headers=member.auth)
    assert r.status_code == 403
    assert org.refresh().role_of(member) == "member"
```

## Do
- Draw the data flow: actors, processes, stores, and the trust boundaries between them. One page is enough.
- Walk STRIDE (spoofing, tampering, repudiation, information disclosure, denial of service, elevation of privilege) on every boundary crossing.
- Write each threat as an attacker goal plus the entry point, then rate likelihood and impact.
- Give each accepted threat a mitigation, an owner, and a test or monitor that proves it.
- Record explicit accepted risks with a reason and a review date.
- Revisit the model when a new integration, auth flow, data class or public endpoint is added.
- Start from assets: what would hurt if read, changed or unavailable.

## Avoid
- Modeling only the external attacker: insiders, compromised dependencies, and a stolen low-privilege token are threats too. Add them as actors.
- A one-time document nobody updates: tie the review to the PR template for changes that cross a boundary.
- Mitigations with no verification ("we validate input"): add the test or alert that would fail if it stopped.
- Listing threats without ranking: everything marked high means nothing is. Rate by impact and likelihood.
- Skipping the data store and queue boundaries: internal services trusting each other is the usual lateral-movement path. Authenticate service to service.
- Treating the model as the output: unmitigated, untested threats are just a list. Turn each into a ticket or a test.

## Review
- [ ] Assets, actors and trust boundaries are named.
- [ ] Each boundary crossing was checked against all six STRIDE categories.
- [ ] Every high threat has a mitigation and a test or monitor.
- [ ] Accepted risks carry an owner and a review date.
- [ ] The model changed in the same PR as the design it describes.
