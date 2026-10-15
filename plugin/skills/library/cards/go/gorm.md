---
name: gorm
title: GORM
area: go
tags: [go, orm, gorm, database, sql, migrations]
detect: [dep:gorm.io/gorm, dep:gorm.io/driver/postgres, dep:gorm.io/driver/mysql, dep:gorm.io/driver/sqlite]
related: [go-testing, go-modules, gin, echo, sqlc]
---
GORM: models and associations, query building, transactions and migrations, with its silent failure modes handled.

## Verify
- `go vet ./... && go build ./...`: static checks and build.
- `go test ./... -race -count=1`: tests against a real or in-memory database.
- `go list -m gorm.io/gorm`: pinned version, matching the driver module versions.
- `go test -run TestMigrate ./...`: a test that runs migrations on an empty database and checks the schema.

## Test first
Use the same dialect as production where possible. SQLite in memory is fine for logic, not for dialect features.
```go
func TestCreateUserDuplicateEmail(t *testing.T) {
	db := openTestDB(t) // gorm.Open(sqlite.Open("file::memory:"), ...) + migrations
	if err := db.Create(&User{Email: "a@b.c"}).Error; err != nil {
		t.Fatal(err)
	}
	err := db.Create(&User{Email: "a@b.c"}).Error
	if !errors.Is(err, gorm.ErrDuplicatedKey) {
		t.Fatalf("got %v", err)
	}
}
```
`ErrDuplicatedKey` needs `TranslateError: true` in `gorm.Config`.

## Do
- Always read `.Error` (or `result.Error`) after every call, and check `RowsAffected` for updates and deletes.
- Pass the request context: `db.WithContext(ctx)`.
- Use `db.Transaction(func(tx *gorm.DB) error {...})` and use only `tx` inside.
- Use `Preload` or `Joins` to avoid N+1 queries, and `Select` to limit columns.
- Use `Where("email = ?", v)` with placeholders, or struct and map conditions.
- Use `First` to expect a row (`ErrRecordNotFound`) and `Find` for lists.
- Prefer versioned SQL migrations (goose, atlas, golang-migrate) in production, and `AutoMigrate` for tests and prototypes.
- Set pool limits via `sqlDB, _ := db.DB()` then `SetMaxOpenConns` and `SetConnMaxLifetime`.

## Avoid
- Ignoring `.Error`: failures are silent. Check every chain's result.
- Struct conditions with zero values (`Where(&User{Active: false})`): zero fields are skipped. Use a map or explicit `Where`.
- `Updates(struct)` to set a field to zero: zero values are skipped. Use `Select("active").Updates(...)`, a map, or `Save`.
- `db.Where(...)` reused as a base across queries: chains mutate shared state unless you call `Session(&gorm.Session{})`. Start each from a fresh `db`.
- `Update` or `Delete` with no conditions: GORM returns `ErrMissingWhereClause`. Never bypass it with `AllowGlobalUpdate` casually.
- String-concatenated `Where`, `Order` or `Raw` with user input: injection. Bind parameters and whitelist sort columns.
- `AutoMigrate` against production as the migration system: it never drops or renames. Use versioned migrations.
- Soft delete surprises: `gorm.DeletedAt` hides rows from queries. Use `Unscoped()` when you mean it.

## Review
- [ ] Every query's error is checked and not-found is mapped deliberately.
- [ ] Multi-step writes run in one transaction using `tx`.
- [ ] No N+1 patterns, and list endpoints are paginated.
- [ ] Zero-value updates use maps or `Select`.
- [ ] User input never reaches SQL strings unbound.
