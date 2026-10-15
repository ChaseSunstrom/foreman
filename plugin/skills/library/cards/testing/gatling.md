---
name: gatling
title: Gatling
area: testing
tags: [testing, load, performance, scala, java, simulation, http]
detect: [dep:gatling-charts-highcharts, dep:io.gatling*, dep:gatling-maven-plugin, file:src/test/scala/*Simulation.scala, file:*Simulation.java]
related: [k6, locust, jmeter, performance-regression, benchmarking]
---
Gatling: code-defined load simulations with an open or closed injection model and assertions that fail the build on SLO breaches.

## Verify
- `mvn gatling:test`: runs the simulations and fails on a broken assertion (Maven plugin).
- `gradle gatlingRun`: the same through the Gradle plugin.
- `sbt Gatling/test`: the same through the sbt plugin.
- `ls target/gatling`: an HTML report directory exists per run, with percentiles and error counts.

## Test first
Write the assertion before the scenario is tuned. A failing SLO is the red test.
```scala
class CheckoutSimulation extends Simulation {
  val http1 = http.baseUrl(sys.props.getOrElse("base", "http://localhost:8080"))
  val scn = scenario("checkout")
    .exec(http("cart").get("/cart").check(status.is(200)))
    .pause(1)
    .exec(http("pay").post("/pay").body(StringBody("""{"a":1}""")).asJson
      .check(status.is(201)))
  setUp(scn.inject(constantUsersPerSec(20).during(60)).protocols(http1))
    .assertions(global.responseTime.percentile(95).lt(400),
                global.failedRequests.percent.lt(1))
}
```

## Do
- Choose the model deliberately: open (`constantUsersPerSec`, `rampUsersPerSec`) for public traffic, closed (`constantConcurrentUsers`) for pooled clients.
- Add `.assertions(...)` on p95/p99 and failure rate so CI exits non-zero.
- Use feeders (`csv(...).circular`) for unique users and ids; extract tokens with `check(...saveAs)`.
- Warm up with a short ramp and exclude it from conclusions.
- Pass base URL and rates by system property so the same simulation runs locally and in CI.
- Run against a production-like environment and record the machine size with the result.
- Keep think time (`pause`) realistic, not zero.

## Avoid
- Judging by averages: they hide tail latency. Assert on percentiles.
- Load generator on the same box as the service: CPU contention skews both. Run it apart.
- Checking only status 200: a 200 with an error body passes. Check body content or a JSON field.
- One hard-coded user for all virtual users: caches make results too good. Use a feeder.
- Huge `.check(bodyString.saveAs)` on every request: memory pressure in the generator. Save only fields needed.
- No assertions, just eyeballing the report: regressions go unnoticed. Add thresholds.

## Review
- [ ] Injection profile matches the real arrival pattern (open vs closed).
- [ ] Assertions on p95/p99 and error rate exist.
- [ ] Feeders supply distinct data; secrets come from env or properties.
- [ ] Checks validate response content, not only status.
- [ ] Target environment and generator sizing are noted.
