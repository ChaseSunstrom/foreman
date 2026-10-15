---
name: audit-trails
title: Audit trails
area: design
tags: [audit, logging, compliance, append-only, security, history]
detect: []
related: [soft-deletes, data-retention, event-sourcing, outbox-pattern, multi-tenancy]
---
Record who did what to which entity, when and with what outcome, in an append-only store written in the same transaction as the change.

## Verify
- `pytest -q -k audit`: every mutating path emits exactly one entry.
- `psql -c "\dp audit_log"`: the application role has INSERT and SELECT only, no UPDATE or DELETE.
- `git grep -nE "audit\.(record|log)\(" -- src`: calls sit in the service layer, next to the mutations.

## Test first
A change and its audit row commit or roll back together, and the log cannot be rewritten.
```python
def test_audit_row_is_atomic_and_immutable(db, actor):
    with pytest.raises(Boom):
        with db.begin():
            rename_project(db, 1, "new", actor=actor)
            raise Boom
    assert audit_rows(db) == []                       # rolled back together
    rename_project(db, 1, "new", actor=actor)
    row = audit_rows(db)[0]
    assert (row.actor_id, row.action, row.entity) == (actor.id, "project.rename", "project:1")
    assert row.before == {"name": "old"} and row.after == {"name": "new"}
    with pytest.raises(PermissionDenied):
        db.execute("update audit_log set action='x'")
```

## Do
- Capture actor (user, service, impersonator), action name, entity type and id, tenant, timestamp (UTC), request or trace id, source IP, outcome, and before and after values for changed fields.
- Write in the same transaction as the mutation, or via the outbox pattern when it must go elsewhere.
- Make the table append-only: revoke UPDATE and DELETE, and consider hash chaining or write-once storage for tamper evidence.
- Log authentication, authorisation failures, permission changes, exports and admin actions, not only CRUD.
- Redact secrets and personal data; store ids or field names rather than raw sensitive values where possible.
- Partition by time, index by entity and actor, and set retention explicitly.
- Give audit reads their own permission and audit those reads.

## Avoid
- Audit in application logs only: lost on rotation and unqueryable. Use a durable table.
- Writing the audit row after commit: a crash drops it. Same transaction.
- Logging full request bodies: leaks secrets. Log a field-level diff with redaction.
- Using the audit table as the source of truth for state: it becomes an accidental event store. Keep them distinct, or adopt event sourcing deliberately.
- Missing system actors: background jobs show as nobody. Record the service identity.

## Review
- [ ] All mutation paths audited, including bulk and admin.
- [ ] Atomic with the change; table append-only.
- [ ] No secrets in entries.
- [ ] Retention and access to the log defined.
