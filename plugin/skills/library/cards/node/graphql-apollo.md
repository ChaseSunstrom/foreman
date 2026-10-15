---
name: graphql-apollo
title: GraphQL with Apollo Server
area: node
tags: [graphql, apollo, schema, resolvers, dataloader, api]
detect: [dep:@apollo/server, dep:graphql, dep:@apollo/client]
related: [node, prisma, typeorm, zod, jest]
---
Apollo Server GraphQL APIs: schema-first types, resolvers, DataLoader batching, depth limits, `executeOperation` tests.

## Verify
- `npx graphql-codegen`: generated resolver and operation types match the schema (when the repo uses codegen).
- `npx tsc --noEmit`: resolvers satisfy generated types.
- `npx jest`: resolver and operation tests via `server.executeOperation`.
- `npm ls graphql`: exactly one `graphql` copy (duplicates cause "Cannot use GraphQLSchema from another module").

## Test first
Execute operations in process against a fake context.
```ts
const server = new ApolloServer({ typeDefs, resolvers });

it('hides email from other users', async () => {
  const res = await server.executeOperation(
    { query: 'query { user(id: "2") { email } }' },
    { contextValue: { user: { id: '1' }, loaders: makeLoaders(fakeDb) } },
  );
  expect(res.body.kind).toBe('single');
  // @ts-expect-error narrowed by kind
  expect(res.body.singleResult.errors?.[0].extensions.code).toBe('FORBIDDEN');
});
```

## Do
- Use `@apollo/server` (v4+) with `expressMiddleware` or `startStandaloneServer`; call `await server.start()` before mounting.
- Build a fresh context per request, including fresh DataLoaders.
- Batch per-field lookups with `DataLoader` to avoid N+1.
- Throw `GraphQLError(msg, { extensions: { code: 'FORBIDDEN' } })` for expected errors.
- Add query depth and complexity limits, and disable introspection in production if the API is not public.
- Authorize in resolvers or a directive per field, not only at the route.
- Make nullability intentional; use input types for mutations and return payload types with errors.

## Avoid
- `apollo-server`, `apollo-server-express`: deprecated and unmaintained. Use `@apollo/server`.
- Creating DataLoaders at module level: the cache leaks between users. Create per request.
- Resolvers that query the DB per list item: N+1. Use a loader.
- Enabling introspection and the landing page in production by accident: set `introspection` explicitly.
- Returning `Error` objects with stack and SQL in messages: use `GraphQLError` and mask internals via `formatError`.
- No depth limit: a recursive query is a cheap DoS. Add `graphql-depth-limit` or cost analysis.
- `expressMiddleware` without `express.json()` and CORS set before it.

## Review
- [ ] Context and loaders are per request.
- [ ] Every sensitive field has an authorization check and a test.
- [ ] Depth/complexity limits and introspection settings are explicit.
- [ ] Error codes are stable; internals are masked.
- [ ] Schema changes are additive or deprecated with `@deprecated`.
