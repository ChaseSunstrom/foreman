---
name: drizzle
title: Drizzle ORM
area: node
tags: [drizzle, orm, sql, migrations, typescript, database]
detect: [dep:drizzle-orm, dep:drizzle-kit, file:drizzle.config.ts]
related: [node, zod, vitest, prisma, hono]
---
Drizzle ORM: TypeScript table definitions, SQL-like query builder, `drizzle-kit` migrations, typed inserts and selects.

## Verify
- `npx drizzle-kit generate`: produces SQL migrations from schema changes; a clean tree afterwards means nothing is un-migrated.
- `npx drizzle-kit check`: migration history is consistent.
- `npx tsc --noEmit`: queries and inserts type-check against the schema.
- `npx vitest run`: the suite against a real or in-memory database.

## Test first
Use a real driver with a disposable DB (PGlite, SQLite in-memory, or a test container) and apply migrations.
```ts
import { migrate } from 'drizzle-orm/better-sqlite3/migrator';
import Database from 'better-sqlite3';
import { drizzle } from 'drizzle-orm/better-sqlite3';
import { addUser } from '../src/users';

it('addUser enforces unique email', () => {
  const db = drizzle(new Database(':memory:'));
  migrate(db, { migrationsFolder: './drizzle' });
  addUser(db, 'a@x.io');
  expect(() => addUser(db, 'a@x.io')).toThrow(/UNIQUE/);
});
```

## Do
- Define tables with the dialect's builder (`pgTable`, `sqliteTable`, `mysqlTable`) in a schema module; infer types with `$inferSelect` and `$inferInsert`.
- Configure `drizzle.config.ts` with `schema`, `out`, `dialect`, `dbCredentials`.
- Use `generate` then `migrate` for reviewed, versioned SQL; commit the `out` folder.
- Express joins and filters with `eq`, `and`, `or`, `inArray` and `sql` templates.
- Use `db.transaction(async (tx) => ...)` and pass `tx` to helper functions.
- Use the relational query API (`db.query.users.findMany({ with: ... })`) when you need nested reads, passing `schema` to `drizzle()`.
- Add `.returning()` to get inserted or updated rows on dialects that support it.
- Add indexes and uniques in the table's extra-config callback.

## Avoid
- `drizzle-kit push` against production: applies schema diffs without a reviewed migration. Use it only for local prototyping.
- Interpolating values into `sql` with `sql.raw(userInput)`: injection. Use `${value}` params in the template.
- `update`/`delete` with no `.where(...)`: touches every row. Always filter.
- Old `drizzle-kit` config keys (`driver`, `dbCredentials.connectionString`) from outdated examples: use `dialect` and the current credentials shape.
- Forgetting to pass `{ schema }` and then using `db.query.*`: it is undefined.
- Editing a generated migration after it shipped: add a new one.

## Review
- [ ] Every schema change has a committed migration in `out`.
- [ ] No `update` or `delete` without `where`.
- [ ] Multi-statement writes use a transaction.
- [ ] Raw SQL uses parameter templates only.
- [ ] Types come from `$inferSelect`/`$inferInsert`, not hand copies.
