---
name: argo-cd
title: Argo CD
area: infra
tags: [argocd, gitops, kubernetes, applications, sync, appproject]
detect: [file:argocd/*.yaml, file:argocd/*.yml, file:applications/*.yaml, file:apps/*/application.yaml, file:applicationset.yaml]
related: [flux, kubernetes, helm, kustomize, vault]
---
Argo CD: GitOps with `Application` and `ApplicationSet` resources, AppProjects, sync policy, waves and hooks.

## Verify
- `argocd app diff <app> --local ./path`: what git would change in the live app.
- `argocd app sync <app> --dry-run`: previews the sync without applying.
- `argocd app wait <app> --health --timeout 120`: the app reached Healthy.
- `argocd app get <app> -o yaml`: sync status, health, and the last operation's message.
- `kubectl apply --dry-run=server -f argocd/`: the Application manifests are valid for the CRD.

## Test first
Render what Argo will apply and validate it before committing the Application.
```sh
kustomize build apps/web/overlays/prod | kubectl apply --dry-run=server -f -
argocd app diff web --local apps/web/overlays/prod --exit-code   # red until the diff is intended
argocd app wait web --health --timeout 120
```
For an `ApplicationSet`, check the generated list: `kubectl get applications -n argocd -l app.kubernetes.io/instance=<set>`.

## Do
- Keep `Application` objects in a repo and bootstrap them with an app-of-apps or an `ApplicationSet`.
- Scope each team with an `AppProject` listing allowed `sourceRepos`, `destinations` and `clusterResourceWhitelist`.
- Set `syncPolicy.automated: { prune: true, selfHeal: true }` once stable, with `syncOptions: [CreateNamespace=true]`.
- Order resources with `argocd.argoproj.io/sync-wave` annotations and run jobs with `PreSync` or `PostSync` hook annotations.
- Pin `targetRevision` to a tag or SHA for production and a branch only for dev.
- Use `ignoreDifferences` with `jsonPointers` or `managedFieldsManagers` for fields controllers mutate (HPA replicas).
- Set `retry` in `syncPolicy` and `finalizers: [resources-finalizer.argocd.argoproj.io]` to cascade deletes deliberately.
- Keep secrets out of git: use External Secrets, Sealed Secrets or an Argo CD Vault plugin.

## Avoid
- `project: default` for everything: it allows any repo and cluster. Create scoped AppProjects.
- `targetRevision: HEAD` in prod: an unreviewed push deploys. Pin a tag.
- `prune: true` before checking the diff: a path move deletes workloads. Preview first.
- Fighting a controller: an HPA or webhook changes a field and the app shows OutOfSync forever. Add `ignoreDifferences`.
- Plaintext Secrets in the app repo: they are base64 only. Use a secrets operator.
- `kubectl edit` on live resources with `selfHeal` on: Argo reverts it. Change git.
- CRDs and their custom resources in the same wave: the resource fails first. Put CRDs earlier or use `SkipDryRunOnMissingResource=true`.
- Huge manifests with the default last-applied annotation: they exceed limits. Use `ServerSideApply=true`.

## Review
- [ ] Applications live in git, project-scoped, with pinned revisions in production.
- [ ] Sync policy and `ignoreDifferences` match how controllers behave.
- [ ] Secrets come from an external mechanism and not from plaintext in the repo.
- [ ] The diff and a server dry run are clean before merge.
