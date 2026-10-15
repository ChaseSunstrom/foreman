---
name: flink
title: Apache Flink
area: data
tags: [flink, streaming, state, checkpoints, watermarks, exactly-once]
detect: [dep:apache-flink, dep:flink-streaming-java]
related: [kafka, apache-beam, spark]
---
Flink streaming jobs: event time and watermarks, keyed state with TTL, checkpointing and tested operators.

## Verify
- `flink run -d job.jar`: submits detached; the job appears in `flink list`.
- `flink list`: job is RUNNING, not restarting.
- `curl -s localhost:8081/jobs/<jobid>/checkpoints`: completed checkpoints, duration and size; failures count is 0.
- `flink savepoint <jobid> <dir>`: a savepoint can be taken, needed before upgrades.

## Test first
Use the harness for operators and the mini cluster for pipelines.
```java
@Test void dedupesByKey() throws Exception {
  var h = ProcessFunctionTestHarnesses.forKeyedProcessFunction(
      new Dedup(), e -> e.id, Types.STRING);
  h.processElement(new Event("a"), 1L);
  h.processElement(new Event("a"), 2L);
  assertEquals(1, h.extractOutputValues().size());
}
```
Pipelines: `MiniClusterWithClientResource` and a collecting sink.

## Do
- Use event time with `WatermarkStrategy.forBoundedOutOfOrderness(Duration.ofSeconds(n))` plus `withIdleness` for idle partitions.
- Enable checkpoints (`env.enableCheckpointing(ms)`), set a state backend (RocksDB for large state) and durable checkpoint storage.
- Give every stateful operator a stable `uid("name")` so savepoints restore after code changes.
- Set state TTL (`StateTtlConfig`) on keyed state that would otherwise grow without bound.
- Choose the key to spread load; watch for hot keys.
- End-to-end exactly-once needs a transactional or idempotent sink (Kafka sink with `DeliveryGuarantee.EXACTLY_ONCE`, upsert keys).
- Set a restart strategy explicitly (fixed delay or exponential delay).
- Set `setParallelism` to at most the source partition count.

## Avoid
- Processing-time windows where results must be reproducible: use event time.
- No `uid()` on operators: topology change breaks savepoint restore.
- Idle source partitions without idleness: the watermark never advances and windows never fire.
- Blocking calls or heavy I/O in `map`: backpressure. Use `AsyncDataStream`.
- Unbounded state in `ValueState` or `MapState` with no TTL or timer cleanup: the job dies on disk or memory.
- Non-serializable fields in functions: closure serialization failures. Use `transient` and `open()`.
- Deprecated `FlinkKafkaConsumer`: use `KafkaSource`.

## Review
- [ ] Watermark strategy and lateness handling stated.
- [ ] State has TTL or cleanup; uids set.
- [ ] Checkpoint interval, storage and restart strategy configured.
- [ ] Sink semantics match the stated delivery guarantee.
- [ ] Savepoint upgrade path tested.
