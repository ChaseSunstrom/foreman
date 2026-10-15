---
name: graphql-schema
title: GraphQL schema design
area: design
tags: [graphql, schema, api, n-plus-one, dataloader, pagination]
detect: [file:*.graphql, file:*.gql, file:schema.graphqls, dep:graphql, dep:@apollo/server, dep:graphene, dep:strawberry-graphql, dep:gqlgen]
related: [pagination, error-handling, api-versioning, caching]
---
GraphQL schemas designed as a stable, nullable-by-intent contract with batched resolvers and bounded queries.

## Verify
- `npx graphql-inspector diff schema.old.graphql schema.graphql`: lists breaking and dangerous changes against the old schema.
- `npx graphql-inspector validate 'src/**/*.graphql' schema.graphql`: documents validate against the schema.
- `npx graphql-schema-linter schema.graphql`: naming and description rules, when configured.
- `curl -s localhost:4000/graphql -H 'content-type: application/json' -d '{"query":"{__typename}"}'`: the endpoint answers.

## Test first
Execute queries against the schema in process and count backend calls.
```js
test("orders resolve customers in one batch", async () => {
  const calls = jest.fn(async (ids) => ids.map((id) => ({ id })));
  const res = await server.executeOperation(
    { query: "{ orders(first: 20) { edges { node { customer { id } } } } }" },
    { contextValue: { loaders: makeLoaders({ customersByIds: calls }) } });
  expect(res.body.singleResult.errors).toBeUndefined();
  expect(calls).toHaveBeenCalledTimes(1);
});
```

## Do
- Make fields nullable unless a null is impossible and the failure of a parent resolver should null the parent. Use `!` deliberately.
- Use mutation payload types (`CreateOrderPayload { order, userErrors }`) and one input object per mutation.
- Paginate lists with Relay-style connections (`first`, `after`, `pageInfo`, `edges.cursor`), with opaque cursors.
- Batch per-request with DataLoader (or the stack's equivalent), created fresh per request.
- Use enums and custom scalars (`DateTime`, `ID`) for domain values instead of free strings.
- Deprecate with `@deprecated(reason: "...")`, never remove directly. Track usage first.
- Enforce depth limits, complexity or cost limits, and request size limits at the server.

## Avoid
- A shared DataLoader across requests: it caches stale data across users and leaks data. Build loaders in context per request.
- Resolvers that query once per parent (N+1): batch by key.
- Leaving introspection and GraphiQL on for production when the API isn't public: disable or gate them.
- Throwing for expected business failures: return them in `userErrors` and keep `errors` for bugs and auth.
- Offset pagination on large or changing lists: use cursors.
- Unbounded query depth with recursive types (`user { friends { friends ... } }`): add a depth or cost limit.
- Authorization only on root fields: check it inside field resolvers or a shared layer.

## Review
- [ ] Schema diff shows no breaking changes, or they are intended and announced.
- [ ] Every list field is paginated and bounded by a maximum page size.
- [ ] Per-parent lookups use loaders, and a test proves the batch count.
- [ ] Mutations take one input and return payloads with typed errors.
- [ ] Depth and cost limits are on, and field-level auth is covered by a test.
