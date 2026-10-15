---
name: gcp-gke
title: GCP GKE
area: cloud
tags: [gcp, gke, kubernetes, workload-identity, autopilot, nodes]
detect: [dep:@google-cloud/container, dep:google-cloud-container]
related: [gcp-iam, aws-eks, azure-aks, gcp-cloud-sql]
---
GKE clusters: Workload Identity for pod credentials, private nodes, release channels, regional control planes, and resource requests on every workload.

## Verify
- `gcloud container clusters describe C --region R --format='value(releaseChannel.channel,workloadIdentityConfig.workloadPool,privateClusterConfig.enablePrivateNodes)'`: channel, Workload Identity pool and private nodes.
- `gcloud container clusters get-credentials C --region R && kubectl get nodes`: access works and nodes are Ready.
- `gcloud projects get-iam-policy P --flatten=bindings --filter=bindings.members:serviceAccount:SA --format='table(bindings.role)'`: the workload's service account holds only intended roles.
- `kubectl get pods -A --field-selector=status.phase!=Running`: no stuck pods.
- `kubectl auth can-i --list -n NS --as system:serviceaccount:NS:SA`: Kubernetes permissions are narrow.

## Test first
Check the identity boundary from inside a pod before shipping the manifest.
```python
def test_pod_can_read_only_its_bucket(gcs_client_as_pod):
    assert gcs_client_as_pod.bucket("app-data").blob("k").exists() in (True, False)
    with pytest.raises(Forbidden):
        gcs_client_as_pod.bucket("other-data").blob("k").download_as_bytes()
```

## Do
- Enable Workload Identity Federation for GKE and bind a Kubernetes service account to a Google service account (or grant roles directly to the principal). Annotate the Kubernetes service account.
- Use Autopilot unless you need node-level control, and Standard with node auto-provisioning otherwise.
- Make clusters regional, private-node, with authorized networks on the control-plane endpoint.
- Subscribe to a release channel for automatic upgrades. Set maintenance windows and exclusions.
- Set requests, limits, PodDisruptionBudgets and probes. Spread pods across zones.
- Use Cloud Logging and Managed Prometheus, and alert on restarts and pending pods.
- Pull images from Artifact Registry with a dedicated node service account that has only `roles/artifactregistry.reader` and logging roles.
- Apply NetworkPolicy and namespace-level Pod Security labels. Enable Binary Authorization for production images.

## Avoid
- Running nodes as the default Compute Engine service account with Editor: every pod inherits it. Use a minimal node service account and Workload Identity.
- Downloading service account JSON keys into secrets: long-lived and leakable. Use Workload Identity.
- A public control-plane endpoint open to all: set authorized networks or private endpoint.
- Legacy ABAC or basic auth: use IAM and RBAC.
- Pinning to a static version with no channel: you fall out of support. Use a release channel.
- `cluster-admin` for developers: bind namespace roles through groups.
- Pods with no requests on Standard: bin packing fails and noisy neighbors appear.

## Review
- [ ] Workload Identity in use, no key files in the cluster.
- [ ] Private nodes, authorized networks, release channel set.
- [ ] Node service account minimal.
- [ ] Workloads carry requests, probes, PDBs.
- [ ] Images come from a scanned registry with pinned tags or digests.
