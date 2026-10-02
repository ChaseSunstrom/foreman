<!-- Foreman's own playbook (written for Foreman, not ported). -->
# Flaky tests

Use when a test passes and fails without a code change.

1. **Prove it's flaky:** run it 20–50 times in a loop (`for i in $(seq 30); do <cmd> || echo FAIL $i; done`), alone and inside the full suite. Note the failure rate and whether order matters.
2. **Classify** by the failure text: timing (sleeps, timeouts, clocks), order (shared state, globals, temp files, ports, env vars), concurrency (races, unawaited work), environment (network, locale, timezone, filesystem order), randomness (unseeded).
3. **Reproduce deterministically** before fixing: pin the seed, shuffle order with a fixed seed, add a stress loop, or inject the delay that exposes the race.
4. **Fix the cause, not the symptom:** wait on a condition instead of sleeping; give each test its own temp dir/port/DB; reset globals in teardown; await every task; sort what the OS returns unordered; seed randomness.
5. **Never** add a blanket retry or skip as the fix; quarantine (with an issue and an owner) only while the real fix is in progress.
6. **Verify:** the loop from step 1 runs clean at least 3× the original attempts; record the rate before and after as evidence.
