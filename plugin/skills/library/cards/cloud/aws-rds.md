---
name: aws-rds
title: AWS RDS and Aurora
area: cloud
tags: [aws, rds, aurora, postgres, mysql, database]
detect: [dep:@aws-sdk/client-rds, dep:@aws-sdk/rds-signer, dep:@aws-sdk/client-rds-data, dep:aws-cdk-lib]
related: [aws-iam, aws-lambda, aws-ecs, aws-cloudformation]
---
RDS and Aurora databases: private subnets, managed secrets, TLS, backups and pooling, tested restores and migrations.

## Verify
- `aws rds describe-db-instances --db-instance-identifier D --query 'DBInstances[0].[PubliclyAccessible,StorageEncrypted,MultiAZ,BackupRetentionPeriod,DeletionProtection]'`: not public, encrypted, backed up, protected.
- `aws rds describe-db-cluster-snapshots --db-cluster-identifier C --max-items 3`: recent snapshots exist (Aurora).
- `aws rds generate-db-auth-token --hostname H --port 5432 --username U --region R`: IAM auth token works for the user.
- `psql "host=H dbname=D user=U sslmode=verify-full sslrootcert=global-bundle.pem" -c 'select 1'`: TLS with certificate verification connects.

## Test first
Test migrations and queries against a local container of the same engine and major version, not a mock.
```python
def test_migration_is_reversible(pg_url):
    run("alembic", "upgrade", "head", url=pg_url)
    run("alembic", "downgrade", "-1", url=pg_url)
    run("alembic", "upgrade", "head", url=pg_url)
```
For infrastructure, a template assertion that `PubliclyAccessible` is false, `StorageEncrypted` true and `DeletionProtection` true.

## Do
- Keep instances in private subnets; allow the app security group on the DB port, not CIDR ranges.
- Let RDS manage the master password in Secrets Manager (`ManageMasterUserPassword`) and read it at runtime.
- Use RDS Proxy or an app pool for Lambda and bursty clients; set pool size below `max_connections`.
- Turn on automated backups, deletion protection and Performance Insights; test a point-in-time restore.
- Use parameter groups for settings; apply and reboot deliberately.
- Run migrations as a separate step before the new code, backward compatible (expand then contract).
- Use Multi-AZ for production; connect through the cluster endpoints (writer, reader).

## Avoid
- `PubliclyAccessible: true` to debug from a laptop: use SSM port forwarding or a bastion.
- A connection per Lambda invocation: it exhausts connections. Reuse at init or use a proxy.
- Hard-coding the instance endpoint after failover: use the cluster endpoint and a DNS TTL-aware client.
- Dropping a column in the same deploy as the code change: old tasks still read it.
- Plain-text master password in IaC or env: use the managed secret.
- `SkipFinalSnapshot: true` and `DeletionPolicy: Delete` on production.

## Review
- [ ] Private, encrypted, deletion-protected, backed up.
- [ ] Credentials from Secrets Manager or IAM auth, TLS enforced.
- [ ] Pool or proxy sized below `max_connections`.
- [ ] Migrations are backward compatible and tested up and down.
- [ ] Restore has been rehearsed.
