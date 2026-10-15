---
name: graphql-security
title: GraphQL security
area: security
tags: [security, graphql, api, authorization, dos, introspection]
detect: [dep:graphql, dep:graphql-depth-limit, dep:strawberry-graphql, dep:graphene]
related: [idor, authorization, rate-limiting, api-security, input-validation]
---
GraphQL APIs: authorize in resolvers, limit depth and cost, batch-safe rate limits, introspection and suggestions off in prod.

## Verify
- `pytest -q -k graphql_security`: depth, cost and authorization tests pass.
- `curl -s localhost:4000/graphql -H 'content-type: application/json' -d '{"query":"{__schema{types{name}}}"}'`: introspection is refused in the production profile.
- `git grep -nE "introspection|depthLimit|costAnalysis|max_depth|validationRules" -- ':!*test*'`: limits are configured.

## Test first
An over-deep query must fail, and a field must enforce ownership.
```python
def test_deep_query_rejected(gql):
    q = "{ me { friends { friends { friends { friends { friends { id }}}}}}}"
    r = gql(q)
    assert "errors" in r and "depth" in r["errors"][0]["message"].lower()

def test_other_users_order_is_not_returned(gql, alice, bob_order):
    r = gql("query($id:ID!){order(id:$id){total}}", {"id": bob_order.id}, as_user=alice)
    assert r["data"]["order"] is None
```

## Do
- Authenticate in context, then authorize in every resolver or with a field-level directive or plugin. Authorize each object, not just each root field.
- Set max query depth and a complexity or cost budget. Cap page sizes and require pagination arguments.
- Limit total operations: restrict batched arrays and aliases, and rate limit by cost rather than request count.
- Use persisted or allow-listed queries for first-party clients in production.
- Disable introspection and field suggestions in production unless a public API needs them.
- Validate arguments with typed inputs and custom scalars. Use parameterised queries in resolvers.
- Return generic errors in production and hide stack traces.
- Add per-request DataLoaders keyed by the viewer so batches do not cross tenants.

## Avoid
- Authorizing only at the gateway or root `Query`: nested fields reach other users' data. Check at each resolver.
- Unlimited depth and aliases: one request fans out into thousands of lookups. Add limits and cost.
- Brute-force protection per HTTP request: one request can hold 1000 login mutations through aliases. Limit per operation.
- GraphQL over GET with no CSRF thought: require JSON content type and non-simple headers.
- A DataLoader cache shared across users: scope it to the request.
- Leaving introspection and GraphiQL on in production: gate them by environment.

## Review
- [ ] Authorization lives in resolvers or field policies and is tested with two users.
- [ ] Depth, complexity, alias and batch limits are set.
- [ ] Introspection, suggestions and the IDE are off in prod.
- [ ] Mutations validate input and have rate limits.
- [ ] Errors leak no internals.
