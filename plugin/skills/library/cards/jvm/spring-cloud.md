---
name: spring-cloud
title: Spring Cloud
area: jvm
tags: [java, spring, microservices, gateway, config, discovery, openfeign]
detect: [dep:spring-cloud-dependencies, dep:spring-cloud-starter-gateway, dep:spring-cloud-starter-config, dep:spring-cloud-starter-openfeign, dep:spring-cloud-starter-netflix-eureka-client, dep:spring-cloud-starter-loadbalancer, dep:spring-cloud-starter-stream-kafka]
related: [spring-boot, spring-webflux, resilience4j, micrometer, spring-security, spring-boot-testing]
---
Spring Cloud for Spring Boot services: Gateway, Config, discovery, OpenFeign, load balancing, with a release train that must match the Boot line.

## Verify
- `./gradlew dependencies --configuration runtimeClasspath | grep -i spring-cloud`: every module resolves from one BOM version.
- `./gradlew test`: context loads with cloud features enabled or stubbed.
- `curl -s localhost:8080/actuator/gateway/routes`: gateway routes loaded (needs the gateway actuator endpoint exposed).
- `curl -s localhost:8080/actuator/health`: config client and discovery health indicators are UP.

## Test first
Run with discovery and config disabled; stub downstream with WireMock or MockWebServer.
```java
@SpringBootTest(properties = {
  "spring.cloud.config.enabled=false",
  "eureka.client.enabled=false",
  "spring.cloud.discovery.enabled=false"})
class RoutesTest {
  @Autowired RouteLocator routes;
  @Test void ordersRouteExists() {
    var ids = routes.getRoutes().map(Route::getId).collectList().block();
    assertThat(ids).contains("orders");
  }
}
```

## Do
- Import the release train through the `spring-cloud-dependencies` BOM (`dependencyManagement` in Maven, `platform(...)` or the dependency-management plugin in Gradle) and leave module versions unset.
- Match the train to the Boot minor version using the compatibility table in the Spring Cloud docs.
- Use `spring.config.import=optional:configserver:` for the config client, not the removed bootstrap context, unless `spring-cloud-starter-bootstrap` is added deliberately.
- Use Spring Cloud LoadBalancer with `@LoadBalanced` clients; Ribbon is gone.
- Set timeouts on Feign (`spring.cloud.openfeign.client.config.default.connect-timeout` and `read-timeout`) and add a circuit breaker.
- Define gateway routes with predicates and filters in YAML or `RouteLocatorBuilder`; apply auth and rate limiting at the gateway and still verify tokens downstream.
- Secure config server and actuator endpoints; encrypt secrets (`{cipher}`) or use Vault.

## Avoid
- Mixing release-train and Boot versions: `NoSuchMethodError` or auto-config failures at startup. Align them via the BOM table.
- `bootstrap.yml` on a modern setup: ignored without the bootstrap starter. Use `spring.config.import`.
- Ribbon, Hystrix, Zuul 1 snippets from old tutorials: removed. Use LoadBalancer, Resilience4j, Gateway.
- Spring Cloud Gateway with `spring-boot-starter-web` present: Gateway is reactive and fails to start. Remove the servlet starter (or use the MVC gateway variant deliberately).
- Gateway routes without timeouts: hung upstreams exhaust connections. Set `spring.cloud.gateway.httpclient.connect-timeout` and `response-timeout`.
- Exposing `/actuator/env` or `/actuator/refresh` publicly: leaks config. Restrict `management.endpoints.web.exposure.include` and secure it.

## Review
- [ ] One BOM governs all Spring Cloud versions and matches the Boot version.
- [ ] Every remote call has timeout, retry bound and circuit breaker.
- [ ] Config client import is explicit, with `optional:` only where startup must survive an outage.
- [ ] Gateway filters do not trust client-supplied identity headers.
- [ ] Tests run without a live config server or registry.
