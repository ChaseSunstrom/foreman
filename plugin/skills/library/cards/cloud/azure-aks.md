---
name: azure-aks
title: Azure AKS
area: cloud
tags: [azure, aks, kubernetes, workload-identity, entra, nodes]
detect: [dep:@azure/arm-containerservice, dep:azure-mgmt-containerservice]
related: [azure-entra-id, azure-key-vault, aws-eks, gcp-gke, azure-bicep]
---
AKS clusters: Entra-integrated access with Kubernetes RBAC, workload identity for pods, managed upgrades, system and user node pools, and private networking.

## Verify
- `az aks show -g RG -n C --query '{ver:kubernetesVersion,oidc:oidcIssuerProfile.enabled,wi:securityProfile.workloadIdentity.enabled,aad:aadProfile.managed,private:apiServerAccessProfile.enablePrivateCluster}'`: version, OIDC issuer, workload identity, Entra integration and private API.
- `az aks get-credentials -g RG -n C && kubectl get nodes -o wide`: nodes Ready.
- `az aks nodepool list -g RG --cluster-name C -o table`: system and user pools, sizes and versions.
- `az aks get-upgrades -g RG -n C -o table`: pending upgrade targets.
- `kubectl auth can-i --list -n NS --as system:serviceaccount:NS:SA`: pod identity permissions are narrow.

## Test first
Verify a pod gets its own identity and only that identity's permissions.
```python
def test_pod_identity_cannot_read_other_vault(secret_client_for):
    ok = secret_client_for("orders-vault").get_secret("db")
    assert ok.value
    with pytest.raises(HttpResponseError) as e:
        secret_client_for("hr-vault").get_secret("db")
    assert e.value.status_code == 403
```

## Do
- Enable the OIDC issuer and workload identity. Create a user-assigned managed identity per workload with a federated credential bound to the namespace and service account.
- Integrate with Entra ID and use Azure RBAC for Kubernetes or Kubernetes RBAC with group bindings. Disable local accounts where possible.
- Keep a dedicated system pool, with the `CriticalAddonsOnly` taint, and separate user pools per workload class. Spread across availability zones.
- Choose an upgrade channel and set planned maintenance windows. Use surge settings on node pools.
- Prefer a private cluster or authorized IP ranges on the API server.
- Use Azure CNI Overlay or Azure CNI with subnets sized for pods. Apply network policies.
- Pull from Azure Container Registry using the kubelet identity with `AcrPull`.
- Pull secrets through the Key Vault secrets store CSI driver using workload identity.
- Set requests, limits, PodDisruptionBudgets and probes. Turn on Container insights or managed Prometheus.

## Avoid
- Putting credentials in pods or using the kubelet identity for apps: it is shared by the node pool. Use workload identity.
- Deprecated AAD Pod Identity for new work: use workload identity.
- A public API server open to all: add authorized ranges or make it private.
- Running apps on the system pool: they compete with CoreDNS and addons. Use user pools.
- Subnets too small for the pod CIDR: scale-out fails at IP exhaustion. Plan the network.
- Skipping upgrades until the version is out of support: forced jumps break workloads. Track the support window.
- `cluster-admin` for broad groups: bind namespace roles.

## Review
- [ ] Workload identity per app, no secrets in manifests.
- [ ] Entra RBAC, local accounts off, API access restricted.
- [ ] System and user pools separated across zones.
- [ ] Upgrade channel and maintenance window defined.
- [ ] Workloads have requests, probes and PDBs.
