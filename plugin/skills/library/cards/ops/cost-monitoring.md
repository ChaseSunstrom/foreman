---
name: cost-monitoring
title: Cost monitoring
area: ops
tags: [cost, finops, budgets, tagging, cloud, anomaly]
detect: []
related: [capacity-planning, log-pipelines, disaster-recovery, slos-alerting]
---
Track spend per service with enforced tags, budget alerts, and anomaly checks, and tie each saving to a measured number.

## Verify
- `aws ce get-cost-and-usage --time-period Start=2026-10-01,End=2026-10-15 --granularity DAILY --metrics UnblendedCost --group-by Type=TAG,Key=service`: daily spend per service tag (AWS).
- `aws budgets describe-budgets --account-id <id>`: budgets exist with thresholds (AWS).
- `aws resourcegroupstaggingapi get-resources --tag-filters Key=owner`: resources carrying an owner tag.
- `kubectl top pods -A --sort-by=memory | head`: heaviest consumers in a cluster (Kubernetes with metrics-server).
- `df -h` and `du -xh --max-depth=1 /var | sort -h | tail`: local disk growth hot spots.

## Test first
Make the untagged-resource check a failing test, then tag until it passes.
```sh
set -e
n=$(aws resourcegroupstaggingapi get-resources --resources-per-page 100 \
  --query 'length(ResourceTagMappingList[?!not_null(Tags[?Key==`owner`])])' --output text)
[ "$n" -eq 0 ] || { echo "$n resources lack an owner tag"; exit 1; }
```
Also test the alert path: send a budget notification to the channel and confirm a human sees it.

## Do
- Enforce tags (`owner`, `service`, `env`, `cost-center`) at creation through policy or IaC modules, not by hope.
- Set budgets per team and environment with alerts at forecast and actual thresholds (for example 50, 80, 100 percent).
- Turn on anomaly detection or a daily delta alert, and route it to an owned channel.
- Review the top ten cost lines weekly: compute, storage, data transfer, logs and metrics volume, managed databases.
- Attack the biggest first: rightsize from utilization data, delete orphans (unattached volumes, old snapshots, idle load balancers), and add lifecycle rules.
- Expire non-production on a schedule (stop or scale to zero at night) and set TTLs on temporary stacks.
- Use commitment discounts only for steady baseline, after rightsizing.
- Include cost in capacity tests and design reviews (cost per request or per customer).

## Avoid
- Judging by the total only: a doubled line item hides in noise. Break down by tag and service.
- Optimizing before tagging: unowned spend stays unowned. Fix attribution first.
- Buying a reserved commitment before rightsizing: you lock in waste. Rightsize, then commit.
- Ignoring data transfer and log ingestion: they surprise the bill. Check egress, cross-zone traffic, and per-GB ingest.
- Leaving test environments up: spend accrues silently. Add TTL tags and a reaper.
- Alerts that go to nobody: the overrun lands at month end. Assign an owner per budget.

## Review
- [ ] Every resource has an owner and service tag, and the check runs in CI or on a schedule.
- [ ] Budgets and anomaly alerts exist and reach an owned channel.
- [ ] The top cost lines have a named owner and a reviewed trend.
- [ ] Orphaned resources and idle environments are removed on a schedule.
- [ ] Each claimed saving has before and after numbers.
