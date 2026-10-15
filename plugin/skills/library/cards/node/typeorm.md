---
name: typeorm
title: TypeORM
area: node
tags: [typeorm, orm, database, migrations, entities, typescript]
detect: [dep:typeorm, dep:@nestjs/typeorm]
related: [nestjs, node, jest, sequelize]
---
TypeORM: decorator entities, `DataSource`, migrations, repositories and transactions, relation loading.

## Verify
- `npx typeorm-ts-node-commonjs migration:generate src/migrations/Change -d src/data-source.ts`: prints "No changes" when entities and migrations agree.
- `npx typeorm-ts-node-commonjs migration:show -d src/data-source.ts`: lists applied and pending migrations.
- `npx tsc --noEmit`: entity and repository types.
- `npx jest`: the suite against a disposable database.

## Test first
Initialize a real `DataSource` (SQLite in-memory or a test Postgres) and run migrations.
```ts
import { DataSource } from 'typeorm';
import { User } from '../src/user.entity';

let ds: DataSource;
beforeAll(async () => {
  ds = await new DataSource({ type: 'better-sqlite3', database: ':memory:', entities: [User], synchronize: true }).initialize();
});
afterAll(() => ds.destroy());

it('enforces unique email', async () => {
  const repo = ds.getRepository(User);
  await repo.save({ email: 'a@x.io' });
  await expect(repo.save({ email: 'a@x.io' })).rejects.toThrow(/UNIQUE/);
});
```
`synchronize: true` is for tests only.

## Do
- Export one `DataSource` and call `initialize()` once at startup.
- Set `synchronize: false` outside tests and use migrations (`migrationsRun` or the CLI).
- Declare `@Index`, `@Unique` and relation `onDelete` on entities.
- Use `repo.find({ select, relations })` or QueryBuilder with joins to control loading.
- Wrap multi-step writes in `dataSource.transaction(async (manager) => ...)` and use `manager`, not the global repo, inside.
- Use QueryBuilder parameters (`where('u.id = :id', { id })`).
- Use explicit column types for Postgres (`type: 'timestamptz'`, `'uuid'`).
- Paginate with `take`/`skip` plus a deterministic `order`.

## Avoid
- `synchronize: true` in production: can drop columns and data on boot. Generate migrations.
- Using the global repository inside a transaction callback: it runs outside the transaction. Use `manager`.
- String-concatenated `where` clauses: SQL injection. Use named parameters.
- Eager relations on large graphs, or lazy relations by accident: unexpected queries. Load relations explicitly.
- `save` with a partial object to "update": it may insert or overwrite. Use `update` or load, modify, save.
- `skip`/`take` with joins on one-to-many in QueryBuilder: row counts mislead. Use `getManyAndCount` carefully or paginate by ids.
- Editing a shipped migration: add a new one.

## Review
- [ ] `synchronize` is false outside tests; migrations exist for every entity change.
- [ ] Transactions use the supplied `manager`.
- [ ] No string-built SQL.
- [ ] Relations are loaded deliberately; no N+1 loops.
- [ ] Indexes exist for filtered and joined columns.
