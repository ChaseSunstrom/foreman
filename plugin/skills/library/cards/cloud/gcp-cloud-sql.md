---
name: gcp-cloud-sql
title: GCP Cloud SQL
area: cloud
tags: [gcp, cloud-sql, postgres, mysql, auth-proxy, backups]
detect: [dep:@google-cloud/cloud-sql-connector, dep:cloud-sql-python-connector]
related: [gcp-iam, gcp-cloud-run, aws-rds, gcp-gke]
---
Cloud SQL instances: private IP, connections through the Auth Proxy or connector with IAM, high availability, backups and point-in-time recovery, pooled clients.

## Verify
- `gcloud sql instances describe I --format='value(settings.availabilityType,settings.backupConfiguration.enabled,settings.backupConfiguration.pointInTimeRecoveryEnabled,settings.ipConfiguration.ipv4Enabled)'`: HA, backups, PITR and whether a public IP is on.
- `gcloud sql instances describe I --format='value(settings.databaseFlags,settings.deletionProtectionEnabled)'`: flags and deletion protection.
- `gcloud sql backups list --instance I`: recent successful backups.
- `cloud-sql-proxy PROJECT:REGION:I --port 5432` then `psql -h 127.0.0.1 -U USER DB -c 'select 1'`: a connection works through the proxy.

## Test first
Run migrations and queries against a local database of the same engine, and assert the connection factory's settings.
```python
def test_engine_uses_pool_limits_and_tls(make_engine):
    e = make_engine()
    assert e.pool.size() <= 5 and e.pool._max_overflow <= 5
    assert "sslmode" not in str(e.url) or "disable" not in str(e.url)
```

## Do
- Use private IP and disable the public IPv4 address unless there is a reason. If a public IP stays, keep authorized networks empty and connect through the Auth Proxy.
- Connect with the Cloud SQL Auth Proxy or a language connector, which encrypts traffic and authorizes by IAM (`roles/cloudsql.client`).
- Prefer IAM database authentication for service accounts. Otherwise keep the password in Secret Manager.
- Enable high availability for production, automated backups and point-in-time recovery, and deletion protection.
- Test a restore regularly into a new instance.
- Size connection pools to the instance's `max_connections` across all replicas of the app. Use a pooler for many small services.
- Run migrations from CI or a job with a separate, higher-privilege user than the app.
- Set maintenance windows and monitor CPU, disk and connections. Enable automatic storage increase.
- Create read replicas for read-heavy reporting.

## Avoid
- `0.0.0.0/0` in authorized networks: the database is exposed. Use the proxy.
- Using the `postgres` or `root` superuser from the app: create a least-privilege role.
- One pool per request or per function invocation: connections run out. Reuse a module-level pool with a small cap.
- Backups enabled but never restored: an untested backup is a guess. Restore to a clone.
- Skipping deletion protection: one command removes the instance. Turn it on.
- Passwords in environment variables set in plaintext IaC: use Secret Manager.
- Large migrations that lock tables at peak: run online-safe changes in steps.

## Review
- [ ] Private connectivity and proxy or connector auth.
- [ ] HA, backups, PITR and deletion protection on for prod.
- [ ] App user has minimal privileges, separate from the migration user.
- [ ] Pool sizes sum to under the connection limit.
- [ ] A restore has been rehearsed.
