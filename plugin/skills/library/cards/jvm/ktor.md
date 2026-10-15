---
name: ktor
title: Ktor
area: jvm
tags: [kotlin, ktor, web, api, coroutines, http]
detect: [dep:ktor-server-core, dep:ktor-server-netty, dep:ktor-server-cio, dep:ktor-client-core, dep:io.ktor:ktor-server-core]
related: [kotlin-coroutines, kotlinx-serialization, gradle, junit5, testcontainers]
---
Ktor servers and clients in Kotlin: plugins (content negotiation, status pages, auth), routing DSL, `testApplication`.

## Verify
- `./gradlew test`: route tests run in process through `testApplication`.
- `./gradlew run`: the server boots with the configured engine and modules.
- `curl -si localhost:8080/health`: a liveness route answers before wiring anything else.
- `./gradlew dependencies --configuration runtimeClasspath | grep ktor`: all `ktor-*` artifacts share one version.

## Test first
`testApplication` from `ktor-server-test-host` runs the module without sockets.
```kotlin
class ItemRoutesTest {
  @Test fun blankNameIsRejected() = testApplication {
    application { module() }
    val client = createClient { install(ContentNegotiation) { json() } }
    val r = client.post("/items") {
      contentType(ContentType.Application.Json)
      setBody(ItemIn(name = ""))
    }
    assertEquals(HttpStatusCode.BadRequest, r.status)
  }
}
```

## Do
- Structure the app as `fun Application.module()` extensions grouped by feature; routes in `fun Route.itemRoutes()`.
- Install `ContentNegotiation` with `json()` (kotlinx.serialization) and `StatusPages` that maps exceptions to responses.
- Use `call.receive<T>()` with `@Serializable` types and validate with the `RequestValidation` plugin.
- Authenticate with the `Authentication` plugin (`jwt`, `basic`) and wrap routes in `authenticate("name") { ... }`.
- Read configuration from `application.conf` or `application.yaml` with `environment.config`.
- Share one `HttpClient` per app (closed on `ApplicationStopped`), with a timeout configured.
- Offload blocking work with `withContext(Dispatchers.IO)`.

## Avoid
- Forgetting `ContentNegotiation` on the test client: bodies are not serialized and the call fails with a cryptic error. Install it in `createClient`.
- Blocking calls in handlers on the default dispatcher: stalls other requests. Use `Dispatchers.IO` or async libraries.
- Ktor 1.x idioms (`Features`, `install(Routing)` boilerplate, `embeddedServer` with old DSL): use plugins and the 2.x/3.x APIs.
- A new `HttpClient` per call: leaks connections. Reuse and close.
- Mixing `ktor-*` versions: runtime `NoSuchMethodError`. Use the Ktor BOM or one version variable.
- Returning `Map<String, Any>` as JSON: kotlinx.serialization cannot encode `Any`. Use `@Serializable` types.
- Swallowing exceptions so the response is 200: map them in `StatusPages`.

## Review
- [ ] Routes are covered by `testApplication` tests, including a failure case.
- [ ] Serialization is installed in server and test client.
- [ ] No blocking work on the request coroutine without a dispatcher switch.
- [ ] Auth wraps every non-public route.
- [ ] Clients and resources are closed on shutdown.
