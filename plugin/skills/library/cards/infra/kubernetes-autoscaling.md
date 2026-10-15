---
name: kubernetes-autoscaling
title: Kubernetes autoscaling
area: infra
tags: [kubernetes, hpa, vpa, keda, autoscaling, resources, scaling]
detect: []
related: [kubernetes, kubernetes-probes, prometheus, helm]
---
HPA, VPA and event-driven scaling: requests must be set, metrics must exist, and scale behavior should be tuned rather than defaulted.

## Verify
- `kubectl get hpa -n NS`: TARGETS shows real numbers, not `<unknown>`.
- `kubectl describe hpa NAME -n NS`: conditions `AbleToScale` and `ScalingActive` are True.
- `kubectl top pods -n NS`: the metrics API answers.
- `kubectl apply --dry-run=server -f hpa.yaml`: the manifest is valid.

## Test first
Render-and-assert the contract the HPA depends on.
```python
def test_hpa_target_has_requests(manifests):
    hpa = manifests.one("HorizontalPodAutoscaler", "api")
    dep = manifests.one("Deployment", hpa["spec"]["scaleTargetRef"]["name"])
    for c in dep["spec"]["template"]["spec"]["containers"]:
        assert "cpu" in c["resources"]["requests"]
    assert hpa["spec"]["minReplicas"] >= 2
```

## Do
- Use `autoscaling/v2` with explicit `metrics`; set `resources.requests` on every container, since utilization is a percent of requests.
- Set `minReplicas` of 2 or more for availability, and a `maxReplicas` that the cluster and downstream can absorb.
- Tune `behavior`: `scaleDown.stabilizationWindowSeconds` to avoid flapping, `scaleUp.policies` to cap bursts.
- Omit `spec.replicas` from the Deployment when an HPA owns it, so applies do not reset the count.
- Scale on a signal tied to load (RPS, queue depth via custom or external metrics, or KEDA scalers), not CPU alone for I/O-bound services.
- Pair with a PodDisruptionBudget and a cluster autoscaler or Karpenter so new pods can schedule.
- Run VPA in `Off` or recommendation mode alongside HPA.

## Avoid
- HPA on CPU with no CPU requests: TARGETS stays `<unknown>`. Set requests.
- HPA and VPA both acting on CPU or memory of the same workload: they fight. Let VPA only recommend, or scale on custom metrics.
- Leaving `replicas: N` in the Deployment manifest under GitOps: every sync resets the scale. Remove the field.
- Missing metrics-server: nothing scales and no error is obvious. Check `kubectl top`.
- `maxReplicas` unbounded in spirit (very high): a runaway loop drains the cluster or the database. Cap it.
- Scale to zero on a serving path without a wake-up buffer: first requests fail. Use KEDA with an interceptor, or keep one replica.

## Review
- [ ] Requests set on all containers of the scaled workload.
- [ ] Min, max and `behavior` are justified.
- [ ] No fight between HPA, VPA and a fixed `replicas` field.
- [ ] Readiness probe delays are accounted for in scale-up timing.
- [ ] Downstream limits (DB connections) survive max replicas.
