---
name: mongoose
title: Mongoose
area: node
tags: [mongoose, mongodb, odm, schema, nosql, node]
detect: [dep:mongoose, dep:mongodb-memory-server]
related: [node, express, nestjs, jest, zod]
---
Mongoose ODM for MongoDB: schemas and validation, indexes, lean queries, population, transactions.

## Verify
- `npx tsc --noEmit`: schema and document typings (TypeScript projects).
- `npm test`: the suite against `mongodb-memory-server` or a disposable database.
- `node -e "require('./src/models/user').User.syncIndexes().then(()=>process.exit(0))"`: declared indexes build against a scratch database (set the URI first).

## Test first
Use `mongodb-memory-server` so unique indexes and validators really run.
```js
const { MongoMemoryServer } = require('mongodb-memory-server');
const mongoose = require('mongoose');
const { User } = require('../src/models/user');

let mongod;
beforeAll(async () => { mongod = await MongoMemoryServer.create(); await mongoose.connect(mongod.getUri()); await User.init(); });
afterAll(async () => { await mongoose.disconnect(); await mongod.stop(); });

test('duplicate email is rejected', async () => {
  await User.create({ email: 'a@x.io' });
  await expect(User.create({ email: 'a@x.io' })).rejects.toMatchObject({ code: 11000 });
});
```
Await `Model.init()` so the unique index exists before asserting.

## Do
- Connect once with `mongoose.connect(uri)` at startup and handle the returned promise.
- Define validation in the schema: `required`, `enum`, `min`/`max`, `match`, custom `validate`.
- Declare indexes in the schema (`schema.index`, `unique: true`) and build them deliberately in production.
- Use `.lean()` for read-only queries to skip document hydration; use `.select()` for needed fields.
- Query with explicit filters and cast request values to primitives before `find`.
- Use `session.withTransaction` for multi-document writes (needs a replica set).
- Set `timestamps: true` and `toJSON` transforms that drop `__v` and secrets.
- Use `populate` with a field list and keep it to one level on hot paths.

## Avoid
- `Model.find(req.body)` or `find({ email: req.body.email })` with an unvalidated object: NoSQL operator injection (`{ "$ne": null }`). Validate to strings first; consider `sanitizeFilter: true`.
- Relying on `unique: true` as a validator: it is an index, so it fails with a duplicate-key error (`11000`) at write time. Handle that code.
- Using `autoIndex: true` blindly in large production collections: index builds hurt startup. Manage indexes via migrations.
- `findOneAndUpdate` without `{ new: true, runValidators: true }`: returns the old doc and skips validators.
- Callbacks and `useNewUrlParser`-era options from old tutorials: current Mongoose uses promises and ignores those options.
- Mutating an object returned by `.lean()` and calling `.save()`: it is a plain object. Query without lean to modify.
- `strictQuery` assumptions: the default differs across majors; set it explicitly.

## Review
- [ ] Inputs are validated or cast before reaching filters.
- [ ] Unique and query indexes exist and duplicate-key errors are handled.
- [ ] Read paths use `lean`/`select`.
- [ ] Updates use `runValidators` and `new` deliberately.
- [ ] Transactions only against a replica set.
