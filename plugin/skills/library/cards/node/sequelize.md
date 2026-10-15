---
name: sequelize
title: Sequelize
area: node
tags: [sequelize, orm, database, migrations, models, sql]
detect: [dep:sequelize, dep:sequelize-cli, dep:sequelize-typescript, file:.sequelizerc]
related: [node, express, jest, typeorm]
---
Sequelize ORM: models, migrations through `sequelize-cli`, associations, transactions, eager loading.

## Verify
- `npx sequelize-cli db:migrate:status`: which migrations are applied.
- `npx sequelize-cli db:migrate && npx sequelize-cli db:migrate:undo`: the latest migration applies and reverses cleanly on a scratch database.
- `npx tsc --noEmit`: model typings (TypeScript projects).
- `npm test`: the suite against a disposable database.

## Test first
Run migrations on a test database and assert constraints in the real DB.
```js
const { sequelize, User } = require('../src/models');

beforeAll(() => sequelize.sync({ force: true })); // tests only
afterAll(() => sequelize.close());

test('email is unique', async () => {
  await User.create({ email: 'a@x.io' });
  await expect(User.create({ email: 'a@x.io' }))
    .rejects.toThrow(/SequelizeUniqueConstraintError|unique/i);
});
```

## Do
- Write schema changes as migrations (`sequelize-cli migration:generate`) with both `up` and `down`.
- Put constraints in the DB: `unique`, `allowNull: false`, foreign keys with `onDelete`; mirror them in the model.
- Define associations (`hasMany`, `belongsTo`) in one place after all models load.
- Use `include` with `attributes` to fetch needed columns; prefer `findAll({ where: { id: ids } })` to loops.
- Wrap multi-step writes in `sequelize.transaction(async (t) => ...)` and pass `{ transaction: t }` to every call.
- Use `replacements` or `bind` for raw queries.
- Pick the pool size (`pool: { max, idle }`) to fit the DB's connection limit.
- Use `paranoid: true` only when soft delete is a requirement, and know it changes every query.

## Avoid
- `sequelize.sync()` or `sync({ alter: true })` in production: drifts or loses data. Use migrations; `sync({ force: true })` drops tables.
- Forgetting `{ transaction: t }` on a call inside a transaction block: it runs outside it. Pass it on every call, or use CLS.
- `sequelize.query` with template strings and user input: injection. Use `replacements`.
- `where: { field: req.query.x }` passing a user object: operator injection (`{ [Op.ne]: ... }` style via parsed JSON). Coerce to string or validate first.
- Editing a shipped migration: add a new one.
- `findAll` with `include` of hasMany plus `limit`: wrong counts and slow subqueries. Use `separate: true` or two queries.
- `Model.update` without `where`: it errors in v6+, but `destroy({ truncate: true })` wipes the table; avoid it outside tests.

## Review
- [ ] Each model change has a reversible migration.
- [ ] Transactions pass `transaction` everywhere.
- [ ] No raw SQL built from user strings; request values are validated before reaching `where`.
- [ ] Pool size fits the database.
- [ ] No `sync` calls outside tests.
