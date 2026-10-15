---
name: aws-ec2
title: AWS EC2
area: cloud
tags: [aws, ec2, instances, ami, autoscaling, imds, ssm]
detect: [dep:@aws-sdk/client-ec2, dep:@aws-sdk/client-auto-scaling, dep:@aws-sdk/client-ssm]
related: [aws-vpc, aws-iam, aws-cloudwatch, aws-kms, aws-cloudformation]
---
EC2 instances: IMDSv2 only, instance profiles not keys, SSM instead of SSH, encrypted volumes, Auto Scaling groups with health checks.

## Verify
- `aws ec2 describe-instances --query 'Reservations[].Instances[].[InstanceId,MetadataOptions.HttpTokens,IamInstanceProfile.Arn]'`: `HttpTokens` is `required` and a profile is attached.
- `aws ec2 describe-volumes --filters Name=encrypted,Values=false --query 'Volumes[].VolumeId'`: no unencrypted volumes.
- `aws ssm describe-instance-information --query 'InstanceInformationList[].[InstanceId,PingStatus]'`: instances are managed by SSM.
- `aws autoscaling describe-auto-scaling-groups --query 'AutoScalingGroups[].[AutoScalingGroupName,HealthCheckType,MinSize,MaxSize]'`: health check type and size bounds.
- `aws ec2 get-ebs-encryption-by-default`: account default encryption is on.

## Test first
Check launch template settings in a policy test before instances exist.
```python
def test_launch_template_forces_imdsv2(lt):
    assert lt["MetadataOptions"]["HttpTokens"] == "required"
    assert lt["MetadataOptions"]["HttpPutResponseHopLimit"] == 1
    assert all(b["Ebs"]["Encrypted"] for b in lt["BlockDeviceMappings"])
```

## Do
- Launch from a launch template with `HttpTokens: required` and hop limit 1, which blocks IMDSv1 and most SSRF credential theft.
- Attach an instance profile with a least-privilege role. Never place access keys on instances.
- Use SSM Session Manager for access and patching, with no inbound port 22.
- Bake an AMI (or use a current maintained AMI through an SSM parameter) and keep user data short and idempotent.
- Encrypt EBS volumes with a KMS key, and snapshot with a lifecycle policy.
- Put instances in an Auto Scaling group behind a load balancer with ELB health checks, across zones. Treat instances as replaceable.
- Pick instance types by measurement. Consider Graviton for compatible workloads, and Spot only for interruption-tolerant work.
- Install the CloudWatch agent for memory and disk metrics and ship logs off the box.
- Tag for owner, environment and cost allocation.

## Avoid
- IMDSv1 left enabled: an SSRF bug leaks role credentials. Require tokens.
- SSH keys shared among people and open to the world: use SSM and per-user access.
- Secrets in user data: readable through the metadata service and console. Fetch from Secrets Manager at boot.
- Pets: hand-configured servers with no AMI or IaC. Rebuild from the template.
- Assuming root volume survives: instance store and terminated-instance volumes are lost. Keep state in EBS with snapshots, RDS or S3.
- Public IPs on app instances: place them in private subnets behind a load balancer.
- `AdministratorAccess` on the instance role: scope to the buckets, queues and parameters used.

## Review
- [ ] Launch template enforces IMDSv2 and encrypted volumes.
- [ ] No keys on disk, no inbound SSH from the internet.
- [ ] Group spans zones with ELB health checks and scaling policy.
- [ ] Role policy is scoped.
- [ ] Logs and metrics leave the instance.
