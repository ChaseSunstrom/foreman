---
name: aws-vpc
title: AWS VPC networking
area: cloud
tags: [aws, vpc, networking, subnets, security-groups, nat, endpoints]
detect: [dep:@aws-sdk/client-ec2]
related: [aws-ec2, aws-eks, aws-rds, aws-iam, aws-cloudformation]
---
VPC design: public, private and isolated subnets across zones, tight security groups, endpoints for AWS services, flow logs on.

## Verify
- `aws ec2 describe-subnets --filters Name=vpc-id,Values=VPC --query 'Subnets[].[SubnetId,AvailabilityZone,CidrBlock,MapPublicIpOnLaunch]'`: at least two zones and no private subnet auto-assigns public IPs.
- `aws ec2 describe-route-tables --filters Name=vpc-id,Values=VPC --query 'RouteTables[].Routes[]'`: private subnets route to NAT, not to the internet gateway.
- `aws ec2 describe-security-groups --filters Name=ip-permission.cidr,Values=0.0.0.0/0 --query 'SecurityGroups[].[GroupId,GroupName]'`: groups open to the world, each one justified.
- `aws ec2 describe-flow-logs`: flow logs are enabled.
- `aws ec2 describe-vpc-endpoints --filters Name=vpc-id,Values=VPC`: endpoints for S3 and other heavy services exist.

## Test first
Assert reachability intent with an IaC test or a policy check before creating resources.
```python
def test_no_ingress_from_world_except_alb(sgs):
    open_sgs = [g for g in sgs if any(r["cidr"] == "0.0.0.0/0" for r in g["ingress"])]
    assert [g["name"] for g in open_sgs] == ["alb"]
```

## Do
- Plan CIDRs that do not overlap with other VPCs, on-premises ranges or peers. Leave room for growth, since a primary CIDR cannot be shrunk.
- Spread public, private app and isolated data subnets over at least two zones.
- Put databases and workloads in private subnets. Only load balancers and NAT sit in public ones.
- Reference security groups by id in rules (app SG allows from ALB SG) instead of CIDRs.
- Add a gateway endpoint for S3 and DynamoDB (no cost) and interface endpoints for ECR, Secrets Manager, STS and logs when private workloads need them.
- Use one NAT gateway per zone for production, and note the cost trade-off if you use one.
- Enable VPC Flow Logs to CloudWatch Logs or S3, and use network ACLs only for coarse subnet-level denies.
- Tag everything and manage it with IaC. Remove the default VPC use from workloads.

## Avoid
- `0.0.0.0/0` on SSH, RDP or database ports: use SSM Session Manager or a bastion with a narrow source range.
- Databases with `PubliclyAccessible` on: keep them in isolated subnets with SG-to-SG rules.
- All traffic to S3 through NAT: pays per GB. Add a gateway endpoint.
- Egress `0.0.0.0/0` everywhere without thought: restrict where data-exfiltration risk matters, and use endpoint policies.
- A single-zone design: a zone outage takes everything down. Use two or three.
- Overly small subnets (/28) for EKS or Lambda ENIs: IPs run out. Size generously.
- Peering assuming transitive routing: it is not transitive. Use Transit Gateway when needed.

## Review
- [ ] Subnet tiers span multiple zones with correct route tables.
- [ ] No data store is internet reachable.
- [ ] Security groups are minimal and reference other groups.
- [ ] Endpoints cover S3 and high-volume AWS APIs.
- [ ] Flow logs and tags are present in IaC.
