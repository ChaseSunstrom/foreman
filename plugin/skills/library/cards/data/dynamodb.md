---
name: dynamodb
title: DynamoDB
area: data
tags: [nosql, dynamodb, aws, single-table, keys, gsi]
detect: [dep:@aws-sdk/client-dynamodb, dep:@aws-sdk/lib-dynamodb, dep:boto3, dep:aws-sdk-dynamodb, dep:aws-sdk-go-v2/service/dynamodb, dep:dynamodb-toolbox, dep:AWSSDK.DynamoDBv2, dep:PynamoDB, dep:dynamodb-onetable]
related: [cassandra, redis, kafka]
---
DynamoDB: access-pattern-first key design, conditional writes, queries not scans, on-demand or planned capacity.

## Verify
- `aws dynamodb describe-table --table-name T`: keys, GSIs, billing mode, TTL and stream settings.
- `aws dynamodb query --table-name T --key-condition-expression "pk = :p" --expression-attribute-values '{":p":{"S":"x"}}' --return-consumed-capacity TOTAL`: the access pattern and its capacity cost.
- `aws dynamodb describe-time-to-live --table-name T`: TTL attribute is enabled.
- `aws dynamodb list-tables --endpoint-url http://localhost:8000`: tests target local DynamoDB, not AWS.

## Test first
Run DynamoDB Local (or a mock with real semantics) and create the table from the same definition as infra.
```python
def test_no_double_create(table):
    put_user(table, "u1")
    with pytest.raises(ClientError) as e:
        put_user(table, "u1")
    assert e.value.response["Error"]["Code"] == "ConditionalCheckFailedException"
```

## Do
- List access patterns first; derive partition key (high cardinality, even traffic) and sort key from them.
- Use `Query` with key conditions; add GSIs for alternate patterns and project only needed attributes.
- Guard writes with `ConditionExpression` (`attribute_not_exists(pk)`, version checks) for uniqueness and optimistic locking.
- Use `UpdateItem` with `SET`/`ADD` expressions for atomic increments.
- Paginate with `LastEvaluatedKey` until absent.
- Use `BatchWriteItem`/`TransactWriteItems` and retry `UnprocessedItems` with backoff.
- Enable TTL for expiry, PITR for backups, and set a ProjectionExpression to cut payload.

## Avoid
- `Scan` in request paths: reads the whole table. Add a key or GSI.
- Low-cardinality partition keys (status, date): hot partitions throttle. Add a shard suffix or better key.
- Reading then writing (`GetItem` then `PutItem`): lost updates. Use conditions or update expressions.
- Ignoring `UnprocessedItems` and `LastEvaluatedKey`: silent data loss and truncated reads. Loop.
- Reserved words in expressions (`name`, `status`): validation error. Use `ExpressionAttributeNames`.
- Items near 400 KB or large blobs: store in S3 and keep a pointer.
- Eventually consistent reads where read-your-writes is required: set `ConsistentRead` (not on GSIs).
- Float in the document client (`boto3` rejects `float`): use `Decimal`.

## Review
- [ ] Every access pattern maps to Query/GetItem on a key or GSI.
- [ ] Writes that must not clobber have condition expressions.
- [ ] Pagination and unprocessed items are handled.
- [ ] Key distribution avoids hot partitions.
- [ ] Tests use local DynamoDB, never real AWS.
