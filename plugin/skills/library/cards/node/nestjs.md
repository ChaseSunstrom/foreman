---
name: nestjs
title: NestJS
area: node
tags: [nestjs, node, typescript, dependency-injection, api, decorators]
detect: [dep:@nestjs/core, dep:@nestjs/common, file:nest-cli.json]
related: [typeorm, prisma, jest, zod, fastify, express]
---
NestJS apps: modules, providers and DI, DTO validation pipes, guards, e2e tests with `Test.createTestingModule`.

## Verify
- `npx tsc --noEmit -p tsconfig.build.json`: types.
- `npx nest build`: the app compiles.
- `npx jest`: unit specs (`*.spec.ts` beside the code).
- `npx jest --config ./test/jest-e2e.json`: e2e specs against the real module graph.
- `npx eslint "{src,test}/**/*.ts"`: lint.

## Test first
Build a testing module, override providers, hit the app with supertest.
```ts
import { Test } from '@nestjs/testing';
import { ValidationPipe } from '@nestjs/common';
import * as request from 'supertest';
import { AppModule } from '../src/app.module';

it('POST /users rejects bad email', async () => {
  const mod = await Test.createTestingModule({ imports: [AppModule] }).compile();
  const app = mod.createNestApplication();
  app.useGlobalPipes(new ValidationPipe({ whitelist: true }));
  await app.init();
  await request(app.getHttpServer()).post('/users').send({ email: 'x' }).expect(400);
  await app.close();
});
```

## Do
- One module per feature; export only the providers other modules need.
- Use constructor injection with `@Injectable()`; depend on abstractions via custom tokens (`{ provide, useClass }`) for things you will fake.
- Validate input with DTO classes (`class-validator`) and a global `ValidationPipe({ whitelist: true, transform: true })`.
- Use `ConfigModule.forRoot({ validate })` and inject `ConfigService`; do not read `process.env` in providers.
- Put auth in guards, shaping in interceptors, error mapping in exception filters.
- Use `app.enableShutdownHooks()` so `OnModuleDestroy` runs.
- Test units with `Test.createTestingModule` and `useValue` mocks.

## Avoid
- Circular module or provider imports: `forwardRef` hides a design problem. Extract a third module.
- `ValidationPipe` without `whitelist`: extra fields reach your service (mass assignment). Enable `whitelist` and `forbidNonWhitelisted` where fitting.
- Plain interfaces as DTOs: they vanish at runtime, so nothing validates. Use classes with decorators.
- Injecting by concrete class in services you mock in tests: use a token.
- Request-scoped providers everywhere: they re-instantiate per request and bubble up scope. Use only when required.
- `synchronize: true` in TypeORM config for production: it alters the schema at boot. Use migrations.
- Business logic in controllers: keep controllers thin, logic in providers.

## Review
- [ ] Global pipe validates with whitelist; DTOs are classes.
- [ ] Guards protect every non-public route (default-deny or explicit).
- [ ] Modules export the minimum; no `forwardRef` cycles.
- [ ] Config is validated at boot.
- [ ] e2e test covers auth failure and validation failure.
