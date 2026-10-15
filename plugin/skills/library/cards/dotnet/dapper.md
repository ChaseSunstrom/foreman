---
name: dapper
title: Dapper
area: dotnet
tags: [dotnet, csharp, sql, orm, database, mapping]
detect: [dep:Dapper, dep:Dapper.Contrib]
related: [ef-core, xunit, nuget]
---
Dapper: thin SQL-to-object mapping over `IDbConnection`, where parameterization, mapping and connection lifetime are all your job.

## Verify
- `dotnet build -warnaserror`: queries and DTOs compile.
- `dotnet test --filter "FullyQualifiedName~Repository"`: repository tests pass against a real database.
- `grep -rnE "(Query|Execute)[A-Za-z]*(Async)?\(\$\"|\+ *[a-z]+ *\+" --include=*.cs .`: finds interpolated or concatenated SQL, which should return nothing.

## Test first
Test against the real engine (Testcontainers or a local SQLite or Postgres), because SQL dialects differ.
```csharp
[Fact]
public async Task Finds_user_by_email_case_insensitively()
{
    await using var conn = await _db.OpenAsync();
    await conn.ExecuteAsync("insert into users(email) values (@e)", new { e = "A@x.io" });

    var repo = new UserRepository(_db);
    var user = await repo.FindByEmail("a@x.io");

    Assert.NotNull(user);
    Assert.Equal("A@x.io", user!.Email);
}
```

## Do
- Always pass parameters: `conn.QueryAsync<User>("select ... where id = @id", new { id })`.
- Use `QuerySingleOrDefaultAsync` when 0 or 1 rows are valid, and `QuerySingleAsync` when exactly one is required. Reserve `QueryFirst*` for ordered queries.
- Create a connection per operation from a factory, and `await using` it. Providers pool the physical connections.
- Wrap multi-statement writes in an explicit `IDbTransaction` and pass it to every call via `transaction:`.
- Select explicit columns, and alias them to property names (`user_name as UserName`) or set `DefaultTypeMap.MatchNamesWithUnderscores = true` once at startup.
- Use `QueryMultipleAsync` for several result sets and `splitOn:` for multi-mapping joins.
- Expand lists with `where id in @ids` and pass an `IEnumerable`, which Dapper expands to parameters.
- Pass `CommandDefinition` with a `CancellationToken` for cancellable calls.

## Avoid
- String-interpolated SQL: it is injection. Use parameters, and whitelist any dynamic column or table name against a fixed set.
- `select *` into DTOs: new columns break mapping silently. List columns.
- A shared singleton connection: it is not thread safe and holds locks. Open per operation.
- `Query` buffering huge results: pass `buffered: false` or page with keyset pagination.
- Forgetting `transaction:` on a call inside a transaction: Dapper throws or runs outside it, depending on the provider.
- `in @ids` with an empty list: the SQL is invalid or matches nothing. Short-circuit before the query.
- Expecting change tracking or migrations: use EF Core or a migration tool for schema.

## Review
- [ ] Every query is parameterized, and dynamic identifiers are whitelisted.
- [ ] Columns are explicit and mapping is covered by a test.
- [ ] Connections and transactions are disposed, and the transaction is passed to each call.
- [ ] Empty-list and null-parameter cases are handled.
- [ ] Repository tests run against the real database engine used in production.
