---
name: junit-platform-launcher
title: JUnit Platform Launcher
area: jvm
tags: [java, kotlin, junit, junit-platform, launcher, test-runner, tooling]
detect: [dep:org.junit.platform:junit-platform-launcher]
related: [junit5, junit4, gradle, maven, archunit]
---
`junit-platform-launcher` is the API that build tools, IDEs and custom runners use to discover and run JUnit Platform engines (Jupiter, Vintage) in code.

## Verify
- `./gradlew dependencies --configuration testRuntimeClasspath | grep junit-platform`: the launcher and the Jupiter engine resolve to the same platform version.
- `./mvnw -q dependency:tree | grep junit-platform-launcher`: one launcher version.
- `./gradlew test`: the suite runs and reports a non-zero test count.
- `./gradlew test --tests 'com.example.LauncherTest'`: the launcher-driven test runs alone.

## Test first
Drive the launcher on one class and count what it found. This is a test of the runner code you wrote on top of the launcher.
```java
import static org.junit.jupiter.api.Assertions.assertEquals;
import org.junit.jupiter.api.Test;
import org.junit.platform.launcher.LauncherDiscoveryRequest;
import org.junit.platform.launcher.core.LauncherDiscoveryRequestBuilder;
import org.junit.platform.launcher.core.LauncherFactory;
import org.junit.platform.launcher.listeners.SummaryGeneratingListener;
import static org.junit.platform.engine.discovery.DiscoverySelectors.selectClass;

class LauncherTest {
  @Test void runsOneClassAndCountsIt() {
    LauncherDiscoveryRequest request = LauncherDiscoveryRequestBuilder.request()
        .selectors(selectClass(SampleTest.class)).build();
    SummaryGeneratingListener listener = new SummaryGeneratingListener();
    LauncherFactory.create().execute(request, listener);
    assertEquals(2, listener.getSummary().getTestsFoundCount());
  }
}
```

## Do
- Keep the launcher on the same version as `junit-jupiter` and the platform; they ship together.
- Create the launcher with `LauncherFactory.create()` and reuse it within one run.
- Register a `TestExecutionListener` (such as `SummaryGeneratingListener`) to read results instead of parsing console output.
- Select tests with `DiscoverySelectors` (`selectClass`, `selectPackage`, `selectMethod`) and keep the selection explicit.
- Let the build tool run the main suite; use the launcher only for a custom runner, report or IDE integration.

## Avoid
- Pinning the launcher to one version and the engines to another: discovery finds no tests or the run fails with a linkage error.
- Using the launcher in the test code to run the same tests the build already runs: the tests run twice.
- Ignoring `getFailures()` on the summary: a failed test then exits the runner with success.
- Reading console output to count results: use the summary listener.
- Treating a zero test count as success: check `getTestsFoundCount()` is above zero.
- Adding the launcher for normal tests: Gradle and Maven bring the launcher they need.

## Review
- [ ] The launcher version matches the platform and Jupiter versions.
- [ ] A custom runner reports its counts from the listener, not from console output.
- [ ] A zero-test result fails the check.
- [ ] Tests started by the launcher are not also run by the build tool.
- [ ] The launcher is declared only where a custom runner needs it.
