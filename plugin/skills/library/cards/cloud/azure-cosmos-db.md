---
name: azure-cosmos-db
title: Azure Cosmos DB
area: cloud
tags: [azure, cosmos-db, nosql, partition-key, ru, emulator]
detect: [dep:@azure/cosmos, dep:azure-cosmos, dep:Microsoft.Azure.Cosmos]
related: [azure-entra-id, azure-key-vault, azure-functions, aws-dynamodb-single-table]
---
Cosmos DB for NoSQL: a high-cardinality partition key chosen from the query list, point reads, RU budgeting, Entra auth instead of keys, handled 429s.

## Verify
- `az cosmosdb sql container show -g RG -a ACCOUNT -d DB -n C --query '{pk:resource.partitionKey,idx:resource.indexingPolicy,ttl:resource.defaultTtl}'`: partition key, indexing policy and TTL.
- `az cosmosdb show -g RG -n ACCOUNT --query '{keys:disableLocalAuth,ha:enableAutomaticFailover,zones:locations[].isZoneRedundant}'`: key auth disabled, failover and zone redundancy.
- `az cosmosdb sql container throughput show -g RG -a ACCOUNT -d DB -n C`: provisioned or autoscale RU.
- `az cosmosdb sql role assignment list -g RG -a ACCOUNT`: data-plane roles granted to identities.

## Test first
Run against the Cosmos DB emulator and test the hot queries for single-partition cost.
```python
def test_orders_by_customer_is_single_partition(container):
    items = list(container.query_items(
        "SELECT * FROM c WHERE c.customerId = @id",
        parameters=[{"name": "@id", "value": "c1"}], partition_key="c1"))
    assert all(i["customerId"] == "c1" for i in items)
```

## Do
- Pick the partition key from the most common query filter and write volume. It needs many distinct values, even spread, and sits in every hot query. Consider a hierarchical or synthetic key.
- Use point reads (`read_item` by id and partition key) wherever possible: far cheaper than queries.
- Always pass the partition key on queries so they do not fan out across partitions.
- Use Entra ID with data-plane RBAC (`disableLocalAuth: true`) instead of account keys.
- Tune the indexing policy: exclude paths you never filter on, add composite indexes for `ORDER BY` on multiple properties.
- Use autoscale throughput for variable load and read the RU charge from response headers while developing.
- Retry on 429 using the retry-after value (the SDK does this by default, so keep that on) and use bulk mode for batch loads.
- Use the change feed for downstream projections, and set TTL for expiring data.
- Use a singleton client per process and the nearest preferred regions.

## Avoid
- A low-cardinality or monotonic key (`status`, date): hot partition and the 20 GB logical partition cap. Choose a better key or a synthetic one.
- Cross-partition queries on hot paths: RU cost and latency scale with partitions. Add the key to the filter.
- Account keys in app config: they are all-powerful and never expire. Use managed identity and RBAC.
- A new `CosmosClient` per request: socket exhaustion and slow starts. Reuse one.
- `SELECT *` with large documents: project needed fields.
- Treating the emulator's behavior as production's: validate RU and consistency on a real account.
- Storing unbounded growing arrays inside a document: documents cap at 2 MB. Use child items.

## Review
- [ ] Partition key justified against the query list and write distribution.
- [ ] Hot reads are point reads or single-partition queries.
- [ ] Local key auth disabled and RBAC used.
- [ ] Indexing policy reviewed, TTL where needed.
- [ ] Client is a singleton with 429 handling.
