---
name: mongodb
title: MongoDB
area: data
tags: [nosql, mongodb, documents, indexes, aggregation, schema]
detect: [dep:pymongo, dep:motor, dep:mongoose, dep:mongodb, dep:mongo-driver, dep:mongoengine, dep:beanie, dep:Mongo2Go, dep:MongoDB.Driver]
related: [query-tuning, n-plus-one, redis]
---
MongoDB: schema designed around access patterns, validated documents, compound indexes proven by explain.

## Verify
- `mongosh "$MONGO_URL" --eval 'db.coll.find({k:1}).explain("executionStats")'`: IXSCAN not COLLSCAN, and docsExamined near nReturned.
- `mongosh "$MONGO_URL" --eval 'db.coll.getIndexes()'`: indexes that exist, including unique and TTL.
- `mongosh "$MONGO_URL" --eval 'db.getCollectionInfos({name:"coll"})'`: the `$jsonSchema` validator is attached.
- `mongosh "$MONGO_URL" --eval 'db.coll.aggregate([...]).explain("executionStats")'`: pipeline uses an index in the first `$match`.

## Test first
Use a real mongod (container or an in-memory server), a fresh database per test.
```python
async def test_unique_email(db):
    await db.users.create_index("email", unique=True)
    await db.users.insert_one({"email": "a@x.io"})
    with pytest.raises(DuplicateKeyError):
        await db.users.insert_one({"email": "a@x.io"})
```

## Do
- Embed data read together and bounded in size; reference data that grows without bound or changes independently.
- Add a `$jsonSchema` validator with `validationLevel` and `validationAction` set deliberately.
- Create indexes following equality, sort, range order (ESR); drop unused ones.
- Put `$match` and `$sort` first in aggregation so indexes apply; use `$project` early.
- Use `updateOne` with operators (`$set`, `$inc`, `$push`) and `upsert` with a unique key.
- Use multi-document transactions only when needed; they need a replica set.
- Set `writeConcern: majority` and read concern for data you cannot lose; add a TTL index for expiring data.

## Avoid
- Unbounded arrays in a document: hits the 16 MB limit and slows updates. Use a child collection.
- Building filters from request JSON (`{"$ne": null}` injection): coerce to strings or validate with a schema.
- `$where` and JavaScript execution: slow and injectable. Use query operators.
- `skip()` for deep pagination: scans skipped docs. Range on an indexed field.
- Replacing a whole document with `replaceOne` for a small change: loses concurrent updates. Use update operators.
- Indexes created on a large live collection without planning: build impact. Schedule and monitor.
- Assuming field order or schema: add validation and handle missing fields.

## Review
- [ ] Each query has a supporting index shown by explain.
- [ ] User input is never passed as a raw operator document.
- [ ] No unbounded arrays; document size is bounded.
- [ ] Write and read concerns are set where durability matters.
- [ ] Schema validator or model layer enforces required fields.
