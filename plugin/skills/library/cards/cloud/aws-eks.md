---
name: aws-eks
title: AWS EKS
area: cloud
tags: [aws, eks, kubernetes, irsa, pod-identity, nodes, karpenter]
detect: [dep:@aws-sdk/client-eks, file:eksctl*.yaml]
related: [aws-vpc, aws-iam, aws-ec2, aws-cloudwatch, aws-ecs]
---
EKS clusters: private API endpoint where possible, IAM roles per service account, managed node groups, pinned versions and an upgrade routine.

## Verify
- `aws eks describe-cluster --name C --query 'cluster.[version,resourcesVpcConfig.endpointPublicAccess,resourcesVpcConfig.publicAccessCidrs,logging]'`: version, API exposure and control-plane logs.
- `aws eks list-access-entries --cluster-name C`: who has cluster access.
- `aws eks update-kubeconfig --name C && kubectl get nodes -o wide`: nodes Ready on the expected version.
- `kubectl auth can-i --list --as system:serviceaccount:NS:SA -n NS`: a workload account holds only what it needs.
- `kubectl get pods -A --field-selector=status.phase!=Running`: no stuck pods.

## Test first
Test the workload's AWS permission boundary before wiring the role.
```python
def test_pod_role_cannot_read_other_buckets(session_for_sa):
    s3 = session_for_sa("payments").client("s3")
    s3.get_object(Bucket="payments-data", Key="k")          # allowed
    with pytest.raises(ClientError) as e:
        s3.get_object(Bucket="hr-data", Key="k")
    assert e.value.response["Error"]["Code"] == "AccessDenied"
```

## Do
- Give each service account its own IAM role through EKS Pod Identity or IRSA. Scope the trust to the namespace and service account name.
- Manage cluster access with access entries and map IAM roles to Kubernetes groups. Avoid editing aws-auth for new clusters.
- Use managed node groups or Karpenter with several instance types and zones. Cordon and drain on upgrades.
- Set resource requests and limits, PodDisruptionBudgets, readiness probes and topology spread across zones.
- Enable control-plane logging for api, audit and authenticator. Install the CloudWatch or another log shipper.
- Upgrade one minor version at a time: control plane, then add-ons (VPC CNI, CoreDNS, kube-proxy), then nodes.
- Restrict the public endpoint with `publicAccessCidrs` or go private, and encrypt secrets with a KMS key.
- Pull images from ECR through a VPC endpoint, and scan on push.
- Apply NetworkPolicies and Pod Security Standards labels per namespace.

## Avoid
- Attaching broad IAM to the node role: every pod inherits it. Use pod-level roles and block pod access to IMDS (hop limit 1).
- Public API endpoint open to `0.0.0.0/0`: restrict the CIDRs or go private.
- Cluster-admin bound to humans by default: grant namespace-scoped roles.
- Skipping version upgrades: standard support ends and forced upgrades come on a deadline. Track the lifecycle.
- Running without requests: the scheduler overpacks nodes and pods get OOM-killed. Set both requests and limits.
- `latest` image tags: unreproducible rollouts. Pin digests or versions.
- Running out of IPs with the VPC CNI in small subnets: plan CIDRs or use prefix delegation.

## Review
- [ ] Workload roles via Pod Identity or IRSA with narrow trust.
- [ ] Endpoint access and control-plane logs configured.
- [ ] Nodes and add-ons on supported versions, with an upgrade plan.
- [ ] PDBs, probes, requests and zone spread on each workload.
- [ ] Images pinned and scanned.
