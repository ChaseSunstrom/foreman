---
name: feature-flags
title: Feature flags
area: design
tags: [feature-flags, rollout, toggles, experiments, kill-switch, config]
detect: [dep:launchdarkly-server-sdk, dep:@openfeature/server-sdk, dep:openfeature-sdk, dep:unleash-client, dep:flagsmith, dep:growthbook, dep:flipper, dep:posthog-node]
related: [configuration, zero-downtime-migrations, api-versioning, caching]
---
Runtime switches that separate deploy from release: typed, owned, tested in both states and removed after rollout.

## Verify
- `grep -rn "flags\.\(is_enabled\|enabled\)(" src | wc -l`: counts call sites (adjust to your flag API) so removal is tracked.
- `pytest -q -k flag`: tests cover each flag in on and off states.
- `grep -rnE "(TODO|REMOVE).*flag" src`: flags scheduled for deletion are findable.

## Test first
Test both branches, and the default when the provider is down.
```python
@pytest.mark.parametrize("on", [True, False])
def test_checkout_totals_with_new_tax_flag(flags, on):
    flags.set("new_tax_engine", on)
    assert checkout_total(cart) == (1075 if on else 1070)

def test_flag_provider_down_uses_safe_default(flags):
    flags.fail()
    assert flags.enabled("new_tax_engine") is False
```

## Do
- Define flags in one registry with a name, owner, type, default, creation date and planned removal date.
- Pick a safe default that holds when the flag service is unreachable, and evaluate with a short timeout and a local cached copy.
- Keep the evaluation at the edge of a code path, and pass the result down as a value. Avoid scattering lookups.
- Use percentage rollouts hashed on a stable ID (user or account), so a user keeps their variant.
- Keep kill switches (operational) separate from release flags and experiments, and label each kind.
- Test with the flag on and off, and test the transition (data written under on, read under off).
- Delete the flag and the dead branch once rollout reaches 100 percent and has been stable.
- Log the evaluated variant on requests, so incidents can be tied to a flag state.

## Avoid
- Flags that never get removed: each doubles the test matrix and rots. Set an expiry and a ticket.
- Nested or combined flags whose interaction is untested: limit combinations and test the ones in use.
- A flag lookup in a hot loop with a network call: evaluate once per request, with a local cache.
- Random bucketing on each request: users flip between variants. Hash a stable ID.
- A schema or data change guarded only by a flag: turning it off leaves unreadable data. Make writes backward compatible first.
- Defaulting to "on" when the provider fails for a risky feature: it fails open. Default to the safe state.
- Secrets or targeting PII in flag payloads that clients receive: client-side SDKs expose them.

## Review
- [ ] Every flag has an owner, default and removal date.
- [ ] Tests cover on, off and provider failure.
- [ ] Rollout hashes a stable ID.
- [ ] Data compatibility holds when the flag flips either way.
- [ ] Finished flags are deleted, with their dead branches.
