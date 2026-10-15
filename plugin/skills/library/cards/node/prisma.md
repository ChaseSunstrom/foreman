---
name: prisma
title: Prisma
area: node
tags: [prisma, orm, database, migrations, typescript, sql]
detect: [dep:prisma, dep:@prisma/client, file:schema.prisma]
related: [node, nestjs, trpc, zod, vitest]
---
Prisma ORM: schema in `schema.prisma`, generated client, migrations, transactions, query shape and N+1 control.

## Verify
- `npx prisma validate`: the schema parses and relations are consistent.
- `npx prisma format`: canonical formatting of the schema.
- `npx prisma generate`: the client matches the schema (rerun after every schema change).
- `npx prisma migrate diff --from-migrations prisma/migrations --to-schema-datamodel prisma/schema.prisma --exit-code`: committed migrations equal the schema (needs a shadow database URL configured).
- `npx prisma migrate status`: applied migrations match the folder.

## Test first
Test against a real throwaway database; reset it between tests.
```ts
import { PrismaClient } from '@prisma/client';
import { createUser } from '../src/users';
const prisma = new PrismaClient();

beforeEach(() => prisma.user.deleteMany());

it('rejects a duplicate email', async () => {
  await createUser(prisma, { email: 'a@x.io' });
  await expect(createUser(prisma, { email: 'a@x.io' })).rejects.toMatchObject({ code: 'P2002' });
});
```
Run `npx prisma migrate deploy` against the test DB first.

## Do
- Create one `PrismaClient` per process and reuse it; in dev with hot reload stash it on `globalThis`.
- Use `migrate dev` locally to create migrations, `migrate deploy` in CI and production.
- Add `@unique`, `@@index` and `onDelete` rules in the schema; the DB enforces them.
- Select only needed fields (`select`) and load relations deliberately (`include`) to avoid N+1.
- Group dependent writes in `prisma.$transaction([...])` or an interactive `$transaction(async tx => ...)`.
- Catch `PrismaClientKnownRequestError` and switch on `code` (`P2002` unique, `P2025` not found).
- Use `$queryRaw` with tagged template for raw SQL.
- Paginate with `cursor` and `take`, with a stable `orderBy`.

## Avoid
- `new PrismaClient()` per request or per module: exhausts connections. Share one.
- `prisma migrate dev` or `db push` against production: can reset or drift. Use `migrate deploy`.
- `$queryRawUnsafe` or `$executeRawUnsafe` with user input: SQL injection. Use the tagged `$queryRaw`.
- Editing an applied migration file: checksums fail elsewhere. Add a new migration.
- Forgetting `prisma generate` in CI and Docker builds: stale or missing client types.
- `findMany` in a loop over ids: N+1. Use `where: { id: { in: ids } }` or `include`.
- Returning full rows (password hashes) from `findUnique`: use `select` or `omit`.

## Review
- [ ] Every schema change has a committed migration.
- [ ] Single shared client; connection limits fit the deployment.
- [ ] Multi-step writes are in a transaction.
- [ ] No raw SQL built from strings.
- [ ] Queries select only required fields.
