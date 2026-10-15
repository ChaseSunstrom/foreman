---
name: ef-core
title: Entity Framework Core
area: dotnet
tags: [dotnet, csharp, orm, database, migrations, linq]
detect: [dep:Microsoft.EntityFrameworkCore, dep:Microsoft.EntityFrameworkCore.Design, dep:Microsoft.EntityFrameworkCore.SqlServer, dep:Npgsql.EntityFrameworkCore.PostgreSQL, dep:Microsoft.EntityFrameworkCore.Sqlite]
related: [aspnet-core, minimal-apis, xunit, dotnet-cli]
---
EF Core: DbContext, entity configuration, migrations, LINQ queries, tracking and concurrency.

## Verify
- `dotnet ef migrations has-pending-model-changes`: model and migrations agree (needs dotnet-ef tool).
- `dotnet ef migrations script --idempotent -o /dev/null`: migrations generate valid SQL.
- `dotnet build -warnaserror`: compiles clean.
- `dotnet test`: tests, ideally against the real provider.

## Test first
Test queries against the real database engine (Testcontainers) or SQLite; the InMemory provider ignores constraints, relational behavior and SQL translation.
```csharp
[Fact]
public async Task Duplicate_email_violates_unique_index()
{
    await using var db = fixture.NewContext();
    db.Users.Add(new User { Email = "a@x.io" });
    db.Users.Add(new User { Email = "a@x.io" });
    await Assert.ThrowsAsync<DbUpdateException>(() => db.SaveChangesAsync());
}
```

## Do
- Configure in `IEntityTypeConfiguration<T>` classes loaded by `ApplyConfigurationsFromAssembly`; add unique indexes, max lengths and required flags there.
- Use `AsNoTracking()` for read-only queries, and project with `Select` into DTOs.
- Register with `AddDbContext` (scoped) and pass `CancellationToken` to every `...Async` call.
- Use `Include` or `AsSplitQuery()` deliberately for related data; prefer projection.
- Add a concurrency token (`IsRowVersion()` or `[Timestamp]`) on rows edited concurrently and handle `DbUpdateConcurrencyException`.
- Use `ExecuteUpdateAsync` / `ExecuteDeleteAsync` for set-based changes.
- Review the generated migration before committing; name migrations by intent.

## Avoid
- Querying inside a loop (N+1): one query with `Include` or a projection.
- Calling `ToList()` then filtering in memory: the filter must stay in the IQueryable so it runs in SQL.
- A singleton `DbContext`: not thread-safe. Use scoped, or `IDbContextFactory<T>` in Blazor Server and background services.
- `FromSqlRaw` with string interpolation: SQL injection. Use `FromSql` or `FromSqlInterpolated`, which parameterize.
- Editing an applied migration: breaks other databases. Add a new migration.
- Using the InMemory provider to prove query behavior: false greens. Use the real engine.
- `EnsureCreated()` alongside migrations: bypasses the history table. Use `Migrate()` or a deploy-time script.

## Review
- [ ] Every new entity change has a migration, reviewed for data loss (drops, renames as drop+add).
- [ ] Read queries use `AsNoTracking` or projection.
- [ ] No N+1 and no client-side evaluation of large sets.
- [ ] Raw SQL is parameterized.
- [ ] Constraints (unique, FK, required) are in the model, not only in code.
