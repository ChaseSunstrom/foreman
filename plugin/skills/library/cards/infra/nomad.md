---
name: nomad
title: Nomad
area: infra
tags: [nomad, scheduler, jobs, hashicorp, orchestration, hcl]
detect: [file:*.nomad, file:*.nomad.hcl, file:nomad.hcl]
related: [consul, vault, docker, terraform]
---
Nomad: job specs planned before submission, with resources, health checks, update strategy and ACLs set deliberately.

## Verify
- `nomad job validate job.nomad.hcl`: the spec parses and validates.
- `nomad job plan job.nomad.hcl`: dry-run showing placements and diffs; it prints a check-index for safe submit.
- `nomad job run -check-index N job.nomad.hcl`: submit only if the job has not changed since the plan.
- `nomad job status NAME`: allocations and deployment state.
- `nomad alloc logs ALLOC`: task output for a failing allocation.

## Test first
Make validation and planning gates, then check placement.
```bash
nomad job validate job.nomad.hcl
nomad job plan -exit-code job.nomad.hcl; test $? -ne 255   # 255 means plan error
nomad job run job.nomad.hcl
curl -fs "http://$(nomad service info -t '{{(index . 0).Address}}:{{(index . 0).Port}}' api)/healthz"
```

## Do
- Set `resources { cpu memory }` on every task; Nomad uses them for bin packing and enforces memory.
- Use `group { count = N }` with `update { max_parallel health_check = "checks" min_healthy_time healthy_deadline auto_revert = true }` for safe rollouts.
- Add `service { name port check { type = "http" path interval timeout } }` (Nomad or Consul provider) so health gates deployments.
- Use `restart` and `reschedule` blocks to bound retry loops.
- Fetch secrets with the `template` block and Vault integration (`vault { }` with workload identity) rather than env literals.
- Use `variable` blocks and `-var-file` for per-environment values; keep job files in git.
- Constrain placement with `constraint` and `affinity`; spread with `spread`.
- Enable ACLs and TLS on servers and clients; use scoped tokens or workload identity for CI.

## Avoid
- Tasks without memory limits sized to reality: OOM kills or overpacking. Measure and set.
- `job run` without `plan` in CI: surprise evictions. Always plan and use `-check-index`.
- `auto_revert = false` with unhealthy canaries left running: manual cleanup. Enable auto revert.
- Plain secrets in `env` blocks: visible in job spec and API. Use templates with Vault.
- `count = 1` stateful jobs on ephemeral disks with no `volume` or `ephemeral_disk { sticky migrate }`: data loss on reschedule. Use host or CSI volumes.
- Unbounded `restart` attempts: a crash loop eats the node. Set `attempts`, `interval` and `mode = "fail"`.

## Review
- [ ] `validate` and `plan` pass in CI.
- [ ] Every task has resources, health checks and an update block.
- [ ] Secrets come from Vault templates.
- [ ] Stateful tasks use proper volumes.
- [ ] ACLs and TLS are enabled.
