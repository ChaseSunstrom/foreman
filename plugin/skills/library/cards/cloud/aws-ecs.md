---
name: aws-ecs
title: AWS ECS
area: cloud
tags: [aws, ecs, fargate, containers, task-definition, deploy]
detect: [dep:@aws-sdk/client-ecs, file:task-definition.json, file:ecs-params.yml, file:*taskdef*.json]
related: [aws-iam, aws-cloudformation, aws-cdk, aws-rds]
---
AWS ECS on Fargate or EC2: task definitions, task vs execution roles, health-checked services, rolling deploys with rollback.

## Verify
- `aws ecs describe-services --cluster C --services S --query 'services[0].[runningCount,desiredCount,deployments[].rolloutState]'`: the deployment completed.
- `aws ecs describe-tasks --cluster C --tasks T --query 'tasks[0].stoppedReason'`: why a task stopped (image pull, OOM, health check).
- `aws ecs wait services-stable --cluster C --services S`: the service reached steady state.
- `aws ecs execute-command --cluster C --task T --container app --interactive --command sh`: shell into a running task (needs ECS Exec enabled).

## Test first
The check that fails first is a smoke request against the health route plus a task-definition lint.
```python
import json

def test_taskdef_has_limits_and_health():
    td = json.load(open("deploy/task-definition.json"))
    c = td["containerDefinitions"][0]
    assert td["taskRoleArn"] and td["executionRoleArn"]
    assert c.get("healthCheck")
    assert td.get("memory") or c.get("memory")
    assert ":latest" not in c["image"]
```
Then `curl -fsS https://HOST/healthz` after deploy.

## Do
- Separate roles: `executionRoleArn` pulls images and reads secrets, `taskRoleArn` is what the app code uses.
- Pin images by tag or digest produced by CI.
- Inject secrets with `secrets` (`valueFrom` Secrets Manager or SSM ARN), not `environment`.
- Define a container `healthCheck` and set the load balancer target group health check path and grace period.
- Enable the deployment circuit breaker with rollback.
- Send logs with the `awslogs` driver and set a retention period.
- Set CPU and memory at task and container level; size from metrics.
- Run tasks in private subnets with a security group per service.
- Handle SIGTERM: ECS sends it, then SIGKILL after `stopTimeout`.

## Avoid
- `latest` image tags: a deploy can't be traced or rolled back.
- Reusing one role for both execution and task: pull access leaks to app code.
- Missing `healthCheckGracePeriodSeconds` on slow-start apps: the ALB kills tasks in a loop.
- Putting secrets in `environment`: visible in `describe-task-definition`.
- Assigning public IPs to Fargate tasks to reach ECR: use NAT or VPC endpoints.
- `force-new-deployment` as a fix for a bad task definition: register a corrected revision.
- Forgetting a new task definition revision is needed for any container change.

## Review
- [ ] Task and execution roles are distinct and minimal.
- [ ] Image is an immutable tag; secrets come from `secrets`.
- [ ] Health checks and grace period set; circuit breaker on.
- [ ] Log group has retention.
- [ ] Container handles SIGTERM within `stopTimeout`.
