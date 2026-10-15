---
name: cloud-cost
title: Cloud cost control
area: cloud
tags: [cost, finops, budgets, tagging, aws, gcp, azure]
detect: []
related: [aws-lambda, aws-s3, gcp-cloud-run, azure-bicep, aws-cdk]
---
Cloud cost control: tag everything, set budgets and alerts, cap scaling, and review the biggest line items before shipping.

## Verify
- `aws ce get-cost-and-usage --time-period Start=2026-01-01,End=2026-02-01 --granularity MONTHLY --metrics UnblendedCost --group-by Type=DIMENSION,Key=SERVICE`: spend per service (use dates in your range).
- `aws budgets describe-budgets --account-id ACCOUNT_ID`: a budget with alert thresholds exists.
- `gcloud billing budgets list --billing-account=ACCOUNT_ID`: GCP budgets are configured.
- `az consumption budget list`: Azure budgets exist.
- `infracost breakdown --path .`: estimated monthly cost of the IaC change, if installed.

## Test first
Fail the build on untagged or uncapped resources.
```python
import json

def test_every_resource_has_cost_tags():
    plan = json.load(open("plan.json"))  # terraform show -json plan.out
    for r in plan["planned_values"]["root_module"]["resources"]:
        tags = r["values"].get("tags") or {}
        assert {"team", "env"} <= set(tags), r["address"]
```
Add a test that autoscaling max, concurrency limits and log retention are set.

## Do
- Apply mandatory tags or labels (`team`, `env`, `service`) through IaC defaults (provider `default_tags`, CDK `Tags.of`) and activate them as cost allocation tags.
- Create budgets with alerts at 50, 80 and 100 percent and a forecast alert.
- Cap scaling: Lambda reserved concurrency, Cloud Run `--max-instances`, autoscale maximums, queue consumer limits.
- Set retention on logs and metrics; expire temp object prefixes with lifecycle rules.
- Prefer managed commitments (savings plans, committed use) only after a stable baseline.
- Delete dev and preview environments automatically with a TTL.
- Watch data transfer: keep traffic in-region, use private endpoints or VPC endpoints, and cache at a CDN.
- Right-size from utilization metrics, and choose arm instances where compatible.
- Review the top five cost drivers in each PR that adds infrastructure.

## Avoid
- NAT gateway for all AWS traffic: S3 and DynamoDB gateway endpoints are free and avoid processing charges.
- Unbounded logging at debug level in production: ingestion costs more than compute.
- Autoscaling with no max: a retry storm or attack becomes a bill.
- Forgotten resources: unattached disks, idle load balancers, old snapshots. Tag with an owner and expiry.
- Cross-region or cross-AZ chatter by default.
- Estimating from the pricing page once: re-check after changes, using real usage.
- Alerting only on actual spend: add forecast alerts.

## Review
- [ ] All resources carry owner and environment tags.
- [ ] Budgets and alerts exist.
- [ ] Every scalable component has a ceiling.
- [ ] Logs and data have retention.
- [ ] The cost of the change is estimated and the biggest line items named.
