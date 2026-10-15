---
name: aws-cdk
title: AWS CDK
area: cloud
tags: [aws, cdk, iac, cloudformation, typescript, constructs]
detect: [dep:aws-cdk-lib, dep:aws-cdk, dep:constructs, file:cdk.json]
related: [aws-cloudformation, aws-iam, aws-lambda, aws-sam]
---
AWS CDK v2 apps: constructs synthesised to CloudFormation, grants over hand-written policies, snapshot and assertion tests.

## Verify
- `npx cdk synth --quiet`: the app synthesises with no errors.
- `npx cdk diff`: exactly the intended changes, especially replacements and IAM changes.
- `npx cdk doctor`: the environment and CLI versions are sane.
- `npm test`: assertions and snapshots pass (Jest by default; use `npx vitest run` if configured).

## Test first
Assert on the synthesised template.
```typescript
import { App } from "aws-cdk-lib";
import { Template } from "aws-cdk-lib/assertions";
import { DataStack } from "../lib/data-stack";

test("bucket is encrypted and blocks public access", () => {
  const t = Template.fromStack(new DataStack(new App(), "T"));
  t.hasResourceProperties("AWS::S3::Bucket", {
    PublicAccessBlockConfiguration: { BlockPublicAcls: true },
  });
});
```
Tests live in `test/`. Prefer fine-grained assertions over whole-template snapshots.

## Do
- Import from `aws-cdk-lib` (single v2 package) and `constructs`.
- Use `grantRead`, `grantWrite`, `grantInvoke` for permissions rather than raw `PolicyStatement`.
- Wrap repeated patterns in your own `Construct`, not copy-pasted resources.
- Let CDK generate physical names; pass values between stacks by props and references.
- Set `removalPolicy` explicitly on stateful resources (buckets, tables, databases) and `RETAIN` for production data.
- Pin the account and region in `env` when you use lookups (`Vpc.fromLookup`); commit `cdk.context.json`.
- Run `cdk bootstrap` once per account and region before first deploy.
- Use `cdk-nag` or Aspects to enforce policy.

## Avoid
- v1 imports (`@aws-cdk/aws-s3`) or `core.Construct`: use `aws-cdk-lib/aws-s3` and `constructs`.
- Hard-coded `bucketName` or `tableName`: a rename or second deploy collides, and it forces replacement.
- Branching on a token value (`if (bucket.bucketName === ...)`): tokens resolve at deploy time. Use `CfnCondition` or context.
- Defaults deleting data: `autoDeleteObjects` and `DESTROY` on a prod bucket.
- Skipping `cdk diff` before deploy: a changed logical id replaces the resource.
- Editing generated templates in `cdk.out/`: change the code.
- Giant single stacks: they hit the 500-resource limit; split by lifecycle.

## Review
- [ ] `cdk diff` reviewed, no surprise replacements.
- [ ] Stateful resources have an explicit removal policy.
- [ ] Permissions come from grants and are least-privilege.
- [ ] Assertion tests cover security-relevant properties.
- [ ] Context and lookups are committed and env pinned.
