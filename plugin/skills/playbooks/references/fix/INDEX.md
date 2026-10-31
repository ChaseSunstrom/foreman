<!-- Foreman's own index (written for Foreman, not ported). -->
# Fix playbooks

Bugs by kind: the failing thing first, then its stack. Paths are relative to the playbooks skill.

- `references/fix/flaky-tests.md` — A test that passes and fails without a code change: prove, classify, reproduce deterministically, fix.
- `references/fix/sql.md` — Slow or new queries: real SQL, call count, plan on real data, query before index, before/after proof.
- `references/fix/migration.md` — Live schema changes: expand, dual-write, batched backfill, switch reads, contract, lock timeout.
- `references/fix/text-time-bytes.md` — Text, time, bytes, money: encodings, Unicode normalisation, UTC and DST, minor units.
- `references/fix/cli-errors.md` — A CLI crashes, rejects a natural argument shape or acts on more than named: usage errors, many at once.
- `references/fix/data-pipeline.md` — An Airflow, Dagster, dbt or Kafka job fails or writes wrong rows: pin the partition, idempotence test.
- `references/fix/mobile-crash.md` — An iOS, Android, React Native or Flutter app crashes on a device: crash text, release build, lowest test.
- `references/fix/serial-and-bus.md` — Hardware on serial, I2C, CAN or BLE does not answer: prove the link, watch the wire, replay a capture.
