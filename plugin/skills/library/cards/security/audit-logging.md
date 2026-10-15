---
name: audit-logging
title: Audit logging
area: security
tags: [security, audit, logging, compliance, forensics, tamper-evidence]
detect: []
related: [pii-logging, authorization, iam-least-privilege, zero-trust, key-rotation]
---
Record who did what to which object, when and from where, for security-relevant events, in append-only storage that holds no secrets.

## Verify
- `pytest -q -k audit`: event emission and redaction tests pass.
- `git grep -nE "audit\.(log|record|emit)" -- ':!*test*'`: every sensitive action calls the audit function.
- `git grep -nEi "password|token|secret|authorization" -- '*audit*'`: audit code handles no raw credentials.

## Test first
Sensitive actions emit one structured event, and secrets never appear in it.
```python
def test_role_change_is_audited_without_secrets(client, admin, user, audit_sink):
    client.post(f"/users/{user.id}/role", json={"role": "admin", "password": "hunter2"},
                headers=admin.auth)
    ev = audit_sink.events[-1]
    assert ev["action"] == "user.role.change"
    assert ev["actor_id"] == admin.id and ev["target_id"] == user.id
    assert ev["outcome"] == "success" and "ts" in ev and "request_id" in ev
    assert "hunter2" not in str(ev)
```

## Do
- Log: login success and failure, MFA changes, password and email changes, role and permission changes, key creation and revocation, data export, admin actions, authorization denials.
- Use a fixed schema: UTC timestamp, actor, action, target, outcome, source IP, user agent, request id, tenant.
- Emit from the service layer where the decision is made, so no entry path is missed. Log the denial as well as the success.
- Write to an append-only sink: a separate account or bucket with object lock, or a log service the app can write but not delete.
- Record before-and-after identifiers or field names for changes, not secret values or full PII.
- Chain entries with a hash or sign batches if tamper evidence is required.
- Restrict read access to the audit store, and audit reads of it.
- Define retention and alert on bursts of failures and on privileged actions.

## Avoid
- Free-text log lines: they cannot be queried reliably. Emit structured JSON with stable keys.
- Logging request bodies or tokens "for debugging": redact with an allow-list of fields.
- Audit rows in the same writable table the app admins can edit: separate and append-only.
- Logging only successes: failed and denied attempts are the signal.
- Trusting client-supplied actor, IP or timestamp: take them from the session and the server clock, and parse forwarded IPs only from trusted proxies.
- Dropping events when the sink is down: queue durably and alert.

## Review
- [ ] Each sensitive action has an event with actor, target and outcome.
- [ ] No credentials or raw PII are in events.
- [ ] The store is append-only and access-controlled.
- [ ] Time comes from the server and is in UTC.
- [ ] Alerts exist for key patterns.
