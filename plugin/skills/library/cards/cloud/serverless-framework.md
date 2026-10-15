---
name: serverless-framework
title: Serverless Framework
area: cloud
tags: [serverless, aws, lambda, yaml, deploy, plugins]
detect: [dep:serverless, dep:serverless-offline, dep:serverless-esbuild, dep:serverless-webpack, dep:serverless-python-requirements, file:serverless.yml, file:serverless.yaml, file:serverless.ts]
related: [aws-lambda, aws-sam, aws-cloudformation, aws-iam, localstack]
---
Serverless Framework services: `serverless.yml` compiled to CloudFormation, per-function IAM, stages and plugins.

## Verify
- `npx serverless print --stage dev`: the resolved config with variables expanded.
- `npx serverless package --stage dev`: the CloudFormation template and artifacts build into `.serverless/`.
- `npx serverless invoke local -f fn -p events/e.json`: a function runs locally with the event.
- `npx serverless deploy --stage dev`: deploys to a dev stage.
- `npx serverless logs -f fn --tail`: live function logs.

## Test first
Unit-test the handler; assert on the packaged template for infrastructure rules.
```typescript
import { readFileSync } from "node:fs";

test("no function role grants wildcard actions", () => {
  const t = JSON.parse(readFileSync(".serverless/cloudformation-template-update-stack.json", "utf8"));
  const doc = JSON.stringify(t.Resources.IamRoleLambdaExecution.Properties.Policies);
  expect(doc).not.toMatch(/"Action":\s*"\*"/);
});
```
Run `serverless package` before this test.

## Do
- Pin the framework major version in `package.json` and `frameworkVersion` in the config.
- Use stages (`--stage`, `${sls:stage}`) and `${param:...}` or SSM variables (`${ssm:/path}`) per stage.
- Prefer per-function IAM (a plugin) or tight `iam.role.statements` scoped to ARNs.
- Bundle with esbuild or a similar plugin to cut package size and cold starts.
- Set `provider.runtime`, `architecture`, `memorySize` and `timeout` explicitly.
- Use `Fn::GetAtt` and `Ref` in `resources:` for ARNs rather than hard-coded names.
- Set `deploymentBucket` and log retention (`logRetentionInDays`).
- Use `serverless-offline` for HTTP flows and unit tests for logic.
- Use `useDotenv` and keep secrets in SSM or Secrets Manager.

## Avoid
- `iam.role.statements` with `Resource: "*"` and `Action: "*"`: scope per function.
- Deploying to prod from a laptop: use CI with a role and a stage.
- Secrets in `environment:` as literals: they appear in the template and console.
- Hard-coded resource names in `resources:`: collisions across stages. Include `${sls:stage}`.
- Mixing framework major versions across teammates: pin and use `npx`.
- `serverless remove` on a stack with unretained data: set `DeletionPolicy: Retain`.
- Ignoring the CloudFormation 500-resource limit: split services.

## Review
- [ ] `serverless print` shows the intended stage values.
- [ ] IAM is scoped; no wildcard statements.
- [ ] Secrets come from SSM or Secrets Manager.
- [ ] Package is bundled; version pinned.
- [ ] Stateful resources retained.
