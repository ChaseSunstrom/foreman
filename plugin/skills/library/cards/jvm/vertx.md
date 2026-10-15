---
name: vertx
title: Eclipse Vert.x
area: jvm
tags: [java, kotlin, vertx, reactive, event-loop, verticles, async]
detect: [dep:vertx-core, dep:vertx-web, dep:vertx-junit5, dep:vertx-web-client, dep:vertx-lang-kotlin-coroutines]
related: [kotlin-coroutines, junit5, testcontainers, micrometer, ktor]
---
Vert.x applications: verticles on event loops, non-blocking handlers, futures, and `executeBlocking` or worker verticles for anything that blocks.

## Verify
- `./gradlew test`: tests with `VertxExtension` pass.
- `mvn -q test`: the same on Maven.
- `java -Dvertx.options.blockedThreadCheckInterval=1000 -jar app.jar`: the blocked-thread checker logs warnings when a handler blocks the event loop.
- `grep -rnE "Thread\.sleep|\.get\(\)|\.join\(\)" src/main`: blocking calls in verticle code.

## Test first
`vertx-junit5` gives `VertxExtension` and `VertxTestContext`; always complete the context.
```java
@ExtendWith(VertxExtension.class)
class ApiTest {
  @Test void healthReturnsOk(Vertx vertx, VertxTestContext ctx) {
    vertx.deployVerticle(new MainVerticle()).compose(id ->
        WebClient.create(vertx).get(8080, "localhost", "/health").send())
      .onComplete(ctx.succeeding(r -> ctx.verify(() -> {
        assertEquals(200, r.statusCode());
        ctx.completeNow();
      })));
  }
}
```

## Do
- Keep handlers non-blocking; hand off to `vertx.executeBlocking(...)` or deploy a worker verticle (`DeploymentOptions().setThreadingModel(ThreadingModel.WORKER)` in 4.5+, `setWorker(true)` earlier).
- Compose with `Future` (`compose`, `map`, `recover`, `Future.all`/`CompositeFuture.all`); every future gets a failure path.
- Route with `Router.router(vertx)`, add `BodyHandler.create()` before reading bodies, and a failure handler: `router.route().failureHandler(...)`.
- Configure through `ConfigRetriever` or env, not constants; pass a `JsonObject` config to deployments.
- Scale with multiple verticle instances (`setInstances(n)`), sharing no mutable state; use the event bus or `SharedData` for communication.
- Close clients and servers in `stop()` and return a completed future.
- Kotlin: use `vertx-lang-kotlin-coroutines` with `CoroutineVerticle` and `awaitResult`.
- Validate input at the edge (`vertx-web-validation`) and set request timeouts.

## Avoid
- Blocking the event loop (JDBC, `Thread.sleep`, `future.get()`): everything on that loop stalls. Use async clients or `executeBlocking`.
- Forgetting `ctx.completeNow()` or `failNow(...)` in tests: they time out. Complete in every branch.
- Reading the body without `BodyHandler`: null body. Register it first.
- Swallowing failed futures: silent errors. Always attach `onFailure` or return the future.
- Sharing mutable objects across verticles: data races. Copy, or message-pass immutable data.
- Mixing Vert.x major versions across modules (`vertx-core` 4.x with 5.x modules): linkage errors. Use the `vertx-stack-depchain` BOM.
- Callback style `Handler<AsyncResult>` in new code: nested and error-prone. Prefer `Future` returns.

## Review
- [ ] No blocking calls on event-loop threads; blocking work is isolated.
- [ ] Every future chain ends in handled failure; routes have a failure handler.
- [ ] Tests always complete or fail their `VertxTestContext`.
- [ ] Resources are closed in `stop`; versions come from one BOM.
- [ ] Config is external and request inputs are validated.
