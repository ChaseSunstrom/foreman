---
name: trpc
title: tRPC
area: node
tags: [trpc, typescript, rpc, api, zod, end-to-end-types]
detect: [dep:@trpc/server, dep:@trpc/client, dep:@trpc/react-query]
related: [zod, prisma, drizzle, vitest, hono]
---
tRPC routers: end-to-end typed procedures, zod input, context and middleware, `createCaller` tests.

## Verify
- `npx tsc --noEmit`: client and server types agree (the point of tRPC).
- `npx vitest run`: router tests via `createCaller`, no HTTP.
- `npm ls @trpc/server @trpc/client`: server and client on the same major.
- `npx eslint .`: lint.

## Test first
Call procedures directly through a caller with a fake context.
```ts
import { it, expect } from 'vitest';
import { appRouter } from '../src/router';

it('rejects anonymous users', async () => {
  const caller = appRouter.createCaller({ user: null, db: {} as any });
  await expect(caller.post.create({ title: 'x' })).rejects.toMatchObject({
    code: 'UNAUTHORIZED',
  });
});
```
In v11 `createCallerFactory(router)` may be required instead; match the installed version.

## Do
- Initialize once: `const t = initTRPC.context<Context>().create()`; export `router`, `publicProcedure` and `protectedProcedure`.
- Put auth in a middleware that narrows context (`ctx.user` non-null) and build `protectedProcedure` from it.
- Validate every input with `.input(zodSchema)`; shape output with `.output(...)` where leaking fields is a risk.
- Throw `TRPCError({ code: 'NOT_FOUND' | 'FORBIDDEN' | ... })`, not bare `Error`.
- Build context per request in `createContext`; keep DB clients created once outside.
- Export `type AppRouter` only; import it as a type in the client (`import type`).
- Use `useUtils` (v11) or `useContext`/`utils` (v10) to invalidate queries after mutations.

## Avoid
- Importing server code (not just the type) into the client bundle: ships DB code to the browser. Use `import type`.
- Procedures without `.input`: unvalidated `unknown` data. Add a schema.
- Mixing `@trpc/*` majors across packages: type errors and runtime mismatch. Align versions.
- Using `.query` for state-changing actions: they are cached and GET-able. Use `.mutation`.
- Doing authorization only in the UI: check in `protectedProcedure` and per-resource in the handler.
- Returning raw ORM rows with secrets: map to a public shape or use `.output`.
- Putting a per-request DB connection in `initTRPC` instead of context.

## Review
- [ ] All procedures have `.input` schemas.
- [ ] Mutations are mutations; queries have no side effects.
- [ ] Auth middleware covers all non-public procedures; resource ownership is checked.
- [ ] Client imports only `AppRouter` type.
- [ ] Errors use `TRPCError` codes.
