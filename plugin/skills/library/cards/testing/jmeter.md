---
name: jmeter
title: Apache JMeter
area: testing
tags: [testing, load, performance, jmx, http, java, benchmark]
detect: [file:*.jmx, dep:jmeter-maven-plugin, dep:ApacheJMeter_core, dep:org.apache.jmeter*]
related: [gatling, k6, locust, performance-regression]
---
JMeter: GUI-authored .jmx plans that must be run headless in CI with assertions, a CSV data source and a results file.

## Verify
- `jmeter -n -t plan.jmx -l results.jtl -e -o report/`: headless run, raw results, HTML dashboard.
- `jmeter -n -t plan.jmx -l results.jtl -Jhost=localhost -Jthreads=20`: properties override the plan values.
- `jmeter -g results.jtl -o report/`: regenerates the report from an existing results file.
- `grep -c ',false,' results.jtl`: counts failed samples (success column false) in the default CSV output.

## Test first
Assertions are the red test. Add a response assertion and a duration assertion before scaling threads.
```xml
<ResponseAssertion testname="status is 201">
  <collectionProp name="Asserion.test_strings"><stringProp name="1">201</stringProp></collectionProp>
  <stringProp name="Assertion.test_field">Assertion.response_code</stringProp>
  <intProp name="Assertion.test_type">8</intProp>
</ResponseAssertion>
<DurationAssertion testname="under 500ms">
  <stringProp name="DurationAssertion.duration">500</stringProp>
</DurationAssertion>
```
Run it with `-n`, then check the `.jtl` for failures.

## Do
- Parameterize host, port, threads, ramp and duration with `${__P(name,default)}`.
- Drive users from a CSV Data Set Config; set recycle and stop-thread behavior on EOF explicitly.
- Extract tokens with a JSON Extractor and reuse them in later samplers.
- Add a Constant Timer or Gaussian Random Timer for realistic think time.
- Use ramp-up so servers warm and the first seconds do not dominate.
- Keep the `.jmx` small and versioned; move shared logic into Test Fragments.
- Fail CI by parsing the `.jtl` (error rate, p95) because JMeter itself exits 0 on failed samples.

## Avoid
- Running load from the GUI: it consumes the CPU you are measuring. Use `-n` only.
- Leaving View Results Tree or listeners enabled in load runs: memory blowup. Disable them and write to `.jtl`.
- No assertions: every 500 page counts as a sample. Add response assertions.
- Hard-coded tokens or sessions in the plan: runs fail after expiry. Extract per user.
- Running generator and target on one machine: skewed results. Separate them.
- Checking in a plan with real credentials: use properties and env.

## Review
- [ ] Runs headless with a documented command.
- [ ] Assertions exist and CI parses the results for failure thresholds.
- [ ] Data and thresholds are parameterized, not baked in.
- [ ] No heavy listeners in the committed plan.
- [ ] No secrets in the `.jmx`.
