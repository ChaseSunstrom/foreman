---
name: spring-batch
title: Spring Batch
area: jvm
tags: [java, spring, batch, etl, jobs, chunk, restart]
detect: [dep:spring-boot-starter-batch, dep:spring-batch-core, dep:spring-batch-test]
related: [spring-boot, spring-data-jpa, testcontainers, flyway, micrometer]
---
Spring Batch jobs: chunk-oriented steps, restartable job state in a repository database, idempotent readers and writers.

## Verify
- `./gradlew test`: job and step tests pass with `JobLauncherTestUtils`.
- `grep -rn "spring.batch.job.enabled" src/main/resources`: jobs do not auto-run on every app start unless intended.
- `grep -rnE "JobBuilderFactory|StepBuilderFactory" src`: no removed builder factories (Batch 5 uses `JobBuilder` and `StepBuilder` with a `JobRepository`).
- `./gradlew test --tests "*JobTest"`: restart and failure scenarios run in isolation.

## Test first
`spring-batch-test` with `@SpringBatchTest`. Use unique job parameters per run.
```java
@SpringBatchTest
@SpringBootTest
class ImportJobTest {
  @Autowired JobLauncherTestUtils utils;

  @Test void badRowIsSkippedAndCounted() throws Exception {
    var params = new JobParametersBuilder()
        .addString("file", "bad-row.csv").toJobParameters();
    JobExecution ex = utils.launchJob(params);
    assertThat(ex.getStatus()).isEqualTo(BatchStatus.COMPLETED);
    assertThat(ex.getStepExecutions().iterator().next().getSkipCount()).isEqualTo(1);
  }
}
```

## Do
- Build with `new JobBuilder("name", jobRepository)` and `new StepBuilder("step", jobRepository).<In,Out>chunk(100, txManager)` (Batch 5 API).
- Make processors pure and writers idempotent (upsert by key) so restarts and retries are safe.
- Configure `faultTolerant()` with explicit `skip(Class)`, `skipLimit`, `retry(Class)`, `retryLimit`; never skip everything.
- Pass identifying `JobParameters` (date, file name); a completed instance with the same parameters will not rerun.
- Use `@StepScope` and `@Value("#{jobParameters['x']}")` for per-run inputs.
- Use a persistent `JobRepository` datasource in production; set a chunk size from measurement, not habit.
- For parallelism use partitioning or multi-threaded steps only with thread-safe readers (`JdbcPagingItemReader`, not cursor readers).
- Add `JobExecutionListener` metrics and alert on `FAILED` status.

## Avoid
- `JobBuilderFactory` and `StepBuilderFactory` from older tutorials: removed in Batch 5. Use the builders above.
- `@EnableBatchProcessing` on Boot 3 without need: it switches off Boot's auto-configuration. Drop it unless customizing deliberately.
- Rerunning with identical parameters and expecting work: `JobInstanceAlreadyCompleteException`. Add a run id parameter.
- Non-thread-safe `JdbcCursorItemReader` in a multi-threaded step: duplicated or lost rows. Use paging readers or `SynchronizedItemStreamReader`.
- In-memory H2 job repository in production: restart state is lost. Use the real database.
- Doing external side effects (HTTP, email) in a processor: replays on retry. Move to an idempotent writer.

## Review
- [ ] Each step is restartable, or explicitly marked `allowStartIfComplete`/not restartable with a reason.
- [ ] Skip and retry policies list exact exceptions and limits.
- [ ] Writers are idempotent; chunk transactions are sized deliberately.
- [ ] Job parameters identify the run and no secrets are placed in them.
- [ ] Tests cover happy path, skip, failure and restart.
