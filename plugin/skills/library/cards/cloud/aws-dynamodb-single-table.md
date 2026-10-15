---
name: aws-dynamodb-single-table
title: AWS DynamoDB single-table design
area: cloud
tags: [aws, dynamodb, nosql, single-table, gsi, access-patterns]
detect: [dep:@aws-sdk/client-dynamodb, dep:@aws-sdk/lib-dynamodb, dep:dynamodb-toolbox, dep:electrodb]
related: [aws-iam, aws-lambda, localstack, aws-cdk]
---
DynamoDB tables modeled from a written list of access patterns: generic PK/SK keys, GSIs for alternate reads, conditional writes for integrity.

## Verify
- `aws dynamodb describe-table --table-name T --query 'Table.[KeySchema,GlobalSecondaryIndexes[].IndexName,BillingModeSummary]'`: keys, indexes and billing mode match the design.
- `aws dynamodb describe-continuous-backups --table-name T`: point-in-time recovery is on.
- `aws dynamodb describe-time-to-live --table-name T`: TTL attribute is enabled when items expire.
- `aws dynamodb query --table-name T --key-condition-expression 'PK = :p' --expression-attribute-values '{":p":{"S":"USER#1"}}' --endpoint-url http://localhost:4566`: an access pattern answers with one Query against LocalStack.

## Test first
Write one test per access pattern against DynamoDB Local or LocalStack before the table code.
```python
def test_orders_for_user_newest_first(table):
    put(table, pk="USER#1", sk="ORDER#2026-01-02#b")
    put(table, pk="USER#1", sk="ORDER#2026-01-01#a")
    res = table.query(KeyConditionExpression=Key("PK").eq("USER#1") & Key("SK").begins_with("ORDER#"),
                      ScanIndexForward=False)
    assert [i["SK"] for i in res["Items"]] == ["ORDER#2026-01-02#b", "ORDER#2026-01-01#a"]
```

## Do
- List every access pattern first (who reads what, by which key, sorted how). The key design follows from that list, not from the entities.
- Use generic `PK` and `SK` strings with type prefixes (`USER#id`, `ORDER#iso-date#id`). ISO timestamps sort correctly as keys.
- Add a GSI only for a pattern the base keys cannot answer. Use overloaded `GSI1PK` and `GSI1SK` and project only needed attributes.
- Guard writes with `ConditionExpression` (`attribute_not_exists(PK)` for create, a version attribute for update).
- Use `TransactWriteItems` for multi-item invariants, and keep each transaction under its item limit.
- Paginate every Query with `LastEvaluatedKey`. Use `ProjectionExpression` to cut payload.
- Pick on-demand billing until traffic is steady. Enable PITR and deletion protection on prod tables.
- Put an item-type attribute on every item so mixed rows can be told apart.

## Avoid
- `Scan` on request paths: it reads the whole table. Add a key or GSI for the pattern.
- A hot partition key (`STATUS#active`, a date): all traffic hits one partition. Shard with a suffix or choose a high-cardinality key.
- Unbounded item collections or items near the 400 KB item limit: split into child items under the same PK.
- Assuming GSI reads are consistent: they are eventually consistent only. Read the base table when staleness matters.
- Read-modify-write without a condition: concurrent writers lose updates. Use `ADD`, `SET x = x + :n` or a version check.
- Reserved words in expressions (`name`, `status`): use `ExpressionAttributeNames`.
- Wildcard `dynamodb:*` on `*`: scope IAM to the table and index ARNs and only the actions used.

## Review
- [ ] Each access pattern is documented and maps to one Query or GetItem.
- [ ] No Scan in service code outside migrations and tools.
- [ ] Writes that must not overwrite carry a condition.
- [ ] Every Query handles pagination.
- [ ] PITR on, TTL set where needed, IAM limited to table and index ARNs.
