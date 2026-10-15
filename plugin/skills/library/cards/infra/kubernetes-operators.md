---
name: kubernetes-operators
title: Kubernetes operators
area: infra
tags: [kubernetes, operator, controller, crd, kubebuilder, reconcile, go]
detect: [file:PROJECT, dep:sigs.k8s.io/controller-runtime, dep:kopf, dep:kube]
related: [kubernetes, kubernetes-rbac, crossplane, helm]
---
Operators and controllers: idempotent reconcile loops, status conditions, finalizers and generated CRDs and RBAC.

## Verify
- `make manifests generate`: CRDs, RBAC and deepcopy regenerated (kubebuilder layout); commit the diff.
- `go vet ./... && go test ./...`: unit and envtest suites.
- `kubectl apply --dry-run=server -f config/samples/`: sample resources pass CRD validation.
- `kubectl get crd NAME -o jsonpath='{.spec.versions[*].name}'`: served versions are what you expect.

## Test first
Use envtest (real API server, no kubelet) and assert on observable state.
```go
It("creates the child Deployment and sets Ready", func() {
    Expect(k8sClient.Create(ctx, widget)).To(Succeed())
    Eventually(func() bool {
        var d appsv1.Deployment
        return k8sClient.Get(ctx, key, &d) == nil
    }, timeout, interval).Should(BeTrue())
})
```
Write a second test that calls reconcile twice and asserts no duplicate objects.

## Do
- Make reconcile idempotent: fetch, compute desired state, create or patch, update status. It can run at any time, many times.
- Set owner references (`controllerutil.SetControllerReference`) so children are garbage collected and `Owns()` triggers reconciles.
- Report progress with `status.conditions` and `observedGeneration`; update status through the status subresource.
- Use finalizers only for external cleanup; remove them on every deletion path.
- Use `RequeueAfter` for polling external systems; return errors for backoff rather than sleeping.
- Add kubebuilder markers for validation (`+kubebuilder:validation:`) and RBAC (`+kubebuilder:rbac:`), then regenerate.
- Version CRDs with a conversion plan before the first breaking change.

## Avoid
- Reconcile that depends on the event that triggered it: events coalesce. Read current state every time.
- Writing status with a full `Update` that races spec edits: use `Status().Patch` or `Status().Update` with conflict retry.
- Hand-edited generated files (`zz_generated.deepcopy.go`, CRD YAML): changes vanish. Edit markers and regenerate.
- Finalizer never removed on error paths: the object hangs in Terminating. Test deletion explicitly.
- Cluster-wide RBAC `*` markers: scope verbs and resources to what the controller touches.
- Caching reads of large kinds you do not watch: memory grows. Restrict cache by namespace or label.

## Review
- [ ] Reconcile is idempotent and tested twice in a row.
- [ ] Children have owner references; deletion is tested.
- [ ] Status conditions are meaningful and use the status subresource.
- [ ] Generated artifacts are regenerated and committed.
- [ ] RBAC markers are minimal.
