---
name: akka-pekko
title: Akka and Apache Pekko
area: jvm
tags: [scala, java, actors, akka, pekko, streams]
detect: [dep:akka-actor-typed, dep:akka-actor, dep:akka-stream, dep:pekko-actor-typed, dep:pekko-stream, dep:pekko-http]
related: [sbt, kotlin-coroutines, gradle, testcontainers]
---
Akka and Apache Pekko typed actors, streams and HTTP: message protocols, supervision, ask patterns, TestKit.

## Verify
- `sbt test` (or `./gradlew test`): actor and stream tests pass.
- `sbt "testOnly *CounterSpec"`: one spec runs while iterating.
- `sbt dependencyTree | grep -E "akka|pekko"`: one version across all modules; no mixed `akka-*` and `pekko-*`.
- `sbt "runMain Main"`: the system boots and logs the expected startup lines.

## Test first
Use `ActorTestKit` with a `TestProbe`; the protocol is the contract.
```scala
class CounterSpec extends ScalaTestWithActorTestKit with AnyWordSpecLike {
  "Counter" should {
    "reply with the new total" in {
      val counter = spawn(Counter())
      val probe = createTestProbe[Counter.Total]()
      counter ! Counter.Add(2, probe.ref)
      probe.expectMessage(Counter.Total(2))
    }
  }
}
```
Pekko uses the same names under `org.apache.pekko`.

## Do
- Use typed actors (`Behavior[Command]`) with a sealed trait protocol; carry `replyTo: ActorRef[Reply]` in requests.
- Keep actor state in the behavior's closure or parameters and return the next `Behavior`.
- Never block inside an actor: run blocking work in a Future on a dedicated dispatcher (`pekko.actor.default-blocking-io-dispatcher`).
- Use `context.ask` or `pipeToSelf` to combine Futures with actor state.
- Supervise with `Behaviors.supervise(...).onFailure(SupervisorStrategy.restart.withLimit(...))`.
- Use persistence or cluster sharding only with serializers configured explicitly (Jackson CBOR or Protobuf), not Java serialization.
- Pick Pekko for new projects when the licence of recent Akka versions is a concern for you; check your organization's rules.

## Avoid
- Classic untyped actors (`Actor` with `receive` and `sender()`) in new code: use typed behaviors.
- Closing over mutable actor state in a Future callback: a race. Send the result back as a message.
- `Await.result` in actors or routes: blocks threads. Compose Futures or use `pipeToSelf`.
- Java serialization for cluster messages: insecure and fragile. Use a defined serializer and `serialization-bindings`.
- Unbounded mailboxes and unbounded streams: set stream buffers and backpressure with `buffer(..., OverflowStrategy.backpressure)`.
- Mixing Akka and Pekko artifacts: conflicting classes at runtime.
- `Thread.sleep` in tests: use `probe.expectMessage` and `awaitAssert`.

## Review
- [ ] Protocols are sealed and include reply addresses.
- [ ] No blocking calls on the default dispatcher.
- [ ] Failure handling is explicit through supervision or stream `recover`.
- [ ] Serialization bindings are configured for remote or persisted messages.
- [ ] Dependency versions are aligned and from one family.
