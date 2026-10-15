---
name: aws-kinesis
title: AWS Kinesis Data Streams
area: cloud
tags: [aws, kinesis, streaming, shards, consumers, firehose]
detect: [dep:@aws-sdk/client-kinesis, dep:amazon-kinesis-client, dep:aws-kinesis-agg]
related: [aws-lambda, aws-sqs-sns, aws-cloudwatch, localstack, aws-eventbridge]
---
Kinesis Data Streams: partition keys that spread load, batched puts with partial-failure handling, idempotent consumers, and iterator-age alarms.

## Verify
- `aws kinesis describe-stream-summary --stream-name S --query 'StreamDescriptionSummary.[StreamModeDetails,OpenShardCount,RetentionPeriodHours,EncryptionType]'`: capacity mode, shards, retention and encryption.
- `aws kinesis put-record --stream-name S --partition-key k1 --data $(echo -n hi | base64)`: a smoke write returns a shard id and sequence number.
- `aws kinesis list-stream-consumers --stream-arn ARN`: enhanced fan-out consumers.
- `aws cloudwatch get-metric-statistics --namespace AWS/Kinesis --metric-name GetRecords.IteratorAgeMilliseconds --dimensions Name=StreamName,Value=S --start-time T0 --end-time T1 --period 300 --statistics Maximum`: consumers keep up.

## Test first
Test the producer's partial-failure handling and the consumer's idempotency first.
```python
def test_producer_retries_only_failed_records(kinesis_stub, producer):
    kinesis_stub.put_records_returns(failed=[1])           # FailedRecordCount = 1
    producer.send([r0, r1, r2])
    assert kinesis_stub.sent_batches == [[r0, r1, r2], [r1]]
```

## Do
- Choose on-demand mode unless traffic is predictable, in which case provisioned shards are cheaper.
- Pick partition keys with many distinct values (entity id) so records spread across shards. Records with the same key stay ordered within a shard.
- Use `PutRecords` in batches (up to 500 records) and retry only entries with an `ErrorCode`, with backoff.
- Make consumers idempotent: delivery is at least once and a Lambda batch can be retried. Checkpoint after processing.
- For Lambda consumers set `BisectBatchOnFunctionError`, `MaximumRetryAttempts` and an on-failure destination so a poison record does not block a shard.
- Use enhanced fan-out when several consumers read the same stream at full speed.
- Turn on server-side encryption with KMS and alarm on `IteratorAgeMilliseconds`, `WriteProvisionedThroughputExceeded` and `ReadProvisionedThroughputExceeded`.
- Set retention to cover your longest consumer outage and replay window.

## Avoid
- A constant or low-cardinality partition key: one hot shard throttles everything. Use a high-cardinality key.
- Ignoring `FailedRecordCount` in a `PutRecords` response: records are silently dropped. Inspect each entry.
- Assuming global order: order holds only per shard and key. Include sequence numbers in the payload.
- A Lambda that throws on one bad record with no bisect or DLQ: the shard stalls until the record expires. Configure failure handling.
- Using the shared-throughput `GetRecords` loop with many consumers: they split read limits. Use enhanced fan-out.
- Records over the 1 MiB limit: store the payload in S3 and send a pointer.
- Wildcard `kinesis:*` on `*`: grant only put or read actions on the stream ARN.

## Review
- [ ] Partition key spreads load and its ordering expectation is documented.
- [ ] Producers handle partial failure, consumers are idempotent.
- [ ] Poison records have a bisect or DLQ path.
- [ ] Iterator age and throttle alarms exist.
- [ ] Encryption on and IAM scoped to the stream.
